# Literature search: method and recording

Read this when the user chooses "literature search" at checkpoint one or two.

**Purpose**: find citations that support, challenge, or explain the results, targeted at this node's specific question. Aimless searching wastes time and tokens, so every search starts from a clear question.

## Method

1. **Propose search questions first and wait for the user's agreement.** List 1–3 specific questions, the reason for each, and what you expect to find. For example:
   - Checkpoint one: "What hyperparameters does the literature typically use for this optimizer on this class of problem?" This avoids picking a default casually.
   - Checkpoint two: "Has anyone observed L-BFGS making the error worse in inverse problems?" This checks whether the observed phenomenon is already known.
   - Checkpoint two: "Is there an existing theoretical explanation for this mechanism?"
2. **Search**: use the search tools the environment provides. Start with a normal search; if results are thin, outdated, or off-topic, use a deeper search or read the paper pages directly. Prefer peer-reviewed papers; label preprints, blogs, and auto-generated summaries as such.
3. **Report**: give a conclusion for each question. If no relevant literature turns up, say so; that is useful information too (it may be a research gap, or just a poor search).
4. **Record**: write each useful paper as `papers/<slug>.md` (template `assets/templates/paper.md`) and link it back to the idea or experiment that triggered the search.

## When recording, pay attention to

- **Be honest in `source:`**: read full text, abstract only, search-result snippet, auto-generated secondary summary, or from memory. If you only saw a search snippet, don't write it up as having read the paper.
- **Numbers come with conditions**: state the setting under which each reported number was obtained.
- **What is not comparable**: how the setting, data, and metrics differ from ours.
- **To-do**: if the full text hasn't been read, list "read the full text to confirm X".
- When replying to the user, list the source links used.
