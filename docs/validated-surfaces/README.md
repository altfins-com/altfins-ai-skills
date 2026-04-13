# Validated Surfaces

This directory stores checked-in snapshots that the skills can treat as stable local reference material.

## CLI Snapshot

The CLI snapshot is generated from the real `af` binary and includes:

- [cli/commands.json](cli/commands.json)
- [cli/manifest.json](cli/manifest.json)
- [cli/af-help.txt](cli/af-help.txt)
- selected subcommand help snapshots for markets, signals, analytics, OHLCV, news, TA, and TUI

Refresh it with:

```bash
python3 scripts/refresh_validated_surfaces.py --cli-bin /path/to/af --skip-mcp
```

## MCP Documented Surface

The MCP snapshot is a curated extract of the official documented surface and currently lives in:

- [mcp/documented-surface.json](mcp/documented-surface.json)

It intentionally captures only documented endpoint, transport, authentication, client setup targets, and capability families. Actual runtime tool names still need discovery from a connected MCP client.

Refresh it with:

```bash
python3 scripts/refresh_validated_surfaces.py --skip-cli
```

## Ground Rules

- Refresh snapshots only from the real local CLI or official altFINS sources.
- Do not hand-edit generated CLI snapshot files.
- When a checked-in snapshot and a live interface disagree, prefer the live interface and refresh the snapshot.
- Use [../validated-sources.md](../validated-sources.md) as the higher-level inventory of authoritative sources.
