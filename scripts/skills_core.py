#!/usr/bin/env python3
"""Core installer logic for altfins-ai-skills."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

ROOT_OVERRIDE_ENV = "ALTFINS_SKILLS_ROOT"
DIST_OVERRIDE_ENV = "ALTFINS_SKILLS_DIST_DIR"
INSTALL_MODES = ("skills", "project")
KNOWN_SKILLS = [
    "altfins-market-analyst",
    "altfins-market-researcher",
    "altfins-query-builder",
]
PROJECT_DATA_ROOT = ".altfins-skills"
CLAUDE_COWORK_NOTE = (
    "Claude Cowork uses upload flow. Run `altfins-skills package ...` and upload the resulting "
    "`.skill.zip` in Claude > Customize > Skills."
)
PLATFORM_ALIASES = {"claude": "claude-code"}


class SkillsError(Exception):
    """Raised for user-facing CLI failures."""


@dataclass(frozen=True)
class PlatformSpec:
    name: str
    skills_install_root: Path | None = None
    skills_mode_adapter: str | None = None
    skills_payload_root: Path | None = None
    project_adapter: str | None = None
    package_note: str | None = None

    @property
    def supported_modes(self) -> list[str]:
        modes: list[str] = []
        if self.skills_install_root is not None:
            modes.append("skills")
        if self.project_adapter is not None:
            modes.append("project")
        return modes

    @property
    def package_only(self) -> bool:
        return self.package_note is not None and not self.supported_modes


@dataclass(frozen=True)
class TargetContext:
    platform: PlatformSpec
    mode: str
    project_dir: Path | None = None


def _expand_home(path: str) -> Path:
    return Path(os.path.expanduser(path)).resolve()


def _env_home(env_name: str, default_home: str) -> Path:
    return _expand_home(os.environ.get(env_name, default_home))


def _looks_like_repo_root(path: Path) -> bool:
    return (
        path.is_dir()
        and (path / "README.md").exists()
        and (path / "scripts" / "skills.py").exists()
        and all((path / skill / "SKILL.md").exists() for skill in KNOWN_SKILLS)
    )


def resolve_repo_root(
    script_file: Path | None = None,
    executable_path: Path | None = None,
    frozen: bool | None = None,
) -> Path:
    override = os.environ.get(ROOT_OVERRIDE_ENV)
    if override:
        candidate = _expand_home(override)
        if not _looks_like_repo_root(candidate):
            raise SkillsError(
                f"{ROOT_OVERRIDE_ENV} does not point to a valid altfins-ai-skills root: {candidate}"
            )
        return candidate

    frozen = getattr(sys, "frozen", False) if frozen is None else frozen
    if frozen:
        exe_path = Path(executable_path or sys.executable).resolve()
        for candidate in (exe_path.parent / "repo", exe_path.parent / "_internal" / "repo"):
            if _looks_like_repo_root(candidate):
                return candidate

    here = Path(script_file or __file__).resolve()
    candidate_roots = []
    if here.parent.name == "scripts":
        candidate_roots.append(here.parents[1])
    candidate_roots.append(here.parent)
    for candidate in candidate_roots:
        if _looks_like_repo_root(candidate):
            return candidate

    raise SkillsError(
        "Could not locate the altfins-ai-skills repository root. Set ALTFINS_SKILLS_ROOT explicitly if needed."
    )


@lru_cache(maxsize=1)
def repo_root() -> Path:
    return resolve_repo_root()


def checkout_layout(root: Path | None = None) -> bool:
    base = root or repo_root()
    return (
        (base / ".gitignore").exists()
        and (base / ".github" / "workflows" / "validate-skills.yml").exists()
    )


def dist_dir() -> Path:
    override = os.environ.get(DIST_OVERRIDE_ENV)
    if override:
        return Path(override).expanduser().resolve()
    if checkout_layout():
        return repo_root() / "dist" / "skills"
    return Path.home() / ".altfins-skills" / "dist" / "skills"


def validator_commands(profile: str = "repo") -> list[list[str]]:
    root = repo_root()
    commands = [
        [sys.executable, str(root / "scripts" / "validate_skills.py"), "--profile", profile],
    ]
    if profile == "repo":
        commands.append([sys.executable, str(root / "scripts" / "lint_markdown_contracts.py")])
    return commands


def canonical_platform_name(name: str | None) -> str | None:
    if name is None:
        return None
    return PLATFORM_ALIASES.get(name, name)


def platform_choice_names() -> list[str]:
    return sorted(set(platform_specs()) | set(PLATFORM_ALIASES))


def emit_platform_alias_warning(name: str | None) -> None:
    if name == "claude":
        print(
            "Warning: --platform claude is deprecated. Use --platform claude-code for local Claude Code subagents "
            "or package skill ZIPs for Claude Cowork.",
            file=sys.stderr,
        )


def platform_specs() -> dict[str, PlatformSpec]:
    codex_home = _expand_home(os.environ.get("CODEX_HOME", "~/.codex"))
    claude_home = _env_home("CLAUDE_HOME", "~/.claude")
    gemini_home = _env_home("GEMINI_HOME", "~/.gemini")
    copilot_home = _env_home("COPILOT_HOME", "~/.copilot")
    return {
        "codex": PlatformSpec("codex", skills_install_root=codex_home / "skills"),
        "claude-code": PlatformSpec(
            "claude-code",
            skills_install_root=claude_home / "agents",
            skills_mode_adapter="claude-code",
            skills_payload_root=claude_home / "skills",
        ),
        "claude-cowork": PlatformSpec("claude-cowork", package_note=CLAUDE_COWORK_NOTE),
        "gemini": PlatformSpec("gemini", skills_install_root=gemini_home / "skills"),
        "copilot": PlatformSpec("copilot", skills_install_root=copilot_home / "skills"),
        "cursor": PlatformSpec("cursor", project_adapter="cursor"),
        "openclaw": PlatformSpec("openclaw", project_adapter="openclaw"),
    }


def find_skill_dirs(root: Path | None = None) -> list[Path]:
    base = root or repo_root()
    return sorted(
        path
        for path in base.iterdir()
        if path.is_dir() and path.name.startswith("altfins-") and (path / "SKILL.md").exists()
    )


def skill_names(root: Path | None = None) -> list[str]:
    return [path.name for path in find_skill_dirs(root)]


def resolve_skills(selected: list[str], use_all: bool, root: Path | None = None) -> list[Path]:
    skills = {path.name: path for path in find_skill_dirs(root)}
    if use_all:
        return list(skills.values())
    if not selected:
        raise SkillsError("Provide at least one skill name or use --all.")
    resolved: list[Path] = []
    for name in selected:
        path = skills.get(name)
        if path is None:
            raise SkillsError(f"Unknown skill: {name}")
        resolved.append(path)
    return resolved


def ensure_valid_repo(profile: str = "repo") -> None:
    for command in validator_commands(profile=profile):
        result = subprocess.run(command, cwd=repo_root())
        if result.returncode != 0:
            joined = " ".join(command)
            raise SkillsError(f"Repository validation failed while running: {joined}")


def get_platform(name: str) -> PlatformSpec:
    specs = platform_specs()
    canonical = canonical_platform_name(name)
    if canonical not in specs:
        raise SkillsError(f"Unknown platform: {name}")
    return specs[canonical]


def resolve_target(platform_name: str, mode: str, project_dir: str | None) -> TargetContext:
    platform = get_platform(platform_name)
    if platform.package_only:
        raise SkillsError(platform.package_note or f"Platform {platform.name} uses package/upload workflow.")
    if mode not in INSTALL_MODES:
        raise SkillsError(f"Unknown mode: {mode}")
    if mode == "skills":
        if platform.skills_install_root is None:
            if platform.project_adapter is not None:
                raise SkillsError(
                    f"Platform {platform.name} uses --mode project. Re-run with --mode project --project-dir <path>."
                )
            raise SkillsError(f"Platform {platform.name} does not support skills mode.")
        return TargetContext(platform=platform, mode=mode)
    if platform.project_adapter is None:
        raise SkillsError(
            f"Platform {platform.name} supports skills mode only. Re-run without --mode project."
        )
    if not project_dir:
        raise SkillsError("Project mode requires --project-dir <path>.")
    return TargetContext(
        platform=platform,
        mode=mode,
        project_dir=Path(project_dir).expanduser().resolve(),
    )


def install_destination(target: TargetContext, skill_name: str) -> Path:
    if target.mode != "skills" or target.platform.skills_install_root is None:
        raise SkillsError(f"Platform {target.platform.name} does not have a skills install root.")
    return target.platform.skills_install_root / skill_name


def claude_code_agent_path(target: TargetContext, skill_name: str) -> Path:
    if target.platform.skills_install_root is None:
        raise SkillsError("Claude Code install requires an agents root.")
    return target.platform.skills_install_root / f"{skill_name}.md"


def claude_code_payload_destination(target: TargetContext, skill_name: str) -> Path:
    if target.platform.skills_payload_root is None:
        raise SkillsError("Claude Code install requires a payload root.")
    return target.platform.skills_payload_root / skill_name


def remove_path(path: Path) -> None:
    if not path.exists():
        return
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


def parse_skill_frontmatter(skill_path: Path) -> tuple[str, str]:
    text = skill_path.read_text(encoding="utf-8").replace("\r\n", "\n")
    if not text.startswith("---\n"):
        raise SkillsError(f"Expected YAML frontmatter in {skill_path}")
    closing = text.find("\n---\n", 4)
    if closing == -1:
        raise SkillsError(f"Could not find closing frontmatter marker in {skill_path}")
    frontmatter = text[4:closing]
    payload: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        payload[key.strip()] = value.strip()
    return payload.get("name", skill_path.parent.name), payload.get("description", skill_path.parent.name)


def render_claude_code_agent(skill_dir: Path, payload_dest: Path) -> str:
    skill_name, description = parse_skill_frontmatter(skill_dir / "SKILL.md")
    return (
        "---\n"
        f"name: {json.dumps(skill_name)}\n"
        f"description: {json.dumps(description)}\n"
        "---\n\n"
        "Use the installed AltFINS skill bundle at the paths below.\n\n"
        "Read and follow these files in order:\n"
        f"- `{payload_dest / 'SKILL.md'}`\n"
        f"- `{payload_dest / 'README.md'}`\n"
        f"- `{payload_dest / 'references'}` for structured guidance and validation scenarios\n"
        f"- `{payload_dest / 'assets'}` for reusable templates and packaging assets\n\n"
        "Treat the installed `SKILL.md` as the primary contract. Load only the additional files you need for the task at hand.\n"
    )


def install_claude_code_skill(target: TargetContext, skill_dir: Path, force: bool) -> tuple[Path, Path]:
    agent_path = claude_code_agent_path(target, skill_dir.name)
    payload_dest = claude_code_payload_destination(target, skill_dir.name)
    if agent_path.exists() and not force:
        raise SkillsError(
            f"Claude Code agent already exists: {agent_path}. Re-run with --force to overwrite."
        )
    if force:
        remove_path(agent_path)
    copy_skill(skill_dir, payload_dest, force=force)
    agent_path.parent.mkdir(parents=True, exist_ok=True)
    agent_path.write_text(render_claude_code_agent(skill_dir, payload_dest), encoding="utf-8")
    return agent_path, payload_dest


def uninstall_claude_code_skill(target: TargetContext, skill_name: str, force: bool) -> tuple[Path, Path]:
    agent_path = claude_code_agent_path(target, skill_name)
    payload_dest = claude_code_payload_destination(target, skill_name)
    if not agent_path.exists() and not payload_dest.exists():
        raise SkillsError(f"Claude Code skill is not installed: {skill_name}")
    if agent_path.exists():
        if agent_path.is_dir() and not force:
            raise SkillsError(
                f"Claude Code agent target is a directory: {agent_path}. Re-run with --force to remove it."
            )
        remove_path(agent_path)
    if payload_dest.exists():
        uninstall_skill(payload_dest, force=force)
    return agent_path, payload_dest


def claude_code_status(platform: PlatformSpec, skill_name: str) -> dict[str, object]:
    agent_root = platform.skills_install_root
    payload_root = platform.skills_payload_root
    agent_path = agent_root / f"{skill_name}.md" if agent_root else None
    payload_dest = payload_root / skill_name if payload_root else None
    agent_exists = agent_path.exists() if agent_path else False
    payload_exists = payload_dest.exists() if payload_dest else False
    return {
        "installed": agent_exists and payload_exists,
        "supported": True,
        "agent_present": agent_exists,
        "payload_present": payload_exists,
        "paths": {
            "agent": str(agent_path) if agent_path else None,
            "payload": str(payload_dest) if payload_dest else None,
        },
    }


def package_archive_path(skill_name: str) -> Path:
    return dist_dir() / f"{skill_name}.skill.zip"


def package_upload_status(platform: PlatformSpec, skill_name: str) -> dict[str, object]:
    archive = package_archive_path(skill_name)
    return {
        "name": skill_name,
        "installed": archive.exists(),
        "supported": True,
        "workflow": "package-upload",
        "reason": platform.package_note,
        "paths": {"archive": str(archive)},
    }


def project_skill_destination(target: TargetContext, skill_name: str) -> Path:
    if target.project_dir is None:
        raise SkillsError("Project mode requires a resolved project directory.")
    return target.project_dir / PROJECT_DATA_ROOT / target.platform.name / skill_name


def cursor_rule_path(target: TargetContext, skill_name: str) -> Path:
    if target.project_dir is None:
        raise SkillsError("Project mode requires a resolved project directory.")
    return target.project_dir / ".cursor" / "rules" / f"{skill_name}.mdc"


def openclaw_agents_path(target: TargetContext) -> Path:
    if target.project_dir is None:
        raise SkillsError("Project mode requires a resolved project directory.")
    return target.project_dir / "AGENTS.md"


def openclaw_section_markers(skill_name: str) -> tuple[str, str]:
    start = f"<!-- altfins-skills:openclaw:{skill_name}:start -->"
    end = f"<!-- altfins-skills:openclaw:{skill_name}:end -->"
    return start, end


def read_text_if_exists(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def render_template(template_path: Path, replacements: dict[str, str]) -> str:
    text = template_path.read_text(encoding="utf-8")
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text


def cleanup_empty_parents(path: Path, stop: Path) -> None:
    current = path
    stop = stop.resolve()
    while current.exists() and current != stop:
        try:
            if any(current.iterdir()):
                return
        except NotADirectoryError:
            return
        current.rmdir()
        current = current.parent


def replace_marked_section(existing: str, start: str, end: str, new_block: str) -> tuple[str, bool]:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\n?", re.DOTALL)
    replaced = bool(pattern.search(existing))
    if replaced:
        updated = pattern.sub(new_block.rstrip() + "\n", existing)
        return updated, True
    base = existing.rstrip()
    if base:
        base += "\n\n"
    updated = base + new_block.rstrip() + "\n"
    return updated, False


def remove_marked_section(existing: str, start: str, end: str) -> tuple[str, bool]:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\n?", re.DOTALL)
    if not pattern.search(existing):
        return existing, False
    updated = pattern.sub("", existing)
    stripped = updated.strip()
    if not stripped:
        return "", True
    updated = re.sub(r"\n{3,}", "\n\n", stripped) + "\n"
    return updated, True


def copy_skill(src: Path, dest: Path, force: bool) -> None:
    if dest.exists():
        if not force:
            raise SkillsError(
                f"Destination already exists: {dest}. Re-run with --force to overwrite."
            )
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dest)


def uninstall_skill(dest: Path, force: bool) -> None:
    if not dest.exists():
        raise SkillsError(f"Skill is not installed: {dest}")
    if not dest.is_dir():
        raise SkillsError(f"Installed target is not a directory: {dest}")
    if not force:
        skill_md = dest / "SKILL.md"
        if not skill_md.exists():
            raise SkillsError(
                f"Refusing to remove {dest} because it does not look like an installed skill. Re-run with --force if this is intentional."
            )
    shutil.rmtree(dest)


def install_cursor_project_skill(target: TargetContext, skill_dir: Path, force: bool) -> None:
    project_dest = project_skill_destination(target, skill_dir.name)
    rule_path = cursor_rule_path(target, skill_dir.name)
    if rule_path.exists() and not force:
        raise SkillsError(
            f"Cursor rule already exists: {rule_path}. Re-run with --force to overwrite."
        )
    copy_skill(skill_dir, project_dest, force=force)
    rendered = render_template(
        skill_dir / "assets" / "project" / "cursor.mdc",
        {
            "{{PROJECT_SKILL_ROOT}}": str(project_dest.relative_to(target.project_dir)).replace("\\", "/"),
            "{{SKILL_NAME}}": skill_dir.name,
        },
    )
    rule_path.parent.mkdir(parents=True, exist_ok=True)
    rule_path.write_text(rendered.rstrip() + "\n", encoding="utf-8")


def install_openclaw_project_skill(target: TargetContext, skill_dir: Path, force: bool) -> None:
    project_dest = project_skill_destination(target, skill_dir.name)
    agents_path = openclaw_agents_path(target)
    start, end = openclaw_section_markers(skill_dir.name)
    section_body = render_template(
        skill_dir / "assets" / "project" / "openclaw-agents.md",
        {
            "{{PROJECT_SKILL_ROOT}}": str(project_dest.relative_to(target.project_dir)).replace("\\", "/"),
            "{{SKILL_NAME}}": skill_dir.name,
        },
    ).rstrip()
    block = f"{start}\n{section_body}\n{end}\n"
    existing = read_text_if_exists(agents_path)
    already_present = start in existing and end in existing
    if already_present and not force:
        raise SkillsError(
            f"OpenClaw project section already exists in {agents_path}. Re-run with --force to overwrite."
        )
    copy_skill(skill_dir, project_dest, force=force)
    updated, _ = replace_marked_section(existing, start, end, block)
    agents_path.parent.mkdir(parents=True, exist_ok=True)
    agents_path.write_text(updated, encoding="utf-8")


def install_project_skill(target: TargetContext, skill_dir: Path, force: bool) -> None:
    if target.platform.project_adapter == "cursor":
        install_cursor_project_skill(target, skill_dir, force=force)
        return
    if target.platform.project_adapter == "openclaw":
        install_openclaw_project_skill(target, skill_dir, force=force)
        return
    raise SkillsError(f"Unknown project adapter for {target.platform.name}")


def uninstall_cursor_project_skill(target: TargetContext, skill_name: str, force: bool) -> None:
    rule_path = cursor_rule_path(target, skill_name)
    project_dest = project_skill_destination(target, skill_name)
    if not rule_path.exists():
        raise SkillsError(f"Cursor rule is not installed: {rule_path}")
    if rule_path.is_dir():
        raise SkillsError(f"Cursor rule target is not a file: {rule_path}")
    rule_path.unlink()
    if project_dest.exists():
        uninstall_skill(project_dest, force=force)
    cleanup_empty_parents(rule_path.parent, target.project_dir)
    cleanup_empty_parents(project_dest.parent, target.project_dir)


def uninstall_openclaw_project_skill(target: TargetContext, skill_name: str, force: bool) -> None:
    agents_path = openclaw_agents_path(target)
    start, end = openclaw_section_markers(skill_name)
    existing = read_text_if_exists(agents_path)
    updated, found = remove_marked_section(existing, start, end)
    if not found:
        raise SkillsError(f"OpenClaw project section is not installed in {agents_path}")
    if updated:
        agents_path.write_text(updated, encoding="utf-8")
    else:
        agents_path.unlink(missing_ok=True)
    project_dest = project_skill_destination(target, skill_name)
    if project_dest.exists():
        uninstall_skill(project_dest, force=force)
    cleanup_empty_parents(project_dest.parent, target.project_dir)


def uninstall_project_skill(target: TargetContext, skill_name: str, force: bool) -> None:
    if target.platform.project_adapter == "cursor":
        uninstall_cursor_project_skill(target, skill_name, force=force)
        return
    if target.platform.project_adapter == "openclaw":
        uninstall_openclaw_project_skill(target, skill_name, force=force)
        return
    raise SkillsError(f"Unknown project adapter for {target.platform.name}")


def create_skill_zip(skill_dir: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for file_path in sorted(skill_dir.rglob("*")):
            if file_path.is_dir():
                continue
            archive.write(file_path, arcname=str(file_path.relative_to(skill_dir.parent)))


def json_dump(payload: object) -> None:
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")


def project_status(target: TargetContext, skill_name: str) -> dict[str, object]:
    project_dest = project_skill_destination(target, skill_name)
    payload_exists = project_dest.exists()
    if target.platform.project_adapter == "cursor":
        integration_path = cursor_rule_path(target, skill_name)
        integration_exists = integration_path.exists()
        return {
            "installed": payload_exists and integration_exists,
            "payload_present": payload_exists,
            "integration_present": integration_exists,
            "paths": {
                "project_copy": str(project_dest),
                "integration": str(integration_path),
            },
        }
    agents_path = openclaw_agents_path(target)
    start, end = openclaw_section_markers(skill_name)
    agents_text = read_text_if_exists(agents_path)
    integration_exists = start in agents_text and end in agents_text
    return {
        "installed": payload_exists and integration_exists,
        "payload_present": payload_exists,
        "integration_present": integration_exists,
        "paths": {
            "project_copy": str(project_dest),
            "integration": str(agents_path),
        },
    }


def skill_status_for_mode(
    platform: PlatformSpec,
    mode: str,
    project_dir: Path | None,
    skill_name: str,
) -> dict[str, object]:
    item: dict[str, object] = {"name": skill_name}
    if mode not in platform.supported_modes:
        item.update(
            {
                "installed": None,
                "supported": False,
                "reason": (
                    "Use --mode project with --project-dir <path>."
                    if platform.project_adapter and mode == "skills"
                    else f"Platform {platform.name} does not support {mode} mode."
                ),
            }
        )
        return item

    if mode == "skills":
        if platform.skills_mode_adapter == "claude-code":
            item.update(claude_code_status(platform, skill_name))
            return item
        destination = platform.skills_install_root / skill_name if platform.skills_install_root else None
        item.update(
            {
                "installed": destination.exists() if destination else False,
                "supported": True,
                "paths": {"install_root": str(destination)} if destination else None,
            }
        )
        return item

    if project_dir is None:
        item.update(
            {
                "installed": None,
                "supported": True,
                "reason": "Provide --project-dir <path> to inspect project-mode installation state.",
            }
        )
        return item

    target = TargetContext(platform=platform, mode=mode, project_dir=project_dir)
    item.update({"supported": True, **project_status(target, skill_name)})
    return item


def list_payload(
    platform_name: str | None = None,
    mode: str | None = None,
    project_dir: str | None = None,
) -> list[dict[str, object]]:
    skills = find_skill_dirs()
    if platform_name is None:
        return [{"name": skill_dir.name} for skill_dir in skills]

    platform = get_platform(platform_name)
    resolved_project_dir = Path(project_dir).expanduser().resolve() if project_dir else None
    payload: list[dict[str, object]] = []
    for skill_dir in skills:
        item: dict[str, object] = {"name": skill_dir.name}
        item["platform"] = {
            "name": platform.name,
            "supported_modes": platform.supported_modes,
            "mode": mode,
            "project_dir": str(resolved_project_dir) if resolved_project_dir else None,
        }
        if platform.package_only:
            item["platform"]["workflow"] = "package-upload"
            item["platform"]["note"] = platform.package_note
            item["platform"]["status"] = package_upload_status(platform, skill_dir.name)
        elif mode:
            item["platform"]["status"] = skill_status_for_mode(
                platform,
                mode,
                resolved_project_dir,
                skill_dir.name,
            )
        payload.append(item)
    return payload


def status_payload(
    platform_name: str | None = None,
    mode: str | None = None,
    project_dir: str | None = None,
) -> dict[str, object]:
    skills = skill_names()
    specs = platform_specs()
    selected = [specs[canonical_platform_name(platform_name)]] if platform_name else [specs[name] for name in sorted(specs)]
    resolved_project_dir = Path(project_dir).expanduser().resolve() if project_dir else None
    platform_items: list[dict[str, object]] = []
    for platform in selected:
        if platform.package_only and mode is None:
            mode_item = {
                "mode": "package",
                "supported": True,
                "workflow": "package-upload",
                "note": platform.package_note,
                "skills": [package_upload_status(platform, skill_name) for skill_name in skills],
            }
            platform_items.append(
                {
                    "name": platform.name,
                    "supported_modes": platform.supported_modes,
                    "status": mode_item,
                }
            )
            continue

        modes = [mode] if mode else platform.supported_modes
        for current_mode in modes:
            mode_item: dict[str, object] = {
                "mode": current_mode,
                "supported": current_mode in platform.supported_modes,
            }
            if current_mode == "skills":
                mode_item["install_root"] = (
                    str(platform.skills_install_root) if platform.skills_install_root else None
                )
                if platform.skills_payload_root is not None:
                    mode_item["payload_root"] = str(platform.skills_payload_root)
                if platform.skills_mode_adapter is not None:
                    mode_item["adapter"] = platform.skills_mode_adapter
            if current_mode == "project":
                mode_item["project_dir"] = str(resolved_project_dir) if resolved_project_dir else None
                mode_item["adapter"] = platform.project_adapter
                if resolved_project_dir is None:
                    mode_item["note"] = "Provide --project-dir <path> to inspect project-mode installation state."
            mode_item["skills"] = [
                skill_status_for_mode(platform, current_mode, resolved_project_dir, skill_name)
                for skill_name in skills
            ]
            platform_items.append(
                {
                    "name": platform.name,
                    "supported_modes": platform.supported_modes,
                    "status": mode_item,
                }
            )
    return {"skills": skills, "platforms": platform_items}


def print_list(platform_name: str | None, mode: str | None, project_dir: str | None, as_json: bool) -> None:
    if as_json:
        json_dump(list_payload(platform_name, mode, project_dir))
        return

    platform = get_platform(platform_name) if platform_name else None
    if platform is not None:
        print(f"Skills for platform {platform.name}:")
        supported_modes = ', '.join(platform.supported_modes) if platform.supported_modes else "package-upload only"
        print(f"Supported modes: {supported_modes}")
        if platform.package_only and platform.package_note:
            print(platform.package_note)
        if mode:
            print(f"Selected mode: {mode}")
        if project_dir:
            print(f"Project dir: {Path(project_dir).expanduser().resolve()}")
        print()

    for skill_dir in find_skill_dirs():
        print(f"- {skill_dir.name}")
        if platform is not None and platform.package_only:
            archive = package_archive_path(skill_dir.name)
            print("  packaged" if archive.exists() else "  not packaged")
        elif platform is not None and mode:
            status = skill_status_for_mode(
                platform,
                mode,
                Path(project_dir).expanduser().resolve() if project_dir else None,
                skill_dir.name,
            )
            if status["installed"] is True:
                print("  installed")
            elif status["installed"] is False:
                print("  not installed")
            else:
                print(f"  {status['reason']}")


def print_status(platform_name: str | None, mode: str | None, project_dir: str | None, as_json: bool) -> None:
    if as_json:
        json_dump(status_payload(platform_name, mode, project_dir))
        return

    payload = status_payload(platform_name, mode, project_dir)
    for platform in payload["platforms"]:
        print(f"Platform: {platform['name']}")
        supported_modes = ', '.join(platform['supported_modes']) if platform['supported_modes'] else "package-upload only"
        print(f"  supported modes: {supported_modes}")
        status = platform["status"]
        print(f"  mode: {status['mode']}")
        if status["mode"] == "skills" and status.get("install_root"):
            print(f"  install root: {status['install_root']}")
            if status.get("payload_root"):
                print(f"  payload root: {status['payload_root']}")
            if status.get("adapter"):
                print(f"  adapter: {status['adapter']}")
        if status["mode"] == "project":
            if status.get("project_dir"):
                print(f"  project dir: {status['project_dir']}")
            else:
                print("  project dir: <required>")
        if status["mode"] == "package" and status.get("note"):
            print(f"  note: {status['note']}")
        for skill in status["skills"]:
            state = skill["installed"]
            if status["mode"] == "package":
                rendered = "packaged" if state is True else "not packaged"
            elif state is True:
                rendered = "installed"
            elif state is False:
                rendered = "not installed"
            else:
                rendered = skill.get("reason", "unknown")
            print(f"  - {skill['name']}: {rendered}")
        print()


def handle_package(skills: list[Path]) -> None:
    ensure_valid_repo(profile="repo" if checkout_layout() else "distribution")
    for skill_dir in skills:
        destination = dist_dir() / f"{skill_dir.name}.skill.zip"
        create_skill_zip(skill_dir, destination)
        print(f"Packaged {skill_dir.name} -> {destination}")


CLI_OPTIONAL_SKILLS = {"altfins-market-researcher", "altfins-market-analyst"}
CLI_REPO_URL = "https://github.com/altfins-com/altfins-cli"


def handle_install(
    platform_name: str,
    mode: str,
    project_dir: str | None,
    skills: list[Path],
    force: bool,
) -> None:
    ensure_valid_repo(profile="distribution")
    target = resolve_target(platform_name, mode, project_dir)
    installed_names: list[str] = []
    for skill_dir in skills:
        if target.mode == "skills":
            if target.platform.skills_mode_adapter == "claude-code":
                agent_path, payload_dest = install_claude_code_skill(target, skill_dir, force=force)
                print(f"Installed {skill_dir.name} -> {agent_path}")
                print(f"Bundled skill payload -> {payload_dest}")
            else:
                destination = install_destination(target, skill_dir.name)
                copy_skill(skill_dir, destination, force=force)
                print(f"Installed {skill_dir.name} -> {destination}")
        else:
            install_project_skill(target, skill_dir, force=force)
            print(f"Installed {skill_dir.name} into project -> {target.project_dir}")
        installed_names.append(skill_dir.name)

    if any(name in CLI_OPTIONAL_SKILLS for name in installed_names) and shutil.which("af") is None:
        print(
            "Optional: install the altFINS CLI (af) for CLI-driven workflows: "
            f"{CLI_REPO_URL}"
        )


def handle_uninstall(
    platform_name: str,
    mode: str,
    project_dir: str | None,
    skills: list[Path],
    force: bool,
) -> None:
    target = resolve_target(platform_name, mode, project_dir)
    for skill_dir in skills:
        if target.mode == "skills":
            if target.platform.skills_mode_adapter == "claude-code":
                agent_path, payload_dest = uninstall_claude_code_skill(target, skill_dir.name, force=force)
                print(f"Uninstalled {skill_dir.name} <- {agent_path}")
                print(f"Removed bundled skill payload <- {payload_dest}")
            else:
                destination = install_destination(target, skill_dir.name)
                uninstall_skill(destination, force=force)
                print(f"Uninstalled {skill_dir.name} <- {destination}")
        else:
            uninstall_project_skill(target, skill_dir.name, force=force)
            print(f"Uninstalled {skill_dir.name} from project <- {target.project_dir}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Package and install altFINS skills for local agents.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List repo skills.")
    list_parser.add_argument(
        "--platform", choices=platform_choice_names(), help="Show support details for one platform."
    )
    list_parser.add_argument(
        "--mode",
        choices=INSTALL_MODES,
        help="Optional install mode to evaluate for the selected platform.",
    )
    list_parser.add_argument(
        "--project-dir",
        help="Project directory for project-mode platforms such as cursor or openclaw.",
    )
    list_parser.add_argument("--json", action="store_true", help="Print JSON output.")

    package_parser = subparsers.add_parser("package", help="Package one or more skills into dist/skills.")
    package_parser.add_argument("skills", nargs="*", help="Skill names to package.")
    package_parser.add_argument("--all", action="store_true", help="Package all discovered skills.")

    install_parser = subparsers.add_parser(
        "install", help="Install one or more skills into a local agent home or project."
    )
    install_parser.add_argument(
        "--platform", required=True, choices=platform_choice_names(), help="Target platform."
    )
    install_parser.add_argument(
        "--mode",
        choices=INSTALL_MODES,
        default="skills",
        help="Install mode: skills (default) or project.",
    )
    install_parser.add_argument(
        "--project-dir",
        help="Project directory for project-mode platforms such as cursor or openclaw.",
    )
    install_parser.add_argument("skills", nargs="*", help="Skill names to install.")
    install_parser.add_argument("--all", action="store_true", help="Install all discovered skills.")
    install_parser.add_argument("--force", action="store_true", help="Overwrite an existing install.")

    uninstall_parser = subparsers.add_parser(
        "uninstall", help="Uninstall one or more skills from a local agent home or project."
    )
    uninstall_parser.add_argument(
        "--platform", required=True, choices=platform_choice_names(), help="Target platform."
    )
    uninstall_parser.add_argument(
        "--mode",
        choices=INSTALL_MODES,
        default="skills",
        help="Install mode: skills (default) or project.",
    )
    uninstall_parser.add_argument(
        "--project-dir",
        help="Project directory for project-mode platforms such as cursor or openclaw.",
    )
    uninstall_parser.add_argument("skills", nargs="*", help="Skill names to uninstall.")
    uninstall_parser.add_argument("--all", action="store_true", help="Uninstall all discovered skills.")
    uninstall_parser.add_argument(
        "--force", action="store_true", help="Allow removal even if the destination looks unusual."
    )

    status_parser = subparsers.add_parser("status", help="Show install support and installed state.")
    status_parser.add_argument(
        "--platform", choices=platform_choice_names(), help="Show status for one platform."
    )
    status_parser.add_argument(
        "--mode",
        choices=INSTALL_MODES,
        help="Optional install mode to evaluate for the selected platform.",
    )
    status_parser.add_argument(
        "--project-dir",
        help="Project directory for project-mode platforms such as cursor or openclaw.",
    )
    status_parser.add_argument("--json", action="store_true", help="Print JSON output.")

    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    emit_platform_alias_warning(getattr(args, "platform", None))
    try:
        if args.command == "list":
            print_list(args.platform, args.mode, args.project_dir, args.json)
            return 0
        if args.command == "status":
            print_status(args.platform, args.mode, args.project_dir, args.json)
            return 0
        if args.command == "package":
            handle_package(resolve_skills(args.skills, args.all))
            return 0
        if args.command == "install":
            handle_install(
                args.platform,
                args.mode,
                args.project_dir,
                resolve_skills(args.skills, args.all),
                args.force,
            )
            return 0
        if args.command == "uninstall":
            handle_uninstall(
                args.platform,
                args.mode,
                args.project_dir,
                resolve_skills(args.skills, args.all),
                args.force,
            )
            return 0
        raise SkillsError(f"Unknown command: {args.command}")
    except SkillsError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
