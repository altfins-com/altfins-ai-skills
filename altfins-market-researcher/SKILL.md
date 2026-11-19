---
name: altfins-market-researcher
description: Use the altFINS CLI to screen crypto, stocks or forex, retrieve historical data, and export reproducible research.
---

# AltFINS Market Researcher

## Purpose

Use this skill to guide repeatable research workflows around the altFINS CLI. The emphasis is on discovering the real command surface, producing structured output, and making the work easy to rerun or hand off.

## Use This Skill When

- the task is centered on the altFINS CLI
- the user needs a repeatable research flow or export-friendly output
- the agent should stay grounded in the validated CLI snapshot or the live local CLI

## Do Not Use This Skill When

- the task is primarily about MCP-based workflows
- the task is mainly translation of natural language into structured requests
- the answer would require inventing unsupported CLI commands or flags

## Validated CLI Anchors

The checked-in CLI snapshot and the live local CLI agree on these core facts:

- top-level groups include `analytics`, `auth`, `commands`, `completion`, `markets`, `news`, `ohlcv`, `quota`, `refs`, `signals`, `ta`, and `tui`
- global flags include `--dry-run`, `--fields`, `--no-color`, and `-o/--output`
- `af commands -o json` exposes command metadata and endpoint mappings for automation-friendly discovery

## Request-Shaping Modes

Choose one of these modes before writing the recommendation:

- flag-only recommendation
- JSON-body planning recommendation
- preview-before-run recommendation

Do not force everything into flags if the query shape is clearly better expressed through `--filter` or `--stdin-json`.

## Working Rules

- Prefer the checked-in CLI snapshot when you need a stable local contract.
- Prefer the live local CLI if the current session depends on runtime truth.
- Use `--dry-run` before a live request when request shape matters.
- Keep examples grounded in validated CLI behavior only.
- If the CLI surface is missing a capability, state the gap clearly.
- When the desired query is more complex than a few obvious flags, prefer request-shaping guidance over guessed shorthand.

## Recommended Workflow

1. Start with `af commands -o json` or the checked-in CLI snapshot to find the correct command family.
2. Inspect the specific subcommand help before suggesting flags.
3. Decide whether the request should stay flag-first or move to `--filter` / `--stdin-json` planning.
4. Choose the output format that matches the task: `table`, `json`, `jsonl`, or `csv`.
5. Use `--dry-run` when the request shape itself is important to verify.

## Expected Outputs

- CLI research plans
- validated command suggestions
- export-friendly workflow recommendations
- request previews and command-discovery guidance
- safe request-shaping plans for complex queries

## Instrument discovery and export

Check `af --version` and `af commands -o json` before choosing flags. CLI 1.2.0 supports `refs symbols --search` and `markets search --asset-class`. On older binaries, inspect `af refs symbols -o json` and use confirmed IDs with existing history commands. Keep the UTC window, interval, sort order, source, retrieval time and missing IDs with the export.

A stock or forex scan sends the full catalogue selection before server sorting and pagination. The regular screener charges by symbol count even for a one-row result. Restrict the universe to explicit IDs when the request concerns only those instruments. Use stored setups for a lookup. Generation is a separately confirmed, billed action.

## References

- Read [references/sources.md](references/sources.md) for source boundaries.
- Read [README.md](https://github.com/altfins-com/altfins-ai-skills/blob/v1.1.0/docs/validated-surfaces/README.md) for the checked-in CLI and MCP surface snapshots.
- Read [references/cli-anchors.md](references/cli-anchors.md) for validated CLI surface details.
- Read [references/request-patterns.md](references/request-patterns.md) for validated request-shaping rules.
- Read [references/filter-body-guidance.md](references/filter-body-guidance.md) for conservative JSON-body planning guidance.
- Read [references/research-playbook.md](references/research-playbook.md) for a reusable CLI workflow.
- Read [references/example-workflows.md](references/example-workflows.md) for validated command patterns and wrappers.
- Read [references/golden-examples.md](references/golden-examples.md) for quality benchmarks that show what a strong CLI recommendation should look like.
- Read [references/validation-scenarios.md](references/validation-scenarios.md) for smoke-check scenarios.
- Reuse [assets/research-handoff-template.md](assets/research-handoff-template.md) when handing a CLI workflow to another agent or user.
- Reuse [assets/filter-handoff-template.md](assets/filter-handoff-template.md) when a complex request needs structured filter/body planning.
