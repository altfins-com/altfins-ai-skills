#!/usr/bin/env python3
"""Smoke tests for scripts/skills.py."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "skills.py"
PYTHON = sys.executable
EXPECTED_SKILLS = [
    "altfins-market-analyst",
    "altfins-market-researcher",
    "altfins-query-builder",
]


def run_cli(*args: str, cwd: Path | None = None, env: dict[str, str] | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    command = [PYTHON, str(SCRIPT), *args]
    result = subprocess.run(command, cwd=cwd or ROOT, env=env, text=True, capture_output=True)
    if check and result.returncode != 0:
        raise AssertionError(
            f"Command failed: {' '.join(command)}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


class SkillsCliTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = Path(tempfile.mkdtemp(prefix="altfins-skills-test-"))
        self.homes = {
            "CODEX_HOME": self.tmpdir / "codex-home",
            "CLAUDE_HOME": self.tmpdir / "claude-home",
            "GEMINI_HOME": self.tmpdir / "gemini-home",
            "COPILOT_HOME": self.tmpdir / "copilot-home",
            "CURSOR_HOME": self.tmpdir / "cursor-home",
            "OPENCLAW_HOME": self.tmpdir / "openclaw-home",
            "ALTFINS_SKILLS_DIST_DIR": self.tmpdir / "dist" / "skills",
        }
        self.env = os.environ.copy()
        for key, value in self.homes.items():
            self.env[key] = str(value)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir)
        shutil.rmtree(self.tmpdir / "dist", ignore_errors=True)
        shutil.rmtree(ROOT / "dist", ignore_errors=True)

    def test_list_returns_all_skills(self) -> None:
        result = run_cli("list", "--json", env=self.env)
        payload = json.loads(result.stdout)
        self.assertEqual([item["name"] for item in payload], EXPECTED_SKILLS)

    def test_package_all_creates_expected_archives(self) -> None:
        run_cli("package", "--all", env=self.env)
        for skill_name in EXPECTED_SKILLS:
            archive_path = self.tmpdir / "dist" / "skills" / f"{skill_name}.skill.zip"
            self.assertTrue(archive_path.exists(), archive_path)
            with zipfile.ZipFile(archive_path) as archive:
                names = archive.namelist()
            self.assertTrue(all(name.startswith(f"{skill_name}/") for name in names), archive_path)
            self.assertIn(f"{skill_name}/SKILL.md", names)

    def test_install_status_and_uninstall_for_supported_platforms(self) -> None:
        for platform in ("codex", "claude", "gemini", "copilot"):
            run_cli("install", "--platform", platform, "altfins-market-analyst", env=self.env)
            result = run_cli("status", "--platform", platform, "--json", env=self.env)
            payload = json.loads(result.stdout)
            self.assertEqual(len(payload["platforms"]), 1)
            statuses = {item["name"]: item["installed"] for item in payload["platforms"][0]["skills"]}
            self.assertTrue(statuses["altfins-market-analyst"])
            run_cli("uninstall", "--platform", platform, "altfins-market-analyst", env=self.env)
            result = run_cli("status", "--platform", platform, "--json", env=self.env)
            payload = json.loads(result.stdout)
            statuses = {item["name"]: item["installed"] for item in payload["platforms"][0]["skills"]}
            self.assertFalse(statuses["altfins-market-analyst"])

    def test_unsupported_platforms_fail_cleanly(self) -> None:
        for platform in ("cursor", "openclaw"):
            result = run_cli(
                "install",
                "--platform",
                platform,
                "altfins-market-analyst",
                env=self.env,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("not supported in v1", result.stderr)

    def test_validator_failure_blocks_package(self) -> None:
        repo_copy = self.tmpdir / "repo-copy"
        shutil.copytree(
            ROOT,
            repo_copy,
            ignore=shutil.ignore_patterns(".git", "dist", "__pycache__", ".pytest_cache", "tmp"),
        )
        broken_readme = repo_copy / "altfins-market-analyst" / "README.md"
        broken_readme.write_text("# Broken\n")
        result = subprocess.run(
            [PYTHON, str(repo_copy / "scripts" / "skills.py"), "package", "altfins-market-analyst"],
            cwd=repo_copy,
            env=self.env,
            text=True,
            capture_output=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Repository validation failed", result.stderr)


if __name__ == "__main__":
    unittest.main()
