---
name: prove-it
description: "prove-it: every claim must be provable. A research log system built on epistemic provenance, plus a human-in-the-loop research workflow: for every claim in a research project, keep a complete record of where it came from, why it holds, and how it changed; every hypothesis passes two checkpoints with the user, at experiment design and at result analysis. Use this skill whenever the user is doing research or experiments: discussing experiment design, analyzing results and deciding next steps, initializing a research log, recording experiment results, writing down a new idea, taking paper notes, updating hypothesis status, comparing experiment numbers, asking about research progress, reviewing the log, or writing papers and reports from the log. Also use it when the user mentions research_log, hypotheses.md, research journal, lab notebook, experiment log, ablation, 研究紀錄, 實驗紀錄, or 研究筆記, even if they don't name this skill."
license: MIT
compatibility: Helper scripts need Python 3 (standard library only). Without Python, the log format and workflows still work.
---

# prove-it: every claim must be provable

Built on the principle of epistemic provenance.

> **For every claim in a research project, keep a complete record of where it came from, why it holds, and how it changed.**

This skill maintains a `research_log/` in the project. Its purpose is to keep researchers, human or agent, from fooling themselves: recording an after-the-fact explanation as the original design (source confusion), rewriting the original reasoning once the result is known (hindsight bias), and comparing same-named numbers measured by different methods (protocol mixing). Each rule below counters one of these. Understanding the reason matters more than following the format; when the format doesn't cover a case, decide by the principles.

## Language

Collaborate with the user, and write the log, in one consistent language, chosen in this order:

1. The user's explicit preference (agent memory, `AGENTS.md`, `CLAUDE.md`, or what they tell you)
2. The "Log language" recorded in the project's `research_log/README.md`
3. The language the user is writing in now

Use that language both in conversation and in every log file. The templates are in English: translate their headings and fixed phrases into the log language when you fill them in. Technical terms may stay in English. When initializing a log, record the chosen language in `README.md` so later sessions and other agents keep it. Don't mix languages within one log; if the user switches languages for good, ask before switching the log, and note the switch in `README.md`.

Keep these tokens in English in every language, because the scripts parse them: status words (`open`, `proposed`, …), frontmatter keys, `H#` IDs, and file names.

## Directory structure

```
research_log/
├── README.md                  How to use the log, log language, causal lines, guidance for reviewers
├── hypotheses.md              Hub index: all hypotheses and their status; the current research frontier sits at the top
├── methods.md                 Evaluation protocol registry: definitions, recipes, pitfalls, version changes
├── research_tree_overview.md  Research tree: hypothesis → design → result → inference ⟹ next hypothesis
├── comparison_catalog.md      Comparison catalog: every "A vs B" in one format, with an index by variable
├── ideas/NNN-slug.md          Idea evolution: numbered chronologically, one file per turn in thinking
├── papers/slug.md             Paper notes: one file per paper
└── experiments/exp-slug.md    Experiment records: one file per set of experiments
```

Templates are in `assets/templates/`. Day to day, read only `hypotheses.md` and open other files as needed; don't read the whole log from the start.

## Core principles

