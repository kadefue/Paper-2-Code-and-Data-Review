#!/usr/bin/env python3
"""
src/04_stochastic_sim.py
========================
Step 4 of Study 2: Two-Stage UVE/MVE + Latin Hypercube Sampling (LHS) +
GRKS Cost/Price/Labor Simulation + Stoplight Risk Ranking Engine.

Reads:
  - outputs/data/ipwra_balanced_panel.parquet

Exports:
  - outputs/tables/table3_model_validation_uve_mve.csv & .md
  - outputs/tables/table4_stochastic_cost_decomposition.csv & .md
  - outputs/tables/table5_nfi_labor_return_by_aez.csv & .md
  - outputs/data/mve_simulation_draws.npz

Usage:
  .venv/bin/python src/04_stochastic_sim.py
"""

import os
import numpy as np
import pandas as pd
from scipy.stats import qmc, norm, ks_2samp

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
IN_PARQUET = os.path.join(OUTPUTS_DIR, "data", "ipwra_balanced_panel.parquet")
OUT_NPZ = os.path.join(OUTPUTS_DIR, "data", "mve_simulation_draws.npz")
OUT_T3_CSV = os.path.join(OUTPUTS_DIR, "tables", "table3_model_validation_uve_mve.csv")
OUT_T3_MD = os.path.join(OUTPUTS_DIR, "tables", "table3_model_validation_uve_mve.md")
OUT_T4_CSV = os.path.join(OUTPUTS_DIR, "tables", "table4_stochastic_cost_decomposition.csv")
OUT_T4_MD = os.path.join(OUTPUTS_DIR, "tables", "table4_stochastic_cost_decomposition.md")
OUT_T5_CSV = os.path.join(OUTPUTS_DIR, "tables", "table5_nfi_labor_return_by_aez.csv")
OUT_T5_MD = os.path.join(OUTPUTS_DIR, "tables", "table5_nfi_labor_return_by_aez.md")

SEED = 2026
N_ITER = 2000

AEZ_NAMES = {
    0: "National (Tanzania)",
    1: "Central Semi-Arid",
    2: "Northern Highlands",
    3: "Southern Highlands",
    4: "Lake Victoria Basin",
    5: "Western Miombo",
    6: "Eastern Coastal Lowlands",
    7: "Southern Coastal Lowlands",
    8: "Northern Coastal Lowlands",
    9: "Zanzibar Archipelago",
}


def weighted_mean(v, w):
    m = pd.notna(v) & pd.notna(w) & (w > 0)
    if not m.any():
        return 0.0
    return float(np.average(v[m], weights=w[m]))


def weighted_quantile_sample(values, weights, u_draws):
    """Inverse-CDF sampling from an empirical weighted distribution (0-padded CDF)."""
    v = np.asarray(values, dtype=float)
    w = np.asarray(weights, dtype=float)
    mask = np.isfinite(v) & np.isfinite(w) & (w > 0)
    if not mask.any():
        return np.zeros_like(u_draws)
    v, w = v[mask], w[mask]
    idx = np.argsort(v)
    v, w = v[idx], w[idx]
    cdf = np.concatenate([[0.0], np.cumsum(w) / np.sum(w)])
    v_pad = np.concatenate([[v[0]], v])
    return np.interp(u_draws, cdf, v_pad)


def grks_ppf(u, a, m, b):
    """
    GRKS (Gray-Richardson-Klose-Schumann) quantile function parameterized by
    (Min=a, Middle/Mean=m, Max=b) where 50% of mass is below m and 95% is in [a, b].
    """
    u = np.clip(np.asarray(u, dtype=float), 1e-6, 1.0 - 1e-6)
    a = min(float(a), float(m))
    b = max(float(b), float(m))
    if b - a < 1e-9:
        return np.full_like(u, m)
    # Two-piece normal-tail GRKS: scale so P(X < a) = 0.025 and P(X > b) = 0.025
    z = norm.ppf(u)
    z975 = norm.ppf(0.975)  # ~1.96
    sig_low = max((m - a) / z975, 1e-6)
    sig_high = max((b - m) / z975, 1e-6)
    draws = np.where(u <= 0.5, m + z * sig_low, m + z * sig_high)
    draws = np.clip(draws, 0.0, None)
    # Mean-preserving calibration: prevents upward mean bias on right-skewed costs (K, B)
    d_mean = float(np.mean(draws))
    if d_mean > 1e-9 and m > 0:
        draws = draws * (m / d_mean)
    return draws


