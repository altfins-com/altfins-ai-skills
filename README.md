# altfins-ai-skills

Reusable AI skills for altFINS workflows.

Install the `altfins-skills` command, copy the skills into your local agent or project, and use them for crypto market analysis, CLI research, and plain-English-to-query translation.

## Install

### macOS and Linux

```bash
brew install altfins-com/tap/altfins-skills
altfins-skills list
altfins-skills install --platform codex --all
```

Brew installs only the `altfins-skills` command. Your agent homes stay untouched until you run `altfins-skills install ...` yourself.

**Optional but recommended for CLI-driven workflows:** install the **altFINS CLI (`af`)** from [altfins-cli](https://github.com/altfins-com/altfins-cli). This is especially useful for `altfins-market-researcher`, and it can also strengthen `altfins-market-analyst` workflows when you want live CLI evidence.

### Windows

Download the current bundle:

<https://github.com/altfins-com/altfins-ai-skills/releases/latest/download/altfins-skills-windows.zip>

Then run:

```powershell
.\altfins-skills.exe list
.\altfins-skills.exe install --platform copilot --all
```

Python fallback inside the ZIP:

```powershell
.\altfins-skills.cmd list
```

### Claude

For **Claude Code**, install local subagents with:

```bash
altfins-skills install --platform claude-code altfins-market-analyst
```

This writes:
- `~/.claude/agents/<skill>.md` as the Claude Code subagent entrypoint
- `~/.claude/skills/<skill>/` as the bundled skill payload referenced by that subagent

For **Claude Cowork**, package the skill and upload the ZIP in `Customize > Skills`:

```bash
altfins-skills package --platform claude-cowork altfins-market-analyst
```

Then upload the produced ZIP. Output goes to `~/.altfins-skills/dist/skills/` when you run the installed command, or `dist/skills/` in a repo checkout.

```text
~/.altfins-skills/dist/skills/altfins-market-analyst.skill.zip
```

### Project-Level Installs

`Cursor` and `OpenClaw` are project integrations rather than user-home skill folders.

```bash
altfins-skills install --platform cursor --mode project --project-dir /path/to/project altfins-query-builder
altfins-skills install --platform openclaw --mode project --project-dir /path/to/project altfins-market-analyst
```

The installer writes project-local glue and a project-local copy of the skill under `.altfins-skills/`.

### Developer Fallback

```bash
git clone https://github.com/altfins-com/altfins-ai-skills
cd altfins-ai-skills
python3 scripts/skills.py list
python3 scripts/skills.py install --platform codex --all
```

Full install details live in [docs/skill-installation.md](docs/skill-installation.md).

## What You Get

This repository ships three reusable skills:

### AltFINS Market Analyst

Use this when you want structured crypto market analysis built around validated altFINS-facing workflows.

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

## Supported Platforms

| Platform | Mode | Install surface |
|----------|------|-----------------|
| Codex | `skills` | `$CODEX_HOME/skills/<skill>` or `~/.codex/skills/<skill>` |
| Claude Code | `skills` | `~/.claude/agents/<skill>.md` + `~/.claude/skills/<skill>/` |
| Claude Cowork | `package-upload` | `dist/skills/<skill>.skill.zip` uploaded in `Customize > Skills` |
| Gemini | `skills` | `~/.gemini/skills/<skill>` |
| Copilot | `skills` | `~/.copilot/skills/<skill>` |
| Cursor | `project` | `<project>/.cursor/rules/<skill>.mdc` + `<project>/.altfins-skills/cursor/<skill>/` |
| OpenClaw | `project` | `<project>/AGENTS.md` + `<project>/.altfins-skills/openclaw/<skill>/` |

## Package Skills

```bash
altfins-skills package --all
```

Developer fallback:

```bash
python3 scripts/skills.py package --all
```

Artifacts land here:

```text
repo checkout: dist/skills/<skill-name>.skill.zip
installed command: ~/.altfins-skills/dist/skills/<skill-name>.skill.zip
```

## Why This Repo Is a Monorepo

The monorepo structure keeps the skills:
- easy to browse
- easy to validate
- easy to package one by one
- easy to extend without guessing where new skills belong

Shared conventions, validated surfaces, packaging helpers, and release automation live at the repo level, while each skill remains independently packageable and installable.

## Validated Reference Material

The repository is grounded in:
- official altFINS API documentation
- the official OpenAPI schema
- official altFINS MCP documentation
- official altFINS CLI documentation
- checked-in validated surface snapshots under [docs/validated-surfaces/](docs/validated-surfaces/README.md)

Start with [docs/validated-sources.md](docs/validated-sources.md) for the shared source inventory.

## Validation

Run these checks before pushing structural or contract changes:

```bash
python3 scripts/validate_skills.py
python3 scripts/lint_markdown_contracts.py
python3 scripts/test_skills.py
python3 scripts/test_release_assets.py
```

These checks cover:
- skill structure and required files
- markdown contract links
- installer list, package, install, uninstall, and status smoke tests
- project-mode smoke tests for Cursor and OpenClaw
- launcher and packaged-layout resolution smoke tests
- source archive, formula, and Windows bundle smoke tests

For scenario-based checks of the skill behavior itself, see [docs/skill-validation.md](docs/skill-validation.md).

## Adding Another Skill

When adding a new skill:

1. Create a new top-level directory with a lowercase, hyphenated name.
2. Add `README.md`, `SKILL.md`, `agents/openai.yaml`, `references/`, `scripts/`, and `assets/`.
3. Keep claims conservative and grounded in validated altFINS behavior.
4. Add `references/validation-scenarios.md` and `references/golden-examples.md`.
5. Add project templates under `assets/project/` if the skill should support project-mode adapters.
6. Run all repository checks before committing.

## Learn More

- [docs/skill-installation.md](docs/skill-installation.md)
- [docs/releasing.md](docs/releasing.md)
- [docs/repository-architecture.md](docs/repository-architecture.md)
- [docs/validated-sources.md](docs/validated-sources.md)
- [docs/validated-surfaces/README.md](docs/validated-surfaces/README.md)
- [docs/skill-validation.md](docs/skill-validation.md)
- [docs/skill-roadmap.md](docs/skill-roadmap.md)
