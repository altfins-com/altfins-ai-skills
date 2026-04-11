# Translation Playbook

Use this playbook to convert a plain-English research request into a safer structured handoff.

## Step 1: Identify the real task type

Classify the request into one of these buckets:

- market scan
- historical indicator lookup
- candle history lookup
- signal feed lookup
- curated technical analysis lookup
- news or event lookup
- broader market analysis workflow

## Step 2: Gather the missing dimensions

Ask for or clearly mark assumptions around:

- assets or asset universe
- timeframe or interval
- date range
- filter conditions
- desired output format
- execution target: CLI, MCP, or neutral brief

## Step 3: Choose the safest output mode

### Interface-neutral brief

Use when the target interface is unclear.

Suggested shape:

- Goal
- Assets
- Timeframe
- Constraints
- Best matching target family
- Missing inputs

### CLI-ready request plan

Use when the CLI target is validated.

Suggested shape:

- Goal
- Best command family
- Required flags or request body inputs
- Optional `--dry-run` preview step
- Output format recommendation

### MCP-ready research prompt

Use when the user is clearly working through an MCP client.

Suggested shape:

- Goal
- Relevant MCP capability family
- Evidence to gather
- Expected synthesis output

## Step 4: Avoid fake precision

- Do not invent JSON body keys.
- Do not invent MCP method names.
- Do not invent display fields or analytics ids when discovery commands exist.
- When the request needs discovery first, say that explicitly.

## Step 5: Hand off clearly

A good translation should let another skill or agent continue the work without reinterpreting the user's intent from scratch.
