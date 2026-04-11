# Golden Examples

Use these examples as quality benchmarks for `altfins-query-builder` outputs. They are not live-data answers. They show the expected clarity, routing quality, and handoff discipline.

## Example 1: Beginner signal request

### Input

```text
Show me bullish BTC and ETH signals since March 1.
```

### Golden output

```text
Best matching category: check signals
Validated target family: signal feed query
Safest output mode: CLI-ready request plan

Why this route fits:
- the request is specific enough for a validated CLI family
- symbols are known
- direction is known
- the date window is known

Recommended command:
af signals list --direction BULLISH --symbols BTC,ETH --from 2026-03-01

Optional preview step:
af signals list --direction BULLISH --symbols BTC,ETH --from 2026-03-01 --dry-run -o json

Notes:
- this stays inside a validated command family
- no extra JSON body is needed for this request shape
```

### Why this is good

- it classifies the request before jumping to a command
- it uses a validated command family
- it keeps the handoff executable without inventing extra parameters

## Example 2: Vague beginner screener request

### Input

```text
What are the best coins right now?
```

### Golden output

```text
Best matching category: find coins
Validated target family: market screening
Safest output mode: interface-neutral research brief

The request is still underspecified. Before turning this into a concrete CLI or MCP request, clarify or record these missing inputs:
- timeframe
- coin universe
- what “best” means for this task: momentum, technical setups, signals, or context-driven opportunities

Suggested brief:
- Goal: identify promising coins
- Candidate family: market screening
- Missing inputs: timeframe, universe, ranking logic
- Next step: ask one clarifying question or proceed with explicit assumptions
```

### Why this is good

- it does not pretend the user gave enough detail
- it still routes the request to the right validated family
- it chooses an interface-neutral brief instead of a fake concrete query

## Example 3: Interactive browsing request

### Input

```text
Open a browser where I can explore BTC.
```

### Golden output

```text
Best matching category: open an interactive browser
Validated target family: TUI market browsing
Safest output mode: CLI-ready request plan

Recommended command:
af tui markets --symbol BTC

Reason:
- the request is clearly interactive
- a TUI launch fits better than a one-shot export
```

### Why this is good

- it respects the interactive intent
- it avoids routing the user to a non-interactive export command

## Example 4: MCP-oriented analysis request

### Input

```text
Give me a complete technical analysis of SOL.
```

### Golden output

```text
Best matching category: ask for a full market analysis
Validated target family: MCP Technical Analysis family
Safest output mode: MCP-ready prompt

Suggested prompt:
Use validated altFINS data only. Give me a complete technical analysis of SOL. Separate the answer into Objective, Validated Facts, Interpretation, Open Questions, and Suggested Next Checks.

Reason:
- the request is analysis-oriented rather than export-oriented
- the prompt stays inside documented MCP capability families
- it avoids inventing runtime tool names
```

### Why this is good

- it chooses the correct output mode
- it gives a reusable prompt with strong evidence-label discipline
- it stays conservative about MCP runtime details
