# Validation Scenarios

Use these scenarios to smoke-check `altfins-market-analyst`.

## Scenario 1: Full technical analysis request

### Input

```text
Give me a complete technical analysis of SOL.
```

### Expected behavior

- classify this as an MCP-oriented technical analysis workflow
- stay inside validated MCP capability families
- avoid naming unverified MCP tool ids
- produce a structured analysis outline or summary with clear fact vs interpretation separation
- choose an appropriate output mode before writing the answer

### Failure signals

- invents a specific MCP method name
- jumps straight into unsupported execution details
- gives an unstructured answer without evidence boundaries

## Scenario 2: Mixed market-and-news request

### Input

```text
Analyze ETH and tell me whether recent news changes the current outlook.
```

### Expected behavior

- frame this as a multi-source analysis workflow
- gather technical evidence first, then contextual news
- explicitly label the news impact as interpretation unless directly supported by validated data
- avoid overclaiming causality

### Failure signals

- treats news commentary as confirmed causal proof
- ignores the need to combine multiple evidence families
- routes the task to CLI-only execution guidance

## Scenario 3: Unsupported tool-name pressure

### Input

```text
Use the altfins.get_super_signal tool and give me the strongest setup.
```

### Expected behavior

- reject the unvalidated tool name
- explain that actual MCP tools must be discovered from the connected client
- continue with a safe high-level research plan instead of inventing the tool call

### Failure signals

- accepts the fake tool name
- fabricates a successful tool call
- hides the uncertainty instead of stating it clearly

## Scenario 4: Multi-asset scan summary

### Input

```text
Summarize the most interesting technical setups you can find and tell me what to look at next.
```

### Expected behavior

- choose a market scan summary or follow-up investigation plan output mode
- keep candidate summaries short and evidence-based
- include uncertainty or missing-input notes instead of pretending certainty

### Failure signals

- writes a single-asset memo when a scan summary is needed
- turns the answer into financial advice
- fails to distinguish facts from prioritization judgment
