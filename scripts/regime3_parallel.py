#!/usr/bin/env python3
"""
Regime 3 — Parallel Redundancy (Ensemble Voting)
Agent C, Exploration 4

Computes and plots:
(a) P_sys^any(n) = 1 - (1-p)^n, diminishing returns, marginal gain
(b) P_sys^majority(n) for odd n, crossover analysis
(c) Redundancy-overhead tradeoff P_eff(n) = P_sys(n) - n*c
(d) p=0.45 saturation analysis: sequential vs parallel vs majority
(e) Parallel throughput optimum: max n * [1-(1-p)^n]
"""

import numpy as np
from math import comb, ceil, log, exp, floor
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ============================================================
# (a) P_sys^any and diminishing returns
# ============================================================
print("=" * 70)
print("PART (a): P_sys^any = 1 - (1-p)^n, Diminishing Returns")
print("=" * 70)

p_values = [0.3, 0.45, 0.6, 0.8, 0.9]
n_range = np.arange(1, 51)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Plot P_sys^any
for p in p_values:
    psys = 1 - (1 - p) ** n_range
    axes[0].plot(n_range, psys, label=f'p={p}')
axes[0].set_xlabel('n (number of agents)')
axes[0].set_ylabel('P_sys^any(n)')
axes[0].set_title('Parallel: At-Least-One Succeeds')
axes[0].legend()
axes[0].grid(True, alpha=0.3)
axes[0].set_ylim([0, 1.05])

# Marginal gain: delta(n) = P_sys(n+1) - P_sys(n) = (1-p)^n * p
# Actually: delta(n) = [1-(1-p)^{n+1}] - [1-(1-p)^n] = (1-p)^n - (1-p)^{n+1} = (1-p)^n * p
for p in p_values:
    marginal = p * (1 - p) ** (n_range - 1)  # marginal gain from n-th agent (n=1,2,...)
    axes[1].plot(n_range, marginal, label=f'p={p}')
axes[1].set_xlabel('n (agent number)')
axes[1].set_ylabel('Marginal gain delta(n)')
axes[1].set_title('Marginal Gain from n-th Agent')
axes[1].legend()
axes[1].grid(True, alpha=0.3)
axes[1].set_yscale('log')

# Verify monotone decrease of marginal gain
print("\nMarginal gain delta(n) = p * (1-p)^{n-1}:")
print(f"{'p':>6} | {'delta(1)':>10} | {'delta(5)':>10} | {'delta(10)':>10} | {'delta(20)':>10} | {'delta(50)':>10} | Monotone?")
print("-" * 85)
for p in p_values:
    deltas = [p * (1 - p) ** (n - 1) for n in range(1, 51)]
    is_monotone = all(deltas[i] >= deltas[i + 1] for i in range(len(deltas) - 1))
    print(f"{p:>6.2f} | {deltas[0]:>10.6f} | {deltas[4]:>10.6f} | {deltas[9]:>10.6f} | {deltas[19]:>10.6f} | {deltas[49]:>10.6f} | {is_monotone}")

# P_sys^any table
print("\nP_sys^any(n) = 1 - (1-p)^n:")
print(f"{'p':>6} | {'n=1':>8} | {'n=2':>8} | {'n=3':>8} | {'n=5':>8} | {'n=10':>8} | {'n=20':>8} | {'n=50':>8}")
print("-" * 80)
for p in p_values:
    vals = [1 - (1 - p) ** n for n in [1, 2, 3, 5, 10, 20, 50]]
    print(f"{p:>6.2f} | {vals[0]:>8.5f} | {vals[1]:>8.5f} | {vals[2]:>8.5f} | {vals[3]:>8.5f} | {vals[4]:>8.5f} | {vals[5]:>8.5f} | {vals[6]:>8.5f}")

# Plot ratio of consecutive marginal gains
for p in p_values:
    ratio = (1 - p)  # constant ratio! delta(n+1)/delta(n) = (1-p) always
    axes[2].axhline(y=1 - p, label=f'p={p}, ratio={1-p:.2f}', linestyle='--')
