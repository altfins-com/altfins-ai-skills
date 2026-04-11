---
name: altfins-query-builder
description: Use this skill for translating plain-English trading or research intent into structured prompts, request briefs, or future altFINS query shapes without overclaiming execution details.
---

# AltFINS Query Builder

## Purpose

Use this skill to turn plain-English market research intent into clearer structured requests. The emphasis is on clarification, decomposition, and clean handoff shapes for future CLI or MCP workflows.

## Use This Skill When

- the user describes a trading or research goal in natural language
- the next step is to shape that goal into a clearer prompt or request brief
- the output may later be used by another skill, CLI workflow, or MCP workflow

## Do Not Use This Skill When

- the task already requires direct execution against a validated interface
- the task is full market analysis rather than intent translation
- the answer would require inventing unsupported parameters or server capabilities

## Translation Modes

Choose one of these output modes explicitly:

- interface-neutral research brief
- CLI-ready request plan
- MCP-ready research prompt

If the target interface is not yet validated, stay interface-neutral.

## Validated Target Families

The current validated target families include:

- market screening
- analytics history
- OHLCV history and snapshots
- signal feed queries
- curated technical analysis
- news search and detail lookup
- reference data such as symbols and intervals
- MCP capability families such as Screener, Technical Analysis, OHLCV Data, Analytics History, Signal Feed, News, Calendar Events, and Portfolio

## Working Rules

- Clarify the user intent before proposing structured request shapes.
- Keep the translation conservative and implementation-neutral unless the target interface is validated.
- Distinguish between the user goal, the structured request, and any later execution step.
- Avoid fake precision in filters, schemas, or endpoints.
- When in doubt, produce a request brief instead of a fake concrete command.

## Recommended Workflow

1. Identify the user's real goal.
2. Classify it into a validated target family.
3. Collect the missing dimensions: assets, timeframe, filters, and desired output.
4. Choose the safest output mode.
5. Produce a handoff that another skill or agent can execute without guessing intent.

## Expected Outputs

- structured prompt drafts
- research briefs
- CLI-ready request plans grounded in validated commands
- future query shapes for validated CLI or MCP workflows

## References

- Read [references/sources.md](references/sources.md) for source boundaries.
- Read [references/target-catalog.md](references/target-catalog.md) for validated target mappings.
- Read [references/translation-playbook.md](references/translation-playbook.md) for a reusable translation flow.
