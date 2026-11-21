# Tanzania Smallholder Farm Mechanization - Farm Mechanization Modeling and Simulation

This repository contains the data-processing and analysis code for a study of
smallholder farm mechanization in Tanzania. The Python pipeline harmonizes
agricultural survey data for maize, paddy, and legumes; estimates
inverse-probability-weighted regression adjustment (IPWRA) effects; simulates
uncertainty in yields, costs, and returns; and produces tables and figures.

## Repository layout

- `src/` — six ordered analysis scripts, from metadata inspection through
  figure generation.
- `data/` — survey files, metadata/codebooks, and Tanzania boundary data used
  by the scripts. The analysis expects the survey files in their existing
  subdirectories; the scripts use paths relative to the repository root.
- `outputs/data/` — intermediate Parquet datasets and simulation draws.
- `outputs/tables/` — CSV and Markdown result tables and diagnostics.
- `outputs/figures/` — generated figures in PNG, JPG, PDF, and TIFF formats.
- `paper_numbers.py` — collects analysis outputs into `paper_numbers.json`.
- `inspect_data.py` — standalone data-inspection utility.
- `requirements.txt` — pinned Python dependencies.

## How the analysis works

Run the numbered scripts in order:

1. `01_audit_metadata.py` inventories data and inspects survey metadata. It
   writes `outputs/schema_inspection_report.md` and
   `outputs/schema_mapping.json`. This is a diagnostic step.
2. `02_harmonize_panel.py` harmonizes survey observations and generates the
   analysis panel plus descriptive tables.
3. `03_ipwra_balance.py` estimates treatment probabilities, trims to common
   support, calibrates weights, checks covariate balance, and estimates
   treatment effects.
4. `04_stochastic_sim.py` runs the seeded, 2,000-draw stochastic simulation and
   writes validation, cost, and return tables.
5. `05_sensitivity_scenarios.py` evaluates cost/price shocks and plot-size
   strata.
6. `06_generate_figures.py` generates the paper figures from the data and
   tables created by earlier steps.

The scripts create their output directories as needed. Later steps depend on
intermediate files from earlier steps, so run them sequentially from the
repository root. Steps 2–6 form the main analysis pipeline; step 1 can be run
independently to inspect the available data.

## Setup and run

Use Python with the packages pinned in `requirements.txt`. From the
repository root, create and activate a virtual environment, install the
dependencies, and run the pipeline:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

python src/01_audit_metadata.py
python src/02_harmonize_panel.py
python src/03_ipwra_balance.py
python src/04_stochastic_sim.py
python src/05_sensitivity_scenarios.py
python src/06_generate_figures.py
python paper_numbers.py
```

`paper_numbers.py` is an optional final step; it reads the generated panels,
tables, and simulation draws and refreshes the root-level `paper_numbers.json`.

## Data and outputs

The analysis reads Stata `.dta` survey data, plus supporting metadata and
geospatial files under `data/`. The source files must be present at the paths
expected by the scripts. The pipeline does not download the data.

Intermediate panels are written as Parquet files under `outputs/data/`.
Tabular results are written under `outputs/tables/`, and figures under
`outputs/figures/`. The simulation uses a fixed seed (`2026`) for reproducible
draws. Re-run the scripts when source data or analysis code changes to refresh
dependent outputs.
