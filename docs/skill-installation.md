# Skill Installation

This document explains the public installation story for `altfins-ai-skills`.

## Summary

The project has three user-facing installation paths:

- `macOS and Linux`: Homebrew-first
- `Windows`: downloadable ZIP-first
- `Cursor` and `OpenClaw`: project-mode integration

A direct repo checkout remains available as a developer fallback.

## macOS and Linux

```bash
brew install altfins-com/tap/altfins-skills
altfins-skills list
altfins-skills install --platform codex --all
```

Notes:
- Homebrew installs the `altfins-skills` command.
- `brew install` does not touch your agent homes.
- The actual skill copy into `~/.codex/skills`, `~/.claude/skills`, `~/.gemini/skills`, or `~/.copilot/skills` happens only when you run `altfins-skills install ...`.

## Windows

Download:

<https://github.com/altfins-com/altfins-ai-skills/releases/latest/download/altfins-skills-windows.zip>

Then run:

```powershell
.ltfins-skills.exe list
.ltfins-skills.exe install --platform copilot --all
```

Python fallback inside the ZIP:

```powershell
.ltfins-skills.cmd list
```

The Windows ZIP contains:
- `altfins-skills.exe`
- `altfins-skills.cmd`
- `repo/` with the bundled skills, docs, and validator scripts

## Project-Mode Platforms

`Cursor` and `OpenClaw` install into a project instead of a user-home skills directory.

### Cursor

```bash
altfins-skills install --platform cursor --mode project --project-dir /path/to/project altfins-query-builder
```

This writes:
- `.cursor/rules/<skill>.mdc`
- `.altfins-skills/cursor/<skill>/`

### OpenClaw

```bash
altfins-skills install --platform openclaw --mode project --project-dir /path/to/project altfins-market-analyst
```

This writes:
- `AGENTS.md` section for the skill
- `.altfins-skills/openclaw/<skill>/`

## Developer Fallback

If you are working directly from a clone of the repository, you can still use the Python entrypoint:

```bash
python3 scripts/skills.py list
python3 scripts/skills.py install --platform codex --all
python3 scripts/skills.py package --all
```

## Supported Platforms

| Platform | Supported mode(s) | Install surface |
|----------|-------------------|-----------------|
| Codex | `skills` | `$CODEX_HOME/skills/<skill>` or `~/.codex/skills/<skill>` |
| Claude | `skills` | `~/.claude/skills/<skill>` |
| Gemini | `skills` | `~/.gemini/skills/<skill>` |
| Copilot | `skills` | `~/.copilot/skills/<skill>` |
| Cursor | `project` | `<project>/.cursor/rules/<skill>.mdc` + `<project>/.altfins-skills/cursor/<skill>/` |
| OpenClaw | `project` | `<project>/AGENTS.md` + `<project>/.altfins-skills/openclaw/<skill>/` |

## Public Commands

```bash
altfins-skills list [--platform PLATFORM] [--mode MODE] [--project-dir PATH] [--json]
altfins-skills package [SKILL ... | --all]
altfins-skills install --platform PLATFORM [--mode skills|project] [--project-dir PATH] [SKILL ... | --all] [--force]
altfins-skills uninstall --platform PLATFORM [--mode skills|project] [--project-dir PATH] [SKILL ... | --all] [--force]
altfins-skills status [--platform PLATFORM] [--mode MODE] [--project-dir PATH] [--json]
```

The same subcommands are available through `python3 scripts/skills.py ...` in a repo checkout.

## Package Output

```text
dist/skills/<skill-name>.skill.zip
```

Each archive contains the skill folder itself as the zip root.

## Validation Behavior

`package` and `install` run these checks before doing any work:

```bash
python3 scripts/validate_skills.py
python3 scripts/lint_markdown_contracts.py
```

## Release Assets

Public releases publish these installable artifacts:
- `altfins-ai-skills-src.tar.gz`
- `altfins-skills-windows.zip`
- `altfins-skills.rb`

See [docs/releasing.md](releasing.md) for the release checklist.
