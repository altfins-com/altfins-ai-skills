# Validated Sources

Validated on April 11, 2026.

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

- MCP endpoint: `https://mcp.altfins.com/mcp`
- transport: Streamable HTTP MCP
- required authentication header: `X-Api-Key`
- documented high-level tool families
- client setup examples for Claude Desktop, VS Code, and Microsoft Copilot Studio

### altFINS CLI documentation

URL: <https://altfins.com/crypto-market-and-analytical-data-api/documentation/altfins-cli/>

Use this as the primary public product documentation for:

- CLI installation and onboarding
- TUI usage and keyboard controls
- documented example workflows
- `af commands -o json` and `--dry-run` positioning

## Locally Observed CLI Surface

The real installed CLI was also inspected on April 11, 2026.

Observed commands:

- `af --help`
- `af commands -o json`
- `af markets search --help`
- `af signals list --help`
- `af analytics history --help`
- `af ohlcv history --help`
- `af news list --help`
- `af ta list --help`

### Important note about the local binary

The installed binary reported:

```text
af version dev
```

Because of that, prefer the observed help output and command metadata for the local command surface, and prefer the official docs and OpenAPI schema for product-level validation.

## Key Validated Facts

### Authentication

- The public API uses API key authentication.
- The MCP server requires the `X-Api-Key` header on requests.
- The public docs and MCP docs both describe API-key based access.

### Public endpoint family shape

Validated REST paths are under the `/api/v2/public/` namespace.

Examples confirmed from the OpenAPI schema and the installed CLI metadata include:

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

### Observed top-level CLI groups

Observed from `af --help`:

- `analytics`
- `auth`
- `commands`
- `markets`
- `news`
- `ohlcv`
- `quota`
- `refs`
- `signals`
- `ta`
- `tui`

### Observed global CLI flags

Observed from `af --help`:

- `--dry-run`
- `--fields`
- `--no-color`
- `-o, --output`

## How to Use This Document

- Use official docs and the OpenAPI schema when validating product capabilities.
- Use observed CLI help and `af commands -o json` when validating local CLI behavior.
- Use MCP docs for endpoint, authentication, transport, and high-level capability families.
- If two sources disagree, prefer the more direct interface source for that layer and call out the mismatch explicitly.
