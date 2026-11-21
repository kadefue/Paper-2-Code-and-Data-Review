#!/usr/bin/env python3
"""
src/03_ipwra_balance.py
=========================
Step 3 of Study 2: Multinomial Generalized Propensity Score (GPS) Estimation,
Entropy-Calibrated Stabilized IPW Weighting, Common Support Trimming,
Covariate Balance (|SMD| < 0.10), and IPWRA Potential Outcomes & Costs.

Reads:
  - outputs/data/harmonized_mechanization_panel.parquet

Exports:
  - outputs/data/ipwra_balanced_panel.parquet
  - outputs/tables/table_s1_covariate_balance_smd.csv & .md

Usage:
  .venv/bin/python src/03_ipwra_balance.py
"""

import os
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.preprocessing import StandardScaler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
IN_PARQUET = os.path.join(OUTPUTS_DIR, "data", "harmonized_mechanization_panel.parquet")
OUT_PARQUET = os.path.join(OUTPUTS_DIR, "data", "ipwra_balanced_panel.parquet")
OUT_SMD_CSV = os.path.join(OUTPUTS_DIR, "tables", "table_s1_covariate_balance_smd.csv")
OUT_SMD_MD = os.path.join(OUTPUTS_DIR, "tables", "table_s1_covariate_balance_smd.md")
OUT_ATE_CSV = os.path.join(OUTPUTS_DIR, "tables", "table_ate_att_causal_effects.csv")
OUT_ATE_MD = os.path.join(OUTPUTS_DIR, "tables", "table_ate_att_causal_effects.md")
OUT_PADDY_2WT_CSV = os.path.join(OUTPUTS_DIR, "tables", "table_s3_paddy_2wt_descriptive.csv")
OUT_CHECKS_CSV = os.path.join(OUTPUTS_DIR, "tables", "table_s4_mediation_and_gps_checks.csv")
OUT_WAGE_GM_CSV = os.path.join(OUTPUTS_DIR, "tables", "table_s4b_wage_and_gross_margin.csv")
OUT_BAL_EXTRA_CSV = os.path.join(OUTPUTS_DIR, "tables", "table_s1b_balance_diagnostics_extra.csv")

# Removed draught_livestock_count (separation with M1) and redundant soil_type (collinear with intercropped_flag)
BASE_COVARIATES = [
    "log_plot_size_ha",
    "log_total_farm_size_ha",
    "hh_head_age",
    "hh_head_sex",
    "hh_head_edu",
    "hh_size",
    "asset_index",
    "credit_access",
    "extension_contact",
    "erosion_or_slope_flag",
    "irrigated_flag",
    "intercropped_flag",
    "dist_road_market_km",
]


def w_mean_std(x, w):
    """Computes weighted mean and weighted standard deviation."""
    mask = pd.notna(x) & pd.notna(w) & (w > 0)
    if not mask.any():
        return np.nan, np.nan
    xv = np.asarray(x[mask], dtype=float)
    wv = np.asarray(w[mask], dtype=float)
    mu = np.average(xv, weights=wv)
    var = np.average((xv - mu) ** 2, weights=wv)
    return float(mu), float(np.sqrt(max(var, 1e-12)))


def compute_smd(df, cov_cols, treat_regime, ref_regime="M0", weight_col="weight"):
    """Computes Standardized Mean Difference (treat_regime vs ref_regime)."""
    sub_t = df[df["model_regime"] == treat_regime]
    sub_0 = df[df["model_regime"] == ref_regime]
    smds = {}
    for col in cov_cols:
        mu_t, sd_t = w_mean_std(sub_t[col], sub_t[weight_col])
        mu_0, sd_0 = w_mean_std(sub_0[col], sub_0[weight_col])
        denom = np.sqrt(0.5 * (sd_t ** 2 + sd_0 ** 2))
        smds[col] = (mu_t - mu_0) / denom if (pd.notna(denom) and denom > 1e-9) else 0.0
    return smds


def kish_neff(w):
    """Computes Kish effective sample size."""
    wv = np.asarray(w, dtype=float)
    wv = wv[wv > 0]
    if len(wv) == 0:
        return 0.0
    return float((wv.sum() ** 2) / np.sum(wv ** 2))


def prepare_design_matrix(df):
    """Imputes residual covariate NaNs with crop-level median and adds AEZ + wave FEs."""
    X_num = df[BASE_COVARIATES].copy()
    for c in BASE_COVARIATES:
        med = X_num[c].median()
        X_num[c] = pd.to_numeric(X_num[c], errors="coerce").fillna(med if pd.notna(med) else 0.0)

    aez_dummies = pd.get_dummies(df["aez_code"].astype("Int64").astype(str), prefix="aez", drop_first=True, dtype=float)
    if df["wave"].nunique() > 1:
        wave_dummies = pd.get_dummies(df["wave"], prefix="wave", drop_first=True, dtype=float)
        X_full = pd.concat([X_num, aez_dummies, wave_dummies], axis=1)
    else:
        X_full = pd.concat([X_num, aez_dummies], axis=1)
    return X_full


def entropy_calibrate_weights(Z_sub, q_base, target_mean, l2_reg=1e-4):
    """
    Hainmueller (2012) entropy balancing: finds exponential tilt weights
    w_i = q_base_i * exp(-lambda @ Z_i) normalized to sum(q_base)
    such that weighted mean of Z_sub matches target_mean.
    """
    Z = np.asarray(Z_sub, dtype=float)
    q = np.asarray(q_base, dtype=float)
    q_norm = q / np.sum(q)
    dZ = Z - target_mean[None, :]

    # Drop zero-variance columns to keep Hessian well-conditioned
    col_std = np.std(dZ, axis=0)
    keep = col_std > 1e-8
    if not keep.any():
        return q
    dZ = dZ[:, keep]

    def dual_obj_grad(lam):
        arg = np.clip(-dZ @ lam, -30.0, 30.0)
        w_unnorm = q_norm * np.exp(arg)
        z_sum = np.sum(w_unnorm)
        obj = np.log(max(z_sum, 1e-15)) + l2_reg * np.sum(lam ** 2)
        grad = -(w_unnorm @ dZ) / max(z_sum, 1e-15) + 2.0 * l2_reg * lam
        return obj, grad

    res = minimize(dual_obj_grad, np.zeros(dZ.shape[1]), jac=True, method="BFGS", options={"maxiter": 500})
    arg = np.clip(-dZ @ res.x, -30.0, 30.0)
    w_cal = q_norm * np.exp(arg)
    w_cal = w_cal / np.sum(w_cal) * np.sum(q)
    return w_cal


