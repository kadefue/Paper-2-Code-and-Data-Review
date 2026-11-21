#!/usr/bin/env python3
"""
src/02_harmonize_panel.py
=========================
Step 2 of Study 2: Harmonization, Unit Standardization, Imputation, Winsorization,
AEZ Yield Normalization (beta_y0), and Tables 1-2 Generation.

Harmonizes plot-level observations for Maize, Paddy, and Legumes across:
  - NCSA 2019/20 (plot-level R081/R082 for baseline yields/prices/costs;
    household-level R000_SOV + R122 + R121 + R041 for M0-M3 farm/area shares)
  - AASS 2022/23 (full plot-level Maize/Paddy/Legumes + M0/M1/M3 + K/L/B costs + IPWRA covariates)
  - AASS 2023/24 (plot-level Maize/Paddy/Legumes; machinery roster absent on disk)
  - AASS 2024/25 (plot-level Maize/Paddy/Legumes; machinery roster absent on disk)

Exports:
  - outputs/data/harmonized_mechanization_panel.parquet
  - outputs/tables/table1_zonal_mechanization_distribution.csv & .md
  - outputs/tables/table2_mechanization_transition_cagr.csv & .md

Usage:
  .venv/bin/python src/02_harmonize_panel.py
"""

import os
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
OUT_DATA_DIR = os.path.join(OUTPUTS_DIR, "data")
OUT_TABLES_DIR = os.path.join(OUTPUTS_DIR, "tables")
os.makedirs(OUT_DATA_DIR, exist_ok=True)
os.makedirs(OUT_TABLES_DIR, exist_ok=True)

ACRE_TO_HA = 0.404686
REGIMES = ("M0", "M1", "M2", "M3")
CROPS = ("Maize", "Paddy", "Legumes")

# Official World Bank WDI / NBS Tanzania CPI (2010 = 100), rebased to 2022/23 avg (210.52)
CPI_2010_BASE = {
    2008: 83.97,
    2010: 100.00,
    2012: 130.72,
    2014: 149.66,
    2019: 187.58,
    2020: 193.60,
    2022: 206.60,
    2023: 214.45,
}
TARGET_CPI_2022_23 = 210.52

# 9 Tanzanian Agroecological Zones (AEZs) + Zanzibar (56)
REGION_TO_AEZ = {}
AEZ_DEFINITIONS = [
    (1, "Central Semi-Arid", [1, 13]),
    (2, "Northern Highlands", [2, 3, 21]),
    (3, "Southern Highlands", [10, 11, 12, 15, 22, 23, 26]),
    (4, "Lake Victoria Basin", [17, 18, 19, 20, 24, 25]),
    (5, "Western Miombo", [14, 16]),
    (6, "Eastern Coastal Lowlands", [5, 6, 7]),
    (7, "Southern Coastal Lowlands", [8, 9]),
    (8, "Northern Coastal Lowlands", [4]),
    (9, "Zanzibar Archipelago", [51, 52, 53, 54, 55, 56]),
]
for aez_code, aez_name, reg_list in AEZ_DEFINITIONS:
    for r in reg_list:
        REGION_TO_AEZ[r] = (aez_code, aez_name)

WAVE_CROP_MAP = {
    "NCSA_2019_20": {11: "Maize", 12: "Paddy", 31: "Legumes", 32: "Legumes", 33: "Legumes", 34: "Legumes", 35: "Legumes", 36: "Legumes", 37: "Legumes", 43: "Legumes", 47: "Legumes"},
    "AASS_2022_23": {11: "Maize", 12: "Paddy", 31: "Legumes", 32: "Legumes", 34: "Legumes", 35: "Legumes", 43: "Legumes", 9930: "Legumes"},
    "AASS_2023_24": {11: "Maize", 12: "Paddy", 31: "Legumes", 32: "Legumes", 34: "Legumes", 35: "Legumes", 43: "Legumes", 9930: "Legumes"},
    "AASS_2024_25": {11: "Maize", 12: "Paddy", 31: "Legumes", 32: "Legumes", 33: "Legumes", 34: "Legumes", 35: "Legumes", 36: "Legumes", 37: "Legumes", 43: "Legumes", 47: "Legumes"},
}


def map_aez(region_series):
    """Maps numeric NBS region codes to (aez_code, aez_name)."""
    codes = pd.to_numeric(region_series, errors="coerce")
    aez_code = codes.map(lambda x: REGION_TO_AEZ.get(int(x), (np.nan, "Unknown"))[0] if pd.notna(x) else np.nan)
    aez_name = codes.map(lambda x: REGION_TO_AEZ.get(int(x), (np.nan, "Unknown"))[1] if pd.notna(x) else "Unknown")
    return aez_code, aez_name


def weighted_mean(values, weights):
    """Computes weighted mean ignoring NaNs and non-positive weights."""
    mask = pd.notna(values) & pd.notna(weights) & (weights > 0)
    if not mask.any():
        return np.nan
    return float(np.average(values[mask], weights=weights[mask]))


def weighted_median(values, weights):
    """Computes weighted median ignoring NaNs and non-positive weights."""
    mask = pd.notna(values) & pd.notna(weights) & (weights > 0)
    if not mask.any():
        return np.nan
    v = np.asarray(values[mask], dtype=float)
    w = np.asarray(weights[mask], dtype=float)
    idx = np.argsort(v)
    v, w = v[idx], w[idx]
    cumw = np.cumsum(w)
    cutoff = 0.5 * cumw[-1]
    return float(v[np.searchsorted(cumw, cutoff)])


def impute_and_flag_costs(df, cols):
    """
    Imputes missing or negative cost/price values using Crop x AEZ x Regime
    weighted medians (with Crop x AEZ and Crop fallbacks) and records *_imputed flags.
    """
    df = df.copy()
    for col in cols:
        flag_col = f"{col}_imputed"
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df.loc[df[col] < 0, col] = np.nan
        df[flag_col] = df[col].isna()

        if not df[flag_col].any():
            continue

        # Compute weighted medians at 3 hierarchy levels
        med_car = {}
        for keys, grp in df.groupby(["crop_group", "aez_code", "regime"], dropna=False):
            m = weighted_median(grp[col], grp["weight"])
            if pd.notna(m):
                med_car[keys] = m

        med_ca = {}
        for keys, grp in df.groupby(["crop_group", "aez_code"], dropna=False):
            m = weighted_median(grp[col], grp["weight"])
            if pd.notna(m):
                med_ca[keys] = m

        med_c = {}
        for crop, grp in df.groupby("crop_group"):
            m = weighted_median(grp[col], grp["weight"])
            med_c[crop] = m if pd.notna(m) else 0.0

        miss_idx = df.index[df[flag_col]]
        imputed_vals = []
        for idx in miss_idx:
            row = df.loc[idx]
            val = med_car.get((row["crop_group"], row["aez_code"], row["regime"]))
            if val is None:
                val = med_ca.get((row["crop_group"], row["aez_code"]))
            if val is None:
                val = med_c.get(row["crop_group"], 0.0)
            imputed_vals.append(max(0.0, float(val)))
        df.loc[miss_idx, col] = imputed_vals

    return df


def winsorize_by_group(df, cols, group_cols, lower=0.01, upper=0.99):
    """Winsorizes continuous variables at 1st/99th percentiles within groups."""
    df = df.copy()
    for col in cols:
        if col not in df.columns:
            continue
        if not df[col].notna().any():
            continue
        grp_sizes = df.groupby(group_cols)[col].transform("count")
        q_low = df.groupby(group_cols)[col].transform(lambda s: s.quantile(lower))
        q_high = df.groupby(group_cols)[col].transform(lambda s: s.quantile(upper))
        fb_low = df.groupby("crop_group")[col].transform(lambda s: s.quantile(lower))
        fb_high = df.groupby("crop_group")[col].transform(lambda s: s.quantile(upper))
        lo = np.where(grp_sizes >= 10, q_low, fb_low)
        hi = np.where(grp_sizes >= 10, q_high, fb_high)
        df[col] = np.clip(df[col], lo, hi)
    return df


# -----------------------------------------------------------------------------
# 1. NCSA 2019/20 HARMONIZATION
# -----------------------------------------------------------------------------

def get_ncsa_region_dist_km():
    """Computes region-level median distance to road/market (km) from NCSA R310."""
    ncsa_dir = os.path.join(DATA_DIR, "NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI")
    r310 = pd.read_stata(os.path.join(ncsa_dir, "R310_ACCESS_INFRASTUCTURE.dta"), columns=["region", "q310c2"], convert_categoricals=False)
    r310["q310c2"] = pd.to_numeric(r310["q310c2"], errors="coerce")
    r310 = r310[(r310["q310c2"] >= 0) & (r310["q310c2"] < 500)]
    return r310.groupby("region")["q310c2"].median().to_dict()


