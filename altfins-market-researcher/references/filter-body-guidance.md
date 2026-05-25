# Filter and Body Guidance

This file provides conservative guidance for command families that may need more than simple flags.

## Markets Search

Validated surface:

- `--symbols`
- `--interval`
- `--display-type`
- `--coin-type`
- `--categories`
- `--trading-types`
- `--exchanges`
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

Guidance:

- use flag-first when the symbol list and display fields are straightforward
- stay flag-first for current simple screener filters such as support/resistance, 52-week high/low proximity, RSI divergence, new local highs/lows, MACD, exchange, trading type, category, coin type, ATH date bounds, and minimum market cap
- switch to `--filter` or `--stdin-json` when the request needs object-array filters such as `numericFilters`, `signalFilters`, `crossAnalyticFilters`, `candlestickPatternFilters`, or `analyticsComparisonsFilters`
- current simple body keys validated from OpenAPI are `coinTypeFilter`, `coinCategoryFilter`, `tradingTypeFilter`, `exchangeFilter`, `athDateBeforeFilter`, `athDateAfterFilter`, `supportResistanceFilter`, `supportResistanceLookBackIntervals`, `weekAnalytics52Filter`, `rsiDivergenceFilter`, `newLowInLastPeriodFilter`, `newHighInLastPeriodFilter`, `macdFilter`, `macdHistogramFilter`, and `minimumMarketCapValue`
- if a requested body key is not in the validated list, describe the body at the planning level instead of writing fake JSON

## Signals Feed

Validated surface:

- `--direction`
- `--signals`
- `--symbols`
- `--from`
- `--to`
- `--filter`
- `--stdin-json`

Guidance:

- stay flag-first for simple symbol, direction, and time-window requests
- use body planning when the user wants a more layered signal screen
- prefer `--dry-run` when handing off a more complex request

## Analytics History

Validated surface:

- `--symbol`
- `--type`
- `--interval`
- `--from`
- `--to`
- `--filter`
- `--stdin-json`

Guidance:

- use the direct flags when one symbol and one analytics type are known
- only move to body-planning guidance if the task clearly exceeds the simple history pattern
- avoid inventing analytics body fields when the direct flags already solve the request

## OHLCV History

Validated surface:

- `--symbol`
- `--interval`
- `--from`
- `--to`
- `--filter`
- `--stdin-json`

Guidance:

- keep this flag-first unless the user asks for a more unusual request shape
- use `-o json` or `-o csv` when the result is clearly meant for downstream use

## News List

Validated surface:

- `--from`
- `--to`
- `--filter`
- `--stdin-json`

Guidance:

- use flag-first for date-window searches
- use request-body planning only when the user wants a more complex news query than the obvious flags express

## Core safety rule

If field-level certainty is missing, write:

- the command family
- the reason a body shape is needed
- the preferred transport (`--filter` file or `--stdin-json`)
- an optional `--dry-run` preview step

Do not fill in speculative JSON keys just to make the example look complete.