def get_triplet(series, weights):
    """Computes IPWRA-weighted (Min_p025, Mean, Max_p975) triplet for GRKS."""
    v = np.asarray(series, dtype=float)
    w = np.asarray(weights, dtype=float)
    mask = np.isfinite(v) & np.isfinite(w) & (w > 0) & (v >= 0)
    if not mask.any():
        return 0.0, 0.0, 0.0
    v, w = v[mask], w[mask]
    mu = float(np.average(v, weights=w))
    lo = float(np.quantile(v, 0.025))
    hi = float(np.quantile(v, 0.975))
    return min(lo, mu), mu, max(hi, mu)


def hurdle_empirical_ppf(u, series, weights):
    """
    Two-part hurdle empirical quantile resampling for zero-inflated cost variables (K, B):
      - Part 1: Exact IPWRA-weighted zero probability p0 = P(X == 0).
      - Part 2: For u > p0, maps u_pos = (u - p0) / (1 - p0) through the IPWRA-weighted
        empirical inverse CDF of strictly positive observations (X > 0), with
        multiplicative mean preservation.
    """
    u = np.clip(np.asarray(u, dtype=float), 1e-6, 1.0 - 1e-6)
    v = np.asarray(series, dtype=float)
    w = np.asarray(weights, dtype=float)
    mask = np.isfinite(v) & np.isfinite(w) & (w > 0) & (v >= 0)
    if not mask.any():
        return np.zeros_like(u)
    v, w = v[mask], w[mask]
    emp_mu = float(np.average(v, weights=w))
    if emp_mu <= 1e-9:
        return np.zeros_like(u)
    p0 = float(np.sum(w[v <= 1e-6]) / np.sum(w))
    pos_mask = v > 1e-6
    if pos_mask.sum() < 5:
        return weighted_quantile_sample(v, w, u)
    draws = np.zeros_like(u)
    if p0 > 1e-6:
        act = u > p0
        if act.any():
            u_pos = np.clip((u[act] - p0) / max(1.0 - p0, 1e-6), 1e-6, 1.0 - 1e-6)
            draws[act] = weighted_quantile_sample(v[pos_mask], w[pos_mask], u_pos)
    else:
        draws = weighted_quantile_sample(v, w, u)
    # Multiplicative mean preservation check
    sim_mu = float(np.mean(draws))
    if sim_mu > 1e-9 and emp_mu > 0:
        draws = draws * (emp_mu / sim_mu)
    return draws


def _load_dr_scales():
    """Loads doubly robust IPWRA potential-outcome yield scaling factors (y_dr / y_ipw)."""
    p = os.path.join(OUTPUTS_DIR, "tables", "dr_potential_outcome_means.csv")
    if not os.path.exists(p):
        return {}
    ddf = pd.read_csv(p)
    return {(r["crop_group"], r["regime"]): float(r["dr_scale"]) for _, r in ddf.iterrows()}


def psd_cholesky(corr):
    """Eigenvalue PSD regularization (eigvals >= 1e-8) + Cholesky decomposition."""
    eigvals, eigvecs = np.linalg.eigh(corr)
    eigvals = np.maximum(eigvals, 1e-8)
    corr_psd = eigvecs @ np.diag(eigvals) @ eigvecs.T
    d = np.sqrt(np.diag(corr_psd))
    corr_psd = corr_psd / np.outer(d, d)
    return np.linalg.cholesky(corr_psd)


def stoplight_probs(arr, red_cut, green_cut):
    """Returns sanitized (Red%, Yellow%, Green%) probabilities (no -0.0)."""
    arr = np.asarray(arr, dtype=float)
    red = 100.0 * float(np.mean(arr < red_cut))
    green = 100.0 * float(np.mean(arr > green_cut))
    yellow = max(0.0, 100.0 - red - green)
    def clean(x):
        r = round(x, 2)
        return 0.0 if abs(r) < 1e-9 else r
    return clean(red), clean(yellow), clean(green)


def write_md(df, title, subtitle, path):
    lines = [f"# {title}", f"*{subtitle}*\n"]
    cols = list(df.columns)
    lines.append("| " + " | ".join(cols) + " |")
    lines.append("|" + "|".join(["---"] * len(cols)) + "|")
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(str(r[c]) if pd.notna(r[c]) else "-" for c in cols) + " |")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def kish_neff(w):
    wv = np.asarray(w, dtype=float)
    wv = wv[np.isfinite(wv) & (wv > 0)]
    if len(wv) == 0:
        return 0.0
    return float((wv.sum() ** 2) / np.sum(wv ** 2))


