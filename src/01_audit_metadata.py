#!/usr/bin/env python3
"""
src/01_audit_metadata.py
========================
Read-only diagnostic pipeline for Study 2:

Inspects Tanzania NBS (NCSA 2019/20, AASS 2022/23–2024/25) and NPS/LSMS-ISA
(Waves 1–5) datasets stored in `data/`, extracts live Stata variable & value
labels via `pyreadstat`, builds the harmonized Study 2 variable crosswalk
(Maize, Paddy, Legumes; M0–M3 power regimes; K/L/B cost buckets; IPWRA
covariates; 9 AEZs), and computes Crop x Regime sample size diagnostics.

Generates:
  - outputs/schema_inspection_report.md
  - outputs/schema_mapping.json
And displays an executive console summary.

Usage:
  python3 src/01_audit_metadata.py
"""

import os
import sys
import json
import struct
from collections import Counter, defaultdict

# Ensure virtual environment site-packages are loaded if running with system python3
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENV_SITE = os.path.join(
    BASE_DIR,
    ".venv",
    "lib",
    f"python{sys.version_info.major}.{sys.version_info.minor}",
    "site-packages",
)
if os.path.exists(VENV_SITE) and VENV_SITE not in sys.path:
    sys.path.insert(0, VENV_SITE)

try:
    import pyreadstat
    HAS_PYREADSTAT = True
except ImportError:
    HAS_PYREADSTAT = False

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

try:
    import pypdf
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# 0. TARGET CROP & REGIME DEFINITIONS (STUDY 2)
# -----------------------------------------------------------------------------

TARGET_CROP_GROUPS = ("Maize", "Paddy", "Legumes")
POWER_REGIMES = ("M0", "M1", "M2", "M3")

# Verified NBS crop codes by survey wave
WAVE_CROP_CODES = {
    "NCSA_2019_20": {
        "Maize": [11],
        "Paddy": [12],
        "Legumes": [31, 32, 33, 34, 35, 36, 37, 43, 47],
    },
    "AASS_2022_23": {
        "Maize": [11],
        "Paddy": [12],
        "Legumes": [31, 32, 34, 35, 43, 9930],
    },
    "AASS_2023_24": {
        "Maize": [11],
        "Paddy": [12],
        "Legumes": [31, 32, 34, 35, 43, 9930],
    },
    "AASS_2024_25": {
        "Maize": [11],
        "Paddy": [12],
        "Legumes": [31, 32, 33, 34, 35, 36, 37, 43, 47],
    },
    "NPS_Waves_1_5": {
        "Maize": [11],
        "Paddy": [12],
        "Legumes": [31, 32, 33, 34, 35, 36, 37, 43, 47],
    },
}

# -----------------------------------------------------------------------------
# 1. DIRECTORY & FILE INVENTORY SCANNER
# -----------------------------------------------------------------------------

def inspect_file(filepath):
    """Inspects a single file and extracts size, rows, cols, and metadata."""
    rel_path = os.path.relpath(filepath, BASE_DIR)
    ext = os.path.splitext(filepath)[1].lower()
    size_bytes = os.path.getsize(filepath)
    size_mb = round(size_bytes / (1024 * 1024), 3)

    rows = None
    cols = None
    col_names = []
    status = "OK"
    error = ""
    extra_info = {}

    try:
        if ext == ".dta":
            if HAS_PYREADSTAT:
                _, meta = pyreadstat.read_dta(filepath, metadataonly=True)
                rows = meta.number_rows
                cols = meta.number_columns
                col_names = meta.column_names
                extra_info["file_label"] = meta.file_label
                extra_info["stata_release"] = getattr(meta, "file_format_version", "unknown")
            else:
                # Fast binary fallback for Stata 117-119
                with open(filepath, "rb") as f:
                    head = f.read(500)
                    if b"<release>" in head:
                        rel = head.split(b"<release>")[1].split(b"</release>")[0].decode("ascii")
                        bo = "<" if b"<byteorder>LSF</byteorder>" in head else ">"
                        k_b = head.split(b"<K>")[1].split(b"</K>")[0]
                        n_b = head.split(b"<N>")[1].split(b"</N>")[0]
                        cols = struct.unpack(f"{bo}H", k_b)[0]
                        rows = struct.unpack(f"{bo}Q", n_b)[0]
                        extra_info["stata_release"] = rel
                    else:
                        rows, cols = 0, 0
        elif ext == ".sav":
            if HAS_PYREADSTAT:
                _, meta = pyreadstat.read_sav(filepath, metadataonly=True)
                rows = meta.number_rows
                cols = meta.number_columns
                col_names = meta.column_names
        elif ext == ".csv":
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                header = f.readline()
                col_names = [c.strip() for c in header.split(",")]
                cols = len(col_names)
                line_count = 1
                for _ in f:
                    line_count += 1
                rows = max(0, line_count - 1)
        elif ext == ".xlsx":
            if HAS_PANDAS:
                xl = pd.ExcelFile(filepath)
                extra_info["sheet_names"] = xl.sheet_names
                first_sheet = xl.sheet_names[0]
                df_sample = pd.read_excel(filepath, sheet_name=first_sheet, nrows=1)
                cols = len(df_sample.columns)
                col_names = list(df_sample.columns)
                df_full = pd.read_excel(filepath, sheet_name=first_sheet)
                rows = len(df_full)
        elif ext == ".pdf":
            if HAS_PYPDF:
                reader = pypdf.PdfReader(filepath)
                extra_info["pdf_pages"] = len(reader.pages)
                rows = len(reader.pages)
                cols = 0
        elif ext == ".geojson":
            with open(filepath, "r", encoding="utf-8") as f:
                geo = json.load(f)
                features = geo.get("features", [])
                rows = len(features)
                if features:
                    cols = len(features[0].get("properties", {}))
                    col_names = list(features[0].get("properties", {}).keys())
                extra_info["feature_type"] = geo.get("type")
        elif ext == ".dbf":
            with open(filepath, "rb") as f:
                header = f.read(32)
                num_recs, _, _ = struct.unpack("<IHH", header[4:12])
                rows = num_recs
                fields = []
                f.seek(32)
                while True:
                    fdesc = f.read(32)
                    if not fdesc or fdesc[0] == 0x0D:
                        break
                    fields.append(fdesc[:11].split(b"\x00")[0].decode("latin1"))
                cols = len(fields)
                col_names = fields
        elif ext == ".shp":
            dbf_path = filepath[:-4] + ".dbf"
            if os.path.exists(dbf_path):
                with open(dbf_path, "rb") as f:
                    header = f.read(32)
                    num_recs, _, _ = struct.unpack("<IHH", header[4:12])
                    rows = num_recs
                    cols = 0
        elif ext in [".json", ".xml", ".txt"]:
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
                rows = len(lines)
                cols = 1
    except Exception as e:
        status = "ERROR"
        error = str(e)

    return {
        "relative_path": rel_path,
        "filename": os.path.basename(filepath),
        "extension": ext,
        "size_mb": size_mb,
        "size_bytes": size_bytes,
        "rows": rows,
        "cols": cols,
        "status": status,
        "error": error,
        "col_names": col_names,
        "extra_info": extra_info,
    }


def run_inventory_scan():
    """Scans all files under data/ recursively."""
    all_files = []
    if not os.path.exists(DATA_DIR):
        return all_files
    for root, _, files in os.walk(DATA_DIR):
        for f in sorted(files):
            if f in [".DS_Store", "Thumbs.db"]:
                continue
            fpath = os.path.join(root, f)
            all_files.append(inspect_file(fpath))
    return all_files


def discover_nps_waves(data_dir):
    """
    Scans data/ for any NPS / LSMS-ISA subdirectories and .dta files,
    categorizing plot/agriculture modules, household rosters, and
    implement/livestock modules.
    """
    nps_markers = ("nps", "lsms", "tza_nps", "tz_nps", "panel")
    discovered_subdirs = set()
    categorized = {
        "plot_agriculture": [],
        "household_roster": [],
        "implements_livestock": [],
        "other": [],
    }
    all_dta = []

    if not os.path.exists(data_dir):
        return {
            "status": "DATA_DIR_MISSING",
            "discovered_subdirs": [],
            "total_dta_files": 0,
            "modules": categorized,
            "all_dta_paths": [],
        }

    for root, _, files in os.walk(data_dir):
        rel_root = os.path.relpath(root, data_dir)
        is_nps_dir = any(m in rel_root.lower() for m in nps_markers)
        for fname in sorted(files):
            if not fname.lower().endswith(".dta"):
                continue
            is_nps_file = is_nps_dir or any(m in fname.lower() for m in nps_markers)
            if not is_nps_file:
                continue
            fpath = os.path.join(root, fname)
            rel_path = os.path.relpath(fpath, BASE_DIR)
            if rel_root != ".":
                discovered_subdirs.add(rel_root)
            all_dta.append(rel_path)

            fl = fname.lower()
            if any(k in fl for k in ("ag_sec", "plot", "crop", "ag_", "agric", "field")):
                categorized["plot_agriculture"].append(rel_path)
            elif any(k in fl for k in ("hh_sec", "roster", "household", "hh_")):
                categorized["household_roster"].append(rel_path)
            elif any(k in fl for k in ("impl", "equip", "asset", "livestock", "lvstk", "ag_sec11", "ag_sec10")):
                categorized["implements_livestock"].append(rel_path)
            else:
                categorized["other"].append(rel_path)

    return {
        "status": "FOUND" if all_dta else "NOT_FOUND_ON_DISK",
        "discovered_subdirs": sorted(discovered_subdirs),
        "total_dta_files": len(all_dta),
        "modules": categorized,
        "all_dta_paths": all_dta,
    }


# -----------------------------------------------------------------------------
# 2. SURVEY WAVE REGISTRY & LIVE .DTA LABEL EXTRACTION
# -----------------------------------------------------------------------------

