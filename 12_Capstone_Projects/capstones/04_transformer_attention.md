# Capstone 4 — Transformer Attention Implementation

| | |
| :--- | :--- |
| **Difficulty** | ███████░░░ 7/10 |
| **Prerequisites** | Capstones 1–3, `01.10`, `02.10`, `03.03`, `05.03` |
| **Estimated time** | ~12–16 hours |
| **Demonstrates** | Attention derived rather than copied: the √dₖ variance argument, softmax as a differentiable soft-argmax, multi-head factorization, and a correct forward *and backward* pass |

---

## 1. Problem statement

Implement scaled dot-product attention and multi-head attention **from the
mathematics up**, deriving *why* each piece is shaped the way it is — especially
the $1/\sqrt{d_k}$ scaling — implement both the forward pass and (by hand) the
backward pass, and verify against PyTorch. Then use your attention layer inside a
minimal working sequence model. The question you are answering: *why is attention
$\mathrm{softmax}(QK^\top/\sqrt{d_k})V$ and not something simpler, and what is it
computing as a mathematical object?*

## 2. Prerequisites

| Notebook | Result you must already command |
| --- | --- |
| Capstone 2 | Manual backward passes; softmax-CE gradient |
| Capstone 3 | Comfort with matrix factorizations and projections |
| `01.10` | The attention formula and multi-head attention as introduced |
| `02.10` | The hand-derived attention backward pass |
| `03.03` | Variance of a sum of independent terms |
| `05.03` | Softmax; cross-entropy |

## 3. Mathematical formulation

For queries $Q\in\mathbb{R}^{n\times d_k}$, keys $K\in\mathbb{R}^{m\times d_k}$,
values $V\in\mathbb{R}^{m\times d_v}$:

$$
\mathrm{Attention}(Q,K,V) = \underbrace{\mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)}_{A\in\mathbb{R}^{n\times m}} V .
$$

