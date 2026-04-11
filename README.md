# altfins-ai-skills

Reusable AI skills for altFINS workflows.

Install them into your local AI agent, then use them for crypto market analysis, CLI research, and plain-English-to-query translation.

## Install in 30 Seconds

Requires Python 3.9+ and one of the supported local agent homes.

```bash
# Clone the repository
git clone https://github.com/altfins-com/altfins-ai-skills
cd altfins-ai-skills

# See the available skills
python3 scripts/skills.py list

# Install all skills into Codex
python3 scripts/skills.py install --platform codex --all
```

Other common installs:

```bash
# Claude
python3 scripts/skills.py install --platform claude --all

# Gemini
python3 scripts/skills.py install --platform gemini --all

# Copilot
python3 scripts/skills.py install --platform copilot --all
```

After installation, restart your assistant so it can pick up the new skills.

Full install details live in [docs/skill-installation.md](docs/skill-installation.md).

## What You Get

This repository currently ships three reusable skills:

### AltFINS Market Analyst

Use this when you want a structured technical or market analysis built around validated altFINS-facing workflows.

Best for:
- single-coin technical outlooks
- comparing two market setups
- summarizing the most interesting opportunities from a scan
- separating facts from interpretation

See:
- [altfins-market-analyst/README.md](altfins-market-analyst/README.md)
- [altfins-market-analyst/SKILL.md](altfins-market-analyst/SKILL.md)

### AltFINS Market Researcher

Use this when you want help with the `af` CLI in a way that is repeatable, export-friendly, and safe.

Best for:
- finding the right `af` command
- deciding between flags, `--filter`, and `--stdin-json`
- preparing JSON, JSONL, CSV, or table workflows
- building repeatable research steps for another agent or user

See:
- [altfins-market-researcher/README.md](altfins-market-researcher/README.md)
- [altfins-market-researcher/SKILL.md](altfins-market-researcher/SKILL.md)

### AltFINS Query Builder

Use this when the user starts with a vague plain-English crypto request and the first job is to turn it into something structured.

Best for:
- clarifying what the user actually wants
- identifying missing inputs
- routing a request toward CLI, MCP, or an interface-neutral brief
- producing a clean handoff for the next skill or agent

See:
- [altfins-query-builder/README.md](altfins-query-builder/README.md)
- [altfins-query-builder/SKILL.md](altfins-query-builder/SKILL.md)

## How to Use the Skills

Once the skills are installed, invoke them by name in your agent environment.

Examples:

```text
Use $altfins-query-builder to turn this into a clean research brief: What are the best coins right now?
```

```text
Use $altfins-market-researcher to give me the safest af workflow for daily RSI history for BTC in JSON.
```

```text
Use $altfins-market-analyst to assess the current technical outlook for ETH and separate facts from interpretation.
```

Each skill also has its own user-facing README with more examples.

## Supported Platforms

The installer currently supports these local agent homes:

| Platform | Install support in v1 | Install root |
|----------|------------------------|--------------|
| Codex | Yes | `$CODEX_HOME/skills` or `~/.codex/skills` |
| Claude | Yes | `~/.claude/skills` |
| Gemini | Yes | `~/.gemini/skills` |
| Copilot | Yes | `~/.copilot/skills` |
| Cursor | Recognized, not installable in v1 | deferred |
| OpenClaw | Recognized, not installable in v1 | deferred |

`Cursor` and `OpenClaw` are intentionally deferred because v1 only handles skills-only installation. Project-level glue such as rules, hooks, or `AGENTS.md` wiring is a later phase.

## Package Skills

If you want individual `skill.zip` bundles:

```bash
python3 scripts/skills.py package --all
```

Artifacts land here:

```text
dist/skills/<skill-name>.skill.zip
```

Each archive contains the skill folder itself as the zip root, so the package stays self-contained.

## Why This Repo Is a Monorepo

The monorepo structure keeps the skills:
- easy to browse
- easy to validate
- easy to package one by one
- easy to extend without guessing where new skills belong

Shared conventions and validation live at the repo level, while each skill remains independently installable and packageable.

## Validated Reference Material

The repository is grounded in:
- official altFINS API documentation
- the official OpenAPI schema
- official altFINS MCP documentation
- official altFINS CLI documentation
- observed local `af` CLI help and command metadata

Start with [docs/validated-sources.md](docs/validated-sources.md) for the shared source inventory.

## Validation

Run these checks before pushing structural or contract changes:

```bash
python3 scripts/validate_skills.py
python3 scripts/lint_markdown_contracts.py
python3 scripts/test_skills.py
```

These checks cover:
- skill structure and required files
- markdown contract links
- installer list, package, install, uninstall, and status smoke tests

For scenario-based checks of the skill behavior itself, see [docs/skill-validation.md](docs/skill-validation.md).

## Adding Another Skill

When adding a new skill:

1. Create a new top-level directory with a lowercase, hyphenated name.
2. Add `README.md`, `SKILL.md`, `agents/openai.yaml`, `references/`, `scripts/`, and `assets/`.
3. Keep claims conservative and grounded in validated altFINS behavior.
4. Add `references/validation-scenarios.md` and `references/golden-examples.md`.
5. Run all repository checks before committing.

## Learn More

- [docs/skill-installation.md](docs/skill-installation.md)
- [docs/repository-architecture.md](docs/repository-architecture.md)
- [docs/validated-sources.md](docs/validated-sources.md)
- [docs/skill-validation.md](docs/skill-validation.md)
- [docs/skill-roadmap.md](docs/skill-roadmap.md)
