---
type: experiment
status: planned
date: {{YYYY-MM-DD}}
seeds: []
results: []
related: []
---

# Experiment: {{Title}}

## Motivation
{{Which idea it comes from, which hypothesis H# it answers, which causal line it belongs to}}

## Prediction (checkpoint one, confirmed by the user on {{YYYY-MM-DD}})
- If it holds, we should see: {{}}
- Seeing {{}} means it does not hold

## Design decision log (checkpoint one)

| Decision | Options | Chosen | Decided by | Reason |
|---|---|---|---|---|
| {{e.g. learning rate}} | {{1e-3 / 1e-2}} | {{1e-3}} | {{user / agent-proposed, user-approved / agent default, undiscussed / per literature}} | {{}} |

Checkpoint-one review: {{not chosen / summary of rigor review / summary of literature search (link to papers/)}}

## Method
- Code version: {{commit hash}}
- Command:
  ```bash
  {{full reproducible command}}
  ```
- Settings: {{differences from the baseline}}
- Protocol: {{which protocol from methods.md is used for evaluation}}
- Hardware: {{; shared with other jobs or not}}

## Results

| Setting | {{Metric (protocol)}} |
|---|---|
| | |

## Analysis discussion (checkpoint two, may take several rounds)
### Initial report (④-1)
- Result vs prediction: {{matches / does not match / partly matches, with specifics}}
- Anomalies and implementation deviations: {{}}
- Alternative explanations: {{}}

### Discussion record (④-2, append one section per round)
#### Round 1 (YYYY-MM-DD): {{Issue}}
- User's interpretation: {{record faithfully; also note the parts the agent thinks need correcting}}
- Extra diagnostics: {{none / design and results}}
- Consensus: {{}}
- Open: {{}}
- Review: {{not chosen / problems found by rigor review and how they were handled / literature search results}}

### Conclusion confirmation (④-3)
- Date confirmed by the user: {{YYYY-MM-DD; status stays analyzing until confirmed}}
- Next-step options and the user's choice: {{proposed only after the conclusion is confirmed; list the options, which one was chosen, and why}}

## Conclusion
1. {{Which hypothesis is supported or refuted, and by what evidence}}

## Limitations
- {{Seed count, conditions tested, alternative explanations not ruled out, incomparabilities, undiscussed design decisions}}
