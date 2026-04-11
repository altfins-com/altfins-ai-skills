---
name: altfins-market-researcher
description: Use this skill for repeatable altFINS CLI research workflows, especially when the task involves command discovery, export-friendly output, and careful verification of the real CLI surface.
---

# AltFINS Market Researcher

## Purpose

Use this skill to guide repeatable research workflows around the altFINS CLI. The emphasis is on discovering the real command surface, producing structured output, and making the work easy to rerun or hand off.

## Use This Skill When

- the task is centered on the altFINS CLI
- the user needs a repeatable research flow or export-friendly output
- the agent should verify commands and flags before making assumptions

## Do Not Use This Skill When

- the task is primarily about MCP-based workflows
- the task is mainly translation of natural language into structured requests
- the answer would require inventing unsupported CLI commands or flags

## Working Rules

- Inspect the real installed CLI help before assuming commands, flags, or output shapes.
- Prefer machine-readable output and reproducible workflows when available.
- Keep examples grounded in validated CLI behavior only.
- If the CLI surface is missing a capability, state the gap clearly.

## Expected Outputs

- CLI research plans
- validated command suggestions
- export-friendly workflow recommendations

## References

- Read [references/sources.md](references/sources.md) before relying on CLI-specific behavior.
