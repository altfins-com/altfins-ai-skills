# AltFINS Market Researcher

`altfins-market-researcher` is the skill to use when you want help with the altFINS CLI in a way that is repeatable, export-friendly, and grounded in the real installed command surface.

It is designed for research tasks such as:
- finding the right `af` command family
- shaping a query safely before execution
- choosing between simple flags and JSON-based filters
- preparing output for `json`, `jsonl`, `csv`, or table workflows
- handing a CLI workflow to another user or agent

It is not the right skill for high-level market interpretation or for translating a vague beginner request into a structured brief. Those jobs belong to `altfins-market-analyst` and `altfins-query-builder`.

## What This Skill Helps With

Use this skill when you want the agent to:
- discover the correct CLI command family
- inspect validated flags and output modes
- recommend `--dry-run` when request shape matters
- keep a workflow easy to rerun later
- avoid guessing undocumented commands or flags

## How to Use It

In an agent environment that supports skills, invoke it by name and describe the CLI task.

Example prompts:

```text
Use $altfins-market-researcher to give me the best af command for daily RSI history for BTC in JSON.
```

```text
Use $altfins-market-researcher to help me build a richer market screen and tell me whether I should use flags, --filter, or --stdin-json.
```

```text
Use $altfins-market-researcher to recommend the best interactive TUI command for exploring BTC.
```

If explicit skill names are not required in your environment, plain-English requests about `af` commands and repeatable research flows should naturally fit this skill.

## Best Inputs to Provide

This skill works best when you include:
- the data family you want, such as markets, signals, analytics, OHLCV, news, or TUI
- symbol list if known
- timeframe or date range if relevant
- desired output format
- whether you want a one-shot command, dry-run preview, or reusable workflow

Good example:

```text
Use $altfins-market-researcher to show me the safest CLI workflow for BTC signal history since March 1 in JSON, and include a dry-run preview step.
```

## What You Should Expect Back

A strong answer from this skill should usually include:
- the best command family
- why that family fits
- whether the request should stay flag-first or move to JSON-body planning
- a recommended command or safe handoff plan
- optional preview and export suggestions

This skill should stay honest about uncertainty. If the exact request body is not fully validated, it should say so instead of inventing keys.

## Recommended Reading Inside This Skill

Start here for the core contract:
- [SKILL.md](SKILL.md)
- [references/cli-anchors.md](references/cli-anchors.md)
- [references/request-patterns.md](references/request-patterns.md)
- [references/filter-body-guidance.md](references/filter-body-guidance.md)
- [references/example-workflows.md](references/example-workflows.md)
- [references/golden-examples.md](references/golden-examples.md)

Reusable handoff templates:
- [assets/research-handoff-template.md](assets/research-handoff-template.md)
- [assets/filter-handoff-template.md](assets/filter-handoff-template.md)

## When to Use Another Skill Instead

Use [../altfins-market-analyst/README.md](../altfins-market-analyst/README.md) when the user wants a structured technical analysis rather than command selection.

Use [../altfins-query-builder/README.md](../altfins-query-builder/README.md) when the first job is to turn a vague trading idea into a cleaner structured request before deciding whether CLI is even the right interface.