def load_ncsa_2019_plots():
    """Loads NCSA 2019/20 plot-crop observations (R081 + R082) for Maize, Paddy, Legumes."""
    ncsa_dir = os.path.join(DATA_DIR, "NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI")
    cmap = WAVE_CROP_MAP["NCSA_2019_20"]
    reg_dist = get_ncsa_region_dist_km()

    r82_cols = [
        "region", "district", "finalweight_hh", "q821c4",
        "q821c6", "q821c7a", "q821c7b", "q821c8f", "q821c9a", "q821c9e", "q821c9f",
        "q821c15", "q821c20", "q821c25", "q821c30", "q821c35", "q821c39",
    ]
    df82 = pd.read_stata(os.path.join(ncsa_dir, "R082_LONG_RAINY_SEASON.dta"), columns=r82_cols, convert_categoricals=False)
    df82 = df82.rename(columns={
        "q821c4": "crop_code", "q821c6": "land_prep_tzs", "q821c7a": "planted_acres",
        "q821c7b": "plant_tzs", "q821c8f": "weed_tzs", "q821c9a": "harvested_acres",
        "q821c9e": "prod_kg", "q821c9f": "harv_tzs", "q821c15": "seed_tzs",
        "q821c20": "fert_tzs", "q821c25": "herb_tzs", "q821c30": "fung_tzs",
        "q821c35": "insect_tzs", "q821c39": "price_tzs_kg",
    })
    df82["season"] = "Long_Masika"

    r81_cols = [
        "region", "district", "finalweight_hh", "q811c4",
        "q811c6", "q811c7a", "q811c7b", "q811c8f", "q811c9a", "q811c9e", "q811c9f",
        "q811c15", "q811c20", "q811c25", "q811c30", "q811c35", "q811c39",
    ]
    df81 = pd.read_stata(os.path.join(ncsa_dir, "R081_SHORT_RAINY_SEASON.dta"), columns=r81_cols, convert_categoricals=False)
    df81 = df81.rename(columns={
        "q811c4": "crop_code", "q811c6": "land_prep_tzs", "q811c7a": "planted_acres",
        "q811c7b": "plant_tzs", "q811c8f": "weed_tzs", "q811c9a": "harvested_acres",
        "q811c9e": "prod_kg", "q811c9f": "harv_tzs", "q811c15": "seed_tzs",
        "q811c20": "fert_tzs", "q811c25": "herb_tzs", "q811c30": "fung_tzs",
        "q811c35": "insect_tzs", "q811c39": "price_tzs_kg",
    })
    df81["season"] = "Short_Vuli"

    df = pd.concat([df82, df81], ignore_index=True)
    df["crop_group"] = df["crop_code"].map(cmap)
    df = df[df["crop_group"].notna()].copy()

    df["wave"] = "NCSA_2019_20"
    df["year"] = 2019
    df["hh_id"] = np.nan
    df["weight"] = pd.to_numeric(df["finalweight_hh"], errors="coerce")
    df["aez_code"], df["aez_name"] = map_aez(df["region"])
    df["planted_ha"] = pd.to_numeric(df["planted_acres"], errors="coerce") * ACRE_TO_HA
    df["harvested_ha"] = pd.to_numeric(df["harvested_acres"], errors="coerce") * ACRE_TO_HA
    df["production_t"] = pd.to_numeric(df["prod_kg"], errors="coerce") / 1000.0
    df["yield_t_ha"] = np.where(df["planted_ha"] > 0, df["production_t"] / df["planted_ha"], np.nan)
    df["price_tzs_t"] = np.where(pd.to_numeric(df["price_tzs_kg"], errors="coerce") > 0, pd.to_numeric(df["price_tzs_kg"], errors="coerce") * 1000.0, np.nan)

    for c in ["land_prep_tzs", "plant_tzs", "weed_tzs", "harv_tzs", "seed_tzs", "fert_tzs", "herb_tzs", "fung_tzs", "insect_tzs"]:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)

    df["mech_cost_tzs_ha"] = np.where(df["planted_ha"] > 0, df["land_prep_tzs"] / df["planted_ha"], np.nan)
    df["labor_cost_tzs_ha"] = np.where(df["planted_ha"] > 0, (df["plant_tzs"] + df["weed_tzs"] + df["harv_tzs"]) / df["planted_ha"], np.nan)
    df["person_days_ha"] = np.nan
    df["biochem_cost_tzs_ha"] = np.where(df["planted_ha"] > 0, (df["seed_tzs"] + df["fert_tzs"] + df["herb_tzs"] + df["fung_tzs"] + df["insect_tzs"]) / df["planted_ha"], np.nan)
    df["regime"] = "Unobserved_Plot_Level"
    df["multi_power_flag"] = False

    # Covariates (placeholders for schema alignment; causal IPWRA uses AASS 22/23)
    df["log_plot_size_ha"] = np.log1p(df["planted_ha"].clip(lower=0))
    df["log_total_farm_size_ha"] = np.nan
    df["hh_head_age"] = np.nan
    df["hh_head_sex"] = np.nan
    df["hh_head_edu"] = np.nan
    df["hh_size"] = np.nan
    df["asset_index"] = np.nan
    df["draught_livestock_count"] = np.nan
    df["credit_access"] = np.nan
    df["extension_contact"] = np.nan
    df["soil_type"] = np.nan
    df["erosion_or_slope_flag"] = np.nan
    df["dist_road_market_km"] = df["region"].map(reg_dist)

    return df


def load_ncsa_2019_hh_regimes():
    """Loads NCSA 2019/20 household-level M0-M3 regimes and land area for Tables 1-2."""
    ncsa_dir = os.path.join(DATA_DIR, "NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI")
    sov = pd.read_stata(os.path.join(ncsa_dir, "R000_SOV.dta"), columns=["HHID", "region", "finalweight_hh"], convert_categoricals=False)
    r122 = pd.read_stata(os.path.join(ncsa_dir, "R122_USE_TRACTOR_ANIMALS.dta"), columns=["HHID", "q122c0", "q122c3"], convert_categoricals=False)
    r121 = pd.read_stata(os.path.join(ncsa_dir, "R121_FARM_IMPLEMENTS.dta"), columns=["HHID", "q121c0", "q121c2"], convert_categoricals=False)
    r041 = pd.read_stata(os.path.join(ncsa_dir, "R041_LAND_OWNERSHIP.dta"), columns=["HHID", "q4_1_c2"], convert_categoricals=False)

    hh_land = r041.groupby("HHID")["q4_1_c2"].sum() * ACRE_TO_HA
    hh_powers = {hid: set() for hid in sov["HHID"]}

    used122 = r122[r122["q122c3"] > 0]
    for hid, code in zip(used122["HHID"], used122["q122c0"]):
        if hid not in hh_powers:
            continue
        if code in (1, 2, 3, 4):
            hh_powers[hid].add("M1")
        elif code == 6:
            hh_powers[hid].add("M2")
        elif code == 5:
            hh_powers[hid].add("M3")

    used121 = r121[r121["q121c2"] == 1]
    for hid, code in zip(used121["HHID"], used121["q121c0"]):
        if hid not in hh_powers:
            continue
        if code in (4, 5, 6, 7, 13):
            hh_powers[hid].add("M1")
        elif code == 12:
            hh_powers[hid].add("M2")
        elif code in (8, 9, 10):
            hh_powers[hid].add("M3")

    def pick(pset):
        if "M3" in pset:
            return "M3"
        if "M2" in pset:
            return "M2"
        if "M1" in pset:
            return "M1"
        return "M0"

    sov["regime"] = [pick(hh_powers[h]) for h in sov["HHID"]]
    sov["multi_power_flag"] = [len(hh_powers[h]) > 1 for h in sov["HHID"]]
    sov["farm_ha"] = sov["HHID"].map(hh_land).fillna(0.0)
    sov["aez_code"], sov["aez_name"] = map_aez(sov["region"])
    sov["weight"] = pd.to_numeric(sov["finalweight_hh"], errors="coerce")
    return sov


# -----------------------------------------------------------------------------
# 2. AASS 2022/23, 2023/24, 2024/25 HARMONIZATION
# -----------------------------------------------------------------------------

