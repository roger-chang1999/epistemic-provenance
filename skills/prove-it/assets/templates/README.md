# Research Log — {{PROJECT}}

This directory records the chain of research thinking for {{PROJECT}}, so that "why we ran this experiment" and "why this paper matters" are not forgotten over time. Files reference each other with relative links:

```
research_log/
├── README.md                  This file: how to use the log, log language, causal line definitions
├── hypotheses.md              Hub index: the status of every hypothesis
├── methods.md                 Evaluation protocol registry: which protocol produced each number
├── research_tree_overview.md  Research tree: hypothesis → design → result → inference ⟹ next hypothesis
├── comparison_catalog.md      Catalog of comparison experiments
├── ideas/NNN-slug.md          Idea evolution: numbered chronologically, one file per turn in thinking
├── papers/slug.md             Paper notes: one file per paper
└── experiments/exp-slug.md    Experiment records: one file per set of experiments
```

Before citing or comparing any number, check [methods.md](methods.md) for the protocol that produced it. **Numbers from different protocols must not go in the same comparison table.**

**Log language**: {{e.g. English / 繁體中文}}. Agents collaborate and write in this language; status words, frontmatter keys, and `H#` IDs stay in English.

## ⚠️ Causal lines: decide which line new content belongs to before writing

<!-- Fill in this project's causal lines. At least "original research motivation"; open a new line for any direction that appeared only after seeing results. -->

- **Line 1 (original research motivation)**: [ideas/001](ideas/001-origin.md). {{One sentence describing the original research question}}
- **Line 2 ({{e.g. contribution framing / methodological questions that appeared after the results}})**: {{When, and because of which result, it appeared}}

**Don't mix lines when writing the paper.** Packaging a line that appeared afterward as the initial design goal is dishonest, and reviewers see through it easily.

## How to use

1. **Idea evolution** (`ideas/`): add one file whenever the thinking turns, with incrementing file names `NNN-slug.md`. Include: which hypothesis or experiment it came from, which causal line it belongs to, and what to test next.
2. **Literature** (`papers/`): record the problem setting, comparability, key numbers, and related lines and hypotheses. **Always record "what is not comparable" and the information source.**
3. **Experiments** (`experiments/`): record the corresponding idea, full commands and settings, results, which hypotheses are supported or refuted, and limitations.
4. **Hypothesis index** (`hypotheses.md`): listed separately by causal line; the top always holds "the current research frontier".
5. **Overviews**: add new comparisons to `comparison_catalog.md`; update `research_tree_overview.md` whenever a hypothesis changes status.

## Link and frontmatter conventions

Use relative markdown links, and start each file with frontmatter:

```markdown
---
type: idea | paper | experiment
status: open | proposed | planned | analyzing | supported | confirmed | refuted | superseded | done
date: YYYY-MM-DD
related: [list of relative paths]
---
```

Old ideas are kept even when refuted (append-only): mark them `status: refuted` and add an "Update" section at the end. **Don't go back and rewrite old content.**

## Guidance for reviewers (human or agent)

This log follows the principle of epistemic provenance: every claim must be traceable to where it came from, why it holds, and how it changed. Reviewing it needs no extra tools; follow the order below.

**Where to start**: `hypotheses.md` (current state) → `research_tree_overview.md` (chain of inference) → individual `experiments/` and `ideas/`. Check `methods.md` before citing a number.

**Core principles** (check each one when reviewing):
1. **Separate causal lines**: each idea states its line; later findings must not be written up as the original motivation.
2. **Append only**: refuted ideas are kept and marked `refuted`; new evidence goes in an "Update" section at the end, without changing the original text.
3. **Prediction first**: predictions in experiment records are written before running, and confirmed by the researcher.
4. **Registered protocols**: every number maps to a protocol and version in `methods.md`; numbers from different protocols are not compared in the same table.
5. **Source strength**: a paper's `source` states whether the full text, the abstract, or memory was used; a paper must be read in full before it is cited, compared against, or implemented from. Experiments state their limitations.
6. **Reproducible**: experiment records have full commands, code version, result paths, and seeds.
7. **Status vocabulary**: open → proposed → planned → analyzing → supported / confirmed / refuted / superseded. Conditions for confirmed: implementation claims need a validation test with a known answer; experimental claims need multiple seeds or conditions; literature-dependent claims stay supported unless we verify them independently.
8. **Decision sources**: design decisions record who decided; undiscussed defaults are labeled as such.

**Review checklist**:
- [ ] Hypothesis statuses match the experiment results (each confirmed is deserved; the limits of each supported are stated)
- [ ] Conclusions in hypotheses.md and comparison_catalog.md are no stronger than the experiment records
- [ ] No causal-line confusion
- [ ] Numbers in each comparison table use a consistent protocol
- [ ] Refuted ideas are kept, not rewritten (check with `git log -p`)
- [ ] Which undiscussed decisions affect current conclusions
- [ ] Every paper that is cited, compared against, or implemented from has been read in full

If the prove-it skill is installed, `scripts/log_status.py` produces a status summary to start from.
