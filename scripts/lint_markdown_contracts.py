#!/usr/bin/env python3
"""Lightweight markdown contract linter for altfins-ai-skills."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_ROOTS = [
    ROOT / "README.md",
    ROOT / "docs",
    ROOT / "altfins-market-analyst",
    ROOT / "altfins-market-researcher",
    ROOT / "altfins-query-builder",
]
LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.*)$")
CODE_FENCE_PATTERN = re.compile(r"^```")


def iter_markdown_files() -> list[Path]:
    files: list[Path] = []
    for root in MARKDOWN_ROOTS:
        if root.is_file() and root.suffix == ".md":
            files.append(root)
        elif root.is_dir():
            files.extend(sorted(root.rglob("*.md")))
    return sorted(files)


def strip_code_fences(text: str) -> str:
    kept_lines: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if CODE_FENCE_PATTERN.match(line.strip()):
            in_fence = not in_fence
            continue
        if not in_fence:
            kept_lines.append(line)
    return "\n".join(kept_lines)


def slugify_heading(text: str) -> str:
    value = text.strip().lower()
    value = re.sub(r"[`*_]", "", value)
    value = re.sub(r"[^a-z0-9\s-]", "", value)
    value = re.sub(r"\s+", "-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-")


def extract_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        match = HEADING_PATTERN.match(line)
        if match:
            slug = slugify_heading(match.group(2))
            if slug:
                anchors.add(slug)
    return anchors


def is_external(target: str) -> bool:
    return target.startswith(("http://", "https://", "mailto:"))


def validate_link(source: Path, target: str, errors: list[str], anchor_cache: dict[Path, set[str]]) -> None:
    if is_external(target):
        return

    path_part, anchor = (target.split("#", 1) + [""])[:2] if "#" in target else (target, "")

    if not path_part:
        destination = source
    else:
        destination = (source.parent / path_part).resolve()

    if path_part and not destination.exists():
        errors.append(f"{source}: broken link target {target!r}")
        return

    if anchor:
        if destination not in anchor_cache:
            anchor_cache[destination] = extract_anchors(destination)
        if anchor not in anchor_cache[destination]:
            errors.append(f"{source}: missing anchor #{anchor} in {destination}")


def validate_skill_references(skill_dir: Path, errors: list[str]) -> None:
    skill_file = skill_dir / "SKILL.md"
    text = skill_file.read_text(encoding="utf-8")
    link_targets = LINK_PATTERN.findall(strip_code_fences(text))
    if not link_targets:
        errors.append(f"{skill_file}: expected at least one markdown reference link")


def main() -> int:
    errors: list[str] = []
    anchor_cache: dict[Path, set[str]] = {}

    for path in iter_markdown_files():
        text = strip_code_fences(path.read_text(encoding="utf-8"))
        for target in LINK_PATTERN.findall(text):
            validate_link(path, target, errors, anchor_cache)

    for skill_dir in sorted(path for path in ROOT.iterdir() if path.is_dir() and path.name.startswith("altfins-")):
        if (skill_dir / "SKILL.md").exists():
            validate_skill_references(skill_dir, errors)

    if errors:
        print("MARKDOWN CONTRACT LINT FAILED")
        for issue in errors:
            print(f"- {issue}")
        return 1

    print("MARKDOWN CONTRACT LINT OK")
    print(f"Markdown files checked: {len(iter_markdown_files())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
