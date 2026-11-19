# Validated MCP Anchors

Documentation and authenticated native discovery reviewed on 19 November 2026.

Primary snapshot file:
- [documented-surface.json](https://github.com/altfins-com/altfins-ai-skills/blob/v1.1.0/docs/validated-surfaces/mcp/documented-surface.json)

## Official source

Primary reference: <https://altfins.com/crypto-market-and-analytical-data-api/documentation/mcp-server/>

## Confirmed MCP Facts

### Endpoint

The documented surface snapshot lists this MCP endpoint:

```text
https://mcp.altfins.com/mcp
```

### Transport

The documented surface snapshot records Streamable HTTP MCP transport.

### Authentication

The documented surface snapshot records the required API key header:

```text
X-Api-Key: YOUR_ALTFINS_API_KEY
```

### Documented capability families

The official docs currently describe these capability families:

- Screener
- Technical Analysis
- OHLCV Data
- Analytics History
- Signal Feed
- News
- Calendar Events
- Portfolio

These names are safe to use as high-level categories. They are not a substitute for real runtime tool discovery.

## Client Setup Anchors

The documented surface snapshot currently includes setup guidance for:

- Claude Desktop
- VS Code (GitHub Copilot)
- Microsoft Copilot Studio

## Safe Usage Guidance

- Discover real tools from the MCP client before naming or calling them.
- Use the documented capability families to decide which research route fits the task.
- If the task requires a capability outside the documented families, call that out explicitly.
- Keep analysis grounded in returned MCP data, not in generic market assumptions.

## Observed tools

Use `symbols_getAvailableSymbols` for catalogue search and `screener_getPresetFilterTypes` for preset metadata when the current connection exposes them. `analytics_getAllLatestHistoryData`, `news_getCryptoNewsSources` and `news_getCryptoNewsMessages` provide latest metrics, news sources and richer crypto-news filters. Calendar accepts explicit symbol CSV. Portfolio is an opt-in account read. This capture contained no chart-pattern or AI setup tool. Consult the [dated input schemas](https://github.com/altfins-com/altfins-ai-skills/blob/v1.1.0/docs/validated-surfaces/mcp/tools-list.json).

Direct clients use an API key. The hosted OAuth connectors for Claude and ChatGPT were described as in review on the observation date.
