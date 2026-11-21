#!/usr/bin/env python3
"""
scan_ncsa_dictionary.py
=======================
Automated scanner and data dictionary generator for the National Census of 
Agriculture (NCSA) 2019/2020 dataset (and Stata .dta format 118 files).

Features:
- Pure Python (Standard library only: struct, os, sys, glob, csv, json, argparse)
- Fast binary extraction of variable names, labels, formats, storage types,
  and complete value label mappings (codebooks).
- Generates:
  1. Detailed Variable Dictionary (.csv)
  2. Structured Metadata Catalog (.json)
  3. Formatted Reference Document (.md)
  4. File and Table Inventory (.csv)
- Built-in search functionality across variables, labels, and value labels.

Usage:
  python3 scan_ncsa_dictionary.py
  python3 scan_ncsa_dictionary.py --search irrigation
  python3 scan_ncsa_dictionary.py --data-dir "data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI" --output-dir "data/ncsa_2019_metadata"
"""

import os
import sys
import glob
import struct
import csv
import json
import argparse
from pathlib import Path

TYPE_MAP = {
    65526: ('byte', 'Numeric', 'Discrete'),
    65527: ('int', 'Numeric', 'Discrete'),
    65528: ('long', 'Numeric', 'Discrete'),
    65529: ('float', 'Numeric', 'Continuous'),
    65530: ('double', 'Numeric', 'Continuous'),
    32768: ('strL', 'character', 'Discrete')
}

def decode_stata_type(code):
    if code in TYPE_MAP:
        return TYPE_MAP[code]
    elif 1 <= code <= 2045:
        return (f"str{code}", "character", "Discrete")
    else:
        return (f"type_{code}", "unknown", "Discrete")

