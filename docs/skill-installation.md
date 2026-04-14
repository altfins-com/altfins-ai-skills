# Skill Installation

This document explains the public installation story for `altfins-ai-skills`.

## Summary

The project has four user-facing installation paths:

- `macOS and Linux`: Homebrew-first
- `Windows`: downloadable ZIP-first
- `Claude Code`: local subagent install
- `Claude Cowork`: package-and-upload flow
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
- The actual skill copy into `$CODEX_HOME/skills`, `~/.claude/agents` plus `~/.claude/skills`, `~/.gemini/skills`, or `~/.copilot/skills` happens only when you run `altfins-skills install ...`.

**Optional companion install:** if you want CLI-driven research workflows, also install the **altFINS CLI (`af`)** from [altfins-cli](https://github.com/altfins-com/altfins-cli). This is most relevant for `altfins-market-researcher`, while `altfins-market-analyst` can use it as an additional evidence source.

## Windows

Download:

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

The Windows ZIP contains:
- `altfins-skills.exe`
- `altfins-skills.cmd`
- `repo/` with the bundled skills, docs, and validator scripts

## Claude

### Claude Code

Use `claude-code` when you want local subagents inside Claude Code.

```bash
altfins-skills install --platform claude-code altfins-market-analyst
```

This writes:
- `~/.claude/agents/<skill>.md`
- `~/.claude/skills/<skill>/`

The `.md` file is the Claude Code subagent entrypoint. The bundled skill folder stays alongside it so the subagent can reference the installed skill contract and assets.

### Claude Cowork

Use `claude-cowork` when you want to upload a skill ZIP in the Claude UI.

```bash
altfins-skills package altfins-market-analyst
```

Then upload:

```text
dist/skills/altfins-market-analyst.skill.zip
```

Upload path in Claude:
- `Customize > Skills`

`claude-cowork` is intentionally package-oriented. It does not support `altfins-skills install ...` because Claude Cowork imports skills through the UI.

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
| Claude Code | `skills` | `~/.claude/agents/<skill>.md` + `~/.claude/skills/<skill>/` |
| Claude Cowork | `package-upload` | `dist/skills/<skill>.skill.zip` uploaded in `Customize > Skills` |
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

Notes:
- Use `--platform claude-code` for local Claude Code subagents.
- Use `altfins-skills package ...` for Claude Cowork ZIP uploads.
- `--platform claude` still works as a backward-compatible alias for `claude-code`, but `claude-code` is the preferred name.

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
