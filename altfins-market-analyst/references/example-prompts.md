# Example Prompts

Validated on April 11, 2026.

This file provides prompt material for `altfins-market-analyst`.

## Official prompt anchors

The following user-style prompts are explicitly documented in the official altFINS MCP documentation as examples of MCP usage:

- `Give me a complete technical analysis of SOL`
- `What is the current technical outlook for BTC?`
- `Is ETH bullish or bearish right now?`
- `Find coins with RSI below 30 and bullish MACD`
- `Show me the latest crypto news about Ethereum`

Use these as validated examples of the kinds of natural-language requests the MCP server is intended to support.

## Safe local wrapper prompts

These are repository-local prompt wrappers built on top of the official prompt anchors. They are safe because they do not invent new tool names or undocumented capabilities.

### Full analysis wrapper

```text
Use validated altFINS data only. Give me a complete technical analysis of SOL. Separate the answer into Objective, Validated Facts, Interpretation, Open Questions, and Suggested Next Checks.
```

### Outlook wrapper

```text
Use validated altFINS data only. What is the current technical outlook for BTC on the daily timeframe? Clearly separate facts from interpretation.
```

### Market scan wrapper

```text
Use validated altFINS data only. Find coins with RSI below 30 and bullish MACD, then summarize the strongest candidates with clear reasoning and open questions.
```

### Context-aware wrapper

```text
Use validated altFINS data only. Show me the latest crypto news about Ethereum, then explain whether any item materially changes the current technical picture.
```

### Comparative analysis wrapper

```text
Use validated altFINS data only. Compare BTC and ETH on the daily timeframe. Separate validated facts, interpretation, and the main open questions before giving a cautious conclusion.
```

### Signal-plus-context wrapper

```text
Use validated altFINS data only. Review recent bullish or bearish signal evidence for SOL and explain whether the broader context strengthens or weakens the setup. Keep facts and interpretation separate.
```

### Scan-summary wrapper

```text
Use validated altFINS data only. Find a small group of technically interesting candidates and summarize them as a market scan. Highlight the strongest evidence, the biggest uncertainty, and the next checks to run.
```

## Usage rules

- Use the official prompt anchors as examples of supported question shape, not as proof of a specific runtime tool name.
- When adding constraints such as timeframe or output format, label them clearly as local prompting additions.
- If the runtime environment has not yet confirmed a needed MCP capability, fall back to a conservative research plan instead of pretending the prompt is executable as-is.