def load_aass_2022_plots():
    """
    Harmonizes AASS 2022/23 plot-crop data with M0/M1/M3 regimes (combining
    items_services.dta rental + AASS2023.dta draught/equipment loan indicators),
    hired + shadow-valued family labor, K/B costs, and full IPWRA covariates.
    """
    d22 = os.path.join(DATA_DIR, "AASS 2022_2023")
    cmap = WAVE_CROP_MAP["AASS_2022_23"]
    reg_dist = get_ncsa_region_dist_km()

    mc = pd.read_stata(os.path.join(d22, "masikacrop.dta"), columns=["holding_id", "Weight", "region", "FIELD__id", "MASIKAPLOT__id", "crop_id", "areaPlanted", "areaHarvested", "production_kg"], convert_categoricals=False)
    mc["season"] = "Long_Masika"
    mc = mc.rename(columns={"MASIKAPLOT__id": "plot_id"})

    vc = pd.read_stata(os.path.join(d22, "vulicrop.dta"), columns=["holding_id", "Weight", "region", "FIELD__id", "VULIPLOT__id", "crop_id", "areaPlanted", "areaHarvested", "production_kg"], convert_categoricals=False)
    vc["season"] = "Short_Vuli"
    vc = vc.rename(columns={"VULIPLOT__id": "plot_id"})

    df = pd.concat([mc, vc], ignore_index=True)
    df["crop_group"] = df["crop_id"].map(cmap)
    df = df[df["crop_group"].notna()].copy()

    # Holding-level core & covariates from AASS2023.dta (filter strictly to smallholder households: holding_type == 2)
    a23 = pd.read_stata(
        os.path.join(d22, "AASS2023.dta"),
        columns=["holding_id", "holding_type", "region", "holding_head_sex", "holding_head_age", "s19q04a", "s19q05", "s19q06a", "s19q07__3", "s19q07__4", "s2q10__1", "s2q10__5", "s20q01"],
        convert_categoricals=False,
    ).rename(columns={"region": "region_a23"})
    a23 = a23[a23["holding_type"] == 2].copy()
    df = df.merge(a23, on="holding_id", how="inner")
    df["region"] = df["region"].fillna(df["region_a23"])
    df = df[df["region"].notna() & (df["region"] != 27)].copy()

    # Household roster: head education (numeric years), hh_size, and family crop labor person-days
    hh = pd.read_stata(
        os.path.join(d22, "household.dta"),
        columns=["holding_id", "s2q03", "s2q07", "s2q08", "s18q04__1", "s18q05a", "s18q05b", "s18q05c"],
        convert_categoricals=False,
    )
    hh_size_map = hh.groupby("holding_id").size()
    aass_edu_map = {90: 0.0, 91: 7.0, 92: 11.0, 93: 12.0, 94: 14.0, 95: 16.0}
    hh_heads = hh[hh["s2q03"] == 1].groupby("holding_id").first()
    fb_edu = pd.Series(np.where(hh_heads["s2q07"] == 1, 7.0, 0.0), index=hh_heads.index)
    heads_edu = np.where(hh_heads["s2q07"] == 0, 0.0, hh_heads["s2q08"].map(aass_edu_map).fillna(fb_edu))
    heads_edu_map = dict(zip(hh_heads.index, heads_edu))
    hh["fam_days"] = np.where(
        hh["s18q04__1"] == 1,
        pd.to_numeric(hh["s18q05a"], errors="coerce").fillna(0)
        * pd.to_numeric(hh["s18q05b"], errors="coerce").fillna(0)
        * (pd.to_numeric(hh["s18q05c"], errors="coerce").fillna(8.0) / 8.0),
        0.0,
    )
    fam_days_hh = hh.groupby("holding_id")["fam_days"].sum()

    # Field size & tenure
    fld = pd.read_stata(os.path.join(d22, "field.dta"), columns=["holding_id", "FIELD__id", "s3q03", "s3q04a_acres"], convert_categoricals=False)
    farm_ha_hh = fld.groupby("holding_id")["s3q04a_acres"].sum() * ACRE_TO_HA

    # Plot organic amendment / irrigation structure (masikaplot / vuliplot)
    mp = pd.read_stata(os.path.join(d22, "masikaplot.dta"), columns=["holding_id", "FIELD__id", "MASIKAPLOT__id", "s6q04", "s6q05a", "s6q07"], convert_categoricals=False).rename(columns={"MASIKAPLOT__id": "plot_id"})
    mp["season"] = "Long_Masika"
    vp = pd.read_stata(os.path.join(d22, "vuliplot.dta"), columns=["holding_id", "FIELD__id", "VULIPLOT__id", "s4q04", "s4q05a", "s4q07"], convert_categoricals=False).rename(columns={"VULIPLOT__id": "plot_id", "s4q04": "s6q04", "s4q05a": "s6q05a", "s4q07": "s6q07"})
    vp["season"] = "Short_Vuli"
    plots_meta = pd.concat([mp, vp], ignore_index=True).groupby(["holding_id", "FIELD__id", "plot_id", "season"], as_index=False).first()
    df = df.merge(plots_meta, on=["holding_id", "FIELD__id", "plot_id", "season"], how="left")

    # Mechanization regime: items_services.dta + AASS2023 draught/equipment indicators
    srv = pd.read_stata(os.path.join(d22, "items_services.dta"), columns=["holding_id", "items_service__id", "s19q01b", "s19q02"], convert_categoricals=False)
    paid = srv[srv["s19q01b"] == 1].copy()
    paid["s19q02"] = pd.to_numeric(paid["s19q02"], errors="coerce").fillna(0.0)

    hh_powers = {hid: set() for hid in df["holding_id"].unique()}
    for hid, sid in zip(paid["holding_id"], paid["items_service__id"]):
        if hid not in hh_powers:
            continue
        if sid == 1:
            hh_powers[hid].add("M1")
        elif sid in (4, 5, 14):
            hh_powers[hid].add("M3")

    # Add owned/loan-financed draught power (s19q07__4) and farm equipment (s19q07__3)
    for hid, dp, eq in zip(a23["holding_id"], a23["s19q07__4"], a23["s19q07__3"]):
        if hid not in hh_powers:
            continue
        if dp == 1:
            hh_powers[hid].add("M1")
        if eq == 1 and "M3" not in hh_powers[hid] and "M1" not in hh_powers[hid]:
            hh_powers[hid].add("M1")

    df["regime"] = df["holding_id"].map(lambda h: "M3" if "M3" in hh_powers.get(h, ()) else ("M1" if "M1" in hh_powers.get(h, ()) else "M0"))
    df["multi_power_flag"] = df["holding_id"].map(lambda h: len(hh_powers.get(h, ())) > 1)

    df["wave"] = "AASS_2022_23"
    df["year"] = 2022
    df["hh_id"] = df["holding_id"].astype(str)
    df["weight"] = pd.to_numeric(df["Weight"], errors="coerce")
    df["aez_code"], df["aez_name"] = map_aez(df["region"])

    df["planted_ha"] = pd.to_numeric(df["areaPlanted"], errors="coerce") * ACRE_TO_HA
    df["harvested_ha"] = pd.to_numeric(df["areaHarvested"], errors="coerce") * ACRE_TO_HA
    df["production_t"] = pd.to_numeric(df["production_kg"], errors="coerce") / 1000.0
    df["yield_t_ha"] = np.where(df["planted_ha"] > 0, df["production_t"] / df["planted_ha"], np.nan)

    hh_total_ha = df.groupby("holding_id")["planted_ha"].sum().replace(0, np.nan)
    df["hh_ha"] = df["holding_id"].map(hh_total_ha)

    # K: mechanization & draft power cost (items_service__id in [1, 4, 5, 14])
    k_hh = paid[paid["items_service__id"].isin([1, 4, 5, 14])].groupby("holding_id")["s19q02"].sum()
    df["mech_cost_tzs_ha"] = df["holding_id"].map(k_hh).fillna(0.0) / df["hh_ha"]

    # L: hired labor expenditure + shadow-valued family labor at AEZ median daily wage
    l_srv_hh = paid[paid["items_service__id"].isin([2, 13])].groupby("holding_id")["s19q02"].sum()
    ext = pd.read_stata(os.path.join(d22, "external_labor_activities.dta"), columns=["holding_id", "s18q06b", "s18q07", "s18q08", "s18q09"], convert_categoricals=False)
    ext = ext[ext["s18q06b"] == 1].copy()
    ext["pdays"] = pd.to_numeric(ext["s18q07"], errors="coerce").fillna(0) * pd.to_numeric(ext["s18q08"], errors="coerce").fillna(0) * pd.to_numeric(ext["s18q09"], errors="coerce").fillna(0)
    hired_pdays_hh = ext.groupby("holding_id")["pdays"].sum()

    df["hired_labor_tzs_ha"] = df["holding_id"].map(l_srv_hh).fillna(0.0) / df["hh_ha"]
    df["hired_pdays_ha"] = df["holding_id"].map(hired_pdays_hh).fillna(0.0) / df["hh_ha"]
    df["fam_pdays_ha"] = df["holding_id"].map(fam_days_hh).fillna(0.0) / df["hh_ha"]

    # Implied daily wage from hired labor where both > 0, aggregated by AEZ (fallback 1,800 TZS/day)
    valid_w = (df["hired_labor_tzs_ha"] > 0) & (df["hired_pdays_ha"] > 0)
    df["implied_wage"] = np.where(valid_w, df["hired_labor_tzs_ha"] / df["hired_pdays_ha"], np.nan)
    aez_wage = df.groupby("aez_code")["implied_wage"].median().clip(lower=1500.0, upper=4000.0).fillna(1800.0).to_dict()
    df["aez_daily_wage"] = df["aez_code"].map(aez_wage).fillna(1800.0)

    # Scale annual household family crop days by 0.45 for single-season plot allocation & bound to [15, 160] (plus [15, 220] sensitivity)
    raw_pdays = df["hired_pdays_ha"] + (0.45 * df["fam_pdays_ha"])
    raw_lcost = df["hired_labor_tzs_ha"] + (0.45 * df["fam_pdays_ha"] * df["aez_daily_wage"])
    bounded_pdays = np.clip(raw_pdays, 15.0, 160.0)
    bounded_pdays_220 = np.clip(raw_pdays, 15.0, 220.0)
    scale_l = np.where(raw_pdays > 0, bounded_pdays / raw_pdays, 1.0)
    df["person_days_ha"] = np.where(raw_pdays > 0, bounded_pdays, np.nan)
    df["person_days_ha_220"] = np.where(raw_pdays > 0, bounded_pdays_220, np.nan)
    df["labor_cost_tzs_ha"] = np.where(raw_pdays > 0, raw_lcost * scale_l, np.nan)

    # B: seeds + inputs
    seeds = pd.read_stata(os.path.join(d22, "seeds.dta"), columns=["holding_id", "crop_id", "s10q04"], convert_categoricals=False)
    seed_hh_crop = seeds.groupby(["holding_id", "crop_id"])["s10q04"].sum()
    inputs = pd.read_stata(os.path.join(d22, "inputs.dta"), columns=["holding_id", "s11q06a", "s11q06b"], convert_categoricals=False)
    inputs["val"] = pd.to_numeric(inputs["s11q06a"], errors="coerce").fillna(0) + pd.to_numeric(inputs["s11q06b"], errors="coerce").fillna(0)
    inp_hh = inputs.groupby("holding_id")["val"].sum()

    crop_ha = df.groupby(["holding_id", "crop_id"])["planted_ha"].transform("sum").replace(0, np.nan)
    seed_series = df.set_index(["holding_id", "crop_id"]).index.map(seed_hh_crop).to_numpy(dtype=float)
    seed_series = np.nan_to_num(seed_series, nan=0.0) / crop_ha.to_numpy(dtype=float)
    df["biochem_cost_tzs_ha"] = seed_series + (df["holding_id"].map(inp_hh).fillna(0.0) / df["hh_ha"])

    # Farmgate price (TZS/t)
    cu = pd.read_stata(os.path.join(d22, "crop_use.dta"), columns=["holding_id", "crop_id", "s9q02__1", "s9q03", "s9q04"], convert_categoricals=False)
    cu = cu[(cu["s9q02__1"] == 1) & (cu["s9q03"] > 0) & (cu["s9q04"] > 0)].copy()
    hh_crop_prod_t = df.groupby(["holding_id", "crop_id"])["production_t"].sum().rename("prod_t")
    cu = cu.join(hh_crop_prod_t, on=["holding_id", "crop_id"])
    cu["sold_t"] = cu["prod_t"] * (cu["s9q03"] / 100.0)
    cu["price_tzs_t"] = np.where(cu["sold_t"] > 0, cu["s9q04"] / cu["sold_t"], np.nan)
    price_map = cu.groupby(["holding_id", "crop_id"])["price_tzs_t"].median()
    df["price_tzs_t"] = df.set_index(["holding_id", "crop_id"]).index.map(price_map).to_numpy(dtype=float)

    # IPWRA covariates
    ext_srv_hh = set(paid.loc[paid["items_service__id"] == 9, "holding_id"])
    df["log_plot_size_ha"] = np.log1p(df["planted_ha"].clip(lower=0))
    df["log_total_farm_size_ha"] = np.log1p(df["holding_id"].map(farm_ha_hh).fillna(df["hh_ha"]).clip(lower=0))
    df["hh_head_age"] = pd.to_numeric(df["holding_head_age"], errors="coerce")
    df["hh_head_sex"] = np.where(pd.to_numeric(df["holding_head_sex"], errors="coerce") == 1, 1.0, 0.0)
    df["hh_head_edu"] = pd.to_numeric(df["holding_id"].map(heads_edu_map), errors="coerce")
    df["hh_size"] = pd.to_numeric(df["holding_id"].map(hh_size_map), errors="coerce")
    df["asset_index"] = (
        (pd.to_numeric(df["s19q05"], errors="coerce") == 1).astype(float)
        + (pd.to_numeric(df["s20q01"], errors="coerce") == 1).astype(float)
        + (pd.to_numeric(df["s2q10__5"], errors="coerce") == 1).astype(float)
    )
    df["draught_livestock_count"] = np.where(pd.to_numeric(df["s19q07__4"], errors="coerce") == 1, 1.0, 0.0)
    df["credit_access"] = np.where((df["s19q04a"] == 1) | (df["s19q06a"] == 1), 1.0, 0.0)
    df["extension_contact"] = np.where(df["holding_id"].isin(ext_srv_hh) | (df["s2q10__1"] == 1), 1.0, 0.0)
    df["soil_type"] = pd.to_numeric(df["s6q04"], errors="coerce").fillna(1.0)
    df["intercropped_flag"] = np.where(pd.to_numeric(df["s6q04"], errors="coerce") == 2, 1.0, 0.0)
    df["irrigated_flag"] = np.where(pd.to_numeric(df["s6q05a"], errors="coerce") == 1, 1.0, 0.0)
    df["is_gps_area"] = 0.0
    df["erosion_or_slope_flag"] = np.where(pd.to_numeric(df["s6q07"], errors="coerce") == 1, 1.0, 0.0)
    df["dist_road_market_km"] = df["region"].map(reg_dist).fillna(np.nanmedian(list(reg_dist.values())))

    return df


def load_aass_2023_plots():
    """Harmonizes AASS 2023/24 plot-crop data (machinery roster absent on disk)."""
    d23 = os.path.join(DATA_DIR, "AASS 2023_2024")
    cmap = WAVE_CROP_MAP["AASS_2023_24"]

    core = pd.read_stata(os.path.join(d23, "AASS2024f.dta"), columns=["holding_id", "region", "weight"], convert_categoricals=False)
    mc = pd.read_stata(os.path.join(d23, "MASIKACROP.dta"), columns=["holding_id", "crop_id", "areaPlanted", "areaHarvested", "harvest_ton"], convert_categoricals=False)
    mc["season"] = "Long_Masika"
    vc = pd.read_stata(os.path.join(d23, "VULICROP.dta"), columns=["holding_id", "crop_id", "areaPlanted", "areaHarvested", "harvest_ton"], convert_categoricals=False)
    vc["season"] = "Short_Vuli"

    df = pd.concat([mc, vc], ignore_index=True).merge(core, on="holding_id", how="left")
    df["crop_group"] = df["crop_id"].map(cmap)
    df = df[df["crop_group"].notna()].copy()

    df["wave"] = "AASS_2023_24"
    df["year"] = 2023
    df["hh_id"] = df["holding_id"].astype(str)
    df["weight"] = pd.to_numeric(df["weight"], errors="coerce")
    df["aez_code"], df["aez_name"] = map_aez(df["region"])
    df["planted_ha"] = pd.to_numeric(df["areaPlanted"], errors="coerce") * ACRE_TO_HA
    df["harvested_ha"] = pd.to_numeric(df["areaHarvested"], errors="coerce") * ACRE_TO_HA
    df["production_t"] = pd.to_numeric(df["harvest_ton"], errors="coerce")
    df["yield_t_ha"] = np.where(df["planted_ha"] > 0, df["production_t"] / df["planted_ha"], np.nan)
    df["price_tzs_t"] = np.nan
    df["mech_cost_tzs_ha"] = np.nan
    df["labor_cost_tzs_ha"] = np.nan
    df["person_days_ha"] = np.nan
    df["biochem_cost_tzs_ha"] = np.nan
    df["regime"] = "Unobserved_Plot_Level"
    df["multi_power_flag"] = False
    return df