def fit_crop_ipwra(df_crop):
    """
    Fits multinomial GPS, trims [0.02, 0.98], applies entropy calibration on
    stabilized IPW weights, caps at 99th percentile, computes IPWRA potential
    yields and costs, and returns SMD diagnostics.
    """
    df = df_crop.copy().reset_index(drop=True)
    crop_name = df["crop_group"].iloc[0]

    # Cap extreme survey weights within each wave at 99th percentile to prevent N_eff collapse
    w_cap_wave = df.groupby("wave")["weight"].transform(lambda s: s.quantile(0.99))
    df["weight"] = np.minimum(df["weight"], w_cap_wave)

    # Pool M2 with M3 (M2_M3) across all crops for robust causal support;
    # Paddy M2 (2WT) plots are reported separately in descriptive Table S3.
    df["gps_regime"] = df["regime"].replace({"M2": "M2_M3", "M3": "M2_M3"})
    df["model_regime"] = df["gps_regime"]

    gps_classes = sorted(df["gps_regime"].unique())
    regimes_present = sorted(df["model_regime"].unique())
    X_full = prepare_design_matrix(df)
    X_scaled = StandardScaler().fit_transform(X_full)

    # Multinomial logit GPS on {M0, M1, M2_M3}
    clf = LogisticRegression(max_iter=2000, C=10.0)
    clf.fit(X_scaled, df["gps_regime"])
    probs = clf.predict_proba(X_scaled)
    class_to_idx = {c: i for i, c in enumerate(clf.classes_)}

    w_tot = df["weight"].sum()
    p_marg = {c: df.loc[df["gps_regime"] == c, "weight"].sum() / w_tot for c in gps_classes}

    df["gps_assigned"] = np.array([probs[i, class_to_idx[r]] for i, r in enumerate(df["gps_regime"])])
    for c in gps_classes:
        df[f"gps_{c}"] = probs[:, class_to_idx[c]]
    df["common_support_keep"] = (df["gps_assigned"] >= 0.02) & (df["gps_assigned"] <= 0.98)

    df_trim = df[df["common_support_keep"]].copy().reset_index(drop=True)
    raw_ipw = (
        np.array([p_marg[r] for r in df_trim["gps_regime"]])
        / np.clip(df_trim["gps_assigned"].to_numpy(), 0.02, 0.98)
    ) * df_trim["weight"].to_numpy()

    # Entropy calibration within each model_regime (including small M2 stratum)
    X_trim = prepare_design_matrix(df_trim)
    Z_bal = StandardScaler().fit_transform(X_trim[BASE_COVARIATES])
    target_mean = np.average(Z_bal, axis=0, weights=df_trim["weight"].to_numpy())

    cal_ipw = raw_ipw.copy()
    for r in regimes_present:
        mask = (df_trim["model_regime"] == r).to_numpy()
        if mask.sum() >= 15:
            # Stronger L2 regularization on small cells (e.g., Paddy M2) preserves N_eff
            reg_val = 0.05 if mask.sum() < 100 else 1e-4
            base_q = np.ones(mask.sum()) if mask.sum() < 100 else raw_ipw[mask]
            cal_ipw[mask] = entropy_calibrate_weights(Z_bal[mask], base_q, target_mean, l2_reg=reg_val)
            cap_99 = np.quantile(cal_ipw[mask], 0.99)
            cal_ipw[mask] = np.clip(cal_ipw[mask], 0.0, cap_99)

    df_trim["ipw_weight"] = cal_ipw

    # IPWRA outcome & cost regressions per regime
    X_trim_scaled = StandardScaler().fit_transform(X_trim)
    df_trim["ipwra_yield_hat"] = np.nan
    df_trim["ipwra_mech_cost_hat"] = np.nan
    df_trim["ipwra_labor_cost_hat"] = np.nan
    df_trim["ipwra_biochem_cost_hat"] = np.nan

    outcome_targets = [
        ("yield_t_ha", "ipwra_yield_hat"),
        ("mech_cost_tzs_ha", "ipwra_mech_cost_hat"),
        ("labor_cost_tzs_ha", "ipwra_labor_cost_hat"),
        ("biochem_cost_tzs_ha", "ipwra_biochem_cost_hat"),
    ]
    for r in regimes_present:
        r_mask = (df_trim["model_regime"] == r)
        for src_col, dst_col in outcome_targets:
            fit_mask = r_mask & df_trim[src_col].notna()
            if fit_mask.sum() < 10:
                continue
            reg = Ridge(alpha=1.0)
            reg.fit(X_trim_scaled[fit_mask], df_trim.loc[fit_mask, src_col], sample_weight=df_trim.loc[fit_mask, "ipw_weight"])
            preds = np.clip(reg.predict(X_trim_scaled), 0.0, None)
            df_trim[f"{src_col}_hat_{r}"] = preds
            df_trim.loc[r_mask, dst_col] = preds[r_mask]

    # SMD diagnostics (Pre vs Post IPW) for M1 vs M0, M2_M3 vs M0, and M2_M3 vs M1
    smd_rows = []
    crop_name = df["crop_group"].iloc[0]
    pairs = [(r, "M0") for r in regimes_present if r != "M0"]
    if "M2_M3" in regimes_present and "M1" in regimes_present:
        pairs.append(("M2_M3", "M1"))
    for r, ref in pairs:
        pre = compute_smd(df, BASE_COVARIATES, r, ref, "weight")
        post = compute_smd(df_trim, BASE_COVARIATES, r, ref, "ipw_weight")
        n_raw_r = int((df_trim["model_regime"] == r).sum())
        n_raw_ref = int((df_trim["model_regime"] == ref).sum())
        neff_r = kish_neff(df_trim.loc[df_trim["model_regime"] == r, "ipw_weight"])
        neff_ref = kish_neff(df_trim.loc[df_trim["model_regime"] == ref, "ipw_weight"])
        for cov in BASE_COVARIATES:
            smd_rows.append({
                "crop_group": crop_name,
                "comparison": f"{r}_vs_{ref}",
                "covariate": cov,
                "pre_ipw_smd": round(pre[cov], 4),
                "post_ipw_smd": round(post[cov], 4),
                "abs_post_smd": round(abs(post[cov]), 4),
                "balanced_lt_010": abs(post[cov]) < 0.10,
                "n_raw_treated": n_raw_r,
                "n_raw_control": n_raw_ref,
                "neff_treated": round(neff_r, 1),
                "neff_control": round(neff_ref, 1),
            })

    return df_trim, smd_rows


