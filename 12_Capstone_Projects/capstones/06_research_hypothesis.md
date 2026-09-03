# Capstone 6 — Experimental Research Hypothesis

| | |
| :--- | :--- |
| **Difficulty** | ██████████ 10/10 |
| **Prerequisites** | Capstones 1–5, `03.05`–`03.09`, `09` (concentration/statistics), `13` (learning theory) |
| **Estimated time** | ~24–40 hours (open-ended) |
| **Demonstrates** | Research itself: formulating a falsifiable hypothesis, designing controlled experiments, analyzing results with statistical rigor, and defending — or honestly retracting — a conclusion |

---

## 1. Problem statement

Formulate your own **falsifiable hypothesis** about the mathematics or behavior of
an AI system, design controlled experiments to test it, analyze the results with
proper statistical rigor, and write it up as a mini research report that reaches
an honest conclusion — *including if that conclusion is "my hypothesis was
wrong."* The question you are answering: *can you do the thing researchers
actually do — turn a hunch into a testable claim and let the evidence decide?*

This is the terminal capstone. There is no answer key, and there cannot be: a real
research question has an unknown answer. You are graded on the *quality of the
science*, not on whether the hypothesis turns out to be true.

## 2. Prerequisites

| Notebook | Result you must already command |
| --- | --- |
| Capstones 1–5 | The full toolkit: you can build, verify, and reproduce |
| `03.05`–`03.09` | Bayesian and frequentist inference; estimators; hypothesis testing |
| `09.04` | Concentration inequalities — how many samples make a difference "real" |
| `13` | Generalization, bias–variance, learning-theoretic framing |

## 3. Mathematical formulation

As in Capstone 5, this section is a **contract you fill in**. Your submission must
state:

- **The hypothesis $H_1$ and null $H_0$**, as precise, falsifiable statements
  about a measurable quantity. "Adam generalizes worse than SGD" is a hunch;
  "on dataset D and architecture A, SGD's final test accuracy exceeds Adam's by
  ≥ δ across the tuned learning-rate range" is a hypothesis.
- **The estimand** — the population quantity you are really asking about — and the
  **estimator** you will use for it, with its bias/variance understood.
- **The decision rule** — what result would make you accept $H_1$, what would make
  you reject it, and the significance/effect-size threshold, *chosen before
  running experiments*.

### Example hypotheses (formulate your own, or sharpen one of these)

| Rough idea | Sharpened into a testable claim |
| --- | --- |
| Wider networks need less depth | "At fixed parameter budget, test error is non-increasing in width up to width $w^\*$, holding depth×width constant" |
| Attention scaling matters | "Removing $1/\sqrt{d_k}$ raises training loss at 10k steps by ≥ δ, and the gap grows with $d_k$" (build on Capstone 4) |
| Batch size and the optimal LR | "The LR that minimizes 1-epoch loss scales linearly with batch size over range B" (the linear-scaling rule) |
| Label noise and memorization | "Test accuracy degrades linearly with label-noise fraction $p$ until $p^\*$, then collapses" |
| Effective dimensionality grows during training | "The participation ratio of penultimate-layer activations increases monotonically over training" (build on Capstone 3) |
| Double descent | "Test error is non-monotone in model size, peaking near the interpolation threshold $d\approx n$" (`13.08`) |

A strong hypothesis is **specific, measurable, falsifiable, and cheap enough to
test honestly** on your compute budget.

## 4. Derivation requirements

- **Derive the estimator's properties.** For whatever you measure (a mean
  accuracy, a slope, a ratio), state its sampling distribution or a concentration
  bound (`09.04`): how many seeds/samples are needed for a difference of size $\delta$
  to be distinguishable from noise. This is what separates a result from an
  anecdote.
- **Derive the prediction $H_1$ makes** from whatever theory motivates it. Even a
  heuristic derivation (a scaling argument, a bias–variance decomposition) turns
  "I guess X" into "theory T predicts X because …," which is what you then test.