SURVEY_WAVES = {
    "NCSA_2019_20": {
        "name": "National Census of Agriculture 2019/20 (Small-Scale Farmers)",
        "folder": "data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI",
        "key_files": {
            "sov": "R000_SOV.dta",
            "hh": "R031_HHRECORD.dta",
            "land_own": "R041_LAND_OWNERSHIP.dta",
            "farming_methods": "R062_FARMING_METHODS.dta",
            "field_dist": "R071_DISTANCE_TO_FIELDS.dta",
            "short_rain": "R081_SHORT_RAINY_SEASON.dta",
            "long_rain": "R082_LONG_RAINY_SEASON.dta",
            "implements": "R121_FARM_IMPLEMENTS.dta",
            "tractor_animals": "R122_USE_TRACTOR_ANIMALS.dta",
            "erosion": "R126_SOIL_EROSION.dta",
            "extension": "R141_EXTENSION_MESSAGES.dta",
            "cattle": "R152_CATTLE_POPULATION.dta",
            "labor": "R291_LABOUR_USE.dta",
            "infrastructure": "R310_ACCESS_INFRASTUCTURE.dta",
            "assets": "R342_HOUSE_ASSETS.dta",
        },
    },
    "AASS_2022_23": {
        "name": "Annual Agricultural Sample Survey 2022/23",
        "folder": "data/AASS 2022_2023",
        "key_files": {
            "core": "AASS2023.dta",
            "household": "household.dta",
            "field": "field.dta",
            "masikaplot": "masikaplot.dta",
            "vuliplot": "vuliplot.dta",
            "masikacrop": "masikacrop.dta",
            "vulicrop": "vulicrop.dta",
            "crop_use": "crop_use.dta",
            "inputs": "inputs.dta",
            "seeds": "seeds.dta",
            "items_services": "items_services.dta",
            "labor": "external_labor_activities.dta",
        },
    },
    "AASS_2023_24": {
        "name": "Annual Agricultural Sample Survey 2023/24",
        "folder": "data/AASS 2023_2024",
        "key_files": {
            "core": "AASS2024f.dta",
            "household": "HOUSEHOLD.dta",
            "field": "FIELD.dta",
            "masikaplot": "MASIKAPLOT.dta",
            "vuliplot": "VULIPLOT.dta",
            "masikacrop": "MASIKACROP.dta",
            "vulicrop": "VULICROP.dta",
            "crop_use": "CROP_USE.dta",
            "inputs_masika": "InputRoster_masika.dta",
            "inputs_vuli": "InputRoster_vuli.dta",
            "buildings": "buildings_roster.dta",
        },
    },
    "AASS_2024_25": {
        "name": "Annual Agricultural Sample Survey 2024/25",
        "folder": "data/AASS 2024_2025",
        "key_files": {
            "core": "AASS2025.dta",
            "household": "HOUSEHOLD.dta",
            "field": "FIELD.dta",
            "masikaplot": "MASIKAPLOT.dta",
            "vuliplot": "VULIPLOT.dta",
            "masikacrop": "MASIKACROP.dta",
            "vulicrop": "VULICROP.dta",
            "crop_use": "CROP_USE.dta",
            "inputs_masika": "inputRoster_masika.dta",
            "inputs_vuli": "inputRoster_vuli.dta",
            "livestock_type": "livestock_type.dta",
            "stock_livestock": "stock_livestock.dta",
        },
    },
    "NPS_Wave_1": {
        "name": "National Panel Survey Wave 1 (2008/09)",
        "folder": "data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1",
        "key_files": {"hh": "SEC_A_T.dta", "plot": "SEC_3A.dta", "crop": "SEC_4A.dta", "implements": "SEC_11_ALL.dta"},
    },
    "NPS_Wave_2": {
        "name": "National Panel Survey Wave 2 (2010/11)",
        "folder": "data/NPS Wave 2 2010_2011  Agriculture/Agriculture",
        "key_files": {"plot": "AG_SEC3A.dta", "crop": "AG_SEC4A.dta", "implements": "AG_SEC11.dta"},
    },
    "NPS_Wave_3": {
        "name": "National Panel Survey Wave 3 (2012/13)",
        "folder": "data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS",
        "key_files": {"hh": "HH_SEC_A.dta", "plot": "AG_SEC_3A.dta", "crop": "AG_SEC_4A.dta", "implements": "AG_SEC_11.dta"},
    },
    "NPS_Wave_4": {
        "name": "National Panel Survey Wave 4 (2014/15)",
        "folder": "data/NPS Wave 4 2014_2015 NPS-4-2014-STATA",
        "key_files": {"hh": "hh_sec_a.dta", "plot": "ag_sec_3a.dta", "crop": "ag_sec_4a.dta", "implements": "ag_sec_11.dta"},
    },
    "NPS_Wave_5": {
        "name": "National Panel Survey Wave 5 (2020/21)",
        "folder": "data/NPS Wave 5 2020_2021 Agriculture-STATA-NPS-Wave5",
        "key_files": {"plot": "AG_SEC_3A.dta", "crop": "AG_SEC_4A.dta", "implements": "AG_SEC_11.dta"},
    },
    "NPS_Waves_1_5": discover_nps_waves(DATA_DIR),
}


def parse_ddi_codebooks():
    """
    Inspects the JSON/CSV DDI dictionaries in data/metadata/,
    data/nbs_aass_metadata/, and data/ncsa_2019_metadata/ to verify exact
    variable names and value codes for M0-M3 land-preparation/tillage power,
    implement ownership, machinery rental/fuel, and labor days/costs across
    NCSA 2019/20, AASS 2022/23, AASS 2023/24, and AASS 2024/25.
    """
    keywords = (
        "tractor", "plough", "tiller", "hoe", "oxen", "animal", "traction",
        "implement", "equipment", "machinery", "fuel", "rental", "rent",
        "labour", "labor", "land prep", "tillage", "crop_id", "q821c4", "q811c4",
        "masikacrop__id", "vulicrop__id", "items_service__id",
    )
    report = {}

    # 1. NCSA 2019/20 JSON
    ncsa_json = os.path.join(DATA_DIR, "ncsa_2019_metadata", "data_dictionary_ncsa_2019.json")
    if os.path.exists(ncsa_json):
        with open(ncsa_json, "r", encoding="utf-8") as f:
            ncsa_data = json.load(f)
        matches = []
        for fobj in ncsa_data:
            fn = fobj.get("filename", "")
            for v in fobj.get("variables", []):
                vn = v.get("variable_name", "")
                vl = v.get("variable_label", "") or ""
                vc = v.get("value_codes_and_labels", "") or ""
                if any(k in f"{vn} {vl} {vc}".lower() for k in keywords):
                    matches.append({
                        "file": fn,
                        "variable": vn,
                        "label": vl,
                        "value_codes": vc[:300],
                    })
        report["NCSA_2019_20"] = {"source": "data_dictionary_ncsa_2019.json", "matched_count": len(matches), "matches": matches[:60]}

    # 2. AASS 2022/23 JSON (Catalog 52)
    aass22_json = os.path.join(DATA_DIR, "nbs_aass_metadata", "data_dictionary_catalog_52.json")
    if os.path.exists(aass22_json):
        with open(aass22_json, "r", encoding="utf-8") as f:
            aass22_data = json.load(f)
        matches = []
        for item in aass22_data:
            fn = item.get("File Name", "")
            vn = item.get("Variable Name", "")
            vl = item.get("Question") or item.get("Variable Label") or ""
            vc = item.get("Value Codes & Labels") or ""
            if any(k in f"{fn} {vn} {vl} {vc}".lower() for k in keywords):
                matches.append({
                    "file": fn,
                    "variable": vn,
                    "label": vl[:120],
                    "value_codes": vc[:300],
                })
        report["AASS_2022_23"] = {"source": "data_dictionary_catalog_52.json", "matched_count": len(matches), "matches": matches[:60]}

    # 3. AASS 2023/24 & 2024/25 DDI JSONs
    ddi_specs = [
        ("AASS_2023_24", os.path.join(DATA_DIR, "metadata", "TZA_AASS_2023-2024_v01.json")),
        ("AASS_2024_25", os.path.join(DATA_DIR, "metadata", "TZA-NBS.OCGS-AASS-2025-v01.json")),
    ]
    for w_key, jpath in ddi_specs:
        if os.path.exists(jpath):
            with open(jpath, "r", encoding="utf-8") as f:
                d = json.load(f)
            fmap = {df.get("file_id"): df.get("file_name") for df in d.get("data_files", [])}
            matches = []
            for v in d.get("variables", []):
                fn = fmap.get(v.get("file_id"), "")
                vn = v.get("name", "")
                vl = v.get("labl") or ""
                cats = [(c.get("value"), c.get("labl")) for c in v.get("var_catgry", [])]
                cat_str = "; ".join(f"{cv}={cl}" for cv, cl in cats[:20])
                if any(k in f"{fn} {vn} {vl} {cat_str}".lower() for k in keywords):
                    matches.append({
                        "file": fn,
                        "variable": vn,
                        "label": vl[:120],
                        "value_codes": cat_str[:300],
                    })
            report[w_key] = {"source": os.path.basename(jpath), "matched_count": len(matches), "matches": matches[:60]}

    return report

# Patterns for live .dta label extraction (crop codes, tillage/land-prep, implements, labor)
LABEL_TARGET_KEYWORDS = {
    "crop_codes": ("crop", "zaocode", "q811c4", "q821c4", "crop_id", "masikacrop__id", "vulicrop__id"),
    "land_prep_tillage": ("land_prep", "tillage", "plough", "tractor", "animal", "q122c", "s6q", "s4q", "ag_sec3"),
    "implement_ownership": ("implement", "equipment", "q121c", "items_service__id", "s21q", "s20q", "ag_sec11"),
    "labor_activity": ("labor", "labour", "activity", "q291", "external_labor", "s18q", "ag_sec3a"),
}


def _classify_label_domain(var_name, var_label):
    """Assigns a variable to one or more Study 2 verification domains."""
    combined = f"{var_name} {var_label}".lower()
    domains = []
    for domain, keywords in LABEL_TARGET_KEYWORDS.items():
        if any(kw in combined for kw in keywords):
            domains.append(domain)
    return domains


