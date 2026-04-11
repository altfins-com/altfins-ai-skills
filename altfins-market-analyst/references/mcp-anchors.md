# Validated MCP Anchors

Validated on April 11, 2026.

## Official source

Primary reference: <https://altfins.com/crypto-market-and-analytical-data-api/documentation/mcp-server/>

## Confirmed MCP facts

### Endpoint

The official docs list the MCP endpoint as:

```text
https://mcp.altfins.com/mcp
```

### Transport

The same docs state that the endpoint supports Streamable HTTP MCP transport.

### Authentication

The official docs state that MCP requests require the API key header:

```text
X-Api-Key: YOUR_ALTFINS_API_KEY
```

### Documented capability families

The docs describe these tool families as automatically discoverable by compatible clients:

- Screener
- Technical Analysis
- OHLCV Data
- Analytics History
- Signal Feed
- News
- Calendar Events
- Portfolio

These names are safe to use as high-level categories. They are not a substitute for real runtime tool discovery.

## Client setup anchors

The official docs currently provide setup guidance for:

- Claude Desktop via `mcp-remote`
- VS Code with native HTTP MCP configuration
- Microsoft Copilot Studio via built-in MCP onboarding

## Safe usage guidance

- Discover real tools from the MCP client before naming or calling them.
- Use the official categories to decide which research route fits the task.
- If the task requires a capability outside the documented families, call that out explicitly.
- Keep analysis grounded in returned MCP data, not in generic market assumptions.