def parse_dta_file(filepath):
    """
    Parses metadata from a Stata 118 .dta binary file without third-party dependencies.
    """
    file_size_bytes = os.path.getsize(filepath)
    file_size_mb = round(file_size_bytes / (1024 * 1024), 3)
    filename = os.path.basename(filepath)

    with open(filepath, 'rb') as f:
        data = f.read()

    if b'<stata_dta>' not in data:
        raise ValueError(f"File {filename} is not a valid Stata XML-wrapped format (.dta 117+)")

    # Byte order
    byteorder_str = data.split(b'<byteorder>')[1].split(b'</byteorder>')[0].decode('ascii')
    byteorder = '<' if byteorder_str == 'LSF' else '>'

    # Release
    release_str = data.split(b'<release>')[1].split(b'</release>')[0].decode('ascii')

    # K (vars) and N (observations)
    k_bytes = data.split(b'<K>')[1].split(b'</K>')[0]
    n_bytes = data.split(b'<N>')[1].split(b'</N>')[0]
    K = struct.unpack(f'{byteorder}H', k_bytes)[0]
    N = struct.unpack(f'{byteorder}Q', n_bytes)[0]

    # Types
    s_t = data.find(b'<variable_types>') + len(b'<variable_types>')
    type_codes = struct.unpack(f'{byteorder}{K}H', data[s_t : s_t + 2*K])

    # Varnames (129 bytes per variable)
    s_v = data.find(b'<varnames>') + len(b'<varnames>')
    varnames = [data[s_v + i*129 : s_v + (i+1)*129].split(b'\x00')[0].decode('utf-8', errors='replace').strip() for i in range(K)]

    # Formats (57 bytes per variable)
    s_f = data.find(b'<formats>') + len(b'<formats>')
    formats = [data[s_f + i*57 : s_f + (i+1)*57].split(b'\x00')[0].decode('utf-8', errors='replace').strip() for i in range(K)]

    # Value label names (129 bytes per variable)
    s_l = data.find(b'<value_label_names>') + len(b'<value_label_names>')
    val_lbl_names = [data[s_l + i*129 : s_l + (i+1)*129].split(b'\x00')[0].decode('utf-8', errors='replace').strip() for i in range(K)]

    # Variable labels (321 bytes per variable)
    s_vl = data.find(b'<variable_labels>') + len(b'<variable_labels>')
    var_labels = [data[s_vl + i*321 : s_vl + (i+1)*321].split(b'\x00')[0].decode('utf-8', errors='replace').strip() for i in range(K)]

    # Value label definitions table
    value_labels = {}
    vl_tag = b'<value_labels>'
    vl_start = data.find(vl_tag)
    if vl_start != -1:
        vl_end = data.find(b'</value_labels>', vl_start)
        cursor = vl_start + len(vl_tag)
        while cursor < vl_end:
            lbl_tag = b'<lbl>'
            next_lbl = data.find(lbl_tag, cursor, vl_end)
            if next_lbl == -1:
                break
            pos = next_lbl + 5
            unit_len = struct.unpack(f'{byteorder}I', data[pos:pos+4])[0]
            pos += 4
            labname = data[pos:pos+129].split(b'\x00')[0].decode('utf-8', errors='replace').strip()
            pos += 129 + 3  # 129 bytes + 3 byte padding alignment
            n_vals, txtlen = struct.unpack(f'{byteorder}II', data[pos:pos+8])
            pos += 8
            offsets = struct.unpack(f'{byteorder}{n_vals}I', data[pos:pos+4*n_vals])
            pos += 4 * n_vals
            vals = struct.unpack(f'{byteorder}{n_vals}i', data[pos:pos+4*n_vals])
            pos += 4 * n_vals
            txt_table = data[pos:pos+txtlen]
            pos += txtlen

            mapping = {}
            for v, off in zip(vals, offsets):
                lbl_str = txt_table[off:].split(b'\x00')[0].decode('utf-8', errors='replace').strip()
                mapping[v] = lbl_str
            value_labels[labname] = mapping
            end_lbl = data.find(b'</lbl>', pos, pos + 20)
            cursor = end_lbl + 6 if end_lbl != -1 else pos

    variables = []
    for idx in range(K):
        vname = varnames[idx]
        vlabel = var_labels[idx]
        fmt = formats[idx]
        lbl_name = val_lbl_names[idx]
        raw_type = type_codes[idx]
        stata_type, gen_type, disc_cont = decode_stata_type(raw_type)

        codes_dict = value_labels.get(lbl_name, {})
        if codes_dict:
            codes_str = "; ".join([f"{k} = {v}" for k, v in sorted(codes_dict.items(), key=lambda x: x[0])])
            disc_cont = "Discrete"
        else:
            codes_str = ""

        variables.append({
            "variable_index": idx + 1,
            "variable_name": vname,
            "variable_label": vlabel,
            "storage_type": stata_type,
            "data_type": gen_type,
            "discrete_continuous": disc_cont,
            "format": fmt,
            "value_label_name": lbl_name,
            "value_codes_and_labels": codes_str,
            "value_mapping": codes_dict
        })

    return {
        "filename": filename,
        "filepath": filepath,
        "file_size_mb": file_size_mb,
        "stata_release": release_str,
        "observations_n": N,
        "variables_k": K,
        "variables": variables,
        "value_labels": value_labels
    }

def scan_dataset(data_dir):
    """
    Scans all .dta files in data_dir and returns structured metadata.
    """
    files = sorted(glob.glob(os.path.join(data_dir, "*.dta")))
    if not files:
        # Search recursively if no direct files
        files = sorted(glob.glob(os.path.join(data_dir, "**", "*.dta"), recursive=True))

    results = []
    print(f"Scanning {len(files)} .dta files in: {data_dir}...")
    for fpath in files:
        try:
            meta = parse_dta_file(fpath)
            results.append(meta)
            print(f"  [OK] {meta['filename']} ({meta['variables_k']} vars, {meta['observations_n']:,} rows)")
        except Exception as e:
            print(f"  [ERROR] {os.path.basename(fpath)}: {e}")
    return results

