# Workflow F: write papers and reports from the log

Read this when the user wants to write paper sections, research reports, or slides from the research log.

- **Tell each causal line separately**: the original research motivation goes in the introduction and methods; findings that appeared only after seeing results go under "further analysis" or "discussion", **not packaged as the original design**. The lines are defined in `research_log/README.md`.
- **Every number must be traceable**: each cited number maps to an experiment record and to a protocol and version in `methods.md`; numbers from different protocols don't go in the same table.
- **Claim strength matches status**: `supported` conclusions carry their limiting conditions; only `confirmed` ones may be stated affirmatively. A mechanistic explanation that depends on the literature is written as "consistent with the explanation in X", not "proves".
- **Read the full text before citing**: papers read only at the abstract level can't be cited; read the full text first, confirm that the cited content, numbers, and applicable conditions are right, then update `source:`.
- **Refuted hypotheses and excluded claims are material too**: they fit in ablations, limitations, or "approaches we also tried that did not work".
- **Undiscussed design decisions**: if one affects a conclusion, put it in the limitations, or confirm with the user before writing whether an extra experiment is needed.
