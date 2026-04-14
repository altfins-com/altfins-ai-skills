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
        self.project_dir = self.tmpdir / "project"
        self.project_dir.mkdir(parents=True, exist_ok=True)
        self.homes = {
            "CODEX_HOME": self.tmpdir / "codex-home",
            "CLAUDE_HOME": self.tmpdir / "claude-home",
            "GEMINI_HOME": self.tmpdir / "gemini-home",
            "COPILOT_HOME": self.tmpdir / "copilot-home",
            "ALTFINS_SKILLS_DIST_DIR": self.tmpdir / "dist" / "skills",
        }
        self.env = os.environ.copy()
        for key, value in self.homes.items():
            self.env[key] = str(value)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir)
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

    def test_install_status_and_uninstall_for_supported_skills_mode_platforms(self) -> None:
        for platform in ("codex", "gemini", "copilot"):
            run_cli("install", "--platform", platform, "altfins-market-analyst", env=self.env)
            result = run_cli("status", "--platform", platform, "--mode", "skills", "--json", env=self.env)
            payload = json.loads(result.stdout)
            statuses = {
                item["name"]: item["installed"]
                for item in payload["platforms"][0]["status"]["skills"]
            }
            self.assertTrue(statuses["altfins-market-analyst"])
            run_cli("uninstall", "--platform", platform, "altfins-market-analyst", env=self.env)
            result = run_cli("status", "--platform", platform, "--mode", "skills", "--json", env=self.env)
            payload = json.loads(result.stdout)
            statuses = {
                item["name"]: item["installed"]
                for item in payload["platforms"][0]["status"]["skills"]
            }
            self.assertFalse(statuses["altfins-market-analyst"])

    def test_install_status_and_uninstall_for_claude_code(self) -> None:
        run_cli("install", "--platform", "claude-code", "altfins-market-analyst", env=self.env)
        agent_path = self.homes["CLAUDE_HOME"] / "agents" / "altfins-market-analyst.md"
        payload_path = self.homes["CLAUDE_HOME"] / "skills" / "altfins-market-analyst" / "SKILL.md"
        self.assertTrue(agent_path.exists())
        self.assertTrue(payload_path.exists())
        agent_text = agent_path.read_text(encoding="utf-8")
        self.assertIn("Use the installed AltFINS skill bundle", agent_text)
        self.assertIn(str(payload_path), agent_text)

        result = run_cli("status", "--platform", "claude-code", "--mode", "skills", "--json", env=self.env)
        payload = json.loads(result.stdout)
        statuses = {
            item["name"]: item
            for item in payload["platforms"][0]["status"]["skills"]
        }
        self.assertTrue(statuses["altfins-market-analyst"]["installed"])
        self.assertTrue(statuses["altfins-market-analyst"]["agent_present"])
        self.assertTrue(statuses["altfins-market-analyst"]["payload_present"])

        run_cli("uninstall", "--platform", "claude-code", "altfins-market-analyst", env=self.env)
        self.assertFalse(agent_path.exists())
        self.assertFalse(payload_path.exists())

    def test_claude_alias_maps_to_claude_code(self) -> None:
        result = run_cli("status", "--platform", "claude", "--mode", "skills", "--json", env=self.env)
        self.assertIn("deprecated", result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["platforms"][0]["name"], "claude-code")

    def test_claude_cowork_uses_package_upload_flow(self) -> None:
        result = run_cli("status", "--platform", "claude-cowork", "--json", env=self.env)
        payload = json.loads(result.stdout)
        platform = payload["platforms"][0]
        self.assertEqual(platform["name"], "claude-cowork")
        self.assertEqual(platform["status"]["mode"], "package")
        self.assertIn("Customize > Skills", platform["status"]["note"])
        statuses = {
            item["name"]: item["installed"]
            for item in platform["status"]["skills"]
        }
        self.assertFalse(statuses["altfins-market-analyst"])

        install_result = run_cli(
            "install",
            "--platform",
            "claude-cowork",
            "altfins-market-analyst",
            env=self.env,
            check=False,
        )
        self.assertNotEqual(install_result.returncode, 0)
        self.assertIn("Customize > Skills", install_result.stderr)

        run_cli("package", "altfins-market-analyst", env=self.env)
        result = run_cli("status", "--platform", "claude-cowork", "--json", env=self.env)
        payload = json.loads(result.stdout)
        statuses = {
            item["name"]: item["installed"]
            for item in payload["platforms"][0]["status"]["skills"]
        }
        self.assertTrue(statuses["altfins-market-analyst"])

    def test_project_mode_install_status_and_uninstall_for_cursor(self) -> None:
        run_cli(
            "install",
            "--platform",
            "cursor",
            "--mode",
            "project",
            "--project-dir",
            str(self.project_dir),
            "altfins-market-analyst",
            env=self.env,
        )
        rule_path = self.project_dir / ".cursor" / "rules" / "altfins-market-analyst.mdc"
        payload_path = self.project_dir / ".altfins-skills" / "cursor" / "altfins-market-analyst" / "SKILL.md"
        self.assertTrue(rule_path.exists())
        self.assertTrue(payload_path.exists())
        result = run_cli(
            "status",
            "--platform",
            "cursor",
            "--mode",
            "project",
            "--project-dir",
            str(self.project_dir),
            "--json",
            env=self.env,
        )
        payload = json.loads(result.stdout)
        statuses = {
            item["name"]: item["installed"]
            for item in payload["platforms"][0]["status"]["skills"]
        }
        self.assertTrue(statuses["altfins-market-analyst"])
        run_cli(
            "uninstall",
            "--platform",
            "cursor",
            "--mode",
            "project",
            "--project-dir",
            str(self.project_dir),
            "altfins-market-analyst",
            env=self.env,
        )
        self.assertFalse(rule_path.exists())
        self.assertFalse(payload_path.exists())

    def test_project_mode_install_status_and_uninstall_for_openclaw(self) -> None:
        run_cli(
            "install",
            "--platform",
            "openclaw",
            "--mode",
            "project",
            "--project-dir",
            str(self.project_dir),
            "altfins-query-builder",
            env=self.env,
        )
        agents_path = self.project_dir / "AGENTS.md"
        payload_path = self.project_dir / ".altfins-skills" / "openclaw" / "altfins-query-builder" / "SKILL.md"
        self.assertTrue(agents_path.exists())
        self.assertTrue(payload_path.exists())
        self.assertIn("altfins-query-builder", agents_path.read_text(encoding="utf-8"))
        result = run_cli(
            "status",
            "--platform",
            "openclaw",
            "--mode",
            "project",
            "--project-dir",
            str(self.project_dir),
            "--json",
            env=self.env,
        )
        payload = json.loads(result.stdout)
        statuses = {
            item["name"]: item["installed"]
            for item in payload["platforms"][0]["status"]["skills"]
        }
        self.assertTrue(statuses["altfins-query-builder"])
        run_cli(
            "uninstall",
            "--platform",
            "openclaw",
            "--mode",
            "project",
            "--project-dir",
            str(self.project_dir),
            "altfins-query-builder",
            env=self.env,
        )
        self.assertFalse(payload_path.exists())
        self.assertFalse(agents_path.exists())

    def test_project_mode_requires_project_dir(self) -> None:
        result = run_cli(
            "install",
            "--platform",
            "cursor",
            "--mode",
            "project",
            "altfins-market-analyst",
            env=self.env,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Project mode requires --project-dir", result.stderr)

    def test_skills_mode_points_cursor_to_project_mode(self) -> None:
        result = run_cli(
            "install",
            "--platform",
            "cursor",
            "altfins-market-analyst",
            env=self.env,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("uses --mode project", result.stderr)

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

    def test_install_works_with_distribution_layout(self) -> None:
        repo_copy = self.tmpdir / "distribution-copy"
        shutil.copytree(
            ROOT,
            repo_copy,
            ignore=shutil.ignore_patterns(
                ".git",
                ".github",
                "bin",
                ".gitignore",
                "dist",
                "__pycache__",
                ".pytest_cache",
                "tmp",
            ),
        )
        env = self.env.copy()
        env["ALTFINS_SKILLS_ROOT"] = str(repo_copy)
        env["ALTFINS_SKILLS_DIST_DIR"] = str(self.tmpdir / "portable-dist")
        result = subprocess.run(
            [
                PYTHON,
                str(repo_copy / "scripts" / "skills.py"),
                "install",
                "--platform",
                "codex",
                "altfins-market-analyst",
            ],
            cwd=repo_copy,
            env=env,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(
            (self.homes["CODEX_HOME"] / "skills" / "altfins-market-analyst" / "SKILL.md").exists()
        )

    @unittest.skipUnless(os.name == "posix", "Unix launcher test only runs on POSIX hosts")
    def test_unix_wrapper_falls_back_to_python3(self) -> None:
        portable = self.tmpdir / "portable-python3"
        repo_dest = portable / "repo"
        shutil.copytree(
            ROOT,
            repo_dest,
            ignore=shutil.ignore_patterns(".git", "dist", "__pycache__", ".pytest_cache", "tmp"),
        )
        wrapper_path = portable / "altfins-skills"
        shutil.copy2(WRAPPER, wrapper_path)
        wrapper_path.chmod(0o755)

        fake_bin = self.tmpdir / "fake-bin"
        fake_bin.mkdir(parents=True, exist_ok=True)
        python3_path = fake_bin / "python3"
        python3_path.write_text(
            f"#!/bin/bash\nexec {PYTHON} \"$@\"\n",
            encoding="utf-8",
        )
        python3_path.chmod(0o755)

        env = self.env.copy()
        env.pop("ALTFINS_SKILLS_PYTHON", None)
        env["PATH"] = os.pathsep.join([str(fake_bin), "/usr/bin", "/bin"])
        result = run_cli("list", "--json", command=[str(wrapper_path)], env=env)
        payload = json.loads(result.stdout)
        self.assertEqual([item["name"] for item in payload], EXPECTED_SKILLS)

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
