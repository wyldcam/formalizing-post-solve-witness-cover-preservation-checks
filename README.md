# Sub-Second GPU Minimum Weight Vertex Cover & MILP Conflict-Graph Witness Suite (5k - 130k Nodes)

Cryptographically verifiable NP witness certificates (`.sol` vertex covers + SHA-256 manifest) produced by **NSPL-GPU-OPT**, a proprietary CUDA 13.0 (`sm_89`) and C++20 optimization engine for large-scale **Minimum Weight Vertex Cover (`MWVC`)**, **Maximum Weight Independent Set (`MWIS`)**, and **MILP conflict-graph presolve / primal heuristics**.

Core `.cu` / `.cpp` solver source code is proprietary and closed-source. Because `MWVC` lies in **NP**, any engineer can independently audit 100% edge coverage, exact vertex-weight sums, and SHA-256 integrity across every instance in seconds using `verify_witnesses.py` with zero access to solver internals.

---

## 1. Hardware-Verified Results (NVIDIA L4 `sm_89` vs. HiGHS MILP, CP-SAT & FastWVC)

All benchmark instances use deterministic `networkx.fast_gnp_random_graph` seeds and the standard literature `mod-200` vertex weight assignment $w(v_i) = ((i + 1) \bmod 200) + 1$ (Cai et al., 2019).

### A. Industrial MILP (`HiGHS`) & 8-Worker `OR-Tools CP-SAT` (`1,000 ms`) vs. NSPL-GPU-OPT (`100 ms`)

| Instance (`N` / Edges) | `HiGHS` MILP (`1.0s`) | 8-Worker `CP-SAT` (`1.0s`) | 8-Thread `FastWVC` (`0.1s`) | **NSPL-GPU-OPT (`0.1s`)** | Net Advantage |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Conflict 5k** (`5,000` / `50,080`) | `502,487` | `417,509` | `382,363` | **`374,266` (C-API) / `379,110` (CLI)** | **-123,377 to -128,221 vs. HiGHS (10x faster)** |
| **Conflict 10k** (`10,000` / `99,845`) | **NO FEASIBLE SOL** *(1.84s)* | **NO FEASIBLE SOL** *(1.11s)* | `768,607` | **`754,018`** | **-14,589 vs. 8xFastWVC (`101.5 ms`)** |

### B. 6-Tier Undefeated Scaling Suite (`5,000` to `130,000` Nodes on NVIDIA L4 `sm_89`)

| Instance (`N` / Edges) | `1xFastWVC` | `8xFastWVC` | **NSPL-GPU-OPT (L4)** | vs. `1xFastWVC` | vs. `8xFastWVC` | Wall Time | Witness Audit |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Conflict 5k** (`5,000` / `50,080`) | `381,132` | `382,363` | **`379,110`** | **-2,022** | **-3,253** | `100.5 ms` | **PASS** |
| **Conflict 10k** (`10,000` / `99,845`) | `771,631` | `768,607` | **`754,018`** | **-17,613** | **-14,589** | `101.5 ms` | **PASS** |
| **Scale 25k** (`25,000` / `124,598`) | `1,655,616` | `1,648,624` | **`1,615,765`** | **-39,851** | **-32,859** | `203.2 ms` | **PASS** |
| **Scale 50k** (`50,000` / `249,308`) | `3,300,622` | `3,285,779` | **`3,244,691`** | **-55,931** | **-41,088** | `258.0 ms` | **PASS** |
| **Scale 100k** (`100,000` / `499,424`) | `6,613,020` | `6,574,869` | **`6,551,419`** | **-61,601** | **-23,450** | `418.7 ms` | **PASS** |
| **Scale 130k** (`130,000` / `648,827`) | `8,610,624` | `8,542,822` | **`8,509,178`** | **-101,446** | **-33,644** | `526.5 ms` | **PASS** |

---

## 2. Reproduce Independent Verification in 30 Seconds

Requires Python 3.9+ and `networkx` (`pip install networkx`).

```bash
python verify_witnesses.py
```

To verify a returned `.sol` certificate on your own custom `.wdimacs` challenge graph:

```bash
python verify_witnesses.py --wdimacs your_blind_graph.wdimacs --sol returned_witness.sol
```

---

## 3. 24-Hour Blind `.wdimacs` Challenge & OEM C-API Binary SDK

Enterprise optimization teams, mine-planning software vendors, and hardware partners can evaluate **NSPL-GPU-OPT** without source-code disclosure:

1. **24-Hour Blind Challenge:** Send any anonymized `.wdimacs` conflict, set-packing, or network graph (`5k-130k` nodes; integer vertex IDs `1..N` and integer weights only) with your target millisecond budget. We return a cryptographically verifiable `.sol` witness certificate for side-by-side audit against your current solver stack.
2. **On-Premise C-API Evaluation Binary (`.dll` / `.so`):** Native x64 Windows/Linux CPU and NVIDIA GPU (`sm_80` / `sm_89`) shared libraries with a single-call C header (`mwvc_solve_graph`) are available under Mutual NDA for commercial OEM integration testing.

**Author & Commercial Inquiries:** Cameron Budd — NullStateParityLabs, Perth, Western Australia
