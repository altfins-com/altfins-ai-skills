# Intent Taxonomy

Use this taxonomy to classify beginner-friendly requests before producing a handoff.

## Category 1: Find coins

### What it sounds like

- find good coins
- screen the market
- show me strong setups
- find oversold names

### Validated target family

- market screening

### Required slots

- asset universe or symbol set
- timeframe or interval
- screening idea or signal concept
- desired output style

### Common missing inputs

- the timeframe is often missing
- the user may not define the coin universe
- the screening rule may be too vague to map directly

### Safe default output mode

- interface-neutral if the filters are vague
- CLI-ready if the user already gives enough specifics

## Category 2: Check signals

### What it sounds like

- show me bullish signals
- find bearish setups
- check if BTC has signals

### Validated target family

- signal feed query

### Required slots

- symbol or symbol set
- direction if relevant
- timeframe or date window

### Common missing inputs

- no date range
- no direction
- unclear whether the user wants one symbol or a screen

### Safe default output mode

- CLI-ready when symbols or direction are known
- interface-neutral when the signal criteria are too vague

## Category 3: Look up indicator history

### What it sounds like

- get RSI history
- show MACD for BTC
- check indicator values over time

### Validated target family

- analytics history

### Required slots

- symbol
- analytics type
- interval
- date range

### Common missing inputs

- missing interval
- missing date range
- missing exact analytics type id

### Safe default output mode

- CLI-ready once those four slots are known

## Category 4: Look up price candles

### What it sounds like

- show price candles
- get OHLCV history
- pull recent candle snapshots

### Validated target family

- OHLCV history or snapshot

### Required slots

- symbol
- interval
- whether history or snapshot is needed
- date range for history

### Safe default output mode

- CLI-ready when the user clearly wants data output

## Category 5: Browse technical analysis

### What it sounds like

- show technical analysis for SOL
- browse setups interactively
- open TA view

### Validated target family

- curated technical analysis
- TUI TA when the user wants interactive browsing

### Required slots

- symbol if narrowing the view
- browsing vs export intent

### Safe default output mode

- CLI-ready for one-shot lookup
- TUI-oriented for interactive requests

## Category 6: Get news or context

### What it sounds like

- what is the latest news on ETH
- get context for BTC
- show news summaries

### Validated target family

- news search or detail lookup

### Required slots

- asset or topic if known
- date window if the user cares about recency bounds
- summary vs detail intent

### Safe default output mode

- CLI-ready when a date-bounded search is clear
- interface-neutral when the user mainly wants analysis context

## Category 7: Open an interactive browser

### What it sounds like

- open a market browser
- let me browse signals interactively
- open the TUI

### Validated target family

- TUI surfaces

### Required slots

- preferred TUI screen
- optional seed symbol or filter

### Safe default output mode

- CLI-ready TUI launch command

## Category 8: Ask for a full market analysis

### What it sounds like

- give me a complete technical analysis
- what is the outlook for BTC
- analyze ETH with context

### Validated target family

- MCP analysis-oriented workflows or interface-neutral research brief

### Required slots

- asset or asset set
- timeframe
- desired analysis depth
- whether MCP is actually available

### Safe default output mode

- MCP-ready when the user is clearly in an MCP-capable environment
- otherwise interface-neutral
