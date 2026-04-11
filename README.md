# altfins-ai-skills

This repository hosts reusable AI skills for altFINS-related workflows.

The goal is to keep each skill self-contained, easy to review, and easy to package later as an individual `skill.zip` bundle. The repository starts with three conservative, documentation-first skills:

- `altfins-market-analyst`: structured market analysis workflows for altFINS MCP-driven research
- `altfins-market-researcher`: repeatable CLI-driven research workflows with export-friendly output habits
- `altfins-query-builder`: translation of plain-English research intent into structured prompts or future query shapes

## Why a Monorepo

This repository uses a monorepo so the skills can share the same contribution model, naming conventions, packaging rules, and roadmap while still remaining independently packageable.

This keeps the project:

- easy for humans to browse
- easy for agents to extend
- easy to version skill-by-skill later
- easy to review without guessing where new skills belong

## Repository Layout

```text
.
├── README.md
├── docs/
├── scripts/
├── altfins-market-analyst/
├── altfins-market-researcher/
└── altfins-query-builder/
```

Each skill directory follows the same internal shape:

- `README.md` for user-facing onboarding and example ways to use the skill
- `SKILL.md` for the core skill contract and invocation guidance
- `agents/openai.yaml` for starter metadata
- `references/` for trusted source boundaries and future reference material
- `scripts/` for future deterministic helpers
- `assets/` for future packaging assets

## Current Skills

### AltFINS Market Analyst

Use this skill when the goal is to guide structured crypto market analysis through validated altFINS-facing workflows, especially when the agent needs to frame research, gather evidence carefully, and summarize findings conservatively.

### AltFINS Market Researcher

Use this skill when the goal is to run or plan repeatable altFINS CLI research tasks, inspect available commands, and prepare output that is easy to export or hand off.

### AltFINS Query Builder

Use this skill when the goal is to turn plain-English trading or research intent into a cleaner structured prompt, request brief, or future query plan without overpromising execution details.

## Validated Reference Material

The repository now includes a validated source layer built from:

- official altFINS API and MCP documentation
- the official altFINS CLI documentation page
- the real installed `af` CLI help output and command metadata observed on April 11, 2026

Start with [docs/validated-sources.md](docs/validated-sources.md) for the shared source inventory, then open the skill-local files in each `references/` directory for deeper, task-specific guidance.

## Installation and Packaging

The repository now includes a shared installer CLI:

```bash
python3 scripts/skills.py list
python3 scripts/skills.py package --all
python3 scripts/skills.py install --platform codex altfins-market-analyst
python3 scripts/skills.py status --platform codex
```

Supported v1 install targets are `codex`, `claude`, `gemini`, and `copilot`. `cursor` and `openclaw` are recognized but intentionally deferred because v1 only handles skills-only installation, not project-level glue.

See [docs/skill-installation.md](docs/skill-installation.md) for the platform matrix, exact commands, package output layout, and current limitations.

## Validation

Use the repository validators before pushing structural changes:

```bash
python3 scripts/validate_skills.py
python3 scripts/lint_markdown_contracts.py
python3 scripts/test_skills.py
```

The first validator checks the required folder shape, `SKILL.md` frontmatter, starter `agents/openai.yaml` metadata, the shared source-linking rules, and the stable skill artifacts.

The markdown contract linter checks internal markdown links and common contract references so a broken path in `SKILL.md`, `docs/`, or skill references is caught early.

The installer smoke test checks listing, packaging, supported platform installs, uninstall flow, unsupported platform handling, and validator-gated packaging behavior.

Use [docs/skill-validation.md](docs/skill-validation.md) to run the scenario-based smoke checks for each skill.

## Adding Another Skill

When adding a new skill:

1. Create a new top-level directory with a lowercase, hyphenated name.
2. Copy the standard folder shape used by the existing skills.
3. Write a short, conservative `SKILL.md` with clear boundaries.
4. Add minimal `agents/openai.yaml` metadata.
5. Put shared conventions in `docs/`, not inside the skill folder.
6. Keep the skill independently archivable for future `skill.zip` packaging.
7. Add `references/validation-scenarios.md` and `references/golden-examples.md` for the new skill.
8. Run both validators before committing structural changes.

## Packaging Direction

This repository does not yet ship packaging automation. The intended direction is simple: package one skill directory at a time, so each skill can later become its own `skill.zip` without depending on shared runtime files from the root.

See [docs/repository-architecture.md](docs/repository-architecture.md) for the structural contract, [docs/validated-sources.md](docs/validated-sources.md) for the shared source inventory, [docs/skill-validation.md](docs/skill-validation.md) for smoke-check guidance, and [docs/skill-roadmap.md](docs/skill-roadmap.md) for the phased roadmap.
