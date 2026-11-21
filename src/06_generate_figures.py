#!/usr/bin/env python3
"""
src/06_generate_figures.py
==========================
Step 6 of Study 2: Publication-Grade Figures (300 DPI, PNG + Vector PDF).

Generates in outputs/figures/:
  1. fig1_tanzania_mechanization_map.png / .pdf
  2. fig2_causal_stochastic_workflow.png / .pdf
  3. fig3_uve_mve_validation_pdfs.png / .pdf
  4. fig4_nfi_and_labor_return_pdfs.png / .pdf
  5. fig5_stoplight_nfi_by_aez.png / .pdf
  6. fig6_stoplight_labor_by_plot_size.png / .pdf

Usage:
  .venv/bin/python src/06_generate_figures.py
"""

import os
import sys
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import ListedColormap
import seaborn as sns

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
from importlib import import_module
sim_mod = import_module("04_stochastic_sim")

BASE_DIR = os.path.dirname(SRC_DIR)
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
FIG_DIR = os.path.join(OUTPUTS_DIR, "figures")
SUB_FIG_DIR = os.path.join(BASE_DIR, "submission_package", "figures")
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(SUB_FIG_DIR, exist_ok=True)

CABI_FIG_NAMES = {
    "fig1_tanzania_mechanization_map": "Figure_1",
    "fig2_causal_stochastic_workflow": "Figure_2",
    "fig3_uve_mve_validation_pdfs": "Figure_3",
    "fig4_nfi_and_labor_return_pdfs": "Figure_4",
    "fig5_stoplight_nfi_by_aez": "Figure_5",
    "fig6_stoplight_labor_by_plot_size": "Figure_6",
    "fig_s1_gps_overlap": "Figure_S1",
}

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

REGIME_COLORS = {
    "M0": "#7f8c8d",
    "M1": "#e67e22",
    "M2": "#2980b9",
    "M3": "#27ae60",
    "M2_M3": "#16a085",
}


def save_fig(fig, stem):
    fig.savefig(os.path.join(FIG_DIR, f"{stem}.png"), dpi=300, bbox_inches="tight", pad_inches=0.15)
    fig.savefig(os.path.join(FIG_DIR, f"{stem}.jpg"), dpi=300, bbox_inches="tight", pad_inches=0.15)
    fig.savefig(os.path.join(FIG_DIR, f"{stem}.pdf"), dpi=300, bbox_inches="tight", pad_inches=0.15)
    fig.savefig(os.path.join(FIG_DIR, f"{stem}.tiff"), dpi=300, bbox_inches="tight", pad_inches=0.15, pil_kwargs={"compression": "tiff_lzw"})
    if stem in CABI_FIG_NAMES:
        cabi_n = CABI_FIG_NAMES[stem]
        fig.savefig(os.path.join(SUB_FIG_DIR, f"{cabi_n}.tiff"), dpi=300, bbox_inches="tight", pad_inches=0.15, pil_kwargs={"compression": "tiff_lzw"})
        fig.savefig(os.path.join(SUB_FIG_DIR, f"{cabi_n}.jpg"), dpi=300, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)


# -----------------------------------------------------------------------------
# FIGURE 1: TANZANIA REGIONAL MECHANIZATION CHOROPLETH MAP
# -----------------------------------------------------------------------------

