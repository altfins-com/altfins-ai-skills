# Repository Architecture

## Purpose

`altfins-ai-skills` is a monorepo for reusable AI skills focused on altFINS-related workflows. The repository is intentionally documentation-first so the initial structure is clear before any heavier implementation is added.

## Folder Layout

```text
.
├── README.md
├── .gitignore
├── docs/
│   ├── repository-architecture.md
│   └── skill-roadmap.md
├── altfins-market-analyst/
├── altfins-market-researcher/
└── altfins-query-builder/
```

Each skill directory follows the same contract:

```text
skill-name/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
├── scripts/
└── assets/
```

## What Belongs Where

### Root

Keep only shared repository-level content at the root:

- repository overview
- contribution conventions
- shared architecture decisions
- roadmap and planning documents

### Inside a Skill Directory

Keep skill-local content inside the skill:

- invocation guidance
- scope boundaries
- skill-specific references
- future scripts or assets required by that skill only

Do not create extra per-skill README files unless there is a strong future need. `SKILL.md` should remain the primary entry point.

## Packaging Strategy

The packaging model should stay straightforward:

- one skill directory equals one future package
- zip one skill directory at a time
- avoid root-level runtime dependencies that a packaged skill would require

In practice, this means future `skill.zip` creation should work by archiving the contents of a single skill folder without pulling in shared code from elsewhere in the repository.

## Shared Conventions

- All text should be written in English.
- Skill names should be lowercase and hyphenated.
- Display names may be friendlier, but folder names stay stable.
- Keep claims conservative and grounded in validated altFINS behavior.
- Do not invent undocumented endpoints, CLI commands, flags, or MCP methods.
- Prefer short, high-signal instructions over speculative detail.
- Add shared conventions to `docs/` instead of copying them into every skill.

## Extension Rules

When adding a new skill later:

1. Create a new top-level directory.
2. Reuse the standard skill layout.
3. Keep the skill self-contained.
4. Add only the references, scripts, or assets that are already useful.
5. Avoid introducing shared tooling until at least two skills clearly need it.