def extract_dta_metadata_labels():
    """
    Uses pyreadstat.read_dta(..., metadataonly=True) to extract exact Stata
    variable labels and value label dictionaries for crop codes,
    land-preparation/tillage variables, implement ownership codes, and labor
    activity codes across all waves.
    """
    extracted = {
        "pyreadstat_available": HAS_PYREADSTAT,
        "waves": {},
    }

    if not HAS_PYREADSTAT:
        extracted["status"] = "pyreadstat_unavailable_in_current_python"
        return extracted

    extracted["status"] = "OK"

    # Build list of (wave_key, rel_paths) to inspect
    wave_files = {}
    for w_key, w_info in SURVEY_WAVES.items():
        if w_key == "NPS_Waves_1_5":
            wave_files[w_key] = w_info.get("all_dta_paths", [])
        else:
            folder = w_info["folder"]
            wave_files[w_key] = [
                os.path.join(folder, fn) for fn in w_info["key_files"].values()
            ]

    for w_key, rel_paths in wave_files.items():
        wave_out = {
            "files_inspected": 0,
            "crop_codes": {},
            "land_prep_tillage": {},
            "implement_ownership": {},
            "labor_activity": {},
        }
        for rel_path in rel_paths:
            abs_path = os.path.join(BASE_DIR, rel_path)
            if not os.path.exists(abs_path):
                continue
            try:
                _, meta = pyreadstat.read_dta(abs_path, metadataonly=True)
                wave_out["files_inspected"] += 1
                col_labels = meta.column_names_to_labels or {}
                val_labels = meta.variable_value_labels or {}
                fname = os.path.basename(abs_path)

                for col in meta.column_names:
                    v_lbl = col_labels.get(col) or ""
                    domains = _classify_label_domain(col, v_lbl)
                    if not domains:
                        continue
                    v_dict = val_labels.get(col, {})
                    # Convert keys to str for clean JSON serialization
                    v_dict_str = {str(k): str(v) for k, v in v_dict.items()}
                    entry = {
                        "file": fname,
                        "variable": col,
                        "label": v_lbl,
                        "value_labels": v_dict_str,
                    }
                    for dom in domains:
                        wave_out[dom][f"{fname}::{col}"] = entry
            except Exception as e:
                wave_out.setdefault("errors", []).append({"file": rel_path, "error": str(e)})

        extracted["waves"][w_key] = wave_out

    return extracted


# -----------------------------------------------------------------------------
# 3. HARMONIZED VARIABLE CROSSWALK (STUDY 2: MECHANIZATION M0-M3)
# -----------------------------------------------------------------------------

