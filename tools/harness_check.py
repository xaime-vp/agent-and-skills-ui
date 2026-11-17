"""Check this developer harness's own contracts without the product checkout.

Run from the workspace root: python3 tools/harness_check.py --help
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]

SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MCP_NAME = re.compile(r"^[A-Za-z0-9_-]+$")
RELATIVE_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(\s*(<[^>]*>|[^\s)]+)(?:\s+\"[^\"]*\")?\s*\)")
FENCE = re.compile(r"^[ \t]*(`{3,}|~{3,})(.*)$")
PLACEHOLDER = re.compile(r"\b(TODO|TBD|FIXME|XXX)\b|<\s*(placeholder|insert)\b", re.IGNORECASE)
SECRET_PATTERNS = (
    ("github token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}")),
    ("github fine-grained token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}")),
    ("openai-style key", re.compile(r"\bsk-[A-Za-z0-9]{20,}")),
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
)
ROUTING_CUE = re.compile(
    r"\b(use (when|for|before|after|during|to)|invoke|load this skill|when|during|before|after)\b",
    re.IGNORECASE,
)

DOC_GLOBS = ("AGENTS.md", "README.md", "docs/**/*.md", "agents/**/*.md", ".pi/skills/**/*.md", ".agents/skills/**/*.md")
TEXT_SUFFIXES = {".md", ".py", ".ts", ".mjs", ".json", ".yaml", ".yml", ".txt", ".cfg", ".toml"}


@dataclass
class Result:
    check: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def yaml_mapping(text: str) -> tuple[dict, str | None]:
    """Parse data only; never execute YAML constructors or inspect credentials."""
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as error:
        # Parser messages can contain source values. Report location, not values.
        mark = getattr(error, "problem_mark", None)
        location = f" at line {mark.line + 1}, column {mark.column + 1}" if mark else ""
        return {}, f"invalid YAML{location}"
    if not isinstance(data, dict):
        return {}, "YAML must be a mapping"
    return data, None


def frontmatter(text: str) -> tuple[dict, str | None]:
    """Parse a delimited YAML mapping, including folded and literal strings."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, "missing frontmatter block"
    end = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end = index
            break
    if end is None:
        return {}, "unterminated frontmatter block"
    return yaml_mapping("\n".join(lines[1:end]))


def skill_root() -> Path:
    """Client discovery paths remain explicit; display metadata is not discovery."""
    codex = ROOT / ".agents" / "skills"
    pi = ROOT / ".pi" / "skills"
    return codex if codex.is_dir() and not pi.is_dir() else pi


def check_skills() -> Result:
    result = Result("skills")
    skill_files = sorted(skill_root().glob("*/SKILL.md"))
    if not skill_files:
        result.errors.append("client skills directory contains no */SKILL.md")
        return result
    for path in skill_files:
        label = path.relative_to(ROOT).as_posix()
        directory = path.parent.name
        text = read_text(path)
        fields, problem = frontmatter(text)
        if problem:
            result.errors.append(f"{label}: {problem}")
            continue
        name = fields.get("name", "")
        description = fields.get("description", "")
        if not isinstance(name, str) or not name.strip():
            result.errors.append(f"{label}: name must be a non-empty string")
        elif name != directory:
            result.errors.append(f"{label}: name '{name}' does not match directory '{directory}'")
        elif not SKILL_NAME.match(name):
            result.errors.append(f"{label}: name '{name}' is not lowercase-hyphenated")
        elif len(name) > 64:
            result.errors.append(f"{label}: name longer than 64 characters")
        if not isinstance(description, str) or not description.strip():
            result.errors.append(f"{label}: description must be a non-empty string")
        elif len(description) > 1024:
            result.errors.append(f"{label}: description longer than 1024 characters")
        elif not ROUTING_CUE.search(description):
            result.warnings.append(f"{label}: description does not state when to use the skill")
        if PLACEHOLDER.search(text):
            result.warnings.append(f"{label}: contains a placeholder marker")
    result.notes.append(f"{len(skill_files)} skills")
    return result


