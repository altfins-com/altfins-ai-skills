# Validated CLI Anchors

Validated on April 11, 2026.

## Official source

Official CLI docs: <https://altfins.com/crypto-market-and-analytical-data-api/documentation/altfins-cli/>

## Locally observed command surface

The installed CLI was inspected with:

- `af --help`
- `af commands -o json`
- `af markets search --help`
- `af signals list --help`
- `af analytics history --help`
- `af ohlcv history --help`
- `af news list --help`
- `af ta list --help`

### Version note

The local binary reported `af version dev`, so the safest references for command behavior are the observed help output and `af commands -o json` metadata.

## Observed top-level commands

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

## Observed global flags

- `--dry-run`
- `--fields`
- `--no-color`
- `-o, --output`

## Observed command-to-endpoint mappings

From `af commands -o json`:

| Command | Method | Endpoint |
| --- | --- | --- |
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

## Observed query-surface examples

### `af markets search`

Observed flags include:

- `--symbols`
- `--interval`
- `--display-type`
- `--filter`
- `--stdin-json`
- `--page`
- `--size`
- `--sort`

### `af signals list`

Observed flags include:

- `--direction`
- `--signals`
- `--symbols`
- `--from`
- `--to`
- `--filter`
- `--stdin-json`

### `af analytics history`

Observed flags include:

- `--symbol`
- `--type`
- `--interval`
- `--from`
- `--to`
- `--filter`
- `--stdin-json`

## Safe usage guidance

- Verify the specific subcommand help before using any flag in an answer.
- Prefer `af commands -o json` when an agent needs command discovery or endpoint metadata.
- Prefer `--dry-run` when the request shape is part of the task.