def extract_wave_variable_crosswalk():
    """
    Constructs an explicit variable mapping crosswalk across NCSA 2019/20,
    AASS 2022/23–2024/25, and NPS Waves 1–5 for causal estimation (IPWRA)
    and stochastic simulation (GRKS / MVE).
    """
    mapping = {
        "Identifiers_and_Weights": {
            "Household_ID": {
                "NCSA_2019_20": {"file": "R000_SOV.dta / All", "column": "HHID / hh_number", "type": "str / float"},
                "AASS_2022_23": {"file": "AASS2023.dta / All", "column": "holding_id", "type": "str"},
                "AASS_2023_24": {"file": "AASS2024f.dta / All", "column": "holding_id", "type": "str"},
                "AASS_2024_25": {"file": "AASS2025.dta / All", "column": "Holding_ID / HHFARMID", "type": "str"},
                "NPS_Waves_1_5": {"file": "hh_sec_a / ag_sec2a", "column": "y1_hhid / y2_hhid / y3_hhid / y4_hhid / y5_hhid", "type": "str"},
            },
            "Plot_Field_Crop_ID": {
                "NCSA_2019_20": {"file": "R081 / R082", "column": "q811c1/q821c1 (Field), q811c3/q821c3 (Plot), q811c4/q821c4 (Crop)", "type": "Numeric"},
                "AASS_2022_23": {"file": "masikacrop.dta / vulicrop.dta", "column": "FIELD__id, MASIKAPLOT__id/VULIPLOT__id, crop_id", "type": "Numeric"},
                "AASS_2023_24": {"file": "MASIKACROP.dta / VULICROP.dta", "column": "FIELD__id, MASIKAPLOT__id/VULIPLOT__id, crop_id", "type": "Numeric"},
                "AASS_2024_25": {"file": "MASIKACROP.dta / VULICROP.dta", "column": "MASIKAPLOT__id/VULIPLOT__id, MASIKACROP__id/VULICROP__id", "type": "Numeric"},
                "NPS_Waves_1_5": {"file": "ag_sec3a / ag_sec4a", "column": "plotnum, zaocode", "type": "str / Numeric"},
            },
            "Region_Code": {
                "NCSA_2019_20": {"file": "All", "column": "region", "codes": "1=Dodoma ... 26=Songwe, 51-55=Zanzibar"},
                "AASS_2022_23": {"file": "All", "column": "region", "codes": "1=Dodoma ... 26=Songwe, 51-55=Zanzibar"},
                "AASS_2023_24": {"file": "All", "column": "region", "codes": "1=Dodoma ... 26=Songwe, 51-55=Zanzibar"},
                "AASS_2024_25": {"file": "AASS2025.dta", "column": "region_id", "codes": "1=Dodoma ... 26=Songwe, 51-55=Zanzibar"},
                "NPS_Waves_1_5": {"file": "hh_sec_a", "column": "hh_a01_1 / region", "codes": "Standard NBS region codes"},
            },
            "District_Code": {
                "NCSA_2019_20": {"file": "All", "column": "district", "details": "199 distinct LGA Council codes (disti_lbl)"},
                "AASS_2022_23": {"file": "household.dta", "column": "district / LGA", "details": "District identifier"},
                "AASS_2023_24": {"file": "wen_TZA.dta", "column": "district_code", "details": "Standard NBS district code"},
                "AASS_2024_25": {"file": "AASS2025.dta", "column": "stratum_id / ea_id", "details": "Stratum and Enumeration Area"},
                "NPS_Waves_1_5": {"file": "hh_sec_a", "column": "hh_a02_1 / district", "details": "District code"},
            },
            "Sampling_Weight": {
                "NCSA_2019_20": {"file": "All", "column": "finalweight_hh", "label": "Household Sampling Weight"},
                "AASS_2022_23": {"file": "All", "column": "Weight", "label": "Holding Survey Weight"},
                "AASS_2023_24": {"file": "AASS2024f.dta", "column": "weight", "label": "Sampling Weight"},
                "AASS_2024_25": {"file": "AASS2025.dta", "column": "Adjusted_HH_weight", "label": "Adjusted HH Weight"},
                "NPS_Waves_1_5": {"file": "hh_sec_a", "column": "y*_weight / hh_weight", "label": "Cross-sectional / Panel Sampling Weight"},
            },
        },
        "Target_Crops": {
            "Maize": {
                "NCSA_2019_20": {"files": "R081 / R082", "column": "q811c4 / q821c4", "codes": [11], "label": "Maize"},
                "AASS_2022_23": {"files": "masikacrop.dta / vulicrop.dta", "column": "crop_id", "codes": [11], "label": "Maize"},
                "AASS_2023_24": {"files": "MASIKACROP.dta / VULICROP.dta", "column": "crop_id", "codes": [11], "label": "Maize"},
                "AASS_2024_25": {"files": "MASIKACROP.dta / VULICROP.dta", "column": "MASIKACROP__id / VULICROP__id", "codes": [11], "label": "Maize"},
                "NPS_Waves_1_5": {"files": "ag_sec4a / ag_sec5a", "column": "zaocode", "codes": [11], "label": "Maize"},
            },
            "Paddy": {
                "NCSA_2019_20": {"files": "R081 / R082", "column": "q811c4 / q821c4", "codes": [12], "label": "Paddy"},
                "AASS_2022_23": {"files": "masikacrop.dta / vulicrop.dta", "column": "crop_id", "codes": [12], "label": "Paddy"},
                "AASS_2023_24": {"files": "MASIKACROP.dta / VULICROP.dta", "column": "crop_id", "codes": [12], "label": "Paddy"},
                "AASS_2024_25": {"files": "MASIKACROP.dta / VULICROP.dta", "column": "MASIKACROP__id / VULICROP__id", "codes": [12], "label": "Paddy"},
                "NPS_Waves_1_5": {"files": "ag_sec4a / ag_sec5a", "column": "zaocode", "codes": [12], "label": "Paddy"},
            },
            "Legumes": {
                "NCSA_2019_20": {
                    "files": "R081 / R082",
                    "column": "q811c4 / q821c4",
                    "codes": [31, 32, 33, 34, 35, 36, 37, 43, 47],
                    "label": "31=Beans, 32=Cowpeas, 33=Green gram, 34=Pigeon pea, 35=Chick peas, 36=Bambaranuts, 37=Field peas, 43=Groundnut, 47=Soyabeans",
                },
                "AASS_2022_23": {
                    "files": "masikacrop.dta / vulicrop.dta",
                    "column": "crop_id",
                    "codes": [31, 32, 34, 35, 43, 9930],
                    "label": "31=Beans, 32=Cowpeas, 34=Pigeon pea, 35=Chick peas, 43=Groundnut, 9930=Other leguminous crops",
                },
                "AASS_2023_24": {
                    "files": "MASIKACROP.dta / VULICROP.dta",
                    "column": "crop_id",
                    "codes": [31, 32, 34, 35, 43, 9930],
                    "label": "31=Beans, 32=Cowpeas, 34=Pigeon pea, 35=Chick peas, 43=Groundnut, 9930=Other leguminous crops",
                },
                "AASS_2024_25": {
                    "files": "MASIKACROP.dta / VULICROP.dta",
                    "column": "MASIKACROP__id / VULICROP__id",
                    "codes": [31, 32, 33, 34, 35, 36, 37, 43, 47],
                    "label": "31=Beans, 32=Cowpeas, 33=Green gram, 34=Pigeon pea, 35=Chick peas, 36=Bambaranuts, 37=Field peas, 43=Groundnut, 47=Soyabeans",
                },
                "NPS_Waves_1_5": {
                    "files": "ag_sec4a / ag_sec5a",
                    "column": "zaocode",
                    "codes": [31, 32, 33, 34, 35, 36, 37, 43, 47],
                    "label": "Common beans, cowpeas, green gram, pigeon peas, chick peas, bambara nuts, field peas, groundnuts, soybeans",
                },
            },
        },
        "Area_and_Production": {
            "Planted_Area": {
                "NCSA_2019_20": {"file": "R081 / R082", "column": "q811c7a / q821c7a", "unit": "Acres (conv: * 0.404686 to ha)"},
                "AASS_2022_23": {"file": "masikacrop.dta / vulicrop.dta", "column": "areaPlanted / s7q02a", "unit": "Acres"},
                "AASS_2023_24": {"file": "MASIKACROP.dta / VULICROP.dta", "column": "areaPlanted", "unit": "Acres"},
                "AASS_2024_25": {"file": "MASIKACROP.dta / VULICROP.dta", "column": "s7q02 * s6q03_acres", "unit": "Percentage of plot planted * plot acres"},
                "NPS_Waves_1_5": {"file": "ag_sec3a / ag_sec4a", "column": "area_gps / area_farmer", "unit": "Acres (conv: * 0.404686 to ha)"},
            },
            "Harvested_Area": {
                "NCSA_2019_20": {"file": "R081 / R082", "column": "q811c9a / q821c9a", "unit": "Acres"},
                "AASS_2022_23": {"file": "masikacrop.dta", "column": "areaHarvested", "unit": "Acres"},
                "AASS_2023_24": {"file": "MASIKACROP.dta", "column": "areaHarvested", "unit": "Acres"},
                "AASS_2024_25": {"file": "MASIKACROP.dta", "column": "s7q05 / s7q06", "unit": "Binary harvest indicator & harvested area"},
                "NPS_Waves_1_5": {"file": "ag_sec4a", "column": "ag4a_08 / ag4a_19", "unit": "Acres"},
            },
            "Quantity_Harvested": {
                "NCSA_2019_20": {"file": "R081 / R082", "column": "q811c9e / q821c9e", "unit": "Total kg (Metric tonnes = kg / 1,000)"},
                "AASS_2022_23": {"file": "masikacrop.dta / vulicrop.dta", "column": "production_kg", "unit": "kg"},
                "AASS_2023_24": {"file": "MASIKACROP.dta / VULICROP.dta", "column": "production_kg", "unit": "kg"},
                "AASS_2024_25": {"file": "MASIKACROP.dta / VULICROP.dta", "column": "s7q08_kg / production_kg", "unit": "kg"},
                "NPS_Waves_1_5": {"file": "ag_sec4a", "column": "ag4a_28 (kg harvested)", "unit": "kg"},
            },
            "Crop_Sales_and_Farmgate_Price": {
                "NCSA_2019_20": {
                    "sold_indicator": "q821c37 (1=Yes, 2=No)",
                    "quantity_sold_kg": "q821c38 (Kgs)",
                    "farmgate_price_tzs_kg": "q821c39 (Average price TZS/kg)",
                    "total_sales_val_tzs": "q821c38 * q821c39",
                },
                "AASS_2022_23": {
                    "file": "crop_use.dta",
                    "sold_indicator": "s9q02__1 (1=Yes, 0=No)",
                    "pct_sold": "s9q03 (%)",
                    "total_sales_val_tzs": "s9q04 (Total value of sales, TZS)",
                },
                "AASS_2023_24": {
                    "file": "CROP_USE.dta",
                    "sold_indicator": "s9q02__1 (1=Yes, 0=No)",
                    "pct_sold": "s9q03 (%)",
                    "total_sales_val_tzs": "s9q04 (Total value of sales, TZS)",
                },
                "AASS_2024_25": {
                    "file": "CROP_USE.dta",
                    "sold_indicator": "s9q02__1 (1=Yes, 0=No)",
                    "pct_sold": "s9q03 (%)",
                    "total_sales_val_tzs": "s9q04 (Total value of sales, TZS)",
                },
                "NPS_Waves_1_5": {
                    "file": "ag_sec5a",
                    "sold_indicator": "ag5a_01",
                    "quantity_sold_kg": "ag5a_02",
                    "total_sales_val_tzs": "ag5a_03",
                },
            },
        },
        "Mechanization_Power_Regimes_M0_to_M3": {
            "Multi_Power_Hierarchy_Rule": {
                "precedence": "M3 > M2 > M1 > M0",
                "rule": (
                    "Mutually exclusive primary land-preparation and farm-power regime. "
                    "Plots/households using multiple power sources (e.g., tractor primary "
                    "tillage + hand-hoe ridging, or ox-plough + hand-hoe) MUST be flagged "
                    "with `is_multi_power = True` so Step 2 applies deterministic hierarchy M3 > M2 > M1 > M0."
                ),
            },
            "M0_Manual_Hand_Hoe": {
                "definition": "Zero mechanical/animal draft power (baseline manual tillage).",
                "NCSA_2019_20": "R122_USE_TRACTOR_ANIMALS: no q122c0 in [1..6] used (q122c3==0) AND R121_FARM_IMPLEMENTS: only hand tools (q121c0 in [1, 2])",
                "AASS_2022_23": "items_services.dta: no items_service__id in [1, 4, 5, 14] for traction/machinery",
                "AASS_2023_24": "input_Use_roster (metadata id==1 manually operated equipment; no id in [2, 3, 5])",
                "AASS_2024_25": "Household/plot tillage module (manual baseline when no animal/tractor power recorded)",
                "NPS_Waves_1_5": "ag_sec3a land-prep method == Hand-hoe / manual; ag_sec11 no animal/tractor implement used",
            },
            "M1_Animal_Traction_Ox_Ploughing": {
                "definition": "Oxen/donkey ploughing, ridging, or animal-drawn cultivation.",
                "NCSA_2019_20": "R122_USE_TRACTOR_ANIMALS: q122c0 in [1 (Oxen), 2 (Bulls), 3 (Cows), 4 (Donkeys)] with q122c3 > 0; OR R121_FARM_IMPLEMENTS: q121c0 in [4 (Oxen), 5 (Ox Plough), 6 (Ox Seed Planter), 7 (Ox Cart), 13 (Ox Ridger)] with q121c2 == 1",
                "AASS_2022_23": "items_services.dta: items_service__id == 1 (Animal traction rental) with s19q01b == 1",
                "AASS_2023_24": "input_Use_roster: input_Use_roster__id == 2 (animal powered equipment)",
                "AASS_2024_25": "stock_livestock.dta (draught cattle/oxen) + land-prep/traction records",
                "NPS_Waves_1_5": "ag_sec3a land-prep == Ox-plough / Animal traction + ag_sec11 ox-plough/oxen ownership & rental",
            },
            "M2_Two_Wheel_Walking_Tractor_Power_Tiller": {
                "definition": "Single-axle two-wheel walking tractor / power tiller (owned or hired).",
                "NCSA_2019_20": "R122_USE_TRACTOR_ANIMALS: q122c0 == 6 (Power Tiller) with q122c3 > 0; OR R121_FARM_IMPLEMENTS: q121c0 == 12 (Power Tiller) with q121c2 == 1",
                "AASS_2022_23": "Pooled with machinery rental (items_service__id == 4) — flag inability to disaggregate 2WT vs 4WT in AASS 22/23",
                "AASS_2023_24": "input_Use_roster: id in [3, 5] (machine-powered land prep; disaggregation note)",
                "AASS_2024_25": "Machinery/power-tiller roster if present; otherwise pooled mechanical proxy",
                "NPS_Waves_1_5": "ag_sec3a / ag_sec11 power tiller / walking tractor code",
            },
            "M3_Four_Wheel_Tractor": {
                "definition": "Owned or custom-hired four-wheel tractor (disc plough, harrow, rotavator).",
                "NCSA_2019_20": "R122_USE_TRACTOR_ANIMALS: q122c0 == 5 (Tractor) with q122c3 > 0; OR R121_FARM_IMPLEMENTS: q121c0 in [8 (Tractor), 9 (Tractor Plough), 10 (Tractor Harrow)] with q121c2 == 1",
                "AASS_2022_23": "items_services.dta: items_service__id == 4 (Rental of machinery/equipment) OR id == 14 (Fuel for machinery) OR id == 5 (Machinery repair)",
                "AASS_2023_24": "input_Use_roster: id in [3 (machine powered equipment), 5 (machine powered land prep)] + buildings_roster s20q01a__7 (Machinery sheds)",
                "AASS_2024_25": "Machinery rental / fuel / tractor ownership indicators",
                "NPS_Waves_1_5": "ag_sec3a land-prep == Tractor + ag_sec11 tractor/tractor-plough ownership & custom-hire expenditure",
            },
        },
        "Mechanization_and_Labor_Costs": {
            "Mechanization_Draft_Power_Cost_K": {
                "unit": "TZS/ha (stochastic bucket K_ij)",
                "NCSA_2019_20": {
                    "file": "R081/R082, R121, R122",
                    "column": "q811c6 / q821c6 (Land prep cost TZS) + R121 q121c3 (Implement ownership) + R122 q122c4 (Area cultivated)",
                },
                "AASS_2022_23": {
                    "file": "items_services.dta",
                    "column": "s19q02 where items_service__id in [1 (Animal traction rental), 4 (Machinery rental), 5 (Machinery repair/maint), 14 (Fuel for machinery)]",
                },
                "AASS_2023_24": {
                    "file": "input_Use_roster / AASS2024f.dta",
                    "column": "s21q08 (Total rent cost of equipment) + s21q03/s21q04 (Owned equipment count & age for depreciation) + s20q08/s20q09",
                },
                "AASS_2024_25": {
                    "file": "AASS2025.dta",
                    "column": "s20q08 / s20q09 (Agricultural structures/equipment) + machinery/fuel expenditure",
                },
                "NPS_Waves_1_5": {
                    "file": "ag_sec3a / ag_sec11",
                    "column": "Tractor/ox-plough rental fees, fuel/maintenance, implement value for depreciation",
                },
            },
            "Tillage_Weeding_Labor_Cost_L_and_Person_Days": {
                "unit": "TZS/ha (L_ij) & Person-Days/ha (for shadow wage & Return to Labor omega_ij)",
                "NCSA_2019_20": {
                    "plot_ops_tzs": "R081/R082 -> q811c6/q821c6 (Land prep), q811c7b/q821c7b (Planting), q811c8f/q821c8f (Weeding), q811c9f/q821c9f (Harvesting)",
                    "activity_labor": "R291_LABOUR_USE.dta -> q2911c0 (1=Land clearing, 2=Hand tilling, 3=Oxen/tractor tilling, 4=Planting, 5=Weeding, 7=Harvesting), q2911c3 (1-8=Family, 9=Hired)",
                },
                "AASS_2022_23": {
                    "hired_labor_tzs": "items_services.dta -> items_service__id == 13 (Hired workers), items_service__id == 2 (Post-harvest labor)",
                    "physical_person_days": "external_labor_activities.dta -> External_labor__id (1=Free, 2=Exchange, 3=Hired), s18q07 (Workers) * s18q08 (Months) * s18q09 (Days/mo), s18q12/s18q13 (Cash/In-kind pay)",
                },
                "AASS_2023_24": {
                    "file": "CROP_USE.dta / MASIKACROP.dta",
                    "column": "s9q02__4 / s9q07 (Crop paid for labor); labor shortage flags s7q06__8, s7q10__8",
                },
                "AASS_2024_25": {
                    "file": "CROP_USE.dta / MASIKACROP.dta",
                    "column": "s9q02__4 / s9q07 (Crop paid for labor); labor shortage flags s7q06__8",
                },
                "NPS_Waves_1_5": {
                    "file": "ag_sec3a / ag_sec3b",
                    "column": "Family labor person-days by activity (land prep, planting, weeding, harvesting) + hired labor person-days & wages (TZS)",
                },
            },
            "Biochemical_Input_Cost_B": {
                "unit": "TZS/ha (stochastic bucket B_ij: Seeds + Fertilizers + Agro-chemicals)",
                "NCSA_2019_20": {
                    "file": "R081 / R082",
                    "column": "q821c15 (Seeds TZS) + q821c20 (Fertilizer TZS) + q821c25 (Herbicides TZS) + q821c30 (Fungicides TZS) + q821c35 (Insecticides TZS)",
                },
                "AASS_2022_23": {
                    "file": "seeds.dta + inputs.dta",
                    "column": "s10q04 (Purchased seeds TZS) + s11q06a + s11q06b (Fertilizer & pesticide/herbicide values)",
                },
                "AASS_2023_24": {
                    "file": "InputRoster_masika.dta / InputRoster_vuli.dta",
                    "column": "s11q06a + s11q06b (Fertilizer, herbicide, pesticide values) + seed quantity/price",
                },
                "AASS_2024_25": {
                    "file": "inputRoster_masika.dta / inputRoster_vuli.dta",
                    "column": "s11q06a + s11q06b (Fertilizer, herbicide, pesticide values) + seed quantity/price",
                },
                "NPS_Waves_1_5": {
                    "file": "ag_sec3a / ag_sec4a",
                    "column": "Seed cost, organic/inorganic fertilizer value, herbicide & pesticide expenditure (TZS)",
                },
            },
        },
        "IPWRA_Covariates": {
            "Household_Head_Age": {
                "NCSA_2019_20": {"file": "R031_HHRECORD.dta", "column": "q3_1c4 where q3_1c2 == 1 (Head)"},
                "AASS_2022_23": {"file": "AASS2023.dta / household.dta", "column": "holding_head_age / s2q04 (where s2q02 == 1)"},
                "AASS_2023_24": {"file": "HOUSEHOLD.dta", "column": "s2q04 (where s2q02 == 1)"},
                "AASS_2024_25": {"file": "HOUSEHOLD.dta", "column": "s2q04 (where s2q02 == 1)"},
                "NPS_Waves_1_5": {"file": "hh_sec_b", "column": "hh_b04 (Age where hh_b05 == 1 Head)"},
            },
            "Household_Head_Sex": {
                "NCSA_2019_20": {"file": "R031_HHRECORD.dta", "column": "q3_1c3 where q3_1c2 == 1 (1=Male, 2=Female)"},
                "AASS_2022_23": {"file": "AASS2023.dta / household.dta", "column": "holding_head_sex / s2q03"},
                "AASS_2023_24": {"file": "HOUSEHOLD.dta", "column": "s2q03 (where s2q02 == 1)"},
                "AASS_2024_25": {"file": "HOUSEHOLD.dta", "column": "s2q03 (where s2q02 == 1)"},
                "NPS_Waves_1_5": {"file": "hh_sec_b", "column": "hh_b02 (Sex where hh_b05 == 1 Head)"},
            },
            "Household_Head_Education": {
                "NCSA_2019_20": {"file": "R031_HHRECORD.dta", "column": "q3_1c8 (Education level attained)"},
                "AASS_2022_23": {"file": "household.dta", "column": "s2q07 (Highest educational qualification)"},
                "AASS_2023_24": {"file": "HOUSEHOLD.dta", "column": "s2q07 (Highest educational qualification)"},
                "AASS_2024_25": {"file": "HOUSEHOLD.dta", "column": "s2q07 (Highest educational qualification)"},
                "NPS_Waves_1_5": {"file": "hh_sec_c", "column": "hh_c07 (Highest grade completed)"},
            },
            "Household_Size": {
                "NCSA_2019_20": {"derivation": "Count of member records per HHID in R031_HHRECORD.dta"},
                "AASS_2022_23": {"derivation": "Count of member records per holding_id in household.dta"},
                "AASS_2023_24": {"derivation": "Count of member records per holding_id in HOUSEHOLD.dta"},
                "AASS_2024_25": {"derivation": "Count of member records per Holding_ID in HOUSEHOLD.dta"},
                "NPS_Waves_1_5": {"derivation": "Count of member records per y*_hhid in hh_sec_b"},
            },
            "Total_Farm_Size": {
                "NCSA_2019_20": {"file": "R000_SOV.dta / R041", "column": "q4_1_8 / sum(q4_1_c2)"},
                "AASS_2022_23": {"file": "field.dta", "column": "sum(s3q04a_acres) per holding_id"},
                "AASS_2023_24": {"file": "FIELD.dta", "column": "sum(s3q04a_acres) per holding_id"},
                "AASS_2024_25": {"file": "FIELD.dta", "column": "sum(s3q04a_acres) per HHFARMID"},
                "NPS_Waves_1_5": {"file": "ag_sec2a", "column": "sum(area_gps / area_farmer) per hhid"},
            },
            "Plot_Size_ha": {
                "NCSA_2019_20": {"file": "R081 / R082", "column": "q811c7a / q821c7a * 0.404686 (Individual plot planted area ha)"},
                "AASS_2022_23": {"file": "masikaplot.dta / vuliplot.dta", "column": "s6q03_acres / s4q03_acres * 0.404686"},
                "AASS_2023_24": {"file": "MASIKAPLOT.dta / VULIPLOT.dta", "column": "s6q03_acres / s4q03_acres * 0.404686"},
                "AASS_2024_25": {"file": "MASIKAPLOT.dta / VULIPLOT.dta", "column": "s6q03_acres / s4q03_acres * 0.404686"},
                "NPS_Waves_1_5": {"file": "ag_sec3a", "column": "area_gps * 0.404686 (GPS plot area ha)"},
            },
            "Plot_Slope_Topography_and_Soil_Type": {
                "NCSA_2019_20": {"file": "R062_FARMING_METHODS.dta / R126_SOIL_EROSION.dta", "column": "q6_2c0 (Contour farming for sloped lands), q12_6_1 (Erosion)"},
                "AASS_2022_23": {"file": "field.dta / masikaplot.dta", "column": "s3q06 (Soil type) / s6q07 (Soil amendments)"},
                "AASS_2023_24": {"file": "FIELD.dta / MASIKAPLOT.dta", "column": "s3q06 (Soil type) / conservation practices"},
                "AASS_2024_25": {"file": "FIELD.dta", "column": "s3q06 (Dominant soil type on field)"},
                "NPS_Waves_1_5": {"file": "ag_sec3a", "column": "ag3a_10 (Soil type), ag3a_11 (Soil quality), ag3a_12 (Slope/topography)"},
            },
            "Soil_Quality_Erosion": {
                "NCSA_2019_20": {"file": "R000_SOV.dta / R126", "column": "q12_6_1 (Erosion problem: 1=Yes, 2=No)"},
                "AASS_2022_23": {"file": "masikaplot.dta", "column": "s6q07 / s6q08 (Organic soil amendments)"},
                "AASS_2023_24": {"file": "MASIKAPLOT.dta", "column": "Soil conservation practices"},
                "AASS_2024_25": {"file": "AASS2025.dta", "column": "pme1q01 (Slash/burn clearing practices)"},
                "NPS_Waves_1_5": {"file": "ag_sec3a", "column": "ag3a_14 / ag3a_15 (Erosion control & soil quality)"},
            },
            "Household_Asset_Index_and_Draught_Livestock": {
                "NCSA_2019_20": {"file": "R342_HOUSE_ASSETS.dta + R152_CATTLE_POPULATION.dta + R122", "column": "Asset ownership PCA + Cattle/Oxen herd count (q122c0 in [1..4])"},
                "AASS_2022_23": {"file": "household.dta / AASS2023.dta", "column": "Asset & livestock holdings"},
                "AASS_2023_24": {"file": "HOUSEHOLD.dta / buildings_roster.dta", "column": "Farm structures & asset holdings"},
                "AASS_2024_25": {"file": "stock_livestock.dta / livestock_type.dta", "column": "Cattle/oxen/donkey stock counts"},
                "NPS_Waves_1_5": {"file": "hh_sec_m / ag_sec10a", "column": "Durable asset index + Cattle/Oxen/Donkey ownership"},
            },
            "Credit_Access": {
                "NCSA_2019_20": {"file": "R000_SOV.dta", "column": "q13_1 (Received credit: 1=Yes, 2=No)"},
                "AASS_2022_23": {"file": "AASS2023.dta", "column": "s19q04a (Credit: 1=Yes, 0=No), s19q06a (Farming loan)"},
                "AASS_2023_24": {"file": "AASS2024f.dta", "column": "Household financial services access"},
                "AASS_2024_25": {"file": "shocks_roster.dta", "column": "pme5q04__1 (Formal credit), pme5q04__2 (Informal credit)"},
                "NPS_Waves_1_5": {"file": "hh_sec_p / ag_sec12", "column": "Credit access & agricultural loan indicator"},
            },
            "Extension_Contact": {
                "NCSA_2019_20": {"file": "R000_SOV.dta / R141", "column": "q14_1 (Extension advice: 1=Yes, 2=No), R141_EXTENSION_MESSAGES"},
                "AASS_2022_23": {"file": "items_services.dta", "column": "s19q01b where items_service__id == 9 (Extension services)"},
                "AASS_2023_24": {"file": "wen_TZA.dta", "column": "Extension service interactions"},
                "AASS_2024_25": {"file": "AASS2025.dta / pme_6_Roster.dta", "column": "pme6q13 (Visits received), pme6q14 (Visits made)"},
                "NPS_Waves_1_5": {"file": "ag_sec12", "column": "Extension advice received (yes/no, source)"},
            },
            "Distance_to_Market_Roads": {
                "NCSA_2019_20": {"file": "R310_ACCESS_INFRASTUCTURE.dta", "column": "q310c2 (Distance in Km to Feeder road, Trunk road, Markets)"},
                "AASS_2022_23": {"file": "household.dta", "column": "Cluster accessibility metrics"},
                "AASS_2023_24": {"file": "wen_TZA.dta", "column": "Community infrastructure distances"},
                "AASS_2024_25": {"file": "AASS2025.dta", "column": "Community infrastructure distances"},
                "NPS_Waves_1_5": {"file": "hh_geovariables", "column": "dist_road, dist_market (km)"},
            },
            "Distance_to_AgroDealer_Mechanization_Hub": {
                "NCSA_2019_20": {"file": "R310_ACCESS_INFRASTUCTURE.dta / R124_ACCESS_FARM_INPUTS.dta", "column": "q310c2 (Distance to Agro-dealer / Input market), R124 distance/access"},
                "AASS_2022_23": {"file": "items_services.dta / household.dta", "column": "Service access / EA cluster hub proxy"},
                "AASS_2023_24": {"file": "wen_TZA.dta", "column": "Community agro-dealer & service hub proximity"},
                "AASS_2024_25": {"file": "pme_6_Roster.dta", "column": "pme6q03__60 (Availability of inputs or equipment)"},
                "NPS_Waves_1_5": {"file": "hh_geovariables / com_sec", "column": "dist_popcenter / community distance to agro-dealer & tractor hire hub"},
            },
        },
        "Agroecological_Zones_Mapping": {
            "Total_AEZs": 9,
            "Zones": {
                "Central_Semi_Arid": {"code": 1, "regions": ["Dodoma", "Singida"], "reg_codes": [1, 13]},
                "Northern_Highlands": {"code": 2, "regions": ["Arusha", "Kilimanjaro", "Manyara"], "reg_codes": [2, 3, 21]},
                "Southern_Highlands": {"code": 3, "regions": ["Iringa", "Mbeya", "Njombe", "Ruvuma", "Songwe", "Rukwa", "Katavi"], "reg_codes": [10, 11, 12, 15, 22, 23, 26]},
                "Lake_Victoria_Basin": {"code": 4, "regions": ["Mwanza", "Geita", "Simiyu", "Kagera", "Mara", "Shinyanga"], "reg_codes": [17, 18, 19, 20, 24, 25]},
                "Western_Miombo": {"code": 5, "regions": ["Tabora", "Kigoma"], "reg_codes": [14, 16]},
                "Eastern_Coastal_Lowlands": {"code": 6, "regions": ["Morogoro", "Pwani", "Dar es Salaam"], "reg_codes": [5, 6, 7]},
                "Southern_Coastal_Lowlands": {"code": 7, "regions": ["Lindi", "Mtwara"], "reg_codes": [8, 9]},
                "Northern_Coastal_Lowlands": {"code": 8, "regions": ["Tanga"], "reg_codes": [4]},
                "Zanzibar_Archipelago": {"code": 9, "regions": ["Kaskazini Unguja", "Kusini Unguja", "Mjini Magharibi", "Kaskazini Pemba", "Kusini Pemba"], "reg_codes": [51, 52, 53, 54, 55]},
            },
        },
    }
    return mapping