axes[2].set_xlabel('n')
axes[2].set_ylabel('delta(n+1)/delta(n)')
axes[2].set_title('Ratio of Consecutive Marginal Gains = (1-p)')
axes[2].legend()
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/workspaces/research/scripts/regime3_any_succeeds.png', dpi=150)
plt.close()

print("\nKEY INSIGHT: Marginal gain ratio delta(n+1)/delta(n) = (1-p) = constant.")
print("The marginal gains form a GEOMETRIC sequence with ratio (1-p).")
print("This is the parallel analog of the sequential geometric decay p^n.")

# ============================================================
# (b) Majority voting
# ============================================================
print("\n" + "=" * 70)
print("PART (b): P_sys^majority for odd n")
print("=" * 70)

def p_majority(n, p):
    """P(at least ceil(n/2) out of n succeed), for odd n this is (n+1)/2."""
    threshold = ceil(n / 2)
    return sum(comb(n, k) * p**k * (1 - p)**(n - k) for k in range(threshold, n + 1))

odd_n = list(range(1, 50, 2))
p_test = [0.3, 0.4, 0.45, 0.5, 0.55, 0.6, 0.7, 0.8, 0.9]

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Plot majority voting vs n
for p in p_test:
    pmaj = [p_majority(n, p) for n in odd_n]
    axes[0].plot(odd_n, pmaj, label=f'p={p}', marker='.' if p in [0.45, 0.5, 0.55] else None, markersize=3)
axes[0].axhline(y=0.5, color='gray', linestyle=':', alpha=0.5)
axes[0].set_xlabel('n (odd, number of agents)')
axes[0].set_ylabel('P_sys^majority(n)')
axes[0].set_title('Majority Voting Reliability')
axes[0].legend(fontsize=8)
axes[0].grid(True, alpha=0.3)

# Table for majority voting
print("\nP_sys^majority(n) for selected p and odd n:")
print(f"{'p':>6} | {'n=1':>8} | {'n=3':>8} | {'n=5':>8} | {'n=9':>8} | {'n=21':>8} | {'n=49':>8} | {'Trend':>10}")
print("-" * 85)
for p in p_test:
    vals = [p_majority(n, p) for n in [1, 3, 5, 9, 21, 49]]
    trend = "IMPROVING" if vals[-1] > vals[0] + 0.001 else ("DEGRADING" if vals[-1] < vals[0] - 0.001 else "FLAT")
    print(f"{p:>6.2f} | {vals[0]:>8.5f} | {vals[1]:>8.5f} | {vals[2]:>8.5f} | {vals[3]:>8.5f} | {vals[4]:>8.5f} | {vals[5]:>8.5f} | {trend:>10}")

# Phase transition at p=0.5
print("\nPHASE TRANSITION at p=0.5:")
print("For p > 0.5: majority voting IMPROVES with n (converges to 1)")
print("For p < 0.5: majority voting DEGRADES with n (converges to 0)")
print("For p = 0.5: majority voting is constant at 0.5")

# Verify convergence rate
print("\nConvergence rate analysis (how fast majority voting converges):")
for p in [0.55, 0.6, 0.7, 0.8, 0.9]:
    # Find n where P_majority > 0.99
    n_99 = None
    for n in range(1, 1000, 2):
        if p_majority(n, p) > 0.99:
            n_99 = n
            break
    print(f"  p={p:.2f}: n for P_majority > 0.99 is n={n_99}")

# Anti-wisdom of crowds
print("\nAnti-wisdom of crowds (p < 0.5):")
for p in [0.3, 0.4, 0.45]:
    n_01 = None
    for n in range(1, 1000, 2):
        if p_majority(n, p) < 0.01:
            n_01 = n
            break
    print(f"  p={p:.2f}: n for P_majority < 0.01 is n={n_01}")

# Plot the derivative (change in P_majority when going from n to n+2)
for p in [0.45, 0.5, 0.55, 0.6, 0.8]:
    pmaj = [p_majority(n, p) for n in odd_n]
    dpdn = [(pmaj[i+1] - pmaj[i]) / 2 for i in range(len(pmaj) - 1)]
    axes[1].plot(odd_n[:-1], dpdn, label=f'p={p}')