def simulate_crop_stratum(df_crop, aez_code, seed=SEED, n_iter=N_ITER, use_dr_anchor=True):
    """
    Runs Stage 1 UVE + Stage 2 MVE + LHS + Two-Part Hurdle Empirical / GRKS simulation for
    one Crop x AEZ (or National aez_code==0) stratum.
    Anchors crop-regime yield means to doubly robust IPWRA potential-outcome means
    (preserving exact empirical fractional deviations S_y and (y, P, D) rank correlations),
    enforces n >= 30 and N_eff >= 20 for AEZ cells, and computes endogenous L = w_aez * D.
    """
    sub_aez = df_crop if aez_code == 0 else df_crop[df_crop["aez_code"] == aez_code]
    regimes = sorted(df_crop["model_regime"].unique())
    k = len(regimes)
    if k == 0 or sub_aez.empty:
        return None
    crop_name = str(df_crop["crop_group"].iloc[0])
    dr_scales = _load_dr_scales() if use_dr_anchor else {}

    # National fractional deviations & fallback parameters per regime
    nat_sdev = {}
    nat_mean_y = {}
    for r in regimes:
        rg = df_crop[df_crop["model_regime"] == r]
        mu_y_raw = max(weighted_mean(rg["yield_t_ha"], rg["ipw_weight"]), 1e-3)
        scale_r = dr_scales.get((crop_name, r), 1.0)
        nat_mean_y[r] = max(mu_y_raw * scale_r, 1e-3)
        nat_sdev[r] = (
            (rg["yield_t_ha"].to_numpy() - mu_y_raw) / mu_y_raw,
            rg["ipw_weight"].to_numpy(),
        )

    # Stage 1: UVE + LHS
    lhs_y = qmc.LatinHypercube(d=k, seed=seed).random(n=n_iter)
    isnd = norm.ppf(np.clip(lhs_y, 1e-6, 1.0 - 1e-6))

    y_uve = np.zeros((n_iter, k))
    mean_y_vec = np.zeros(k)
    sdev_list = []
    borrowed_flags = {}
    insufficient_flags = {}
    cell_n = {}
    cell_neff = {}

    for j, r in enumerate(regimes):
        rg = sub_aez[sub_aez["model_regime"] == r]
        n_r = len(rg)
        neff_r = kish_neff(rg["ipw_weight"].to_numpy()) if n_r > 0 else 0.0
        cell_n[r] = n_r
        cell_neff[r] = neff_r
        insufficient_flags[r] = (aez_code != 0) and (n_r < 30 or neff_r < 20.0)
        scale_r = dr_scales.get((crop_name, r), 1.0)

        if n_r >= 30:
            mu_y_raw = max(weighted_mean(rg["yield_t_ha"], rg["ipw_weight"]), 1e-3)
            mu_y = max(mu_y_raw * scale_r, 1e-3)
            s_dev = (rg["yield_t_ha"].to_numpy() - mu_y_raw) / mu_y_raw
            w_arr = rg["ipw_weight"].to_numpy()
            borrowed_flags[r] = False
        else:
            mu_y_raw = weighted_mean(rg["yield_t_ha"], rg["ipw_weight"]) if n_r >= 3 else (nat_mean_y[r] / max(scale_r, 1e-6))
            mu_y = max(mu_y_raw * scale_r, 1e-3)
            s_dev, w_arr = nat_sdev[r]
            borrowed_flags[r] = True

        mean_y_vec[j] = mu_y
        sdev_list.append((s_dev, w_arr))
        u_stage1 = norm.cdf(isnd[:, j])
        s_draw_1 = weighted_quantile_sample(s_dev, w_arr, u_stage1)
        y_uve[:, j] = np.clip(mu_y * (1.0 + s_draw_1), 0.0, None)

    # Stage 2: MVE + CUSDs (cross-regime residual correlation from AEZ x Regime cell means)
    aez_res = []
    for a_id, grp in df_crop.groupby("aez_code"):
        row_res = []
        for j, r in enumerate(regimes):
            rg = grp[grp["model_regime"] == r]
            if len(rg) > 0:
                m_a = weighted_mean(rg["yield_t_ha"], rg["ipw_weight"])
                row_res.append((m_a - nat_mean_y[r]) / nat_mean_y[r])
            else:
                row_res.append(0.0)
        aez_res.append(row_res)
    res_mat = np.asarray(aez_res, dtype=float)
    if res_mat.shape[0] >= 3:
        corr = np.corrcoef(res_mat, rowvar=False)
        corr = np.nan_to_num(corr, nan=0.0)
        np.fill_diagonal(corr, 1.0)
    else:
        corr = np.eye(k)

    L = psd_cholesky(corr)
    csnd = isnd @ L.T
    u2 = np.clip(norm.cdf(csnd), 1e-6, 1.0 - 1e-6)

    y_mve = np.zeros((n_iter, k))
    for j in range(k):
        s_dev, w_arr = sdev_list[j]
        s_draw_2 = weighted_quantile_sample(s_dev, w_arr, u2[:, j])
        y_mve[:, j] = np.clip(mean_y_vec[j] * (1.0 + s_draw_2), 0.0, None)

    # GRKS Costs, Prices, Wage, and Person-Days with joint (y, P, D) correlation
    lhs_c = qmc.LatinHypercube(d=5 * k, seed=seed + 10).random(n=n_iter)
    z_indep = norm.ppf(np.clip(lhs_c, 1e-6, 1.0 - 1e-6))
    P_sim = np.zeros((n_iter, k))
    K_sim = np.zeros((n_iter, k))
    L_sim = np.zeros((n_iter, k))
    B_sim = np.zeros((n_iter, k))
    D_sim = np.zeros((n_iter, k))

    # Common crop-AEZ price and rural daily wage distributions across regimes
    # (isolates mechanical technology and input/yield effects from price-level selection)
    aez_fb = sub_aez if len(sub_aez) >= 30 else df_crop
    w_aez_fb = aez_fb["ipw_weight"].to_numpy()
    p_triplet_common = get_triplet(aez_fb["price_tzs_t"], w_aez_fb)

    implied_w_all = np.where(
        (aez_fb["person_days_ha"] > 0) & (aez_fb["labor_cost_tzs_ha"] > 0),
        aez_fb["labor_cost_tzs_ha"] / aez_fb["person_days_ha"],
        np.nan,
    )
    w_series_all = pd.Series(implied_w_all).clip(lower=1500.0, upper=4000.0)
    if w_series_all.notna().sum() >= 5:
        w_triplet_common = get_triplet(w_series_all, w_aez_fb)
        w_sim_common = np.clip(grks_ppf(lhs_c[:, 2], *w_triplet_common), 1500.0, 4000.0)
    else:
        w_sim_common = np.full(n_iter, 1800.0)

    for j, r in enumerate(regimes):
        rg = sub_aez[sub_aez["model_regime"] == r]
        rg_fb = rg if len(rg) >= 30 else df_crop[df_crop["model_regime"] == r]
        w_c = rg_fb["ipw_weight"].to_numpy()

        # IPW-weighted empirical (y, P, D) correlation from non-missing observations
        ypd = rg_fb[["yield_t_ha", "price_tzs_t", "person_days_ha", "ipw_weight"]].dropna()
        if len(ypd) >= 30:
            mat = ypd[["yield_t_ha", "price_tzs_t", "person_days_ha"]].to_numpy(dtype=float)
            w_ypd = ypd["ipw_weight"].to_numpy(dtype=float)
            mu_ypd = np.average(mat, axis=0, weights=w_ypd)
            d_ypd = mat - mu_ypd
            cov_w = (d_ypd.T * w_ypd) @ d_ypd / np.sum(w_ypd)
            sd_ypd = np.sqrt(np.maximum(np.diag(cov_w), 1e-12))
            c3 = np.nan_to_num(cov_w / np.outer(sd_ypd, sd_ypd), nan=0.0)
            np.fill_diagonal(c3, 1.0)
            L3 = psd_cholesky(c3)
            # Condition on z_y = csnd[:, j]; use common price quantile z_indep[:, 0] across regimes
            z_base = np.column_stack([csnd[:, j], z_indep[:, 0], z_indep[:, 5 * j + 4]])
            z_ypd = z_base @ L3.T
            u_p = np.clip(norm.cdf(z_ypd[:, 1]), 1e-6, 1.0 - 1e-6)
            u_d = np.clip(norm.cdf(z_ypd[:, 2]), 1e-6, 1.0 - 1e-6)
        else:
            u_p = lhs_c[:, 0]
            u_d = lhs_c[:, 5 * j + 4]

        P_sim[:, j] = grks_ppf(u_p, *p_triplet_common)
        K_sim[:, j] = hurdle_empirical_ppf(lhs_c[:, 5 * j + 1], rg_fb["mech_cost_tzs_ha"], w_c)
        B_sim[:, j] = hurdle_empirical_ppf(lhs_c[:, 5 * j + 3], rg_fb["biochem_cost_tzs_ha"], w_c)
        D_sim[:, j] = np.clip(grks_ppf(u_d, *get_triplet(rg_fb["person_days_ha"], w_c)), 15.0, 160.0)
        L_sim[:, j] = w_sim_common * D_sim[:, j]

    rev = P_sim * y_mve
    tot_cost = K_sim + L_sim + B_sim
    nfi = rev - tot_cost
    mech_share_rev = 100.0 * (K_sim / np.maximum(rev, 1.0))
    ret_labor = (rev - K_sim - B_sim) / np.clip(D_sim, 15.0, 160.0)

    return {
        "regimes": regimes,
        "borrowed": borrowed_flags,
        "insufficient": insufficient_flags,
        "cell_n": cell_n,
        "cell_neff": cell_neff,
        "y_uve": y_uve,
        "y_mve": y_mve,
        "P_sim": P_sim,
        "K_sim": K_sim,
        "L_sim": L_sim,
        "B_sim": B_sim,
        "D_sim": D_sim,
        "rev": rev,
        "nfi": nfi,
        "mech_share_rev": mech_share_rev,
        "ret_labor": ret_labor,
    }


