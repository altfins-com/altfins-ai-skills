# AltFINS Query Builder

`altfins-query-builder` is the skill to use when the user starts with a plain-English trading or research idea and the first job is to turn that idea into a clearer structured request.

It is designed for translation tasks such as:
- turning vague requests into cleaner research briefs
- identifying missing inputs before execution
- routing a request toward CLI, MCP, or interface-neutral output
- preparing another agent to continue the work without guessing intent

It is not the right skill for final market analysis or detailed CLI command discovery. Those jobs belong to `altfins-market-analyst` and `altfins-market-researcher`.

## What This Skill Helps With

Use this skill when you want the agent to:
- classify a beginner request into a clear category
- identify missing details such as asset, timeframe, or filter logic
- choose the safest output mode
- produce a clean handoff for a later CLI or MCP workflow
- stay conservative when the target interface is not yet validated

## How to Use It

In an agent environment that supports skills, invoke it by name and give it the natural-language request you want translated.

Example prompts:

```text
Use $altfins-query-builder to turn this into a clean research brief: What are the best coins right now?
```

```text
Use $altfins-query-builder to translate this into a CLI-ready request plan: show me bullish BTC and ETH signals since March 1.
```

```text
Use $altfins-query-builder to turn this into an MCP-ready analysis prompt: give me a complete technical analysis of SOL.
```

If explicit skill invocation is not needed in your environment, plain-English requests about what the user wants to find, scan, compare, or explore should naturally fit this skill.

## Best Inputs to Provide

This skill works best when you include as much of the request as you already know:
- asset or market universe
- timeframe or date window
- whether the goal is discovery, signals, indicators, news, or analysis
- whether you want a neutral brief, CLI-ready plan, or MCP-ready prompt
- any constraints, such as export format or interactive browsing

Good example:

```text
Use $altfins-query-builder to translate this into the safest next-step plan: I want to find coins with interesting bullish setups and then open an interactive browser to inspect them.
```

## What You Should Expect Back

A strong answer from this skill should usually include:
- the best matching request category
- the validated target family
- the safest output mode
- missing inputs if the request is underspecified
- a structured brief, prompt, or request plan that another agent can continue

This skill should not fake precision. If the user has not given enough detail, the output should expose the missing pieces instead of pretending the request is ready to run.

## Recommended Reading Inside This Skill

Start here for the core contract:
- [SKILL.md](SKILL.md)
- [references/intent-taxonomy.md](references/intent-taxonomy.md)
- [references/target-catalog.md](references/target-catalog.md)
- [references/translation-playbook.md](references/translation-playbook.md)
- [references/example-translations.md](references/example-translations.md)
- [references/golden-examples.md](references/golden-examples.md)

Reusable handoff templates:
- [assets/request-brief-template.md](assets/request-brief-template.md)
- [assets/intent-routing-matrix.md](assets/intent-routing-matrix.md)

## When to Use Another Skill Instead

Use [../altfins-market-researcher/README.md](../altfins-market-researcher/README.md) when the request is already concrete enough that the next step is choosing or shaping the exact `af` CLI command.

Use [../altfins-market-analyst/README.md](../altfins-market-analyst/README.md) when the request is already an analysis task and the user needs evidence-backed interpretation rather than request translation.
