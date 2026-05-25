# Target Catalog

Validated on April 12, 2026.

This file maps common user intents to validated altFINS-facing target families.

Reference snapshots:
- [../../docs/validated-surfaces/cli/commands.json](../../docs/validated-surfaces/cli/commands.json)
- [../../docs/validated-surfaces/mcp/documented-surface.json](../../docs/validated-surfaces/mcp/documented-surface.json)

## Beginner-Facing Category Layer

Use one of these plain-English categories first:

| Beginner-facing category | What the user usually means |
| --- | --- |
| find coins | screen a market or shortlist candidates |
| check signals | look for bullish or bearish trigger-style results |
| look up indicator history | pull historical values for RSI, MACD, or similar metrics |
| look up price candles | get OHLCV history or snapshots |
| browse technical analysis | review curated technical analysis entries |
| get news or context | search summaries or inspect context around a coin |
| open an interactive browser | use the TUI instead of a one-shot export |
| ask for a full market analysis | produce a documented-MCP-ready analysis prompt or an interface-neutral research brief |

## Agent-Facing Routing Layer

| Beginner-facing category | Best validated target family | Preferred output mode |
| --- | --- | --- |
| find coins | market screening | CLI-ready or interface-neutral |
| check signals | signal feed query | CLI-ready |
| look up indicator history | analytics history | CLI-ready |
| look up price candles | OHLCV history or snapshot | CLI-ready |
| browse technical analysis | curated technical analysis | CLI-ready or TUI |
| get news or context | news search or summary lookup | CLI-ready or interface-neutral |
| open an interactive browser | TUI surfaces | CLI-ready |
| ask for a full market analysis | documented MCP capability families or an analysis-oriented brief | documented-MCP-ready or interface-neutral |

## CLI-Oriented Targets

| User intent | Validated CLI target | Endpoint family |
| --- | --- | --- |
| Screen coins by filters or display fields | `af markets search` | `/api/v2/public/screener-data/search-requests` |
| Discover available screener field ids | `af markets fields` | `/api/v2/public/screener-data/value-types` |
| Pull historical indicator or metric data | `af analytics history` | `/api/v2/public/analytics/search-requests` |
| Discover analytics type ids | `af analytics types` | `/api/v2/public/analytics/types` |
| Pull historical candles | `af ohlcv history` | `/api/v2/public/ohlcv/history-requests` |
| Pull latest candle snapshots | `af ohlcv snapshot` | `/api/v2/public/ohlcv/snapshot-requests` |
| Query signal feed results | `af signals list` | `/api/v2/public/signals-feed/search-requests` |
| Discover signal keys | `af signals keys` | `/api/v2/public/signals-feed/signal-keys` |
| Browse curated technical analysis | `af ta list` | `/api/v2/public/technical-analysis/data` |
| Search news summaries | `af news list` | `/api/v2/public/news-summary/search-requests` |
| Fetch a specific news summary | `af news get` | `/api/v2/public/news-summary/find-summary` |
| Discover intervals | `af refs intervals` | `/api/v2/public/intervals` |
| Discover symbols | `af refs symbols` | `/api/v2/public/symbols` |

Current `af markets search` direct flags cover simple REST screener filters for support/resistance, 52-week high/low proximity, RSI divergence, new local highs/lows, MACD, exchange, trading type, category, coin type, ATH date bounds, and minimum market cap. Use `--filter` or `--stdin-json` for object-array filters such as numeric, signal, cross-analytic, candlestick, and analytics-comparison filters.

## TUI-Oriented Targets

The validated CLI snapshot also exposes these TUI surfaces:

- `af tui markets`
- `af tui signals`
- `af tui ta`
- `af tui news`

Use TUI-oriented targets when the user wants interactive browsing rather than a one-shot export.

## MCP-Oriented Target Families

From the documented MCP surface snapshot, the safe high-level families are:

- Screener
- Technical Analysis
- OHLCV Data
- Analytics History
- Signal Feed
- News
- Calendar Events
- Portfolio

Treat these as validated capability families until a connected MCP client reveals the discovered runtime tool list.

## When to Stay Interface-Neutral

Stay interface-neutral if:

- the user goal is clear but the target interface is not
- required fields such as symbol, interval, or date range are missing
- the request would otherwise force you to invent flags, JSON keys, or runtime tool names
