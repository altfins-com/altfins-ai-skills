# Target Catalog

Validated on April 11, 2026.

This file maps common user intents to validated altFINS-facing target families.

## CLI-oriented targets

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

## TUI-oriented targets

The installed CLI also exposes these validated TUI surfaces:

- `af tui markets`
- `af tui signals`
- `af tui ta`
- `af tui news`

Use TUI-oriented targets when the user wants interactive browsing rather than a one-shot export.

## MCP-oriented target families

From the official altFINS MCP docs, the safe high-level families are:

- Screener
- Technical Analysis
- OHLCV Data
- Analytics History
- Signal Feed
- News
- Calendar Events
- Portfolio

Treat these as category labels until the actual MCP client reveals the discovered tool list.

## When to stay interface-neutral

Stay interface-neutral if:

- the user goal is clear but the target interface is not
- required fields such as symbol, interval, or date range are missing
- the request would otherwise force you to invent flags, JSON keys, or MCP methods
