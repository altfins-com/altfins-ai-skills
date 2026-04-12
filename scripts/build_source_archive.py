#!/usr/bin/env python3
"""Build a source tarball for altfins-ai-skills release assets."""

from __future__ import annotations

import argparse
import hashlib
import sys
import tarfile
from pathlib import Path

from skills_core import repo_root

EXCLUDES = {
    ".git",
    "dist",
    "tmp",
    "__pycache__",
    ".pytest_cache",
}


def should_skip(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    return any(part in EXCLUDES for part in relative.parts)


def build_archive(version: str, output_path: Path) -> tuple[Path, str]:
    root = repo_root()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    prefix = f"altfins-ai-skills-{version}"
    with tarfile.open(output_path, "w:gz") as archive:
        for path in sorted(root.rglob("*")):
            if should_skip(path, root):
                continue
            archive.add(path, arcname=str(Path(prefix) / path.relative_to(root)), recursive=False)
    digest = hashlib.sha256(output_path.read_bytes()).hexdigest()
    return output_path, digest


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Build a source tarball for Homebrew releases.")
    parser.add_argument("--version", required=True, help="Semantic version without the v prefix.")
    parser.add_argument("--output", required=True, help="Output tar.gz path.")
    parser.add_argument("--sha256-file", help="Optional file path for the computed sha256.")
    args = parser.parse_args(argv)

    output_path, digest = build_archive(args.version, Path(args.output).expanduser().resolve())
    if args.sha256_file:
        Path(args.sha256_file).expanduser().resolve().write_text(digest + "\n", encoding="utf-8")
    print(output_path)
    print(digest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
