# Trusted Sources

Use this skill conservatively.

## Shared starting point

Start with [../../docs/validated-sources.md](../../docs/validated-sources.md) for the shared cross-repository source inventory.

## Preferred source order

1. User-provided task context
2. Checked-in CLI snapshots under `../../docs/validated-surfaces/cli/`
3. Live local `af` help output and `af commands -o json`
4. Official altFINS documentation
5. Verified repository context relevant to the CLI workflow

## Rules

- Do not invent commands, flags, output formats, or filters.
- Prefer examples that are easy to rerun and export.
- If the checked-in snapshot and the live CLI disagree, prefer the live CLI and refresh the snapshot.
- Keep the workflow reproducible and explicit.