def export_dictionary_csv(results, out_path):
    """
    Exports variable dictionary CSV adhering to standard microdata catalog format.
    """
    fieldnames = [
        "File Name",
        "Variable Index",
        "Variable Name",
        "Variable Label",
        "Storage Type",
        "Data Type",
        "Discrete/Continuous",
        "Format",
        "Value Label Name",
        "Value Codes & Labels",
        "Observations (N)"
    ]

    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for file_meta in results:
            fname = file_meta['filename']
            n_obs = file_meta['observations_n']
            for v in file_meta['variables']:
                writer.writerow({
                    "File Name": fname,
                    "Variable Index": v['variable_index'],
                    "Variable Name": v['variable_name'],
                    "Variable Label": v['variable_label'],
                    "Storage Type": v['storage_type'],
                    "Data Type": v['data_type'],
                    "Discrete/Continuous": v['discrete_continuous'],
                    "Format": v['format'],
                    "Value Label Name": v['value_label_name'],
                    "Value Codes & Labels": v['value_codes_and_labels'],
                    "Observations (N)": n_obs
                })
    print(f"Exported CSV dictionary: {out_path}")

def export_inventory_csv(results, out_path):
    """
    Exports summary inventory of all files.
    """
    fieldnames = [
        "file_number",
        "filename",
        "size_MB",
        "observations_N",
        "variables_K",
        "has_value_labels",
        "variable_list"
    ]
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i, meta in enumerate(results, 1):
            var_names = " | ".join([v['variable_name'] for v in meta['variables']])
            writer.writerow({
                "file_number": i,
                "filename": meta['filename'],
                "size_MB": meta['file_size_mb'],
                "observations_N": meta['observations_n'],
                "variables_K": meta['variables_k'],
                "has_value_labels": len(meta['value_labels']) > 0,
                "variable_list": var_names
            })
    print(f"Exported File Inventory CSV: {out_path}")

def export_dictionary_json(results, out_path):
    """
    Exports structured metadata JSON.
    """
    # Clean file paths for portability
    clean_results = []
    for m in results:
        entry = dict(m)
        entry['filepath'] = os.path.basename(m['filepath'])
        clean_results.append(entry)

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(clean_results, f, indent=2, ensure_ascii=False)
    print(f"Exported JSON dictionary: {out_path}")

def export_dictionary_markdown(results, out_path):
    """
    Exports a comprehensive Markdown data dictionary document.
    """
    total_files = len(results)
    total_vars = sum(m['variables_k'] for m in results)
    total_obs = sum(m['observations_n'] for m in results)

    lines = []
    lines.append("# NCSA 2019/2020 Small-Scale Farmers Data Dictionary\n")
    lines.append(f"**Generated automatically from Stata binary `.dta` metadata.**\n")
    lines.append(f"- **Total Tables / Files:** {total_files}")
    lines.append(f"- **Total Variables:** {total_vars}")
    lines.append(f"- **Cumulative Observations:** {total_obs:,}\n")

    lines.append("## Table of Contents\n")
    for i, meta in enumerate(results, 1):
        clean_anchor = meta['filename'].lower().replace('.', '').replace('_', '-')
        lines.append(f"{i}. [{meta['filename']}](#{clean_anchor}) ({meta['variables_k']} vars, {meta['observations_n']:,} rows)")
    lines.append("\n---\n")

    for i, meta in enumerate(results, 1):
        clean_anchor = meta['filename'].lower().replace('.', '').replace('_', '-')
        lines.append(f"## {i}. {meta['filename']}\n")
        lines.append(f"- **File size:** {meta['file_size_mb']} MB")
        lines.append(f"- **Observations ($N$):** {meta['observations_n']:,}")
        lines.append(f"- **Variables ($K$):** {meta['variables_k']}")
        lines.append(f"- **Stata Format:** Release {meta['stata_release']}\n")

        lines.append("| # | Variable | Label / Description | Type | Format | Value Labels / Codes |")
        lines.append("|---|---|---|---|---|---|")
        for v in meta['variables']:
            v_idx = v['variable_index']
            v_name = f"`{v['variable_name']}`"
            v_lbl = v['variable_label'].replace('|', '/') or "*none*"
            v_type = f"`{v['storage_type']}`"
            v_fmt = f"`{v['format']}`"
            v_codes = v['value_codes_and_labels'].replace('|', '/')
            if len(v_codes) > 80:
                v_codes = v_codes[:77] + "..."
            if not v_codes and v['value_label_name']:
                v_codes = f"[{v['value_label_name']}]"
            lines.append(f"| {v_idx} | {v_name} | {v_lbl} | {v_type} | {v_fmt} | {v_codes} |")
        lines.append("\n")

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    print(f"Exported Markdown dictionary: {out_path}")