def load_all_nps_waves():
    """
    Harmonizes NPS Waves 1-5 (2008/09, 2010/11, 2012/13, 2014/15, 2020/21)
    plot-crop observations with M0-M3 regimes (including M2 Power Tiller in
    Waves 3-5), planted area, yield, implement rental cost, and IPWRA covariates.
    """
    cmap = {
        11: "Maize", 12: "Paddy",
        31: "Legumes", 32: "Legumes", 33: "Legumes", 34: "Legumes",
        35: "Legumes", 36: "Legumes", 37: "Legumes", 43: "Legumes", 47: "Legumes",
    }
    reg_dist = get_ncsa_region_dist_km()

    specs = [
        {
            "wave": "NPS_Wave_1", "year": 2008, "id_col": "hhid", "plot_col": "plotnum",
            "hh_path": os.path.join(DATA_DIR, "NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_A_T.dta"),
            "reg_col": "region", "wt_col": "hh_weight",
            "area_path": os.path.join(DATA_DIR, "NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_2A.dta"),
            "area_gps": "area", "area_est": "s2aq4",
            "crop_path": os.path.join(DATA_DIR, "NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_4A.dta"),
            "crop_col": "zaocode", "kg_col": "s4aq15", "harv_ac": "s4aq8", "intercrop_col": "s4aq6",
            "irrig_path": os.path.join(DATA_DIR, "NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_3A.dta"),
            "irrig_col": "s3aq15",
            "imp_path": os.path.join(DATA_DIR, "NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_11_ALL.dta"),
            "item_col": "impcode", "use_col": "s11q4", "rent_col": "s11q6", "rcost_col": "s11q9",
            "m1": (3, 4, 5, 6), "m2": (), "m3": (7, 8, 9),
        },
        {
            "wave": "NPS_Wave_2", "year": 2010, "id_col": "y2_hhid", "plot_col": "plotnum",
            "hh_path": os.path.join(DATA_DIR, "NPS Wave 2 2010_2011  Household/Household/HH_SEC_A.dta"),
            "reg_col": "region", "wt_col": "y2_weight",
            "area_path": os.path.join(DATA_DIR, "NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_SEC2A.dta"),
            "area_gps": "ag2a_09", "area_est": "ag2a_04",
            "crop_path": os.path.join(DATA_DIR, "NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_SEC4A.dta"),
            "crop_col": "zaocode", "kg_col": "ag4a_15", "harv_ac": "ag4a_08", "intercrop_col": "ag4a_04",
            "irrig_path": os.path.join(DATA_DIR, "NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_SEC3A.dta"),
            "irrig_col": "ag3a_17",
            "imp_path": os.path.join(DATA_DIR, "NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_SEC11.dta"),
            "item_col": "itemcode", "use_col": "ag11_04", "rent_col": "ag11_06", "rcost_col": "ag11_09",
            "m1": (3, 4, 5), "m2": (), "m3": (6, 7, 8),
        },
        {
            "wave": "NPS_Wave_3", "year": 2012, "id_col": "y3_hhid", "plot_col": "plotnum",
            "hh_path": os.path.join(DATA_DIR, "NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_A.dta"),
            "reg_col": "hh_a01_1", "wt_col": "y3_weight",
            "area_path": os.path.join(DATA_DIR, "NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_SEC_2A.dta"),
            "area_gps": "ag2a_09", "area_est": "ag2a_04",
            "crop_path": os.path.join(DATA_DIR, "NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_SEC_4A.dta"),
            "crop_col": "zaocode", "kg_col": "ag4a_28", "harv_ac": "ag4a_21", "intercrop_col": "ag4a_04",
            "irrig_path": os.path.join(DATA_DIR, "NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_SEC_3A.dta"),
            "irrig_col": "ag3a_18",
            "imp_path": os.path.join(DATA_DIR, "NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_SEC_11.dta"),
            "item_col": "itemid", "use_col": "ag11_04", "rent_col": "ag11_06", "rcost_col": "ag11_09",
            "m1": (3, 4, 5), "m2": (14,), "m3": (6, 7, 8),
        },
        {
            "wave": "NPS_Wave_4", "year": 2014, "id_col": "y4_hhid", "plot_col": "plotnum",
            "hh_path": os.path.join(DATA_DIR, "NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_sec_a.dta"),
            "reg_col": "hh_a01_1", "wt_col": "y4_weights",
            "area_path": os.path.join(DATA_DIR, "NPS Wave 4 2014_2015 NPS-4-2014-STATA/ag_sec_2a.dta"),
            "area_gps": "ag2a_09", "area_est": "ag2a_04",
            "crop_path": os.path.join(DATA_DIR, "NPS Wave 4 2014_2015 NPS-4-2014-STATA/ag_sec_4a.dta"),
            "crop_col": "zaocode", "kg_col": "ag4a_28", "harv_ac": "ag4a_21", "intercrop_col": "ag4a_04",
            "irrig_path": os.path.join(DATA_DIR, "NPS Wave 4 2014_2015 NPS-4-2014-STATA/ag_sec_3a.dta"),
            "irrig_col": "ag3a_18",
            "imp_path": os.path.join(DATA_DIR, "NPS Wave 4 2014_2015 NPS-4-2014-STATA/ag_sec_11.dta"),
            "item_col": "itemid", "use_col": "ag11_04", "rent_col": "ag11_06", "rcost_col": "ag11_09",
            "m1": (3, 4, 5), "m2": (14,), "m3": (6, 7, 8),
        },
        {
            "wave": "NPS_Wave_5", "year": 2020, "id_col": "y5_hhid", "plot_col": "plot_id",
            "hh_path": os.path.join(DATA_DIR, "NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_A.dta"),
            "reg_col": "hh_a01_1", "wt_col": "y5_crossweight",
            "area_path": os.path.join(DATA_DIR, "NPS Wave 5 2020_2021 Agriculture-STATA-NPS-Wave5/AG_SEC_02.dta"),
            "area_gps": "ag2a_09", "area_est": "ag2a_04",
            "crop_path": os.path.join(DATA_DIR, "NPS Wave 5 2020_2021 Agriculture-STATA-NPS-Wave5/AG_SEC_4A.dta"),
            "crop_col": "cropid", "kg_col": "ag4a_27", "harv_ac": "ag4a_21", "intercrop_col": "ag4a_04",
            "irrig_path": os.path.join(DATA_DIR, "NPS Wave 5 2020_2021 Agriculture-STATA-NPS-Wave5/AG_SEC_3A.dta"),
            "irrig_col": "ag3a_18",
            "imp_path": os.path.join(DATA_DIR, "NPS Wave 5 2020_2021 Agriculture-STATA-NPS-Wave5/AG_SEC_11.dta"),
            "item_col": "itemid", "use_col": "ag11_04", "rent_col": "ag11_06", "rcost_col": "ag11_09",
            "m1": (3, 4, 5), "m2": (14,), "m3": (6, 7, 8),
        },
    ]

    def nps_edu_to_years(code):
        if pd.isna(code):
            return np.nan
        c = int(code)
        if c in (1, 2):
            return 0.0
        if 11 <= c <= 19:
            return float(min(c - 10, 8))
        if 20 <= c <= 26:
            return float(7 + (c - 20))
        if c >= 31:
            return 15.0
        return 0.0

    nps_demo_specs = {
        "NPS_Wave_1": (
            os.path.join(DATA_DIR, "NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_B_C_D_E1_F_G1_U.dta"),
            "hhid", None, "sbq5", "sbq4", "sbq2", "scq7", None,
        ),
        "NPS_Wave_2": (
            os.path.join(DATA_DIR, "NPS Wave 2 2010_2011  Household/Household/HH_SEC_B.dta"),
            "y2_hhid", "indidy2", "hh_b05", "hh_b04", "hh_b02", "hh_c07",
            os.path.join(DATA_DIR, "NPS Wave 2 2010_2011  Household/Household/HH_SEC_C.dta"),
        ),
        "NPS_Wave_3": (
            os.path.join(DATA_DIR, "NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_B.dta"),
            "y3_hhid", "indidy3", "hh_b05", "hh_b04", "hh_b02", "hh_c07",
            os.path.join(DATA_DIR, "NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_C.dta"),
        ),
        "NPS_Wave_4": (
            os.path.join(DATA_DIR, "NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_sec_b.dta"),
            "y4_hhid", "indidy4", "hh_b05", "hh_b04", "hh_b02", "hh_c07",
            os.path.join(DATA_DIR, "NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_sec_c.dta"),
        ),
        "NPS_Wave_5": (
            os.path.join(DATA_DIR, "NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_B.dta"),
            "y5_hhid", "indidy5", "hh_b05", "hh_b04", "hh_b02", "hh_c07",
            os.path.join(DATA_DIR, "NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_C.dta"),
        ),
    }

    parts = []
    for sp in specs:
        idc, pc = sp["id_col"], sp["plot_col"]
        hh = pd.read_stata(sp["hh_path"], columns=[idc, sp["reg_col"], sp["wt_col"]], convert_categoricals=False).rename(columns={sp["reg_col"]: "region", sp["wt_col"]: "weight"})
        hh = hh.drop_duplicates(subset=[idc])

        # Load household head demographics & schooling
        b_path, did, ind_col, rel_col, age_col, sex_col, edu_col, c_path = nps_demo_specs[sp["wave"]]
        b_cols = [c for c in [did, ind_col, rel_col, age_col, sex_col, (edu_col if c_path is None else None)] if c]
        hb = pd.read_stata(b_path, columns=b_cols, convert_categoricals=False)
        hh_sz_map = hb.groupby(did).size()
        hb_head = hb[hb[rel_col] == 1].groupby(did, as_index=False).first()
        if c_path is not None:
            hc = pd.read_stata(c_path, columns=[did, ind_col, edu_col], convert_categoricals=False).drop_duplicates(subset=[did, ind_col])
            hb_head = hb_head.merge(hc, on=[did, ind_col], how="left")
        head_age_map = dict(zip(hb_head[did], pd.to_numeric(hb_head[age_col], errors="coerce")))
        head_sex_map = dict(zip(hb_head[did], np.where(pd.to_numeric(hb_head[sex_col], errors="coerce") == 1, 1.0, 0.0)))
        head_edu_map = dict(zip(hb_head[did], hb_head[edu_col].map(nps_edu_to_years)))

        acols = list({idc, pc, sp["area_gps"], sp["area_est"]})
        area = pd.read_stata(sp["area_path"], columns=acols, convert_categoricals=False)
        area["is_gps_area"] = pd.to_numeric(area[sp["area_gps"]], errors="coerce").notna().astype(float)
        area["acres"] = pd.to_numeric(area[sp["area_gps"]], errors="coerce").fillna(pd.to_numeric(area[sp["area_est"]], errors="coerce"))
        area = area.groupby([idc, pc], as_index=False).agg({"acres": "mean", "is_gps_area": "max"})
        farm_ha_hh = area.groupby(idc)["acres"].sum() * ACRE_TO_HA

        cr = pd.read_stata(sp["crop_path"], columns=[idc, pc, sp["crop_col"], sp["kg_col"], sp["harv_ac"], sp["intercrop_col"]], convert_categoricals=False)
        cr["crop_group"] = cr[sp["crop_col"]].map(cmap)
        cr = cr[cr["crop_group"].notna()].copy()
        cr["intercropped_flag"] = np.where(pd.to_numeric(cr[sp["intercrop_col"]], errors="coerce") == 1, 1.0, 0.0)
        irrig = pd.read_stata(sp["irrig_path"], columns=[idc, pc, sp["irrig_col"]], convert_categoricals=False)
        irrig["irrigated_flag"] = np.where(pd.to_numeric(irrig[sp["irrig_col"]], errors="coerce") == 1, 1.0, 0.0)
        irrig = irrig.groupby([idc, pc], as_index=False)["irrigated_flag"].max()
        cr = cr.merge(area, on=[idc, pc], how="left").merge(irrig, on=[idc, pc], how="left").merge(hh, on=idc, how="left")
        cr["irrigated_flag"] = cr["irrigated_flag"].fillna(0.0)
        cr["is_gps_area"] = cr["is_gps_area"].fillna(0.0)

        imp = pd.read_stata(sp["imp_path"], columns=[idc, sp["item_col"], sp["use_col"], sp["rent_col"], sp["rcost_col"]], convert_categoricals=False)
        used = imp[(imp[sp["use_col"]] == 1) | (imp[sp["rent_col"]] == 1)].copy()
        hh_powers = {hid: set() for hid in cr[idc].unique()}
        for hid, code in zip(used[idc], used[sp["item_col"]]):
            if hid not in hh_powers:
                continue
            if code in sp["m1"]:
                hh_powers[hid].add("M1")
            elif code in sp["m2"]:
                hh_powers[hid].add("M2")
            elif code in sp["m3"]:
                hh_powers[hid].add("M3")

        mech_codes = set(sp["m1"]) | set(sp["m2"]) | set(sp["m3"])
        rent_hh = used[used[sp["item_col"]].isin(mech_codes)].groupby(idc)[sp["rcost_col"]].sum()

        cr["wave"] = sp["wave"]
        cr["year"] = sp["year"]
        cr["season"] = "Long_Masika"
        cr["hh_id"] = cr[idc].astype(str)
        cr["weight"] = pd.to_numeric(cr["weight"], errors="coerce")
        cr["aez_code"], cr["aez_name"] = map_aez(cr["region"])
        cr["regime"] = cr[idc].map(lambda h: "M3" if "M3" in hh_powers.get(h, ()) else ("M2" if "M2" in hh_powers.get(h, ()) else ("M1" if "M1" in hh_powers.get(h, ()) else "M0")))
        cr["multi_power_flag"] = cr[idc].map(lambda h: len(hh_powers.get(h, ())) > 1)
        cr["planted_ha"] = pd.to_numeric(cr["acres"], errors="coerce") * ACRE_TO_HA
        cr["harvested_ha"] = pd.to_numeric(cr[sp["harv_ac"]], errors="coerce") * ACRE_TO_HA
        cr["production_t"] = pd.to_numeric(cr[sp["kg_col"]], errors="coerce") / 1000.0
        cr["yield_t_ha"] = np.where(cr["planted_ha"] > 0, cr["production_t"] / cr["planted_ha"], np.nan)

        hh_tot_ha = cr.groupby(idc)["planted_ha"].sum().replace(0, np.nan)
        cr["mech_cost_tzs_ha"] = cr[idc].map(rent_hh).fillna(0.0) / cr[idc].map(hh_tot_ha)
        cr["price_tzs_t"] = np.nan
        cr["labor_cost_tzs_ha"] = np.nan
        cr["person_days_ha"] = np.nan
        cr["biochem_cost_tzs_ha"] = np.nan

        cr["log_plot_size_ha"] = np.log1p(cr["planted_ha"].clip(lower=0))
        cr["log_total_farm_size_ha"] = np.log1p(cr[idc].map(farm_ha_hh).fillna(cr["planted_ha"]).clip(lower=0))
        cr["hh_head_age"] = cr[idc].map(head_age_map)
        cr["hh_head_sex"] = cr[idc].map(head_sex_map)
        cr["hh_head_edu"] = cr[idc].map(head_edu_map)
        cr["hh_size"] = cr[idc].map(hh_sz_map)
        cr["draught_livestock_count"] = np.where(cr["regime"] == "M1", 1.0, 0.0)
        cr["dist_road_market_km"] = cr["region"].map(reg_dist).fillna(np.nanmedian(list(reg_dist.values())))
        parts.append(cr)

    return pd.concat(parts, ignore_index=True)