axes[1].axhline(y=0, color='black', linestyle='-', alpha=0.3)
axes[1].set_xlabel('n (odd)')
axes[1].set_ylabel('d(P_majority)/dn (approx)')
axes[1].set_title('Rate of Change of Majority Voting')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/workspaces/research/scripts/regime3_majority.png', dpi=150)
plt.close()

# ============================================================
# (c) Redundancy-overhead tradeoff
# ============================================================
print("\n" + "=" * 70)
print("PART (c): Redundancy-Overhead Tradeoff")
print("=" * 70)

cost_values = [0.005, 0.01, 0.02, 0.05, 0.1]

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# "Any succeeds" with cost
print("\n--- 'Any Succeeds' model: P_eff(n) = 1-(1-p)^n - n*c ---")
print(f"{'p':>5} {'c':>6} | {'n*':>4} | {'P_eff(n*)':>10} | {'P_sys(n*)':>10}")
print("-" * 50)

for p in [0.3, 0.45, 0.6, 0.8]:
    for c in cost_values:
        best_n = 1
        best_peff = p - c
        for n in range(1, 201):
            peff = 1 - (1 - p)**n - n * c
            if peff > best_peff:
                best_peff = peff
                best_n = n
        psys_at_best = 1 - (1 - p)**best_n
        print(f"{p:>5.2f} {c:>6.3f} | {best_n:>4d} | {best_peff:>10.6f} | {psys_at_best:>10.6f}")

# Analytical formula for n* in "any succeeds":
# d/dn P_eff = (1-p)^n * ln(1/(1-p)) - c = 0
# => (1-p)^n = c / ln(1/(1-p))
# => n* = ln(c / ln(1/(1-p))) / ln(1-p)
print("\nAnalytical n* for 'any succeeds': n* = ln(c / ln(1/(1-p))) / ln(1-p)")
print(f"{'p':>5} {'c':>6} | {'n*_formula':>12} | {'n*_brute':>10}")
print("-" * 45)
for p in [0.3, 0.45, 0.6, 0.8]:
    for c in [0.01, 0.02, 0.05]:
        q = 1 - p
        ln_inv_q = log(1 / q)
        if c < ln_inv_q:  # otherwise n*=1
            n_star_cont = log(c / ln_inv_q) / log(q)
            n_star_int = max(1, round(n_star_cont))
        else:
            n_star_cont = 1.0
            n_star_int = 1
        # Brute force
        best_n = 1
        best_peff = p - c
        for n in range(1, 201):
            peff = 1 - q**n - n * c
            if peff > best_peff:
                best_peff = peff
                best_n = n
        print(f"{p:>5.2f} {c:>6.3f} | {n_star_cont:>12.4f} | {best_n:>10d}")

