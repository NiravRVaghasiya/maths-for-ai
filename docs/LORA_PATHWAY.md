# The Mathematical Anatomy of LoRA — Pathway Guide

> Full document: `workspace/artifacts/LoRA_Math_Pathway.md`

A rigorous guided pathway deriving every mathematical component of Low-Rank Adaptation (LoRA)
from the curriculum's existing notebooks.

## Sections

1. **The Central Equation** — $W' = W_0 + BA$ with full symbol/shape table
2. **Matrix Rank** — `01.02`, `01.07` → rank constraint on $\Delta W$
3. **Why Low-Rank Works** — `08.05` → Aghajanyan's intrinsic dimensionality, Eckart-Young bound
4. **Parameter Count** — `12.04` → compression ratio $d/(2r)$, GPT-2 worked example
5. **Initialization** — `08.04` → $B=0$ prevents damage, asymmetric gradient flow
6. **Gradient Flow** — `02.04`, `08.02` → chain rule through factorization, cost comparison
7. **Minimal Implementation** — full `LoRALinear` class with gradient-checked backward pass
8. **Full FT vs. LoRA** — controlled experiment: memory, params, MSE, convergence
9. **Computational Implications** — memory, FLOPs, inference merging (zero overhead)
10. **Limitations** — rank ceiling, layer selection, $r$ choice, training dynamics

## Curriculum thread

`01.02` → `01.07` → `08.01` → `08.02` → `08.04` → `08.05` → `08.06` → `04.03` → `06.08`
