# Example Workflows

Validated on April 11, 2026.

This file provides example command patterns for `altfins-market-researcher`.

## Validation basis

These examples are grounded in:

- the official altFINS CLI documentation
- the real installed `af` help output
- the observed command metadata from `af commands -o json`

## Command family examples

### Market scan

Use when the user wants a quick screener-style overview for a known set of symbols.

```bash
af markets search --symbols BTC,ETH,SOL --interval DAILY --display-type MARKET_CAP,RSI14,MACD
```

### Signal scan

Use when the user wants recent signal feed events filtered by direction and time.

```bash
af signals list --direction BULLISH --from 2026-03-01
```

### Analytics history lookup

Use when the user wants historical values for a specific indicator or metric.

```bash
af analytics history --symbol BTC --type RSI14 --interval DAILY --from 2026-03-01 --to 2026-03-18
```

### OHLCV history export

Use when the user wants reusable candle data for downstream analysis.

```bash
af ohlcv history --symbol BTC --interval DAILY --from 2026-03-01 --to 2026-03-18 -o json
```

### Technical analysis lookup

Use when the user wants curated technical analysis entries rather than raw history.

```bash
af ta list --symbol SOL
```

### News lookup

Use when the user wants recent news summaries in a date window.

```bash
af news list --from 2026-03-01 --to 2026-03-18
```

## Safe wrapper patterns

### Dry-run wrapper

Use when the request body or endpoint mapping matters before execution.

```bash
af markets search --symbols BTC,ETH --display-type MARKET_CAP,RSI14 --dry-run -o json
```

### Export wrapper

Use when the workflow is meant for pipelines or handoff.

```bash
af signals list --direction BULLISH --from 2026-03-01 -o json
```

### Discovery wrapper

Use when the next agent needs validated command or endpoint discovery.

```bash
af commands -o json
```

## Usage rules

- Do not copy these examples blindly when the user intent points to a different command family.
- Re-check subcommand help if you are adding or changing flags.
- Prefer `--filter` or `--stdin-json` when the request shape becomes more complex than a few simple flags.
