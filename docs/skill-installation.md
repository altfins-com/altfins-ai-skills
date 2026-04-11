# Skill Installation

This document explains the v1 installer flow for `altfins-ai-skills`.

## Goal

The repository now ships a shared Python installer so each skill can be:
- listed from the monorepo
- packaged into its own `skill.zip`
- installed into a supported local agent home
- uninstalled cleanly later

The v1 installer is intentionally conservative. It supports skills-only installation, not project-level glue such as `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, Cursor rules, or hooks.

## Installer Entry Point

Run the installer from the repository root:

```bash
python3 scripts/skills.py list
python3 scripts/skills.py status
python3 scripts/skills.py package --all
python3 scripts/skills.py install --platform codex altfins-market-analyst
python3 scripts/skills.py uninstall --platform codex altfins-market-analyst
```

## Supported Platforms

| Platform | Install support in v1 | Install root |
|----------|------------------------|--------------|
| Codex | Yes | `$CODEX_HOME/skills` or `~/.codex/skills` |
| Claude | Yes | `~/.claude/skills` |
| Gemini | Yes | `~/.gemini/skills` |
| Copilot | Yes | `~/.copilot/skills` |
| Cursor | No, recognized only | n/a in skills-only mode |
| OpenClaw | No, recognized only | n/a in skills-only mode |

### Why Cursor and OpenClaw are deferred

The current v1 design installs self-contained skill folders only. Cursor and OpenClaw integration patterns are closer to project-level rules or AGENTS-based wiring, so they are intentionally deferred until a later project-integration phase.

## Commands

### List skills

```bash
python3 scripts/skills.py list
python3 scripts/skills.py list --platform codex
python3 scripts/skills.py list --json
```

### Show status

```bash
python3 scripts/skills.py status
python3 scripts/skills.py status --platform gemini
python3 scripts/skills.py status --json
```

### Package skills

```bash
python3 scripts/skills.py package --all
python3 scripts/skills.py package altfins-market-analyst altfins-query-builder
```

Package output goes to:

```text
dist/skills/<skill-name>.skill.zip
```

Each archive contains the skill folder as the zip root, for example:

```text
altfins-market-analyst/
  README.md
  SKILL.md
  agents/
  references/
  scripts/
  assets/
```

### Install skills

```bash
python3 scripts/skills.py install --platform codex altfins-market-analyst
python3 scripts/skills.py install --platform claude --all
```

If a skill is already installed, the command fails unless you add `--force`.

### Uninstall skills

```bash
python3 scripts/skills.py uninstall --platform codex altfins-market-analyst
python3 scripts/skills.py uninstall --platform gemini --all
```

## Validation Behavior

`package` and `install` run these checks before doing any work:

```bash
python3 scripts/validate_skills.py
python3 scripts/lint_markdown_contracts.py
```

If validation fails, packaging or installation stops immediately.

## Test and Automation

The repository now includes a smoke test for the installer:

```bash
python3 scripts/test_skills.py
```

GitHub Actions runs this smoke test alongside the existing repository validators.
