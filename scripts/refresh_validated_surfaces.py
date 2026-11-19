#!/usr/bin/env python3
"""Refresh checked-in validated surface snapshots for altFINS CLI and MCP docs."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SURFACE_ROOT = ROOT / "docs" / "validated-surfaces"
CLI_ROOT = SURFACE_ROOT / "cli"
MCP_ROOT = SURFACE_ROOT / "mcp"
CLI_SNAPSHOTS = {
    "af-help.txt": ["--help"],
    "commands.json": ["commands", "-o", "json"],
    "analytics-history-help.txt": ["analytics", "history", "--help"],
    "markets-search-help.txt": ["markets", "search", "--help"],
    "news-list-help.txt": ["news", "list", "--help"],
    "ohlcv-history-help.txt": ["ohlcv", "history", "--help"],
    "signals-list-help.txt": ["signals", "list", "--help"],
    "ta-list-help.txt": ["ta", "list", "--help"],
    "tui-markets-help.txt": ["tui", "markets", "--help"],
}
def run_cli(cli_bin: str, args: list[str]) -> str:
    result = subprocess.run([cli_bin, *args], cwd=ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        raise SystemExit(
            f"CLI snapshot command failed: {' '.join([cli_bin, *args])}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    return result.stdout


def refresh_cli(cli_bin: str, commit: str, validated_on: str) -> None:
    CLI_ROOT.mkdir(parents=True, exist_ok=True)
    for filename, args in CLI_SNAPSHOTS.items():
        output = run_cli(cli_bin, args)
        (CLI_ROOT / filename).write_text(output, encoding="utf-8")

    commands_payload = json.loads((CLI_ROOT / "commands.json").read_text(encoding="utf-8"))
    manifest = {
        "validated_on": validated_on,
        "cli_version": run_cli(cli_bin, ["--version"]).strip(),
        "cli_commit": commit,
        "top_level_command": commands_payload.get("command"),
        "top_level_children": [child["use"].split()[0] for child in commands_payload.get("children", [])],
        "global_flags": [flag["name"] for flag in commands_payload.get("flags", [])],
    }
    (CLI_ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def refresh_mcp(capture: Path, validated_on: str) -> None:
    envelope = json.loads(capture.read_text(encoding="utf-8"))
    tools = envelope["result"]["tools"]
    if envelope["result"].get("nextCursor") or not tools or not all(
        isinstance(tool.get("name"), str) and isinstance(tool.get("inputSchema"), dict)
        for tool in tools
    ):
        raise ValueError("Expected a complete tools/list response with input schemas")
    snapshot = {"validated_on": validated_on, "endpoint": "https://mcp.altfins.com/mcp",
                "method": "tools/list", "tools": tools}
    (MCP_ROOT / "tools-list.json").write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Refresh observed altFINS interfaces.")
    parser.add_argument("--cli-bin", default="af")
    parser.add_argument("--cli-commit", help="Source commit used to build the CLI binary")
    parser.add_argument("--skip-cli", action="store_true")
    parser.add_argument("--mcp-capture", type=Path, help="Complete native tools/list response")
    parser.add_argument(
        "--validated-on",
        default=str(date.today()),
        help="Override the validation date written into the snapshots.",
    )
    args = parser.parse_args(argv)

    if not args.skip_cli:
        if not args.cli_commit:
            parser.error("--cli-commit is required when refreshing CLI snapshots")
        refresh_cli(args.cli_bin, args.cli_commit, args.validated_on)
    if args.mcp_capture:
        refresh_mcp(args.mcp_capture, args.validated_on)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
