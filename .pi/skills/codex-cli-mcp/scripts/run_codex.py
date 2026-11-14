#!/usr/bin/env python3
"""Launch Codex CLI from the MCP-connected ./codex folder."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def resolve_codex_bin() -> str:
    found = shutil.which("codex")
    if not found:
        raise SystemExit("codex CLI not found on PATH.")
    return found


def inspect_mcp_json(codex_dir: Path) -> list[str]:
    mcp_file = codex_dir / ".mcp.json"
    if not mcp_file.is_file():
        mcp_file = codex_dir / "mcp.json"
    if not mcp_file.is_file():
        return []
    data = json.loads(mcp_file.read_text(encoding="utf-8"))
    servers = data.get("mcpServers") or data.get("servers") or {}
    return sorted(servers.keys()) if isinstance(servers, dict) else []


def ensure_codex_dir(raw: str) -> Path:
    p = Path(raw).resolve()
    if not p.is_dir():
        raise SystemExit(f"Codex MCP directory does not exist: {p}")
    return p


def cmd_check(args: argparse.Namespace) -> int:
    codex_bin = resolve_codex_bin()
    codex_dir = ensure_codex_dir(args.codex_dir)
    servers = inspect_mcp_json(codex_dir)
    ver = subprocess.run([codex_bin, "--version"], text=True, capture_output=True, check=False)
    print(f"codex_bin: {codex_bin}")
    print(f"codex_version: {ver.stdout.strip() or ver.stderr.strip()}")
    print(f"codex_dir: {codex_dir}")
    print(f"mcp_json_servers: {servers}")
    mcp_list = subprocess.run([codex_bin, "mcp"], cwd=str(codex_dir), check=False)
    return mcp_list.returncode


def cmd_interactive(args: argparse.Namespace) -> int:
    codex_bin = resolve_codex_bin()
    codex_dir = ensure_codex_dir(args.codex_dir)
    cmd = [codex_bin, "-C", str(codex_dir)]
    if args.model:
        cmd.extend(["-m", args.model])
    return subprocess.run(cmd, cwd=str(codex_dir), check=False).returncode


def cmd_exec(args: argparse.Namespace) -> int:
    codex_bin = resolve_codex_bin()
    codex_dir = ensure_codex_dir(args.codex_dir)
    prompt = args.prompt
    if args.repo:
        repo_path = Path(args.repo).resolve()
        if not repo_path.exists():
            raise SystemExit(f"Target repository path does not exist: {repo_path}")
        prompt = f"Target repository checkout: {repo_path}\n\n{prompt}"

    cmd = [codex_bin, "exec", "-C", str(codex_dir)]
    if args.full_auto:
        cmd.append("--full-auto")
    if args.sandbox:
        cmd.extend(["-s", args.sandbox])
    if args.model:
        cmd.extend(["-m", args.model])
    cmd.append(prompt)
    return subprocess.run(cmd, cwd=str(codex_dir), check=False).returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run Codex CLI in the MCP-connected ./codex folder for GitHub PR/issue access."
    )
    parser.add_argument(
        "--codex-dir",
        default="codex",
        help="Directory containing the Codex .mcp.json connection (default: ./codex)",
    )
    sub = parser.add_subparsers(dest="subcommand", required=True)

    p_check = sub.add_parser("check", help="Verify codex CLI, ./codex/.mcp.json servers, and MCP list")
    p_check.set_defaults(func=cmd_check)

    p_int = sub.add_parser("interactive", help="Open interactive Codex CLI in ./codex")
    p_int.add_argument("-m", "--model", help="Optional model override")
    p_int.set_defaults(func=cmd_interactive)

    p_exec = sub.add_parser("exec", help="Run non-interactive codex exec in ./codex")
    p_exec.add_argument("--repo", help="Optional target checkout path to pass in task context (e.g. . or constant-integration)")
    p_exec.add_argument("--full-auto", action="store_true", help="Pass --full-auto to codex exec")
    p_exec.add_argument(
        "-s",
        "--sandbox",
        choices=("read-only", "workspace-write", "danger-full-access"),
        help="Optional sandbox mode",
    )
    p_exec.add_argument("-m", "--model", help="Optional model override")
    p_exec.add_argument("prompt", help="Prompt for codex exec")
    p_exec.set_defaults(func=cmd_exec)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
