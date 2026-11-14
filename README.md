# prove-it

> **Every claim must be provable: where it came from, why it holds, how it changed.**

A research log system and human-in-the-loop research workflow for AI agents and the people who work with them. It follows the open [Agent Skills](https://agentskills.io/specification) format, so it works with Claude Code, Codex, Cursor, GitHub Copilot, Antigravity / Gemini CLI, and other agents that support `SKILL.md`. The `research_log/` it produces is plain markdown: people and agents without the skill can read and review it directly.

The agent collaborates and writes the log in the user's language (see [Language](#language)).

*(Formerly `epistemic-provenance`; renamed in v0.7.0.)*

## Why

> "The first principle is that you must not fool yourself — and you are the easiest person to fool." — Richard Feynman

Researchers fool themselves easily, and agents do too: an agent can state a guess as a fact, report an experiment it never ran, or pass a half-checked conclusion on to the next agent. prove-it guards against the common ways this happens in research:

- **Source confusion**: recording an explanation thought up after seeing the results as the original design
- **Hindsight bias**: rewriting the original reasoning once the result is known
- **Protocol mixing**: putting same-named numbers measured by different methods in one comparison table

The name *epistemic provenance* comes from art history: provenance is the complete record of a work's ownership, every hand it passed through, kept tamper-proof. Here the objects being traced are knowledge claims.

## Workflow: two human checkpoints per node

Research advances in nodes (one hypothesis plus the experiments that test it). At two checkpoints the agent stops and discusses with the user:

```
① Propose a hypothesis → ② Checkpoint one: design discussion → ③ Run → ④ Checkpoint two: analysis discussion (several rounds) → ⑤ Record once the conclusion is confirmed, then open the next node
```

- **Checkpoint one**: the agent proposes a design table (variables, controls, protocol, prediction, cost, what the user needs to decide); it runs only after the user confirms.
- **Checkpoint two** is a multi-round discussion, not a report. The agent gives an initial report (result vs prediction, anomalies, alternative explanations, limitations) and stops; each later round settles one or two issues, with anomalies and extra diagnostics kept in the same node; only after the user confirms the conclusion does it propose options for the next node.
- Both checkpoints list two **optional reviews**, done only if the user asks: a **rigor review** (checks for research fallacies item by item with specific questions) and a **literature search** (finds citations for specific questions).
- Every design decision records **who made it**; undiscussed defaults are labeled as such.

## The log

The skill maintains a `research_log/` in your project:

```
research_log/
├── README.md                  How to use the log, log language, causal line definitions
├── hypotheses.md              Hub index: every hypothesis and its status
├── methods.md                 Evaluation protocol registry
├── research_tree_overview.md  Research tree: hypothesis → design → result → inference ⟹ next hypothesis
├── comparison_catalog.md      Catalog of A vs B comparisons
├── ideas/NNN-slug.md          Idea evolution (append only, never rewritten)
├── papers/slug.md             Paper notes (incl. what is not comparable, information source)
└── experiments/exp-slug.md    Experiment records (incl. full commands, limitations)
```

## Language

The agent collaborates with you, and writes the log, in one consistent language, chosen in this order:

1. Your explicit preference (agent memory, `AGENTS.md`, `CLAUDE.md`, or just telling it)
2. The "Log language" recorded in `research_log/README.md` when the log was initialized
3. The language you are writing in

Because the language is recorded in the log, later sessions and other agents keep using it. Templates are in English and get translated as they are filled in; status words, frontmatter keys, and `H#` IDs stay in English so the scripts can parse them. The scripts recognize logs written in English or Chinese.

## Real example

The `research_log/` of [sediment-pinn-2d](https://github.com/roger-chang1999/sediment-pinn-2d) was maintained with this skill from the start: a physics-informed neural network (PINN) study with 20 hypotheses, several rounds of ablations, who made each design decision, and the full "find a problem → diagnose → revise the conclusion" process. The log is in Chinese. With the skill installed, ask an agent in that project "where is the research now?" to see it in action.

## Install

The skill itself is the `skills/prove-it/` folder. Put it where your agent looks for skills.

### Universal: `.agents/skills/` (Codex, Cursor, GitHub Copilot, Antigravity / Gemini CLI)

```bash
git clone https://github.com/roger-chang1999/prove-it.git

# For all your projects (personal)
mkdir -p ~/.agents/skills && cp -r prove-it/skills/prove-it ~/.agents/skills/

# Or for one project only (shared with your team through the repo)
mkdir -p <your-project>/.agents/skills && cp -r prove-it/skills/prove-it <your-project>/.agents/skills/
```

To keep it updated, use a symlink (on Windows, `mklink /J`) to the cloned folder instead, then `git pull`.

| Agent | Other directories it reads | How to invoke |
|---|---|---|
| Codex (CLI, IDE extension) | `~/.agents/skills`, `.agents/skills` at each level of the project | Automatic by description; or `/skills`, `$prove-it` |
| Cursor | `~/.cursor/skills`, `.cursor/skills`; also `.claude/skills`, `.codex/skills` | Automatic; or type `/prove-it` |
| GitHub Copilot | `~/.copilot/skills`, `.github/skills`, `.claude/skills` | Loaded automatically when relevant (support varies by surface and version) |
| Antigravity / Gemini CLI | `~/.gemini/skills`, `.gemini/skills` | Automatic (asks you to confirm activation); `gemini skills install <git url>` also works |

Directory locations are taken from each tool's official docs (November 2026) and may change; the official docs take precedence.

### Claude Code

```bash
claude plugin marketplace add roger-chang1999/prove-it
claude plugin install prove-it@prove-it
```

Or type `/plugin marketplace add roger-chang1999/prove-it` in a Claude Code conversation, then install from the `/plugin` panel.

Update: `claude plugin marketplace update prove-it`

### claude.ai

```bash
python tools/package_for_claudeai.py
```

This creates `dist/prove-it.zip`. Upload it under Settings → Capabilities → Skills on claude.ai.

## Usage

After installing, just talk to your agent, for example:

- "Set up a research log for this project"
- "Record the results of the experiment we just ran"
- "Open a new idea for what we just discussed"
- "Take notes on this paper"
- "Where is the research now?"
- "I want to test X; let's discuss the experiment design"
- "The experiment finished; help me analyze the results"
- "Review the research log"

Explicit invocation: in Claude Code, `/prove-it:prove-it` (plugin install) or `/prove-it`; for other tools, see the install table above.

## Contents

```
.claude-plugin/
  plugin.json, marketplace.json
skills/prove-it/
  SKILL.md                         Core principles and workflows
  references/rigor-review.md       Rigor review: method and research fallacy checklist
  references/workflow-*.md         Initialize, progress report and history review, review the log, write papers (read only when needed)
  references/literature-search.md  Literature search: method and recording
  assets/templates/                Blank templates for each kind of file
  scripts/init_research_log.py     Create the skeleton (never overwrites existing files)
  scripts/check_links.py           Check relative links, frontmatter, idea numbering
  scripts/log_status.py            Status summary: hypotheses by status, nodes awaiting confirmation, status inconsistencies, single seeds, undiscussed decisions, weakly sourced papers
tools/package_for_claudeai.py      Package as a zip for claude.ai
```

## License

[MIT](LICENSE)
