# Minimum Weight Vertex Cover (MWVC) — Public NP Witness Archive

[![Verify Witnesses CI](https://github.com/wyldcam/nspl-gpu-mwvc-witnesses/actions/workflows/verify_witnesses.yml/badge.svg)](https://github.com/wyldcam/nspl-gpu-mwvc-witnesses/actions/workflows/verify_witnesses.yml)
[![Dependencies: Zero (Python Stdlib)](https://img.shields.io/badge/Dependencies-Zero_(Python_3.10%2B_Stdlib)-10b981.svg)](./verify_witnesses.py)
[![MCP Ready](https://img.shields.io/badge/AI_Audit-wyldcam--verifier_MCP-8b5cf6.svg)](https://github.com/wyldcam/the-ai-repository)

Zero-source, cryptographically pinned archive of **13 Minimum Weight Vertex Cover (MWVC)** NP witness certificates (`1,969,742` total edges across **7 distinct graph topologies**).

Every claim in this repository is backed by a static `.sol` certificate audited in linear $O(|V| + |E|)$ time using **only the Python 3.10+ standard library** (`zero pip installs`, `zero binaries`, `zero proprietary solver source`).

---

## Instant Independent Verification (`< 2s`, Zero Installs)

```bash
git clone https://github.com/wyldcam/nspl-gpu-mwvc-witnesses.git
cd nspl-gpu-mwvc-witnesses
python verify_witnesses.py
```

> **Verify With Your Own AI Assistant:** Clone [`wyldcam/the-ai-repository`](https://github.com/wyldcam/the-ai-repository) alongside this repository to audit every certificate directly inside **VS Code Copilot**, **Claude Code**, **Cursor**, or **Gemini CLI** via the `wyldcam-verifier` Model Context Protocol (MCP) server.

---

## Suite A — Cloud GPU Scale-Up (`NVIDIA L4`, 5k to 130k Nodes)

Executed on a dedicated cloud **NVIDIA L4 Tensor Core GPU** (Ada Lovelace architecture, 24 GB GDDR6) in standalone CLI mode on deterministic Batagelj-Brandes $G(n, p)$ instances (`mod200` integer vertex weights):

| Instance | Nodes ($N$) | Edges ($\lvert E \rvert$) | `1xFastWVC` | `8xFastWVC` [1] | Certified Witness | vs `8xFastWVC` | L4 Budget | Audit |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :--- |
| **Conflict_5k** | 5,000 | 50,080 | 381,132 | 382,363 | **379,110** | `-3,253` | 100.5 ms | `PASS` |
| **Conflict_10k** | 10,000 | 99,845 | 771,631 | 768,607 | **754,018** | `-14,589` | 101.6 ms | `PASS` |
| **Scale_25k** | 25,000 | 124,598 | 1,655,616 | 1,648,624 | **1,615,765** | `-32,859` | 203.2 ms | `PASS` |
| **Scale_50k** | 50,000 | 249,308 | 3,300,622 | 3,285,779 | **3,244,691** | `-41,088` | 258.0 ms | `PASS` |
| **Scale_100k** | 100,000 | 499,424 | 6,613,020 | 6,574,869 | **6,551,419** | `-23,450` | 418.7 ms | `PASS` |
| **Scale_130k** | 130,000 | 648,827 | 8,610,624 | 8,542,822 | **8,509,178** | `-33,644` | 526.5 ms | `PASS` |

---

## Suite B — Multi-Domain & Heavy-Tailed Topologies (Same-Host CPU Mode)

Executed in **Multi-Core Host CPU mode** (zero GPU hardware attached) head-to-head on the identical x86_64 host against `1xFastWVC`, `8xFastWVC` (`100–200 ms`), **SciPy HiGHS MILP** (`1.0s` target), and **Google OR-Tools CP-SAT** (`1.0s` target):

| Instance | Topology Family | $N$ / $\lvert E \rvert$ | $\Delta_{\max}$ | HiGHS (`1s`) | CP-SAT (`1s`) | `8xFastWVC` | Certified Witness | vs `8xFastWVC` | Status |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :--- |
| **BHOSLIB_frb30_15** | Planted Phase-Transition | 450 / 22,514 | 125 | 60,146 | 54,266 | 54,266 | **54,266** | `0 (Tie OPT)` | **`EXACT OPT`** |
| **DIMACS_brock200_vc** | Hidden Independent-Set Trap | 200 / 8,924 | 114 | 19,877 | 18,456 | 17,860 | **17,860** | `0 (Beats CP-SAT -596)` | **`EXACT OPT`** |
| **Sparse_InfraHub_10k** | Sparse Power-Law Hubs | 10k / 17,986 | 233 | 322,016 *(24.9s)* | 322,016 *(0.31s)* | 325,042 | **322,016** *(2.3ms)* | `-3,026` | **`EXACT OPT`** |
| **Mine_Precedence_4k** | Layered Bench Precedence | 4k / 24,536 | 57 | 688,735 *(5.1s)* | 438,920 *(0.97s)* | 444,235 | **439,600** | `-4,635` | `100% Feasible` |
| **BA_ScaleFree_5k** | Barabasi-Albert Scale-Free | 5k / 49,945 | 370 | 436,374 *(7.5s)* | 349,916 *(1.35s)* | 326,125 | **321,521** | `-4,604` | `100% Feasible` |
| **MILP_HubConflict_5k** | Extreme Hub-Conflict MILP | 5k / 48,770 | 1,181 | 456,621 *(7.3s)* | 344,797 *(1.36s)* | 296,299 | **291,605** | `-4,694` | `100% Feasible` |
| **BA_ScaleFree_25k** | Large Scale-Free Network | 25k / 124,985 | 488 | *Skipped (>10k)* | *Skipped (>10k)* | 1,362,510 | **1,329,565** | **`-32,945`** | `100% Feasible` |

*(Under an equal `100 ms` real-time cutoff on `Mine_Precedence_4k`, `BA_ScaleFree_5k`, and `MILP_HubConflict_5k`, both HiGHS and CP-SAT return `UNKNOWN` with zero feasible integer solutions.)*

---

## Execution Modes & Measurement Boundaries

See **[`BENCHMARKS.md`](./BENCHMARKS.md)** for full methodology, hardware tier separation, and baseline definitions:

1. **Compute Backend (`GPU Backend` vs. `Host CPU Backend`):** Suite A demonstrates throughput on dedicated cloud GPU silicon (`NVIDIA L4`), whereas Suite B demonstrates that even on CPU-only infrastructure without a GPU attached, the solver outperforms parallel local-search portfolios and 1-second MILP/CP-SAT runs.
2. **Integration Boundary (`Standalone File CLI` vs. `In-Memory Native API`):** Public `.sol` witnesses are emitted via the standalone file CLI (which includes ASCII graph parsing and file I/O inside wall-clock budgets); enterprise deployments also support direct in-memory array invocation with zero file-parsing overhead.
3. **Hardware-Independent Mathematical Proof:** While wall-clock timings vary across hardware environments, **100% edge coverage and integer objective weights in `.sol` certificates are static mathematical invariants** verifiable on any machine.

---

## Blind-Challenge Evaluation (`.wdimacs`)

To evaluate solver quality on your own anonymized conflict graphs under a zero-trust protocol, export a standard `.wdimacs` file (`p edge N M`, optional `n <id> <weight>`, `e <u> <v>`) and audit the returned `.sol` certificate locally:

```bash
python verify_witnesses.py --wdimacs challenge.wdimacs --sol returned.sol
```

---

### Footnotes

- **[1] `1xFastWVC` & `8xFastWVC` Baselines:** `1xFastWVC` implements the published single-thread local search baseline of Cai, Li, Hou & Wang, *"Towards faster local search for minimum weight vertex cover on massive graphs,"* *Information Sciences* 471: 64–79 (2019). `8xFastWVC` runs an 8-worker concurrent OpenMP multi-seed portfolio under the identical wall-clock cutoff and reports $\min_{k \in \{1..8\}} W(C_k)$.
