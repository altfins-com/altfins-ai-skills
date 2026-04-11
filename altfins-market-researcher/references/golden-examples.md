# Golden Examples

Use these examples as quality benchmarks for `altfins-market-researcher` outputs. They show what a strong CLI recommendation should look like when grounded in validated command surfaces.

## Example 1: Simple history export

### Input

```text
I need daily RSI history for BTC for the first half of March in JSON.
```

### Golden output

```text
Best command family: af analytics history
Why it fits:
- the task is a one-symbol indicator history request
- the key parameters map cleanly to validated flags
- JSON output is explicitly requested

Recommended command:
af analytics history --symbol BTC --type RSI14 --interval DAILY --from 2026-03-01 --to 2026-03-15 -o json

Optional preview step:
af analytics history --symbol BTC --type RSI14 --interval DAILY --from 2026-03-01 --to 2026-03-15 --dry-run -o json
```

### Why this is good

- it chooses the correct command family quickly
- it uses only validated flags
- it adds a dry-run preview because the request shape matters

## Example 2: Complex market-screen planning

### Input

```text
I want a richer market screen than simple flags can express. Show me the safest CLI way to shape that request.
```

### Golden output

```text
Best command family: af markets search
Best shaping mode: JSON-body planning

Why this route fits:
- the request is explicitly more complex than a simple symbol list plus display fields
- af markets search validates both --filter and --stdin-json
- the exact body keys should only be written when they are validated for the specific task

Safe handoff:
- use af markets search with --filter @market-screen.json or --stdin-json
- describe the body at the planning level if field-level certainty is not available
- add a --dry-run preview step before execution
```

### Why this is good

- it does not force a complex screen into guessed shorthand flags
- it stays honest about body-key certainty
- it preserves a practical next step

## Example 3: Interactive TUI recommendation

### Input

```text
I want an interactive market browser starting from BTC.
```

### Golden output

```text
Best command family: af tui markets
Why it fits:
- the request is explicitly interactive
- the CLI already exposes a validated TUI market surface

Recommended command:
af tui markets --symbol BTC

Note:
- use / inside the TUI for local search over loaded rows
- keep API-side filtering separate from local TUI search
```

### Why this is good

- it respects the interactive intent
- it does not confuse TUI-local search with remote filtering