def make_fig1():
    geo_path = os.path.join(DATA_DIR, "tanzania_maps", "tanzania_regions_2022phc.geojson")
    gdf = gpd.read_file(geo_path)
    gdf["reg_int"] = pd.to_numeric(gdf["reg_code"], errors="coerce").astype("Int64")

    # Compute regional M0-M3 shares from NCSA 2019/20 census (all 31 regions)
    ncsa_dir = os.path.join(DATA_DIR, "NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI")
    sov = pd.read_stata(os.path.join(ncsa_dir, "R000_SOV.dta"), columns=["HHID", "region", "finalweight_hh"], convert_categoricals=False)
    r122 = pd.read_stata(os.path.join(ncsa_dir, "R122_USE_TRACTOR_ANIMALS.dta"), columns=["HHID", "q122c0", "q122c3"], convert_categoricals=False)
    r121 = pd.read_stata(os.path.join(ncsa_dir, "R121_FARM_IMPLEMENTS.dta"), columns=["HHID", "q121c0", "q121c2"], convert_categoricals=False)

    hh_p = {h: set() for h in sov["HHID"]}
    for h, c in zip(r122.loc[r122["q122c3"] > 0, "HHID"], r122.loc[r122["q122c3"] > 0, "q122c0"]):
        if h in hh_p:
            if c in (1, 2, 3, 4): hh_p[h].add("M1")
            elif c == 6: hh_p[h].add("M2")
            elif c == 5: hh_p[h].add("M3")
    for h, c in zip(r121.loc[r121["q121c2"] == 1, "HHID"], r121.loc[r121["q121c2"] == 1, "q121c0"]):
        if h in hh_p:
            if c in (4, 5, 6, 7, 13): hh_p[h].add("M1")
            elif c == 12: hh_p[h].add("M2")
            elif c in (8, 9, 10): hh_p[h].add("M3")

    sov["regime"] = [("M3" if "M3" in hh_p[h] else ("M2" if "M2" in hh_p[h] else ("M1" if "M1" in hh_p[h] else "M0"))) for h in sov["HHID"]]
    reg_rows = []
    for reg, grp in sov.groupby("region"):
        wt = grp["finalweight_hh"].sum()
        s = {r: 100.0 * grp.loc[grp["regime"] == r, "finalweight_hh"].sum() / wt for r in ("M0", "M1", "M2", "M3")}
        dom = max(s, key=s.get)
        dom_idx = {"M0": 0, "M1": 1, "M2": 2, "M3": 3}[dom]
        reg_rows.append({"reg_int": int(reg), "dom_idx": dom_idx, "M1_pct": s["M1"], "M3_pct": s["M3"]})
    gdf = gdf.merge(pd.DataFrame(reg_rows), on="reg_int", how="left")

    fig, axes = plt.subplots(1, 3, figsize=(14.5, 5.2))
    cmap_dom = ListedColormap(["#7f8c8d", "#e67e22", "#2980b9", "#27ae60"])
    gdf.plot(column="dom_idx", ax=axes[0], cmap=cmap_dom, vmin=0, vmax=3, edgecolor="white", linewidth=0.5)
    axes[0].set_title("(a) Dominant Land-Prep Regime ($M_0$–$M_3$)", fontweight="bold")
    leg_patches = [patches.Patch(color=REGIME_COLORS[r], label=lbl) for r, lbl in [("M0", "$M_0$ Hand-Hoe"), ("M1", "$M_1$ Oxen"), ("M3", "$M_3$ 4WT Tractor")]]
    axes[0].legend(handles=leg_patches, loc="lower left", bbox_to_anchor=(0.01, 0.01), frameon=True, framealpha=0.92, fontsize=7.5)

    gdf.plot(column="M3_pct", ax=axes[1], cmap="YlGn", edgecolor="white", linewidth=0.5, legend=True, legend_kwds={"label": "4WT Tractor Share (%)", "shrink": 0.7})
    axes[1].set_title("(b) Four-Wheel Tractor ($M_3$) Share (%)", fontweight="bold")

    gdf.plot(column="M1_pct", ax=axes[2], cmap="YlOrBr", edgecolor="white", linewidth=0.5, legend=True, legend_kwds={"label": "Animal Traction Share (%)", "shrink": 0.7})
    axes[2].set_title("(c) Animal Traction ($M_1$) Share (%)", fontweight="bold")

    for ax in axes:
        ax.set_axis_off()
    # Add North arrow & 300 km scale bar to panel (a)
    xlim = axes[0].get_xlim()
    ylim = axes[0].get_ylim()
    x0 = xlim[0] + 0.08 * (xlim[1] - xlim[0])
    y0 = ylim[0] + 0.22 * (ylim[1] - ylim[0])
    # At ~6 deg S, 1 deg lon ~ 110.7 km -> 300 km ~ 2.71 deg
    axes[0].plot([x0, x0 + 2.71], [y0, y0], color="black", lw=2.2)
    axes[0].text(x0 + 1.355, y0 + 0.25, "300 km", ha="center", va="bottom", fontsize=7.5, fontweight="bold")
    nx = xlim[1] - 0.10 * (xlim[1] - xlim[0])
    ny = ylim[1] - 0.14 * (ylim[1] - ylim[0])
    axes[0].annotate("N", xy=(nx, ny + 0.7), xytext=(nx, ny),
                     ha="center", va="center", fontsize=9, fontweight="bold",
                     arrowprops=dict(facecolor="black", width=2, headwidth=6))

    fig.suptitle("Figure 1: Spatial Distribution of Smallholder Farm Power Regimes Across Tanzania (NCSA 2019/20)", fontsize=12, fontweight="bold", y=1.02)
    plt.tight_layout()
    save_fig(fig, "fig1_tanzania_mechanization_map")