def load_aass_2024_plots():
    """Harmonizes AASS 2024/25 plot-crop data (machinery roster absent on disk)."""
    d24 = os.path.join(DATA_DIR, "AASS 2024_2025")
    cmap = WAVE_CROP_MAP["AASS_2024_25"]

    core = pd.read_stata(os.path.join(d24, "AASS2025.dta"), columns=["Holding_ID", "region_id", "Adjusted_HH_weight"], convert_categoricals=False)
    core = core.rename(columns={"Holding_ID": "HHFARMID", "region_id": "region", "Adjusted_HH_weight": "weight"})

    mp = pd.read_stata(os.path.join(d24, "MASIKAPLOT.dta"), columns=["HHFARMID", "MASIKAPLOT__id", "s6q03_Hectares"], convert_categoricals=False)
    mp = mp.groupby(["HHFARMID", "MASIKAPLOT__id"], as_index=False)["s6q03_Hectares"].mean()
    mc = pd.read_stata(os.path.join(d24, "MASIKACROP.dta"), columns=["HHFARMID", "MASIKAPLOT__id", "MASIKACROP__id", "s7q02", "harvest_ton"], convert_categoricals=False)
    mc = mc.merge(mp, on=["HHFARMID", "MASIKAPLOT__id"], how="left")
    mc["planted_ha"] = pd.to_numeric(mc["s6q03_Hectares"], errors="coerce") * (pd.to_numeric(mc["s7q02"], errors="coerce").fillna(100.0) / 100.0)
    mc = mc.rename(columns={"MASIKACROP__id": "crop_id"})
    mc["season"] = "Long_Masika"

    vp = pd.read_stata(os.path.join(d24, "VULIPLOT.dta"), columns=["HHFARMID", "FIELD__id", "VULIPLOT__id", "s4q03_Hectares"], convert_categoricals=False)
    vp = vp.groupby(["HHFARMID", "FIELD__id", "VULIPLOT__id"], as_index=False)["s4q03_Hectares"].mean()
    vc = pd.read_stata(os.path.join(d24, "VULICROP.dta"), columns=["HHFARMID", "FIELD__id", "VULIPLOT__id", "VULICROP__id", "s5q02", "harvest_ton"], convert_categoricals=False)
    vc = vc.merge(vp, on=["HHFARMID", "FIELD__id", "VULIPLOT__id"], how="left")
    vc["planted_ha"] = pd.to_numeric(vc["s4q03_Hectares"], errors="coerce") * (pd.to_numeric(vc["s5q02"], errors="coerce").fillna(100.0) / 100.0)
    vc = vc.rename(columns={"VULICROP__id": "crop_id"})
    vc["season"] = "Short_Vuli"

    df = pd.concat([mc, vc], ignore_index=True).merge(core, on="HHFARMID", how="left")
    df["crop_group"] = df["crop_id"].map(cmap)
    df = df[df["crop_group"].notna()].copy()

    df["wave"] = "AASS_2024_25"
    df["year"] = 2024
    df["hh_id"] = df["HHFARMID"].astype(str)
    df["weight"] = pd.to_numeric(df["weight"], errors="coerce")
    df["aez_code"], df["aez_name"] = map_aez(df["region"])
    df["harvested_ha"] = np.nan
    df["production_t"] = pd.to_numeric(df["harvest_ton"], errors="coerce")
    df["yield_t_ha"] = np.where(df["planted_ha"] > 0, df["production_t"] / df["planted_ha"], np.nan)
    df["price_tzs_t"] = np.nan
    df["mech_cost_tzs_ha"] = np.nan
    df["labor_cost_tzs_ha"] = np.nan
    df["person_days_ha"] = np.nan
    df["biochem_cost_tzs_ha"] = np.nan
    df["regime"] = "Unobserved_Plot_Level"
    df["multi_power_flag"] = False
    return df


