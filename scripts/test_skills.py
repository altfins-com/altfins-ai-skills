#!/usr/bin/env python3
"""Smoke tests for altfins-skills installer surfaces."""

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
sys.path.insert(0, str(ROOT / "scripts"))
from skills_core import resolve_repo_root  # noqa: E402

SCRIPT = ROOT / "scripts" / "skills.py"
WRAPPER = ROOT / "bin" / "altfins-skills"
PYTHON = sys.executable
EXPECTED_SKILLS = [
    "altfins-market-analyst",
    "altfins-market-researcher",
    "altfins-query-builder",
]


def run_cli(
    *args: str,
    command: list[str] | None = None,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    cmd = command or [PYTHON, str(SCRIPT)]
    result = subprocess.run([*cmd, *args], cwd=cwd or ROOT, env=env, text=True, capture_output=True)
    if check and result.returncode != 0:
        raise AssertionError(
            f"Command failed: {' '.join([*cmd, *args])}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
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
        broken_readme.write_text("# Broken\n", encoding="utf-8")
        env = self.env.copy()
        env["ALTFINS_SKILLS_ROOT"] = str(repo_copy)
        env["ALTFINS_SKILLS_DIST_DIR"] = str(self.tmpdir / "broken-dist")
        result = subprocess.run(
            [PYTHON, str(repo_copy / "scripts" / "skills.py"), "package", "altfins-market-analyst"],
            cwd=repo_copy,
            env=env,
            text=True,
            capture_output=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Repository validation failed", result.stderr)

    @unittest.skipUnless(os.name == "posix", "Unix launcher test only runs on POSIX hosts")
    def test_unix_wrapper_works_with_installed_style_tree(self) -> None:
        portable = self.tmpdir / "portable"
        repo_dest = portable / "repo"
        shutil.copytree(
            ROOT,
            repo_dest,
            ignore=shutil.ignore_patterns(".git", "dist", "__pycache__", ".pytest_cache", "tmp"),
        )
        wrapper_path = portable / "altfins-skills"
        shutil.copy2(WRAPPER, wrapper_path)
        wrapper_path.chmod(0o755)
        result = run_cli("list", "--json", command=[str(wrapper_path)], env=self.env)
        payload = json.loads(result.stdout)
        self.assertEqual([item["name"] for item in payload], EXPECTED_SKILLS)

    def test_root_resolution_for_frozen_layout(self) -> None:
        exe_root = self.tmpdir / "frozen"
        repo_dest = exe_root / "repo"
        shutil.copytree(
            ROOT,
            repo_dest,
            ignore=shutil.ignore_patterns(".git", "dist", "__pycache__", ".pytest_cache", "tmp"),
        )
        resolved = resolve_repo_root(
            script_file=repo_dest / "scripts" / "skills.py",
            executable_path=exe_root / "altfins-skills.exe",
            frozen=True,
        )
        self.assertEqual(resolved, repo_dest.resolve())


if __name__ == "__main__":
    unittest.main()