def main():
    print("================================================================================")
    print(" STEP 4: TWO-STAGE UVE/MVE + LHS + GRKS STOCHASTIC SIMULATION")
    print("================================================================================")

    df = pd.read_parquet(IN_PARQUET)
    t3_rows, t4_rows, t5_rows = [], [], []
    npz_payload = {}

    dr_scales = _load_dr_scales()
    for crop in ("Maize", "Paddy", "Legumes"):
        df_c = df[df["crop_group"] == crop].copy()
        if df_c.empty:
            continue

        # National (aez_code == 0) for Tables 3 & 4
        res_nat = simulate_crop_stratum(df_c, aez_code=0)
        regs = res_nat["regimes"]

        for j, r in enumerate(regs):
            sub_r = df_c.loc[df_c["model_regime"] == r]
            scale_r = dr_scales.get((crop, r), 1.0)
            obs = sub_r["yield_t_ha"].dropna().to_numpy() * scale_r
            w_obs = sub_r.loc[sub_r["yield_t_ha"].notna(), "ipw_weight"].to_numpy()
            y_u = res_nat["y_uve"][:, j]
            y_m = res_nat["y_mve"][:, j]
            rng_ks = np.random.default_rng(SEED + j)
            obs_w_boot = rng_ks.choice(obs, size=len(obs), replace=True, p=w_obs / np.sum(w_obs))
            ks_stat, ks_p = ks_2samp(obs_w_boot, y_m)

            for stage, arr, w_a in [("Observed_IPWRA", obs_w_boot, None), ("Stage1_UVE", y_u, None), ("Stage2_MVE", y_m, None)]:
                mu = float(np.mean(arr))
                sd = float(np.std(arr))
                t3_rows.append({
                    "Crop": crop, "Regime": r, "Series": stage,
                    "Mean_tha": round(mu, 3), "SD_tha": round(sd, 3),
                    "CV_pct": round(100.0 * sd / mu, 1) if mu > 0 else np.nan,
                    "Min_tha": round(float(np.min(arr)), 3),
                    "Median_tha": round(float(np.median(arr)), 3),
                    "Max_tha": round(float(np.max(arr)), 3),
                    "KS_D_vs_Obs": round(float(ks_stat), 4) if stage == "Stage2_MVE" else np.nan,
                    "KS_p_value": round(float(ks_p), 4) if stage == "Stage2_MVE" else np.nan,
                })

            k_m = float(np.mean(res_nat["K_sim"][:, j]))
            l_m = float(np.mean(res_nat["L_sim"][:, j]))
            b_m = float(np.mean(res_nat["B_sim"][:, j]))
            d_m = float(np.mean(res_nat["D_sim"][:, j]))
            p_m = float(np.mean(res_nat["P_sim"][:, j]))
            rev_m = float(np.mean(res_nat["rev"][:, j]))
            nfi_m = float(np.mean(res_nat["nfi"][:, j]))
            tc_m = k_m + l_m + b_m
            rho_bounded = (k_m / nfi_m) if nfi_m > 0 else np.nan
            mech_share_rev_ratio = (k_m / max(rev_m, 1.0)) * 100.0
            rent_sub = sub_r[sub_r["mech_cost_tzs_ha"] > 0]
            k_rent_m = weighted_mean(rent_sub["mech_cost_tzs_ha"], rent_sub["ipw_weight"]) if len(rent_sub) > 0 else 0.0
            emp_k_arr = sub_r["mech_cost_tzs_ha"].to_numpy(dtype=float)
            emp_b_arr = sub_r["biochem_cost_tzs_ha"].to_numpy(dtype=float)
            emp_d_arr = np.clip(sub_r["person_days_ha"].to_numpy(dtype=float), 15.0, 160.0)
            w_sub = sub_r["ipw_weight"].to_numpy(dtype=float)
            emp_k = weighted_mean(emp_k_arr, w_sub)
            emp_b = weighted_mean(emp_b_arr, w_sub)
            emp_d = weighted_mean(emp_d_arr, w_sub)

            def _moments(arr, w_a=None):
                a = np.asarray(arr, dtype=float)
                if w_a is not None:
                    m = np.isfinite(a) & np.isfinite(w_a) & (w_a > 0)
                    a, w_f = a[m], w_a[m]
                    mu = float(np.average(a, weights=w_f))
                    sd = float(np.sqrt(np.average((a - mu) ** 2, weights=w_f)))
                    idx = np.argsort(a)
                    cdf = np.cumsum(w_f[idx]) / np.sum(w_f)
                    med = float(np.interp(0.50, cdf, a[idx]))
                    p95 = float(np.interp(0.95, cdf, a[idx]))
                    zpct = 100.0 * float(np.average(a <= 1e-6, weights=w_f))
                else:
                    mu = float(np.mean(a))
                    sd = float(np.std(a))
                    med = float(np.median(a))
                    p95 = float(np.quantile(a, 0.95))
                    zpct = 100.0 * float(np.mean(a <= 1e-6))
                return mu, sd, med, p95, zpct

            ek_m, ek_sd, ek_med, ek_p95, ek_z = _moments(emp_k_arr, w_sub)
            sk_m, sk_sd, sk_med, sk_p95, sk_z = _moments(res_nat["K_sim"][:, j])
            eb_m, eb_sd, eb_med, eb_p95, eb_z = _moments(emp_b_arr, w_sub)
            sb_m, sb_sd, sb_med, sb_p95, sb_z = _moments(res_nat["B_sim"][:, j])
            ed_m, ed_sd, ed_med, ed_p95, ed_z = _moments(emp_d_arr, w_sub)
            sd_m, sd_sd, sd_med, sd_p95, sd_z = _moments(res_nat["D_sim"][:, j])

            t4_rows.append({
                "Crop": crop, "Regime": r,
                "Mech_Cost_K_TZS_ha": round(k_m, 0),
                "Mech_Cost_K_Renters_TZS_ha": round(k_rent_m, 0),
                "Labor_Cost_L_TZS_ha": round(l_m, 0),
                "Biochem_Cost_B_TZS_ha": round(b_m, 0),
                "Total_Cost_TZS_ha": round(tc_m, 0),
                "Person_Days_ha": round(d_m, 1),
                "Price_P_TZS_t": round(p_m, 0),
                "Mech_to_Margin_Ratio_rho": round(rho_bounded, 3) if pd.notna(rho_bounded) else np.nan,
                "Mech_Share_GrossRev_pct": round(mech_share_rev_ratio, 2),
                "_s3b_rows": [
                    {"Crop": crop, "Regime": r, "Variable": "Mech Cost K (TZS/ha)", "Emp_Mean": round(ek_m, 0), "Sim_Mean": round(sk_m, 0), "Emp_SD": round(ek_sd, 0), "Sim_SD": round(sk_sd, 0), "Emp_Median": round(ek_med, 0), "Sim_Median": round(sk_med, 0), "Emp_P95": round(ek_p95, 0), "Sim_P95": round(sk_p95, 0), "Emp_Zero_pct": round(ek_z, 1), "Sim_Zero_pct": round(sk_z, 1)},
                    {"Crop": crop, "Regime": r, "Variable": "Biochem Cost B (TZS/ha)", "Emp_Mean": round(eb_m, 0), "Sim_Mean": round(sb_m, 0), "Emp_SD": round(eb_sd, 0), "Sim_SD": round(sb_sd, 0), "Emp_Median": round(eb_med, 0), "Sim_Median": round(sb_med, 0), "Emp_P95": round(eb_p95, 0), "Sim_P95": round(sb_p95, 0), "Emp_Zero_pct": round(eb_z, 1), "Sim_Zero_pct": round(sb_z, 1)},
                    {"Crop": crop, "Regime": r, "Variable": "Labor D (person-days/ha)", "Emp_Mean": round(ed_m, 1), "Sim_Mean": round(sd_m, 1), "Emp_SD": round(ed_sd, 1), "Sim_SD": round(sd_sd, 1), "Emp_Median": round(ed_med, 1), "Sim_Median": round(sd_med, 1), "Emp_P95": round(ed_p95, 1), "Sim_P95": round(sd_p95, 1), "Emp_Zero_pct": round(ed_z, 1), "Sim_Zero_pct": round(sd_z, 1)},
                ],
            })

            npz_payload[f"{crop}__{r}__y_mve"] = y_m
            npz_payload[f"{crop}__{r}__nfi"] = res_nat["nfi"][:, j]
            npz_payload[f"{crop}__{r}__ret_labor"] = res_nat["ret_labor"][:, j]
            npz_payload[f"{crop}__{r}__K"] = res_nat["K_sim"][:, j]

        # AEZ 1..9 + National (0) for Table 5
        for aez_id in [0] + list(range(1, 10)):
            res_a = res_nat if aez_id == 0 else simulate_crop_stratum(df_c, aez_code=aez_id)
            if res_a is None:
                continue
            for j, r in enumerate(res_a["regimes"]):
                insuff = res_a["insufficient"][r]
                nfi_arr = res_a["nfi"][:, j]
                rl_arr = res_a["ret_labor"][:, j]
                mu_nfi = float(np.mean(nfi_arr))
                med_nfi = float(np.median(nfi_arr))
                sd_nfi = float(np.std(nfi_arr))
                t5_rows.append({
                    "Crop": crop, "AEZ_Code": aez_id, "AEZ_Name": AEZ_NAMES[aez_id], "Regime": r,
                    "n_plots": res_a["cell_n"][r],
                    "N_eff": round(res_a["cell_neff"][r], 1),
                    "Insufficient_Support": insuff,
                    "Borrowed_S_dev": res_a["borrowed"][r],
                    "NFI_Mean_TZS_ha": np.nan if insuff else round(mu_nfi, 0),
                    "NFI_Median_TZS_ha": np.nan if insuff else round(med_nfi, 0),
                    "NFI_SD_TZS_ha": np.nan if insuff else round(sd_nfi, 0),
                    "NFI_CV_pct": np.nan if (insuff or mu_nfi <= 10_000.0) else round(100.0 * sd_nfi / mu_nfi, 1),
                    "Return_to_Labor_TZS_day": np.nan if insuff else round(float(np.mean(rl_arr)), 0),
                    "Return_to_Labor_Median_TZS_day": np.nan if insuff else round(float(np.median(rl_arr)), 0),
                })

    t3 = pd.DataFrame(t3_rows)
    t4_full = pd.DataFrame(t4_rows)
    # Export Table S3b: Expanded Empirical vs Simulated Cost/Labor Validation (Mean, SD, Median, P95, Zero%)
    s3b_list = []
    for rows_sub in t4_full["_s3b_rows"]:
        s3b_list.extend(rows_sub)
    s3b = pd.DataFrame(s3b_list)
    s3b.to_csv(os.path.join(OUTPUTS_DIR, "tables", "table_s3b_cost_validation_emp_vs_sim.csv"), index=False)
    t4 = t4_full.drop(columns=["_s3b_rows"])
    t5 = pd.DataFrame(t5_rows)

    t3.to_csv(OUT_T3_CSV, index=False)
    write_md(t3, "Table 3: Two-Stage Model Validation (Observed IPWRA vs. Stage 1 UVE vs. Stage 2 MVE)", "N=2,000 Latin Hypercube draws; two-sample Kolmogorov-Smirnov test vs. observed", OUT_T3_MD)
    t4.to_csv(OUT_T4_CSV, index=False)
    write_md(t4, "Table 4: Simulated Stochastic Cost Decomposition, Person-Days, Price, and Mechanization-to-Margin Ratio", "GRKS-simulated (Min, Mean, Max) across M0-M3 and target crops", OUT_T4_MD)
    t5.to_csv(OUT_T5_CSV, index=False)
    write_md(t5, "Table 5: Simulated Net Farm Income (NFI) and Return to Labor Across 9 AEZs and Regimes (M0-M3)", "Stage 2 MVE + Two-Part Hurdle Empirical / GRKS simulation (N=2,000 draws per stratum)", OUT_T5_MD)
    np.savez_compressed(OUT_NPZ, **npz_payload)

    # Reconciliation Audit Table: Table 3a (DR ATE) vs. Table 5 (DR-Anchored Stage 2 Simulation)
    ate_path = os.path.join(OUTPUTS_DIR, "tables", "table_ate_att_causal_effects.csv")
    if os.path.exists(ate_path):
        ate_df = pd.read_csv(ate_path)
        t5_nat = t5[t5["AEZ_Code"] == 0].set_index(["Crop", "Regime"])
        t4_idx = t4.set_index(["Crop", "Regime"])
        diag_rows = []
        for crop in ("Maize", "Paddy", "Legumes"):
            for r1, r0, c_lbl in [("M1", "M0", "M1 vs. M0"), ("M2_M3", "M0", "M2/M3 vs. M0"), ("M2_M3", "M1", "M2/M3 vs. M1")]:
                a_nfi = ate_df[(ate_df["crop_group"] == crop) & (ate_df["outcome"] == "Net Farm Income (TZS/ha)") & (ate_df["contrast"] == c_lbl)]["ate"].iloc[0]
                a_rl = ate_df[(ate_df["crop_group"] == crop) & (ate_df["outcome"] == "Return to Labor (TZS/person-day)") & (ate_df["contrast"] == c_lbl)]["ate"].iloc[0]
                s_nfi_diff = t5_nat.loc[(crop, r1), "NFI_Mean_TZS_ha"] - t5_nat.loc[(crop, r0), "NFI_Mean_TZS_ha"]
                s_rl_mean_diff = t5_nat.loc[(crop, r1), "Return_to_Labor_TZS_day"] - t5_nat.loc[(crop, r0), "Return_to_Labor_TZS_day"]
                s_rl_med_diff = t5_nat.loc[(crop, r1), "Return_to_Labor_Median_TZS_day"] - t5_nat.loc[(crop, r0), "Return_to_Labor_Median_TZS_day"]
                # Ratio of means: E[P*y - K - B] / E[D] = (E[NFI] + E[L]) / E[D]
                rom_1 = (t5_nat.loc[(crop, r1), "NFI_Mean_TZS_ha"] + t4_idx.loc[(crop, r1), "Labor_Cost_L_TZS_ha"]) / t4_idx.loc[(crop, r1), "Person_Days_ha"]
                rom_0 = (t5_nat.loc[(crop, r0), "NFI_Mean_TZS_ha"] + t4_idx.loc[(crop, r0), "Labor_Cost_L_TZS_ha"]) / t4_idx.loc[(crop, r0), "Person_Days_ha"]
                diag_rows.append({
                    "Crop": crop, "Contrast": c_lbl,
                    "Table3a_DR_NFI_ATE": round(float(a_nfi), 0),
                    "Table5_Sim_NFI_Diff": round(float(s_nfi_diff), 0),
                    "Table3a_DR_RL_ATE": round(float(a_rl), 0),
                    "Table5_Sim_RL_Mean_Diff": round(float(s_rl_mean_diff), 0),
                    "Table5_Sim_RL_RatioOfMeans_Diff": round(float(rom_1 - rom_0), 0),
                    "Table5_Sim_RL_Median_Diff": round(float(s_rl_med_diff), 0),
                })
        diag_df = pd.DataFrame(diag_rows)
        diag_df.to_csv(os.path.join(OUTPUTS_DIR, "tables", "diagnostics_table3a_vs_table5.csv"), index=False)
        print("\n[AUDIT] Table 3a vs Table 5 Reconciliation:")
        print(diag_df.to_string(index=False))

    print("[1/3] Table 3 (Validation) sample:")
    print(t3[t3["Series"] == "Stage2_MVE"][["Crop", "Regime", "Mean_tha", "SD_tha", "CV_pct", "KS_D_vs_Obs", "KS_p_value"]].to_string(index=False))
    print("\n[2/3] Table 4 (Cost Decomposition):")
    print(t4.to_string(index=False))
    print("\n[3/3] Table 5 (National NFI & Return to Labor):")
    print(t5[t5["AEZ_Code"] == 0].to_string(index=False))
    print("================================================================================")


if __name__ == "__main__":
    main()