def load_all_nps_waves():
    """
    Harmonizes NPS Waves 1-5 (2008/09, 2010/11, 2012/13, 2014/15, 2020/21)
    plot-crop observations with M0-M3 regimes (including M2 Power Tiller in
    Waves 3-5), planted area, yield, implement rental cost, and IPWRA covariates.
    """
    cmap = {
        11: "Maize", 12: "Paddy",
        31: "Legumes", 32: "Legumes", 33: "Legumes", 34: "Legumes",
        35: "Legumes", 36: "Legumes", 37: "Legumes", 43: "Legumes", 47: "Legumes",
    }
    reg_dist = get_ncsa_region_dist_km()

    specs = [
        {
            "wave": "NPS_Wave_1", "year": 2008, "id_col": "hhid", "plot_col": "plotnum",
            "hh_path": os.path.join(DATA_DIR, "NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_A_T.dta"),
            "reg_col": "region", "wt_col": "hh_weight",
            "area_path": os.path.join(DATA_DIR, "NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_2A.dta"),
            "area_gps": "area", "area_est": "s2aq4",
            "crop_path": os.path.join(DATA_DIR, "NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_4A.dta"),
            "crop_col": "zaocode", "kg_col": "s4aq15", "harv_ac": "s4aq8", "intercrop_col": "s4aq6",
            "irrig_path": os.path.join(DATA_DIR, "NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_3A.dta"),
            "irrig_col": "s3aq15",
            "imp_path": os.path.join(DATA_DIR, "NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_11_ALL.dta"),
            "item_col": "impcode", "use_col": "s11q4", "rent_col": "s11q6", "rcost_col": "s11q9",
            "m1": (3, 4, 5, 6), "m2": (), "m3": (7, 8, 9),
        },
        {
            "wave": "NPS_Wave_2", "year": 2010, "id_col": "y2_hhid", "plot_col": "plotnum",
            "hh_path": os.path.join(DATA_DIR, "NPS Wave 2 2010_2011  Household/Household/HH_SEC_A.dta"),
            "reg_col": "region", "wt_col": "y2_weight",
            "area_path": os.path.join(DATA_DIR, "NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_SEC2A.dta"),
            "area_gps": "ag2a_09", "area_est": "ag2a_04",
            "crop_path": os.path.join(DATA_DIR, "NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_SEC4A.dta"),
            "crop_col": "zaocode", "kg_col": "ag4a_15", "harv_ac": "ag4a_08", "intercrop_col": "ag4a_04",
            "irrig_path": os.path.join(DATA_DIR, "NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_SEC3A.dta"),
            "irrig_col": "ag3a_17",
            "imp_path": os.path.join(DATA_DIR, "NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_SEC11.dta"),
            "item_col": "itemcode", "use_col": "ag11_04", "rent_col": "ag11_06", "rcost_col": "ag11_09",
            "m1": (3, 4, 5), "m2": (), "m3": (6, 7, 8),
        },
        {
            "wave": "NPS_Wave_3", "year": 2012, "id_col": "y3_hhid", "plot_col": "plotnum",
            "hh_path": os.path.join(DATA_DIR, "NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_A.dta"),
            "reg_col": "hh_a01_1", "wt_col": "y3_weight",
            "area_path": os.path.join(DATA_DIR, "NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_SEC_2A.dta"),
            "area_gps": "ag2a_09", "area_est": "ag2a_04",
            "crop_path": os.path.join(DATA_DIR, "NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_SEC_4A.dta"),
            "crop_col": "zaocode", "kg_col": "ag4a_28", "harv_ac": "ag4a_21", "intercrop_col": "ag4a_04",
            "irrig_path": os.path.join(DATA_DIR, "NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_SEC_3A.dta"),
            "irrig_col": "ag3a_18",
            "imp_path": os.path.join(DATA_DIR, "NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_SEC_11.dta"),
            "item_col": "itemid", "use_col": "ag11_04", "rent_col": "ag11_06", "rcost_col": "ag11_09",
            "m1": (3, 4, 5), "m2": (14,), "m3": (6, 7, 8),
        },
        {
            "wave": "NPS_Wave_4", "year": 2014, "id_col": "y4_hhid", "plot_col": "plotnum",
            "hh_path": os.path.join(DATA_DIR, "NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_sec_a.dta"),
            "reg_col": "hh_a01_1", "wt_col": "y4_weights",
            "area_path": os.path.join(DATA_DIR, "NPS Wave 4 2014_2015 NPS-4-2014-STATA/ag_sec_2a.dta"),
            "area_gps": "ag2a_09", "area_est": "ag2a_04",
            "crop_path": os.path.join(DATA_DIR, "NPS Wave 4 2014_2015 NPS-4-2014-STATA/ag_sec_4a.dta"),
            "crop_col": "zaocode", "kg_col": "ag4a_28", "harv_ac": "ag4a_21", "intercrop_col": "ag4a_04",
            "irrig_path": os.path.join(DATA_DIR, "NPS Wave 4 2014_2015 NPS-4-2014-STATA/ag_sec_3a.dta"),
            "irrig_col": "ag3a_18",
            "imp_path": os.path.join(DATA_DIR, "NPS Wave 4 2014_2015 NPS-4-2014-STATA/ag_sec_11.dta"),
            "item_col": "itemid", "use_col": "ag11_04", "rent_col": "ag11_06", "rcost_col": "ag11_09",
            "m1": (3, 4, 5), "m2": (14,), "m3": (6, 7, 8),
        },
        {
            "wave": "NPS_Wave_5", "year": 2020, "id_col": "y5_hhid", "plot_col": "plot_id",
            "hh_path": os.path.join(DATA_DIR, "NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_A.dta"),
            "reg_col": "hh_a01_1", "wt_col": "y5_crossweight",
            "area_path": os.path.join(DATA_DIR, "NPS Wave 5 2020_2021 Agriculture-STATA-NPS-Wave5/AG_SEC_02.dta"),
            "area_gps": "ag2a_09", "area_est": "ag2a_04",
            "crop_path": os.path.join(DATA_DIR, "NPS Wave 5 2020_2021 Agriculture-STATA-NPS-Wave5/AG_SEC_4A.dta"),
            "crop_col": "cropid", "kg_col": "ag4a_27", "harv_ac": "ag4a_21", "intercrop_col": "ag4a_04",
            "irrig_path": os.path.join(DATA_DIR, "NPS Wave 5 2020_2021 Agriculture-STATA-NPS-Wave5/AG_SEC_3A.dta"),
            "irrig_col": "ag3a_18",
            "imp_path": os.path.join(DATA_DIR, "NPS Wave 5 2020_2021 Agriculture-STATA-NPS-Wave5/AG_SEC_11.dta"),
            "item_col": "itemid", "use_col": "ag11_04", "rent_col": "ag11_06", "rcost_col": "ag11_09",
            "m1": (3, 4, 5), "m2": (14,), "m3": (6, 7, 8),
        },
    ]

    def nps_edu_to_years(code):
        if pd.isna(code):
            return np.nan
        c = int(code)
        if c in (1, 2):
            return 0.0
        if 11 <= c <= 19:
            return float(min(c - 10, 8))
        if 20 <= c <= 26:
            return float(7 + (c - 20))
        if c >= 31:
            return 15.0
        return 0.0

    nps_demo_specs = {
        "NPS_Wave_1": (
            os.path.join(DATA_DIR, "NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_B_C_D_E1_F_G1_U.dta"),
            "hhid", None, "sbq5", "sbq4", "sbq2", "scq7", None,
        ),
        "NPS_Wave_2": (
            os.path.join(DATA_DIR, "NPS Wave 2 2010_2011  Household/Household/HH_SEC_B.dta"),
            "y2_hhid", "indidy2", "hh_b05", "hh_b04", "hh_b02", "hh_c07",
            os.path.join(DATA_DIR, "NPS Wave 2 2010_2011  Household/Household/HH_SEC_C.dta"),
        ),
        "NPS_Wave_3": (
            os.path.join(DATA_DIR, "NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_B.dta"),
            "y3_hhid", "indidy3", "hh_b05", "hh_b04", "hh_b02", "hh_c07",
            os.path.join(DATA_DIR, "NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_C.dta"),
        ),
        "NPS_Wave_4": (
            os.path.join(DATA_DIR, "NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_sec_b.dta"),
            "y4_hhid", "indidy4", "hh_b05", "hh_b04", "hh_b02", "hh_c07",
            os.path.join(DATA_DIR, "NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_sec_c.dta"),
        ),
        "NPS_Wave_5": (
            os.path.join(DATA_DIR, "NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_B.dta"),
            "y5_hhid", "indidy5", "hh_b05", "hh_b04", "hh_b02", "hh_c07",
            os.path.join(DATA_DIR, "NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_C.dta"),
        ),
    }

    parts = []
    for sp in specs:
        idc, pc = sp["id_col"], sp["plot_col"]
        hh = pd.read_stata(sp["hh_path"], columns=[idc, sp["reg_col"], sp["wt_col"]], convert_categoricals=False).rename(columns={sp["reg_col"]: "region", sp["wt_col"]: "weight"})
        hh = hh.drop_duplicates(subset=[idc])

        # Load household head demographics & schooling
        b_path, did, ind_col, rel_col, age_col, sex_col, edu_col, c_path = nps_demo_specs[sp["wave"]]
        b_cols = [c for c in [did, ind_col, rel_col, age_col, sex_col, (edu_col if c_path is None else None)] if c]
        hb = pd.read_stata(b_path, columns=b_cols, convert_categoricals=False)
        hh_sz_map = hb.groupby(did).size()
        hb_head = hb[hb[rel_col] == 1].groupby(did, as_index=False).first()
        if c_path is not None:
            hc = pd.read_stata(c_path, columns=[did, ind_col, edu_col], convert_categoricals=False).drop_duplicates(subset=[did, ind_col])
            hb_head = hb_head.merge(hc, on=[did, ind_col], how="left")
        head_age_map = dict(zip(hb_head[did], pd.to_numeric(hb_head[age_col], errors="coerce")))
        head_sex_map = dict(zip(hb_head[did], np.where(pd.to_numeric(hb_head[sex_col], errors="coerce") == 1, 1.0, 0.0)))
        head_edu_map = dict(zip(hb_head[did], hb_head[edu_col].map(nps_edu_to_years)))

        acols = list({idc, pc, sp["area_gps"], sp["area_est"]})
        area = pd.read_stata(sp["area_path"], columns=acols, convert_categoricals=False)
        area["is_gps_area"] = pd.to_numeric(area[sp["area_gps"]], errors="coerce").notna().astype(float)
        area["acres"] = pd.to_numeric(area[sp["area_gps"]], errors="coerce").fillna(pd.to_numeric(area[sp["area_est"]], errors="coerce"))
        area = area.groupby([idc, pc], as_index=False).agg({"acres": "mean", "is_gps_area": "max"})
        farm_ha_hh = area.groupby(idc)["acres"].sum() * ACRE_TO_HA

        cr = pd.read_stata(sp["crop_path"], columns=[idc, pc, sp["crop_col"], sp["kg_col"], sp["harv_ac"], sp["intercrop_col"]], convert_categoricals=False)
        cr["crop_group"] = cr[sp["crop_col"]].map(cmap)
        cr = cr[cr["crop_group"].notna()].copy()
        cr["intercropped_flag"] = np.where(pd.to_numeric(cr[sp["intercrop_col"]], errors="coerce") == 1, 1.0, 0.0)
        irrig = pd.read_stata(sp["irrig_path"], columns=[idc, pc, sp["irrig_col"]], convert_categoricals=False)
        irrig["irrigated_flag"] = np.where(pd.to_numeric(irrig[sp["irrig_col"]], errors="coerce") == 1, 1.0, 0.0)
        irrig = irrig.groupby([idc, pc], as_index=False)["irrigated_flag"].max()
        cr = cr.merge(area, on=[idc, pc], how="left").merge(irrig, on=[idc, pc], how="left").merge(hh, on=idc, how="left")
        cr["irrigated_flag"] = cr["irrigated_flag"].fillna(0.0)
        cr["is_gps_area"] = cr["is_gps_area"].fillna(0.0)

        imp = pd.read_stata(sp["imp_path"], columns=[idc, sp["item_col"], sp["use_col"], sp["rent_col"], sp["rcost_col"]], convert_categoricals=False)
        used = imp[(imp[sp["use_col"]] == 1) | (imp[sp["rent_col"]] == 1)].copy()
        hh_powers = {hid: set() for hid in cr[idc].unique()}
        for hid, code in zip(used[idc], used[sp["item_col"]]):
            if hid not in hh_powers:
                continue
            if code in sp["m1"]:
                hh_powers[hid].add("M1")
            elif code in sp["m2"]:
                hh_powers[hid].add("M2")
            elif code in sp["m3"]:
                hh_powers[hid].add("M3")

        mech_codes = set(sp["m1"]) | set(sp["m2"]) | set(sp["m3"])
        rent_hh = used[used[sp["item_col"]].isin(mech_codes)].groupby(idc)[sp["rcost_col"]].sum()

        cr["wave"] = sp["wave"]
        cr["year"] = sp["year"]
        cr["season"] = "Long_Masika"
        cr["hh_id"] = cr[idc].astype(str)
        cr["weight"] = pd.to_numeric(cr["weight"], errors="coerce")
        cr["aez_code"], cr["aez_name"] = map_aez(cr["region"])
        cr["regime"] = cr[idc].map(lambda h: "M3" if "M3" in hh_powers.get(h, ()) else ("M2" if "M2" in hh_powers.get(h, ()) else ("M1" if "M1" in hh_powers.get(h, ()) else "M0")))
        cr["multi_power_flag"] = cr[idc].map(lambda h: len(hh_powers.get(h, ())) > 1)
        cr["planted_ha"] = pd.to_numeric(cr["acres"], errors="coerce") * ACRE_TO_HA
        cr["harvested_ha"] = pd.to_numeric(cr[sp["harv_ac"]], errors="coerce") * ACRE_TO_HA
        cr["production_t"] = pd.to_numeric(cr[sp["kg_col"]], errors="coerce") / 1000.0
        cr["yield_t_ha"] = np.where(cr["planted_ha"] > 0, cr["production_t"] / cr["planted_ha"], np.nan)

        hh_tot_ha = cr.groupby(idc)["planted_ha"].sum().replace(0, np.nan)
        cr["mech_cost_tzs_ha"] = cr[idc].map(rent_hh).fillna(0.0) / cr[idc].map(hh_tot_ha)
        cr["price_tzs_t"] = np.nan
        cr["labor_cost_tzs_ha"] = np.nan
        cr["person_days_ha"] = np.nan
        cr["biochem_cost_tzs_ha"] = np.nan

        cr["log_plot_size_ha"] = np.log1p(cr["planted_ha"].clip(lower=0))
        cr["log_total_farm_size_ha"] = np.log1p(cr[idc].map(farm_ha_hh).fillna(cr["planted_ha"]).clip(lower=0))
        cr["hh_head_age"] = cr[idc].map(head_age_map)
        cr["hh_head_sex"] = cr[idc].map(head_sex_map)
        cr["hh_head_edu"] = cr[idc].map(head_edu_map)
        cr["hh_size"] = cr[idc].map(hh_sz_map)
        cr["draught_livestock_count"] = np.where(cr["regime"] == "M1", 1.0, 0.0)
        cr["dist_road_market_km"] = cr["region"].map(reg_dist).fillna(np.nanmedian(list(reg_dist.values())))
        parts.append(cr)

    return pd.concat(parts, ignore_index=True)