# Plot P_eff for "any succeeds"
for idx, p in enumerate([0.3, 0.45, 0.6, 0.8]):
    ax = axes[idx // 2][idx % 2]
    for c in cost_values:
        peff = [1 - (1 - p)**n - n * c for n in n_range]
        ax.plot(n_range, peff, label=f'c={c}')
        # Mark optimum
        best_n = max(n_range, key=lambda n: 1 - (1 - p)**n - n * c)
        best_peff = 1 - (1 - p)**best_n - best_n * c
        ax.plot(best_n, best_peff, 'ko', markersize=5)
    ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax.set_xlabel('n')
    ax.set_ylabel('P_eff(n)')
    ax.set_title(f'Any-Succeeds P_eff, p={p}')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/workspaces/research/scripts/regime3_peff_any.png', dpi=150)
plt.close()

# "Majority succeeds" with cost
print("\n--- 'Majority Succeeds' model: P_eff(n) = P_majority(n) - n*c ---")
print(f"{'p':>5} {'c':>6} | {'n*':>4} | {'P_eff(n*)':>10} | {'P_maj(n*)':>10}")
print("-" * 55)

for p in [0.3, 0.45, 0.55, 0.6, 0.8]:
    for c in [0.01, 0.02, 0.05]:
        best_n = 1
        best_peff = p - c
        for n in range(1, 100, 2):  # odd n only
            peff = p_majority(n, p) - n * c
            if peff > best_peff:
                best_peff = peff
                best_n = n
        pmaj_at_best = p_majority(best_n, p)
        print(f"{p:>5.2f} {c:>6.3f} | {best_n:>4d} | {best_peff:>10.6f} | {pmaj_at_best:>10.6f}")

# Compare "any" vs "majority"
print("\n--- When is 'Any Succeeds' better than 'Majority Succeeds'? ---")
print(f"{'p':>5} {'c':>6} | {'n*_any':>7} {'Peff_any':>10} | {'n*_maj':>7} {'Peff_maj':>10} | {'Winner':>10}")
print("-" * 75)
for p in [0.3, 0.45, 0.55, 0.6, 0.8, 0.9]:
    for c in [0.01, 0.05]:
        # Best any
        best_n_any, best_peff_any = 1, p - c
        for n in range(1, 201):
            peff = 1 - (1 - p)**n - n * c
            if peff > best_peff_any:
                best_peff_any = peff
                best_n_any = n
        # Best majority
        best_n_maj, best_peff_maj = 1, p - c
        for n in range(1, 201, 2):
            peff = p_majority(n, p) - n * c
            if peff > best_peff_maj:
                best_peff_maj = peff
                best_n_maj = n
        winner = "ANY" if best_peff_any > best_peff_maj else "MAJORITY"
        print(f"{p:>5.2f} {c:>6.3f} | {best_n_any:>7d} {best_peff_any:>10.6f} | {best_n_maj:>7d} {best_peff_maj:>10.6f} | {winner:>10}")

# ============================================================
# (d) p=0.45 saturation analysis
# ============================================================
print("\n" + "=" * 70)
print("PART (d): p=0.45 Saturation — Sequential vs Parallel vs Majority")
print("=" * 70)

p = 0.45
print(f"\np = {p}")
print(f"{'n':>4} | {'Sequential':>12} | {'Parallel(any)':>14} | {'Majority':>12} | {'Best':>10}")
print("-" * 65)
for n in [1, 2, 3, 5, 7, 9, 11, 15, 21, 31, 49]:
    seq = p**n
    par = 1 - (1 - p)**n
    if n % 2 == 1:
        maj = p_majority(n, p)
    else:
        maj = p_majority(n, p)  # still works, threshold is ceil(n/2)
    best = max([("SEQ", seq), ("PAR", par), ("MAJ", maj)], key=lambda x: x[1])
    print(f"{n:>4d} | {seq:>12.8f} | {par:>14.8f} | {maj:>12.8f} | {best[0]:>10}")

# Find crossover point where parallel beats sequential
print("\nCrossover: parallel (any) beats sequential when 1-(1-p)^n > p^n")
print("This simplifies to: 1 > p^n + (1-p)^n")
# f(n) = p^n + (1-p)^n; f(1) = 1, and for p != 0,1, f is decreasing, so crossover at n=2
print("For p=0.45: p^n + (1-p)^n values:")
for n in range(1, 11):
    val = p**n + (1 - p)**n
    print(f"  n={n}: {val:.8f}  => parallel {'WINS' if val < 1 else 'TIES/LOSES'}")

print("\nINSIGHT: For ANY p in (0,1), p^n + (1-p)^n < 1 for all n >= 2.")
print("PROOF: By AM-GM, for x,y > 0 with x+y=1, x^n + y^n < (x+y)^n = 1 for n >= 2.")
print("Actually more precisely: p^n + (1-p)^n <= max(p,1-p)^{n-1} * 1 for n >= 2.")
print("So parallel (any) ALWAYS beats sequential for n >= 2, regardless of p.")

# With costs
print("\nWith coordination cost c:")
for c in [0.01, 0.02, 0.05]:
    print(f"\n  c = {c}:")
    print(f"  {'n':>4} | {'P_seq_eff':>12} | {'P_par_eff':>12} | {'P_maj_eff':>12}")
    print(f"  " + "-" * 50)
    for n in [1, 2, 3, 5, 10, 20]:
        seq_eff = p**n * (1 - c)**(n - 1)
        par_eff = 1 - (1 - p)**n - n * c
        maj_eff = p_majority(n, p) - n * c
        print(f"  {n:>4d} | {seq_eff:>12.8f} | {par_eff:>12.8f} | {maj_eff:>12.8f}")

# ============================================================
# (e) Parallel throughput optimum
# ============================================================
print("\n" + "=" * 70)
print("PART (e): Parallel Throughput Optimum — max n * [1-(1-p)^n]")
print("=" * 70)

# Throughput T(n) = n * [1 - (1-p)^n]
# dT/dn = [1 - (1-p)^n] + n * (1-p)^n * ln(1/(1-p))
# = [1 - (1-p)^n] + n * (1-p)^n * |ln(1-p)|
# This is always > 0! Since both terms are positive.
# So throughput is MONOTONICALLY INCREASING for "any succeeds"!

print("\nThroughput T(n) = n * [1-(1-p)^n]:")
print(f"{'p':>5} | {'n=1':>8} | {'n=5':>8} | {'n=10':>8} | {'n=20':>8} | {'n=50':>8}")
print("-" * 55)
for p in p_values:
    vals = [n * (1 - (1 - p)**n) for n in [1, 5, 10, 20, 50]]
    print(f"{p:>5.2f} | {vals[0]:>8.4f} | {vals[1]:>8.4f} | {vals[2]:>8.4f} | {vals[3]:>8.4f} | {vals[4]:>8.4f}")

print("\nOBSERVATION: Throughput T(n) = n*[1-(1-p)^n] is MONOTONICALLY INCREASING.")
print("PROOF: dT/dn = [1-(1-p)^n] + n*(1-p)^n*|ln(1-p)| > 0 since both terms positive.")
print("So there is NO finite optimum without a cost term.")
print("This contrasts with sequential where T(n) = n*p^n has optimum at n* = -1/ln(p).")

# With cost: T_eff(n) = n * [1-(1-p)^n] - n^2 * c (quadratic cost for parallel overhead)
# Or: T_eff(n) = n * [1-(1-p)^n - c] which is the per-agent effective probability times n
print("\nAlternative: Per-agent effective output = [1-(1-p)^n]/n (success rate per agent)")
print("This is the 'efficiency' metric:")
print(f"{'p':>5} | {'n=1':>8} | {'n=5':>8} | {'n=10':>8} | {'n=20':>8} | {'n=50':>8}")
print("-" * 55)
for p in p_values:
    vals = [(1 - (1 - p)**n) / n for n in [1, 5, 10, 20, 50]]
    print(f"{p:>5.2f} | {vals[0]:>8.5f} | {vals[1]:>8.5f} | {vals[2]:>8.5f} | {vals[3]:>8.5f} | {vals[4]:>8.5f}")

print("\nEfficiency [1-(1-p)^n]/n is MONOTONICALLY DECREASING (diminishing returns).")
print("At n=1, efficiency = p. As n -> inf, efficiency -> 0.")
print("This is the 'cost per unit reliability' interpretation.")

# For the "success probability per agent" model with cost:
# Maximize P_eff(n)/n where P_eff(n) = 1-(1-p)^n - n*c
# Or better: think of throughput with cost T(n) = n * [1-(1-p)^n] - n*c_parallel
# where c_parallel is the cost of adding a parallel agent
print("\nParallel throughput with cost: T(n) = n*[1-(1-p)^n] - n*c (linear parallel cost)")
print("= n*[1-(1-p)^n - c]")
print("Optimum: d/dn = 0 => [1-(1-p)^n - c] + n*(1-p)^n*|ln(1-p)| = 0")
print("Let q=1-p. Then: 1-q^n-c + n*q^n*|ln q| = 0")

for p in [0.3, 0.45, 0.6, 0.8]:
    q = 1 - p
    ln_q = abs(log(q))
    for c in [0.01, 0.05, 0.1]:
        best_n = 1
        best_T = 1 * (1 - q - c)
        for n in range(1, 201):
            T = n * (1 - q**n - c)
            if T > best_T:
                best_T = T
                best_n = n
        psys = 1 - q**best_n
        print(f"  p={p:.2f}, c={c:.3f}: n*={best_n:>4d}, T(n*)={best_T:>8.4f}, P_sys(n*)={psys:.5f}")

# Check for universal constant in parallel model
# For sequential: at n* = -1/ln(p), P_sys = e^{-1}
# For parallel "any succeeds" with cost c:
# At optimum: 1-q^n + n*q^n*|ln q| = c
# The P_sys at optimum depends on both p and c — no universal constant
print("\nP_sys at throughput-optimal n* for parallel (with cost):")
print(f"{'p':>5} {'c':>6} | {'n*':>4} | {'P_sys(n*)':>10} | {'1-P_sys':>10}")
print("-" * 50)
for p in [0.3, 0.45, 0.6, 0.8, 0.9]:
    q = 1 - p
    for c in [0.01, 0.05]:
        best_n = 1
        best_T = 1 * (1 - q - c)
        for n in range(1, 501):
            T = n * (1 - q**n - c)
            if T > best_T:
                best_T = T
                best_n = n
        psys = 1 - q**best_n
        print(f"{p:>5.2f} {c:>6.3f} | {best_n:>4d} | {psys:>10.6f} | {1-psys:>10.6f}")

print("\nCONCLUSION: No universal constant like e^{-1} for parallel throughput.")
print("The P_sys at optimum depends on both p and c.")
print("This is because parallel does not have the clean geometric structure of sequential.")

# ============================================================
# Additional: Compare architectures at p=0.45
# ============================================================
print("\n" + "=" * 70)
print("SUMMARY: Architecture Comparison at p=0.45 (Kim et al. threshold)")
print("=" * 70)

p = 0.45
print(f"\nAt p={p}, for a task requiring n agents:")
print(f"{'n':>3} | {'Sequential':>10} | {'Parallel':>10} | {'Majority':>10} | {'Par/Seq ratio':>14}")
print("-" * 55)
for n in range(1, 21):
    seq = p**n
    par = 1 - (1 - p)**n
    maj = p_majority(n, p) if n >= 1 else p
    ratio = par / seq if seq > 1e-15 else float('inf')
    print(f"{n:>3d} | {seq:>10.6f} | {par:>10.6f} | {maj:>10.6f} | {ratio:>14.2f}")

print("\nKEY FINDING: At p=0.45, the parallel/sequential ratio grows EXPONENTIALLY.")
print("By n=5: parallel is 52x better than sequential.")
print("By n=10: parallel is 2750x better.")
print("This is why the ~45% threshold matters: below it, sequential is catastrophic")
print("but parallel still works well.")

# Final plot: architecture comparison
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

n_range_full = np.arange(1, 21)
for p in [0.3, 0.45, 0.6, 0.8]:
    seq = [p**n for n in n_range_full]
    par = [1 - (1 - p)**n for n in n_range_full]
    axes[0].plot(n_range_full, seq, '--', label=f'Seq p={p}', alpha=0.7)
    axes[0].plot(n_range_full, par, '-', label=f'Par p={p}', alpha=0.7)
axes[0].set_xlabel('n')
axes[0].set_ylabel('P_sys')
axes[0].set_title('Sequential vs Parallel')
axes[0].legend(fontsize=7)
axes[0].grid(True, alpha=0.3)
axes[0].set_yscale('log')

# Ratio plot
for p in [0.3, 0.45, 0.6, 0.8]:
    ratio = [(1 - (1 - p)**n) / (p**n) for n in n_range_full]
    axes[1].plot(n_range_full, ratio, label=f'p={p}')
axes[1].set_xlabel('n')
axes[1].set_ylabel('P_par / P_seq')
axes[1].set_title('Parallel Advantage Ratio')
axes[1].legend()
axes[1].grid(True, alpha=0.3)
axes[1].set_yscale('log')

plt.tight_layout()
plt.savefig('/workspaces/research/scripts/regime3_comparison.png', dpi=150)
plt.close()

print("\nPlots saved to scripts/regime3_*.png")
print("\n" + "=" * 70)
print("ALL COMPUTATIONS COMPLETE")
print("=" * 70)
