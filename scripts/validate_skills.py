#!/usr/bin/env python3
"""Lightweight structural validator for altfins-ai-skills."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROOT_REQUIRED_FILES = [
    ROOT / "README.md",
    ROOT / ".gitignore",
    ROOT / "docs" / "repository-architecture.md",
    ROOT / "docs" / "skill-roadmap.md",
    ROOT / "docs" / "validated-sources.md",
    ROOT / "scripts" / "validate_skills.py",
]
SKILL_REQUIRED_RELATIVE = [
    Path("SKILL.md"),
    Path("agents/openai.yaml"),
    Path("references/sources.md"),
    Path("scripts"),
    Path("assets"),
]


def find_skill_dirs() -> list[Path]:
    return sorted(
        path
        for path in ROOT.iterdir()
        if path.is_dir() and path.name.startswith("altfins-") and (path / "SKILL.md").exists()
    )


def parse_frontmatter(skill_file: Path) -> dict[str, str]:
    text = skill_file.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise ValueError("missing YAML frontmatter")
    frontmatter = {}
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip()
    return frontmatter


def file_contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8")


def validate_openai_yaml(skill_dir: Path, errors: list[str]) -> None:
    path = skill_dir / "agents" / "openai.yaml"
    text = path.read_text(encoding="utf-8")
    required_snippets = [
        "interface:",
        'display_name: "',
        'short_description: "',
        'default_prompt: "',
        "policy:",
        "allow_implicit_invocation: false",
    ]
    for snippet in required_snippets:
        if snippet not in text:
            errors.append(f"{path}: missing required snippet {snippet!r}")
    skill_invocation = f"${skill_dir.name}"
    if skill_invocation not in text:
        errors.append(f"{path}: default_prompt must mention {skill_invocation}")


def validate_skill(skill_dir: Path, errors: list[str]) -> None:
    for relative in SKILL_REQUIRED_RELATIVE:
        if not (skill_dir / relative).exists():
            errors.append(f"{skill_dir / relative}: missing required skill path")

    readme_path = skill_dir / "README.md"
    if readme_path.exists():
        errors.append(f"{readme_path}: per-skill README files are not part of the current convention")

    skill_file = skill_dir / "SKILL.md"
    try:
        frontmatter = parse_frontmatter(skill_file)
    except ValueError as exc:
        errors.append(f"{skill_file}: {exc}")
        frontmatter = {}

    if frontmatter.get("name") != skill_dir.name:
        errors.append(f"{skill_file}: frontmatter name must match directory name {skill_dir.name!r}")
    if not frontmatter.get("description"):
        errors.append(f"{skill_file}: missing frontmatter description")

    validate_openai_yaml(skill_dir, errors)

    sources_file = skill_dir / "references" / "sources.md"
    if sources_file.exists() and "../../docs/validated-sources.md" not in sources_file.read_text(encoding="utf-8"):
        errors.append(f"{sources_file}: must link back to ../../docs/validated-sources.md")


def main() -> int:
    errors: list[str] = []

    for path in ROOT_REQUIRED_FILES:
        if not path.exists():
            errors.append(f"{path}: missing required repository file")

    skill_dirs = find_skill_dirs()
    if not skill_dirs:
        errors.append("No skill directories found at repository root")

    for skill_dir in skill_dirs:
        validate_skill(skill_dir, errors)

    if errors:
        print("VALIDATION FAILED")
        for issue in errors:
            print(f"- {issue}")
        return 1

    print("VALIDATION OK")
    print(f"Skills checked: {len(skill_dirs)}")
    for skill_dir in skill_dirs:
        print(f"- {skill_dir.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
