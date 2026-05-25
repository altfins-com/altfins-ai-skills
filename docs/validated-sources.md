# Validated Sources

Validated on April 12, 2026.

This document is the shared source inventory for the repository. Use it to decide which sources are authoritative before you extend any individual skill.

## Official altFINS Sources

### Public API documentation

URL: <https://altfins.com/crypto-market-and-analytical-data-api/documentation/>

Use this as the primary human-readable source for:

- public API feature families
- authentication expectations
- endpoint group descriptions
- common enums and public docs navigation

### OpenAPI schema

URL: <https://altfins.com/crypto-market-and-analytical-data-api/openApi.json>

Use this as the primary machine-readable source for:

- REST path names
- request and response schema shapes
- enum values
- payload field names

### MCP server documentation

URL: <https://altfins.com/crypto-market-and-analytical-data-api/documentation/mcp-server/>

Use this as the primary source for:

- MCP endpoint
- transport
- required authentication header
- documented high-level capability families
- client setup examples

### altFINS CLI documentation

URL: <https://altfins.com/crypto-market-and-analytical-data-api/documentation/altfins-cli/>

Use this as the primary public product documentation for:

- CLI installation and onboarding
- TUI usage and keyboard controls
- documented example workflows
- `af commands -o json` and `--dry-run` positioning

## Checked-In Validated Surfaces

The repository now carries local snapshots under [docs/validated-surfaces/README.md](validated-surfaces/README.md).

### CLI snapshot

Use the files under `docs/validated-surfaces/cli/` when you need a stable, local reference for the currently validated CLI surface.

The checked-in CLI snapshot includes:

- `commands.json`
- `manifest.json`
- `af-help.txt`
- selected subcommand help snapshots

### MCP documented surface snapshot

Use `docs/validated-surfaces/mcp/documented-surface.json` when you need a stable, local reference for the currently documented MCP surface.

This snapshot is intentionally limited to documented endpoint, transport, authentication, client setup targets, and capability families. Runtime tool identifiers still need discovery from the connected MCP client.

## Locally Observed CLI Surface

The local CLI surface was refreshed into `docs/validated-surfaces/cli/` on May 24, 2026 using a local `af` binary built from the current source.

Important note about the local binary:

- if the installed binary and the checked-in snapshot disagree, prefer the live local binary and refresh the snapshot
- if the live local binary and official docs disagree, call out the mismatch explicitly and prefer the interface you are actually targeting

## Key Validated Facts

### Authentication

- The public API uses API key authentication.
- The MCP server requires the `X-Api-Key` header on requests.
- The public docs and MCP docs both describe API-key based access.

### Public endpoint family shape

Validated REST paths are under the `/api/v2/public/` namespace.

Examples confirmed from the OpenAPI schema and the checked-in CLI snapshot include:

- `/api/v2/public/screener-data/search-requests`
- `/api/v2/public/analytics/search-requests`
- `/api/v2/public/analytics/types`
- `/api/v2/public/ohlcv/history-requests`
- `/api/v2/public/ohlcv/snapshot-requests`
- `/api/v2/public/signals-feed/search-requests`
- `/api/v2/public/signals-feed/signal-keys`
- `/api/v2/public/news-summary/search-requests`
- `/api/v2/public/news-summary/find-summary`
- `/api/v2/public/technical-analysis/data`
- `/api/v2/public/symbols`
- `/api/v2/public/intervals`

### Public schema details checked on May 24, 2026

The OpenAPI schema for `/api/v2/public/screener-data/search-requests` includes direct simple filter fields for support/resistance, 52-week high/low proximity, RSI divergence, new local highs/lows, MACD, exchange, trading type, category, coin type, ATH date bounds, and minimum market cap.

The OpenAPI schema for `/api/v2/public/signals-feed/search-requests` exposes signal result direction as a `bullish` boolean response field. CLI table/TUI workflows may derive a human-readable `direction` label from that field.

### Observed top-level CLI groups

Observed from the checked-in CLI snapshot:

- `analytics`
- `auth`
- `commands`
- `completion`
- `markets`
- `news`
- `ohlcv`
- `quota`
- `refs`
- `signals`
- `ta`
- `tui`

### Observed global CLI flags

Observed from the checked-in CLI snapshot:

- `--dry-run`
- `--fields`
- `--no-color`
- `-o, --output`

## How to Use This Document

- Use official docs and the OpenAPI schema when validating product capabilities.
- Use checked-in validated surface snapshots when you need a stable local contract.
- Use a live local CLI binary or connected MCP client when runtime truth matters more than the checked-in snapshot.
- If two sources disagree, prefer the more direct interface source for that layer and call out the mismatch explicitly.
