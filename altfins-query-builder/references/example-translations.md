# Example Translations

Validated on April 12, 2026.

This file shows how to translate plain-English requests into safe, structured handoffs without inventing unsupported altFINS behavior.

## Example 1: Signal feed lookup

### User intent

```text
Show me bullish BTC and ETH signals since March 1.
```

### Best target family

- signal feed query

### Safe CLI-ready plan

- Command family: `af signals list`
- Required inputs: `--direction BULLISH`, `--symbols BTC,ETH`, `--from 2026-03-01`
- Example command:

```bash
af signals list --direction BULLISH --symbols BTC,ETH --from 2026-03-01
```

## Example 2: Historical indicator lookup

### User intent

```text
I want RSI history for BTC for the last month.
```

### Best target family

- analytics history

### Safe CLI-ready plan

- Command family: `af analytics history`
- Required inputs: symbol, analytics type, interval, date range
- Example command:

```bash
af analytics history --symbol BTC --type RSI14 --interval DAILY --from 2026-03-01 --to 2026-03-31
```

## Example 3: Market screening request

### User intent

```text
Find large-cap coins and show me RSI and MACD.
```

### Best target family

- market screening

### Safe output mode

This may start as a CLI-ready plan or as an interface-neutral brief if the user has not defined the coin universe or timeframe.

### Safe CLI-ready plan

```bash
af markets search --symbols BTC,ETH,SOL --interval DAILY --display-type MARKET_CAP,RSI14,MACD
```

### Caveat

If the user wants broader market filters rather than a fixed symbol list, prefer a request brief or validated JSON body planning rather than inventing unsupported shorthand flags.

## Example 4: Interactive browsing request

### User intent

```text
Open an interactive market browser for BTC.
```

### Best target family

- TUI market browsing

### Safe CLI-ready plan

```bash
af tui markets --symbol BTC
```

## Example 5: MCP-ready analysis request

### User intent

```text
Give me a complete technical analysis of SOL.
```

### Best target family

- MCP Technical Analysis family

### Safe MCP-ready prompt

```text
Use validated altFINS data only. Give me a complete technical analysis of SOL. Separate the answer into Objective, Validated Facts, Interpretation, Open Questions, and Suggested Next Checks.
```

## Example 6: Vague beginner request

### User intent

```text
What are the best coins right now?
```

### Best target family

- market screening, but underspecified

### Safe output mode

- interface-neutral research brief

### Safe handoff

Ask for or mark the missing dimensions explicitly:

- timeframe
- coin universe
- what “best” means: momentum, signals, technical analysis, or news-driven context

## Example 7: News-context request

### User intent

```text
Catch me up on Ethereum and whether anything important happened recently.
```

### Best target family

- news search or analysis-context brief

### Safe output mode

- CLI-ready if the user mainly wants news summaries
- interface-neutral if they also want interpretive analysis and the exact execution path is unclear

## Example 8: Interactive beginner request

### User intent

```text
I just want to browse the market and click around from BTC.
```

### Best target family

- TUI market browsing

### Safe CLI-ready plan

```bash
af tui markets --symbol BTC
```

## Example 9: Missing-slot indicator request

### User intent

```text
Show me MACD for SOL.
```

### Best target family

- analytics history

### Safe output mode

- interface-neutral or partially specified CLI-ready plan

### Missing inputs

- date range
- interval

## Usage rules

- Prefer CLI-ready outputs only when the command family and flags are already validated.
- Prefer MCP-ready prompts only when the user is clearly working through an MCP-capable client.
- Prefer an interface-neutral request brief when the user goal is clearer than the target interface.
