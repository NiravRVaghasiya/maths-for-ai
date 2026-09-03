# Capstone 2 — Neural Network with Manual Backpropagation

| | |
| :--- | :--- |
| **Difficulty** | ████░░░░░░ 4/10 |
| **Prerequisites** | Capstone 1, `02.04`–`02.06`, `02.10`, `04.02`–`04.04`, `05.03` |
| **Estimated time** | ~8–12 hours |
| **Demonstrates** | The multivariate chain rule made mechanical: hand-derived per-layer gradients for a multilayer perceptron, verified by gradient checking, then used to train a real classifier |

---

## 1. Problem statement

Implement a multilayer perceptron (MLP) and its backward pass **entirely by
hand** — no autodiff engine — derive every gradient the backward pass uses, verify
those gradients against finite differences *and* PyTorch autograd, and train the
network to a competitive accuracy on a real classification task. The question you
are answering: *what exactly is `loss.backward()` computing, and why is it just
the chain rule applied to a composition of layers?*

## 2. Prerequisites

| Notebook | Result you must already command |
| --- | --- |
| Capstone 1 | Gradient descent on a convex objective; gradient checking |
| `02.04` | The chain rule on a computation graph; reverse-mode accumulation |
| `02.06` | Jacobians; the gradient of a scalar loss w.r.t. a matrix parameter |
| `02.10` | The hand-derived dense-layer backward formula $\partial L/\partial W = \delta\,x^\top$ |
| `04.02`–`04.04` | SGD and at least one adaptive optimizer |
| `05.03` | Cross-entropy loss and its combined gradient with softmax |

## 3. Mathematical formulation

Consider a two-hidden-layer MLP for $K$-class classification. For input
$x\in\mathbb{R}^{d}$:

$$
\begin{aligned}
z^{(1)} &= W^{(1)}x + b^{(1)}, & a^{(1)} &= \phi(z^{(1)}),\\
z^{(2)} &= W^{(2)}a^{(1)} + b^{(2)}, & a^{(2)} &= \phi(z^{(2)}),\\
z^{(3)} &= W^{(3)}a^{(2)} + b^{(3)}, & \hat{p} &= \mathrm{softmax}(z^{(3)}),
\end{aligned}
$$

with elementwise nonlinearity $\phi$ (use ReLU) and the cross-entropy loss
against a one-hot target $y$:

$$
\mathcal{L} = -\sum_{k=1}^{K} y_k \log \hat{p}_k .
$$

The two identities that make the backward pass work:

