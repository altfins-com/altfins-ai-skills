---
name: altfins-market-analyst
description: Analyze crypto, stock and forex evidence from altFINS, including technical outlooks, cross-market comparisons and coverage gaps.
---

# AltFINS Market Analyst

## Purpose

Use this skill to structure crypto, stock and forex analysis around validated altFINS-facing workflows. The emphasis is on research framing, evidence gathering, and disciplined synthesis rather than fast speculation.

## Use This Skill When

- the task is to analyze a market setup or research question step by step
- the workflow may involve altFINS MCP access or MCP-shaped research planning
- the user needs a structured summary with clear reasoning and source boundaries

## Do Not Use This Skill When

- the task is mainly about direct CLI command execution
- the task is only prompt rewriting without analysis workflow design
- the answer would require assuming undocumented altFINS MCP methods

## Validated MCP Anchors

The documented MCP surface confirms these high-level capability families:

- Screener
- Technical Analysis
- OHLCV Data
- Analytics History
- Signal Feed
- News
- Calendar Events
- Portfolio

Treat these as documented capability families, not as guaranteed runtime tool names. Actual tool identifiers should be discovered from the connected MCP client at runtime.

## Output Modes

Choose an output mode before writing the analysis:

- short outlook
- structured analysis memo
- market scan summary
- follow-up investigation plan

The output mode should match the user's actual need, not just the amount of available data.

## Working Rules

- Treat official altFINS documentation, checked-in validated surfaces, and user-provided context as the trusted sources.
- Do not invent tool names, server methods, or analysis capabilities.
- Make uncertainty explicit when the needed runtime tool is not confirmed in the current session.
- Prefer structured findings, assumptions, and next investigative steps.
- Separate validated facts from inferences and market interpretation.
- Keep the skill analytical, not advisory.

## Recommended Workflow

1. Clarify the market question, assets, timeframe, and desired output.
2. Choose the right output mode first.
3. Decide which documented capability family is relevant.
4. Confirm the actual available MCP tools from the connected client before planning any tool use.
5. Gather evidence in a traceable order: market state, supporting indicators, signals, then contextual news or events when relevant.
6. Finish with a conservative summary that clearly labels facts, inferences, and missing inputs.

## Expected Outputs

- research plans
- evidence-backed market analysis summaries
- conservative next-step recommendations for further investigation
- clearly labeled analysis outputs that distinguish facts from interpretation

## Cross-market evidence

Resolve each instrument in the catalogue. Keep Apple common stock (`CS_AAPL`) separate from tokenized Apple (`AAPLX`). Match each requested symbol against returned rows and report the last available bar in UTC. Account for stock exchange sessions and the FX trading week. Check price, trend and RSI on comparable intervals. Exclude crypto on-chain measures from equity analysis. FX volume can be zero or unavailable, so omit volume, OBV, VWMA, supply and market-cap rankings for FX.

For a signal, report its detection time separately from the retrieval-time price, daily change and market cap. Some plans delay signals by 24 hours. For historical analysis use contemporaneous candles. An empty curated TA page means editorial coverage is missing. Continue with candles and indicators for the same ID. Distinguish editorial TA, stored AI setups and newly generated material.

## References

- Read [references/sources.md](references/sources.md) for source boundaries.
- Read [README.md](https://github.com/altfins-com/altfins-ai-skills/blob/v1.1.0/docs/validated-surfaces/README.md) for the checked-in CLI and MCP surface snapshots.
- Read [references/mcp-anchors.md](references/mcp-anchors.md) for validated MCP facts.
- Read [references/analysis-workflow.md](references/analysis-workflow.md) for a reusable analysis flow.
- Read [references/synthesis-rules.md](references/synthesis-rules.md) for evidence and reasoning discipline.
- Read [references/output-modes.md](references/output-modes.md) to choose the right output shape.
- Read [references/example-prompts.md](references/example-prompts.md) for validated prompt anchors and safe wrappers.
- Read [references/golden-examples.md](references/golden-examples.md) for quality benchmarks that show what a strong analysis answer should look like.
- Read [references/validation-scenarios.md](references/validation-scenarios.md) for smoke-check scenarios.
- Reuse [assets/analysis-summary-template.md](assets/analysis-summary-template.md) when a structured written output is useful.
- Reuse [assets/market-scan-summary-template.md](assets/market-scan-summary-template.md) when summarizing a scan across multiple assets.
