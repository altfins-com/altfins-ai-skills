#!/usr/bin/env python3
"""Build a portable Windows bundle for altfins-ai-skills."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from skills_core import repo_root

EXCLUDES = {".git", "dist", "tmp", "__pycache__", ".pytest_cache"}


def should_skip(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    return any(part in EXCLUDES for part in relative.parts)


def copy_repo_payload(destination: Path) -> None:
    root = repo_root()
    repo_dest = destination / "repo"
    for path in sorted(root.rglob("*")):
        if should_skip(path, root):
            continue
        target = repo_dest / path.relative_to(root)
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)


def build_exe(dist_dir: Path, work_dir: Path, spec_dir: Path) -> Path:
    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--name",
        "altfins-skills",
        "--distpath",
        str(dist_dir),
        "--workpath",
        str(work_dir),
        "--specpath",
        str(spec_dir),
        str(repo_root() / "scripts" / "skills.py"),
    ]
    result = subprocess.run(command, cwd=repo_root())
    if result.returncode != 0:
        raise SystemExit(result.returncode)
    exe_path = dist_dir / "altfins-skills.exe"
    if not exe_path.exists():
        raise FileNotFoundError(exe_path)
    return exe_path


def zip_directory(source: Path, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source.rglob("*")):
            if path.is_dir():
                continue
            archive.write(path, arcname=str(path.relative_to(source)))


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Build the altfins-skills Windows release bundle.")
    parser.add_argument("--version", required=True)
    parser.add_argument("--output-dir", default=str(repo_root() / "dist" / "release"))
    args = parser.parse_args(argv)

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    zip_path = output_dir / "altfins-skills-windows.zip"

    with tempfile.TemporaryDirectory(prefix="altfins-skills-win-") as tmp:
        tmp_path = Path(tmp)
        exe = build_exe(
            tmp_path / "pyinstaller-dist",
            tmp_path / "pyinstaller-work",
            tmp_path / "pyinstaller-spec",
        )
        staging = tmp_path / "bundle"
        staging.mkdir(parents=True, exist_ok=True)
        shutil.copy2(exe, staging / "altfins-skills.exe")
        shutil.copy2(repo_root() / "bin" / "altfins-skills.cmd", staging / "altfins-skills.cmd")
        copy_repo_payload(staging)
        zip_directory(staging, zip_path)

    print(zip_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