- **Pre-register the analysis.** Write down the decision rule and the number of
  runs *before* looking at results, to avoid fooling yourself (see Research
  Directions on the garden of forking paths).

## 5. Implementation

- Build the experimental harness on top of your Capstone 1–4 code (that is what
  those capstones were *for*). Keep every non-varied factor fixed and logged.
- Instrument it to record raw per-run results (not just aggregates), seeded, so
  the analysis is reproducible and the uncertainty is real.

**Oracle rule.** Correctness of the components you built earlier is assumed
(they passed their own capstones); here the "oracle" is **statistical**: a result
is real only if it survives a proper test against the null, not because a single
run looked good.

## 6. Experiments

1. **A minimal, controlled design.** Vary the *one* factor your hypothesis is
   about; hold everything else fixed. Include the right baseline/control.
2. **Adequate replication.** Enough seeds (justified by your Section-4 sample-size
   argument) to estimate the effect *and its uncertainty*.
3. **A pre-specified analysis.** Apply the decision rule you pre-registered:
   effect size with a confidence interval, and/or an appropriate test against
   $H_0$.
4. **Robustness / falsification attempts.** Actively try to *break* your own
   result: a different dataset, a different seed range, a confound you can rule
   out. A hypothesis that survives a genuine attempt to falsify it is worth far
   more than one that was never challenged.

## 7. Expected outputs

- A one-paragraph **pre-registration** (hypothesis, estimand, decision rule,
  planned runs) dated before the results.
- A **results figure/table** with effect sizes and uncertainty (CIs or error
  bars over seeds), *not* single-run numbers.
- The **pre-specified test** applied, with the verdict: supported / not supported /
  inconclusive — all acceptable if honestly reached.
- A **threats-to-validity** paragraph: confounds, the compute-budget limits, and
  what a larger-scale test would need.
- A short **abstract** (≤ 150 words) stating the question, method, result, and
  honest conclusion, as a real paper would.

## 8. Evaluation criteria

This capstone is graded almost entirely on scientific quality, not on outcome:

| Axis | Weight | "Meets expectations" bar |
| --- | --- | --- |
| Mathematical correctness | 15% | Estimator properties / sample-size argument derived correctly; the $H_1$ prediction is motivated, not guessed |
| Derivation independence | 10% | The theoretical prediction is your own reasoning |
| Implementation fidelity | 15% | Harness controls all non-varied factors; raw results logged and reproducible |
| Experimental rigor | 45% | Pre-registered decision rule; adequate seeds with uncertainty; genuine falsification attempt; honest verdict |
| Communication | 15% | Abstract + report read like real science; every claim tied to evidence; limitations stated plainly |

A rigorous experiment that **refutes** your own hypothesis, honestly reported, is
a top-scoring submission. A "confirmed" result with p-hacking, a single seed, or an
uncontrolled confound is not.

## 9. Extensions

- **Turn it into a short paper.** Write it up in a workshop-paper format
  (abstract, method, experiments, related work, limitations) and cite the
  literature your hypothesis touches.
- **Adversarial collaboration.** Pair with someone who expects the opposite
  result; agree on the experiment in advance and let it decide.
- **Scale study.** If a trend holds at small scale, design (even if you can't run)
  the experiment that would test it at the next order of magnitude, and predict
  the outcome.
- **Theory follow-up.** If the effect is real, attempt a derivation that explains
  *why* — the move from empirical observation to theorem.

## 10. Research directions

- **The garden of forking paths.** Analysis decisions made after seeing data
  inflate false positives; pre-registration is the standard defense. This capstone
  is a deliberate exercise in it.
- **Effect size vs. significance.** A "significant" result can be trivially small;
  reporting and interpreting effect sizes is where honest ML empiricism is heading.
- **Benchmarks and construct validity.** Whether your measured quantity actually
  captures the phenomenon you care about is a deep, unsolved question across ML
  evaluation.
- **From capstone to contribution.** A clean, honest negative result on a question
  people assume they know the answer to is a genuine, publishable contribution —
  this capstone is designed to be the on-ramp to real research.