def check_skill_parity() -> Result:
    result = Result("skill-parity")
    for skill_dir in sorted(skill_root().iterdir()) if skill_root().is_dir() else []:
        if not skill_dir.is_dir():
            continue
        manifest = skill_dir / "agents" / "openai.yaml"
        label = manifest.relative_to(ROOT).as_posix()
        if not manifest.is_file():
            result.errors.append(f"{label}: missing Codex display metadata")
            continue
        data, problem = yaml_mapping(read_text(manifest))
        if problem:
            result.errors.append(f"{label}: {problem}")
            continue
        interface = data.get("interface")
        if not isinstance(interface, dict):
            result.errors.append(f"{label}: interface must be a mapping")
            continue
        for key in ("display_name", "short_description"):
            value = interface.get(key)
            if not isinstance(value, str) or not value.strip():
                result.errors.append(f"{label}: interface.{key} must be a non-empty string")
    result.notes.append("Codex metadata present for every skill")
    return result


def check_prompts() -> Result:
    result = Result("prompts")
    prompt_dir = ROOT / ".pi" / "prompts"
    templates = sorted(prompt_dir.glob("*.md")) if prompt_dir.is_dir() else []
    if not prompt_dir.is_dir():
        result.notes.append("no .pi/prompts directory; prompt templates are unused")
        return result
    skill_names = {path.parent.name for path in skill_root().glob("*/SKILL.md")}
    for path in templates:
        label = path.relative_to(ROOT).as_posix()
        if not SKILL_NAME.match(path.stem):
            result.errors.append(f"{label}: filename is not a valid lowercase-hyphenated command name")
        if path.stem in skill_names:
            result.warnings.append(f"{label}: command name also names a skill directory")
        text = read_text(path)
        if text.lstrip().startswith("---"):
            fields, problem = frontmatter(text)
            if problem:
                result.errors.append(f"{label}: {problem}")
            for key in ("description", "argument-hint"):
                if key in fields and not isinstance(fields[key], str):
                    result.errors.append(f"{label}: {key} must be a string")
        if "${@}" in text:
            result.errors.append(f"{label}: Pi uses $@, not ${{@}}, for all arguments")
        if not text.strip():
            result.errors.append(f"{label}: empty template")
    result.notes.append(f"{len(templates)} templates")
    return result


def iter_markdown() -> list[Path]:
    found: list[Path] = []
    for pattern in DOC_GLOBS:
        found.extend(ROOT.glob(pattern))
    return sorted({path for path in found if path.is_file()})


def check_links() -> Result:
    result = Result("links")
    checked = 0
    for path in iter_markdown():
        fence = None
        for number, line in enumerate(read_text(path).splitlines(), start=1):
            match_fence = FENCE.match(line)
            if fence:
                if match_fence:
                    marker, tail = match_fence.groups()
                    if marker[0] == fence[0] and len(marker) >= len(fence) and not tail.strip():
                        fence = None
                continue
            if match_fence:
                marker, tail = match_fence.groups()
                if marker[0] != "`" or "`" not in tail:
                    fence = marker
                continue
            for match in RELATIVE_LINK.finditer(line):
                target = match.group(1).strip()
                if target.startswith("<") and target.endswith(">"):
                    target = target[1:-1].strip()
                if not target or target.startswith(("#", "http://", "https://", "mailto:", "/")):
                    continue
                clean = target.split("#", 1)[0].split("?", 1)[0]
                if not clean:
                    continue
                resolved = (path.parent / clean).resolve()
                config = ROOT / "harness.config.json"
                targets = json.loads(read_text(config)).get("targets", {}) if config.is_file() else {}
                names = targets.get("optional_checkouts", []) + [targets.get("checkout_dir", "constant-integration"), "constant-integration-ui"]
                optional_checkouts = tuple((ROOT / name).resolve() for name in names
                                           if isinstance(name, str) and re.fullmatch(r"[A-Za-z0-9_-]+", name))
                if any(resolved == co or co in resolved.parents for co in optional_checkouts):
                    continue
                checked += 1
                try:
                    resolved.relative_to(ROOT.resolve())
                except ValueError:
                    result.errors.append(
                        f"{path.relative_to(ROOT).as_posix()}:{number}: link escapes the repository: {target}"
                    )
                    continue
                if not resolved.exists():
                    result.errors.append(
                        f"{path.relative_to(ROOT).as_posix()}:{number}: missing link target: {target}"
                    )
    result.notes.append(f"{checked} relative links")
    return result