# -----------------------------------------------------------------------------
# 4. SAMPLE SIZE CALCULATION ENGINE (CROP x REGIME M0-M3)
# -----------------------------------------------------------------------------

def _empty_regime_counts():
    return {"total_n": 0, "M0": 0, "M1": 0, "M2": 0, "M3": 0, "multi_power_flagged": 0}


def _assign_ncsa_hh_regime(df_r122, df_r121):
    """
    Derives household-level mechanization regime (M3 > M2 > M1 > M0) and
    multi-power flag from NCSA R122_USE_TRACTOR_ANIMALS and R121_FARM_IMPLEMENTS.
    """
    hh_powers = defaultdict(set)

    if df_r122 is not None and not df_r122.empty:
        used = df_r122[df_r122["q122c3"] > 0]
        for hhid, code in zip(used["HHID"], used["q122c0"]):
            if code in (1, 2, 3, 4):
                hh_powers[hhid].add("M1")
            elif code == 6:
                hh_powers[hhid].add("M2")
            elif code == 5:
                hh_powers[hhid].add("M3")

    if df_r121 is not None and not df_r121.empty:
        used_impl = df_r121[df_r121["q121c2"] == 1]
        for hhid, code in zip(used_impl["HHID"], used_impl["q121c0"]):
            if code in (4, 5, 6, 7, 13):
                hh_powers[hhid].add("M1")
            elif code == 12:
                hh_powers[hhid].add("M2")
            elif code in (8, 9, 10):
                hh_powers[hhid].add("M3")

    hh_regime = {}
    hh_multi = {}
    for hhid, pset in hh_powers.items():
        if "M3" in pset:
            hh_regime[hhid] = "M3"
        elif "M2" in pset:
            hh_regime[hhid] = "M2"
        elif "M1" in pset:
            hh_regime[hhid] = "M1"
        else:
            hh_regime[hhid] = "M0"
        hh_multi[hhid] = len(pset) > 1
    return hh_regime, hh_multi


