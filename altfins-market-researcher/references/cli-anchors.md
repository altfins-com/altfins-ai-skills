# Validated CLI Anchors

Validated against CLI v1.2.0 on 19 November 2026.

Primary snapshot files:
- [commands.json](https://github.com/altfins-com/altfins-ai-skills/blob/v1.1.0/docs/validated-surfaces/cli/commands.json)
- [manifest.json](https://github.com/altfins-com/altfins-ai-skills/blob/v1.1.0/docs/validated-surfaces/cli/manifest.json)
- [af-help.txt](https://github.com/altfins-com/altfins-ai-skills/blob/v1.1.0/docs/validated-surfaces/cli/af-help.txt)

## Official source

Official CLI docs: <https://altfins.com/crypto-market-and-analytical-data-api/documentation/altfins-cli/>

## Checked-In Command Surface

The checked-in CLI snapshot was refreshed from the real local `af` binary.

## Observed top-level commands

- `analytics`
- `auth`
- `commands`
- `completion`
- `calendar`
- `portfolio`
- `patterns`
- `setups`
- `markets`
- `news`
- `ohlcv`
- `quota`
- `refs`
- `signals`
- `ta`
- `tui`

## Observed global flags

- `--dry-run`
- `--fields`
- `--no-color`
- `-o, --output`

## Observed command-to-endpoint mappings

From the checked-in `commands.json` snapshot:

| Command | Method | Endpoint |
| --- | --- | --- |
| `af markets preset` | `POST` | `/api/v2/public/screener-data/preset-filter` |
| `af patterns list` | `POST` | `/api/v2/public/patterns-data/search-requests` |
| `af setups list` | `GET` | `/api/v2/public/ai-trade-setup/search-requests` |
| `af setups report` | `GET` | `/api/v2/public/ai-trade-setup/{id}/report` |
| `af setups generate` | `GET` (billed write) | `/api/v2/public/ai-trade-setup/generate` |
| `af markets search` | `POST` | `/api/v2/public/screener-data/search-requests` |
| `af markets fields` | `GET` | `/api/v2/public/screener-data/value-types` |
| `af analytics history` | `POST` | `/api/v2/public/analytics/search-requests` |
| `af analytics types` | `GET` | `/api/v2/public/analytics/types` |
| `af ohlcv history` | `POST` | `/api/v2/public/ohlcv/history-requests` |
| `af ohlcv snapshot` | `POST` | `/api/v2/public/ohlcv/snapshot-requests` |
| `af signals list` | `POST` | `/api/v2/public/signals-feed/search-requests` |
| `af signals keys` | `GET` | `/api/v2/public/signals-feed/signal-keys` |
| `af news list` | `POST` | `/api/v2/public/news-summary/search-requests` |
| `af news get` | `POST` | `/api/v2/public/news-summary/find-summary` |
| `af ta list` | `GET` | `/api/v2/public/technical-analysis/data` |
| `af refs symbols` | `GET` | `/api/v2/public/symbols` |
| `af refs intervals` | `GET` | `/api/v2/public/intervals` |
| `af quota all` | `GET` | `/api/v2/public/all-available-permits` |
| `af quota current` | `GET` | `/api/v2/public/available-permits` |
| `af quota monthly` | `GET` | `/api/v2/public/monthly-available-permits` |

## Query-Surface Examples

The checked-in help snapshots confirm these common flag families:

### `af markets search`

- `--symbols`
- `--interval`
- `--display-type`
- `--coin-type`
- `--categories`
- `--trading-type` and `--exchange` take one value each
- `--asset-class stock|forex` resolves the catalogue universe
- `--percent-down-from-ath`
- `--ath-before`
- `--ath-after`
- `--support-resistance`
- `--support-resistance-lookback`
- `--week-52`
- `--rsi-divergence`
- `--new-low`
- `--new-high`
- `--macd`
- `--macd-histogram`
- `--min-market-cap`
- `--filter`
- `--stdin-json`
- `--page`
- `--size`
- `--sort`

### `af signals list`

- `--direction`
- `--signals`
- `--symbols`
- `--from`
- `--to`
- `--filter`
- `--stdin-json`

### `af analytics history`

- `--symbol`
- `--type`
- `--interval`
- `--from`
- `--to`
- `--filter`
- `--stdin-json`

## Safe Usage Guidance

- Prefer the checked-in snapshot when you need a stable local contract.
- Prefer the live local CLI when the current session depends on runtime truth.
- Prefer `af commands -o json` when an agent needs command discovery or endpoint metadata.
- Prefer `--dry-run` when the request shape is part of the task.
