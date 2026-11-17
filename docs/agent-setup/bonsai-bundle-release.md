# Bonsai harness release packaging

The [worker bundles](https://github.com/xaime-vp/agent-and-skills/blob/a701dcf2de332cce285b49c0b7c609f2d75d4328/harnesses/bonsai/README.md) are source assets in `agent-and-skills`. The offline [packager](https://github.com/xaime-vp/agent-and-skills/blob/a701dcf2de332cce285b49c0b7c609f2d75d4328/tools/bonsai_harnesses.py) exports a curated import closure and returns digest-bound resource selection for a trusted Constant Integration consumer. It never edits the product checkout, installs a worker, starts a task or modifies a sealed release.

## Check, export, verify and select

Run from the workspace root with Python 3.11+; the Constant Integration product still requires its own supported Python version.

```sh
python tools/bonsai_harnesses.py check
python tools/bonsai_harnesses.py export --output /existing/staging/bonsai-bundle
python tools/bonsai_harnesses.py verify --bundle /existing/staging/bonsai-bundle
```

The output directory must be new and its parent must exist. Existing directories, linked assets/destinations, malformed manifests and missing imports are rejected. `--role coder` (repeatable) exports a subset; omission exports all four model-driven roles. Only runtime extensions, manifests, selected method skills and shared modules are copied. Tests, node_modules, README files, credentials and developer extensions are excluded. The output has no host paths or timestamps, so identical source produces identical bytes and content digest.

Keep the `content_sha256` from an independently trusted export/review record. It hashes the canonical file records, which include every curated path, byte count and SHA-256. Verify that expected value and select one role:

```sh
python tools/bonsai_harnesses.py verify --bundle /existing/staging/bonsai-bundle --expected-digest TRUSTED_64_HEX_DIGEST
python tools/bonsai_harnesses.py select --bundle /existing/staging/bonsai-bundle --role reviewer --expected-digest TRUSTED_64_HEX_DIGEST
```

Replace `TRUSTED_64_HEX_DIGEST` with the recorded digest. Selection returns explicit additive `--extension`/`--skill` arguments, six `additional_tools`, the required base extension, context environment name and selected file evidence. It does not emit or run a complete launch command. The supervisor still selects native tools and must preserve the sealed profile, base guard, isolated discovery and role restrictions. Selection always reports `activation_observed: false`.

Self-contained hashes detect corruption, not authenticity. Without an independently trusted digest, `verify` only proves consistency with the files' own index. Runtime integration must verify the product release manifest as well. Do not fetch bundles from an issue, task worktree or untrusted path.

## Product adapter requirements

Use the [release consumption contract](https://github.com/xaime-vp/agent-and-skills/blob/a701dcf2de332cce285b49c0b7c609f2d75d4328/harnesses/bonsai/README.md#release-consumption-contract).
Current product source integrates the bundles through `harness_resources.py`,
verified resource staging and explicit `harness_roles` selection; see the
[capability map](platform-capabilities.md#selective-pi-role-harnesses-integrated-in-source)
for the currently vendored revision/digest. An older installation may lack this
adapter. Preserve explicit arguments, allowlisted tools and read-scope guards
when updating it. A changed method skill requires a new reviewed export,
product-side pinned bundle refresh and sealed release; updating this repository
does not update a running worker.

Native `bonsai_call_agent` is a separate supervisor-selected runtime capability,
not a seventh helper to register in the coder manifest. See
[repository consultation](repository-consultation.md) for policy, eligibility
and no-shell restrictions. Keep the six read-only helper tools unchanged.

Keep the existing supervisor approval/admission, protected checks, identity/environment, process-stop confirmation, frozen-source review and Git/publication paths. There is no model supervisor bundle, no worker GitHub MCP and no worker-controlled tool loader. A reviewer gets no shell or writes and must preserve the supervisor-selected legacy/v2 report schema. Documentation still has no embedded reviewer. Rollback means selecting the prior sealed release/resources; never modify an installed release in place.

## Verification

```sh
npm ci --prefix harnesses/bonsai --ignore-scripts --no-audit --no-fund
npm test --prefix harnesses/bonsai
python -m unittest tools.test_bonsai_harnesses
node --test .pi/extensions/*.test.mjs
```

The packaging tests cover reproducibility, exact role/tool manifests, import closure, tampering, unexpected entries, linked assets, missing resources, strict JSON and mandatory digest-bound selection.

For a real host-loader check, point at a separately installed trusted Pi CLI bundle. Use Node 22.19+ and an export of all four roles:

```sh
node tools/smoke_bonsai_pi.mjs --pi-cli /trusted/pi/dist/bundle/cli.js --bundle /existing/staging/bonsai-bundle
```

The smoke test starts temporary, isolated RPC processes, loads each exported role and checks the registered/active tool names. It sends only `get_state`, never a model prompt, and removes its temporary state. CI runs this against Pi 1.5.0, the observed product pin. Local verification additionally used cached Pi 1.5.2. The [CI workflow](https://github.com/xaime-vp/agent-and-skills/blob/a701dcf2de332cce285b49c0b7c609f2d75d4328/.github/workflows/bonsai-harnesses.yml) checks the exported closure rather than relying on workspace dependency resolution. Neither loader success nor offline tests prove installed admission, protected validation, review verdicts or live delivery.