- **Attention weights** $A$ are row-stochastic ($A\mathbf{1}=\mathbf{1}$, $A\ge0$):
  each output row is a **convex combination** of value rows. Attention is a
  *data-dependent* linear map (contrast Capstone 3's *fixed* linear PCA basis).
- **The $\sqrt{d_k}$ scaling.** If entries of $Q,K$ are independent with mean 0 and
  variance 1, then each score $q\cdot k=\sum_{i=1}^{d_k} q_i k_i$ has variance
  $d_k$. Dividing by $\sqrt{d_k}$ restores unit variance, keeping the softmax out
  of its saturated regime where gradients vanish.
- **Multi-head.** With $h$ heads, project into $h$ subspaces of dimension
  $d_k=d_{\text{model}}/h$, attend independently, concatenate, and project:
  $\mathrm{MHA}(X) = \mathrm{Concat}(\text{head}_1,\dots,\text{head}_h)W^O$.
- **Backward pass.** With upstream gradient $\partial\mathcal{L}/\partial \text{out}$,
  you need $\partial\mathcal{L}/\partial V = A^\top(\partial\mathcal{L}/\partial\text{out})$,
  the gradient back through the softmax (using its Jacobian
  $\mathrm{diag}(a)-aa^\top$ per row), and then through the $QK^\top/\sqrt{d_k}$
  bilinear form to $Q$ and $K$.

## 4. Derivation requirements

Derive each yourself:

1. **The variance calculation** giving $\operatorname{Var}(q\cdot k)=d_k$ under the
   stated assumptions, and hence *why* the scale is $\sqrt{d_k}$ and not $d_k$ or
   $1$. Show empirically (Experiments) that without it, softmax saturates.
2. **Row-stochasticity** of $A$ and the interpretation of each output as a convex
   combination of values; state what the attention weight $A_{ij}$ *means*.
3. **The softmax Jacobian** $\mathrm{diag}(a)-aa^\top$ (reuse Capstone 2) and the
   vector-Jacobian product that pushes a gradient back through one attention row.
4. **The full attention backward pass**: $\partial\mathcal{L}/\partial\{Q,K,V\}$,
   matching `02.10`. Show the shapes are consistent at every step.
5. **Multi-head equivalence.** Show that $h$ heads of dimension $d_{\text{model}}/h$
   have the same parameter count as one head of dimension $d_{\text{model}}$, and
   argue what multi-head buys that single-head does not (multiple subspaces /
   relation types).

## 5. Implementation

NumPy for the from-scratch core; PyTorch only as oracle:

- `scaled_dot_product_attention(Q, K, V, mask=None) -> (out, A)` — forward pass,
  numerically stable softmax (subtract row max), optional causal mask.
- `attention_backward(dout, cache) -> (dQ, dK, dV)` — your hand-derived backward
  pass.
- `MultiHeadAttention` — projections $W^Q,W^K,W^V,W^O$, head split/merge, forward
  and backward.
- A minimal `TransformerBlock` (attention + residual + LayerNorm + FFN) used in the
  Experiments' sequence task.

**Oracle rule.** No `torch.nn.MultiheadAttention` or
`torch.nn.functional.scaled_dot_product_attention` inside your implementation.
PyTorch appears only to (a) check your forward output and (b) check your
hand-derived gradients against `torch.autograd` on the identical computation.

## 6. Experiments

1. **Forward correctness.** Match your `scaled_dot_product_attention` output to a
   PyTorch reference on random inputs (and with a causal mask).
2. **Backward correctness.** Gradient-check `attention_backward` against central
   finite differences, *and* against `torch.autograd` on the same inputs.
3. **The scaling ablation.** Compare score variance and softmax entropy with vs.
   without the $1/\sqrt{d_k}$ factor, sweeping $d_k$. Show that unscaled scores
   saturate the softmax (near one-hot, tiny gradients) as $d_k$ grows — the exact
   failure the scaling prevents.
4. **What attention learns.** Train the `TransformerBlock` on a task that
   *requires* routing information across positions (e.g. copy / reverse / a
   "look back to position 0" task). Visualize the attention matrix $A$ and show it
   attends where the task demands.
5. **Multi-head vs single-head.** On a task with multiple relation types, show
   multi-head outperforms a single head of equal total width, and inspect what
   different heads attend to.

## 7. Expected outputs

- Forward output vs PyTorch: max abs difference $< 10^{-5}$ (with and without
  mask).
- Backward: gradient-check max relative error $< 10^{-4}$; autograd agreement
  $< 10^{-5}$.
- A scaling-ablation figure: softmax entropy collapsing toward 0 as $d_k$ grows
  *without* scaling, staying stable *with* it.
- A trained sequence model solving the routing task, with an attention-matrix
  heatmap that visibly matches the task structure.
- A multi-head vs single-head comparison with per-head attention visualizations.

## 8. Evaluation criteria

| Axis | Weight | "Meets expectations" bar |
| --- | --- | --- |
| Mathematical correctness | 30% | Variance/scaling argument, row-stochasticity, softmax Jacobian, and full backward pass all derived correctly with consistent shapes |
| Derivation independence | 20% | Backward matches both finite differences and autograd; no library attention used in the core |
| Implementation fidelity | 20% | Stable softmax, correct masking, correct head split/merge; forward matches PyTorch |
| Experimental rigor | 20% | Scaling ablation and routing task designed so the result actually tests the claim; seeded |
| Communication | 10% | Attention explained as a data-dependent convex combination, with the scaling motivated, not asserted |

Automatic fail if a library attention op is used inside the implementation, or if
the $\sqrt{d_k}$ scaling is used without the variance derivation.

## 9. Extensions

- **Positional information.** Add sinusoidal or rotary (RoPE) positional encodings
  and show the model can now use order (connect to `06.05`, `12.05`).
- **Efficient attention.** Implement a linear-attention or FlashAttention-style
  tiling variant and analyze the memory/time complexity change (connect to `06.07`,
  `12.04`).
- **KV cache.** Add incremental decoding with a key/value cache and derive the
  per-token compute/memory (connect to `12.04`).
- **Full transformer.** Stack blocks into a small language model and train it on
  character-level text.

## 10. Research directions

- **Why scaling matters at depth.** The interaction of the $\sqrt{d_k}$ scaling
  with LayerNorm placement (pre- vs post-norm) controls trainability of deep
  transformers (`06.07`).
- **Attention as kernel smoothing.** Softmax attention is a Nadaraya–Watson
  estimator with a particular kernel; this view connects it to `11.02` (RKHS) and
  to linear-attention approximations.
- **Induction heads and mechanistic interpretability.** Specific attention-head
  circuits implement in-context copying; analyzing $A$ is the entry point to
  mechanistic interpretability research.
- **Expressivity.** What functions a single attention layer can and cannot
  represent — an active theoretical question (`13`).
