#!/usr/bin/env python3
"""Release artifact smoke tests for altfins-ai-skills."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run([PYTHON, *args], cwd=cwd or ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        raise AssertionError(
            f"Command failed: {' '.join([PYTHON, *args])}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


class ReleaseAssetTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = Path(tempfile.mkdtemp(prefix="altfins-skills-release-"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir)
        shutil.rmtree(ROOT / "dist", ignore_errors=True)

    def test_source_archive_shape(self) -> None:
        output = self.tmpdir / "altfins-ai-skills-src.tar.gz"
        sha = self.tmpdir / "altfins-ai-skills-src.sha256"
        run(
            "scripts/build_source_archive.py",
            "--version",
            "0.1.0-test",
            "--output",
            str(output),
            "--sha256-file",
            str(sha),
        )
        self.assertTrue(output.exists())
        self.assertTrue(sha.exists())
        prefix = "altfins-ai-skills-0.1.0-test/"
        with tarfile.open(output, "r:gz") as archive:
            names = archive.getnames()
            extract_dir = self.tmpdir / "extracted"
            archive.extractall(extract_dir)
        self.assertIn(prefix + "README.md", names)
        self.assertIn(prefix + "scripts/skills.py", names)
        self.assertIn(prefix + "altfins-market-analyst/SKILL.md", names)
        self.assertTrue(all(not name.startswith(prefix + ".git/") for name in names))
        extracted_root = extract_dir / prefix.rstrip("/")
        result = subprocess.run(
            [PYTHON, str(extracted_root / "scripts" / "validate_skills.py"), "--profile", "distribution"],
            cwd=extracted_root,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_formula_shape(self) -> None:
        output = self.tmpdir / "altfins-skills.rb"
        run(
            "scripts/render_homebrew_formula.py",
            "--version",
            "0.1.0",
            "--url",
            "https://github.com/altfins-com/altfins-ai-skills/releases/download/v0.1.0/altfins-ai-skills-src.tar.gz",
            "--sha256",
            "1234abcd",
            "--output",
            str(output),
        )
        text = output.read_text(encoding="utf-8")
        self.assertIn('class AltfinsSkills < Formula', text)
        self.assertIn('bin/"altfins-skills"', text)
        self.assertIn('ALTFINS_SKILLS_ROOT', text)
        self.assertIn('python3.12', text)
        self.assertIn('1234abcd', text)

    @unittest.skipUnless(sys.platform.startswith("win"), "Windows bundle smoke only runs on Windows")
    def test_windows_bundle_shape(self) -> None:
        output_dir = self.tmpdir / "release"
        run(
            "scripts/build_windows_bundle.py",
            "--version",
            "0.1.0",
            "--output-dir",
            str(output_dir),
        )
        bundle = output_dir / "altfins-skills-windows.zip"
        self.assertTrue(bundle.exists())
        with zipfile.ZipFile(bundle) as archive:
            names = archive.namelist()
        self.assertIn("altfins-skills.exe", names)
        self.assertIn("altfins-skills.cmd", names)
        self.assertIn("repo/README.md", names)
        self.assertIn("repo/scripts/skills.py", names)
        self.assertIn("repo/altfins-market-researcher/SKILL.md", names)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run release artifact smoke tests.")
    parser.parse_args(argv)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ReleaseAssetTest)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
