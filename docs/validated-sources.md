# Validated sources

Reviewed on 19 November 2026.

| Source | What it establishes |
| --- | --- |
| [Public endpoint documentation](https://altfins.com/crypto-market-and-analytical-data-api/documentation/) | Request semantics, entitlement, setup generation cost and pending behavior. |
| [Public OpenAPI download](https://altfins.com/crypto-market-and-analytical-data-api/openApi.json) | The static download still contains 16 public v2 paths. |
| [CLI v1.2.0 reconciled contract](https://github.com/altfins-com/altfins-cli/blob/v1.2.0/openapi/altfins-openapi.json) | All 21 public v2 operations and the corrected response shapes. The snapshot records its provenance. |
| [CLI command tree](validated-surfaces/cli/commands.json) and [manifest](validated-surfaces/cli/manifest.json) | Exact flags, required inputs, endpoint mappings and mutation metadata. Use the installed binary to check availability. |
| [Official CLI guide](https://altfins.com/crypto-market-and-analytical-data-api/documentation/altfins-cli/) | Installation, authentication and TUI navigation. |
| [MCP documentation](https://altfins.com/crypto-market-and-analytical-data-api/documentation/mcp-server/) and [documentation extract](validated-surfaces/mcp/documented-surface.json) | API-key access for direct clients and OAuth for hosted connectors. The docs listed Claude and ChatGPT directory integrations as in review. |
| [Native MCP tools/list](validated-surfaces/mcp/tools-list.json) | Sixteen tool names and their input schemas observed on the capture date. Discover tools for the current account before use. |

Public catalogue records expose instrument identifiers, names and blockchain platforms. The observed stock namespace is `CS_` and the forex namespace is `FX_`. The remaining IDs include crypto, fiat and tokens. Website screener parameters and MCP tool argument names can differ from public REST inputs.

Current signal rows supply `direction`. Older responses can carry `bullish`. Treat feed detection time, quote retrieval time and plan delay separately. Monthly quotas distinguish ordinary API credits and AI generation prompts.
