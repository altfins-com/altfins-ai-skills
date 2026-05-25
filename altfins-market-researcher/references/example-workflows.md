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

#### Simple flags version

```bash
af markets search --symbols BTC,ETH,SOL --interval DAILY --display-type MARKET_CAP,RSI14,MACD
```

#### Screener filter flags version

```bash
af markets search --coin-type REGULAR --support-resistance BROKEN_ABOVE_RESISTANCE --rsi-divergence BULLISH --display-type MARKET_CAP,RSI14,PRICE_CHANGE_1W
```

#### Body-planning version

```text
Use af markets search with --filter @market-screen.json or --stdin-json when the request needs object-array filters such as numericFilters, signalFilters, crossAnalyticFilters, candlestickPatternFilters, or analyticsComparisonsFilters. If the exact body keys are not validated for the current task, describe the JSON at the planning level and add a --dry-run preview step.
```

### Signal scan

Use when the user wants recent signal feed events filtered by direction and time.

#### Simple flags version

```bash
af signals list --direction BULLISH --from 2026-03-01
```

#### Body-planning version

```text
Use af signals list with --filter or --stdin-json when the request combines multiple signal constraints that are awkward to express as simple flags. Add --dry-run when handing the request to another agent.
```

### Analytics history lookup

Use when the user wants historical values for a specific indicator or metric.

#### Simple flags version

```bash
af analytics history --symbol BTC --type RSI14 --interval DAILY --from 2026-03-01 --to 2026-03-18
```

#### Body-planning version

```text
Stay flag-first for normal one-symbol one-metric history lookups. Only move to --filter or --stdin-json planning when the request clearly exceeds that direct pattern.
```

### OHLCV history export

Use when the user wants reusable candle data for downstream analysis.

#### Simple flags version

```bash
af ohlcv history --symbol BTC --interval DAILY --from 2026-03-01 --to 2026-03-18 -o json
```

#### Body-planning version

```text
Keep OHLCV history flag-first unless the task explicitly calls for a more unusual request shape. Prefer output-mode guidance over speculative body design.
```

### Technical analysis lookup

Use when the user wants curated technical analysis entries rather than raw history.

```bash
af ta list --symbol SOL
```

### News lookup

Use when the user wants recent news summaries in a date window.

#### Simple flags version

```bash
af news list --from 2026-03-01 --to 2026-03-18
```

#### Body-planning version

```text
Use af news list with --filter or --stdin-json only when the date window alone is not enough and the query shape needs a richer request body. If the exact body keys are not validated for the task, describe the body plan instead of fabricating it.
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
- If the exact body schema is not validated for the task, write a planning note instead of fake JSON.