def _count_aass_wave(wave_dir, mc_name, vc_name, crop_col, id_col, hh_regime=None, hh_multi=None, crop_codes=None):
    """Counts unweighted plot observations by Crop x Regime for an AASS wave."""
    mc_path = os.path.join(wave_dir, mc_name)
    vc_path = os.path.join(wave_dir, vc_name)
    df_mc = pd.read_stata(mc_path, columns=[id_col, crop_col], convert_categoricals=False)
    df_vc = pd.read_stata(vc_path, columns=[id_col, crop_col], convert_categoricals=False)
    df_all = pd.concat([df_mc, df_vc], ignore_index=True)

    res = {}
    for cname in TARGET_CROP_GROUPS:
        codes = crop_codes[cname]
        sub = df_all[df_all[crop_col].isin(codes)]
        counts = _empty_regime_counts()
        counts["total_n"] = int(len(sub))
        if hh_regime is not None:
            reg_series = sub[id_col].map(hh_regime).fillna("M0")
            for r in POWER_REGIMES:
                counts[r] = int((reg_series == r).sum())
            if hh_multi is not None:
                counts["multi_power_flagged"] = int(sub[id_col].map(hh_multi).fillna(False).sum())
        else:
            counts["note"] = "Mechanization roster not on disk; total_n only"
        res[cname] = counts
    return res


