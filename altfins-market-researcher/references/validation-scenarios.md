# Validation Scenarios

Use these scenarios to smoke-check `altfins-market-researcher`.

## Scenario 1: Historical analytics export

### Input

```text
I need daily RSI history for BTC for the first half of March in JSON.
```

### Expected behavior

- pick `af analytics history`
- include symbol, analytics type, interval, and date range
- recommend `-o json`
- avoid inventing shortcut flags that were not validated

### Failure signals

- routes to the wrong command family
- invents unsupported flags
- forgets the date range or output format requirement

## Scenario 2: Request-shape verification

### Input

```text
Show me how to preview the exact market search request before sending it.
```

### Expected behavior

- route to a validated CLI command family such as `af markets search`
- use `--dry-run`
- explain that `af commands -o json` is also available for command discovery if relevant

### Failure signals

- ignores `--dry-run`
- claims the CLI cannot preview requests
- invents a non-existent debug flag

## Scenario 3: Interactive browsing request

### Input

```text
I want an interactive market browser starting from BTC.
```

### Expected behavior

- route to `af tui markets --symbol BTC`
- keep the answer focused on the TUI path rather than a one-shot export
- avoid treating local `/` search as remote API filtering

### Failure signals

- suggests an unrelated one-shot command instead of TUI
- invents unsupported TUI flags
- misdescribes local search behavior

## Scenario 4: Complex screening request

### Input

```text
I want a richer market screen than simple flags can express. Show me the safest CLI way to shape that request.
```

### Expected behavior

- identify that this should move beyond flag-only guidance
- recommend `--filter` or `--stdin-json`
- avoid fabricating body keys if they are not fully validated for the task
- suggest `--dry-run` when the request shape matters

### Failure signals

- forces everything into guessed shorthand flags
- invents unvalidated JSON keys
- skips the preview-before-run step when it would help
