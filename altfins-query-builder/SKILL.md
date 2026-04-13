---
name: altfins-query-builder
description: Use this skill for translating plain-English trading or research intent into structured prompts, request briefs, or validated altFINS-ready handoffs without overclaiming execution details.
---

# AltFINS Query Builder

## Purpose

Use this skill to turn plain-English market research intent into clearer structured requests. The emphasis is on clarification, decomposition, and clean handoff shapes for validated CLI workflows, documented MCP workflows, or interface-neutral briefs.

## Use This Skill When

- the user describes a trading or research goal in natural language
- the next step is to shape that goal into a clearer prompt or request brief
- the output may be used by another skill, a validated CLI workflow, or a documented MCP workflow

## Do Not Use This Skill When

- the task already requires direct execution against a validated interface
- the task is full market analysis rather than intent translation
- the answer would require inventing unsupported parameters or server capabilities

## Translation Modes

Choose one of these output modes explicitly:

- interface-neutral research brief
- CLI-ready request plan
- documented-MCP-ready research prompt

If the target interface is not confirmed in the current validated surface, stay interface-neutral.

## Beginner-Friendly Request Categories

Start by classifying the request into one plain-English category:

- find coins
- check signals
- look up indicator history
- look up price candles
- browse technical analysis
- get news or context
- open an interactive browser
- ask for a full market analysis

## Agent-Facing Routing Layer

After choosing a beginner-facing category:

1. identify the validated target family
2. fill the required slots
3. choose the safest output mode
4. produce a handoff another agent can continue without guessing

## Working Rules

- Clarify the user intent before proposing structured request shapes.
- Keep the translation conservative and implementation-neutral unless the target interface is confirmed in the current validated surface.
- Distinguish between the user goal, the structured request, and the separate execution step that may follow.
- Avoid fake precision in filters, schemas, or endpoints.
- When in doubt, produce a request brief instead of a fake concrete command.
- Keep beginner-facing language simple, then map it to the more formal routing layer internally.

## Recommended Workflow

1. Identify the user's real goal.
2. Classify it into a beginner-facing request category.
3. Map that category to a validated target family.
4. Collect the missing dimensions: assets, timeframe, filters, and desired output.
5. Choose the safest output mode.
6. Produce a handoff that another skill or agent can execute without guessing intent.

## Expected Outputs

- structured prompt drafts
- research briefs
- CLI-ready request plans grounded in validated command snapshots
- documented-MCP-ready prompts grounded in the documented MCP surface

## References

- Read [references/sources.md](references/sources.md) for source boundaries.
- Read [../docs/validated-surfaces/README.md](../docs/validated-surfaces/README.md) for the checked-in CLI and MCP surface snapshots.
- Read [references/target-catalog.md](references/target-catalog.md) for validated target mappings.
- Read [references/intent-taxonomy.md](references/intent-taxonomy.md) for beginner-facing categories and routing rules.
- Read [references/translation-playbook.md](references/translation-playbook.md) for a reusable translation flow.
- Read [references/example-translations.md](references/example-translations.md) for worked translations from plain English into safe handoff shapes.
- Read [references/golden-examples.md](references/golden-examples.md) for quality benchmarks that show what a strong final translation should look like.
- Read [references/validation-scenarios.md](references/validation-scenarios.md) for smoke-check scenarios.
- Reuse [assets/request-brief-template.md](assets/request-brief-template.md) when the safest output is a neutral or multi-step request brief.
- Reuse [assets/intent-routing-matrix.md](assets/intent-routing-matrix.md) when you want a quick fill-in routing sheet before writing the final handoff.
