/**
 * Bonsai Podman Tools - Pi extension wrapping .agents/skills/bonsai-containers/scripts/podman_wsl.py
 * for read-only inspection/status/logs and safe build/stop operations in podman-machine-default.
 */

import path from "node:path";
import { Type } from "@earendil-works/pi-ai";
import { defineTool, type ExtensionAPI } from "@earendil-works/pi-coding-agent";

const SAFE_NAME = /^[A-Za-z0-9][A-Za-z0-9_.:/-]*$/;
const SAFE_SUFFIX = /^[A-Za-z0-9._-]+$/;
const PODMAN_WSL_SCRIPT = path.join(".agents", "skills", "bonsai-containers", "scripts", "podman_wsl.py");

type ExecFn = (
	command: string,
	args: string[],
	cwd: string,
	signal?: AbortSignal,
) => Promise<{ stdout: string; stderr: string; code: number }>;

let piExecRef: ExecFn;

async function runPodmanWsl(args: string[], cwd: string, signal?: AbortSignal): Promise<string> {
	const scriptPath = path.resolve(cwd, PODMAN_WSL_SCRIPT);
	const res = await piExecRef("py", ["-3", scriptPath, ...args], cwd, signal);
	const output = [res.stdout, res.stderr].filter(Boolean).join("\n").trim();
	if (res.code !== 0) {
		throw new Error(`podman_wsl.py ${args[0] ?? ""} failed (exit ${res.code}):\n${output}`);
	}
	return output;
}

const inspectWorkersTool = defineTool({
	name: "bonsai_inspect_workers",
	label: "Bonsai Inspect Workers",
	description:
		"Read-only inventory of Bonsai Podman containers, images, bound target repositories, and volumes in podman-machine-default.",
	parameters: Type.Object({}),

	async execute(_toolCallId, _params, signal, _onUpdate, ctx) {
		const output = await runPodmanWsl(["inspect"], ctx.cwd, signal);
		return {
			content: [{ type: "text", text: output || "No containers found." }],
			details: {},
		};
	},
});

const taskStatusTool = defineTool({
	name: "bonsai_task_status",
	label: "Bonsai Task Status",
	description:
		"Read-only status check for a Bonsai worker container: live task slots, state.db, release_root, and progress-*.jsonl without exposing secrets.",
	parameters: Type.Object({
		container: Type.Optional(
			Type.String({
				description: "Container name (default: bonsai-ui-worker)",
			}),
		),
		issue: Type.Optional(
			Type.Number({
				description: "Filter by GitHub issue number",
			}),
		),
		key: Type.Optional(
			Type.String({
				description: "Filter by task key",
			}),
		),
		tail: Type.Optional(
			Type.Number({
				description: "Number of recent events/progress lines per task",
			}),
		),
	}),

	async execute(_toolCallId, params, signal, _onUpdate, ctx) {
		const container = params.container ?? "bonsai-ui-worker";
		if (!SAFE_NAME.test(container)) {
			throw new Error(`Invalid container name: ${container}`);
		}
		if (params.key && !SAFE_NAME.test(params.key)) {
			throw new Error(`Invalid task key: ${params.key}`);
		}
		const args = ["task-status", container];
		if (params.issue !== undefined) args.push("--issue", String(params.issue));
		if (params.key) args.push("--key", params.key);
		if (params.tail !== undefined) args.push("--tail", String(params.tail));

		const output = await runPodmanWsl(args, ctx.cwd, signal);
		return {
			content: [{ type: "text", text: output || "No task status output." }],
			details: { container, issue: params.issue ?? null, key: params.key ?? null },
		};
	},
});

