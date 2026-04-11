# Validation Scenarios

Use these scenarios to smoke-check `altfins-query-builder`.

## Scenario 1: Clear CLI-ready request

### Input

```text
Show me bullish BTC and ETH signals since March 1.
```

### Expected behavior

- classify this as a signal feed request
- choose a CLI-ready request plan
- map it to `af signals list` with validated inputs
- keep the output clear enough that another agent can execute it directly

### Failure signals

- chooses the wrong command family
- invents unsupported parameters
- stays vague even though the target family is clear

## Scenario 2: Ambiguous screening request

### Input

```text
Find me promising large-cap setups.
```

### Expected behavior

- classify this as a market screening request
- note that the target family is clear but key filters are missing
- choose an interface-neutral brief or a partially specified CLI-ready plan with explicit missing inputs

### Failure signals

- invents unsupported shorthand filters
- pretends the request is fully specified when it is not
- skips the missing-inputs section

## Scenario 3: MCP-oriented analysis prompt

### Input

```text
Give me a complete technical analysis of SOL.
```

### Expected behavior

- classify this as an MCP-oriented technical analysis request
- return an MCP-ready prompt or structured brief
- avoid inventing MCP method names
- keep the prompt grounded in validated capability families

### Failure signals

- outputs fake MCP tool calls
- routes it to an unrelated CLI family
- omits the expected structured output boundary
