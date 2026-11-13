/**
 * Bonsai Podman Tools - Quick tools to build Bonsai worker images and safely stop previous workers.
 */

import path from "node:path";
import { Type } from "@earendil-works/pi-ai";
import { defineTool, type ExtensionAPI } from "@earendil-works/pi-coding-agent";

function toWslPath(winOrRelPath: string, cwd: string): string {
	const abs = path.resolve(cwd, winOrRelPath);
	const match = /^([A-Za-z]):[\\/](.*)$/.exec(abs);
	if (!match) {
		return abs.replace(/\\/g, "/");
	}
	const drive = match[1].toLowerCase();
	const rest = match[2].replace(/\\/g, "/");
	return `/mnt/${drive}/${rest}`;
}

const SAFE_NAME = /^[A-Za-z0-9][A-Za-z0-9_.:/-]*$/;
const SAFE_SUFFIX = /^[A-Za-z0-9._-]+$/;

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
				description:
					"Image tag (default: localhost/bonsai-worker:main-<shortsha>)",
			}),
		),
		runCheck: Type.Optional(
			Type.Boolean({
				description: "Run `podman run --rm <tag> check` after building (default: false)",
			}),
		),
	}),

	async execute(_toolCallId, params, signal, _onUpdate, ctx) {
		const repoWsl = toWslPath(params.repoPath ?? "constant-integration", ctx.cwd);
		const scriptWsl = toWslPath(".pi/skills/bonsai-podman-ops/scripts/build_image.sh", ctx.cwd);
		if (params.tag && !SAFE_NAME.test(params.tag)) {
			throw new Error(`Invalid image tag: ${params.tag}`);
		}
		const args = ["-d", "podman-machine-default", "-e", "sh", scriptWsl, repoWsl];
		if (params.tag) args.push(params.tag);
		if (params.runCheck) args.push("--check");

		const res = await piExecRef(args, signal);
		const output = [res.stdout, res.stderr].filter(Boolean).join("\n").trim();
		if (res.code !== 0) {
			throw new Error(`bonsai_build_image failed (exit ${res.code}):\n${output}`);
		}
		return {
			content: [{ type: "text", text: output || "Image built." }],
			details: { repoWsl, tag: params.tag ?? "auto", runCheck: Boolean(params.runCheck) },
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
				description: "Container name (default: bonsai-worker)",
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
		const container = params.container ?? "bonsai-worker";
		if (!SAFE_NAME.test(container)) {
			throw new Error(`Invalid container name: ${container}`);
		}
		if (params.backupSuffix && !SAFE_SUFFIX.test(params.backupSuffix)) {
			throw new Error(`Invalid backupSuffix: ${params.backupSuffix}`);
		}
		const scriptWsl = toWslPath(".pi/skills/bonsai-podman-ops/scripts/stop_worker.sh", ctx.cwd);
		const args = ["-d", "podman-machine-default", "-e", "sh", scriptWsl, container];
		if (params.backupSuffix) {
			args.push("--backup-suffix", params.backupSuffix);
		}
		if (params.force) {
			args.push("--force");
		}

		const res = await piExecRef(args, signal);
		const output = [res.stdout, res.stderr].filter(Boolean).join("\n").trim();
		if (res.code !== 0) {
			throw new Error(`bonsai_stop_worker failed (exit ${res.code}):\n${output}`);
		}
		return {
			content: [{ type: "text", text: output || `Stopped ${container}.` }],
			details: { container, backupSuffix: params.backupSuffix ?? null, force: Boolean(params.force) },
		};
	},
});

let piExecRef: (args: string[], signal?: AbortSignal) => Promise<{ stdout: string; stderr: string; code: number }>;

export default function (pi: ExtensionAPI) {
	piExecRef = (args, signal) => pi.exec("wsl", args, { signal });
	pi.registerTool(buildImageTool);
	pi.registerTool(stopWorkerTool);
}