1. **Separate causal lines**: research branches into several causal lines, for example "original research motivation" and "contribution framing or methodological questions that appeared only after seeing results". Each idea states which line it belongs to. Reason: packaging an advantage found after the fact as the original design is dishonest, and reviewers see through it easily. The lines are defined in the project's `research_log/README.md`.
2. **Append only, never rewrite**: refuted ideas are kept; change the frontmatter to `status: refuted` and add an "## Update (date)" section at the end explaining the new evidence. Reason: once rewritten, you can no longer see why you thought what you thought. Exception: fixing typos, broken links, or numbering, with a note at the fix.
3. **Write the prediction before seeing the result**: before an experiment, write down "what we should see if it holds, and what result means it does not", and **get the user's confirmation** at checkpoint one. Reason: without a prior prediction, any result can be explained as expected; predictions written by the agent alone tend to be too vague.
4. **Know how every number was measured**: `methods.md` registers every evaluation protocol; before citing or comparing a number, confirm it uses the same protocol and version; record protocol changes in the version history. Reason: same-named numbers may come from different methods, and mixing them is the most common source of misjudgment.
5. **Incomparabilities and information source**: paper notes state comparability, **what is not comparable**, and `source` (read full text / abstract only / secondary summary / from memory). Experiment records state limitations. **A paper must be read in full before it is compared against, cited, or used as the basis for an implementation**; then update `source` to "read full text (date)". Papers read only at the abstract level can be used for brainstorming only.
6. **Reproducible**: experiment records include the full command, code version (commit hash), result paths, seeds, and hardware.
7. **Hypothesis status vocabulary**: `open` (not yet tested) → `proposed` (design proposed, awaiting user confirmation) → `planned` (confirmed by the user) → `analyzing` (experiment finished, analysis under discussion, conclusion not confirmed) → `supported` (evidence under limited conditions) / `confirmed` / `refuted` / `superseded` (replaced by a more precise hypothesis). When a conclusion only half holds, state exactly which part holds. What counts as `confirmed` depends on the claim type, and the status cell must state the type:

   | Claim type | Condition for confirmed |
   |---|---|
   | Implementation (code or formula implemented correctly) | Passes a validation test **with a known correct answer** (analytic solution, reference implementation, equivalence test); a smoke test that only shows it runs is not enough |
   | Experimental (a phenomenon we observed ourselves) | Holds across multiple seeds or multiple conditions |
   | Literature-dependent (mechanistic explanation, others' conclusions) | Stays `supported` unless our own experiments independently verify it |
8. **Record who made each decision**: for every design decision, record the options, the choice, **who decided** (user / agent-proposed, user-approved / agent default, undiscussed / per literature), and the reason. Reason: decisions have sources too; how much "why this value" weighs in a paper depends on who decided it and on what basis.

## Frontmatter and links

```markdown
---
type: idea | experiment | paper
status: open | proposed | planned | analyzing | supported | confirmed | refuted | superseded | done
date: YYYY-MM-DD
related: [relative paths, ...]
---
```

Experiments also have `seeds:` and `results:`; papers also have `title`, `authors`, `venue`, `source`. Link files with **relative markdown links**. Run `scripts/check_links.py` after writing.

## Node lifecycle and human checkpoints (core workflow)

Research advances in **nodes** (one hypothesis plus the set of experiments that tests it). Each node has two human checkpoints where the agent stops, discusses with the user, and continues only after confirmation. Reason: research direction and experiment design are the user's research judgment; if the agent finishes first and then says "you can overrule this", overruling means rerunning, and users tend to accept the fait accompli.

```
① Propose a hypothesis (idea; status open)
② Checkpoint one: design discussion → agent proposes a design table → lists review options → user confirms (proposed → planned)
③ Run (don't actively monitor long runs; wait for the user to say it's done)
④ Checkpoint two: analysis discussion (status analyzing; usually many rounds, still the same node)
   ④-1 Initial report → stop and wait for the user
   ④-2 Discussion loop: settle one or two issues at a time, run diagnostics if needed → record consensus and open issues each round
   ④-3 Conclusion confirmation: agent summarizes the conclusion → user explicitly agrees
⑤ Record (workflow B); only after the conclusion is confirmed, propose options for the next node
```

**The checkpoint-one design table** contains at least: the hypothesis to answer (H#) and its causal line; variables, controls or baselines, fixed conditions; evaluation protocol and number of seeds; **the prediction**; cost estimate; **what the user needs to decide** (list the options and the agent's recommendation; don't choose on your own). Once confirmed, set the status to `planned` and write the decisions into the experiment record's "Design decision log". A related batch of experiments can share one checkpoint one. Only decisions that affect **variables, metrics, or claims** need to pass a checkpoint; details like plot formatting do not.

**Checkpoint two is a discussion, not a report.** Conclusions form over several rounds of discussion; the next node is a product of the conclusion, not an add-on to the analysis. Reason: agents tend to deliver a "complete" answer in one turn, packaging analysis, conclusion, and next steps together, so the user faces a finished conclusion and a menu instead of reasoning together.

- **④-1 Initial report**: result vs prediction, anomalies, deviations of the implementation from the source paper or the design, alternative explanations (noise, confounders, implementation bugs, protocol problems), what this result **cannot** support, and review options. Then **stop** and ask for the user's interpretation and which issue to discuss first. **Don't propose the next node yet**, and don't update hypothesis status. If the result relies on papers not yet read in full, read them before reporting.
- **④-2 Discussion loop**: handle only one or two issues per round. Anomalies, implementation bugs, and needed diagnostic experiments **stay within the same node** (explain the design of any small extra experiment and run it only with the user's consent); they are not a reason to open a new node. At the end of each round, faithfully record the user's interpretation, the consensus reached, and what remains open in the experiment record's "Analysis discussion", including the parts the agent thinks need correcting. Review options can be invoked at any point in the loop.
- **④-3 Conclusion confirmation**: when the agent thinks all issues are settled, it summarizes "this node's conclusion, claim type and status, limitations, open issues" and asks the user to confirm or revise. **Only after the user explicitly agrees** does it record per workflow B and update the hypothesis status.
- **⑤ Next node**: only after the conclusion is confirmed, propose 2–3 options, each stating what it would answer, its cost, and its value to the main line, with the agent's recommendation. The user may also propose a direction during the discussion; record it faithfully.

**Review options**: at both checkpoints, **proactively list** the two options below; do them only if the user asks; the user may choose neither. The agent may add its view on whether it's worth doing this time (for example, "the result contradicts the prediction; I recommend a rigor review"), but the user decides. Use a multiple-choice question tool if available (multi-select); otherwise ask with a bulleted list.
- **Rigor review**: find fallacies and give rigorous recommendations. Method and fallacy checklist in `references/rigor-review.md`. If the user has an interrogation-style skill or tool (e.g. grill-me), it can be used instead.
- **Literature search**: first propose specific search questions and reasons; search only after the user agrees. See `references/literature-search.md`.

## Day-to-day workflows

**B. Record experiment results** (after the checkpoint-two conclusion is confirmed; during discussion, update only the experiment record's "Results" and "Analysis discussion", with status `analyzing`). Update in this order; skipping any one makes the log contradict itself:
1. `experiments/exp-<slug>.md` (template `experiment.md`): motivation, prediction, design decision log, method, results, analysis discussion, conclusion, limitations
2. `hypotheses.md`: status and evidence cells (state the claim type), new hypotheses, the frontier questions at the top
3. `comparison_catalog.md`: A vs B comparisons and the variable index
4. `research_tree_overview.md`: blocks whose status changed
5. `methods.md`: new protocols or protocol changes
6. Open a new idea if it sparked one; run `check_links.py`; commit per the user's conventions

Write only what actual data supports; mark experiments not yet run as `planned`.

**C. New idea**: open one when a new hypothesis, a new interpretation, a user's viewpoint, a change of direction, or abandoning a path appears. Continue from the highest number; state the source, causal line, argument, prediction, and next steps. **Record the user's ideas faithfully**, including which parts hold and which need correcting.

**D. Paper notes**: template `paper.md`; the key parts are "Relation to our work", "What is not comparable", and an honest `source`.

**E. Progress report and research history review**: first decide whether the user wants the short version ("where are we": frontier only) or the full version ("review from the start", "report to my advisor": **review node by node in the order the research depended on**, not regrouped by topic); if unclear, ask. Method in `references/workflow-progress-report.md`.

**Other workflows** (read only when needed):
| Situation | Read |
|---|---|
| Initialize a research log for a new project | `references/workflow-init.md` |
| Report progress, review the research history from the start, report to an advisor or collaborator | `references/workflow-progress-report.md` |
| Check the log itself for errors (inaccurate status, mixed protocols, conclusions beyond the evidence); do this before handing it to others | `references/workflow-review-log.md` |
| Write papers or reports from the log | `references/workflow-writing.md` |

## Writing style
Use the language chosen under "Language" above. Prefer tables to long paragraphs. Give numbers with units, seed counts, and protocol. When unsure, say "speculative" or "unverified" outright.
