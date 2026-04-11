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

## Working Rules

- Clarify the user intent before proposing structured request shapes.
- Keep the translation conservative and implementation-neutral unless the target interface is validated.
- Distinguish between the user goal, the structured request, and any later execution step.
- Avoid fake precision in filters, schemas, or endpoints.

## Expected Outputs

- structured prompt drafts
- research briefs
- future query shapes for validated CLI or MCP workflows

## References

- Read [references/sources.md](references/sources.md) before mapping intent to any altFINS-facing structure.