def check_mcp() -> Result:
    result = Result("mcp")
    config = ROOT / ".pi" / "mcp.json"
    if not config.is_file():
        result.notes.append("no project .pi/mcp.json")
        return result
    try:
        data = json.loads(read_text(config))
    except json.JSONDecodeError as error:
        result.errors.append(f".pi/mcp.json: invalid JSON: {error}")
        return result
    servers = data.get("mcpServers") if isinstance(data, dict) else None
    if not isinstance(servers, dict) or not servers:
        result.errors.append(".pi/mcp.json: no mcpServers entries")
        return result
    for name, entry in servers.items():
        label = f".pi/mcp.json[{name}]"
        if not MCP_NAME.match(name):
            result.errors.append(f"{label}: server name must use letters, digits, '_' or '-'")
        if not isinstance(entry, dict):
            result.errors.append(f"{label}: entry must be an object")
            continue
        kind = entry.get("type")
        has_command, has_url = "command" in entry, "url" in entry
        if "type" in entry and kind not in ("stdio", "http", "sse"):
            result.errors.append(f"{label}: type must be stdio, http or sse")
        if has_command and has_url:
            result.errors.append(f"{label}: declares both command and url")
        elif kind == "stdio" or (kind is None and has_command):
            if not isinstance(entry.get("command"), str) or not entry["command"].strip():
                result.errors.append(f"{label}: stdio requires a non-empty command")
            if has_url:
                result.errors.append(f"{label}: stdio cannot declare url")
        elif kind in ("http", "sse") or (kind is None and has_url):
            url = entry.get("url")
            try:
                parsed = urlparse(url) if isinstance(url, str) else None
                valid_url = parsed and parsed.scheme in ("http", "https") and parsed.hostname
            except ValueError:
                valid_url = False
            if not valid_url:
                result.errors.append(f"{label}: HTTP/SSE requires an absolute http(s) url")
            if has_command:
                result.errors.append(f"{label}: HTTP/SSE cannot declare command")
        elif kind is None:
            result.warnings.append(f"{label}: no transport; it only overrides another server")
        if "args" in entry and (
            not isinstance(entry["args"], list) or not all(isinstance(arg, str) for arg in entry["args"])
        ):
            result.errors.append(f"{label}: args must be a list of strings")
        for section in ("headers", "env"):
            values = entry.get(section)
            if section not in entry:
                continue
            if not isinstance(values, dict):
                result.errors.append(f"{label}.{section}: must be an object of strings")
                continue
            for key, value in values.items():
                if not isinstance(value, str):
                    result.errors.append(f"{label}.{section}.{key}: must be a string")
                    continue
                if value.startswith("${") or value.startswith("!"):
                    continue
                for label_secret, pattern in SECRET_PATTERNS:
                    if pattern.search(value):
                        result.errors.append(f"{label}.{section}.{key}: literal {label_secret}; use ${{VAR}}")
    result.notes.append(f"{len(servers)} servers")
    return result


