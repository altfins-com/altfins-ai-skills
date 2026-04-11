# Trusted Sources

Use this skill conservatively.

## Shared starting point

Start with [../../docs/validated-sources.md](../../docs/validated-sources.md) for the shared cross-repository source inventory.

## Preferred source order

1. User-provided task context
2. Real installed altFINS CLI help output
3. `af commands -o json` command metadata
4. Official altFINS documentation
5. Verified repository context relevant to the CLI workflow

## Rules

- Do not invent commands, flags, output formats, or filters.
- Verify the CLI surface from the real binary or checked-in docs before making recommendations.
- Prefer examples that are easy to rerun and export.
- Distinguish validated CLI behavior from future ideas.