- **Softmax + cross-entropy gradient collapses:**
  $\dfrac{\partial \mathcal{L}}{\partial z^{(3)}} = \hat{p} - y.$ (This is why the
  output layer's error signal is so simple.)
- **Dense-layer backward:** given the incoming gradient
  $\delta^{(\ell)} = \partial\mathcal{L}/\partial z^{(\ell)}$,
  $$
  \frac{\partial\mathcal{L}}{\partial W^{(\ell)}} = \delta^{(\ell)} (a^{(\ell-1)})^\top,\quad
  \frac{\partial\mathcal{L}}{\partial b^{(\ell)}} = \delta^{(\ell)},\quad
  \delta^{(\ell-1)} = \big(W^{(\ell)\top}\delta^{(\ell)}\big)\odot \phi'(z^{(\ell-1)}).
  $$

## 4. Derivation requirements

Derive each yourself, for the batched (mini-batch of size $B$) case:

1. **The softmax Jacobian** $\partial \hat{p}/\partial z = \mathrm{diag}(\hat{p}) -
   \hat{p}\hat{p}^\top$, and then the **collapse** to $\hat{p}-y$ when composed
   with cross-entropy against a one-hot target. Show the cancellation explicitly.
2. **The dense-layer weight gradient** $\partial\mathcal{L}/\partial W = \delta
   a^\top$ from the chain rule (connect to `02.10`), including the batch sum
   $\partial\mathcal{L}/\partial W = \sum_{b}\delta_b a_b^\top$ and why the bias
   gradient is the sum of $\delta$ over the batch.
3. **The ReLU local gradient** $\phi'(z) = \mathbf{1}[z>0]$ and how it gates the
   backward signal (why "dead" units pass zero gradient).
4. **The full recurrence** $\delta^{(\ell-1)} = (W^{(\ell)\top}\delta^{(\ell)})
   \odot\phi'(z^{(\ell-1)})$, and a statement of *why* reverse order (output → input)
   is the efficient evaluation order (reuse of $\delta$, connect to `02.04`).

## 5. Implementation

Build a small framework, NumPy only for the core:

- A `Layer` interface with `forward(x)` (caching what backward needs) and
  `backward(grad)` (returning the upstream gradient and storing parameter
  gradients).
- `Linear`, `ReLU`, and `SoftmaxCrossEntropy` layers.
- An `MLP` that composes layers and exposes `forward`, `backward`, and a
  `parameters()` view for the optimizer.
- An optimizer (`SGD` with momentum, or reuse your Capstone-style Adam) that steps
  on the stored gradients.
- A `gradient_check(model, x, y)` utility comparing every parameter gradient to a
  central finite difference.

**Oracle rule.** No `torch.autograd`, no `torch.nn` layers, and no
`autograd`-style engine inside your MLP — the whole point is that *you* compute
the gradients. PyTorch appears only in Experiments, rebuilding the *same* network
with `torch.nn` to check your gradients and training curve against it.

## 6. Experiments

1. **Gradient check** on every parameter tensor at initialization and after a few
   steps: max relative error vs. central differences.
2. **Autograd agreement.** Rebuild the identical architecture in PyTorch, copy
   your initial weights in, and confirm your gradients match `torch`'s on the same
   batch to within finite-precision tolerance.
3. **Train a real classifier.** On a real dataset (MNIST, or `sklearn`'s digits
   for a CPU-only run), train to a target accuracy. Plot train/val loss and
   accuracy curves.
4. **Ablations that must behave as the math predicts:** remove the nonlinearity
   (network collapses to linear — accuracy drops to a linear model's); scale the
   initialization up/down and observe the vanishing/exploding gradient regimes
   (connect to `02.10`, `08.04`).
5. **Optimizer comparison.** SGD vs. momentum vs. Adam on the same network; relate
   convergence speed to what each optimizer does to the update.

## 7. Expected outputs

- Gradient-check: max relative error $< 10^{-5}$ for every parameter tensor.
- Autograd agreement: your gradients vs. PyTorch's, max abs difference
  $< 10^{-5}$.
- A trained model reaching a stated target (e.g. $\geq 97\%$ test accuracy on
  MNIST, or $\geq 95\%$ on digits) with train/val curves.
- An ablation table: linear-only accuracy $\approx$ logistic-regression baseline;
  init-scale sweep showing gradient-norm blow-up/decay.
- Optimizer-comparison plot with Adam/momentum converging in fewer epochs than
  plain SGD.

## 8. Evaluation criteria

| Axis | Weight | "Meets expectations" bar |
| --- | --- | --- |
| Mathematical correctness | 30% | Softmax-CE collapse, dense-layer gradients, ReLU gating, and the full recurrence derived correctly for the batched case |
| Derivation independence | 25% | Gradient check *and* autograd agreement pass; no autodiff used in the core |
| Implementation fidelity | 20% | Modular layer API; forward caches exactly what backward needs; trains to target |
| Experimental rigor | 15% | Ablations seeded and interpreted; results match mathematical predictions |
| Communication | 10% | Backward pass explained as chain rule, not as a recipe |

Automatic fail if any autodiff computes the graded gradients, or if the softmax-CE
collapse is asserted without the cancellation shown.

## 9. Extensions

- **New layer types.** Add BatchNorm or Dropout and derive their backward passes
  (BatchNorm's is a genuinely instructive derivation).
- **A tiny autodiff engine.** Generalize your hand-derived layers into a reverse-
  mode engine that backprops through *arbitrary* compositions (this is exactly
  what `12.02` does — use it to check yourself).
- **Second-order info.** Compute the diagonal of the Hessian (or a Hessian-vector
  product) and use it for a diagonal-Newton step; compare to Adam.
- **Weight tying / convolution.** Derive the backward pass for a shared-weight
  (convolutional) layer and explain the gradient accumulation over positions.

## 10. Research directions

- **Initialization theory.** Why Xavier/He scaling keeps signal and gradient
  variance stable across depth (`08.04` random matrix theory); reproduce the
  variance-preservation calculation.
- **The neural tangent kernel.** In the infinite-width limit the network's
  training dynamics become linear in its parameters (`11.03`, `11.04`) — a bridge
  from your finite MLP to a closed-form theory.
- **Flat vs. sharp minima.** The Hessian spectrum at the solution correlates with
  generalization; measure it and connect to `04.09`, `13`.