# -----------------------------------------------------------------------------
# 3. AEZ YIELD NORMALIZATION FACTOR (beta_y0) & TABLES 1-2
# -----------------------------------------------------------------------------

def compute_beta_y0(panel):
    """
    Computes AEZ x Crop Yield Normalization Factor:
        beta_y0 = y_bar_recent(2022/23-2024/25) / y_bar_census(NCSA 2019/20)
    """
    base = panel[panel["wave"] == "NCSA_2019_20"]
    recent = panel[panel["wave"].isin(["AASS_2022_23", "AASS_2023_24", "AASS_2024_25"])]

    rows = []
    for aez_code, aez_name, _ in AEZ_DEFINITIONS:
        for crop in CROPS:
            b_sub = base[(base["aez_code"] == aez_code) & (base["crop_group"] == crop)]
            r_sub = recent[(recent["aez_code"] == aez_code) & (recent["crop_group"] == crop)]
            y_h = weighted_mean(b_sub["yield_t_ha"], b_sub["weight"])
            y_c = weighted_mean(r_sub["yield_t_ha"], r_sub["weight"])
            beta = (y_c / y_h) if (pd.notna(y_h) and y_h > 0 and pd.notna(y_c)) else 1.0
            rows.append({"aez_code": aez_code, "aez_name": aez_name, "crop_group": crop, "beta_y0": beta})
    return pd.DataFrame(rows)


def build_table1_and_table2(ncsa_hh, aass22_plots, nps_plots):
    """Builds Table 1 (chronological) and Table 2 across NPS Waves 1-5, NCSA 2019/20, and AASS 2022/23."""
    wave_dfs = []
    for w_key, w_lbl in [
        ("NPS_Wave_1", "NPS W1 08/09"), ("NPS_Wave_2", "NPS W2 10/11"),
        ("NPS_Wave_3", "NPS W3 12/13"), ("NPS_Wave_4", "NPS W4 14/15"),
    ]:
        sub = nps_plots[(nps_plots["wave"] == w_key) & (nps_plots["planted_ha"].fillna(0) <= 20.0)]
        if not sub.empty:
            hh_sub = sub.groupby("hh_id", as_index=False).agg(
                aez_code=("aez_code", "first"), aez_name=("aez_name", "first"),
                weight=("weight", "first"), regime=("regime", "first"), farm_ha=("planted_ha", "sum"),
            )
            wave_dfs.append((w_lbl, hh_sub))

    wave_dfs.append(("NCSA 2019/20", ncsa_hh))

    sub_w5 = nps_plots[(nps_plots["wave"] == "NPS_Wave_5") & (nps_plots["planted_ha"].fillna(0) <= 20.0)]
    if not sub_w5.empty:
        hh_w5 = sub_w5.groupby("hh_id", as_index=False).agg(
            aez_code=("aez_code", "first"), aez_name=("aez_name", "first"),
            weight=("weight", "first"), regime=("regime", "first"), farm_ha=("planted_ha", "sum"),
        )
        wave_dfs.append(("NPS W5 20/21", hh_w5))

    a22_hh = aass22_plots[aass22_plots["planted_ha"].fillna(0) <= 20.0].groupby("hh_id", as_index=False).agg(
        aez_code=("aez_code", "first"), aez_name=("aez_name", "first"),
        weight=("weight", "first"), regime=("regime", "first"), farm_ha=("planted_ha", "sum"),
    )
    wave_dfs.append(("AASS 2022/23", a22_hh))

    strata = [(0, "National (Tanzania)")] + [(c, n) for c, n, _ in AEZ_DEFINITIONS]

    def summarize_wave(df, wave_label):
        out = []
        scope = "Hired Only" if wave_label == "AASS 2022/23" else "Owned + Rented"
        for aez_code, aez_name in strata:
            sub = df if aez_code == 0 else df[df["aez_code"] == aez_code]
            w_tot = sub["weight"].sum()
            area_tot = (sub["weight"] * sub["farm_ha"]).sum()
            row = {
                "wave": wave_label, "instrument_scope": scope,
                "aez_code": aez_code, "aez_name": aez_name, "unweighted_farms": len(sub),
            }
            for r in REGIMES:
                rsub = sub[sub["regime"] == r]
                row[f"{r}_farm_share_pct"] = round(100.0 * rsub["weight"].sum() / w_tot, 2) if w_tot > 0 else 0.0
                row[f"{r}_area_share_pct"] = round(100.0 * (rsub["weight"] * rsub["farm_ha"]).sum() / area_tot, 2) if area_tot > 0 else 0.0
            out.append(row)
        return pd.DataFrame(out)

    t1_parts = {lbl: summarize_wave(wdf, lbl) for lbl, wdf in wave_dfs}
    t1 = pd.concat(list(t1_parts.values()), ignore_index=True)

    t1_08 = t1_parts["NPS W1 08/09"]
    t1_20 = t1_parts["NPS W5 20/21"]
    t1_19 = t1_parts["NCSA 2019/20"]
    t1_22 = t1_parts["AASS 2022/23"]
    t2_rows = []
    for aez_code, aez_name in strata:
        r08 = t1_08[t1_08["aez_code"] == aez_code].iloc[0]
        r20 = t1_20[t1_20["aez_code"] == aez_code].iloc[0]
        r19 = t1_19[t1_19["aez_code"] == aez_code].iloc[0]
        r22 = t1_22[t1_22["aez_code"] == aez_code].iloc[0]
        mech08 = r08["M1_farm_share_pct"] + r08["M2_farm_share_pct"] + r08["M3_farm_share_pct"]
        mech20 = r20["M1_farm_share_pct"] + r20["M2_farm_share_pct"] + r20["M3_farm_share_pct"]
        mech22 = r22["M1_farm_share_pct"] + r22["M2_farm_share_pct"] + r22["M3_farm_share_pct"]
        cagr_m3_12 = ((r20["M3_farm_share_pct"] / r08["M3_farm_share_pct"]) ** (1 / 12.0) - 1) * 100.0 if r08["M3_farm_share_pct"] > 0 and r20["M3_farm_share_pct"] > 0 else np.nan
        cagr_m3_11_ncsa = ((r19["M3_farm_share_pct"] / r08["M3_farm_share_pct"]) ** (1 / 11.0) - 1) * 100.0 if r08["M3_farm_share_pct"] > 0 and r19["M3_farm_share_pct"] > 0 else np.nan
        cagr_mech_12 = ((mech20 / mech08) ** (1 / 12.0) - 1) * 100.0 if mech08 > 0 and mech20 > 0 else np.nan
        # Log-linear trend regression CAGR across all 5 NPS waves (2008, 2010, 2012, 2014, 2020)
        nps_yrs, nps_m3, nps_n = [], [], []
        for yr_v, w_lbl in [(2008, "NPS W1 08/09"), (2010, "NPS W2 10/11"), (2012, "NPS W3 12/13"), (2014, "NPS W4 14/15"), (2020, "NPS W5 20/21")]:
            rw = t1_parts[w_lbl][t1_parts[w_lbl]["aez_code"] == aez_code].iloc[0]
            if rw["M3_farm_share_pct"] > 0:
                nps_yrs.append(float(yr_v))
                nps_m3.append(np.log(float(rw["M3_farm_share_pct"])))
                nps_n.append(float(max(rw["unweighted_farms"], 1)))
        if len(nps_yrs) >= 3:
            slope = np.polyfit(nps_yrs, nps_m3, 1, w=np.sqrt(nps_n))[0]
            loglin_m3_cagr = (np.exp(slope) - 1.0) * 100.0
        else:
            loglin_m3_cagr = np.nan
        t2_rows.append({
            "aez_code": aez_code,
            "aez_name": aez_name,
            "M0_2008_pct": round(r08["M0_farm_share_pct"], 2),
            "M0_2020_pct": round(r20["M0_farm_share_pct"], 2),
            "M1_2008_pct": round(r08["M1_farm_share_pct"], 2),
            "M1_2020_pct": round(r20["M1_farm_share_pct"], 2),
            "M2_2020_pct": round(r20["M2_farm_share_pct"], 2),
            "M3_2008_pct": round(r08["M3_farm_share_pct"], 2),
            "M3_2020_pct": round(r20["M3_farm_share_pct"], 2),
            "Total_Mech_2008_pct": round(mech08, 2),
            "Total_Mech_2020_pct": round(mech20, 2),
            "CAGR_12yr_Tractor_pct": round(cagr_m3_12, 2) if pd.notna(cagr_m3_12) else np.nan,
            "LogLinear_NPS_Tractor_CAGR_pct": round(loglin_m3_cagr, 2) if pd.notna(loglin_m3_cagr) else np.nan,
            "CAGR_11yr_NCSA_Tractor_pct": round(cagr_m3_11_ncsa, 2) if pd.notna(cagr_m3_11_ncsa) else np.nan,
            "CAGR_12yr_AnyMech_pct": round(cagr_mech_12, 2) if pd.notna(cagr_mech_12) else np.nan,
            "M1_NCSA_2019_pct": round(r19["M1_farm_share_pct"], 2),
            "M3_NCSA_2019_pct": round(r19["M3_farm_share_pct"], 2),
            "M1_AASS_2022_pct": round(r22["M1_farm_share_pct"], 2),
            "M3_AASS_2022_pct": round(r22["M3_farm_share_pct"], 2),
            "Total_Mech_2022_pct": round(mech22, 2),
        })
    t2 = pd.DataFrame(t2_rows)
    return t1, t2


