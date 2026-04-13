# Repository Architecture

## Purpose

`altfins-ai-skills` is a monorepo for reusable AI skills focused on altFINS-related workflows. The repository is documentation-first, but it now also carries the installer, packaging, validated surfaces, and project adapters needed to publish and consume the skills directly.

## Folder Layout

```text
.
├── README.md
├── .gitignore
├── bin/
│   ├── altfins-skills
│   └── altfins-skills.cmd
├── docs/
│   ├── releasing.md
│   ├── repository-architecture.md
│   ├── skill-installation.md
│   ├── skill-roadmap.md
│   ├── skill-validation.md
│   ├── validated-sources.md
│   └── validated-surfaces/
├── packaging/
│   └── homebrew/
├── scripts/
│   ├── build_source_archive.py
│   ├── build_windows_bundle.py
│   ├── lint_markdown_contracts.py
│   ├── refresh_validated_surfaces.py
│   ├── render_homebrew_formula.py
│   ├── skills.py
│   ├── skills_core.py
│   ├── test_release_assets.py
│   ├── test_skills.py
│   └── validate_skills.py
├── altfins-market-analyst/
├── altfins-market-researcher/
└── altfins-query-builder/
```

Each skill directory follows the same contract:

```text
skill-name/
├── README.md
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
├── scripts/
└── assets/
    └── project/
```

## What Belongs Where

### Root

Keep only shared repository-level content at the root:

- repository overview
- install and release conventions
- shared architecture decisions
- shared validated source inventory
- checked-in validated CLI and MCP surface snapshots
- repository-wide validation and packaging helpers
- roadmap and planning documents

### Inside a Skill Directory

Keep skill-local content inside the skill:

- invocation guidance
- scope boundaries
- skill-specific references
- skill-specific validation scenarios
- quality benchmarks via golden examples
- skill-local output templates
- project adapter templates for that skill when needed

Per-skill `README.md` files are user-facing onboarding docs. `SKILL.md` remains the primary agent contract.

## Packaging Strategy

The packaging model stays straightforward:

- one skill directory equals one package
- zip one skill directory at a time
- use `altfins-skills package ...` or `python3 scripts/skills.py package ...` as the canonical packaging entrypoint
- tagged releases publish a source tarball for Homebrew and a Windows ZIP for end users
- the repo-level installer owns user-home installs and project-mode adapters

In practice, this means a packaged skill remains self-contained, while the repo-level installer and release helpers distribute the repository in friendlier ways.

## Install Modes

The installer supports two distinct install modes:

- `skills`
  - copies a full skill directory into a user-home skill folder
  - used for Codex, Claude, Gemini, and Copilot
- `project`
  - copies a full skill directory into a project-local `.altfins-skills/` tree
  - writes platform-specific project glue for Cursor or OpenClaw

The project-mode adapters intentionally mirror the project-local style used by `Graphify`:
- Cursor gets a `.cursor/rules/<skill>.mdc` rule file
- OpenClaw gets a managed section in `AGENTS.md`

## Shared Conventions

- All text should be written in English.
- Skill names should be lowercase and hyphenated.
- Display names may be friendlier, but folder names stay stable.
- Keep claims conservative and grounded in validated altFINS behavior.
- Do not invent undocumented endpoints, CLI commands, flags, or MCP methods.
- Prefer short, high-signal instructions over speculative detail.
- Add shared conventions to `docs/` instead of copying them into every skill.
- Put cross-skill source validation into `docs/validated-sources.md`.
- Put checked-in local interface snapshots into `docs/validated-surfaces/`.
- Keep repository-wide validators and packaging helpers under `scripts/` and keep them lightweight and dependency-free when possible.
- Keep markdown links and contract references valid; the markdown linter treats those links as part of the stable repo contract.

## Extension Rules

When adding a new skill:

1. Create a new top-level directory.
2. Reuse the standard skill layout.
3. Keep the skill self-contained.
4. Add only the references, scripts, or assets that are already useful.
5. Avoid introducing shared tooling until at least two skills clearly need it.
6. Add at least one `references/validation-scenarios.md` file.
7. Add at least one `references/golden-examples.md` file.
8. Add `assets/project/` templates if the skill should support project-mode adapters.
9. Run the repository validators before committing structural changes.
