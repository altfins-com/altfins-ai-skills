# Golden Examples

Use these examples as quality benchmarks for `altfins-market-analyst` outputs. They intentionally use evidence placeholders where live data would normally appear, because this repository should not embed fabricated market facts.

## Example 1: Short outlook

### Input

```text
What is the current technical outlook for BTC?
```

### Golden output

```text
Objective
- Assess the current technical outlook for BTC using validated altFINS-facing evidence.

Validated Facts
- [validated trend or structure fact]
- [validated indicator or technical-analysis fact]
- [validated signal or context fact, if present]

Interpretation
- Taken together, the validated evidence supports [cautious bullish / cautious bearish / mixed] conditions rather than a fully confirmed move.
- The strongest part of the case is [most important validated factor].
- The weakest part of the case is [main uncertainty or unsupported link].

Open Questions
- [open question 1]
- [open question 2]

Suggested Next Checks
- [next check 1]
- [next check 2]
```

### Why this is good

- facts and interpretation are clearly separated
- the answer avoids fake certainty
- the output mode matches a short outlook request

## Example 2: Structured analysis memo

### Input

```text
Give me a complete technical analysis of SOL.
```

### Golden output

```text
Objective
- Deliver a structured technical analysis of SOL using validated altFINS-facing evidence.

Validated Facts
- [validated market structure fact]
- [validated indicator fact]
- [validated signal fact]
- [validated context fact if relevant]

Interpretation
- The evidence currently points to [summary interpretation], but that conclusion still depends on [main uncertainty].
- The setup looks strongest if [supporting condition].
- Confidence should remain limited where the evidence does not directly confirm [claim].

Open Questions
- [open question 1]
- [open question 2]

Suggested Next Checks
- [next check 1]
- [next check 2]
```

### Why this is good

- it uses the right analysis-memo shape
- it preserves analytical discipline without drifting into advice
- it shows how to end with next checks instead of overclaiming certainty

## Example 3: Market scan summary

### Input

```text
Summarize the most interesting technical setups you can find and tell me what to look at next.
```

### Golden output

```text
Scan Objective
- Identify a small set of technically interesting candidates using validated altFINS-facing evidence.

Top Candidates
- Candidate 1: [asset] — strongest validated facts: [fact cluster]; biggest uncertainty: [uncertainty]
- Candidate 2: [asset] — strongest validated facts: [fact cluster]; biggest uncertainty: [uncertainty]
- Candidate 3: [asset] — strongest validated facts: [fact cluster]; biggest uncertainty: [uncertainty]

Common Patterns
- [pattern 1]
- [pattern 2]

Risks and Missing Inputs
- [risk or missing input 1]
- [risk or missing input 2]

Suggested Follow-Up Checks
- [follow-up 1]
- [follow-up 2]
```

### Why this is good

- it chooses a scan-summary mode instead of forcing a single-asset memo
- it keeps the candidate summaries short and evidence-led
- it still highlights uncertainty and next steps
