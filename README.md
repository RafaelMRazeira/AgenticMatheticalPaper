# Probabilistic Scaling Laws for Agent Systems

From Multiplication Laws to Unified Reliability Polynomials

## Overview

This project develops a rigorous probabilistic framework for the scaling behavior of multi-agent systems. Each agent is modeled as a Bernoulli random variable, and composition laws are derived that govern system-level performance across five regimes:

1. **Independent Sequential Pipelines** — System reliability decays exponentially with a universal throughput constant P_sys(n*) = e⁻¹.
2. **Dependent Pipelines** — Analyzed as absorbing Markov chains with coordination gain determined by the geometric mean of coordination multipliers.
3. **Parallel Ensembles** — Diminishing returns governed by the Condorcet jury theorem.
4. **Hybrid Series-Parallel Topologies** — Optimized via a marginal equalization principle with a unique efficiency maximum.
5. **Capability Saturation** — Architecture-specific thresholds and a phase diagram in capability–cost space.

All five regimes are unified as special cases of a **reliability polynomial** on the task DAG.

## Empirical Grounding

The theoretical predictions are quantitatively consistent with the empirical findings of [Kim et al. (2025)](Towards%20a%20Science%20of%20Scaling%20Agent%20Systems.pdf), including:

- Tool-coordination tradeoff (R² = 0.267)
- Capability saturation at ~45% baseline
- Centralized coordination yielding +81% on structured tasks
- Independent coordination yielding -70% on sequential planning
- Task-contingent optimal architecture with 87% prediction accuracy

## Repository Structure

```
proofs/
  main.tex                   # Master paper document
  definitions.tex            # Formal definitions
  regime_1_independent.tex   # Regime 1: Independent agents
  regime_2_dependent.tex     # Regime 2: Dependent agents
  regime_3_parallel.tex      # Regime 3: Parallel ensembles
  regime_4_hybrid.tex        # Regime 4: Hybrid topologies
  regime_5_saturation.tex    # Regime 5: Capability saturation
  main.pdf                   # Compiled paper

scripts/
  regime1_numerical.py       # Numerical verification for Regime 1
  regime1_error_amplification.py  # Error amplification plots
  regime3_parallel.py        # Parallel ensemble simulations

agents/
  agent_o_prompt.md          # Orchestrator agent prompt
  agent_c_prompt.md          # Contributor agent prompt

exploration_log.md           # Research log tracking all proof attempts
CLAUDE.md                    # Project instructions and methodology
```

## Building the Paper

Compile the LaTeX document:

```bash
cd proofs
pdflatex main.tex
pdflatex main.tex  # run twice for TOC/references
```

## Running Scripts

```bash
cd scripts
python regime1_numerical.py
python regime1_error_amplification.py
python regime3_parallel.py
```

Requires Python with NumPy, SciPy, and Matplotlib.