def tracked_text_files() -> list[Path]:
    try:
        listing = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
            timeout=60,
        ).stdout
        names = [name for name in listing.split("\0") if name]
    except (OSError, subprocess.SubprocessError):
        names = [path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*") if path.is_file()]
    return [ROOT / name for name in names if Path(name).suffix in TEXT_SUFFIXES]


def check_secrets() -> Result:
    result = Result("secrets")
    scanned = 0
    for path in tracked_text_files():
        if not path.is_file():
            continue
        scanned += 1
        text = read_text(path)
        for label, pattern in SECRET_PATTERNS:
            if pattern.search(text):
                result.errors.append(f"{path.relative_to(ROOT).as_posix()}: looks like a {label}")
    result.notes.append(f"{scanned} tracked files scanned")
    return result


def check_extensions() -> Result:
    result = Result("extensions")
    directory = ROOT / ".pi" / "extensions"
    entries = sorted(directory.glob("*.ts")) if directory.is_dir() else []
    if not entries:
        result.notes.append("no .pi/extensions entries")
    tests = sorted(directory.glob("*.test.mjs"))
    for legacy in (".pi/tools", ".pi/hooks"):
        if (ROOT / legacy).exists():
            result.errors.append(f"{legacy}: Pi tools and hooks must live in .pi/extensions")
    for entry in entries:
        label = entry.relative_to(ROOT).as_posix()
        source = read_text(entry)
        if re.search(
            r"""import\s+(?:type\s+)?\{[^}]*\b(?:Type|Static|TSchema)\b[^}]*\}\s+from\s+["']@earendil-works/pi-ai["']""",
            source,
            flags=re.DOTALL,
        ):
            result.errors.append(f"{label}: import TypeBox schema types from 'typebox', not 'pi-ai'")
        imported = re.search(r'from\s+"\./([A-Za-z0-9_-]+-core\.mjs)"', source)
        if not imported:
            result.warnings.append(f"{label}: does not import a sibling *-core.mjs module")
            continue
        core = directory / imported.group(1)
        if not core.is_file():
            result.errors.append(f"{label}: imports missing module {core.name}")
        elif not (directory / f"{core.stem}.test.mjs").is_file():
            result.warnings.append(f"{label}: {core.name} has no dependency-free test")
    result.notes.append(f"{len(entries)} entries, {len(tests)} node test files (not executed here)")
    return result


CHECKS = {
    "skills": check_skills,
    "skill-parity": check_skill_parity,
    "prompts": check_prompts,
    "links": check_links,
    "mcp": check_mcp,
    "secrets": check_secrets,
    "extensions": check_extensions,
}


def main(argv: list[str] | None = None) -> int:
    global ROOT
    parser = argparse.ArgumentParser(
        prog="harness_check.py",
        description="Check this developer harness's own contracts. Read-only; no network.",
        epilog="Checks: " + ", ".join(CHECKS),
    )
    parser.add_argument("--root", default=str(ROOT), help="workspace root (default: repository root)")
    parser.add_argument("--only", default="", help="comma-separated check ids")
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    parser.add_argument("--json", action="store_true", help="emit a machine-readable result")
    parser.add_argument("--list", action="store_true", help="list check ids and exit")
    args = parser.parse_args(argv)

    if args.list:
        print("\n".join(CHECKS))
        return 0

    if yaml is None:
        print("harness_check: install dependencies with python -m pip install -r tools/requirements-harness.txt",
              file=sys.stderr)
        return 2

    ROOT = Path(args.root).resolve()
    if not (ROOT / "AGENTS.md").is_file():
        print(f"harness_check: {ROOT} does not look like the workspace root", file=sys.stderr)
        return 2

    selected = [name.strip() for name in args.only.split(",") if name.strip()] or list(CHECKS)
    unknown = [name for name in selected if name not in CHECKS]
    if unknown:
        print(f"harness_check: unknown check(s): {', '.join(unknown)}", file=sys.stderr)
        return 2

    results = [CHECKS[name]() for name in selected]
    failed = [item for item in results if not item.ok]
    warned = [item for item in results if item.warnings]
    status = 0 if not failed and not (args.strict and warned) else 1

    if args.json:
        print(
            json.dumps(
                {
                    "status": status,
                    "checks": [
                        {
                            "check": item.check,
                            "ok": item.ok,
                            "errors": item.errors,
                            "warnings": item.warnings,
                            "notes": item.notes,
                        }
                        for item in results
                    ],
                },
                indent=2,
            )
        )
        return status

    width = max(len(item.check) for item in results)
    for item in results:
        state = "PASS" if item.ok else "FAIL"
        detail = "; ".join(item.notes)
        print(f"{state} {item.check.ljust(width)}  {detail}")
        for line in item.errors:
            print(f"     error: {line}")
        for line in item.warnings:
            print(f"     warn:  {line}")
    print()
    print(
        f"harness_check: {len(results) - len(failed)}/{len(results)} checks passed, "
        f"{sum(len(item.warnings) for item in results)} warning(s)"
    )
    return status


if __name__ == "__main__":
    raise SystemExit(main())
