# AltFINS Market Analyst

`altfins-market-analyst` is the skill to use when you want a structured crypto market analysis built around validated altFINS-facing workflows.

It is designed for analysis tasks such as:
- understanding the technical outlook for one coin
- comparing two or more setups
- scanning for the most interesting market structures
- turning raw technical evidence into a conservative written summary

It is not the right skill for direct CLI command discovery or for translating a vague plain-English idea into a structured request. Those jobs belong to `altfins-market-researcher` and `altfins-query-builder`.

## What This Skill Helps With

Use this skill when you want the agent to:
- frame a market question clearly
- gather evidence in a disciplined order
- separate validated facts from interpretation
- choose a clean output mode such as a short outlook or a structured memo
- avoid overclaiming certainty from technical data alone

## How to Use It

In an agent environment that supports skills, the clearest path is to invoke it by name and then describe the analysis you want.

Example prompts:

```text
Use $altfins-market-analyst to assess the current technical outlook for BTC.
```

```text
Use $altfins-market-analyst to compare ETH and SOL and summarize which setup looks stronger right now.
```

```text
Use $altfins-market-analyst to scan for the most interesting technical setups and give me a short market scan summary.
```

If your agent environment does not require explicit skill names, you can still ask in plain English. This skill is meant to match requests that clearly sound like structured market analysis.

## Best Inputs to Provide

This skill works best when you include at least some of these details:
- asset or asset list, such as `BTC`, `ETH`, or `SOL`
- timeframe or time horizon
- whether you want a single-asset view, comparison, or scan
- desired output style, such as short outlook or structured memo
- any special focus, such as signals, trend structure, or indicator context

Good example:

```text
Use $altfins-market-analyst to give me a short outlook for BTC on the daily timeframe. Separate facts from interpretation and end with the next things I should check.
```

## What You Should Expect Back

A strong answer from this skill should usually include:
- the objective of the analysis
- validated facts
- interpretation that is clearly labeled as interpretation
- open questions or uncertainty
- suggested next checks

This skill is analytical, not advisory. It should help the user understand the setup better, not pretend to predict outcomes with certainty.

## Recommended Reading Inside This Skill

If you want to understand how the skill thinks, start here:
- [SKILL.md](SKILL.md)
- [references/analysis-workflow.md](references/analysis-workflow.md)
- [references/synthesis-rules.md](references/synthesis-rules.md)
- [references/output-modes.md](references/output-modes.md)
- [references/golden-examples.md](references/golden-examples.md)

Reusable output templates:
- [assets/analysis-summary-template.md](assets/analysis-summary-template.md)
- [assets/market-scan-summary-template.md](assets/market-scan-summary-template.md)

## When to Use Another Skill Instead

Use [../altfins-market-researcher/README.md](../altfins-market-researcher/README.md) when you need actual `af` CLI commands, export formats, or repeatable research workflows.

Use [../altfins-query-builder/README.md](../altfins-query-builder/README.md) when the user starts with a vague plain-English request and the first job is to turn it into a clean structured brief or validated request plan.
