# Workflow E: progress report and research history review

Read this when the user asks "where are we now", "review it from the start", "summarize the whole process", or wants to report progress to an advisor or collaborator.

The goal is to let the reader understand each decision **along the path the research actually took**: why this experiment was run, what was seen, and where that led. This differs from workflow G (`workflow-review-log.md`): **G finds errors in the log itself; E tells the path the research took**. When handing the log to others, do both, G first, then E.

## First decide which one is wanted

| What the user says | Output |
|---|---|
| "Where are we", "what are we working on", "any recent results" | **Short version**: frontier only |
| "Review from the start", "summarize the whole process", "report to my advisor / collaborators" | **Full version**: node by node, in dependency order |

If you can't tell, ask; don't pick a structure yourself.

## Short version

Read the frontier questions at the top of `hypotheses.md` and the most recent blocks of `research_tree_overview.md`, and list: nodes in progress, items waiting for the user's decision, and conclusions recently confirmed or refuted. Link each item to its file.

## Full version: node by node, in dependency order

1. **Run the status summary first**: `scripts/log_status.py` (same as step 1 of workflow G). Deal with any inconsistent statuses or waiting nodes first, or flag them in the review.
2. **Structure the review by the research's dependency order, not regrouped by topic.** Follow the block order of `research_tree_overview.md`. If it is outdated or missing nodes, rebuild the order from the H# IDs in `hypotheses.md`, idea numbers and dates, and the `related` fields of experiment records; add the missing blocks to `research_tree_overview.md` first, then write the review.
   Reason: grouping by topic ("mechanism", "comparisons", "boundary conditions", one section each) cuts the causal chain "because of A's result, we did B". The reader sees a pile of conclusions, not how the research got here step by step, and can't tell which directions were forced by results.
3. **One block per node, with fixed fields**:

   ```markdown
   ### N. H# — one-line title (line X; status, claim type)

   - **How we got here**: which result of the previous node triggered it (for the first node, the original motivation)
   - **Hypothesis**: one sentence; who proposed it and when (only if recorded)
   - **Design**: variables, controls, evaluation protocol, number of seeds / folds
   - **Result**: key numbers, with protocol and seed count. A small table or two or three numbers; don't paste the full tables
   - **Inference**: separate measured facts from speculation; state the limitations
   - **⟹ Next**: which node it led to, and why
   ```

4. **List refuted, abandoned, and failed nodes in their original order.** Don't skip them or collect them at the end. They are usually the reason for a change of direction; without them, later nodes look as if they came from nowhere.
5. **Branches**: at the node where the research forks, note "two lines branch from here". Parallel branches can be walked one after the other, but each starts by stating which node it branched from.
6. **Opening and closing**: open with a 5–7 point summary (where things stand: confirmed, refuted, in progress); close with the items awaiting the user's decision and the known corrections needed.
7. **Numbers and wording** follow workflow F (`workflow-writing.md`): separate by causal line, every number traceable to a protocol and seed count, claim strength consistent with status, speculation labeled.

## Where the output goes

The review is a product derived from the log, not part of the log. Don't write it into `research_log/`; put it in the project's reports directory (e.g. `reports/`) or give it directly in the conversation. If you find errors in the log while reviewing, fix them in `research_log/` first (following the append-only rule), then write the review.
