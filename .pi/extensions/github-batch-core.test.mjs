import test from "node:test";
import assert from "node:assert/strict";
import os from "node:os";
import path from "node:path";
import fs from "node:fs/promises";
import { spawn } from "node:child_process";
import {buildStagedPlan, parseStatusNul, matchingOrigin, publishStagedPlan, boundedSummary, validateRequest} from "./github-batch-core.mjs";

async function git(cwd, args) {
  return await new Promise(resolve => {
    const p = spawn("git", ["-C", cwd, ...args], {stdio:["ignore","pipe","pipe"]});
    let stdout = "", stderr = "";
    p.stdout.setEncoding("utf8"); p.stdout.on("data", v => stdout += v);
    p.stderr.setEncoding("utf8"); p.stderr.on("data", v => stderr += v);
    p.on("close", code => resolve({code,stdout,stderr}));
  });
}

async function fixture(fn) {
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), "batch-publish-"));
  try {
    for (const args of [["init","-b","feature"],["config","user.name","Test"],["config","user.email","test@example.invalid"],["remote","add","origin","git@github.com:xaime-vp/test-repo.git"]]) {
      assert.equal((await git(dir,args)).code, 0);
    }
    await fs.writeFile(path.join(dir,"a.txt"),"before\n");
    await fs.writeFile(path.join(dir,"delete.txt"),"delete\n");
    for (const args of [["add","."],["commit","-m","base"]]) assert.equal((await git(dir,args)).code,0);
    const sha = (await git(dir,["rev-parse","HEAD"])).stdout.trim();
    await fs.writeFile(path.join(dir,"a.txt"),"after\n");
    await fs.writeFile(path.join(dir,"new file.txt"),"new\n");
    await fs.unlink(path.join(dir,"delete.txt"));
    assert.equal((await git(dir,["add","-A"])).code,0);
    await fn({dir,sha,runGit: args => git(dir,args)});
  } finally { await fs.rm(dir,{recursive:true,force:true}); }
}

test("status parser and origin validation", () => {
  assert.deepEqual(parseStatusNul("M\0a.txt\0D\0b.txt\0"), [{status:"M",path:"a.txt"},{status:"D",path:"b.txt"}]);
  assert.throws(() => parseStatusNul("R100\0a\0b\0"));
  assert.equal(matchingOrigin("git@github.com:xaime-vp/test-repo.git","xaime-vp/test-repo"),true);
  assert.equal(matchingOrigin("https://github.com/other/repo","xaime-vp/test-repo"),false);
  assert.throws(() => validateRequest({repositoryFullName:"wrong",branch:"main",expectedHeadSha:"abc",paths:["x"]}));
});

test("reads explicit staged changes, not unstaged worktree content", async () => {
  await fixture(async ({dir,sha,runGit}) => {
    await fs.writeFile(path.join(dir,"a.txt"),"unrelated worktree edits\n");
    const plan = await buildStagedPlan({runGit,repositoryFullName:"xaime-vp/test-repo",branch:"feature",expectedHeadSha:sha,paths:["a.txt","new file.txt","delete.txt"],includeContent:true});
    assert.deepEqual(plan.entries.map(e=>e.status),["M","A","D"]);
    assert.equal(plan.entries[0].content,"after\n");
    assert.equal(plan.entries[1].content,"new\n");
    assert.equal(plan.entries[2].content,undefined);
    assert.match(plan.baseTreeSha,/^[a-f0-9]{40}$/);
  });
});

test("refuses incorrect head, repository, unstaged path, traversal and symlinks", async () => {
  await fixture(async ({dir,sha,runGit}) => {
    const base={runGit,repositoryFullName:"xaime-vp/test-repo",branch:"feature",expectedHeadSha:sha,paths:["a.txt"]};
    await assert.rejects(buildStagedPlan({...base,expectedHeadSha:"a".repeat(40)}),/Local HEAD/);
    await assert.rejects(buildStagedPlan({...base,repositoryFullName:"evil/other"}),/Local origin/);
    await assert.rejects(buildStagedPlan({...base,paths:["nothing.txt"]}),/not staged/);
    await assert.rejects(buildStagedPlan({...base,paths:["../a.txt"]}),/Invalid staged path/);
    await fs.symlink("a.txt", path.join(dir,"link"));
    await git(dir,["add","link"]);
    await assert.rejects(buildStagedPlan({...base,paths:["link"]}),/Unsupported staged file mode/);
  });
});

test("uploads blobs and creates tree/commit before lease-checked ref mutation", async () => {
  await fixture(async ({sha,runGit}) => {
    const plan=await buildStagedPlan({runGit,repositoryFullName:"xaime-vp/test-repo",branch:"feature",expectedHeadSha:sha,paths:["a.txt","new file.txt","delete.txt"],includeContent:true});
    plan.commitMessage="batch commit";
    const calls=[];
    const result=await publishStagedPlan({plan,prNumber:123,execute:async (name,args) => {
      calls.push({name,args});
      if (name==="get_pr_info") return {content:[{type:"text",text:JSON.stringify({result:{head:"feature",head_sha:sha,head_repo_full_name:"xaime-vp/test-repo",state:"open"}})}]};
      if (name==="update_ref") return {content:[{type:"text",text:JSON.stringify({result:{success:true}})}]};
      return {content:[{type:"text",text:JSON.stringify({result:{sha:(name==="create_commit"?"c":"a").repeat(40)}})}]};
    }});
    assert.equal(result.newHead,"c".repeat(40));
    assert.deepEqual(calls.map(x=>x.name),["get_pr_info","create_blob","create_blob","create_tree","create_commit","get_pr_info","update_ref"]);
    assert.deepEqual(calls.find(x=>x.name==="create_tree").args.tree_elements[2],{path:"delete.txt",mode:"100644",type:"blob",sha:null});
    assert.deepEqual(calls.at(-1).args,{repository_full_name:"xaime-vp/test-repo",branch_name:"feature",sha:"c".repeat(40),force:false,expected_sha:sha});
  });
});

test("stops before uploading when PR revision changed", async () => {
  await fixture(async ({sha,runGit}) => {
    const plan=await buildStagedPlan({runGit,repositoryFullName:"xaime-vp/test-repo",branch:"feature",expectedHeadSha:sha,paths:["a.txt"],includeContent:true});
    plan.commitMessage="test";
    const calls=[];
    await assert.rejects(publishStagedPlan({plan,prNumber:1,execute:async name => {
      calls.push(name);
      if (name==="get_pr_info") return {content:[{type:"text",text:JSON.stringify({result:{head:"feature",head_sha:"f".repeat(40),head_repo_full_name:"xaime-vp/test-repo",state:"open"}})}]};
      throw new Error("unexpected");
    }}),/PR head/);
    assert.deepEqual(calls,["get_pr_info"]);
  });
});

test("limits output text, not uploaded file contents", () => {
  const output = boundedSummary("abc".repeat(5000),150);
  assert.ok(Buffer.byteLength(output,"utf8") <= 450);
  assert.match(output,/truncated/i);
});