def calculate_sample_sizes():
    """
    Computes unweighted plot observation counts across NCSA_2019_20,
    AASS_2022_23, AASS_2023_24, AASS_2024_25, and NPS_Waves_1_5 broken down
    by Crop (Maize, Paddy, Legumes) x Mechanization Regime (M0, M1, M2, M3).
    """
    results = {}

    if not HAS_PANDAS:
        return {
            "status": "pandas_unavailable_in_current_python",
            "waves": {},
        }

    # 1. NCSA 2019/20
    try:
        ncsa_dir = os.path.join(DATA_DIR, "NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI")
        df_long = pd.read_stata(os.path.join(ncsa_dir, "R082_LONG_RAINY_SEASON.dta"), columns=["region", "district", "finalweight_hh", "q821c4"], convert_categoricals=False)
        df_short = pd.read_stata(os.path.join(ncsa_dir, "R081_SHORT_RAINY_SEASON.dta"), columns=["region", "district", "finalweight_hh", "q811c4"], convert_categoricals=False)
        df_long = df_long.rename(columns={"q821c4": "crop_code"})
        df_short = df_short.rename(columns={"q811c4": "crop_code"})
        df_ncsa = pd.concat([df_long, df_short], ignore_index=True)

        df_sov = pd.read_stata(os.path.join(ncsa_dir, "R000_SOV.dta"), columns=["HHID"], convert_categoricals=False)
        df_r122 = pd.read_stata(os.path.join(ncsa_dir, "R122_USE_TRACTOR_ANIMALS.dta"), columns=["HHID", "q122c0", "q122c3"], convert_categoricals=False)
        df_r121 = pd.read_stata(os.path.join(ncsa_dir, "R121_FARM_IMPLEMENTS.dta"), columns=["HHID", "q121c0", "q121c2"], convert_categoricals=False)
        hh_reg, hh_mult = _assign_ncsa_hh_regime(df_r122, df_r121)

        sov_reg = df_sov["HHID"].map(hh_reg).fillna("M0")
        hh_m0 = int((sov_reg == "M0").sum())
        hh_m1 = int((sov_reg == "M1").sum())
        hh_m2 = int((sov_reg == "M2").sum())
        hh_m3 = int((sov_reg == "M3").sum())
        hh_multi_n = int(df_sov["HHID"].map(hh_mult).fillna(False).sum())

        ncsa_res = {}
        for cname in TARGET_CROP_GROUPS:
            sub = df_ncsa[df_ncsa["crop_code"].isin(WAVE_CROP_CODES["NCSA_2019_20"][cname])]
            counts = _empty_regime_counts()
            counts["total_n"] = int(len(sub))
            counts["note"] = (
                f"R081/R082 lack HHID; HH-level R122/R121 (N={len(df_sov):,}): "
                f"M0={hh_m0:,}, M1={hh_m1:,}, M2={hh_m2:,}, M3={hh_m3:,}, multi={hh_multi_n:,}"
            )
            ncsa_res[cname] = counts
        results["NCSA_2019_20"] = ncsa_res
    except Exception as e:
        results["NCSA_2019_20"] = {"error": str(e)}

    # 2. AASS 2022/23
    try:
        aass22_dir = os.path.join(DATA_DIR, "AASS 2022_2023")
        df_srv = pd.read_stata(os.path.join(aass22_dir, "items_services.dta"), columns=["holding_id", "items_service__id", "s19q01b"], convert_categoricals=False)
        paid = df_srv[df_srv["s19q01b"] == 1]
        hh_powers = defaultdict(set)
        for hid, sid in zip(paid["holding_id"], paid["items_service__id"]):
            if sid == 1:
                hh_powers[hid].add("M1")
            elif sid in (4, 5, 14):
                hh_powers[hid].add("M3")
        hh_reg22 = {
            hid: ("M3" if "M3" in ps else ("M1" if "M1" in ps else "M0"))
            for hid, ps in hh_powers.items()
        }
        hh_mult22 = {hid: len(ps) > 1 for hid, ps in hh_powers.items()}
        results["AASS_2022_23"] = _count_aass_wave(
            aass22_dir, "masikacrop.dta", "vulicrop.dta",
            "crop_id", "holding_id", hh_reg22, hh_mult22, WAVE_CROP_CODES["AASS_2022_23"]
        )
    except Exception as e:
        results["AASS_2022_23"] = {"error": str(e)}

    # 3. AASS 2023/24
    try:
        aass23_dir = os.path.join(DATA_DIR, "AASS 2023_2024")
        results["AASS_2023_24"] = _count_aass_wave(
            aass23_dir, "MASIKACROP.dta", "VULICROP.dta",
            "crop_id", "holding_id", None, None, WAVE_CROP_CODES["AASS_2023_24"]
        )
    except Exception as e:
        results["AASS_2023_24"] = {"error": str(e)}

    # 4. AASS 2024/25
    try:
        aass24_dir = os.path.join(DATA_DIR, "AASS 2024_2025")
        df_mc = pd.read_stata(os.path.join(aass24_dir, "MASIKACROP.dta"), columns=["HHFARMID", "MASIKACROP__id"], convert_categoricals=False).rename(columns={"MASIKACROP__id": "crop_code"})
        df_vc = pd.read_stata(os.path.join(aass24_dir, "VULICROP.dta"), columns=["HHFARMID", "VULICROP__id"], convert_categoricals=False).rename(columns={"VULICROP__id": "crop_code"})
        df_all = pd.concat([df_mc, df_vc], ignore_index=True)
        aass24_res = {}
        for cname in TARGET_CROP_GROUPS:
            sub = df_all[df_all["crop_code"].isin(WAVE_CROP_CODES["AASS_2024_25"][cname])]
            counts = _empty_regime_counts()
            counts["total_n"] = int(len(sub))
            counts["note"] = "Mechanization roster not on disk; total_n only"
            aass24_res[cname] = counts
        results["AASS_2024_25"] = aass24_res
    except Exception as e:
        results["AASS_2024_25"] = {"error": str(e)}

    # 5. NPS Waves 1-5
    nps_specs = [
        ("NPS_Wave_1", os.path.join(DATA_DIR, "NPS Wave 1 2008_2009 TZA_2008_NPS1", "TZA_2008_NPS1", "SEC_4A.dta"), os.path.join(DATA_DIR, "NPS Wave 1 2008_2009 TZA_2008_NPS1", "TZA_2008_NPS1", "SEC_11_ALL.dta"), "hhid", "zaocode", "impcode", "s11q4", "s11q6", (3, 4, 5, 6), (), (7, 8, 9)),
        ("NPS_Wave_2", os.path.join(DATA_DIR, "NPS Wave 2 2010_2011  Agriculture", "Agriculture", "AG_SEC4A.dta"), os.path.join(DATA_DIR, "NPS Wave 2 2010_2011  Agriculture", "Agriculture", "AG_SEC11.dta"), "y2_hhid", "zaocode", "itemcode", "ag11_04", "ag11_06", (3, 4, 5), (), (6, 7, 8)),
        ("NPS_Wave_3", os.path.join(DATA_DIR, "NPS Wave 3 2012_2013 STATA_Y3_DATASETS", "AG_SEC_4A.dta"), os.path.join(DATA_DIR, "NPS Wave 3 2012_2013 STATA_Y3_DATASETS", "AG_SEC_11.dta"), "y3_hhid", "zaocode", "itemid", "ag11_04", "ag11_06", (3, 4, 5), (14,), (6, 7, 8)),
        ("NPS_Wave_4", os.path.join(DATA_DIR, "NPS Wave 4 2014_2015 NPS-4-2014-STATA", "ag_sec_4a.dta"), os.path.join(DATA_DIR, "NPS Wave 4 2014_2015 NPS-4-2014-STATA", "ag_sec_11.dta"), "y4_hhid", "zaocode", "itemid", "ag11_04", "ag11_06", (3, 4, 5), (14,), (6, 7, 8)),
        ("NPS_Wave_5", os.path.join(DATA_DIR, "NPS Wave 5 2020_2021 Agriculture-STATA-NPS-Wave5", "AG_SEC_4A.dta"), os.path.join(DATA_DIR, "NPS Wave 5 2020_2021 Agriculture-STATA-NPS-Wave5", "AG_SEC_11.dta"), "y5_hhid", "cropid", "itemid", "ag11_04", "ag11_06", (3, 4, 5), (14,), (6, 7, 8)),
    ]
    for w_key, c_path, i_path, id_col, crop_col, item_col, use_col, rent_col, m1_codes, m2_codes, m3_codes in nps_specs:
        try:
            df_c = pd.read_stata(c_path, columns=[id_col, crop_col], convert_categoricals=False)
            df_i = pd.read_stata(i_path, columns=[id_col, item_col, use_col, rent_col], convert_categoricals=False)
            used_i = df_i[(df_i[use_col] == 1) | (df_i[rent_col] == 1)]
            hh_powers = defaultdict(set)
            for hid, code in zip(used_i[id_col], used_i[item_col]):
                if code in m1_codes:
                    hh_powers[hid].add("M1")
                elif code in m2_codes:
                    hh_powers[hid].add("M2")
                elif code in m3_codes:
                    hh_powers[hid].add("M3")
            hh_reg = {h: ("M3" if "M3" in ps else ("M2" if "M2" in ps else ("M1" if "M1" in ps else "M0"))) for h, ps in hh_powers.items()}
            hh_mult = {h: len(ps) > 1 for h, ps in hh_powers.items()}

            w_res = {}
            for cname in TARGET_CROP_GROUPS:
                sub = df_c[df_c[crop_col].isin(WAVE_CROP_CODES["NPS_Waves_1_5"][cname])]
                counts = _empty_regime_counts()
                counts["total_n"] = int(len(sub))
                reg_series = sub[id_col].map(hh_reg).fillna("M0")
                for r in POWER_REGIMES:
                    counts[r] = int((reg_series == r).sum())
                counts["multi_power_flagged"] = int(sub[id_col].map(hh_mult).fillna(False).sum())
                w_res[cname] = counts
            results[w_key] = w_res
        except Exception as e:
            results[w_key] = {"error": str(e)}

    return {"status": "OK", "waves": results}


# -----------------------------------------------------------------------------
# 5. REPORT GENERATOR (MARKDOWN & JSON)
# -----------------------------------------------------------------------------

WAVE_DISPLAY_ORDER = [
    ("NPS_Wave_1", "NPS W1 08/09"),
    ("NPS_Wave_2", "NPS W2 10/11"),
    ("NPS_Wave_3", "NPS W3 12/13"),
    ("NPS_Wave_4", "NPS W4 14/15"),
    ("NCSA_2019_20", "NCSA 2019/20"),
    ("NPS_Wave_5", "NPS W5 20/21"),
    ("AASS_2022_23", "AASS 2022/23"),
    ("AASS_2023_24", "AASS 2023/24"),
    ("AASS_2024_25", "AASS 2024/25"),
]


