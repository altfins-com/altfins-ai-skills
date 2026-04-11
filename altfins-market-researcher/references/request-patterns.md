# Request Patterns

Use this file to choose a safe request-shaping pattern for the altFINS CLI.

## Pattern 1: Simple flag-first requests

Use this when:

- the command family is obvious
- the request only needs a few validated flags
- the intent does not require a complex JSON body

Common fits:

- `af analytics history`
- `af signals list`
- `af ohlcv history`
- `af ta list`
- `af news list`

## Pattern 2: `--filter` JSON file usage

Use this when:

- the user wants a more complex query than simple flags can express cleanly
- you want a reusable request body stored in a file
- the request should be reviewed before execution

Safe rule:

- only describe `--filter @path/to/filter.json` when the CLI surface explicitly validates `--filter`
- if the body keys themselves are not fully validated, describe the planning shape rather than inventing the JSON

## Pattern 3: `--stdin-json` usage

Use this when:

- the request body should be piped in from another process or shell step
- the command already validates `--stdin-json`
- the user or agent wants to avoid a temp file

Safe rule:

- present this as a body-delivery pattern, not as proof of a specific body schema

## Pattern 4: `--fields` trimming

Use this when:

- the result set is too noisy for the task
- the user wants a smaller export or handoff
- the exact field selection is already known or discoverable

## Pattern 5: `--dry-run` preview

Use this when:

- the request shape itself needs review
- the agent is handing off a command to another user or system
- the body/filter plan is more important than immediate execution

## Selection Rule

Choose the lightest pattern that safely represents the query:

- stay flag-first when the request is already clear
- escalate to `--filter` or `--stdin-json` when flag-only guidance would become speculative