def write_smd_markdown(smd_df, path):
    """Writes Table S1 Covariate Balance SMD report."""
    lines = [
        "# Table S1: Pre- vs. Post-IPWRA Covariate Balance (Standardized Mean Differences)",
        "*Common support trimmed to [0.02, 0.98]; entropy-calibrated stabilized IPW weights capped at 99th percentile.*\n",
        "| Crop | Comparison | Covariate | Pre-IPW SMD | Post-IPW SMD | |Post SMD| < 0.10 | N_eff (Treated) | N_eff (M0) |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for _, r in smd_df.iterrows():
        lines.append(
            f"| {r['crop_group']} | {r['comparison']} | `{r['covariate']}` | "
            f"{r['pre_ipw_smd']:.4f} | {r['post_ipw_smd']:.4f} | "
            f"{'PASS' if r['balanced_lt_010'] else 'WARN'} | {r['neff_treated']:.1f} | {r['neff_control']:.1f} |"
        )
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def compute_dr_ate_att(df_crop, X_mat, outcome_col, r1, r0, alpha=10.0):
    """Doubly robust IPWRA ATE and ATT for contrast r1 vs r0."""
    y = pd.to_numeric(df_crop[outcome_col], errors="coerce").to_numpy(dtype=float)
    w_ipw = df_crop["ipw_weight"].to_numpy(dtype=float)
    w_srv = df_crop["weight"].to_numpy(dtype=float)
    reg = df_crop["model_regime"].to_numpy()

    valid = np.isfinite(y) & np.isfinite(w_ipw) & (w_ipw > 0)
    if (reg[valid] == r1).sum() < 10 or (reg[valid] == r0).sum() < 10:
        return np.nan, np.nan

    # Fit weighted Ridge outcome models on r1 and r0
    m1_mask = valid & (reg == r1)
    m0_mask = valid & (reg == r0)
    mod1 = Ridge(alpha=alpha).fit(X_mat[m1_mask], y[m1_mask], sample_weight=w_ipw[m1_mask])
    mod0 = Ridge(alpha=alpha).fit(X_mat[m0_mask], y[m0_mask], sample_weight=w_ipw[m0_mask])
    mu1 = mod1.predict(X_mat[valid])
    mu0 = mod0.predict(X_mat[valid])

    y_v = y[valid]
    w_v = w_ipw[valid]
    ws_v = w_srv[valid]
    r_v = reg[valid]

    # Doubly robust ATE
    ind1 = (r_v == r1).astype(float)
    ind0 = (r_v == r0).astype(float)
    aug1 = np.sum(w_v * ind1 * (y_v - mu1)) / max(np.sum(w_v * ind1), 1e-12)
    aug0 = np.sum(w_v * ind0 * (y_v - mu0)) / max(np.sum(w_v * ind0), 1e-12)
    ate = float(np.average(mu1 - mu0, weights=ws_v) + aug1 - aug0)

    # ATT evaluated on treated (r1)
    t_mask = r_v == r1
    att_aug0 = np.sum(w_v[r_v == r0] * (y_v[r_v == r0] - mu0[r_v == r0])) / max(np.sum(w_v[r_v == r0]), 1e-12)
    att = float(np.average(y_v[t_mask] - mu0[t_mask], weights=ws_v[t_mask]) - att_aug0)
    return ate, att


def _boot_ate_se(sub_df, X_mat, outcome_col, r1, r0, rng, n_boot=250, alpha=10.0):
    """Computes household-clustered bootstrap SE and 95% CI for DR ATE."""
    ate_pt, _ = compute_dr_ate_att(sub_df, X_mat, outcome_col, r1, r0, alpha=alpha)
    if not np.isfinite(ate_pt):
        return np.nan, np.nan, np.nan, np.nan
    hh_ids = sub_df["hh_id"].astype(str).to_numpy()
    uniq_hh, inv = np.unique(hh_ids, return_inverse=True)
    hh_groups = [np.where(inv == idx)[0] for idx in range(len(uniq_hh))]
    n_hh = len(hh_groups)
    boot_vals = []
    for _ in range(n_boot):
        sel_hh = rng.integers(0, n_hh, size=n_hh)
        idx = np.concatenate([hh_groups[h] for h in sel_hh])
        b_ate, _ = compute_dr_ate_att(sub_df.iloc[idx], X_mat[idx], outcome_col, r1, r0, alpha=alpha)
        if np.isfinite(b_ate):
            boot_vals.append(b_ate)
    se = float(np.std(boot_vals, ddof=1)) if len(boot_vals) > 5 else np.nan
    ci_lo = ate_pt - 1.96 * se if np.isfinite(se) else np.nan
    ci_hi = ate_pt + 1.96 * se if np.isfinite(se) else np.nan
    return ate_pt, se, ci_lo, ci_hi


def estimate_ate_att_and_checks(balanced_df, causal_raw_df, n_boot=500):
    """
    Computes household-clustered bootstrap (n_boot=500) IPWRA ATE & ATT,
    biochemical (B) mediation sensitivity, GPS-area subsample check, and
    Paddy 2WT (M2) descriptive summary.
    """
    df = balanced_df.copy()
    pdays = np.clip(pd.to_numeric(df["person_days_ha"], errors="coerce").to_numpy(dtype=float), 15.0, 160.0)
    # Use common crop-AEZ IPW-weighted mean prices and median daily wages across regimes
    # (matching Stage 2 simulation) so Table 3a/S4b/Table 5 share the exact same price anchor
    df["_obs_wage"] = np.where(pdays > 0, df["labor_cost_tzs_ha"] / pdays, np.nan).clip(1500.0, 4000.0)
    aez_p_map = {}
    for (c_g, a_c), grp in df.groupby(["crop_group", "aez_code"]):
        vp = grp["price_tzs_t"].notna() & grp["ipw_weight"].notna() & (grp["ipw_weight"] > 0)
        if vp.any():
            aez_p_map[(c_g, a_c)] = float(np.average(grp.loc[vp, "price_tzs_t"], weights=grp.loc[vp, "ipw_weight"]))
    crop_p_map = {}
    for c_g, grp in df.groupby("crop_group"):
        vp = grp["price_tzs_t"].notna() & grp["ipw_weight"].notna() & (grp["ipw_weight"] > 0)
        crop_p_map[c_g] = float(np.average(grp.loc[vp, "price_tzs_t"], weights=grp.loc[vp, "ipw_weight"])) if vp.any() else float(grp["price_tzs_t"].median())
    aez_price = pd.Series([aez_p_map.get((c_g, a_c), crop_p_map.get(c_g, 0.0)) for c_g, a_c in zip(df["crop_group"], df["aez_code"])], index=df.index)
    aez_wage = df.groupby(["crop_group", "aez_code"])["_obs_wage"].transform("median").fillna(1528.0).clip(1500.0, 4000.0)
    gross = df["yield_t_ha"].to_numpy(dtype=float) * aez_price.to_numpy(dtype=float)
    k_cost = df["mech_cost_tzs_ha"].to_numpy(dtype=float)
    l_cost = aez_wage.to_numpy(dtype=float) * pdays
    b_cost = df["biochem_cost_tzs_ha"].to_numpy(dtype=float)
    df["nfi_tzs_ha"] = gross - (k_cost + l_cost + b_cost)
    df["nfi_w5000_tzs_ha"] = gross - (k_cost + 5000.0 * pdays + b_cost)
    df["return_to_labor"] = (gross - k_cost - b_cost) / pdays

    rng = np.random.default_rng(42)
    ate_rows = []
    check_rows = []

    contrasts = [("M1", "M0", "M1 vs. M0"), ("M2_M3", "M0", "M2/M3 vs. M0"), ("M2_M3", "M1", "M2/M3 vs. M1")]
    outcomes = [
        ("yield_t_ha", "Yield (t/ha)"),
        ("nfi_tzs_ha", "Net Farm Income (TZS/ha)"),
        ("return_to_labor", "Return to Labor (TZS/person-day)"),
    ]

    for crop in ("Maize", "Paddy", "Legumes"):
        sub = df[df["crop_group"] == crop].copy().reset_index(drop=True)
        if sub.empty:
            continue
        X_sub = StandardScaler().fit_transform(prepare_design_matrix(sub))

        # Precompute HH cluster indices for fast clustered bootstrap
        hh_ids = sub["hh_id"].astype(str).to_numpy()
        uniq_hh, inv = np.unique(hh_ids, return_inverse=True)
        hh_groups = [np.where(inv == idx)[0] for idx in range(len(uniq_hh))]
        n_hh = len(hh_groups)

        for out_col, out_lbl in outcomes:
            for r1, r0, c_lbl in contrasts:
                ate_pt, att_pt = compute_dr_ate_att(sub, X_sub, out_col, r1, r0)
                boot_ate = []
                boot_att = []
                for _ in range(n_boot):
                    sel_hh = rng.integers(0, n_hh, size=n_hh)
                    idx = np.concatenate([hh_groups[h] for h in sel_hh])
                    b_ate, b_att = compute_dr_ate_att(sub.iloc[idx], X_sub[idx], out_col, r1, r0)
                    if np.isfinite(b_ate):
                        boot_ate.append(b_ate)
                    if np.isfinite(b_att):
                        boot_att.append(b_att)
                se_ate = float(np.std(boot_ate, ddof=1)) if len(boot_ate) > 5 else np.nan
                se_att = float(np.std(boot_att, ddof=1)) if len(boot_att) > 5 else np.nan
                ate_rows.append({
                    "crop_group": crop,
                    "outcome": out_lbl,
                    "contrast": c_lbl,
                    "ate": round(ate_pt, 4) if np.isfinite(ate_pt) else np.nan,
                    "ate_se_boot": round(se_ate, 4) if np.isfinite(se_ate) else np.nan,
                    "ate_ci95_low": round(ate_pt - 1.96 * se_ate, 4) if np.isfinite(se_ate) else np.nan,
                    "ate_ci95_high": round(ate_pt + 1.96 * se_ate, 4) if np.isfinite(se_ate) else np.nan,
                    "att": round(att_pt, 4) if np.isfinite(att_pt) else np.nan,
                    "att_se_boot": round(se_att, 4) if np.isfinite(se_att) else np.nan,
                    "att_ci95_low": round(att_pt - 1.96 * se_att, 4) if np.isfinite(se_att) else np.nan,
                    "att_ci95_high": round(att_pt + 1.96 * se_att, 4) if np.isfinite(se_att) else np.nan,
                    "n_hh_clusters": n_hh,
                })

        # B-mediation sensitivity check on Yield
        b_log = np.log1p(np.clip(pd.to_numeric(sub["biochem_cost_tzs_ha"], errors="coerce").fillna(0.0).to_numpy(), 0.0, None)).reshape(-1, 1)
        b_scaled = StandardScaler().fit_transform(b_log)
        X_med = np.hstack([X_sub, b_scaled])
        for r1, r0, c_lbl in [("M1", "M0", "M1 vs. M0"), ("M2_M3", "M0", "M2/M3 vs. M0")]:
            tot_ate, tot_se, tot_lo, tot_hi = _boot_ate_se(sub, X_sub, "yield_t_ha", r1, r0, rng, n_boot=250)
            cde_ate, _ = compute_dr_ate_att(sub, X_med, "yield_t_ha", r1, r0)
            atten_pct = 100.0 * (tot_ate - cde_ate) / tot_ate if (np.isfinite(tot_ate) and abs(tot_ate) > 1e-6) else np.nan
            check_rows.append({
                "check_type": "B_Mediation_CDE",
                "crop_group": crop,
                "stratum": "All Balanced Plots",
                "contrast": c_lbl,
                "n_plots": len(sub),
                "total_ate_t_ha": round(tot_ate, 4),
                "ate_se_boot": round(tot_se, 4) if np.isfinite(tot_se) else np.nan,
                "ate_ci95_low": round(tot_lo, 4) if np.isfinite(tot_lo) else np.nan,
                "ate_ci95_high": round(tot_hi, 4) if np.isfinite(tot_hi) else np.nan,
                "cde_ate_t_ha": round(cde_ate, 4),
                "attenuation_pct": round(atten_pct, 2) if np.isfinite(atten_pct) else np.nan,
            })

        # GPS-measured plot-area-only subsample check (NPS GPS area)
        gps_sub = sub[sub["is_gps_area"] == 1.0].copy().reset_index(drop=True)
        if len(gps_sub) >= 100:
            for s_lbl, s_mask in [
                ("GPS Plots (< 1.0 ha)", gps_sub["planted_ha"] < 1.0),
                ("GPS Plots (> 3.0 ha)", gps_sub["planted_ha"] > 3.0),
                ("All GPS Plots", pd.Series(True, index=gps_sub.index)),
            ]:
                gsub = gps_sub[s_mask].copy().reset_index(drop=True)
                if len(gsub) < 50:
                    continue
                Xg = StandardScaler().fit_transform(prepare_design_matrix(gsub))
                for r1, r0, c_lbl in [("M1", "M0", "M1 vs. M0"), ("M2_M3", "M0", "M2/M3 vs. M0")]:
                    g_ate, g_se, g_lo, g_hi = _boot_ate_se(gsub, Xg, "yield_t_ha", r1, r0, rng, n_boot=250)
                    if np.isfinite(g_ate):
                        check_rows.append({
                            "check_type": "GPS_Area_Subsample",
                            "crop_group": crop,
                            "stratum": s_lbl,
                            "contrast": c_lbl,
                            "n_plots": len(gsub),
                            "total_ate_t_ha": round(g_ate, 4),
                            "ate_se_boot": round(g_se, 4) if np.isfinite(g_se) else np.nan,
                            "ate_ci95_low": round(g_lo, 4) if np.isfinite(g_lo) else np.nan,
                            "ate_ci95_high": round(g_hi, 4) if np.isfinite(g_hi) else np.nan,
                            "cde_ate_t_ha": np.nan,
                            "attenuation_pct": np.nan,
                        })

        # WLS (alpha ~ 0) vs Ridge (alpha = 10.0) comparison
        for r1, r0, c_lbl in [("M1", "M0", "M1 vs. M0"), ("M2_M3", "M0", "M2/M3 vs. M0")]:
            ridge_ate, r_se, r_lo, r_hi = _boot_ate_se(sub, X_sub, "yield_t_ha", r1, r0, rng, n_boot=250, alpha=10.0)
            wls_ate, _ = compute_dr_ate_att(sub, X_sub, "yield_t_ha", r1, r0, alpha=1e-6)
            check_rows.append({
                "check_type": "WLS_vs_Ridge",
                "crop_group": crop,
                "stratum": "All Balanced Plots (alpha=1e-6 vs 10)",
                "contrast": c_lbl,
                "n_plots": len(sub),
                "total_ate_t_ha": round(ridge_ate, 4),
                "ate_se_boot": round(r_se, 4) if np.isfinite(r_se) else np.nan,
                "ate_ci95_low": round(r_lo, 4) if np.isfinite(r_lo) else np.nan,
                "ate_ci95_high": round(r_hi, 4) if np.isfinite(r_hi) else np.nan,
                "cde_ate_t_ha": round(wls_ate, 4),
                "attenuation_pct": np.nan,
            })

        # Tighter GPS trimming [0.05, 0.95] sensitivity check for weight-concentration robustness
        trim05_sub = sub[(sub["gps_assigned"] >= 0.05) & (sub["gps_assigned"] <= 0.95)].copy().reset_index(drop=True)
        if len(trim05_sub) >= 100:
            Xt05 = StandardScaler().fit_transform(prepare_design_matrix(trim05_sub))
            for r1, r0, c_lbl in [("M1", "M0", "M1 vs. M0"), ("M2_M3", "M0", "M2/M3 vs. M0")]:
                t05_ate, t05_se, t05_lo, t05_hi = _boot_ate_se(trim05_sub, Xt05, "yield_t_ha", r1, r0, rng, n_boot=250)
                if np.isfinite(t05_ate):
                    check_rows.append({
                        "check_type": "Tighter_GPS_Trim_005_095",
                        "crop_group": crop,
                        "stratum": "Trimmed [0.05, 0.95]",
                        "contrast": c_lbl,
                        "n_plots": len(trim05_sub),
                        "total_ate_t_ha": round(t05_ate, 4),
                        "ate_se_boot": round(t05_se, 4) if np.isfinite(t05_se) else np.nan,
                        "ate_ci95_low": round(t05_lo, 4) if np.isfinite(t05_lo) else np.nan,
                        "ate_ci95_high": round(t05_hi, 4) if np.isfinite(t05_hi) else np.nan,
                        "cde_ate_t_ha": np.nan,
                        "attenuation_pct": np.nan,
                    })

        # NPS-only subsample (owned + rented implements consistently observed) & Mundlak CRE check
        nps_sub = sub[sub["wave"].str.startswith("NPS_")].copy().reset_index(drop=True)
        if len(nps_sub) >= 100:
            Xn = StandardScaler().fit_transform(prepare_design_matrix(nps_sub))
            hh_cov_cols = ["log_plot_size_ha", "log_total_farm_size_ha", "asset_index", "credit_access", "extension_contact"]
            hh_means = nps_sub.groupby("hh_id")[hh_cov_cols].transform("mean").fillna(0.0)
            Xm = np.hstack([Xn, StandardScaler().fit_transform(hh_means)])
            for r1, r0, c_lbl in [("M1", "M0", "M1 vs. M0"), ("M2_M3", "M0", "M2/M3 vs. M0")]:
                n_ate, n_se, n_lo, n_hi = _boot_ate_se(nps_sub, Xn, "yield_t_ha", r1, r0, rng, n_boot=250)
                m_ate, m_se, m_lo, m_hi = _boot_ate_se(nps_sub, Xm, "yield_t_ha", r1, r0, rng, n_boot=250)
                check_rows.append({
                    "check_type": "NPS_Only_Sample",
                    "crop_group": crop,
                    "stratum": "NPS W1-W5 (Owned+Rented)",
                    "contrast": c_lbl,
                    "n_plots": len(nps_sub),
                    "total_ate_t_ha": round(n_ate, 4) if np.isfinite(n_ate) else np.nan,
                    "ate_se_boot": round(n_se, 4) if np.isfinite(n_se) else np.nan,
                    "ate_ci95_low": round(n_lo, 4) if np.isfinite(n_lo) else np.nan,
                    "ate_ci95_high": round(n_hi, 4) if np.isfinite(n_hi) else np.nan,
                    "cde_ate_t_ha": np.nan,
                    "attenuation_pct": np.nan,
                })
                check_rows.append({
                    "check_type": "Mundlak_CRE_NPS",
                    "crop_group": crop,
                    "stratum": "NPS W1-W5 + HH Means",
                    "contrast": c_lbl,
                    "n_plots": len(nps_sub),
                    "total_ate_t_ha": round(m_ate, 4) if np.isfinite(m_ate) else np.nan,
                    "ate_se_boot": round(m_se, 4) if np.isfinite(m_se) else np.nan,
                    "ate_ci95_low": round(m_lo, 4) if np.isfinite(m_lo) else np.nan,
                    "ate_ci95_high": round(m_hi, 4) if np.isfinite(m_hi) else np.nan,
                    "cde_ate_t_ha": np.nan,
                    "attenuation_pct": np.nan,
                })

        # VanderWeele & Ding (2017) E-value bound for M2/M3 vs M0 yield ATE
        ate_m23, se_m23, lo_m23, hi_m23 = _boot_ate_se(sub, X_sub, "yield_t_ha", "M2_M3", "M0", rng, n_boot=250)
        _, sd_m0 = w_mean_std(sub.loc[sub["model_regime"] == "M0", "yield_t_ha"], sub.loc[sub["model_regime"] == "M0", "ipw_weight"])
        if np.isfinite(ate_m23) and np.isfinite(sd_m0) and sd_m0 > 0 and ate_m23 > 0:
            rr = float(np.exp(0.91 * (ate_m23 / sd_m0)))
            e_val = rr + np.sqrt(max(rr * (rr - 1.0), 0.0))
            check_rows.append({
                "check_type": "E_Value_Sensitivity",
                "crop_group": crop,
                "stratum": "All Balanced Plots",
                "contrast": "M2/M3 vs. M0",
                "n_plots": len(sub),
                "total_ate_t_ha": round(ate_m23, 4),
                "ate_se_boot": round(se_m23, 4) if np.isfinite(se_m23) else np.nan,
                "ate_ci95_low": round(lo_m23, 4) if np.isfinite(lo_m23) else np.nan,
                "ate_ci95_high": round(hi_m23, 4) if np.isfinite(hi_m23) else np.nan,
                "cde_ate_t_ha": round(e_val, 3),
                "attenuation_pct": np.nan,
            })

        # Legacy beta_y0 normalized yield ATE sensitivity check
        for r1, r0, c_lbl in [("M1", "M0", "M1 vs. M0"), ("M2_M3", "M0", "M2/M3 vs. M0")]:
            norm_ate, norm_se, norm_lo, norm_hi = _boot_ate_se(sub, X_sub, "yield_t_ha_normalized", r1, r0, rng, n_boot=250)
            check_rows.append({
                "check_type": "Beta_y0_Normalized_Sensitivity",
                "crop_group": crop,
                "stratum": "Legacy β_y0-Normalized Yield",
                "contrast": c_lbl,
                "n_plots": len(sub),
                "total_ate_t_ha": round(norm_ate, 4) if np.isfinite(norm_ate) else np.nan,
                "ate_se_boot": round(norm_se, 4) if np.isfinite(norm_se) else np.nan,
                "ate_ci95_low": round(norm_lo, 4) if np.isfinite(norm_lo) else np.nan,
                "ate_ci95_high": round(norm_hi, 4) if np.isfinite(norm_hi) else np.nan,
                "cde_ate_t_ha": np.nan,
                "attenuation_pct": np.nan,
            })

        # Renters-only (K > 0) subsample check for M2/M3 vs M1 (symmetric paid cash cost)
        rent_sub = sub[(sub["mech_cost_tzs_ha"] > 0) & (sub["model_regime"].isin(["M1", "M2_M3"]))].copy().reset_index(drop=True)
        if len(rent_sub) >= 100 and (rent_sub["model_regime"] == "M1").sum() >= 30 and (rent_sub["model_regime"] == "M2_M3").sum() >= 30:
            Xr = StandardScaler().fit_transform(prepare_design_matrix(rent_sub))
            rent_ate, rent_se, rent_lo, rent_hi = _boot_ate_se(rent_sub, Xr, "yield_t_ha", "M2_M3", "M1", rng, n_boot=250)
            check_rows.append({
                "check_type": "Renters_Only_K_gt_0",
                "crop_group": crop,
                "stratum": "Paid Renters Only (K > 0)",
                "contrast": "M2/M3 vs. M1",
                "n_plots": len(rent_sub),
                "total_ate_t_ha": round(rent_ate, 4) if np.isfinite(rent_ate) else np.nan,
                "ate_se_boot": round(rent_se, 4) if np.isfinite(rent_se) else np.nan,
                "ate_ci95_low": round(rent_lo, 4) if np.isfinite(rent_lo) else np.nan,
                "ate_ci95_high": round(rent_hi, 4) if np.isfinite(rent_hi) else np.nan,
                "cde_ate_t_ha": np.nan,
                "attenuation_pct": np.nan,
            })

        # AASS 2022/23-only subsample check (hired mechanization services only)
        aass_sub = sub[sub["wave"] == "AASS_2022_23"].copy().reset_index(drop=True)
        if len(aass_sub) >= 100:
            Xa = StandardScaler().fit_transform(prepare_design_matrix(aass_sub))
            for r1, r0, c_lbl in [("M1", "M0", "M1 vs. M0"), ("M2_M3", "M0", "M2/M3 vs. M0")]:
                a_ate, a_se, a_lo, a_hi = _boot_ate_se(aass_sub, Xa, "yield_t_ha", r1, r0, rng, n_boot=250)
                if np.isfinite(a_ate):
                    check_rows.append({
                        "check_type": "AASS_Only_Sample",
                        "crop_group": crop,
                        "stratum": "AASS 2022/23 (Hired Only)",
                        "contrast": c_lbl,
                        "n_plots": len(aass_sub),
                        "total_ate_t_ha": round(a_ate, 4),
                        "ate_se_boot": round(a_se, 4) if np.isfinite(a_se) else np.nan,
                        "ate_ci95_low": round(a_lo, 4) if np.isfinite(a_lo) else np.nan,
                        "ate_ci95_high": round(a_hi, 4) if np.isfinite(a_hi) else np.nan,
                        "cde_ate_t_ha": np.nan,
                        "attenuation_pct": np.nan,
                    })

        # Gender-disaggregated robustness check (Male- vs Female-headed households)
        for g_lbl, g_val in [("Male-Headed HHs", 1.0), ("Female-Headed HHs", 0.0)]:
            gsub = sub[sub["hh_head_sex"] == g_val].copy().reset_index(drop=True)
            if len(gsub) >= 100:
                Xgn = StandardScaler().fit_transform(prepare_design_matrix(gsub))
                g_ate, g_se, g_lo, g_hi = _boot_ate_se(gsub, Xgn, "yield_t_ha", "M2_M3", "M0", rng, n_boot=250)
                if np.isfinite(g_ate):
                    check_rows.append({
                        "check_type": "Gender_Subgroup_ATE",
                        "crop_group": crop,
                        "stratum": g_lbl,
                        "contrast": "M2/M3 vs. M0",
                        "n_plots": len(gsub),
                        "total_ate_t_ha": round(g_ate, 4),
                        "ate_se_boot": round(g_se, 4) if np.isfinite(g_se) else np.nan,
                        "ate_ci95_low": round(g_lo, 4) if np.isfinite(g_lo) else np.nan,
                        "ate_ci95_high": round(g_hi, 4) if np.isfinite(g_hi) else np.nan,
                        "cde_ate_t_ha": np.nan,
                        "attenuation_pct": np.nan,
                    })

        # Overlap-Weighted (ATO, Li & Li 2019) robustness check attenuating extreme IPW weights
        if all(c in sub.columns for c in ("gps_M0", "gps_M1", "gps_M2_M3")):
            ov_sub = sub.copy()
            p_m0 = np.clip(ov_sub["gps_M0"].to_numpy(dtype=float), 1e-4, 1.0)
            p_m1 = np.clip(ov_sub["gps_M1"].to_numpy(dtype=float), 1e-4, 1.0)
            p_m23 = np.clip(ov_sub["gps_M2_M3"].to_numpy(dtype=float), 1e-4, 1.0)
            h_x = 1.0 / (1.0 / p_m0 + 1.0 / p_m1 + 1.0 / p_m23)
            p_ass = np.clip(ov_sub["gps_assigned"].to_numpy(dtype=float), 1e-4, 1.0)
            ov_sub["ipw_weight"] = ov_sub["weight"].to_numpy(dtype=float) * (h_x / p_ass)
            for r1, r0, c_lbl in [("M2_M3", "M0", "M2/M3 vs. M0"), ("M2_M3", "M1", "M2/M3 vs. M1")]:
                ov_ate, ov_se, ov_lo, ov_hi = _boot_ate_se(ov_sub, X_sub, "yield_t_ha", r1, r0, rng, n_boot=250)
                if np.isfinite(ov_ate):
                    check_rows.append({
                        "check_type": "Overlap_Weighted_ATO",
                        "crop_group": crop,
                        "stratum": "Generalized Overlap Weights (ATO)",
                        "contrast": c_lbl,
                        "n_plots": len(ov_sub),
                        "total_ate_t_ha": round(ov_ate, 4),
                        "ate_se_boot": round(ov_se, 4) if np.isfinite(ov_se) else np.nan,
                        "ate_ci95_low": round(ov_lo, 4) if np.isfinite(ov_lo) else np.nan,
                        "ate_ci95_high": round(ov_hi, 4) if np.isfinite(ov_hi) else np.nan,
                        "cde_ate_t_ha": np.nan,
                        "attenuation_pct": np.nan,
                    })

        # Labor upper-cap sensitivity check ([15, 220] person-days/ha) on NFI & Return to Labor ATEs
        if "person_days_ha_220" in sub.columns:
            l220_sub = sub.copy()
            pd220 = np.clip(pd.to_numeric(l220_sub["person_days_ha_220"], errors="coerce").fillna(l220_sub["person_days_ha"]).to_numpy(dtype=float), 15.0, 220.0)
            sub_p = pd.Series([aez_p_map.get((crop, a_c), crop_p_map.get(crop, 0.0)) for a_c in l220_sub["aez_code"]], index=l220_sub.index).to_numpy(dtype=float)
            sub_w = l220_sub.groupby("aez_code")["_obs_wage"].transform("median").fillna(1528.0).clip(1500.0, 4000.0).to_numpy(dtype=float)
            sub_gross = l220_sub["yield_t_ha"].to_numpy(dtype=float) * sub_p
            sub_k = l220_sub["mech_cost_tzs_ha"].to_numpy(dtype=float)
            sub_b = l220_sub["biochem_cost_tzs_ha"].to_numpy(dtype=float)
            l220_sub["nfi_220"] = sub_gross - (sub_k + sub_w * pd220 + sub_b)
            l220_sub["rl_220"] = (sub_gross - sub_k - sub_b) / pd220
            for out_c, s_lbl in [("nfi_220", "Labor Cap [15, 220]: NFI (TZS/ha)"), ("rl_220", "Labor Cap [15, 220]: Ret. Labor (TZS/day)")]:
                l_ate, l_se, l_lo, l_hi = _boot_ate_se(l220_sub, X_sub, out_c, "M2_M3", "M0", rng, n_boot=250)
                if np.isfinite(l_ate):
                    check_rows.append({
                        "check_type": "Labor_Cap_220_Sensitivity",
                        "crop_group": crop,
                        "stratum": s_lbl,
                        "contrast": "M2/M3 vs. M0",
                        "n_plots": len(l220_sub),
                        "total_ate_t_ha": round(l_ate, 2),
                        "ate_se_boot": round(l_se, 2) if np.isfinite(l_se) else np.nan,
                        "ate_ci95_low": round(l_lo, 2) if np.isfinite(l_lo) else np.nan,
                        "ate_ci95_high": round(l_hi, 2) if np.isfinite(l_hi) else np.nan,
                        "cde_ate_t_ha": np.nan,
                        "attenuation_pct": np.nan,
                    })

    # Paddy 2WT (M2) descriptive-only summary from causal_raw_df
    paddy_raw = causal_raw_df[causal_raw_df["crop_group"] == "Paddy"].copy()
    paddy_rows = []
    for reg in ("M0", "M1", "M2", "M3"):
        rsub = paddy_raw[paddy_raw["regime"] == reg]
        if rsub.empty:
            continue
        w = rsub["weight"].to_numpy(dtype=float)
        y_mu, y_sd = w_mean_std(rsub["yield_t_ha"], w)
        k_mu, _ = w_mean_std(rsub["mech_cost_tzs_ha"], w)
        d_mu, _ = w_mean_std(np.clip(rsub["person_days_ha"], 15.0, 160.0), w)
        irr_mu, _ = w_mean_std(rsub["irrigated_flag"], w)
        paddy_rows.append({
            "regime": reg,
            "n_plots": len(rsub),
            "weighted_yield_t_ha": round(y_mu, 3),
            "weighted_yield_sd": round(y_sd, 3),
            "weighted_mech_cost_tzs_ha": round(k_mu, 0),
            "weighted_person_days_ha": round(d_mu, 1),
            "weighted_irrigated_pct": round(100.0 * irr_mu, 1),
        })

    return pd.DataFrame(ate_rows), pd.DataFrame(check_rows), pd.DataFrame(paddy_rows)


def main():
    print("================================================================================")
    print(" STEP 3: ENTROPY-CALIBRATED MULTINOMIAL GPS / IPWRA BALANCING")
    print("================================================================================")

    panel = pd.read_parquet(IN_PARQUET)
    causal = panel[
        panel["regime"].isin(["M0", "M1", "M2", "M3"])
        & panel["yield_t_ha"].notna()
        & (panel["yield_t_ha"] > 0)
        & panel["weight"].notna()
        & (panel["weight"] > 0)
    ].copy()
    print(f"[1/4] Causal-eligible plots (observed M0-M3 & valid yield): {len(causal):,}")

    balanced_parts = []
    all_smd = []
    for crop in ("Maize", "Paddy", "Legumes"):
        sub = causal[causal["crop_group"] == crop]
        if sub.empty:
            continue
        b_df, smds = fit_crop_ipwra(sub)
        balanced_parts.append(b_df)
        all_smd.extend(smds)
        max_abs_post = max(abs(x["post_ipw_smd"]) for x in smds) if smds else 0.0
        pass_pct = 100.0 * sum(1 for x in smds if x["balanced_lt_010"]) / len(smds) if smds else 100.0
        print(f"      {crop:8}: retained {len(b_df):,}/{len(sub):,} plots | max|SMD|={max_abs_post:.4f} | {pass_pct:.1f}% < 0.10")

    balanced_df = pd.concat(balanced_parts, ignore_index=True)
    smd_df = pd.DataFrame(all_smd)

    balanced_df.to_parquet(OUT_PARQUET, index=False)
    smd_df.to_csv(OUT_SMD_CSV, index=False)
    write_smd_markdown(smd_df, OUT_SMD_MD)
    # Append Step 3 common-support trimming row to Table S0
    s0_path = os.path.join(OUTPUTS_DIR, "tables", "table_s0_sample_attrition.csv")
    if os.path.exists(s0_path):
        s0_df = pd.read_csv(s0_path)
        s0_df = s0_df[~s0_df["Stage"].str.startswith("5.")].copy()
        s0_new = pd.DataFrame([{
            "Stage": "5. Retained after GPS common-support trimming [0.02, 0.98]",
            "Plots_N": int(len(balanced_df)),
            "Dropped_N": int(len(causal) - len(balanced_df)),
        }])
        pd.concat([s0_df, s0_new], ignore_index=True).to_csv(s0_path, index=False)
    print(f"[2/4] Exported balanced panel: {OUT_PARQUET}")
    print(f"[3/4] Exported Table S1 SMD:   {OUT_SMD_CSV} & .md")

    print("[4/4] Crop x Regime Weighted Moments Ready for Step 4 Monte Carlo:")
    summary_rows = []
    for (crop, reg), grp in balanced_df.groupby(["crop_group", "model_regime"]):
        w = grp["ipw_weight"].to_numpy()
        y_mu, _ = w_mean_std(grp["yield_t_ha"], w)
        k_mu, _ = w_mean_std(grp["mech_cost_tzs_ha"], w)
        l_mu, _ = w_mean_std(grp["labor_cost_tzs_ha"], w)
        b_mu, _ = w_mean_std(grp["biochem_cost_tzs_ha"], w)
        summary_rows.append({
            "crop": crop, "regime": reg, "n_plots": len(grp),
            "yield_t_ha": round(y_mu, 3), "mech_tzs_ha": round(k_mu, 0),
            "labor_tzs_ha": round(l_mu, 0), "biochem_tzs_ha": round(b_mu, 0),
        })
    print(pd.DataFrame(summary_rows).to_string(index=False))

    print("[5/5] Estimating IPWRA ATE/ATT (500 HH-clustered bootstrap), B-mediation & GPS-area checks...")
    ate_df, checks_df, paddy2wt_df = estimate_ate_att_and_checks(balanced_df, causal, n_boot=500)
    ate_df.to_csv(OUT_ATE_CSV, index=False)
    checks_df.to_csv(OUT_CHECKS_CSV, index=False)
    paddy2wt_df.to_csv(OUT_PADDY_2WT_CSV, index=False)

    # Export Table S1b: Weight dispersion & AEZ/wave FE max post-SMD diagnostics
    extra_bal = []
    for crop in ("Maize", "Paddy", "Legumes"):
        sub = balanced_df[balanced_df["crop_group"] == crop]
        for reg in ("M0", "M1", "M2_M3"):
            rsub = sub[sub["model_regime"] == reg]
            if rsub.empty:
                continue
            w = rsub["ipw_weight"].to_numpy(dtype=float)
            w_norm = w / np.mean(w)
            extra_bal.append({
                "crop_group": crop,
                "regime": reg,
                "n_plots": len(rsub),
                "neff": round(kish_neff(w), 1),
                "neff_ratio_pct": round(100.0 * kish_neff(w) / len(rsub), 1),
                "w_median": round(float(np.median(w_norm)), 2),
                "w_p99": round(float(np.quantile(w_norm, 0.99)), 2),
                "w_max": round(float(np.max(w_norm)), 2),
            })
    pd.DataFrame(extra_bal).to_csv(OUT_BAL_EXTRA_CSV, index=False)

    # Export Table S4b: Cash Gross Margin vs Economic NFI (baseline ~1,528 vs 5,000 TZS/day)
    wgm_rows = []
    for crop in ("Maize", "Paddy", "Legumes"):
        sub = balanced_df[balanced_df["crop_group"] == crop].copy()
        pdays = np.clip(pd.to_numeric(sub["person_days_ha"], errors="coerce").to_numpy(dtype=float), 15.0, 160.0)
        vp_c = sub["price_tzs_t"].notna() & sub["ipw_weight"].notna() & (sub["ipw_weight"] > 0)
        crop_p_wm = float(np.average(sub.loc[vp_c, "price_tzs_t"], weights=sub.loc[vp_c, "ipw_weight"])) if vp_c.any() else float(sub["price_tzs_t"].median())
        aez_p_wm = {}
        for a_c, agrp in sub.groupby("aez_code"):
            vp_a = agrp["price_tzs_t"].notna() & agrp["ipw_weight"].notna() & (agrp["ipw_weight"] > 0)
            if vp_a.any():
                aez_p_wm[a_c] = float(np.average(agrp.loc[vp_a, "price_tzs_t"], weights=agrp.loc[vp_a, "ipw_weight"]))
        aez_p = sub["aez_code"].map(aez_p_wm).fillna(crop_p_wm).to_numpy(dtype=float)
        obs_w = np.where(pdays > 0, sub["labor_cost_tzs_ha"] / pdays, np.nan).clip(1500.0, 4000.0)
        sub["_ow"] = obs_w
        aez_w = sub.groupby("aez_code")["_ow"].transform("median").fillna(1528.0).clip(1500.0, 4000.0).to_numpy(dtype=float)
        gross = sub["yield_t_ha"].to_numpy(dtype=float) * aez_p
        k_c = sub["mech_cost_tzs_ha"].to_numpy(dtype=float)
        b_c = sub["biochem_cost_tzs_ha"].to_numpy(dtype=float)
        sub["cash_gm"] = gross - k_c - b_c
        sub["nfi_base"] = gross - k_c - b_c - aez_w * pdays
        sub["nfi_5k"] = gross - k_c - b_c - 5000.0 * pdays
        X_s = StandardScaler().fit_transform(prepare_design_matrix(sub))
        ate_5k, _ = compute_dr_ate_att(sub, X_s, "nfi_5k", "M2_M3", "M0")
        for reg in ("M0", "M1", "M2_M3"):
            rsub = sub[sub["model_regime"] == reg]
            w = rsub["ipw_weight"].to_numpy(dtype=float)
            wgm_rows.append({
                "crop_group": crop,
                "regime": reg,
                "cash_gross_margin_tzs_ha": round(w_mean_std(rsub["cash_gm"], w)[0], 0),
                "econ_nfi_base_tzs_ha": round(w_mean_std(rsub["nfi_base"], w)[0], 0),
                "econ_nfi_5000_tzs_ha": round(w_mean_std(rsub["nfi_5k"], w)[0], 0),
                "ate_m23_vs_m0_5000_tzs_ha": round(ate_5k, 0) if reg == "M2_M3" else np.nan,
            })
    pd.DataFrame(wgm_rows).to_csv(OUT_WAGE_GM_CSV, index=False)

    # Export doubly robust IPWRA potential-outcome yield means for Stage 1/2 simulation anchoring
    dr_po_rows = []
    cens_rows = []
    for crop in ("Maize", "Paddy", "Legumes"):
        sub = balanced_df[balanced_df["crop_group"] == crop].copy().reset_index(drop=True)
        X_s = StandardScaler().fit_transform(prepare_design_matrix(sub))
        w_srv = sub["weight"].to_numpy(dtype=float)
        w_ipw = sub["ipw_weight"].to_numpy(dtype=float)
        y_arr = sub["yield_t_ha"].to_numpy(dtype=float)
        reg_arr = sub["model_regime"].to_numpy()
        for reg in ("M0", "M1", "M2_M3"):
            rmask = reg_arr == reg
            if rmask.sum() < 10:
                continue
            y_ipw = float(np.average(y_arr[rmask], weights=w_ipw[rmask]))
            mod = Ridge(alpha=10.0).fit(X_s[rmask], y_arr[rmask], sample_weight=w_ipw[rmask])
            mu_hat = mod.predict(X_s)
            aug = float(np.sum(w_ipw[rmask] * (y_arr[rmask] - mu_hat[rmask])) / max(np.sum(w_ipw[rmask]), 1e-12))
            y_dr = float(np.average(mu_hat, weights=w_srv) + aug)
            dr_po_rows.append({
                "crop_group": crop, "regime": reg,
                "y_ipw": round(y_ipw, 6), "y_dr": round(y_dr, 6),
                "dr_scale": round(y_dr / max(y_ipw, 1e-6), 6),
            })
            d_arr = np.clip(pd.to_numeric(sub.loc[rmask, "person_days_ha"], errors="coerce").to_numpy(dtype=float), 15.0, 160.0)
            w_r = w_ipw[rmask]
            cens_rows.append({
                "crop_group": crop, "regime": reg, "n_plots": int(rmask.sum()),
                "pct_censored_15": round(100.0 * float(np.average(d_arr <= 15.001, weights=w_r)), 2),
                "pct_censored_160": round(100.0 * float(np.average(d_arr >= 159.999, weights=w_r)), 2),
                "emp_mean_D": round(float(np.average(d_arr, weights=w_r)), 1),
            })
    pd.DataFrame(dr_po_rows).to_csv(os.path.join(OUTPUTS_DIR, "tables", "dr_potential_outcome_means.csv"), index=False)
    pd.DataFrame(cens_rows).to_csv(os.path.join(OUTPUTS_DIR, "tables", "table_s3c_labor_censoring_diagnostics.csv"), index=False)
    # Write markdown version of ATE/ATT table
    ate_lines = [
        "# Table 3b: Doubly Robust IPWRA Average Treatment Effects (ATE & ATT) with 500 Household-Clustered Bootstrap SEs",
        "| Crop | Outcome | Contrast | ATE | SE (Boot) | 95% CI | ATT | SE (Boot) |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for _, r in ate_df.iterrows():
        ate_lines.append(
            f"| {r['crop_group']} | {r['outcome']} | {r['contrast']} | "
            f"{r['ate']:.4f} | {r['ate_se_boot']:.4f} | [{r['ate_ci95_low']:.4f}, {r['ate_ci95_high']:.4f}] | "
            f"{r['att']:.4f} | {r['att_se_boot']:.4f} |"
        )
    with open(OUT_ATE_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(ate_lines) + "\n")
    print(f"      Exported: {OUT_ATE_CSV}, {OUT_CHECKS_CSV}, {OUT_PADDY_2WT_CSV}")
    print("================================================================================")


if __name__ == "__main__":
    main()
