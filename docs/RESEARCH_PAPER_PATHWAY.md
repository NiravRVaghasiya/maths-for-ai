# How to Read Research Paper Mathematics — Pathway Guide

> Full document: `workspace/artifacts/Research_Paper_Math_Pathway.md`

A ten-skill pathway teaching learners to engage with ML research paper equations, demonstrated
on representative topics from optimization, representation learning, transformers, generative
models, and efficient fine-tuning.

## The Ten Skills

1. **Identify Prerequisites** — Adam optimizer → list 5+ math concepts before reading
2. **Read Notation** — Attention equation → build a symbol table with shapes/types
3. **Expand Equations** — VAE ELBO → reconstruct the 5-step Jensen's inequality derivation
4. **Check Dimensions** — Attention → verify every tensor shape through the pipeline
5. **Re-Derive Key Results** — $\sqrt{d_k}$ scaling → variance calculation from first principles
6. **Translate to Code** — DDPM forward process → equation-to-NumPy translation protocol
7. **Reproduce Experiments** — Double descent → minimal reproduction of the key curve
8. **Identify Assumptions** — SGD convergence → 5 standard assumptions, which hold in practice
9. **Find Limitations** — LoRA → rank ceiling, initialization asymmetry, scale sensitivity
10. **Extend a Method** — Chinchilla → re-derive under a memory constraint instead of compute

## Scoring

- Skills 1–3: you've *read* the paper
- Skills 4–6: you *understand* the paper
- Skills 7–9: you could *implement and critique* the paper
- All 10: you could *build on* the paper — you're doing research
