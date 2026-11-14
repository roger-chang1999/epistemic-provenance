# Rigor review: method and fallacy checklist

Read this when the user chooses "rigor review" at checkpoint one or two.

**Purpose**: give rigorous recommendations and catch fallacies before they enter the log and the paper. The value of a review lies in **specific questions**, not in reciting a checklist: "Are there any confounders?" is useless; "Were the learning rates of both A and B tuned, or only B's?" is useful.

## Method

1. **Pick the relevant items**: from the checklist below, pick the 3–6 highest-risk items for this node. Don't ask about every item; it dilutes the focus and tires the user.
2. **Ask specific questions**: phrase each item in terms of this node's actual content, pointing to specific numbers, settings, or sentences. Ask all at once or over two or three rounds; if an answer raises a new doubt, keep asking.
3. **Give a judgment**: after the user answers, give a conclusion for each item:
   | Item | Problem | Severity | Suggested fix |
   |---|---|---|---|
   Three severity levels:
   - **Fatal**: the conclusion may not hold at all; must be fixed before continuing
   - **Major**: the conclusion needs added conditions, or an extra experiment is needed
   - **Minor**: noting it in the limitations is enough
4. **Both directions**: the user can also ask the agent to defend its own design or interpretation; the agent must then honestly point out the weakest part of its own argument, not defend it reflexively.
5. **Record**: write the review results into the experiment record. A checkpoint-one review goes after the "Design decision log"; a checkpoint-two review goes in "Analysis discussion". For each fix adopted, state what was changed.

A review is not meant to reject; it is meant to make the conclusion stand firm. If you find no problems, say so plainly; don't manufacture problems to appear rigorous.

## Checklist

### Design stage (checkpoint one)

| Fallacy | Question to ask |
|---|---|
| **Confounders** | Besides the target variable, what else differs between the groups being compared? (randomness, data, steps, implementation, hardware) |
| **Unfair baseline** | The new method was tuned; was the baseline tuned with the same effort? Is the baseline a reasonable setting from the literature? |
| **Unfalsifiable prediction** | Is the prediction specific enough? Is there any possible result that would count as "does not hold"? |
| **Insufficient power** | How does the expected effect size compare with the seed-to-seed variance? Can the current number of repetitions distinguish the difference? |
| **Inconsistent protocol** | Do all groups use the same evaluation protocol and the same data version? |
| **Data leakage** | Did test or validation data take part in training, tuning, or model selection in any form? (including random splits of time series) |
| **Wrong operationalization** | Does this metric really measure what the hypothesis is about, or is it just a convenient proxy? |
| **Forking paths** | After the results come in, will there be many possible ways to analyze them? Should the main analysis be fixed in advance? |

### Analysis stage (checkpoint two)

| Fallacy | Question to ask |
|---|---|
| **HARKing** | Did this explanation exist before seeing the result, or was it thought up afterward? If afterward, mark it as a new hypothesis, not as a verification. |
| **Confirmation bias** | When the result "fits expectations perfectly", did anyone seriously look for counter-evidence? Were only the metrics that support the hypothesis reported? |
| **Noise as signal** | Is the difference larger than the seed-to-seed variance? Can a single-seed difference support a conclusion? |
| **Multiple comparisons** | After comparing many groups, was the best-looking one picked out to talk about? |
| **Gamed metric (Goodhart)** | The optimized metric improved; did the thing we actually care about also improve? (e.g. very low loss but a wrong solution) |
| **Overgeneralization** | It holds under one condition; is the conclusion written as holding in general? (e.g. "SGD is inherently unsuitable" when only two settings were tested) |
| **Correlation as causation** | Two things change together; has a third factor been ruled out? |
| **Mechanism conflated with conclusion** | The conclusion holding doesn't mean the proposed mechanism is right. Was the mechanism verified independently? |
| **Survivorship bias** | Were failed, diverged, or broken runs excluded from the statistics? |
| **Regression to the mean** | If the worst-performing setting was picked and then improved, could the improvement be a natural regression to the mean? |
| **Base-rate neglect** | How big is this improvement compared with typical differences between methods of this kind? |

### Literature and claims

| Fallacy | Question to ask |
|---|---|
| **Confused source strength** | Is the cited conclusion from reading the full text, only the abstract, or memory? |
| **Incomparable comparison** | When comparing our numbers with another paper's, are the settings really comparable? |
| **Causal-line confusion** | Is this claim the original research motivation or a later finding? When written into the paper, is it packaged as the original design? |
