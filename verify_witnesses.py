#!/usr/bin/env python3
"""
Zero-Knowledge NP Witness Verifier (NSPL-GPU-OPT)
=================================================
Audits 100% edge feasibility, exact MWVC objective weight, and SHA-256 integrity
across all 5,000 to 130,000-node witness certificates with ZERO solver source code.

Modes:
  1. Default Suite Audit  : python verify_witnesses.py
  2. Blind Challenge Check: python verify_witnesses.py --wdimacs instance.wdimacs --sol answer.sol
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import networkx as nx


def mod200_weights(n: int) -> list[int]:
    return [((i + 1) % 200) + 1 for i in range(n)]


def verify_blind_wdimacs(wdimacs_path: Path, sol_path: Path) -> None:
    n = 0
    weights: list[int] = []
    has_weights = False
    edges: list[tuple[int, int]] = []

    with open(wdimacs_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            parts = line.strip().split()
            if not parts or parts[0] in ("c", "%"):
                continue
            if parts[0] == "p":
                n = int(parts[2])
                weights = [1] * n
            elif parts[0] in ("n", "v") and len(parts) >= 3:
                idx = int(parts[1]) - 1
                if 0 <= idx < n:
                    weights[idx] = max(1, int(float(parts[2])))
                    has_weights = True
            elif parts[0] == "e" and len(parts) >= 3:
                u, v = int(parts[1]) - 1, int(parts[2]) - 1
                if u != v:
                    edges.append((u, v))

    if not has_weights:
        weights = mod200_weights(n)

    raw_sol = sol_path.read_text(encoding="utf-8")
    cov = {int(tok) for ln in raw_sol.splitlines() if not ln.startswith("#") for tok in ln.split()}
    uncov = sum(1 for u, v in edges if u not in cov and v not in cov)
    if uncov > 0:
        raise SystemExit(f"FAIL: {uncov} uncovered edges detected!")
    total_w = sum(weights[v] for v in cov)
    sha = hashlib.sha256(raw_sol.encode("utf-8")).hexdigest()[:16]
    print(f"BLIND WITNESS PASS | N={n:,d} E={len(edges):,d} | |C|={len(cov):,d} | Exact Weight={total_w:,d} | SHA256={sha}...")


def main() -> None:
    ap = argparse.ArgumentParser(description="NSPL-GPU-OPT Zero-Source Witness Auditor")
    ap.add_argument("--wdimacs", type=Path, help="Path to custom .wdimacs challenge graph")
    ap.add_argument("--sol", type=Path, help="Path to returned .sol witness file")
    args = ap.parse_args()

    if args.wdimacs and args.sol:
        verify_blind_wdimacs(args.wdimacs, args.sol)
        return

    here = Path(__file__).resolve().parent
    manifest = json.loads((here / "witness_manifest.json").read_text(encoding="utf-8"))
    print(f"{'Instance':<15} | {'Nodes':>9} | {'Edges':>9} | {'1xFastWVC':>11} | {'8xFastWVC':>11} | {'NSPL L4 GPU':>11} | {'vs 8xFastWVC':>12} | {'Audit'}")
    print("-" * 107)

    for rec in manifest:
        inst, n, sd, p_edge = rec["instance"], rec["n"], rec["seed"], rec["p_edge"]
        sol_file = here / f"{inst}_N{n}_seed{sd}.sol"
        raw = sol_file.read_text(encoding="utf-8")
        sha = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        assert sha == rec["sha256"], f"SHA-256 mismatch on {sol_file.name}"

        cov = {int(x) for ln in raw.splitlines() if not ln.startswith("#") for x in ln.split()}
        assert all(0 <= v < n for v in cov), f"Out-of-range vertex in {sol_file.name}"

        G = nx.fast_gnp_random_graph(n, p_edge, seed=sd)
        assert G.number_of_edges() == rec["edges"], f"Graph generator mismatch on {inst}"
        assert all((u in cov or v in cov) for u, v in G.edges()), f"Uncovered edge in {inst}"

        weights = mod200_weights(n)
        true_w = sum(weights[v] for v in cov)
        exp_w = rec.get("gpu_weight", rec.get("l4_weight"))
        assert true_w == exp_w, f"Weight mismatch on {inst}: {true_w} != {exp_w}"

        f1 = rec.get("fastwvc1_weight", true_w)
        f8 = rec.get("fastwvc8_weight", true_w)
        saved_vs_8x = true_w - f8
        print(
            f"{inst:<15} | {n:>9,d} | {rec['edges']:>9,d} | {f1:>11,d} | "
            f"{f8:>11,d} | {true_w:>11,d} | {saved_vs_8x:>+12,d} | PASS (SHA OK)"
        )

    print("-" * 107)
    print(f"ALL {len(manifest)}/{len(manifest)} NP WITNESS CERTIFICATES MATHEMATICALLY VERIFIED (100% EDGE COVERAGE).")


if __name__ == "__main__":
    main()
