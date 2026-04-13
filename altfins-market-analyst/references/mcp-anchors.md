# Validated MCP Anchors

Validated on April 12, 2026.

Primary snapshot file:
- [../../docs/validated-surfaces/mcp/documented-surface.json](../../docs/validated-surfaces/mcp/documented-surface.json)

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
