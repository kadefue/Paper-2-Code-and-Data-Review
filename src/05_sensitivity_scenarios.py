#!/usr/bin/env python3
"""
src/05_sensitivity_scenarios.py
===============================
Step 5 of Study 2: Counterfactual Sensitivity Scenarios
(+30% Tractor/Tiller Hire & Diesel Shock + Plot-Size Scale Threshold Strata).

Reads:
  - outputs/data/ipwra_balanced_panel.parquet
  - outputs/data/mve_simulation_draws.npz

Exports:
  - outputs/tables/table6_stoplight_sensitivity_scenarios.csv & .md
  - outputs/data/mve_simulation_draws.npz (updated with scenario draws)

Usage:
  .venv/bin/python src/05_sensitivity_scenarios.py
"""

import os
import sys
import numpy as np
import pandas as pd

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from importlib import import_module
sim_mod = import_module("04_stochastic_sim")

BASE_DIR = os.path.dirname(SRC_DIR)
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
IN_PARQUET = os.path.join(OUTPUTS_DIR, "data", "ipwra_balanced_panel.parquet")
OUT_NPZ = os.path.join(OUTPUTS_DIR, "data", "mve_simulation_draws.npz")
OUT_T6_CSV = os.path.join(OUTPUTS_DIR, "tables", "table6_stoplight_sensitivity_scenarios.csv")
OUT_T6_MD = os.path.join(OUTPUTS_DIR, "tables", "table6_stoplight_sensitivity_scenarios.md")


def nfi_cuts_for_crop(crop):
    if crop == "Paddy":
        return 800_000.0, 1_800_000.0
    return 600_000.0, 1_200_000.0


def evaluate_stoplight(crop, scenario, res, hire_shock_mult=1.0, biochem_shock_mult=1.0, price_shock_mult=1.0):
    """Computes NFI and Return-to-Labor stoplight probabilities for a scenario."""
    red_nfi, green_nfi = nfi_cuts_for_crop(crop)
    rows = []
    for j, r in enumerate(res["regimes"]):
        k_arr = res["K_sim"][:, j] * (hire_shock_mult if r in ("M2", "M3", "M2_M3") else 1.0)
        b_arr = res["B_sim"][:, j] * biochem_shock_mult
        rev = (res["P_sim"][:, j] * price_shock_mult) * res["y_mve"][:, j]
        nfi = rev - (k_arr + res["L_sim"][:, j] + b_arr)
        ret_lab = (rev - k_arr - b_arr) / np.clip(res["D_sim"][:, j], 15.0, 160.0)

        nr, ny, ng = sim_mod.stoplight_probs(nfi, red_nfi, green_nfi)
        lr, ly, lg = sim_mod.stoplight_probs(ret_lab, 7000.0, 12000.0)
        rows.append({
            "Crop": crop,
            "Scenario": scenario,
            "Regime": r,
            "n_plots": res["cell_n"][r],
            "N_eff": round(res["cell_neff"][r], 1),
            "NFI_Mean_TZS_ha": round(float(np.mean(nfi)), 0),
            "NFI_Median_TZS_ha": round(float(np.median(nfi)), 0),
            "NFI_Red_pct": nr,
            "NFI_Yellow_pct": ny,
            "NFI_Green_pct": ng,
            "Labor_Mean_TZS_day": round(float(np.mean(ret_lab)), 0),
            "Labor_Median_TZS_day": round(float(np.median(ret_lab)), 0),
            "Labor_Red_pct": lr,
            "Labor_Yellow_pct": ly,
            "Labor_Green_pct": lg,
        })
    return rows


def main():
    print("================================================================================")
    print(" STEP 5: SENSITIVITY SCENARIOS (+30% FUEL/HIRE SHOCK & PLOT-SIZE STRATA)")
    print("================================================================================")

    df = pd.read_parquet(IN_PARQUET)
    existing_npz = dict(np.load(OUT_NPZ)) if os.path.exists(OUT_NPZ) else {}
    t6_rows = []

    scale_strata = [
        ("Scale_Small_lt_1ha", lambda d: d[d["planted_ha"] < 1.0]),
        ("Scale_Medium_1_3ha", lambda d: d[(d["planted_ha"] >= 1.0) & (d["planted_ha"] <= 3.0)]),
        ("Scale_Large_gt_3ha", lambda d: d[d["planted_ha"] > 3.0]),
    ]

    for crop in ("Maize", "Paddy", "Legumes"):
        df_c = df[df["crop_group"] == crop].copy()
        if df_c.empty:
            continue

        # 1. Baseline, +30% Diesel/Hire Shock, Combined (+30% K, +15% B) Shock, & -10% Farmgate Price Shock
        res_base = sim_mod.simulate_crop_stratum(df_c, aez_code=0, seed=sim_mod.SEED, n_iter=sim_mod.N_ITER)
        t6_rows.extend(evaluate_stoplight(crop, "Baseline", res_base, hire_shock_mult=1.00, biochem_shock_mult=1.00))
        t6_rows.extend(evaluate_stoplight(crop, "Shock_Plus30pct_Fuel_Hire", res_base, hire_shock_mult=1.30, biochem_shock_mult=1.00))
        t6_rows.extend(evaluate_stoplight(crop, "Shock_Fuel30_Biochem15", res_base, hire_shock_mult=1.30, biochem_shock_mult=1.15))
        t6_rows.extend(evaluate_stoplight(crop, "Shock_Minus10pct_Price", res_base, hire_shock_mult=1.00, biochem_shock_mult=1.00, price_shock_mult=0.90))

        for j, r in enumerate(res_base["regimes"]):
            mult = 1.30 if r in ("M2", "M3", "M2_M3") else 1.0
            k_shk = res_base["K_sim"][:, j] * mult
            rev = res_base["P_sim"][:, j] * res_base["y_mve"][:, j]
            existing_npz[f"{crop}__{r}__nfi_shock30"] = rev - (k_shk + res_base["L_sim"][:, j] + res_base["B_sim"][:, j])

        # 2. Plot-Size Scale Threshold Strata
        for s_name, s_fn in scale_strata:
            sub_s = s_fn(df_c)
            if len(sub_s) < 20:
                continue
            res_s = sim_mod.simulate_crop_stratum(sub_s, aez_code=0, seed=sim_mod.SEED, n_iter=sim_mod.N_ITER)
            if res_s is not None:
                t6_rows.extend(evaluate_stoplight(crop, s_name, res_s, hire_shock_mult=1.00))

    t6 = pd.DataFrame(t6_rows)
    t6.to_csv(OUT_T6_CSV, index=False)
    sim_mod.write_md(
        t6,
        "Table 6: Stoplight Sensitivity Scenarios (Baseline, +30% Fuel/Hire Shock, and Plot-Size Strata)",
        "NFI thresholds: Maize/Legumes (<0.6M, 0.6-1.2M, >1.2M), Paddy (<0.8M, 0.8-1.8M, >1.8M); Labor (<7k, 7k-12k, >12k TZS/day)",
        OUT_T6_MD,
    )
    np.savez_compressed(OUT_NPZ, **existing_npz)

    print(t6.to_string(index=False))
    print("================================================================================")


if __name__ == "__main__":
    main()