# -----------------------------------------------------------------------------
# FIGURE 2: 5-STAGE CAUSAL-STOCHASTIC WORKFLOW
# -----------------------------------------------------------------------------

def make_fig2():
    s0 = pd.read_csv(os.path.join(OUTPUTS_DIR, "tables", "table_s0_sample_attrition.csv"))
    n_raw = int(s0.iloc[0]["Plots_N"])
    n_area = int(s0.iloc[1]["Plots_N"])
    n_bal = int(s0.iloc[-1]["Plots_N"])

    fig, ax = plt.subplots(figsize=(13.5, 3.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2.5)
    ax.axis("off")

    boxes = [
        (0.2, f"1. Multi-Wave Harmonization\n(NPS W1–5, NCSA 19/20,\nAASS 22/23–24/25)\n• N = {n_raw:,} → {n_area:,}\n• 0.05–20 ha; 2022/23 TZS", "#eaf2f8", "#2980b9"),
        (2.15, f"2. Multinomial GPS &\nEntropy-Calibrated IPWRA\n• Retained N = {n_bal:,}\n• Trimmed [0.02, 0.98]\n• 100% |SMD| < 0.10", "#fef9e7", "#d68910"),
        (4.1, "3. Stage 1 UVE + LHS\n• N=2,000 LHS ISNDs\n• Fractional Devs $S_y$\n• DR-Anchored + Wave FEs\n• n ≥ 30 Cell Guardrail", "#eafaf1", "#27ae60"),
        (6.05, "4. Stage 2 MVE + CUSD\n• Cross-Regime & (y,P,D)\n  Empirical Correlation\n• PSD + Cholesky → CUSD\n• Non-Negative Yields", "#f4ecf7", "#8e44ad"),
        (8.0, "5. Two-Part Hurdle & GRKS\n• Common P, w; L = w × D\n• D ∈ [15, 160] days/ha\n• NFI & Labor Stoplights\n• +30% K, −10% P & Scale", "#fdedec", "#c0392b"),
    ]
    for x, txt, fc, ec in boxes:
        rect = patches.FancyBboxPatch((x, 0.35), 1.75, 1.75, boxstyle="round,pad=0.08", facecolor=fc, edgecolor=ec, linewidth=1.8)
        ax.add_patch(rect)
        ax.text(x + 0.875, 1.225, txt, ha="center", va="center", fontsize=8, linespacing=1.35)

    for x in (1.98, 3.93, 5.88, 7.83):
        ax.annotate("", xy=(x + 0.16, 1.225), xytext=(x - 0.02, 1.225), arrowprops=dict(arrowstyle="->", lw=2.0, color="#34495e"))

    ax.set_title("Figure 2: Five-Stage Causal-Stochastic Simulation Pipeline (IPWRA + Two-Stage MVE/GRKS)", fontsize=11, fontweight="bold", pad=6)
    save_fig(fig, "fig2_causal_stochastic_workflow")


# -----------------------------------------------------------------------------
# FIGURE 3: UVE / MVE VALIDATION PDFs
# -----------------------------------------------------------------------------

def make_fig3():
    df = pd.read_parquet(os.path.join(OUTPUTS_DIR, "data", "ipwra_balanced_panel.parquet"))
    t3 = pd.read_csv(os.path.join(OUTPUTS_DIR, "tables", "table3_model_validation_uve_mve.csv"))
    npz = np.load(os.path.join(OUTPUTS_DIR, "data", "mve_simulation_draws.npz"))

    dr_path = os.path.join(OUTPUTS_DIR, "tables", "dr_potential_outcome_means.csv")
    dr_scales = {}
    if os.path.exists(dr_path):
        ddf = pd.read_csv(dr_path)
        dr_scales = {(r["crop_group"], r["regime"]): float(r["dr_scale"]) for _, r in ddf.iterrows()}

    fig, axes = plt.subplots(1, 3, figsize=(14.5, 4.6))
    for ax, crop in zip(axes, ("Maize", "Paddy", "Legumes")):
        regs = [r for r in ("M0", "M1", "M2", "M3", "M2_M3") if f"{crop}__{r}__y_mve" in npz]
        ks_notes = []
        for r in regs:
            sub_r = df[(df["crop_group"] == crop) & (df["model_regime"] == r) & df["yield_t_ha"].notna()]
            obs = sub_r["yield_t_ha"].to_numpy() * dr_scales.get((crop, r), 1.0)
            w_obs = sub_r["ipw_weight"].to_numpy()
            y_mve = npz[f"{crop}__{r}__y_mve"]
            ks_row = t3[(t3["Crop"] == crop) & (t3["Regime"] == r) & (t3["Series"] == "Stage2_MVE")].iloc[0]
            col = REGIME_COLORS[r]
            r_lbl = r.replace("M2_M3", "M2/M3")
            sns.ecdfplot(x=obs, weights=w_obs, ax=ax, label=f"{r_lbl} Obs", color=col, lw=1.6, alpha=0.8)
            sns.ecdfplot(x=y_mve, ax=ax, label=f"{r_lbl} MVE", color=col, lw=1.6, ls="--")
            ks_notes.append(f"{r_lbl}: D={ks_row['KS_D_vs_Obs']:.3f}")

        ax.set_title(f"{crop} Validation\n" + ", ".join(ks_notes), fontweight="bold", fontsize=8.5)
        ax.set_xlabel("Yield (t/ha)")
        ax.set_ylabel("Cumulative Probability")
        ax.set_xlim(0, 5.0 if crop != "Legumes" else 3.0)
        ax.legend(frameon=False, fontsize=6.5, ncol=2)

    fig.suptitle("Figure 3: IPWRA-Weighted Empirical vs. Stage 2 MVE Simulated Yield Distributions Across All Regimes", fontsize=11, fontweight="bold", y=1.03)
    plt.tight_layout()
    save_fig(fig, "fig3_uve_mve_validation_pdfs")


# -----------------------------------------------------------------------------
# FIGURE 4: 2x3 NFI & RETURN TO LABOR PDFs
# -----------------------------------------------------------------------------

def make_fig4():
    npz = np.load(os.path.join(OUTPUTS_DIR, "data", "mve_simulation_draws.npz"))
    fig, axes = plt.subplots(2, 3, figsize=(14.0, 7.6))

    for col_i, crop in enumerate(("Maize", "Paddy", "Legumes")):
        regs = [r for r in ("M0", "M1", "M2", "M3", "M2_M3") if f"{crop}__{r}__nfi" in npz]
        ax_top, ax_bot = axes[0, col_i], axes[1, col_i]

        for r in regs:
            nfi_m = npz[f"{crop}__{r}__nfi"] / 1e6
            rl_k = npz[f"{crop}__{r}__ret_labor"] / 1e3
            r_lbl = r.replace("M2_M3", "M2/M3")
            rt_nfi = 100.0 * float(np.mean(nfi_m > 4.0))
            rt_rl = 100.0 * float(np.mean(rl_k > 45.0))
            sns.kdeplot(np.clip(nfi_m, -1.5, 5.0), ax=ax_top, label=f"{r_lbl} (>{4.0:.0f}M: {rt_nfi:.1f}%)", color=REGIME_COLORS[r], lw=1.8)
            sns.kdeplot(np.clip(rl_k, -10, 60), ax=ax_bot, label=f"{r_lbl} (>45k: {rt_rl:.1f}%)", color=REGIME_COLORS[r], lw=1.8)

        r_cut, g_cut = (0.8, 1.8) if crop == "Paddy" else (0.6, 1.2)
        ax_top.axvline(r_cut, color="#c0392b", ls="--", lw=1.1, label="Red Cutoff")
        ax_top.axvline(g_cut, color="#27ae60", ls="--", lw=1.1, label="Green Cutoff")
        ax_top.set_title(f"{crop}: Net Farm Income (M TZS/ha)", fontweight="bold")
        ax_top.set_xlabel("NFI (Million TZS/ha)")
        ax_top.set_xlim(-1.0, 4.0)
        ax_top.legend(frameon=False, fontsize=7.5)

        ax_bot.axvline(7.0, color="#c0392b", ls="--", lw=1.1, label="7k/day (Drudgery)")
        ax_bot.axvline(12.0, color="#27ae60", ls="--", lw=1.1, label="12k/day (Target)")
        ax_bot.set_title(f"{crop}: Return to Labor (k TZS/day)", fontweight="bold")
        ax_bot.set_xlabel("Return to Labor (Thousand TZS/person-day)")
        ax_bot.set_xlim(-5, 45)
        ax_bot.legend(frameon=False, fontsize=7.5)

    fig.suptitle("Figure 4: Simulated Net Farm Income and Return to Labor Probability Density Functions", fontsize=12, fontweight="bold", y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    save_fig(fig, "fig4_nfi_and_labor_return_pdfs")


# -----------------------------------------------------------------------------
# FIGURE 5: STOPLIGHT NFI BY AEZ (MAIZE & PADDY)
# -----------------------------------------------------------------------------

def make_fig5():
    df = pd.read_parquet(os.path.join(OUTPUTS_DIR, "data", "ipwra_balanced_panel.parquet"))
    rows = []
    for crop in ("Maize", "Paddy", "Legumes"):
        df_c = df[df["crop_group"] == crop]
        r_cut, g_cut = (800_000.0, 1_800_000.0) if crop == "Paddy" else (600_000.0, 1_200_000.0)
        for aez_id in range(1, 10):
            res_a = sim_mod.simulate_crop_stratum(df_c, aez_code=aez_id)
            if res_a is None:
                continue
            for j, r in enumerate(res_a["regimes"]):
                if res_a["insufficient"][r]:
                    continue
                red, yel, grn = sim_mod.stoplight_probs(res_a["nfi"][:, j], r_cut, g_cut)
                rows.append({"Crop": crop, "AEZ": f"AEZ {aez_id}", "Regime": r.replace("M2_M3", "M2/M3"), "Red": red, "Yellow": yel, "Green": grn})
    sdf = pd.DataFrame(rows)

    fig, axes = plt.subplots(1, 3, figsize=(16.5, 6.2), sharey=False)
    for ax, crop in zip(axes, ("Maize", "Paddy", "Legumes")):
        sub = sdf[sdf["Crop"] == crop].copy()
        sub["Label"] = sub["AEZ"] + " | " + sub["Regime"]
        sub = sub.iloc[::-1]
        ax.barh(sub["Label"], sub["Red"], color="#e74c3c", label="Red (Loss/Low)")
        ax.barh(sub["Label"], sub["Yellow"], left=sub["Red"], color="#f1c40f", label="Yellow (Moderate)")
        ax.barh(sub["Label"], sub["Green"], left=sub["Red"] + sub["Yellow"], color="#2ecc71", label="Green (High Return)")
        ax.set_title(f"{crop}: NFI Stoplight by AEZ × Regime", fontweight="bold")
        ax.set_xlabel("Probability (%)")
        ax.set_xlim(0, 100)
        ax.tick_params(axis="y", labelsize=7.0)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.94), ncol=3, frameon=False, fontsize=9)
    fig.suptitle(r"Figure 5: Agroecological Zone (AEZ 1–9) Stoplight Risk Profiles for Net Farm Income (Cells with $n \geq 30$, $N_{\mathrm{eff}} \geq 20$)", fontsize=11.5, fontweight="bold", y=0.99)
    plt.tight_layout(rect=[0, 0, 1, 0.90])
    save_fig(fig, "fig5_stoplight_nfi_by_aez")


