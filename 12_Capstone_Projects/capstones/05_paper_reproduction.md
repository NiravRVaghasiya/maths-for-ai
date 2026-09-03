# Capstone 5 — Research-Paper Mathematical Reproduction

| | |
| :--- | :--- |
| **Difficulty** | ████████░░ 8/10 |
| **Prerequisites** | Capstones 1–4, plus whatever the chosen paper requires |
| **Estimated time** | ~16–24 hours |
| **Demonstrates** | Reading mathematics you did not write: decoding a paper's notation, deriving its key equations, and reproducing one of its quantitative claims from those equations |

---

## 1. Problem statement

Choose a research paper with a self-contained mathematical result, **decode its
notation, derive its central equation(s) yourself, implement the method, and
reproduce one specific quantitative claim** (a figure trend, a table number, an
ablation direction). The question you are answering: *can you take a claim stated
in a paper's own notation and independently re-derive and re-verify it, rather
than trusting it?*

This is the bridge from "I can build a thing I was told to build" to "I can
reconstruct a result from the literature." The deliverable is a reproduction
report, not a re-implementation of the authors' entire codebase.

## 2. Prerequisites

| Notebook | Result you must already command |
| --- | --- |
| Capstones 1–4 | The full from-scratch toolkit: gradients, spectral methods, attention |
| `12.05` | The worked example of reading "Attention Is All You Need" mathematically — use it as the template for *how* to decode a paper |
| Paper-specific | Whatever mathematics the chosen paper rests on (identify this up front) |

## 3. Mathematical formulation

Because the content depends on your chosen paper, this section is a *contract you
fill in*, not fixed math. Your submission's formulation section must contain:

- The paper's **central mathematical object and claim**, restated in the
  curriculum's notation (not copied verbatim), with every symbol defined.
- A **notation dictionary** mapping the paper's symbols to standard ones, flagging
  any abuse of notation or implicit assumptions you had to uncover.
- The **specific claim you will reproduce**, stated as a checkable proposition
  ("Figure 3's loss curve for method X lies below baseline Y by ≥ Z"; "the
  estimator in Eq. 7 is unbiased"; "Table 2's ablation removing component C costs
  ≥ D accuracy").

### Suggested papers (pick one, or propose your own)

Choose one whose core result is provable/reproducible on a CPU or a single small
GPU. A good target has a *derivable* central equation and a *small* reproducible
experiment.

| Paper | Reproducible mathematical core | Curriculum tie-in |
| --- | --- | --- |
| Dropout (Srivastava et al., 2014) | Dropout as an approximate ensemble / its expected-value scaling | `03`, `05` |
| Batch Normalization (Ioffe & Szegedy, 2015) | The normalization transform and its backward pass; effect on the loss-landscape conditioning | Capstone 2, `04` |
| Adam (Kingma & Ba, 2015) | The bias-correction derivation and a convergence claim on a convex problem | `04.04`, `12.03` |
| Layer Normalization (Ba et al., 2016) | The transform and gradient; contrast with BatchNorm | Capstone 2/4 |
| Variational Autoencoder (Kingma & Welling, 2014) | The ELBO derivation and reparameterization gradient | `09.05` |
| LoRA (Hu et al., 2021) | The low-rank update math and its parameter-count claim | `08.06`, Capstone 3 |
| Grokking (Power et al., 2022) | Reproduce delayed generalization on modular arithmetic | `13` |

**Propose-your-own is encouraged**, subject to: (a) a derivable central result,
(b) a claim reproducible with your compute budget, (c) not a paper already fully
worked in the curriculum.

## 4. Derivation requirements

- **Derive the paper's central equation(s) yourself.** Reconstruct the key
  derivation (e.g. the ELBO, the bias-correction, the BatchNorm backward pass)
  from stated assumptions, filling every gap the paper leaves to the reader. This
  is the graded core — a re-typed copy of the paper's algebra does not count.
- **Identify and justify one hidden assumption.** Papers routinely omit a
  regularity condition, an independence assumption, or a limit. Name one, and show
  where the result would break without it.
- **State the claim as a falsifiable prediction** before you run anything, so the
  reproduction can succeed or fail honestly.

## 5. Implementation

- Implement the method from your own derivation, reusing your Capstone 1–4 code
  where the paper's method overlaps (e.g. your MLP + backprop for a BatchNorm
  study, your attention for an attention-variant paper).
- Keep the reproduction **minimal**: the smallest model/dataset that can exhibit
  the claimed effect. Reproducing a *trend* on a small setup is worth more than
  failing to reproduce a full-scale run.

**Oracle rule.** You may use trusted libraries for *infrastructure* (data loading,
a reference optimizer) but the component whose claim you are reproducing must be
your own implementation, checked for correctness against an oracle before you
trust any experimental result built on it.

## 6. Experiments

1. **Correctness first.** Before reproducing the claim, verify your implementation
   of the paper's method against an oracle (gradient check, a known special case,
   or a library reference on a component).
2. **The reproduction.** Run the minimal experiment that tests your stated claim,
   with a proper baseline (the "without the paper's idea" control).
3. **Seeds and uncertainty.** Repeat over several seeds; report the effect with a
   spread (std or CI), not a single lucky run.
4. **A sensitivity check.** Vary one hyperparameter the paper fixed and report
   whether the claimed effect is robust or fragile.

## 7. Expected outputs

- A **notation dictionary** and a self-contained restatement of the central
  result.
- A **derivation** of the central equation(s), in your own steps.
- A **correctness check** of your implementation against an oracle (with the
  numbers).
- A **reproduction figure or table** with your result next to the paper's claim,
  over multiple seeds with uncertainty, and an explicit verdict:
  reproduced / partially reproduced / not reproduced — *all three are acceptable
  outcomes if honestly analyzed.*
- A short **discrepancy analysis** if your numbers differ from the paper's
  (scale, hyperparameters, implicit tricks).

## 8. Evaluation criteria

Weighting shifts toward experimental judgment here:

| Axis | Weight | "Meets expectations" bar |
| --- | --- | --- |
| Mathematical correctness | 25% | The central equation is correctly re-derived; the hidden assumption is real and correctly explained |
| Derivation independence | 20% | The derivation is yours; the reproduced component is your own implementation, oracle-checked |
| Implementation fidelity | 15% | The method matches the paper's math; correctness verified before claims |
| Experimental rigor | 30% | Controlled baseline, multiple seeds with uncertainty, honest verdict incl. discrepancy analysis |
| Communication | 10% | A reader can follow paper-claim → derivation → your evidence → verdict |

An honest "not reproduced" with a correct derivation and a rigorous experiment
**passes**. A "reproduced" built on an unchecked implementation or a single seed
does not.

## 9. Extensions

- **Reproduce a second claim** from the same paper and check internal consistency.
- **Stress the claim** past the paper's regime (larger $d_k$, more layers, harder
  data) and report where it breaks.
- **Compare two papers** that make competing claims about the same phenomenon and
  design an experiment that discriminates them.
- **Write the missing appendix.** Fully formalize a step the paper hand-waved.

## 10. Research directions

- **The reproducibility crisis.** Many published deep-learning results are
  sensitive to seeds, hyperparameters, and undocumented tricks; your discrepancy
  analysis is a microcosm of a real methodological problem.
- **From reproduction to extension.** A claim you can reproduce *and* stress-test
  is one you can extend — this capstone is the natural runway into Capstone 6.
- **Mathematical vs. empirical claims.** Note which parts of the paper are
  *proved* and which are *observed*; the gap between them is where most open
  research questions live.