def write_markdown_table(df, title, subtitle, path):
    """Writes a clean Markdown table file from a DataFrame."""
    lines = [f"# {title}", f"*{subtitle}*\n"]
    cols = list(df.columns)
    lines.append("| " + " | ".join(cols) + " |")
    lines.append("|" + "|".join(["---"] * len(cols)) + "|")
    for _, row in df.iterrows():
        vals = [str(row[c]) if pd.notna(row[c]) else "-" for c in cols]
        lines.append("| " + " | ".join(vals) + "|")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


# -----------------------------------------------------------------------------
# 4. MAIN EXECUTION
# -----------------------------------------------------------------------------

def main():
    print("================================================================================")
    print(" STEP 2 (PATCHED): HARMONIZING MECHANIZATION PANEL & GENERATING TABLES 1-2")
    print("================================================================================")

    df_19 = load_ncsa_2019_plots()
    df_22 = load_aass_2022_plots()
    df_23 = load_aass_2023_plots()
    df_24 = load_aass_2024_plots()
    df_nps = load_all_nps_waves()
    ncsa_hh = load_ncsa_2019_hh_regimes()

    keep_cols = [
        "wave", "year", "season", "hh_id", "region", "aez_code", "aez_name", "weight",
        "crop_group", "regime", "multi_power_flag", "planted_ha", "harvested_ha",
        "production_t", "yield_t_ha", "price_tzs_t", "mech_cost_tzs_ha",
        "labor_cost_tzs_ha", "person_days_ha", "person_days_ha_220", "biochem_cost_tzs_ha",
        "log_plot_size_ha", "log_total_farm_size_ha", "hh_head_age", "hh_head_sex",
        "hh_head_edu", "hh_size", "asset_index", "draught_livestock_count",
        "credit_access", "extension_contact", "soil_type", "erosion_or_slope_flag",
        "irrigated_flag", "intercropped_flag", "is_gps_area", "dist_road_market_km",
    ]
    for d in (df_nps, df_19, df_22, df_23, df_24):
        for c in keep_cols:
            if c not in d.columns:
                d[c] = np.nan

    raw_panel = pd.concat([d[keep_cols] for d in (df_nps, df_19, df_22, df_23, df_24)], ignore_index=True)
    n_raw = len(raw_panel)
    # Enforce valid smallholder plot area [0.05, 20.0] ha to prevent micro-plot and m^2/unit-entry outliers
    panel = raw_panel[raw_panel["planted_ha"].notna() & (raw_panel["planted_ha"] >= 0.05) & (raw_panel["planted_ha"] <= 20.0)].copy()
    n_area_ok = len(panel)
    # Deflate all nominal monetary values to constant 2022/23 TZS (CPI base 2010=100, target 210.52)
    cpi_factor = TARGET_CPI_2022_23 / panel["year"].map(CPI_2010_BASE).fillna(TARGET_CPI_2022_23)
    for mcol in ["price_tzs_t", "mech_cost_tzs_ha", "labor_cost_tzs_ha", "biochem_cost_tzs_ha"]:
        panel[mcol] = panel[mcol] * cpi_factor
    print(f"[1/5] Total harmonized plot observations (0.05–20.0 ha, constant 2022/23 TZS): {n_area_ok:,} (from {n_raw:,} raw)")

    print("[2/5] Enforcing agronomic yield ceilings, winsorizing 1st/99th percentiles, & imputing missing costs/prices...")
    bio_ceilings = {"Maize": 10.0, "Paddy": 10.0, "Legumes": 4.5}
    for crop_n, ceil_v in bio_ceilings.items():
        mask_out = (panel["crop_group"] == crop_n) & (panel["yield_t_ha"] > ceil_v)
        panel.loc[mask_out, "yield_t_ha"] = np.nan

    num_cols = ["yield_t_ha", "price_tzs_t", "mech_cost_tzs_ha", "labor_cost_tzs_ha", "person_days_ha", "biochem_cost_tzs_ha"]
    panel = winsorize_by_group(panel, ["yield_t_ha"], ["crop_group", "regime"])
    panel = winsorize_by_group(panel, num_cols, ["crop_group", "aez_code"])
    panel = impute_and_flag_costs(panel, ["price_tzs_t", "mech_cost_tzs_ha", "labor_cost_tzs_ha", "person_days_ha", "person_days_ha_220", "biochem_cost_tzs_ha"])
    panel["person_days_ha"] = np.clip(panel["person_days_ha"], 15.0, 160.0)
    panel["person_days_ha_220"] = np.clip(panel["person_days_ha_220"], 15.0, 220.0)

    # Enforce consistent shadow wage valuation between labor_cost_tzs_ha and person_days_ha
    obs_wage = np.where(
        (~panel["labor_cost_tzs_ha_imputed"]) & (~panel["person_days_ha_imputed"]) & (panel["person_days_ha"] > 0),
        panel["labor_cost_tzs_ha"] / panel["person_days_ha"],
        np.nan,
    )
    panel["_obs_wage"] = obs_wage
    aez_wage_map = panel.groupby("aez_code")["_obs_wage"].median().clip(lower=1500.0, upper=3500.0).to_dict()
    panel["_aez_wage"] = panel["aez_code"].map(aez_wage_map).fillna(1800.0)
    inconsistent_l = (
        panel["labor_cost_tzs_ha_imputed"]
        | (panel["labor_cost_tzs_ha"] < 0.7 * panel["_aez_wage"] * panel["person_days_ha"])
        | (panel["labor_cost_tzs_ha"] > 2.5 * panel["_aez_wage"] * panel["person_days_ha"])
    )
    panel.loc[inconsistent_l, "labor_cost_tzs_ha"] = panel.loc[inconsistent_l, "person_days_ha"] * panel.loc[inconsistent_l, "_aez_wage"]
    panel = panel.drop(columns=["_obs_wage", "_aez_wage"])

    print("[3/5] Computing AEZ Yield Normalization Factor (beta_y0)...")
    beta_df = compute_beta_y0(panel)
    beta_df.to_csv(os.path.join(OUT_TABLES_DIR, "table_s5_beta_y0.csv"), index=False)
    panel = panel.merge(beta_df[["aez_code", "crop_group", "beta_y0"]], on=["aez_code", "crop_group"], how="left")
    panel["beta_y0"] = panel["beta_y0"].fillna(1.0)
    panel["yield_t_ha_normalized"] = np.where(panel["wave"] == "NCSA_2019_20", panel["yield_t_ha"], panel["yield_t_ha"] / panel["beta_y0"])
    # Enforce biological yield ceilings AFTER beta_y0 normalization as well
    for crop_n, ceil_v in bio_ceilings.items():
        mask_norm_out = (panel["crop_group"] == crop_n) & (panel["yield_t_ha_normalized"] > ceil_v)
        panel.loc[mask_norm_out, "yield_t_ha_normalized"] = np.nan

    # Record sample attrition through Step 2 for Table S0 (primary specification uses un-normalized yield_t_ha)
    s0_rows = [
        {"Stage": "1. Raw multi-wave Maize/Paddy/Legumes plots (9 surveys)", "Plots_N": n_raw, "Dropped_N": 0},
        {"Stage": "2. Valid smallholder plot area [0.05, 20.0] ha", "Plots_N": n_area_ok, "Dropped_N": n_raw - n_area_ok},
        {"Stage": "3. Causal-eligible waves (exclude NCSA 19/20 & AASS 23/24-24/25 without plot/machinery rosters)", "Plots_N": int(panel["regime"].isin(["M0", "M1", "M2", "M3"]).sum()), "Dropped_N": n_area_ok - int(panel["regime"].isin(["M0", "M1", "M2", "M3"]).sum())},
        {"Stage": "4. Valid yield (>0, <= biological ceiling) & survey weight (>0)", "Plots_N": int((panel["regime"].isin(["M0", "M1", "M2", "M3"]) & panel["yield_t_ha"].notna() & (panel["yield_t_ha"] > 0) & panel["weight"].notna() & (panel["weight"] > 0)).sum()), "Dropped_N": int(panel["regime"].isin(["M0", "M1", "M2", "M3"]).sum()) - int((panel["regime"].isin(["M0", "M1", "M2", "M3"]) & panel["yield_t_ha"].notna() & (panel["yield_t_ha"] > 0) & panel["weight"].notna() & (panel["weight"] > 0)).sum())},
    ]
    pd.DataFrame(s0_rows).to_csv(os.path.join(OUT_TABLES_DIR, "table_s0_sample_attrition.csv"), index=False)

    parquet_path = os.path.join(OUT_DATA_DIR, "harmonized_mechanization_panel.parquet")
    panel.to_parquet(parquet_path, index=False)
    print(f"      Saved parquet: {parquet_path}")

    print("[4/5] Building Table 1 & Table 2...")
    t1, t2 = build_table1_and_table2(ncsa_hh, df_22, df_nps)
    t1.to_csv(os.path.join(OUT_TABLES_DIR, "table1_zonal_mechanization_distribution.csv"), index=False)
    write_markdown_table(t1, "Table 1: Weighted National and 9-AEZ Farm & Area Share Across Mechanization Regimes (M0–M3)", "NPS Waves 1–5 (2008/09–2020/21), NCSA 2019/20, & AASS 2022/23", os.path.join(OUT_TABLES_DIR, "table1_zonal_mechanization_distribution.md"))

    t2.to_csv(os.path.join(OUT_TABLES_DIR, "table2_mechanization_transition_cagr.csv"), index=False)
    write_markdown_table(t2, "Table 2: Multi-Wave Mechanization Transition Trends (2008/09–2020/21) and 12-Year Harmonized NPS CAGR Across AEZs", "12-year Compound Annual Growth Rate (NPS Wave 1 2008/09 to NPS Wave 5 2020/21), with NCSA 2019/20 & AASS 2022/23 comparability", os.path.join(OUT_TABLES_DIR, "table2_mechanization_transition_cagr.md"))

    print("[5/5] Summary (National Table 1 & Table 2):")
    print(t1[t1["aez_code"] == 0][["wave", "unweighted_farms", "M0_farm_share_pct", "M1_farm_share_pct", "M2_farm_share_pct", "M3_farm_share_pct"]].to_string(index=False))
    print("\n" + t2[["aez_name", "M0_2008_pct", "M0_2020_pct", "Total_Mech_2008_pct", "Total_Mech_2020_pct", "CAGR_12yr_Tractor_pct", "CAGR_12yr_AnyMech_pct"]].to_string(index=False))


if __name__ == "__main__":
    main()