const workerLogsTool = defineTool({
	name: "bonsai_worker_logs",
	label: "Bonsai Worker Logs",
	description:
		"Read-only tail of container logs or /var/lib/bonsaiworker/private/controller.log for a Bonsai worker container.",
	parameters: Type.Object({
		container: Type.Optional(
			Type.String({
				description: "Container name (default: bonsai-ui-worker)",
			}),
		),
		tail: Type.Optional(
			Type.Number({
				description: "Number of trailing lines",
			}),
		),
		controller: Type.Optional(
			Type.Boolean({
				description: "Read controller.log instead of podman logs (default: false)",
			}),
		),
	}),

	async execute(_toolCallId, params, signal, _onUpdate, ctx) {
		const container = params.container ?? "bonsai-ui-worker";
		if (!SAFE_NAME.test(container)) {
			throw new Error(`Invalid container name: ${container}`);
		}
		const args = ["logs", container];
		if (params.tail !== undefined) args.push("--tail", String(params.tail));
		if (params.controller) args.push("--controller");

		const output = await runPodmanWsl(args, ctx.cwd, signal);
		return {
			content: [{ type: "text", text: output || "(no log lines)" }],
			details: { container, controller: Boolean(params.controller), tail: params.tail ?? null },
		};
	},
});

const buildImageTool = defineTool({
	name: "bonsai_build_image",
	label: "Bonsai Build Image",
	description:
		"Build a Bonsai worker Podman image in podman-machine-default from a local repo checkout (defaults to constant-integration).",
	parameters: Type.Object({
		repoPath: Type.Optional(
			Type.String({
				description: "Path to the constant-integration checkout (default: constant-integration)",
			}),
		),
		tag: Type.Optional(
			Type.String({
				description: "Image tag (default: localhost/bonsai-worker:main-<shortsha>)",
			}),
		),
		runCheck: Type.Optional(
			Type.Boolean({
				description: "Run `podman run --rm <tag> check` after building (default: false)",
			}),
		),
	}),

	async execute(_toolCallId, params, signal, _onUpdate, ctx) {
		if (params.tag && !SAFE_NAME.test(params.tag)) {
			throw new Error(`Invalid image tag: ${params.tag}`);
		}
		const args = ["build"];
		if (params.repoPath) args.push("--repo", params.repoPath);
		if (params.tag) args.push("--tag", params.tag);
		if (params.runCheck) args.push("--check");

		const output = await runPodmanWsl(args, ctx.cwd, signal);
		return {
			content: [{ type: "text", text: output || "Image built." }],
			details: { repoPath: params.repoPath ?? "constant-integration", tag: params.tag ?? "auto", runCheck: Boolean(params.runCheck) },
		};
	},
});

const stopWorkerTool = defineTool({
	name: "bonsai_stop_worker",
	label: "Bonsai Stop Worker",
	description:
		"Safely stop a running Bonsai worker container in podman-machine-default (checks for active tasks first, optional backup rename).",
	parameters: Type.Object({
		container: Type.Optional(
			Type.String({
				description: "Container name (default: bonsai-ui-worker)",
			}),
		),
		backupSuffix: Type.Optional(
			Type.String({
				description: "If provided, rename the stopped container to <container>-before-<backupSuffix>",
			}),
		),
		force: Type.Optional(
			Type.Boolean({
				description: "Stop even if active task_process/pi/check.py processes are running (default: false)",
			}),
		),
	}),

	async execute(_toolCallId, params, signal, _onUpdate, ctx) {
		const container = params.container ?? "bonsai-ui-worker";
		if (!SAFE_NAME.test(container)) {
			throw new Error(`Invalid container name: ${container}`);
		}
		if (params.backupSuffix && !SAFE_SUFFIX.test(params.backupSuffix)) {
			throw new Error(`Invalid backupSuffix: ${params.backupSuffix}`);
		}
		const args = ["stop", container];
		if (params.backupSuffix) args.push("--backup-suffix", params.backupSuffix);
		if (params.force) args.push("--force");

		const output = await runPodmanWsl(args, ctx.cwd, signal);
		return {
			content: [{ type: "text", text: output || `Stopped ${container}.` }],
			details: { container, backupSuffix: params.backupSuffix ?? null, force: Boolean(params.force) },
		};
	},
});

export default function (pi: ExtensionAPI) {
	piExecRef = (command, args, cwd, signal) => pi.exec(command, args, { cwd, signal });
	pi.registerTool(inspectWorkersTool);
	pi.registerTool(taskStatusTool);
	pi.registerTool(workerLogsTool);
	pi.registerTool(buildImageTool);
	pi.registerTool(stopWorkerTool);
}
