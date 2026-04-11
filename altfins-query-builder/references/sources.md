# Trusted Sources

Use this skill conservatively.

## Preferred source order

1. User intent and constraints
2. Official altFINS documentation
3. Validated CLI help or MCP metadata for the intended target interface
4. Verified repository context relevant to the translation target

## Rules

- Do not invent query parameters, command flags, endpoints, or MCP methods.
- Keep translations high-signal and easy to hand off.
- When the target interface is unconfirmed, produce an interface-neutral request brief instead of a fake concrete query.
- Make missing inputs explicit when they block a reliable translation.
