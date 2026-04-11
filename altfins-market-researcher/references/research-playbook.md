# Research Playbook

Use this playbook when turning a market question into a repeatable CLI workflow.

## Command discovery flow

1. Start with `af commands -o json` for machine-readable discovery or `af --help` for quick orientation.
2. Choose the smallest command family that fits the task.
3. Inspect the exact subcommand help.

## Preferred output strategy

- Use `table` for quick human scanning.
- Use `json` for structured single-result or page-style output.
- Use `jsonl` for line-by-line pipelines.
- Use `csv` when the output is intended for spreadsheets or simple exports.

## Preferred request strategy

- Use explicit flags when the query is simple and obvious.
- Use `--filter` or `--stdin-json` when the API body would otherwise become ambiguous.
- Use `--fields` to reduce noisy output.
- Use `--page`, `--size`, and `--sort` for stable paged workflows.

## TUI guidance

For TUI entrypoints, the installed CLI and official docs validate these starting modes:

- `af tui markets`
- `af tui signals`
- `af tui ta`
- `af tui news`

When seeding TUI requests:

- use `--symbol` for a simple seed where supported
- use `--filter` or `--stdin-json` for richer API-side filters
- treat `/` inside the TUI as local search, not remote API search

## Safe handoff shape

When giving a user or another agent a CLI workflow, prefer this order:

1. short explanation of why this command family fits
2. the exact command
3. optional `--dry-run` preview step
4. notes about output format or follow-up commands
