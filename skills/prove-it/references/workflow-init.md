# Workflow A: initialize a research log for a new project

Read this when the user wants to set up a research log for a project.

1. Ask the user, or gather from the conversation and the proposal: the project name, the **log language** (see "Language" in `SKILL.md`), the current causal lines (at least one "original research motivation"), and the main evaluation metrics.
2. Run:
   ```bash
   python <skill directory>/scripts/init_research_log.py <project root> --project "<project name>"
   ```
   This creates the directories and skeletons for all hub files (including "Guidance for reviewers"); existing files are never overwritten. The templates are in English; when the log language is different, translate the headings and fixed phrases as you fill them in.
3. Fill in:
   - `README.md`: the log language and the causal line definitions
   - `methods.md`: the first evaluation protocol
   - `hypotheses.md`: the initial hypotheses
   - `ideas/001-origin.md`: the original research motivation. If there is a proposal, extract from it the research questions, the hypotheses to test, and **the conclusions that should not be claimed in advance**.
4. If the project already has a history of discussions or experiments, write it up as ideas and experiments in chronological order, **clearly marked as written after the fact**, and mark in the design decision logs which decisions were not discussed at the time.
5. Run `scripts/check_links.py`.