def search_dictionary(results, query):
    """
    Search variables, descriptions, and labels across all files.
    """
    query_lower = query.lower()
    matches = []
    for m in results:
        for v in m['variables']:
            score = 0
            match_fields = []
            if query_lower in v['variable_name'].lower():
                match_fields.append("variable_name")
            if query_lower in v['variable_label'].lower():
                match_fields.append("variable_label")
            if query_lower in v['value_codes_and_labels'].lower():
                match_fields.append("value_codes")
            if query_lower in m['filename'].lower():
                match_fields.append("filename")

            if match_fields:
                matches.append({
                    "file": m['filename'],
                    "variable": v['variable_name'],
                    "label": v['variable_label'],
                    "type": v['storage_type'],
                    "codes": v['value_codes_and_labels'],
                    "matched_in": match_fields
                })

    print(f"\n=======================================================")
    print(f"Search Results for: '{query}' ({len(matches)} matches found)")
    print(f"=======================================================")
    for item in matches:
        print(f"File:     {item['file']}")
        print(f"Variable: {item['variable']} ({item['type']})")
        print(f"Label:    {item['label']}")
        if item['codes']:
            print(f"Codes:    {item['codes'][:120]}{'...' if len(item['codes']) > 120 else ''}")
        print(f"Matched:  {', '.join(item['matched_in'])}")
        print("-" * 55)

def main():
    parser = argparse.ArgumentParser(description="Scan NCSA 2019/2020 Stata dataset and create data dictionary.")
    parser.add_argument("--data-dir", default="data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI",
                        help="Path to folder containing .dta files")
    parser.add_argument("--output-dir", default="data/ncsa_2019_metadata",
                        help="Directory to save generated data dictionaries")
    parser.add_argument("--search", type=str, default=None,
                        help="Search query to filter variables, labels, or value codes")
    args = parser.parse_args()

    if not os.path.exists(args.data_dir):
        print(f"Error: Data directory does not exist: {args.data_dir}")
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)

    results = scan_dataset(args.data_dir)

    if not results:
        print("No .dta files found.")
        sys.exit(1)

    # Output paths
    csv_dict_path = os.path.join(args.output_dir, "data_dictionary_ncsa_2019.csv")
    inv_csv_path = os.path.join(args.output_dir, "ncsa_2019_file_inventory.csv")
    json_path = os.path.join(args.output_dir, "data_dictionary_ncsa_2019.json")
    md_path = os.path.join(args.output_dir, "data_dictionary_ncsa_2019.md")

    # Export all formats
    export_dictionary_csv(results, csv_dict_path)
    export_inventory_csv(results, inv_csv_path)
    export_dictionary_json(results, json_path)
    export_dictionary_markdown(results, md_path)

    print("\n[SUCCESS] All data dictionaries successfully generated in:", args.output_dir)

    if args.search:
        search_dictionary(results, args.search)

if __name__ == "__main__":
    main()
