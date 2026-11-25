# Benchmark Methodology & Execution Tier Guide

This document defines the hardware separation, solver execution modes, and baseline protocols behind the **13 public MWVC certificates** in [`witness_manifest.json`](./witness_manifest.json).

---

## 1. Hardware Tier Separation

To prevent conflating dedicated accelerator timings with general-purpose CPU environments, public benchmarks are strictly partitioned into two execution tiers:

| Suite | Execution Tier | Role & Scope |
| :--- | :--- | :--- |
| **Suite A** (`Conflict_5k` – `Scale_130k`) | **Dedicated Cloud GPU** (`NVIDIA L4 Tensor Core GPU`, Ada Lovelace, 24 GB GDDR6) | Measures large-scale throughput (`50k` to `648k` edges) under strict sub-second real-time budgets (`100 ms – 527 ms`). |
| **Suite B** (`BHOSLIB`, `DIMACS`, `ScaleFree`, `MILP_Hub`, `Mine_Precedence`, `InfraHub`) | **Multi-Core Host CPU** (Same-Host x86_64 Head-to-Head, `0` GPUs attached) | Evaluates structural diversity across adversarial cliques, heavy-tailed hubs ($\Delta_{\max}=1,181$), and precedence graphs where solver and all 4 baselines share the exact same host CPU. |

> **Why Objective Weights Are Bulletproof Across Hardware:** OS background jitter or CPU clock differences only affect wall-clock milliseconds; they can never alter the mathematical validity or exact integer weight sum $W(C) = \sum_{v \in C} w(v)$ of a published `.sol` witness certificate. Every certificate in this repository satisfies 100% edge coverage with zero uncovered edges.

---

## 2. Black-Box Execution Modes

Without disclosing proprietary internal algorithms, evaluators should note two black-box operational boundaries when interpreting timings:

### A. Compute Backend (`GPU Backend` vs. `Host CPU Backend`)
- **GPU Backend:** Dispatches massively parallel trajectory waves on NVIDIA GPUs for high-cardinality industrial conflict graphs.
- **Host CPU Backend:** Runs deterministically across standard multi-core x86_64 threads when GPU hardware is unavailable (used for all Suite B certificates).

### B. Invocation Boundary (`Standalone File CLI` vs. `In-Memory Native API`)
- **Standalone File CLI:** Reads ASCII benchmark graphs from disk, parses text streams, solves, and writes `.sol` output files. Reported CLI wall-clock times therefore include **disk I/O and text-parsing overhead**.
- **In-Memory Native API:** Accepts pre-resident memory buffers directly inside host applications (such as MILP callbacks, mine schedulers, or dispatch engines), eliminating disk and ASCII parsing latency so 100% of the time budget goes to optimization.

---

## 3. Baseline Solvers & Fairness Protocol

1. **`1xFastWVC` (Single-Thread Academic Baseline):** Faithful implementation of Cai, Li, Hou & Wang (*Information Sciences* 471: 64–79, 2019) given the identical time budget.
2. **`8xFastWVC` (8-Worker Parallel Portfolio):** Concurrent 8-thread OpenMP portfolio running independent random seeds and returning the minimum-weight feasible cover $\min_{k \in \{1..8\}} W(C_k)$ within the same wall-clock budget.
3. **Exact & Commercial-Grade Solvers (Suite B):**
   - **SciPy / HiGHS MILP (`1.0s` target):** Given **10x** the time budget (`1,000 ms` vs `100 ms`), HiGHS still trails by thousands of weight units on `Mine_Precedence_4k`, `BA_ScaleFree_5k`, and `MILP_HubConflict_5k` (and requires `24.9s` to match the `2.33 ms` optimal witness on `Sparse_InfraHub_10k`).
   - **Google OR-Tools CP-SAT (`1.0s` target):** Given **10x** the time budget (`1,000 ms` vs `100 ms`), CP-SAT remains suboptimal on `DIMACS_brock200_vc` (`+596`), `BA_ScaleFree_5k` (`+28,395`), and `MILP_HubConflict_5k` (`+53,192`).