# -----------------------------------------------------------------------------
# FIGURE 6: STOPLIGHT LABOR RETURN BY PLOT SIZE & SHOCK
# -----------------------------------------------------------------------------

def make_fig6():
    t6 = pd.read_csv(os.path.join(OUTPUTS_DIR, "tables", "table6_stoplight_sensitivity_scenarios.csv"))
    scenarios = ["Baseline", "Shock_Plus30pct_Fuel_Hire", "Shock_Minus10pct_Price", "Scale_Small_lt_1ha", "Scale_Medium_1_3ha", "Scale_Large_gt_3ha"]
    sub = t6[t6["Scenario"].isin(scenarios)].copy()
    scen_map = {
        "Baseline": "Baseline",
        "Shock_Plus30pct_Fuel_Hire": "+30% Fuel/Hire",
        "Shock_Minus10pct_Price": "−10% Output Price",
        "Scale_Small_lt_1ha": "< 1 ha",
        "Scale_Medium_1_3ha": "1–3 ha",
        "Scale_Large_gt_3ha": "> 3 ha",
    }

    fig, axes = plt.subplots(1, 3, figsize=(16.5, 6.8), sharey=False)
    for ax, crop in zip(axes, ("Maize", "Paddy", "Legumes")):
        sc = sub[sub["Crop"] == crop].copy()
        sc["Label"] = sc["Scenario"].map(scen_map) + " | " + sc["Regime"].str.replace("M2_M3", "M2/M3", regex=False)
        sc = sc.iloc[::-1]
        ax.barh(sc["Label"], sc["Labor_Red_pct"], color="#e74c3c", label="Red (< 7,000 TZS/day)")
        ax.barh(sc["Label"], sc["Labor_Yellow_pct"], left=sc["Labor_Red_pct"], color="#f1c40f", label="Yellow (7,000–12,000 TZS/day)")
        ax.barh(sc["Label"], sc["Labor_Green_pct"], left=sc["Labor_Red_pct"] + sc["Labor_Yellow_pct"], color="#2ecc71", label="Green (> 12,000 TZS/day)")
        ax.set_title(f"{crop}: Return to Labor Stoplight", fontweight="bold")
        ax.set_xlabel("Probability (%)")
        ax.set_xlim(0, 100)
        ax.tick_params(axis="y", labelsize=7.5)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.94), ncol=3, frameon=False, fontsize=9)
    fig.suptitle("Figure 6: Return to Labor Stoplight Across Plot-Size Thresholds, +30% Fuel/Hire, and −10% Output Price Shocks", fontsize=11.5, fontweight="bold", y=0.99)
    plt.tight_layout(rect=[0, 0, 1, 0.90])
    save_fig(fig, "fig6_stoplight_labor_by_plot_size")


