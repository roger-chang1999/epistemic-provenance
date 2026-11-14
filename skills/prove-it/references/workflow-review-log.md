# Workflow G: review the whole log

Read this when the user says "review the research log", wants to hand the log to an advisor or collaborator, or returns to the project after some time away. This reviews **the log itself**, unlike reviewing a single node at a checkpoint (`rigor-review.md`).

**Note**: if what the user wants is "review the path the research took" or "report progress to my advisor", that is workflow E (`workflow-progress-report.md`), not this one. This one only finds errors in the log; when handing the log to others, do this first, then write the review per E.

1. Run:
   ```bash
   python <skill directory>/scripts/log_status.py <research_log directory>
   ```
   This gives a status summary: hypotheses grouped by status, nodes waiting on the user, suspected status inconsistencies, single-seed experiments, undiscussed decisions, papers read only at the abstract level, and stale ideas. The summary is heuristic, meant to point at what is worth a look; **read the summary first and open only the flagged files**; don't read the whole log from the start.
2. Check each flagged item, and also check what the script can't catch:
   - **Is each status accurate?** Does each confirmed meet the condition for its claim type (implementation: a validation test with a known answer; experimental: multiple seeds or conditions; literature-dependent: should stay supported)? Are the limits of each supported stated clearly?
   - **Do conclusions exceed the evidence?** Are the conclusions in hypotheses.md and comparison_catalog.md stronger than what the experiment records say?
   - **Are causal lines confused?** Has any later finding been written up as the original motivation?
   - **Are protocols consistent?** Are the numbers in each comparison table from the same protocol and version?
   - **Append-only**: are refuted ideas kept and marked, not deleted or rewritten? (check with `git log -p`)
   - **Undiscussed decisions**: which of them affect current conclusions and are worth discussing with the user?
   - **Literature basis**: have all papers that are cited, compared against, or implemented from been read in full?
3. Produce a review report sorted by severity (fatal / major / minor), with a file link and a suggested fix for each item.
4. **Confirm with the user before fixing anything.** Follow the append-only rule when fixing: use an "Update" section on old ideas, don't change the original text; the status cells in hypotheses.md may be updated directly, with the reason written down.
5. Run `scripts/check_links.py` to check for format problems.
