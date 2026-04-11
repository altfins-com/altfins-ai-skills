---
name: altfins-market-analyst
description: Use this skill for structured altFINS market analysis workflows, especially when the task involves MCP-driven research planning, evidence gathering, and conservative synthesis.
---

# AltFINS Market Analyst

## Purpose

Use this skill to structure crypto market analysis around validated altFINS-facing workflows. The emphasis is on research framing, evidence gathering, and disciplined synthesis rather than fast speculation.

## Use This Skill When

- the task is to analyze a market setup or research question step by step
- the workflow may involve altFINS MCP access or MCP-shaped research planning
- the user needs a structured summary with clear reasoning and source boundaries

## Do Not Use This Skill When

- the task is mainly about direct CLI command execution
- the task is only prompt rewriting without analysis workflow design
- the answer would require assuming undocumented altFINS MCP methods

## Working Rules

- Treat official altFINS documentation, validated MCP metadata, and user-provided context as the trusted sources.
- Do not invent tool names, server methods, or analysis capabilities.
- Make uncertainty explicit when MCP coverage is not yet validated.
- Prefer structured findings, assumptions, and next investigative steps.

## Expected Outputs

- research plans
- evidence-backed market analysis summaries
- conservative next-step recommendations for further investigation

## References

- Read [references/sources.md](references/sources.md) before relying on external altFINS-facing behavior.
