#!/usr/bin/env python3
"""
paper_numbers.py
================
Extracts all empirical results dynamically from the Step 2-5 modeling outputs
(harmonized_mechanization_panel.parquet, ipwra_balanced_panel.parquet,
mve_simulation_draws.npz, and outputs/tables/table*.csv) and writes
`paper_numbers.json`.

Usage:
  .venv/bin/python paper_numbers.py
"""

import os
import json
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
TABLES_DIR = os.path.join(OUTPUTS_DIR, "tables")
DATA_DIR = os.path.join(OUTPUTS_DIR, "data")
OUT_JSON = os.path.join(BASE_DIR, "paper_numbers.json")


def _clean(val):
    if isinstance(val, (np.integer,)):
        return int(val)
    if isinstance(val, (np.floating,)):
        v = float(val)
        return None if np.isnan(v) else (0.0 if abs(v) < 1e-12 else v)
    if isinstance(val, (np.bool_,)):
        return bool(val)
    return val


def main():
    panel = pd.read_parquet(os.path.join(DATA_DIR, "harmonized_mechanization_panel.parquet"))
    bal = pd.read_parquet(os.path.join(DATA_DIR, "ipwra_balanced_panel.parquet"))
    t1 = pd.read_csv(os.path.join(TABLES_DIR, "table1_zonal_mechanization_distribution.csv"))
    t2 = pd.read_csv(os.path.join(TABLES_DIR, "table2_mechanization_transition_cagr.csv"))
    t3 = pd.read_csv(os.path.join(TABLES_DIR, "table3_model_validation_uve_mve.csv"))
    t4 = pd.read_csv(os.path.join(TABLES_DIR, "table4_stochastic_cost_decomposition.csv"))
    t5 = pd.read_csv(os.path.join(TABLES_DIR, "table5_nfi_labor_return_by_aez.csv"))
    t6 = pd.read_csv(os.path.join(TABLES_DIR, "table6_stoplight_sensitivity_scenarios.csv"))
    s1 = pd.read_csv(os.path.join(TABLES_DIR, "table_s1_covariate_balance_smd.csv"))

    # 1. Sample & Panel Overview
    nps_n = int(bal["wave"].str.startswith("NPS_").sum())
    aass_n = int(len(bal) - nps_n)
    s0 = pd.read_csv(os.path.join(TABLES_DIR, "table_s0_sample_attrition.csv"))
    mz_bal = bal[bal["crop_group"] == "Maize"]
    mz_pure = mz_bal[mz_bal["intercropped_flag"] == 0]
    mz_aez3_m0 = panel[(panel["crop_group"] == "Maize") & (panel["aez_code"] == 3) & (panel["regime"] == "M0")]
    mz_aez9_m0 = panel[(panel["crop_group"] == "Maize") & (panel["aez_code"] == 9) & (panel["regime"] == "M0")]
    paddy_m23_n = int(((bal["crop_group"] == "Paddy") & (bal["model_regime"] == "M2_M3")).sum())
    paddy_m0_n = int(((bal["crop_group"] == "Paddy") & (bal["model_regime"] == "M0")).sum())
    paddy_m1_n = int(((bal["crop_group"] == "Paddy") & (bal["model_regime"] == "M1")).sum())
    non_imp_w = panel.loc[(~panel["labor_cost_tzs_ha_imputed"]) & (~panel["person_days_ha_imputed"]) & (panel["person_days_ha"] > 0)]
    med_wage = float((non_imp_w["labor_cost_tzs_ha"] / non_imp_w["person_days_ha"]).median())
    overview = {
        "raw_plots": int(s0.iloc[0]["Plots_N"]),
        "total_harmonized_plots": int(len(panel)),
        "causal_retained_plots": int(len(bal)),
        "nps_causal_plots": nps_n,
        "aass_causal_plots": aass_n,
        "aass_causal_share_pct": round(100.0 * aass_n / len(bal), 1),
        "waves_count": int(panel["wave"].nunique()),
        "aez_count": 9,
        "multi_power_share_pct": round(100.0 * float(bal["multi_power_flag"].mean()), 2),
        "paddy_m0_retained_n": paddy_m0_n,
        "paddy_m1_retained_n": paddy_m1_n,
        "paddy_m23_retained_n": paddy_m23_n,
        "pure_stand_maize_raw_tha": round(float(mz_pure["yield_t_ha"].mean()), 3),
        "pure_stand_maize_norm_tha": round(float(mz_pure["yield_t_ha_normalized"].mean()), 3),
        "aez3_maize_m0_price": round(float(mz_aez3_m0["price_tzs_t"].mean()), 0),
        "aez9_maize_m0_price": round(float(mz_aez9_m0["price_tzs_t"].mean()), 0),
        "aez3_maize_m0_intercrop_pct": round(100.0 * float(mz_aez3_m0["intercropped_flag"].mean()), 1),
        "national_median_wage_tzs": round(med_wage, 0),
        "plots_by_crop": {k: int(v) for k, v in panel["crop_group"].value_counts().items()},
        "causal_plots_by_crop": {k: int(v) for k, v in bal["crop_group"].value_counts().items()},
    }

    # 2. Table 1 & Table 2: National & AEZ Transitions
    t1_nat_08 = t1[(t1["wave"] == "NPS W1 08/09") & (t1["aez_code"] == 0)].iloc[0]
    t1_nat_14 = t1[(t1["wave"] == "NPS W4 14/15") & (t1["aez_code"] == 0)].iloc[0]
    t1_nat_20 = t1[(t1["wave"] == "NPS W5 20/21") & (t1["aez_code"] == 0)].iloc[0]
    t1_nat_19 = t1[(t1["wave"] == "NCSA 2019/20") & (t1["aez_code"] == 0)].iloc[0]
    t1_nat_22 = t1[(t1["wave"] == "AASS 2022/23") & (t1["aez_code"] == 0)].iloc[0]
    t2_nat = t2[t2["aez_code"] == 0].iloc[0]

    aez_highlights = {}
    for _, row in t1[t1["wave"] == "NPS W5 20/21"].iterrows():
        ac = int(row["aez_code"])
        if ac == 0:
            continue
        t2_row = t2[t2["aez_code"] == ac].iloc[0]
        r22_row = t1[(t1["wave"] == "AASS 2022/23") & (t1["aez_code"] == ac)].iloc[0]
        aez_highlights[f"AEZ_{ac}"] = {
            "name": row["aez_name"],
            "M0_farm_2020_pct": _clean(row["M0_farm_share_pct"]),
            "M1_farm_2020_pct": _clean(row["M1_farm_share_pct"]),
            "M2_farm_2020_pct": _clean(row["M2_farm_share_pct"]),
            "M3_farm_2020_pct": _clean(row["M3_farm_share_pct"]),
            "M3_area_2020_pct": _clean(row["M3_area_share_pct"]),
            "M3_farm_2008_pct": _clean(t2_row["M3_2008_pct"]),
            "M3_farm_2022_pct": _clean(r22_row["M3_farm_share_pct"]),
            "M3_area_2022_pct": _clean(r22_row["M3_area_share_pct"]),
            "M1_farm_2022_pct": _clean(r22_row["M1_farm_share_pct"]),
            "CAGR_12yr_Tractor_pct": _clean(t2_row["CAGR_12yr_Tractor_pct"]),
            "CAGR_12yr_AnyMech_pct": _clean(t2_row["CAGR_12yr_AnyMech_pct"]),
        }

    transitions = {
        "national_2008": {
            "M0_farm_pct": _clean(t1_nat_08["M0_farm_share_pct"]),
            "M1_farm_pct": _clean(t1_nat_08["M1_farm_share_pct"]),
            "M3_farm_pct": _clean(t1_nat_08["M3_farm_share_pct"]),
            "M3_area_pct": _clean(t1_nat_08["M3_area_share_pct"]),
        },
        "national_2019_ncsa": {
            "M0_farm_pct": _clean(t1_nat_19["M0_farm_share_pct"]),
            "M1_farm_pct": _clean(t1_nat_19["M1_farm_share_pct"]),
            "M2_farm_pct": _clean(t1_nat_19["M2_farm_share_pct"]),
            "M3_farm_pct": _clean(t1_nat_19["M3_farm_share_pct"]),
        },
        "national_2020_nps5": {
            "M0_farm_pct": _clean(t1_nat_20["M0_farm_share_pct"]),
            "M0_area_pct": _clean(t1_nat_20["M0_area_share_pct"]),
            "M1_farm_pct": _clean(t1_nat_20["M1_farm_share_pct"]),
            "M2_farm_pct": _clean(t1_nat_20["M2_farm_share_pct"]),
            "M3_farm_pct": _clean(t1_nat_20["M3_farm_share_pct"]),
            "M3_area_pct": _clean(t1_nat_20["M3_area_share_pct"]),
        },
        "national_2022_aass": {
            "M0_farm_pct": _clean(t1_nat_22["M0_farm_share_pct"]),
            "M0_area_pct": _clean(t1_nat_22["M0_area_share_pct"]),
            "M1_farm_pct": _clean(t1_nat_22["M1_farm_share_pct"]),
            "M3_farm_pct": _clean(t1_nat_22["M3_farm_share_pct"]),
            "M3_area_pct": _clean(t1_nat_22["M3_area_share_pct"]),
        },
        "national_2014_nps4": {
            "M3_farm_pct": _clean(t1_nat_14["M3_farm_share_pct"]),
        },
        "national_total_mech_2008_pct": _clean(t2_nat["Total_Mech_2008_pct"]),
        "national_total_mech_2020_pct": _clean(t2_nat["Total_Mech_2020_pct"]),
        "national_cagr_12yr_tractor_pct": _clean(t2_nat["CAGR_12yr_Tractor_pct"]),
        "national_loglin_nps_tractor_cagr_pct": _clean(t2_nat["LogLinear_NPS_Tractor_CAGR_pct"]),
        "national_cagr_11yr_ncsa_tractor_pct": _clean(t2_nat["CAGR_11yr_NCSA_Tractor_pct"]),
        "national_cagr_12yr_anymech_pct": _clean(t2_nat["CAGR_12yr_AnyMech_pct"]),
        "aez": aez_highlights,
    }

    # 3. Table S1: Covariate Balance
    n_smd_total = int(len(s1))
    n_smd_pass = int(s1["balanced_lt_010"].sum())
    balance = {
        "total_comparisons": n_smd_total,
        "balanced_lt_010_count": n_smd_pass,
        "balanced_lt_010_pct": round(100.0 * n_smd_pass / n_smd_total, 1),
        "by_comparison": {
            f"{r['crop_group']}__{r['comparison']}": {
                "max_abs_smd": _clean(r["abs_post_smd"]),
                "neff_treated": _clean(r["neff_treated"]),
                "neff_control": _clean(r["neff_control"]),
            }
            for _, r in s1.sort_values("abs_post_smd", ascending=False).drop_duplicates(["crop_group", "comparison"]).iterrows()
        },
    }

    # 4. Table 3: Validation & Yields
    validation = {}
    for _, r in t3[t3["Series"] == "Stage2_MVE"].iterrows():
        key = f"{r['Crop']}__{r['Regime']}"
        validation[key] = {
            "mean_tha": _clean(r["Mean_tha"]),
            "sd_tha": _clean(r["SD_tha"]),
            "cv_pct": _clean(r["CV_pct"]),
            "ks_d": _clean(r["KS_D_vs_Obs"]),
            "ks_p": _clean(r["KS_p_value"]),
        }

    # Compute yield lifts vs M0
    for crop, reg in [("Maize", "M1"), ("Maize", "M2_M3"), ("Paddy", "M1"), ("Paddy", "M2_M3"), ("Legumes", "M1"), ("Legumes", "M2_M3")]:
        y0 = validation[f"{crop}__M0"]["mean_tha"]
        yr = validation[f"{crop}__{reg}"]["mean_tha"]
        validation[f"{crop}__{reg}"]["lift_vs_M0_pct"] = round(100.0 * (yr - y0) / y0, 1)

    # 5. Table 4: Costs
    costs = {}
    for _, r in t4.iterrows():
        key = f"{r['Crop']}__{r['Regime']}"
        costs[key] = {
            "mech_K_tzs_ha": _clean(r["Mech_Cost_K_TZS_ha"]),
            "mech_K_renters_tzs_ha": _clean(r["Mech_Cost_K_Renters_TZS_ha"]),
            "labor_L_tzs_ha": _clean(r["Labor_Cost_L_TZS_ha"]),
            "biochem_B_tzs_ha": _clean(r["Biochem_Cost_B_TZS_ha"]),
            "total_cost_tzs_ha": _clean(r["Total_Cost_TZS_ha"]),
            "person_days_ha": _clean(r["Person_Days_ha"]),
            "price_tzs_t": _clean(r["Price_P_TZS_t"]),
            "rho": _clean(r["Mech_to_Margin_Ratio_rho"]),
            "mech_share_rev_pct": _clean(r["Mech_Share_GrossRev_pct"]),
        }

    # 6. Table 5: NFI & Return to Labor (National & AEZs)
    nfi_national = {}
    for _, r in t5[t5["AEZ_Code"] == 0].iterrows():
        key = f"{r['Crop']}__{r['Regime']}"
        nfi_national[key] = {
            "nfi_mean": _clean(r["NFI_Mean_TZS_ha"]),
            "nfi_median": _clean(r["NFI_Median_TZS_ha"]),
            "nfi_cv_pct": _clean(r["NFI_CV_pct"]),
            "return_to_labor": _clean(r["Return_to_Labor_TZS_day"]),
            "return_to_labor_median": _clean(r["Return_to_Labor_Median_TZS_day"]),
        }

    nfi_aez = {}
    for _, r in t5[t5["AEZ_Code"] > 0].iterrows():
        key = f"{r['Crop']}__AEZ_{int(r['AEZ_Code'])}__{r['Regime']}"
        nfi_aez[key] = {
            "aez_name": r["AEZ_Name"],
            "n_plots": _clean(r["n_plots"]),
            "neff": _clean(r["N_eff"]),
            "insufficient_support": _clean(r["Insufficient_Support"]),
            "nfi_mean": _clean(r["NFI_Mean_TZS_ha"]),
            "nfi_median": _clean(r["NFI_Median_TZS_ha"]),
            "return_to_labor": _clean(r["Return_to_Labor_TZS_day"]),
            "return_to_labor_median": _clean(r["Return_to_Labor_Median_TZS_day"]),
            "borrowed_s_dev": _clean(r["Borrowed_S_dev"]),
        }

    # 7. Table 6: Stoplight & Sensitivity Scenarios
    stoplight = {}
    for _, r in t6.iterrows():
        key = f"{r['Crop']}__{r['Scenario']}__{r['Regime']}"
        stoplight[key] = {
            "nfi_mean": _clean(r["NFI_Mean_TZS_ha"]),
            "nfi_median": _clean(r["NFI_Median_TZS_ha"]),
            "nfi_red_pct": _clean(r["NFI_Red_pct"]),
            "nfi_yellow_pct": _clean(r["NFI_Yellow_pct"]),
            "nfi_green_pct": _clean(r["NFI_Green_pct"]),
            "labor_mean": _clean(r["Labor_Mean_TZS_day"]),
            "labor_median": _clean(r["Labor_Median_TZS_day"]),
            "labor_red_pct": _clean(r["Labor_Red_pct"]),
            "labor_yellow_pct": _clean(r["Labor_Yellow_pct"]),
            "labor_green_pct": _clean(r["Labor_Green_pct"]),
        }

    # 8. Causal ATE/ATT, Mediation/GPS Checks, and Paddy 2WT Descriptive
    ate_df = pd.read_csv(os.path.join(TABLES_DIR, "table_ate_att_causal_effects.csv"))
    ate_att = {}
    for _, r in ate_df.iterrows():
        key = f"{r['crop_group']}__{r['outcome']}__{r['contrast']}"
        ate_att[key] = {
            "ate": _clean(r["ate"]),
            "ate_se": _clean(r["ate_se_boot"]),
            "ate_ci95_low": _clean(r["ate_ci95_low"]),
            "ate_ci95_high": _clean(r["ate_ci95_high"]),
            "att": _clean(r["att"]),
            "att_se": _clean(r["att_se_boot"]),
            "n_hh_clusters": _clean(r["n_hh_clusters"]),
        }

    chk_df = pd.read_csv(os.path.join(TABLES_DIR, "table_s4_mediation_and_gps_checks.csv"))
    checks = chk_df.to_dict(orient="records")
    checks_by_key = {}
    for c in checks:
        for k in list(c.keys()):
            c[k] = _clean(c[k])
        ckey = f"{c['check_type']}__{c['crop_group']}__{c['stratum']}__{c['contrast']}"
        checks_by_key[ckey] = c

    wgm_df = pd.read_csv(os.path.join(TABLES_DIR, "table_s4b_wage_and_gross_margin.csv"))
    wage_gm = {}
    for _, r in wgm_df.iterrows():
        wkey = f"{r['crop_group']}__{r['regime']}"
        wage_gm[wkey] = {
            "cash_gm": _clean(r["cash_gross_margin_tzs_ha"]),
            "econ_nfi_base": _clean(r["econ_nfi_base_tzs_ha"]),
            "econ_nfi_5000": _clean(r["econ_nfi_5000_tzs_ha"]),
            "ate_5000": _clean(r["ate_m23_vs_m0_5000_tzs_ha"]),
        }

    p2_df = pd.read_csv(os.path.join(TABLES_DIR, "table_s3_paddy_2wt_descriptive.csv"))
    paddy_2wt = {
        r["regime"]: {
            "n_plots": _clean(r["n_plots"]),
            "yield_t_ha": _clean(r["weighted_yield_t_ha"]),
            "mech_cost_tzs_ha": _clean(r["weighted_mech_cost_tzs_ha"]),
            "person_days_ha": _clean(r["weighted_person_days_ha"]),
            "irrigated_pct": _clean(r["weighted_irrigated_pct"]),
        }
        for _, r in p2_df.iterrows()
    }
    overview["paddy_m2_share_of_m23_pct"] = round(100.0 * paddy_2wt["M2"]["n_plots"] / max(overview["paddy_m23_retained_n"], 1), 1)

    nfi_lifts = {}
    for crop in ("Maize", "Paddy", "Legumes"):
        m0_v = nfi_national[f"{crop}__M0"]["nfi_mean"]
        m23_v = nfi_national[f"{crop}__M2_M3"]["nfi_mean"]
        nfi_lifts[f"{crop}__M2_M3_vs_M0_pct"] = round(100.0 * (m23_v - m0_v) / abs(m0_v), 1) if m0_v != 0 else 0.0

    m23_rev_shares = [costs[f"{c}__M2_M3"]["mech_share_rev_pct"] for c in ("Maize", "Paddy", "Legumes")]
    costs["m23_mech_rev_min_pct"] = min(m23_rev_shares)
    costs["m23_mech_rev_max_pct"] = max(m23_rev_shares)

    payload = {
        "overview": overview,
        "transitions": transitions,
        "balance": balance,
        "validation": validation,
        "costs": costs,
        "nfi_national": nfi_national,
        "nfi_lifts": nfi_lifts,
        "nfi_aez": nfi_aez,
        "stoplight": stoplight,
        "ate_att": ate_att,
        "checks": checks,
        "checks_by_key": checks_by_key,
        "wage_gm": wage_gm,
        "paddy_2wt_descriptive": paddy_2wt,
    }

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"[SUCCESS] Wrote {OUT_JSON} dynamically from modeling outputs.")


if __name__ == "__main__":
    main()
