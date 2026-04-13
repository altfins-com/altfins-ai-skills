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
MCP_DOCS_URL = "https://altfins.com/crypto-market-and-analytical-data-api/documentation/mcp-server/"
MCP_DOCUMENTED_SURFACE = {
    "source_kind": "official-docs-curated",
    "docs_url": MCP_DOCS_URL,
    "endpoint": "https://mcp.altfins.com/mcp",
    "transport": "streamable-http",
    "authentication": {
        "header": "X-Api-Key",
        "scheme": "api-key",
    },
    "documented_capability_families": [
        "Screener",
        "Technical Analysis",
        "OHLCV Data",
        "Analytics History",
        "Signal Feed",
        "News",
        "Calendar Events",
        "Portfolio",
    ],
    "documented_client_setups": [
        "Claude Desktop",
        "VS Code (GitHub Copilot)",
        "Microsoft Copilot Studio",
    ],
    "runtime_tool_names_confirmed": False,
    "note": "Use a connected MCP client to discover actual runtime tool identifiers before naming or calling tools in a response.",
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


def refresh_cli(cli_bin: str, validated_on: str) -> None:
    CLI_ROOT.mkdir(parents=True, exist_ok=True)
    for filename, args in CLI_SNAPSHOTS.items():
        output = run_cli(cli_bin, args)
        (CLI_ROOT / filename).write_text(output, encoding="utf-8")

    commands_payload = json.loads((CLI_ROOT / "commands.json").read_text(encoding="utf-8"))
    manifest = {
        "validated_on": validated_on,
        "cli_bin": cli_bin,
        "top_level_command": commands_payload.get("command"),
        "top_level_children": [child["use"].split()[0] for child in commands_payload.get("children", [])],
        "global_flags": [flag["name"] for flag in commands_payload.get("flags", [])],
    }
    (CLI_ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def refresh_mcp(validated_on: str) -> None:
    MCP_ROOT.mkdir(parents=True, exist_ok=True)
    payload = dict(MCP_DOCUMENTED_SURFACE)
    payload["validated_on"] = validated_on
    (MCP_ROOT / "documented-surface.json").write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Refresh validated CLI and MCP surface snapshots.")
    parser.add_argument("--cli-bin", default="af", help="Path to the af CLI binary.")
    parser.add_argument("--skip-cli", action="store_true", help="Do not refresh CLI snapshots.")
    parser.add_argument("--skip-mcp", action="store_true", help="Do not refresh the MCP documented surface snapshot.")
    parser.add_argument(
        "--validated-on",
        default=str(date.today()),
        help="Override the validation date written into the snapshots.",
    )
    args = parser.parse_args(argv)

    if not args.skip_cli:
        refresh_cli(args.cli_bin, args.validated_on)
    if not args.skip_mcp:
        refresh_mcp(args.validated_on)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