def make_fig_s1_gps_overlap():
    """3x3 grid (3 crops x 3 regimes) comparing p_j(X_i) for D_i = j vs. D_i != j."""
    df = pd.read_parquet(os.path.join(OUTPUTS_DIR, "data", "ipwra_balanced_panel.parquet"))
    fig, axes = plt.subplots(3, 3, figsize=(13.5, 10.5), sharex=True)
    crops = ("Maize", "Paddy", "Legumes")
    regimes = ("M0", "M1", "M2_M3")
    for row_i, crop in enumerate(crops):
        sub = df[df["crop_group"] == crop]
        for col_j, r in enumerate(regimes):
            ax = axes[row_i, col_j]
            gps_col = f"gps_{r}"
            r_lbl = r.replace("M2_M3", "M2/M3")
            in_r = sub.loc[sub["model_regime"] == r, gps_col].dropna()
            out_r = sub.loc[sub["model_regime"] != r, gps_col].dropna()
            if len(in_r) > 10:
                sns.kdeplot(in_r, ax=ax, label=f"$D_i = {r_lbl}$", color=REGIME_COLORS[r], lw=1.8, fill=True, alpha=0.22)
            if len(out_r) > 10:
                sns.kdeplot(out_r, ax=ax, label=f"$D_i \\neq {r_lbl}$", color="#34495e", lw=1.5, ls="--", fill=False)
            ax.axvline(0.02, color="#7f8c8d", ls=":", lw=0.9)
            ax.axvline(0.98, color="#7f8c8d", ls=":", lw=0.9)
            ax.set_title(f"{crop}: $p_{{{r_lbl}}}(X_i)$", fontweight="bold", fontsize=9.5)
            ax.set_xlim(0, 1.0)
            if row_i == 2:
                ax.set_xlabel("Generalized Propensity Score $p_j(X_i)$")
            if col_j == 0:
                ax.set_ylabel("Density")
            else:
                ax.set_ylabel("")
            ax.legend(frameon=False, fontsize=7.5)
    fig.suptitle("Figure S1: Regime-Specific Generalized Propensity Score Overlap ($D_i = j$ vs. $D_i \\neq j$)", fontsize=12, fontweight="bold", y=0.985)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    save_fig(fig, "fig_s1_gps_overlap")


def main():
    print("================================================================================")
    print(" STEP 6: GENERATING PUBLICATION-GRADE 300-DPI FIGURES (PNG + PDF + TIFF)")
    print("================================================================================")
    make_fig1()
    print("[1/7] Saved fig1_tanzania_mechanization_map")
    make_fig2()
    print("[2/7] Saved fig2_causal_stochastic_workflow")
    make_fig3()
    print("[3/7] Saved fig3_uve_mve_validation_pdfs")
    make_fig4()
    print("[4/7] Saved fig4_nfi_and_labor_return_pdfs")
    make_fig5()
    print("[5/7] Saved fig5_stoplight_nfi_by_aez")
    make_fig6()
    print("[6/7] Saved fig6_stoplight_labor_by_plot_size")
    make_fig_s1_gps_overlap()
    print("[7/7] Saved fig_s1_gps_overlap")
    print("================================================================================")


if __name__ == "__main__":
    main()
