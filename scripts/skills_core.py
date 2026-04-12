#!/usr/bin/env python3
"""Core installer logic for altfins-ai-skills."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import zipfile
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

ROOT_OVERRIDE_ENV = "ALTFINS_SKILLS_ROOT"
DIST_OVERRIDE_ENV = "ALTFINS_SKILLS_DIST_DIR"
KNOWN_SKILLS = [
    "altfins-market-analyst",
    "altfins-market-researcher",
    "altfins-query-builder",
]


class SkillsError(Exception):
    """Raised for user-facing CLI failures."""


@dataclass(frozen=True)
class PlatformSpec:
    name: str
    install_root: Path | None
    supported: bool
    unsupported_reason: str | None = None


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


def dist_dir() -> Path:
    override = os.environ.get(DIST_OVERRIDE_ENV)
    if override:
        return Path(override).expanduser().resolve()
    return repo_root() / "dist" / "skills"


def validator_commands() -> list[list[str]]:
    root = repo_root()
    return [
        [sys.executable, str(root / "scripts" / "validate_skills.py")],
        [sys.executable, str(root / "scripts" / "lint_markdown_contracts.py")],
    ]


def platform_specs() -> dict[str, PlatformSpec]:
    codex_home = _expand_home(os.environ.get("CODEX_HOME", "~/.codex"))
    claude_home = _env_home("CLAUDE_HOME", "~/.claude")
    gemini_home = _env_home("GEMINI_HOME", "~/.gemini")
    copilot_home = _env_home("COPILOT_HOME", "~/.copilot")
    cursor_home = _env_home("CURSOR_HOME", "~/.cursor")
    openclaw_home = _env_home("OPENCLAW_HOME", "~/.openclaw")
    return {
        "codex": PlatformSpec("codex", codex_home / "skills", True),
        "claude": PlatformSpec("claude", claude_home / "skills", True),
        "gemini": PlatformSpec("gemini", gemini_home / "skills", True),
        "copilot": PlatformSpec("copilot", copilot_home / "skills", True),
        "cursor": PlatformSpec(
            "cursor",
            cursor_home / "rules",
            False,
            "direct skill installation is not supported in v1 because skills-only mode does not include Cursor rules-based project integration",
        ),
        "openclaw": PlatformSpec(
            "openclaw",
            openclaw_home / "skills",
            False,
            "direct skill installation is not supported in v1 because skills-only mode does not include AGENTS-based project integration",
        ),
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


def ensure_valid_repo() -> None:
    for command in validator_commands():
        result = subprocess.run(command, cwd=repo_root())
        if result.returncode != 0:
            joined = " ".join(command)
            raise SkillsError(f"Repository validation failed while running: {joined}")


def require_supported_platform(name: str) -> PlatformSpec:
    specs = platform_specs()
    if name not in specs:
        raise SkillsError(f"Unknown platform: {name}")
    spec = specs[name]
    if not spec.supported:
        raise SkillsError(
            f"Platform {name} is recognized but not supported in v1: {spec.unsupported_reason}"
        )
    return spec


def get_platform(name: str) -> PlatformSpec:
    specs = platform_specs()
    if name not in specs:
        raise SkillsError(f"Unknown platform: {name}")
    return specs[name]


def install_destination(platform: PlatformSpec, skill_name: str) -> Path:
    if platform.install_root is None:
        raise SkillsError(f"Platform {platform.name} does not have an install root in v1.")
    return platform.install_root / skill_name


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


def platform_status_for_skill(platform: PlatformSpec, skill_name: str) -> dict[str, object]:
    destination = install_destination(platform, skill_name) if platform.install_root else None
    return {
        "name": platform.name,
        "supported": platform.supported,
        "install_root": str(platform.install_root) if platform.install_root else None,
        "installed": destination.exists() if destination else False,
        "reason": platform.unsupported_reason,
    }


def list_payload(platform_name: str | None = None) -> list[dict[str, object]]:
    skills = find_skill_dirs()
    specs = platform_specs()
    selected_platform = specs.get(platform_name) if platform_name else None
    payload: list[dict[str, object]] = []
    for skill_dir in skills:
        item: dict[str, object] = {"name": skill_dir.name}
        if selected_platform:
            item["platform"] = platform_status_for_skill(selected_platform, skill_dir.name)
        payload.append(item)
    return payload


def status_payload(platform_name: str | None = None) -> dict[str, object]:
    skills = skill_names()
    specs = platform_specs()
    selected = [specs[platform_name]] if platform_name else [specs[name] for name in sorted(specs)]
    return {
        "skills": skills,
        "platforms": [
            {
                "name": platform.name,
                "supported": platform.supported,
                "install_root": str(platform.install_root) if platform.install_root else None,
                "reason": platform.unsupported_reason,
                "skills": [
                    {
                        "name": skill_name,
                        "installed": install_destination(platform, skill_name).exists()
                        if platform.install_root and platform.supported
                        else False,
                    }
                    for skill_name in skills
                ],
            }
            for platform in selected
        ],
    }


def print_list(platform_name: str | None, as_json: bool) -> None:
    if as_json:
        json_dump(list_payload(platform_name))
        return

    if platform_name:
        platform = get_platform(platform_name)
        print(f"Skills for platform {platform.name}:")
        if platform.supported:
            print(f"Install root: {platform.install_root}")
        else:
            print(f"Status: not supported in v1 ({platform.unsupported_reason})")
        print()

    for skill_dir in find_skill_dirs():
        print(f"- {skill_dir.name}")
        if platform_name:
            platform = get_platform(platform_name)
            if platform.supported and platform.install_root is not None:
                installed = install_destination(platform, skill_dir.name).exists()
                suffix = "installed" if installed else "not installed"
                print(f"  {suffix} -> {install_destination(platform, skill_dir.name)}")
            else:
                print(f"  {platform.unsupported_reason}")


def print_status(platform_name: str | None, as_json: bool) -> None:
    if as_json:
        json_dump(status_payload(platform_name))
        return

    specs = platform_specs()
    selected = [specs[platform_name]] if platform_name else [specs[name] for name in sorted(specs)]
    for platform in selected:
        print(f"Platform: {platform.name}")
        if platform.supported:
            print(f"  install root: {platform.install_root}")
            for skill_name in skill_names():
                installed = install_destination(platform, skill_name).exists()
                print(f"  - {skill_name}: {'installed' if installed else 'not installed'}")
        else:
            print(f"  not supported in v1: {platform.unsupported_reason}")
        print()


def handle_package(skills: list[Path]) -> None:
    ensure_valid_repo()
    for skill_dir in skills:
        destination = dist_dir() / f"{skill_dir.name}.skill.zip"
        create_skill_zip(skill_dir, destination)
        print(f"Packaged {skill_dir.name} -> {destination}")


def handle_install(platform_name: str, skills: list[Path], force: bool) -> None:
    ensure_valid_repo()
    platform = require_supported_platform(platform_name)
    for skill_dir in skills:
        destination = install_destination(platform, skill_dir.name)
        copy_skill(skill_dir, destination, force=force)
        print(f"Installed {skill_dir.name} -> {destination}")


def handle_uninstall(platform_name: str, skills: list[Path], force: bool) -> None:
    platform = require_supported_platform(platform_name)
    for skill_dir in skills:
        destination = install_destination(platform, skill_dir.name)
        uninstall_skill(destination, force=force)
        print(f"Uninstalled {skill_dir.name} <- {destination}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Package and install altFINS skills for local agents.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List repo skills.")
    list_parser.add_argument(
        "--platform", choices=sorted(platform_specs()), help="Show support details for one platform."
    )
    list_parser.add_argument("--json", action="store_true", help="Print JSON output.")

    package_parser = subparsers.add_parser("package", help="Package one or more skills into dist/skills.")
    package_parser.add_argument("skills", nargs="*", help="Skill names to package.")
    package_parser.add_argument("--all", action="store_true", help="Package all discovered skills.")

    install_parser = subparsers.add_parser(
        "install", help="Install one or more skills into a local agent home."
    )
    install_parser.add_argument(
        "--platform", required=True, choices=sorted(platform_specs()), help="Target platform."
    )
    install_parser.add_argument("skills", nargs="*", help="Skill names to install.")
    install_parser.add_argument("--all", action="store_true", help="Install all discovered skills.")
    install_parser.add_argument("--force", action="store_true", help="Overwrite an existing installed skill.")

    uninstall_parser = subparsers.add_parser(
        "uninstall", help="Uninstall one or more skills from a local agent home."
    )
    uninstall_parser.add_argument(
        "--platform", required=True, choices=sorted(platform_specs()), help="Target platform."
    )
    uninstall_parser.add_argument("skills", nargs="*", help="Skill names to uninstall.")
    uninstall_parser.add_argument("--all", action="store_true", help="Uninstall all discovered skills.")
    uninstall_parser.add_argument(
        "--force", action="store_true", help="Allow removal even if the destination looks unusual."
    )

    status_parser = subparsers.add_parser("status", help="Show install support and installed state.")
    status_parser.add_argument(
        "--platform", choices=sorted(platform_specs()), help="Show status for one platform."
    )
    status_parser.add_argument("--json", action="store_true", help="Print JSON output.")

    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        if args.command == "list":
            print_list(args.platform, args.json)
            return 0
        if args.command == "status":
            print_status(args.platform, args.json)
            return 0
        if args.command == "package":
            handle_package(resolve_skills(args.skills, args.all))
            return 0
        if args.command == "install":
            handle_install(args.platform, resolve_skills(args.skills, args.all), args.force)
            return 0
        if args.command == "uninstall":
            handle_uninstall(args.platform, resolve_skills(args.skills, args.all), args.force)
            return 0
        raise SkillsError(f"Unknown command: {args.command}")
    except SkillsError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
