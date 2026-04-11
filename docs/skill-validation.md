# Skill Validation

This document describes the lightweight smoke-check process for the skills in this repository.

## Goal

The goal is not to prove full correctness. The goal is to catch obvious drift in:

- trigger intent
- scope boundaries
- source discipline
- output shape discipline
- handoff usefulness
- routing taxonomy quality
- filter and body planning discipline
- synthesis discipline
- answer quality against repository golden examples
- broken contract links between skill docs, references, and assets

## How to Run a Smoke Check

For each skill:

1. Open the skill's `SKILL.md`.
2. Open the skill's `references/validation-scenarios.md`.
3. Open the skill's `references/golden-examples.md`.
4. Pick one scenario that matches the kind of work you want to validate.
5. Check whether the skill would produce the expected behavior without inventing undocumented altFINS behavior.
6. Compare the shape and quality of the answer against the golden example style for that skill.
7. Run `python3 scripts/lint_markdown_contracts.py` if you changed markdown links or contract references.
8. Record any failure as a repository issue or update the skill docs if the contract is outdated.

## Shared Pass Criteria

A scenario passes if the skill:

- chooses the correct high-level workflow for the request
- stays within validated altFINS capabilities
- does not invent endpoints, CLI flags, MCP methods, or schemas
- produces the expected output mode for the task
- makes missing inputs and assumptions explicit when needed
- uses the taxonomy, request-shaping, or synthesis layer that now belongs to that skill's contract
- reaches the same quality bar shown by the skill's golden examples
- keeps internal markdown links and referenced assets valid

## Shared Failure Signals

A scenario fails if the skill:

- routes the request to the wrong family of tools or workflows
- overclaims unsupported product behavior
- skips required clarification when key inputs are missing
- produces an output shape that another agent cannot reliably continue from
- ignores validated discovery paths such as `af --help`, `af commands -o json`, or MCP runtime tool discovery
- skips the newer skill-specific discipline layer that should now guide the answer
- falls materially below the clarity or caution level shown in the golden examples
- leaves a broken internal markdown link or broken contract reference behind

## Current Validation Files

- `altfins-market-analyst/references/validation-scenarios.md`
- `altfins-market-analyst/references/golden-examples.md`
- `altfins-market-researcher/references/validation-scenarios.md`
- `altfins-market-researcher/references/golden-examples.md`
- `altfins-query-builder/references/validation-scenarios.md`
- `altfins-query-builder/references/golden-examples.md`

## Maintenance Rule

Whenever a skill gains a major new capability or output asset, update its validation scenarios and golden examples so another agent can quickly verify both behavior and answer quality.