def generate_markdown_report(inventory, crosswalk, dta_labels, ddi_codebooks, sample_sizes):
    """Builds a publication-grade markdown diagnostic inspection report for Study 2."""
    md = []
    total_files = len(inventory)
    total_mb = sum(f["size_mb"] for f in inventory)
    ext_counts = Counter(f["extension"] for f in inventory)

    md.append("# Schema & Data Diagnostic Inspection Report")
    md.append("## Study 2: Risk-Adjusted Returns to Smallholder Farm Mechanization in Tanzania: A Causal-Stochastic Simulation of Hand-Hoe, Animal Traction, and Tractor Power Regimes\n")
    md.append("**Mode:** Read-Only Diagnostic Audit | **Script:** `src/01_audit_metadata.py`\n")

    md.append("### Executive Summary")
    md.append(f"- **Total Files Inventoried:** {total_files}")
    md.append(f"- **Total Storage Footprint:** {total_mb:.2f} MB")
    md.append("- **File Formats:** " + ", ".join([f"`{k}`: {v}" for k, v in sorted(ext_counts.items())]))
    md.append("- **Survey Coverage (Active Waves in `data/`):**")
    md.append("  1. **NCSA 2019/20:** National Census of Agriculture (Small-Scale Farmers).")
    md.append("  2. **AASS 2022/23:** Annual Agricultural Sample Survey.")
    md.append("  3. **AASS 2023/24:** Annual Agricultural Sample Survey.")
    md.append("  4. **AASS 2024/25:** Annual Agricultural Sample Survey.")
    md.append(f"- **Live `.dta` Label Extraction (`pyreadstat`):** `{dta_labels.get('status')}`")
    md.append(f"- **DDI Codebooks Parsed:** {', '.join(ddi_codebooks.keys())}\n")

    md.append("---\n")
    md.append("## 1. Cross-Wave Target Crop × Mechanization Regime ($M_0 - M_3$) Sample Sizes")
    md.append("Unweighted plot observation counts for Maize, Paddy, and Legumes across power regimes ($M_3 > M_2 > M_1 > M_0$):\n")
    md.append("| Survey Wave | Crop | Total $N$ | $M_0$ (Hand-Hoe) | $M_1$ (Animal Traction) | $M_2$ (2WT / Power Tiller) | $M_3$ (4WT Tractor) | Multi-Power Flagged | Notes |")
    md.append("|---|---|---|---|---|---|---|---|---|")

    waves_ss = sample_sizes.get("waves", {})
    if not waves_ss:
        md.append(f"| *All Waves* | *N/A* | - | - | - | - | - | - | `{sample_sizes.get('status', 'No data')}` |")
    else:
        for w_key, w_name in WAVE_DISPLAY_ORDER:
            w_data = waves_ss.get(w_key, {})
            if "error" in w_data:
                md.append(f"| **{w_name}** | *Error* | - | - | - | - | - | - | `{w_data['error']}` |")
                continue
            for cname in TARGET_CROP_GROUPS:
                cdata = w_data.get(cname, {})
                if not cdata:
                    continue
                note = cdata.get("note", "")
                md.append(
                    f"| **{w_name}** | {cname} | {cdata.get('total_n', 0):,} | "
                    f"{cdata.get('M0', 0):,} | {cdata.get('M1', 0):,} | "
                    f"{cdata.get('M2', 0):,} | {cdata.get('M3', 0):,} | "
                    f"{cdata.get('multi_power_flagged', 0):,} | {note} |"
                )

    md.append("\n---\n")
    md.append("## 2. Harmonized Variable Crosswalk Matrix ($M_0 - M_3$, Cost Buckets, IPWRA)")
    cw = crosswalk

    md.append("### A. Target Crop Groups (Maize, Paddy, Legumes)")
    md.append("| Crop Group | NCSA 2019/20 | AASS 2022/23 | AASS 2023/24 | AASS 2024/25 | NPS Waves 1–5 |")
    md.append("|---|---|---|---|---|---|")
    for crop, details in cw["Target_Crops"].items():
        row = [f"**{crop}**"]
        for w_key, _ in WAVE_DISPLAY_ORDER:
            wd = details.get(w_key, {})
            row.append(f"`{wd.get('codes')}` (`{wd.get('column')}`)")
        md.append("| " + " | ".join(row) + " |")

    md.append("\n### B. Mechanization Power Regimes ($M_0 - M_3$)")
    md.append("| Regime | Definition | Hierarchy & Multi-Power Rule |")
    md.append("|---|---|---|")
    for r_key in ("M0_Manual_Hand_Hoe", "M1_Animal_Traction_Ox_Ploughing", "M2_Two_Wheel_Walking_Tractor_Power_Tiller", "M3_Four_Wheel_Tractor"):
        r_info = cw["Mechanization_Power_Regimes_M0_to_M3"][r_key]
        md.append(f"| **{r_key.replace('_', ' ')}** | {r_info['definition']} | Deterministic precedence: $M_3 > M_2 > M_1 > M_0$ |")

    md.append("\n### C. Stochastic Cost Buckets ($\\tilde{K}, \\tilde{L}, \\tilde{B}$) & IPWRA Covariates")
    md.append("| Construct | NCSA 2019/20 | AASS 2022/23 | AASS 2023/24 | AASS 2024/25 | NPS Waves 1–5 |")
    md.append("|---|---|---|---|---|---|")
    for construct, details in {**cw["Mechanization_and_Labor_Costs"], **cw["IPWRA_Covariates"]}.items():
        cells = [f"**{construct.replace('_', ' ')}**"]
        for w_key, _ in WAVE_DISPLAY_ORDER:
            wd = details.get(w_key, {})
            val = wd.get("column") or wd.get("plot_ops_tzs") or wd.get("hired_labor_tzs") or wd.get("derivation") or wd.get("file") or "Available in module"
            cells.append(f"`{val}`")
        md.append("| " + " | ".join(cells) + " |")

    md.append("\n---\n")
    md.append("## 3. Live `.dta` Variable & Value Label Verification (`pyreadstat`)")
    if not dta_labels.get("pyreadstat_available"):
        md.append("> **Note:** `pyreadstat` was not available in the active Python interpreter during this run. Install `requirements.txt` in `.venv` to embed live `.dta` variable and value label dictionaries.\n")
    else:
        for w_key, w_name in WAVE_DISPLAY_ORDER:
            w_lbls = dta_labels.get("waves", {}).get(w_key, {})
            md.append(f"### {w_name} (Files inspected: {w_lbls.get('files_inspected', 0)})")
            for dom in ("crop_codes", "land_prep_tillage", "implement_ownership", "labor_activity"):
                dom_dict = w_lbls.get(dom, {})
                md.append(f"- **{dom}:** {len(dom_dict)} matched variables")
                for k, v in list(dom_dict.items())[:8]:
                    sample_vals = ", ".join(f"{vk}={vv}" for vk, vv in list(v.get("value_labels", {}).items())[:6])
                    md.append(f"  - `{k}` ({v.get('label', '')}): {sample_vals or 'No value labels'}")

    md.append("\n---\n")
    md.append("## 4. Spatial Alignment & Agroecological Zones (AEZs)")
    md.append("| Zone ID | Agroecological Zone (AEZ) | Region Codes (NBS Standard) | Regions Included |")
    md.append("|---|---|---|---|")
    for zname, zinfo in cw["Agroecological_Zones_Mapping"]["Zones"].items():
        rcodes_str = ", ".join(str(c) for c in zinfo["reg_codes"])
        rnames_str = ", ".join(zinfo["regions"])
        md.append(f"| **AEZ {zinfo['code']}** | {zname.replace('_', ' ')} | `{rcodes_str}` | {rnames_str} |")

    md.append("\n---\n")
    md.append("## 4b. DDI Codebook Verification Summary")
    for w_key, w_name in WAVE_DISPLAY_ORDER:
        info = ddi_codebooks.get(w_key, {})
        if not info:
            continue
        md.append(f"### {w_name} (`{info.get('source')}` — {info.get('matched_count', 0)} matched variables)")
        for m in info.get("matches", [])[:12]:
            vc = m.get("value_codes", "")
            vc_str = f" — `{vc[:160]}`" if vc else ""
            md.append(f"- `{m['file']}::{m['variable']}`: {m['label']}{vc_str}")

    md.append("\n---\n")
    md.append("## 5. Complete Directory & File Inventory")
    md.append("| # | Subdirectory / File | Extension | Size (MB) | Rows ($N$) | Columns ($K$) | Status |")
    md.append("|---|---|---|---|---|---|---|")
    for i, f in enumerate(sorted(inventory, key=lambda x: x["relative_path"]), 1):
        r_str = f"{f['rows']:,}" if f["rows"] is not None else "-"
        c_str = f"{f['cols']:,}" if f["cols"] is not None else "-"
        md.append(f"| {i} | `{f['relative_path']}` | `{f['extension']}` | {f['size_mb']} | {r_str} | {c_str} | {f['status']} |")

    return "\n".join(md)


# -----------------------------------------------------------------------------
# 6. MAIN EXECUTION CONTROLLER
# -----------------------------------------------------------------------------

def main():
    print("================================================================================")
    print(" STUDY 2 DIAGNOSTIC PIPELINE: SMALLHOLDER FARM MECHANIZATION IN TANZANIA")
    print("================================================================================")
    print(f"Executing in: {BASE_DIR}")
    print(f"Data root:    {DATA_DIR}")
    print(f"Outputs:      {OUTPUTS_DIR}")
    print("--------------------------------------------------------------------------------")

    print("[1/5] Running comprehensive file & directory inventory...")
    inventory = run_inventory_scan()
    print(f"      Scanned {len(inventory)} total files across all directories.")

    print("[2/5] Extracting live .dta variable & value labels (pyreadstat) and parsing DDI codebooks...")
    dta_labels = extract_dta_metadata_labels()
    ddi_codebooks = parse_ddi_codebooks()
    print(f"      Label extraction status: {dta_labels.get('status')} | DDI codebooks parsed: {len(ddi_codebooks)}")

    print("[3/5] Constructing harmonized Study 2 variable crosswalk (M0-M3)...")
    crosswalk = extract_wave_variable_crosswalk()

    print("[4/5] Computing Crop x Mechanization Regime (M0-M3) sample sizes...")
    sample_sizes = calculate_sample_sizes()

    json_path = os.path.join(OUTPUTS_DIR, "schema_mapping.json")
    print(f"[5/5] Writing outputs to {json_path} and schema_inspection_report.md...")
    full_output = {
        "metadata": {
            "study": "Study 2: Risk-Adjusted Returns to Smallholder Farm Mechanization in Tanzania",
            "country": "Tanzania",
            "total_files": len(inventory),
        },
        "sample_sizes": sample_sizes,
        "ddi_codebook_verification": ddi_codebooks,
        "dta_metadata_labels": dta_labels,
        "variable_crosswalk": crosswalk,
        "file_inventory": inventory,
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(full_output, f, indent=2, ensure_ascii=False)

    md_path = os.path.join(OUTPUTS_DIR, "schema_inspection_report.md")
    md_content = generate_markdown_report(inventory, crosswalk, dta_labels, ddi_codebooks, sample_sizes)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print("--------------------------------------------------------------------------------")
    print("[SUCCESS] All Study 2 diagnostics generated!")
    print("================================================================================")
    print("\nEXECUTIVE CONSOLE SUMMARY:")
    print(f"1. Total Datasets & Files: {len(inventory)} files ({sum(f['size_mb'] for f in inventory):.2f} MB)")
    print("\n2. Unweighted Crop x Mechanization Regime (M0-M3) Sample Sizes:")
    print("   +---------------+---------+-----------+---------+---------+---------+---------+-------+")
    print("   | Survey Wave   | Crop    | Total N   | M0(Hoe) | M1(Ox)  | M2(2WT) | M3(4WT) | Multi |")
    print("   +---------------+---------+-----------+---------+---------+---------+---------+-------+")
    waves_ss = sample_sizes.get("waves", {})
    if not waves_ss:
        print(f"   | (pandas unavailable: {sample_sizes.get('status')})                                      |")
    else:
        for w_key, w_name in WAVE_DISPLAY_ORDER:
            w_data = waves_ss.get(w_key, {})
            if "error" in w_data:
                print(f"   | {w_name:13} | ERROR   | {w_data['error'][:57]:57} |")
                continue
            for cname in TARGET_CROP_GROUPS:
                c = w_data.get(cname, {})
                print(
                    f"   | {w_name:13} | {cname:7} | {c.get('total_n', 0):9,d} | "
                    f"{c.get('M0', 0):7,d} | {c.get('M1', 0):7,d} | "
                    f"{c.get('M2', 0):7,d} | {c.get('M3', 0):7,d} | {c.get('multi_power_flagged', 0):5,d} |"
                )
    print("   +---------------+---------+-----------+---------+---------+---------+---------+-------+")
    print(f"\nReport saved to: file://{md_path}")
    print(f"JSON mapping saved to: file://{json_path}")
    print("================================================================================")


if __name__ == "__main__":
    main()
