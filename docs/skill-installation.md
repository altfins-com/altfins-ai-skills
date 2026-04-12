# Skill Installation

This document explains the public installation story for `altfins-ai-skills`.

## Summary

The project now has two user-facing installation paths:

- `macOS and Linux`: Homebrew-first
- `Windows`: downloadable ZIP-first

The current repo checkout path remains available as a developer fallback.

## macOS and Linux

The intended public install flow for tagged releases is:

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

The intended public install flow for tagged releases is:

```powershell
# Download and unzip altfins-skills-windows.zip
.\altfins-skills.exe list
.\altfins-skills.exe install --platform copilot --all
```

Python fallback inside the ZIP:

```powershell
.\altfins-skills.cmd list
```

The Windows ZIP should contain:
- `altfins-skills.exe`
- `altfins-skills.cmd`
- `repo/` with the bundled skills, docs, and validator scripts

## Developer Fallback

If you are working directly from a clone of the repository, you can still use the Python entrypoint:

```bash
python3 scripts/skills.py list
python3 scripts/skills.py install --platform codex --all
python3 scripts/skills.py package --all
```

## Supported Platforms

| Platform | Install support in v1 | Install root |
|----------|------------------------|--------------|
| Codex | Yes | `$CODEX_HOME/skills` or `~/.codex/skills` |
| Claude | Yes | `~/.claude/skills` |
| Gemini | Yes | `~/.gemini/skills` |
| Copilot | Yes | `~/.copilot/skills` |
| Cursor | Recognized, not installable in v1 | deferred |
| OpenClaw | Recognized, not installable in v1 | deferred |

`Cursor` and `OpenClaw` remain deferred in this pass because the current installer only handles skills-only installation, not project-level rules, hooks, or `AGENTS.md` wiring.

## Public Commands

```bash
altfins-skills list [--platform PLATFORM] [--json]
altfins-skills package [SKILL ... | --all]
altfins-skills install --platform PLATFORM [SKILL ... | --all] [--force]
altfins-skills uninstall --platform PLATFORM [SKILL ... | --all] [--force]
altfins-skills status [--platform PLATFORM] [--json]
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

Tagged releases are expected to publish these public artifacts:
- `altfins-ai-skills-src.tar.gz`
- `altfins-skills-windows.zip`
- `altfins-skills.rb` as a rendered Homebrew formula helper artifact

See [docs/releasing.md](releasing.md) for the release checklist.
