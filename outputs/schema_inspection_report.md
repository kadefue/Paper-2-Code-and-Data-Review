# Schema & Data Diagnostic Inspection Report
## Study 2: Risk-Adjusted Returns to Smallholder Farm Mechanization in Tanzania: A Causal-Stochastic Simulation of Hand-Hoe, Animal Traction, and Tractor Power Regimes

**Mode:** Read-Only Diagnostic Audit | **Script:** `src/01_audit_metadata.py`

### Executive Summary
- **Total Files Inventoried:** 517
- **Total Storage Footprint:** 869.15 MB
- **File Formats:** `.cpg`: 1, `.csv`: 5, `.dbf`: 1, `.dta`: 486, `.geojson`: 1, `.json`: 6, `.md`: 1, `.pdf`: 4, `.prj`: 1, `.py`: 1, `.sbn`: 1, `.sbx`: 1, `.shp`: 1, `.shx`: 1, `.txt`: 1, `.xlsx`: 2, `.xml`: 3
- **Survey Coverage (Active Waves in `data/`):**
  1. **NCSA 2019/20:** National Census of Agriculture (Small-Scale Farmers).
  2. **AASS 2022/23:** Annual Agricultural Sample Survey.
  3. **AASS 2023/24:** Annual Agricultural Sample Survey.
  4. **AASS 2024/25:** Annual Agricultural Sample Survey.
- **Live `.dta` Label Extraction (`pyreadstat`):** `OK`
- **DDI Codebooks Parsed:** NCSA_2019_20, AASS_2022_23, AASS_2023_24, AASS_2024_25

---

## 1. Cross-Wave Target Crop × Mechanization Regime ($M_0 - M_3$) Sample Sizes
Unweighted plot observation counts for Maize, Paddy, and Legumes across power regimes ($M_3 > M_2 > M_1 > M_0$):

| Survey Wave | Crop | Total $N$ | $M_0$ (Hand-Hoe) | $M_1$ (Animal Traction) | $M_2$ (2WT / Power Tiller) | $M_3$ (4WT Tractor) | Multi-Power Flagged | Notes |
|---|---|---|---|---|---|---|---|---|
| **NPS W1 08/09** | Maize | 1,999 | 1,469 | 457 | 0 | 73 | 25 |  |
| **NPS W1 08/09** | Paddy | 539 | 414 | 93 | 0 | 32 | 1 |  |
| **NPS W1 08/09** | Legumes | 1,438 | 1,085 | 316 | 0 | 37 | 15 |  |
| **NPS W2 10/11** | Maize | 2,368 | 1,758 | 388 | 0 | 222 | 146 |  |
| **NPS W2 10/11** | Paddy | 659 | 471 | 92 | 0 | 96 | 24 |  |
| **NPS W2 10/11** | Legumes | 1,449 | 1,071 | 247 | 0 | 131 | 88 |  |
| **NPS W3 12/13** | Maize | 3,079 | 2,021 | 590 | 10 | 458 | 302 |  |
| **NPS W3 12/13** | Paddy | 805 | 485 | 157 | 9 | 154 | 66 |  |
| **NPS W3 12/13** | Legumes | 2,069 | 1,455 | 332 | 10 | 272 | 194 |  |
| **NPS W4 14/15** | Maize | 2,088 | 1,081 | 596 | 8 | 403 | 294 |  |
| **NPS W4 14/15** | Paddy | 491 | 190 | 157 | 6 | 138 | 82 |  |
| **NPS W4 14/15** | Legumes | 1,523 | 787 | 420 | 1 | 315 | 235 |  |
| **NCSA 2019/20** | Maize | 28,171 | 0 | 0 | 0 | 0 | 0 | R081/R082 lack HHID; HH-level R122/R121 (N=30,650): M0=17,659, M1=8,478, M2=226, M3=4,287, multi=1,391 |
| **NCSA 2019/20** | Paddy | 8,416 | 0 | 0 | 0 | 0 | 0 | R081/R082 lack HHID; HH-level R122/R121 (N=30,650): M0=17,659, M1=8,478, M2=226, M3=4,287, multi=1,391 |
| **NCSA 2019/20** | Legumes | 18,850 | 0 | 0 | 0 | 0 | 0 | R081/R082 lack HHID; HH-level R122/R121 (N=30,650): M0=17,659, M1=8,478, M2=226, M3=4,287, multi=1,391 |
| **NPS W5 20/21** | Maize | 2,378 | 1,393 | 765 | 20 | 200 | 85 |  |
| **NPS W5 20/21** | Paddy | 685 | 286 | 324 | 20 | 55 | 21 |  |
| **NPS W5 20/21** | Legumes | 1,410 | 849 | 448 | 7 | 106 | 46 |  |
| **AASS 2022/23** | Maize | 17,936 | 12,290 | 1,740 | 0 | 3,906 | 645 |  |
| **AASS 2022/23** | Paddy | 3,730 | 2,637 | 478 | 0 | 615 | 71 |  |
| **AASS 2022/23** | Legumes | 11,354 | 7,981 | 1,014 | 0 | 2,359 | 389 |  |
| **AASS 2023/24** | Maize | 17,983 | 0 | 0 | 0 | 0 | 0 | Mechanization roster not on disk; total_n only |
| **AASS 2023/24** | Paddy | 4,223 | 0 | 0 | 0 | 0 | 0 | Mechanization roster not on disk; total_n only |
| **AASS 2023/24** | Legumes | 10,274 | 0 | 0 | 0 | 0 | 0 | Mechanization roster not on disk; total_n only |
| **AASS 2024/25** | Maize | 8,452 | 0 | 0 | 0 | 0 | 0 | Mechanization roster not on disk; total_n only |
| **AASS 2024/25** | Paddy | 2,024 | 0 | 0 | 0 | 0 | 0 | Mechanization roster not on disk; total_n only |
| **AASS 2024/25** | Legumes | 6,690 | 0 | 0 | 0 | 0 | 0 | Mechanization roster not on disk; total_n only |

---

## 2. Harmonized Variable Crosswalk Matrix ($M_0 - M_3$, Cost Buckets, IPWRA)
### A. Target Crop Groups (Maize, Paddy, Legumes)
| Crop Group | NCSA 2019/20 | AASS 2022/23 | AASS 2023/24 | AASS 2024/25 | NPS Waves 1–5 |
|---|---|---|---|---|---|
| **Maize** | `None` (`None`) | `None` (`None`) | `None` (`None`) | `None` (`None`) | `[11]` (`q811c4 / q821c4`) | `None` (`None`) | `[11]` (`crop_id`) | `[11]` (`crop_id`) | `[11]` (`MASIKACROP__id / VULICROP__id`) |
| **Paddy** | `None` (`None`) | `None` (`None`) | `None` (`None`) | `None` (`None`) | `[12]` (`q811c4 / q821c4`) | `None` (`None`) | `[12]` (`crop_id`) | `[12]` (`crop_id`) | `[12]` (`MASIKACROP__id / VULICROP__id`) |
| **Legumes** | `None` (`None`) | `None` (`None`) | `None` (`None`) | `None` (`None`) | `[31, 32, 33, 34, 35, 36, 37, 43, 47]` (`q811c4 / q821c4`) | `None` (`None`) | `[31, 32, 34, 35, 43, 9930]` (`crop_id`) | `[31, 32, 34, 35, 43, 9930]` (`crop_id`) | `[31, 32, 33, 34, 35, 36, 37, 43, 47]` (`MASIKACROP__id / VULICROP__id`) |

### B. Mechanization Power Regimes ($M_0 - M_3$)
| Regime | Definition | Hierarchy & Multi-Power Rule |
|---|---|---|
| **M0 Manual Hand Hoe** | Zero mechanical/animal draft power (baseline manual tillage). | Deterministic precedence: $M_3 > M_2 > M_1 > M_0$ |
| **M1 Animal Traction Ox Ploughing** | Oxen/donkey ploughing, ridging, or animal-drawn cultivation. | Deterministic precedence: $M_3 > M_2 > M_1 > M_0$ |
| **M2 Two Wheel Walking Tractor Power Tiller** | Single-axle two-wheel walking tractor / power tiller (owned or hired). | Deterministic precedence: $M_3 > M_2 > M_1 > M_0$ |
| **M3 Four Wheel Tractor** | Owned or custom-hired four-wheel tractor (disc plough, harrow, rotavator). | Deterministic precedence: $M_3 > M_2 > M_1 > M_0$ |

### C. Stochastic Cost Buckets ($\tilde{K}, \tilde{L}, \tilde{B}$) & IPWRA Covariates
| Construct | NCSA 2019/20 | AASS 2022/23 | AASS 2023/24 | AASS 2024/25 | NPS Waves 1–5 |
|---|---|---|---|---|---|
| **Mechanization Draft Power Cost K** | `Available in module` | `Available in module` | `Available in module` | `Available in module` | `q811c6 / q821c6 (Land prep cost TZS) + R121 q121c3 (Implement ownership) + R122 q122c4 (Area cultivated)` | `Available in module` | `s19q02 where items_service__id in [1 (Animal traction rental), 4 (Machinery rental), 5 (Machinery repair/maint), 14 (Fuel for machinery)]` | `s21q08 (Total rent cost of equipment) + s21q03/s21q04 (Owned equipment count & age for depreciation) + s20q08/s20q09` | `s20q08 / s20q09 (Agricultural structures/equipment) + machinery/fuel expenditure` |
| **Tillage Weeding Labor Cost L and Person Days** | `Available in module` | `Available in module` | `Available in module` | `Available in module` | `R081/R082 -> q811c6/q821c6 (Land prep), q811c7b/q821c7b (Planting), q811c8f/q821c8f (Weeding), q811c9f/q821c9f (Harvesting)` | `Available in module` | `items_services.dta -> items_service__id == 13 (Hired workers), items_service__id == 2 (Post-harvest labor)` | `s9q02__4 / s9q07 (Crop paid for labor); labor shortage flags s7q06__8, s7q10__8` | `s9q02__4 / s9q07 (Crop paid for labor); labor shortage flags s7q06__8` |
| **Biochemical Input Cost B** | `Available in module` | `Available in module` | `Available in module` | `Available in module` | `q821c15 (Seeds TZS) + q821c20 (Fertilizer TZS) + q821c25 (Herbicides TZS) + q821c30 (Fungicides TZS) + q821c35 (Insecticides TZS)` | `Available in module` | `s10q04 (Purchased seeds TZS) + s11q06a + s11q06b (Fertilizer & pesticide/herbicide values)` | `s11q06a + s11q06b (Fertilizer, herbicide, pesticide values) + seed quantity/price` | `s11q06a + s11q06b (Fertilizer, herbicide, pesticide values) + seed quantity/price` |
| **Household Head Age** | `Available in module` | `Available in module` | `Available in module` | `Available in module` | `q3_1c4 where q3_1c2 == 1 (Head)` | `Available in module` | `holding_head_age / s2q04 (where s2q02 == 1)` | `s2q04 (where s2q02 == 1)` | `s2q04 (where s2q02 == 1)` |
| **Household Head Sex** | `Available in module` | `Available in module` | `Available in module` | `Available in module` | `q3_1c3 where q3_1c2 == 1 (1=Male, 2=Female)` | `Available in module` | `holding_head_sex / s2q03` | `s2q03 (where s2q02 == 1)` | `s2q03 (where s2q02 == 1)` |
| **Household Head Education** | `Available in module` | `Available in module` | `Available in module` | `Available in module` | `q3_1c8 (Education level attained)` | `Available in module` | `s2q07 (Highest educational qualification)` | `s2q07 (Highest educational qualification)` | `s2q07 (Highest educational qualification)` |
| **Household Size** | `Available in module` | `Available in module` | `Available in module` | `Available in module` | `Count of member records per HHID in R031_HHRECORD.dta` | `Available in module` | `Count of member records per holding_id in household.dta` | `Count of member records per holding_id in HOUSEHOLD.dta` | `Count of member records per Holding_ID in HOUSEHOLD.dta` |
| **Total Farm Size** | `Available in module` | `Available in module` | `Available in module` | `Available in module` | `q4_1_8 / sum(q4_1_c2)` | `Available in module` | `sum(s3q04a_acres) per holding_id` | `sum(s3q04a_acres) per holding_id` | `sum(s3q04a_acres) per HHFARMID` |
| **Plot Size ha** | `Available in module` | `Available in module` | `Available in module` | `Available in module` | `q811c7a / q821c7a * 0.404686 (Individual plot planted area ha)` | `Available in module` | `s6q03_acres / s4q03_acres * 0.404686` | `s6q03_acres / s4q03_acres * 0.404686` | `s6q03_acres / s4q03_acres * 0.404686` |
| **Plot Slope Topography and Soil Type** | `Available in module` | `Available in module` | `Available in module` | `Available in module` | `q6_2c0 (Contour farming for sloped lands), q12_6_1 (Erosion)` | `Available in module` | `s3q06 (Soil type) / s6q07 (Soil amendments)` | `s3q06 (Soil type) / conservation practices` | `s3q06 (Dominant soil type on field)` |
| **Soil Quality Erosion** | `Available in module` | `Available in module` | `Available in module` | `Available in module` | `q12_6_1 (Erosion problem: 1=Yes, 2=No)` | `Available in module` | `s6q07 / s6q08 (Organic soil amendments)` | `Soil conservation practices` | `pme1q01 (Slash/burn clearing practices)` |
| **Household Asset Index and Draught Livestock** | `Available in module` | `Available in module` | `Available in module` | `Available in module` | `Asset ownership PCA + Cattle/Oxen herd count (q122c0 in [1..4])` | `Available in module` | `Asset & livestock holdings` | `Farm structures & asset holdings` | `Cattle/oxen/donkey stock counts` |
| **Credit Access** | `Available in module` | `Available in module` | `Available in module` | `Available in module` | `q13_1 (Received credit: 1=Yes, 2=No)` | `Available in module` | `s19q04a (Credit: 1=Yes, 0=No), s19q06a (Farming loan)` | `Household financial services access` | `pme5q04__1 (Formal credit), pme5q04__2 (Informal credit)` |
| **Extension Contact** | `Available in module` | `Available in module` | `Available in module` | `Available in module` | `q14_1 (Extension advice: 1=Yes, 2=No), R141_EXTENSION_MESSAGES` | `Available in module` | `s19q01b where items_service__id == 9 (Extension services)` | `Extension service interactions` | `pme6q13 (Visits received), pme6q14 (Visits made)` |
| **Distance to Market Roads** | `Available in module` | `Available in module` | `Available in module` | `Available in module` | `q310c2 (Distance in Km to Feeder road, Trunk road, Markets)` | `Available in module` | `Cluster accessibility metrics` | `Community infrastructure distances` | `Community infrastructure distances` |
| **Distance to AgroDealer Mechanization Hub** | `Available in module` | `Available in module` | `Available in module` | `Available in module` | `q310c2 (Distance to Agro-dealer / Input market), R124 distance/access` | `Available in module` | `Service access / EA cluster hub proxy` | `Community agro-dealer & service hub proximity` | `pme6q03__60 (Availability of inputs or equipment)` |

---

## 3. Live `.dta` Variable & Value Label Verification (`pyreadstat`)
### NPS W1 08/09 (Files inspected: 4)
- **crop_codes:** 16 matched variables
  - `SEC_3A.dta::s3aq5name` (S3AQ5name. Main crop cultivated on this plot in LongRainy08?: NAME): No value labels
  - `SEC_3A.dta::s3aq5code` (S3AQ5code. Main crop cultivated on this plot in LongRainy08?: CODE): 11=Maize, 12=Paddy, 13=Sorghum, 14=Bulrush Millet, 15=Finger Millet, 16=Wheat
  - `SEC_3A.dta::s3aq66` (S3AQ66. Main crop cultivated on this plot in ShortRainy07): 11=Maize, 12=Paddy, 13=Sorghum, 14=Bulrush Millet, 15=Finger Millet, 16=Wheat
  - `SEC_3A.dta::s3aq71` (S3AQ71. Main crop cultivated on this plot in ShortRainy08?): 11=Maize, 12=Paddy, 13=Sorghum, 14=Bulrush Millet, 15=Finger Millet, 16=Wheat
  - `SEC_4A.dta::zaocode` (CROP ID): 11=Maize, 12=Paddy, 13=Sorghum, 14=Bulrush Millet, 15=Finger Millet, 16=Wheat
  - `SEC_4A.dta::s4aq1` (S4AQ1. Did you harvest any [CROP] on this plot in LongRainy08?): 1=YES, 2=NO
  - `SEC_4A.dta::s4aq2` (S4AQ2. Why didn't you harvest any [CROP] on this plot?): 1=Not mine to harvest, 2=Still in plot, 3=Destruction, 4=Other
  - `SEC_4A.dta::s4aq3` (S4AQ3. Was crop planted in entire area of plot?): 1=YES, 2=NO
- **land_prep_tillage:** 0 matched variables
- **implement_ownership:** 1 matched variables
  - `SEC_11_ALL.dta::impcode` (Farm implements): 1=HAND HOE, 2=HAND-POWERED SPRAYER, 3=OX USED FOR ALL AGRICULTURAL PURPOSES, 4=OX PLOUGH, 5=OX SEED PLANTER, 6=OX CART
- **labor_activity:** 1 matched variables
  - `SEC_3A.dta::s3aq62` (S3AQ62. Did you hire any labor to work on this plot in LongRainy08?): 1=YES, 2=NO
### NPS W2 10/11 (Files inspected: 3)
- **crop_codes:** 16 matched variables
  - `AG_SEC3A.dta::ag3a_07_1` (Main crop on [PLOT] in the long rainy season 2010?): No value labels
  - `AG_SEC3A.dta::zaocode` (Crop code for main crop): 11=Maize, 12=Paddy, 13=Sorghum, 14=Bulrush Millet, 15=Finger Millet, 16=Wheat
  - `AG_SEC3A.dta::ag3a_75` (What was the main crop cultivated on [PLOT] in the short rainy season 2009?): 11=Maize, 12=Paddy, 13=Sorghum, 14=Bulrush Millet, 15=Finger Millet, 16=Wheat
  - `AG_SEC3A.dta::ag3a_80` (What was the main crop cultivated on [PLOT] in the short rainy season 2010?): 11=Maize, 12=Paddy, 13=Sorghum, 14=Bulrush Millet, 15=Finger Millet, 16=Wheat
  - `AG_SEC4A.dta::zaocode` (Crop Code): 11=Maize, 12=Paddy, 13=Sorghum, 14=Bulrush Millet, 15=Finger Millet, 16=Wheat
  - `AG_SEC4A.dta::ag4a_01` (Was crop planted in entire area of [PLOT}?): 1=YES, 2=NO
  - `AG_SEC4A.dta::ag4a_02` (Approximately, how much of the plot was planted with [CROP]?): 1=1/4, 2=1/2, 3=3/4
  - `AG_SEC4A.dta::ag4a_03` (Why didn't you plant the entire plot with [CROP]?): 1=Was Divided, 2=Drought, 3=Lack of tools/Equipments, 4=Lack Seeds, 5=Floods, 6=Loans
- **land_prep_tillage:** 0 matched variables
- **implement_ownership:** 0 matched variables
- **labor_activity:** 1 matched variables
  - `AG_SEC3A.dta::ag3a_71` (Did you hire any labor to work on [PLOT] in the long rainy season 2010?): 1=YES, 2=NO
### NPS W3 12/13 (Files inspected: 4)
- **crop_codes:** 20 matched variables
  - `AG_SEC_3A.dta::ag3a_07_1` (What was the main crop cultivated on this plot in the long rainy season 2012?): No value labels
  - `AG_SEC_3A.dta::ag3a_07_2` (What was the main crop cultivated on this plot in the long rainy season 2012?): 11=MAIZE, 12=PADDY, 13=SORGHUM, 14=BULRUSH MILLET, 15=FINGER MILLET, 16=WHEAT
  - `AG_SEC_3A.dta::ag3a_77` (What was the main crop cultivated on this plot in the short rainy season 2011?): 11=MAIZE, 12=PADDY, 13=SORGHUM, 14=BULRUSH MILLET, 15=FINGER MILLET, 16=WHEAT
  - `AG_SEC_3A.dta::ag3a_82` (What was the main crop cultivated on this plot in the short rainy season 2012?): 11=MAIZE, 12=PADDY, 13=SORGHUM, 14=BULRUSH MILLET, 15=FINGER MILLET, 16=WHEAT
  - `AG_SEC_4A.dta::zaocode` (CROP CODE): 11=MAIZE, 12=PADDY, 13=SORGHUM, 14=BULRUSH MILLET, 15=FINGER MILLET, 16=WHEAT
  - `AG_SEC_4A.dta::zaoname` (CROP NAME): No value labels
  - `AG_SEC_4A.dta::ag4a_01` (Was crop planted in entire area of plot?): 1=YES, 2=NO
  - `AG_SEC_4A.dta::ag4a_02` (Approximately, how much of the plot was planted with [CROP]?): 1=1/4, 2=1/2, 3=3/4
- **land_prep_tillage:** 0 matched variables
- **implement_ownership:** 0 matched variables
- **labor_activity:** 1 matched variables
  - `AG_SEC_3A.dta::ag3a_73` (Did you hire any labor to work on this plot in the long rainy seaon 2012?): 1=YES, 2=NO
### NPS W4 14/15 (Files inspected: 4)
- **crop_codes:** 19 matched variables
  - `ag_sec_3a.dta::ag3a_07_1` (What was the main crop cultivated on this plot in long rainy season 2014 (NAME)?): No value labels
  - `ag_sec_3a.dta::ag3a_07_2` (What was the main crop cultivated on this plot in long rainy season 2014 (CODE)?): 11=maize, 12=paddy, 13=sorghum, 14=BULRUSH MILLET, 15=FINGER MILLET, 16=wheat
  - `ag_sec_3a.dta::ag3a_77` (What was the main crop cultivated on this plot in the short rainy season 2013?): 11=maize, 12=paddy, 13=sorghum, 14=BULRUSH MILLET, 15=FINGER MILLET, 16=wheat
  - `ag_sec_3a.dta::ag3a_82` (What was the main crop cultivated on this plot in the short rainy season 2014?): 11=maize, 12=paddy, 13=sorghum, 14=BULRUSH MILLET, 15=FINGER MILLET, 16=wheat
  - `ag_sec_4a.dta::zaocode` (CROP CODE): 11=maize, 12=paddy, 13=sorghum, 14=BULRUSH MILLET, 15=FINGER MILLET, 16=wheat
  - `ag_sec_4a.dta::zaoname` (CROP NAME): No value labels
  - `ag_sec_4a.dta::ag4a_01` (Was crop planted in entire area of plot?): 1=yes, 2=no
  - `ag_sec_4a.dta::ag4a_02` (Approximately, how much of the plot was planted with [CROP]?): 1=1/4, 2=1/2, 3=3/4
- **land_prep_tillage:** 1 matched variables
  - `ag_sec_3a.dta::ag3a_71b` (Did you use any animal traction on this plot in the long rainy season 2014?): 1=yes, 2=no
- **implement_ownership:** 0 matched variables
- **labor_activity:** 1 matched variables
  - `ag_sec_3a.dta::ag3a_73` (Did you hire any labor to work on this plot in the long rainy season 2014?): 1=yes, 2=no
### NCSA 2019/20 (Files inspected: 14)
- **crop_codes:** 30 matched variables
  - `R000_SOV.dta::q8_1` (8.1 Did the Hh plant any crops 2019/20 during Short Rainy Season?): 1=Yes, 2=No
  - `R000_SOV.dta::q8_2` (8.2 Did the Hh plant any crop during 2019/20 Long Rainy Season?): 1=Yes, 2=No
  - `R000_SOV.dta::q8_3` (8.3 Does your Household have any Permanent / Perennial Crops of Fruit Tree?): 1=Yes, 2=No
  - `R000_SOV.dta::q9_1` (9.1 Did you use Secondary Products from any of your crops during the 2019/20 yea): 1=Yes, 2=No
  - `R000_SOV.dta::q10_1` (10.1 Did the household process any of the crops harvested on the farm during 201): 1=Yes, 2=No
  - `R000_SOV.dta::q11_1` (11.1 Do  you currently have any crops in storage ?): 1=Yes, 2=No
  - `R000_SOV.dta::q14_1` (14.1 Did your household receive any extension advice for crop production during): 1=Yes, 2=No
  - `R081_SHORT_RAINY_SEASON.dta::q811c4` (Crop Code): 11=Maize, 12=Paddy, 13=Sorghum, 14=Bulrush Millet, 15=Finger Millet, 16=Wheat
- **land_prep_tillage:** 6 matched variables
  - `R000_SOV.dta::q12_2` (12.2 Did you useTractors/Draft animals to cultivate?): 1=Yes, 2=No
  - `R000_SOV.dta::q23_2` (23.2 Did you deworm your animals during 2019/20?): 1=Yes, 2=No
  - `R122_USE_TRACTOR_ANIMALS.dta::q122c0` (SN): 1=Oxen, 2=Bulls, 3=Cows, 4=Donkeys, 5=Tractor, 6=Power Tiller
  - `R122_USE_TRACTOR_ANIMALS.dta::q122c2` (Number owned out of number used): No value labels
  - `R122_USE_TRACTOR_ANIMALS.dta::q122c3` (Number Used): No value labels
  - `R122_USE_TRACTOR_ANIMALS.dta::q122c4` (Area Cultivated (Acres)): No value labels
- **implement_ownership:** 6 matched variables
  - `R000_SOV.dta::q132_5_tools_source__a` (Tools/Equipments(a)): 1=Yes, 2=No
  - `R000_SOV.dta::q132_5_tools_source_b` (Tools/Equipments(b)): 1=Yes, 2=No
  - `R000_SOV.dta::q132_5_tools_source_c` (Tools/Equipments(c)): 1=Yes, 2=No
  - `R121_FARM_IMPLEMENTS.dta::q121c0` (Equipment SN): 1=Panga, 2=Hand Hoe, 3=Hand Sprayer, 4=Oxen, 5=Ox Plough, 6=Ox Seed Planter
  - `R121_FARM_IMPLEMENTS.dta::q121c2` (Used): 1=Yes, 2=No
  - `R121_FARM_IMPLEMENTS.dta::q121c3` (Number owned): No value labels
- **labor_activity:** 6 matched variables
  - `R000_SOV.dta::q132_1_labour_source_a` (Labour (a)): 1=Yes, 2=No
  - `R000_SOV.dta::q132_1_labour_source_b` (Labour (b)): 1=Yes, 2=No
  - `R000_SOV.dta::q132_1_labour_source_c` (Labour (c)): 1=Yes, 2=No
  - `R291_LABOUR_USE.dta::q2911c0` (Activity SN): 1=Land Clearing, 2=Land tilling (by hand), 3=Land tilling (oxen/tractor), 4=Planting, 5=Weeding, 6=Crop Protection
  - `R291_LABOUR_USE.dta::q2911c2` (Is your household  involved in  [..]?): 1=Yes, 2=No
  - `R291_LABOUR_USE.dta::q2911c3` (Main responsible person(s)): 1=Hosehold head alone, 2=Adult Males, 3=Adult Females, 4=Adults, 5=Boys, 6=Girls
### NPS W5 20/21 (Files inspected: 3)
- **crop_codes:** 17 matched variables
  - `AG_SEC_3A.dta::ag3a_07` (What was the main crop cultivated on [PLOT] in the long rainy season 2020?): 11=MAIZE, 12=PADDY, 13=SORGHUM, 14=BULRUSH MILLET, 15=FINGER MILLET, 16=WHEAT
  - `AG_SEC_3A.dta::ag3a_77` (What was the main crop cultivated on [PLOT] in the short rainy season 2019?): 11=MAIZE, 12=PADDY, 13=SORGHUM, 14=BULRUSH MILLET, 15=FINGER MILLET, 16=WHEAT
  - `AG_SEC_3A.dta::ag3a_82` (What was the main crop cultivated on [PLOT] in the short rainy season 2020?): 11=MAIZE, 12=PADDY, 13=SORGHUM, 14=BULRUSH MILLET, 15=FINGER MILLET, 16=WHEAT
  - `AG_SEC_4A.dta::cropid` (CROP CODE): 11=MAIZE, 12=PADDY, 13=SORGHUM, 14=BULRUSH MILLET, 15=FINGER MILLET, 16=WHEAT
  - `AG_SEC_4A.dta::ag4a_01` (Was crop planted in entire area of plot?): 1=YES, 2=NO
  - `AG_SEC_4A.dta::ag4a_02` (Approximately, how much of the plot was planted with [CROP]?): 1=1/4, 2=1/2, 3=3/4
  - `AG_SEC_4A.dta::ag4a_03` (Why didn't you plant the entire plot with [CROP]?): 1=WAS DIVIDED, 2=DROUGHT, 3=LACK OF TOOLS/EQUIPMENTS, 4=LACK SEEDS, 5=FLOODS, 6=LOANS
  - `AG_SEC_4A.dta::ag4a_04` (Was cultivation intercropped?): 1=YES, 2=NO
- **land_prep_tillage:** 1 matched variables
  - `AG_SEC_3A.dta::ag3a_71b` (Did you use any animal traction on [PLOT] in the long rainy season 2020?): 1=YES, 2=NO
- **implement_ownership:** 0 matched variables
- **labor_activity:** 1 matched variables
  - `AG_SEC_3A.dta::ag3a_73` (Did you hire any labor to work on [PLOT] in the long rainy season 2020?): 1=YES, 2=NO
### AASS 2022/23 (Files inspected: 12)
- **crop_codes:** 56 matched variables
  - `AASS2023.dta::s3q06` (Total amount earned from renting/sharecropping land during ag year (TZS)): 1=[ 0 - 50 000 ), 2=[ 50 000 - 100 000 ), 3=[ 100 000 - 250 000 ), 4=[ 250 000 - 500 000 ), 5=[ 500 000 - 750 000 ), 6=[ 750 000 - 1 000 000 )
  - `household.dta::s18q04__1` (Did household member worked on crop production?): 0=No, 1=Yes
  - `household.dta::s18q05a` (Number of months household member worked on crop activities): No value labels
  - `household.dta::s18q05b` (Days per month household member worked on crops): No value labels
  - `household.dta::s18q05c` (Hours per day household member worked on crops, on average): No value labels
  - `masikaplot.dta::s6q08__3` (Organic fertilizers in past masika/dry?_Green manure (crop residues)): 0=No, 1=Yes
  - `vuliplot.dta::s4q08__3` (Organic fertilizers in past vuli? Green manure (crop residues)): 0=No, 1=Yes
  - `masikacrop.dta::TEMP_PERM` (Is this crop a temporary or permanent?): 1=Temporary, 2=Permanent
- **land_prep_tillage:** 66 matched variables
  - `AASS2023.dta::s19q07__5` (Three main reason for loans? Purchase animals): 0=No, 1=Yes
  - `AASS2023.dta::s19q07__6` (Three main reason for loans?  Purchase animal input): 0=No, 1=Yes
  - `masikaplot.dta::s6q02` (During the past 2022/2023 masika & dry seasons, how was this plot used?): 1=A kitchen garden/backyard, 2=Cultivated with crops, 3=Temporarily left fallow
  - `masikaplot.dta::s6q03_acres` (Plot area (acres)): No value labels
  - `masikaplot.dta::s6q04` (Pure stand or mixed): 1=Pure stand, 2=Mixed/intercropped
  - `masikaplot.dta::s6q05a` (Any irrigation structures on this plot in the 22/23 masika/dry season?): 0=No, 1=Yes
  - `masikaplot.dta::s6q05b` (Percentage of this plot was irrigated in past 2022/23 masika/dry season?): No value labels
  - `masikaplot.dta::s6q06` (Main irrigation method on this plot in past 2022/23 masika/dry season): 1=Irrigation by using watering cans or buckets, 2=Sprinkler irrigation, 3=Drip irrigation, 4=Flooding/SURFACE irrigation, 99=Other
- **implement_ownership:** 4 matched variables
  - `AASS2023.dta::s19q07__3` (Three main reason for loans? Buy/repair farm equipment, etc): 0=No, 1=Yes
  - `AASS2023.dta::s20q01` (Is the farm recorded in an official register?): 0=No, 1=Yes
  - `AASS2023.dta::s20q02a` (Type of Register): 1=Registration of Business name, 2=Registration of Company limited by Shares
  - `items_services.dta::items_service__id` (Item or service): 0=None of the above, 1=Animal traction rental (rent-in), 2=Post-harvest labor, 3=Transport related to agricultural activities, 4=Rental of machinery, equipment and vehicles, 5=Repair and maintenance of machinery, equipment, vehicles
- **labor_activity:** 26 matched variables
  - `AASS2023.dta::s19q07__1` (Three main reason for loans? Pay for laborers): 0=No, 1=Yes
  - `household.dta::s18q04__1` (Did household member worked on crop production?): 0=No, 1=Yes
  - `household.dta::s18q04__2` (Did household member work on livestock?): 0=No, 1=Yes
  - `household.dta::s18q04__3` (Did household member work on aquaculture?): 0=No, 1=Yes
  - `household.dta::s18q05a` (Number of months household member worked on crop activities): No value labels
  - `household.dta::s18q05b` (Days per month household member worked on crops): No value labels
  - `household.dta::s18q05c` (Hours per day household member worked on crops, on average): No value labels
  - `household.dta::s18q05d` (Number of months household member worked on livestock): No value labels
### AASS 2023/24 (Files inspected: 11)
- **crop_codes:** 72 matched variables
  - `MASIKAPLOT.dta::s6q08__3` (Apply organic fertilizer during Masika/Dry season: GREEN MANURE (CROP RESIDUES)): 0=No, 1=Yes
  - `MASIKAPLOT.dta::s6q10__118` (Inorganic fertilizer applied on plot: MACROP): 0=No, 1=Yes
  - `VULIPLOT.dta::s4q08__3` (Apply organic fertilizer during Vuli season: GREEN MANURE (CROP RESIDUES)): 0=No, 1=Yes
  - `VULIPLOT.dta::s4q10__118` (Inorganic fertilizer applied on plot: MACROP): No value labels
  - `MASIKACROP.dta::crop_id` (Masika crop ID): 11=Maize, 12=Paddy, 13=Sorghum, 14=Bulrush Millet, 15=Finger Millet, 18=Black Pepper
  - `MASIKACROP.dta::TEMP_PERM` (Crop type): 1=Temporary, 2=Permanent
  - `MASIKACROP.dta::s7q02a` ([CROP] under a greenhouse/high shelter during Masika/Dry?): 0=No, 1=Yes
  - `MASIKACROP.dta::s7q04__1` (Type of [CROP] seeds used during Masika/Dry: Improved): 0=No, 1=Yes
- **land_prep_tillage:** 87 matched variables
  - `MASIKAPLOT.dta::s6q02` (During the past 23/24 Masika and Dry season, how was this [PLOT] used?): 1=A KITCHEN GARDEN/BACKYARD, 2=CULTIVATED WITH CROPS, 3=TEMPORARILY LEFT FALLOW
  - `MASIKAPLOT.dta::s6q03_hectares` (Masika plot area (hectares)): No value labels
  - `MASIKAPLOT.dta::s6q04` (Was this [PLOT] in pure stand or mixed during 2023/24 Masika/Dry season?): 1=PURE STAND, 2=MIXED, 3=INTERCROPPED
  - `MASIKAPLOT.dta::s6q05a` (Any irrigation infrastructure on [PLOT] during 2023/24 Masika/Dry season?): 0=No, 1=Yes
  - `MASIKAPLOT.dta::s6q05b` (What percentage of [PLOT] was irrigated during 2023/24 Masika/Dry season?): 0=zero - 0%, 25=One quarter - 25%, 50=Half - 50%, 75=Three-quarters - 75%, 100=All - 100%
  - `MASIKAPLOT.dta::s6q06` (Main method of irrigation on this [PLOT] during 2023/24 Masika/Dry season): 1=MANUAL IRRIGATION, 2=SPRINKLER IRRIGATION, 3=DRIP IRRIGATION, 4=FLOODING/SURFACE/FURROW, 5=PIVOT IRRIGATION, 6=TERRACED IRRIGATION
  - `MASIKAPLOT.dta::s6q07` (Did you apply any organic fertilizer on [PLOT] during 2023/24 Masika/Dry season?): 0=No, 1=Yes
  - `MASIKAPLOT.dta::s6q08__1` (Apply organic fertilizer during Masika/Dry season: SOLID MANURE/FARM YARD MANURE): 0=No, 1=Yes
- **implement_ownership:** 64 matched variables
  - `AASS2024f.dta::s20q08` (Did you own any other building or structures for agricultural activities): 0=No, 1=Yes
  - `AASS2024f.dta::s20q09` (How many were they?): No value labels
  - `buildings_roster.dta::s20q01` (Did your household/farm use any building or structure during the past 2023/24?): 0=No, 1=Yes
  - `buildings_roster.dta::s20q01a__1` (Building/structure used for Ag. year 23/24: TRADITIONAL GRAIN SILOS): 0=No, 1=Yes
  - `buildings_roster.dta::s20q01a__2` (Building/structure used for Ag. year 23/24: WAREHOUSE): 0=No, 1=Yes
  - `buildings_roster.dta::s20q01a__3` (Building/structure used for Ag. year 23/24: STORE): 0=No, 1=Yes
  - `buildings_roster.dta::s20q01a__4` (Building/structure used for Ag. year 23/24: COLD STORAGE ROOMS): 0=No, 1=Yes
  - `buildings_roster.dta::s20q01a__5` (Building/structure used for Ag. year 23/24: GREENHOUSES): 0=No, 1=Yes
- **labor_activity:** 6 matched variables
  - `MASIKACROP.dta::s7q06__8` (Reason for not harvesting: NO AVAILABLE LABOUR): 0=No, 1=Yes
  - `MASIKACROP.dta::s7q10__8` (Reason for not harvesting all the area planted: NO AVAILABLE LABOR): 0=No, 1=Yes
  - `VULICROP.dta::s5q06__8` (Reason for not harvesting: NO AVAILABLE LABOUR): 0=No, 1=Yes
  - `VULICROP.dta::s5q10__8` (Reason for not harvesting all the area planted: NO AVAILABLE LABOR): 0=No, 1=Yes
  - `CROP_USE.dta::s9q02__4` (HH/farm use or intended to use [CROP] for: PAYING FOR LAND, LABOUR OR INPUTS): 0=No, 1=Yes
  - `CROP_USE.dta::s9q07` (% of [CROP] harvested in the 23/24 Ag. year used/to be to pay land/labour/inputs): 25=One quarter - 25%, 50=Half - 50%, 75=Three-quarters - 75%, 100=All - 100%
### AASS 2024/25 (Files inspected: 12)
- **crop_codes:** 109 matched variables
  - `AASS2025.dta::s1q06` (Did your HH engage in own-account crop cultivation during 24/25 Ag Year?): 1=No, 2=Yes
  - `AASS2025.dta::pme2q07` (pme2q07-In general, when do you  apply pesticides on your crops/plots?): 1=AS SOON AS THE PEST APPEARS, 2=WHEN THE CROP REACHES A SPECIFIC GROWING STAGE, 3=WHEN THE PESTICIDE IS AVAILABLE, 4=SOON AFTER PLANTING, 5=OTHER (SPECIFY)
  - `AASS2025.dta::pme2q08` (pme2q08-In general, at what time of the day do you apply pesticides on your crop): 1=EARLY MORNING, BEFORE SUN GETS HOT, 2=EVENING (AFTER 4PM), 3=OTHER TIMES OF THE DAY, 4=IMMEDIATELY AFTER PLANTING
  - `FIELD.dta::s3q13` (s3q13 - How frequently has crop rotation been practiced on this  [FIELD] in the): 1=EVERY SEASON, 2=EVERY AGRICULTURAL YEAR, 3=EVERY OTHER YEAR, 4=EVERY THREE YEARS
  - `FIELD.dta::s3q14` (s3q14 - Were leguminous crops involved in the last rotation cycle practiced on t): 0=No, 1=Yes
  - `MASIKAPLOT.dta::s6q08__3` (Apply organic fertilizer during Masika/Dry season: GREEN MANURE (CROP RESIDUES)): 0=No, 1=Yes
  - `MASIKAPLOT.dta::s6q10__118` (Inorganic fertilizer applied on plot: MACROP): 0=No, 1=Yes
  - `MASIKAPLOT.dta::s7q01__0` (List all temporary/permanent crops planted in 24/25 Masika/Dry season: Crop 1): 11=Maize, 12=Paddy, 13=Sorghum, 14=Bulrush Millet, 15=Finger Millet, 16=Wheat
- **land_prep_tillage:** 122 matched variables
  - `MASIKAPLOT.dta::s6q02` (During the past 24/25 Masika and Dry season, how was this [PLOT] used?): 1=A KITCHEN GARDEN/BACKYARD, 2=CULTIVATED WITH CROPS, 3=TEMPORARILY LEFT FALLOW
  - `MASIKAPLOT.dta::s6q03` (What was the area of this [PLOT]?): No value labels
  - `MASIKAPLOT.dta::s6q03_unit` (Unit of measurement): 1=Hectare, 2=Acres, 3=Square Meters
  - `MASIKAPLOT.dta::s6q03_Hectares` (What was the area of this [PLOT] in Hectares ? (imputed with regression-fitted v): No value labels
  - `MASIKAPLOT.dta::s6q04` (Was this [PLOT] in pure stand or mixed during 2024/25 Masika/Dry season?): 1=PURE STAND, 2=MIXED, 3=INTERCROPPED
  - `MASIKAPLOT.dta::s6q05a` (Any irrigation infrastructure on [PLOT] during 2024/25 Masika/Dry season?): 0=No, 1=Yes
  - `MASIKAPLOT.dta::s6q05b` (What percentage of [PLOT] was irrigated during 2024/25 Masika/Dry season?): 0=zero - 0%, 25=One quarter - 25%, 50=Half - 50%, 75=Three-quarters - 75%, 100=All - 100%
  - `MASIKAPLOT.dta::s6q06` (Main method of irrigating plants on [PLOT] during 24/25 Masika/Dry season): 1=MANUAL IRRIGATION, 2=SPRINKLER IRRIGATION, 3=DRIP IRRIGATION, 4=FLOODING/SURFACE/FURROW, 5=PIVOT IRRIGATION, 6=TERRACED IRRIGATION
- **implement_ownership:** 1 matched variables
  - `AASS2025.dta::pme4q08` (pme4q08 - What was the main solution implemented to provide water to livestock): 1=USE ANOTHER SOURCE NEAR HOLDING, FOR FREE (NEIGHBORS, ETC.), 2=USE ANOTHER SOURCE NEAR HOLDING, WITH PAYMENT (CASH OR KIND), 3=USE ANOTHER SOURCE FAR FROM HOLDING, FOR FREE, 4=USE ANOTHER SOURCE FAR FROM HOLDING, WITH PAYMENT (CASH OR KIND), 5=NOTHING (LIVESTOCK DRANK POORER OR LESS(WATER), 6=OTHER (SPECIFY)
- **labor_activity:** 6 matched variables
  - `AASS2025.dta::s1q09` (Did your HH engage in own-account aquaculture activity from Oct-24 to Sep-25?): 1=No, 2=Yes
  - `MASIKACROP.dta::s7q06__8` (Reason for not harvesting: NO AVAILABLE LABOUR): 1=No, 2=Yes
  - `MASIKACROP.dta::s7q10__8` (Reason for not harvesting all the area planted: NO AVAILABLE LABOR): 1=No, 2=Yes
  - `VULICROP.dta::s5q06__8` (Reason for not harvesting: NO AVAILABLE LABOUR): 0=No, 1=Yes
  - `CROP_USE.dta::s9q02__4` (HH/farm use or intended to use [CROP] for: PAYING FOR LAND, LABOUR OR INPUTS): No value labels
  - `CROP_USE.dta::s9q07` (% of [CROP] harvested in the 24/25 Ag. year used/to be to pay land/labour/inputs): 1=1, 2=2, 3=3, 4=4, 5=5, 6=6

---

## 4. Spatial Alignment & Agroecological Zones (AEZs)
| Zone ID | Agroecological Zone (AEZ) | Region Codes (NBS Standard) | Regions Included |
|---|---|---|---|
| **AEZ 1** | Central Semi Arid | `1, 13` | Dodoma, Singida |
| **AEZ 2** | Northern Highlands | `2, 3, 21` | Arusha, Kilimanjaro, Manyara |
| **AEZ 3** | Southern Highlands | `10, 11, 12, 15, 22, 23, 26` | Iringa, Mbeya, Njombe, Ruvuma, Songwe, Rukwa, Katavi |
| **AEZ 4** | Lake Victoria Basin | `17, 18, 19, 20, 24, 25` | Mwanza, Geita, Simiyu, Kagera, Mara, Shinyanga |
| **AEZ 5** | Western Miombo | `14, 16` | Tabora, Kigoma |
| **AEZ 6** | Eastern Coastal Lowlands | `5, 6, 7` | Morogoro, Pwani, Dar es Salaam |
| **AEZ 7** | Southern Coastal Lowlands | `8, 9` | Lindi, Mtwara |
| **AEZ 8** | Northern Coastal Lowlands | `4` | Tanga |
| **AEZ 9** | Zanzibar Archipelago | `51, 52, 53, 54, 55` | Kaskazini Unguja, Kusini Unguja, Mjini Magharibi, Kaskazini Pemba, Kusini Pemba |

---

## 4b. DDI Codebook Verification Summary
### NCSA 2019/20 (`data_dictionary_ncsa_2019.json` — 39 matched variables)
- `R000_SOV.dta::q11_1`: 11.1 Do  you currently have any crops in storage ? — `1 = Yes; 2 = No`
- `R000_SOV.dta::q12_2`: 12.2 Did you useTractors/Draft animals to cultivate? — `1 = Yes; 2 = No`
- `R000_SOV.dta::q23_2`: 23.2 Did you deworm your animals during 2019/20? — `1 = Yes; 2 = No`
- `R000_SOV.dta::q132_1_labour_source_a`: Labour (a) — `1 = Yes; 2 = No`
- `R000_SOV.dta::q132_5_tools_source__a`: Tools/Equipments(a) — `1 = Yes; 2 = No`
- `R000_SOV.dta::q132_1_labour_source_b`: Labour (b) — `1 = Yes; 2 = No`
- `R000_SOV.dta::q132_5_tools_source_b`: Tools/Equipments(b) — `1 = Yes; 2 = No`
- `R000_SOV.dta::q132_1_labour_source_c`: Labour (c) — `1 = Yes; 2 = No`
- `R000_SOV.dta::q132_5_tools_source_c`: Tools/Equipments(c) — `1 = Yes; 2 = No`
- `R041_LAND_OWNERSHIP.dta::q4_1_c0`: 4.1 Land Access SN — `1 = Land Leased/Certificate of ownership; 2 = Land owned under Customary Law; 3 = Land Bought from others; 4 = Land Rented from others; 5 = Land Borrowed from o`
- `R051_LAND_USE.dta::q5_1_c0`: 5.1 Land Use S/N — `1 = Area under Temporary Mono Crops; 2 = Area under Temporary Mixed Crops; 3 = Area under Permanent Mono Crops; 4 = Area under Permanent Mixed Crops; 5 = Area u`
- `R081_SHORT_RAINY_SEASON.dta::q811c4`: Crop Code — `11 = Maize; 12 = Paddy; 13 = Sorghum; 14 = Bulrush Millet; 15 = Finger Millet; 16 = Wheat; 17 = Barley; 18 = Black Pepper; 19 = Seaweed; 21 = Cassava; 22 = Swee`
### AASS 2022/23 (`data_dictionary_catalog_52.json` — 27 matched variables)
- `crop_use::crop_id`:  — `11 = Maize; 12 = Paddy; 13 = Sorghum; 14 = Bulrush Millet; 15 = Finger Millet; 18 = Black Pepper; 21 = Cassava; 22 = Sweet potatoes; 23 = Irish potatoes; 25 = C`
- `external_labor_activities::holding_id`: 
- `external_labor_activities::Weight`: 
- `external_labor_activities::holding_type`:  — `1 = Large farm; 2 = Household`
- `external_labor_activities::region`:  — `1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; 7 = Dar es Salaam; 8 = Lindi; 9 = Mtwara; 10 = Ruvuma; 11 = Iringa; 12 = Mbeya; 13 `
- `external_labor_activities::External_labor__id`:  — `1 = Free workers; 2 = Exchange workers; 3 = Hired workers; Sysmiss = `
- `external_labor_activities::External_labor_activities__id`:  — `1 = Crop; 2 = Livestock; 3 = Aquaculture; Sysmiss = `
- `external_labor_activities::s18q06b`:  — `0 = No; 1 = Yes; Sysmiss = `
- `external_labor_activities::s18q07`:  — `Sysmiss = `
- `external_labor_activities::s18q08`:  — `Sysmiss = `
- `external_labor_activities::s18q09`:  — `Sysmiss = `
- `external_labor_activities::s18q10`:  — `Sysmiss = `
### AASS 2023/24 (`TZA_AASS_2023-2024_v01.json` — 41 matched variables)
- `CROP_USE::crop_id`: Crop ID — `11=Maize; 12=Paddy; 13=Sorghum; 14=Bulrush Millet; 15=Finger Millet; 18=Black Pepper; 21=Cassava; 22=Sweet potatoes; 23=Irish potatoes; 25=Cocoyams; 31=Beans; 3`
- `CROP_USE::s9q02__4`: HH/farm use or intended to use [CROP] for: PAYING FOR LAND, LABOUR OR INPUTS — `0=No; 1=Yes`
- `CROP_USE::s9q02__5`: HH/farm use or intended to use [CROP] for: ANIMAL FEED — `0=No; 1=Yes`
- `CROP_USE::s9q07`: % of [CROP] harvested in the 23/24 Ag. year used/to be to pay land/labour/inputs
- `CROP_USE::s9q08`: % of [CROP] harvested in the 23/24 Ag. year used/to be used for animal feed
- `FIELD::s3q03`: What type of tenure rights do the farm have on this field? — `89=Customary right of occupancy; 90=Granted right of occupancy; 92=Purchased; 93=Rented or leased in; 94=Borrowed for free; 95=Inherited; 98=Other; Sysmiss=None`
- `MASIKACROP::crop_id`: Masika crop ID — `11=Maize; 12=Paddy; 13=Sorghum; 14=Bulrush Millet; 15=Finger Millet; 18=Black Pepper; 21=Cassava; 22=Sweet potatoes; 23=Irish potatoes; 25=Cocoyams; 31=Beans; 3`
- `MASIKACROP::s7q06__8`: Reason for not harvesting: NO AVAILABLE LABOUR — `0=No; 1=Yes; Sysmiss=None`
- `MASIKACROP::s7q06__10`: Reason for not harvesting: ANIMAL/BIRDS DAMAGE — `0=No; 1=Yes; Sysmiss=None`
- `MASIKACROP::s7q10__8`: Reason for not harvesting all the area planted: NO AVAILABLE LABOR — `0=No; 1=Yes; Sysmiss=None`
- `MASIKACROP::s7q10__10`: Reason for not harvesting all the area planted: ANIMAL/BIRDS DAMAGE — `0=No; 1=Yes; Sysmiss=None`
- `permanent_crop::crop_id`: Permanent crop ID — `11=Maize; 12=Paddy; 13=Sorghum; 14=Bulrush Millet; 15=Finger Millet; 18=Black Pepper; 21=Cassava; 22=Sweet potatoes; 23=Irish potatoes; 25=Cocoyams; 26=Onion; 2`
### AASS 2024/25 (`TZA-NBS.OCGS-AASS-2025-v01.json` — 59 matched variables)
- `AASS2025::pme4q08`: pme4q08 - What was the main solution implemented to provide water to livestock — `1=USE ANOTHER SOURCE NEAR HOLDING, FOR FREE (NEIGHBORS, ETC.); 2=USE ANOTHER SOURCE NEAR HOLDING, WITH PAYMENT (CASH OR KIND); 3=USE ANOTHER SOURCE FAR FROM HOL`
- `CROP_USE::s9q02__4`: HH/farm use or intended to use [CROP] for: PAYING FOR LAND, LABOUR OR INPUTS — `0=None; 1=None`
- `CROP_USE::s9q02__5`: HH/farm use or intended to use [CROP] for: ANIMAL FEED — `0=None; 1=None`
- `CROP_USE::s9q07`: % of [CROP] harvested in the 24/25 Ag. year used/to be to pay land/labour/inputs — `1=1; 2=2; 3=3; 4=4; 5=5; 6=6; 7=7; 8=8; 9=9; 10=10; 11=11; 12=12; 13=13; 14=14; 15=15; 16=16; 17=17; 18=18; 19=19; 20=20`
- `CROP_USE::s9q08`: % of [CROP] harvested in the 24/25 Ag. year used/to be used for animal feed — `1=1; 2=2; 3=3; 4=4; 5=5; 6=6; 7=7; 8=9; 9=10; 10=11; 11=12; 12=13; 13=15; 14=17; 15=20; 16=One quarter - 25%; 17=29; 18=31; 19=33.3333358764648; 20=34`
- `FIELD::s3q03`: s3q03 - [FIELD] tenure type? — `1=CUSTOMARY RIGHT OF OCCUPANCY; 2=GRANTED RIGHT OF OCCUPANCY; 3=PURCHASED; 4=RENTED/LEASED IN; 5=SHARECROPPED IN; 6=BORROWED FOR FREE; 7=MOVED IN WITHOUT PERMIS`
- `livestock_type::s12q03`: How many [ANIMAL] were born ? — `1=NONE; 2=1; 3=2; 4=3; 5=4; 6=5; 7=6; 8=7; 9=8; 10=9; 11=10; 12=11; 13=12; 14=13; 15=14; 16=15; 17=16; 18=17; 19=18; 20=19`
- `livestock_type::s12q04`: How many [ANIMAL] did this holding buy alive ? — `1=NONE; 2=1; 3=2; 4=3; 5=4; 6=5; 7=6; 8=7; 9=8; 10=9; 11=10; 12=11; 13=12; 14=13; 15=14; 16=15; 17=16; 18=17; 19=18; 20=19`
- `livestock_type::s12q05`: What was the average unit price of the [ANIMAL] purchased ?
- `livestock_type::s12q06`: How many [ANIMAL] were received for free or as gift/dowry ? — `1=NONE; 2=1; 3=2; 4=3; 5=4; 6=5; 7=6; 8=7; 9=8; 10=9; 11=10; 12=11; 13=12; 14=13; 15=14; 16=15; 17=16; 18=17; 19=18; 20=19`
- `livestock_type::s12q07`: How many [ANIMAL] has this farm sold alive ? — `1=NONE; 2=1; 3=2; 4=3; 5=4; 6=5; 7=6; 8=7; 9=8; 10=9; 11=10; 12=11; 13=12; 14=13; 15=14; 16=15; 17=16; 18=17; 19=18; 20=19`
- `livestock_type::s12q08c`: What was the average unit price of one [ANIMAL] sold ?

---

## 5. Complete Directory & File Inventory
| # | Subdirectory / File | Extension | Size (MB) | Rows ($N$) | Columns ($K$) | Status |
|---|---|---|---|---|---|---|
| 1 | `data/01_file_headers/file_headers.csv` | `.csv` | 0.026 | 74 | 10 | OK |
| 2 | `data/01_file_headers/file_headers.txt` | `.txt` | 0.04 | 2,338 | 1 | OK |
| 3 | `data/AASS 2022_2023/AASS2023.dta` | `.dta` | 5.623 | 15,944 | 46 | OK |
| 4 | `data/AASS 2022_2023/aquaculture.dta` | `.dta` | 0.041 | 381 | 13 | OK |
| 5 | `data/AASS 2022_2023/crop_use.dta` | `.dta` | 6.383 | 36,147 | 23 | OK |
| 6 | `data/AASS 2022_2023/external_labor_activities.dta` | `.dta` | 1.335 | 12,351 | 14 | OK |
| 7 | `data/AASS 2022_2023/field.dta` | `.dta` | 1.55 | 28,472 | 7 | OK |
| 8 | `data/AASS 2022_2023/household.dta` | `.dta` | 14.739 | 76,863 | 25 | OK |
| 9 | `data/AASS 2022_2023/inputs.dta` | `.dta` | 3.529 | 19,967 | 23 | OK |
| 10 | `data/AASS 2022_2023/items_services.dta` | `.dta` | 0.929 | 13,300 | 9 | OK |
| 11 | `data/AASS 2022_2023/masika_use.dta` | `.dta` | 1.975 | 36,296 | 7 | OK |
| 12 | `data/AASS 2022_2023/masikacrop.dta` | `.dta` | 8.097 | 32,002 | 33 | OK |
| 13 | `data/AASS 2022_2023/masikaplot.dta` | `.dta` | 7.146 | 25,896 | 36 | OK |
| 14 | `data/AASS 2022_2023/otherproducts.dta` | `.dta` | 0.668 | 5,755 | 15 | OK |
| 15 | `data/AASS 2022_2023/permanent_crop.dta` | `.dta` | 1.265 | 8,201 | 20 | OK |
| 16 | `data/AASS 2022_2023/seeds.dta` | `.dta` | 7.035 | 36,667 | 25 | OK |
| 17 | `data/AASS 2022_2023/vuli_use.dta` | `.dta` | 1.95 | 35,828 | 7 | OK |
| 18 | `data/AASS 2022_2023/vulicrop.dta` | `.dta` | 6.945 | 28,300 | 32 | OK |
| 19 | `data/AASS 2022_2023/vuliplot.dta` | `.dta` | 5.632 | 20,405 | 36 | OK |
| 20 | `data/AASS 2023_2024/AASS2024f.dta` | `.dta` | 2.213 | 18,836 | 16 | OK |
| 21 | `data/AASS 2023_2024/CROP_USE.dta` | `.dta` | 6.095 | 36,480 | 22 | OK |
| 22 | `data/AASS 2023_2024/FIELD.dta` | `.dta` | 0.982 | 29,390 | 4 | OK |
| 23 | `data/AASS 2023_2024/HOUSEHOLD.dta` | `.dta` | 11.799 | 88,977 | 17 | OK |
| 24 | `data/AASS 2023_2024/InputRoster_masika.dta` | `.dta` | 0.466 | 15,694 | 4 | OK |
| 25 | `data/AASS 2023_2024/InputRoster_vuli.dta` | `.dta` | 0.155 | 5,192 | 4 | OK |
| 26 | `data/AASS 2023_2024/MASIKACROP.dta` | `.dta` | 12.113 | 34,574 | 46 | OK |
| 27 | `data/AASS 2023_2024/MASIKAPLOT.dta` | `.dta` | 9.037 | 27,917 | 42 | OK |
| 28 | `data/AASS 2023_2024/VULICROP.dta` | `.dta` | 6.004 | 18,757 | 42 | OK |
| 29 | `data/AASS 2023_2024/VULIPLOT.dta` | `.dta` | 5.019 | 15,495 | 42 | OK |
| 30 | `data/AASS 2023_2024/buildings_roster.dta` | `.dta` | 8.645 | 17,566 | 64 | OK |
| 31 | `data/AASS 2023_2024/collection_roster (1).dta` | `.dta` | 0.017 | 535 | 4 | OK |
| 32 | `data/AASS 2023_2024/collection_roster.dta` | `.dta` | 0.017 | 535 | 4 | OK |
| 33 | `data/AASS 2023_2024/permanent_crop.dta` | `.dta` | 1.818 | 6,999 | 34 | OK |
| 34 | `data/AASS 2023_2024/s17_aquaculture.dta` | `.dta` | 0.013 | 262 | 6 | OK |
| 35 | `data/AASS 2023_2024/sec16_otherproducts.dta` | `.dta` | 0.538 | 6,764 | 10 | OK |
| 36 | `data/AASS 2023_2024/wen_TZA.dta` | `.dta` | 5.825 | 4,405 | 153 | OK |
| 37 | `data/AASS 2024_2025/AASS2025.dta` | `.dta` | 2.896 | 18,904 | 35 | OK |
| 38 | `data/AASS 2024_2025/CROP_USE.dta` | `.dta` | 5.317 | 41,111 | 22 | OK |
| 39 | `data/AASS 2024_2025/FIELD.dta` | `.dta` | 0.766 | 31,579 | 8 | OK |
| 40 | `data/AASS 2024_2025/HOUSEHOLD.dta` | `.dta` | 1.787 | 92,945 | 9 | OK |
| 41 | `data/AASS 2024_2025/MASIKACROP.dta` | `.dta` | 9.91 | 40,485 | 54 | OK |
| 42 | `data/AASS 2024_2025/MASIKAPLOT.dta` | `.dta` | 14.334 | 31,497 | 59 | OK |
| 43 | `data/AASS 2024_2025/VULICROP.dta` | `.dta` | 1.52 | 26,105 | 26 | OK |
| 44 | `data/AASS 2024_2025/VULIPLOT.dta` | `.dta` | 8.56 | 18,441 | 60 | OK |
| 45 | `data/AASS 2024_2025/collection_roster.dta` | `.dta` | 0.065 | 3,341 | 4 | OK |
| 46 | `data/AASS 2024_2025/inputRoster_masika.dta` | `.dta` | 0.51 | 19,648 | 4 | OK |
| 47 | `data/AASS 2024_2025/inputRoster_vuli.dta` | `.dta` | 0.193 | 7,342 | 4 | OK |
| 48 | `data/AASS 2024_2025/livestock_type.dta` | `.dta` | 12.454 | 30,142 | 74 | OK |
| 49 | `data/AASS 2024_2025/permanent_crop.dta` | `.dta` | 0.775 | 13,885 | 24 | OK |
| 50 | `data/AASS 2024_2025/pme_6_Roster.dta` | `.dta` | 3.273 | 13,491 | 55 | OK |
| 51 | `data/AASS 2024_2025/s14_milk.dta` | `.dta` | 1.109 | 9,992 | 17 | OK |
| 52 | `data/AASS 2024_2025/s17_aquaculture.dta` | `.dta` | 0.047 | 925 | 6 | OK |
| 53 | `data/AASS 2024_2025/s17a1_aquastructure.dta` | `.dta` | 0.05 | 953 | 19 | OK |
| 54 | `data/AASS 2024_2025/sec16_otherproducts.dta` | `.dta` | 0.664 | 9,182 | 10 | OK |
| 55 | `data/AASS 2024_2025/shocks_roster.dta` | `.dta` | 9.211 | 43,445 | 19 | OK |
| 56 | `data/AASS 2024_2025/stock_livestock.dta` | `.dta` | 2.39 | 58,142 | 6 | OK |
| 57 | `data/AASS_metadata/data_dictionary_catalog_52.csv` | `.csv` | 0.12 | 371 | 11 | OK |
| 58 | `data/AASS_metadata/data_dictionary_catalog_52.json` | `.json` | 0.383 | 14,682 | 1 | OK |
| 59 | `data/AASS_metadata/data_dictionary_catalog_52.xlsx` | `.xlsx` | 0.034 | 371 | 11 | OK |
| 60 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R000_SOV.dta` | `.dta` | 7.304 | 30,650 | 137 | OK |
| 61 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R031_HHRECORD.dta` | `.dta` | 6.252 | - | - | ERROR |
| 62 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R041_LAND_OWNERSHIP.dta` | `.dta` | 5.742 | 214,550 | 7 | OK |
| 63 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R051_LAND_USE.dta` | `.dta` | 10.652 | 398,450 | 7 | OK |
| 64 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R062_FARMING_METHODS.dta` | `.dta` | 1.597 | 66,462 | 7 | OK |
| 65 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R071_DISTANCE_TO_FIELDS.dta` | `.dta` | 1.303 | 50,023 | 9 | OK |
| 66 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R072_COMMUNIAL_RESOURCES.dta` | `.dta` | 7.731 | 245,200 | 9 | OK |
| 67 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R081_SHORT_RAINY_SEASON.dta` | `.dta` | 7.132 | 26,799 | 63 | OK |
| 68 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R082_LONG_RAINY_SEASON.dta` | `.dta` | 14.127 | 53,278 | 63 | OK |
| 69 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R083_PERMANENT_CROPS.dta` | `.dta` | 6.075 | 23,138 | 61 | OK |
| 70 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R102_AGROPROCESSING.dta` | `.dta` | 0.272 | 4,460 | 21 | OK |
| 71 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R112_CROP_STORAGE.dta` | `.dta` | 7.047 | 223,399 | 12 | OK |
| 72 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R121_FARM_IMPLEMENTS.dta` | `.dta` | 12.173 | 490,400 | 8 | OK |
| 73 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R122_USE_TRACTOR_ANIMALS.dta` | `.dta` | 1.827 | 63,372 | 9 | OK |
| 74 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R123_USE_ORGANIC_FERTILIZER.dta` | `.dta` | 0.41 | 13,028 | 8 | OK |
| 75 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R124_ACCESS_FARM_INPUTS.dta` | `.dta` | 5.455 | 183,900 | 13 | OK |
| 76 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R126_SOIL_EROSION.dta` | `.dta` | 0.72 | 25,544 | 9 | OK |
| 77 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R141_EXTENSION_MESSAGES.dta` | `.dta` | 0.778 | 28,548 | 10 | OK |
| 78 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R152_CATTLE_POPULATION.dta` | `.dta` | 2.473 | 61,369 | 11 | OK |
| 79 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R153_CATTLE_INTAKE.dta` | `.dta` | 2.708 | 61,369 | 12 | OK |
| 80 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R154_CATTLE_OFFTAKE.dta` | `.dta` | 2.943 | 61,369 | 14 | OK |
| 81 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R155_CATTLE_DISEASES.dta` | `.dta` | 3.253 | 78,903 | 14 | OK |
| 82 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R157_CATTLE_MILK_PRODUCTION.dta` | `.dta` | 0.915 | 19,208 | 14 | OK |
| 83 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R162_GOAT_POPULATION.dta` | `.dta` | 2.042 | 36,620 | 13 | OK |
| 84 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R163_GOAT_INTAKE.dta` | `.dta` | 1.622 | 36,620 | 12 | OK |
| 85 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R164_GOAT_OFFTAKE.dta` | `.dta` | 1.763 | 36,620 | 14 | OK |
| 86 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R165_GOAT_DISEASES.dta` | `.dta` | 2.42 | 58,592 | 14 | OK |
| 87 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R166_GOAT_MILK_PRODUCTION.dta` | `.dta` | 0.035 | 426 | 14 | OK |
| 88 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R172_SHEEP_POPULATION.dta` | `.dta` | 0.629 | 15,335 | 11 | OK |
| 89 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R173_SHEEP_INTAKE.dta` | `.dta` | 0.688 | 15,335 | 12 | OK |
| 90 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R174_SHEEP_OFFTAKE.dta` | `.dta` | 0.748 | 15,335 | 14 | OK |
| 91 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R175_SHEEP_DISEASES.dta` | `.dta` | 1.024 | 24,536 | 14 | OK |
| 92 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R182_PIG_POPULATION.dta` | `.dta` | 0.387 | 11,544 | 8 | OK |
| 93 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R183_PIG_INTAKE.dta` | `.dta` | 0.522 | 11,544 | 12 | OK |
| 94 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R184_PIG_OFFTAKE.dta` | `.dta` | 0.567 | 11,544 | 14 | OK |
| 95 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R185_PIG_DISEASES.dta` | `.dta` | 0.57 | 13,468 | 14 | OK |
| 96 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R192_POULTRY_POPULATION.dta` | `.dta` | 5.718 | 108,744 | 11 | OK |
| 97 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R193_POULTRY_DISEASES.dta` | `.dta` | 6.238 | 108,744 | 13 | OK |
| 98 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R202_OTHER_LIVESTOCK_POP.dta` | `.dta` | 1.428 | 30,252 | 11 | OK |
| 99 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R203_OTHER_LIVESTOCK_PROD.dta` | `.dta` | 8.048 | 153,160 | 11 | OK |
| 100 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R210_OUTLET_SALES_LIVEST.dta` | `.dta` | 1.696 | 31,436 | 12 | OK |
| 101 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R220_LIVEST_STUCTURES_AC.dta` | `.dta` | 19.745 | 459,750 | 10 | OK |
| 102 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R241_LIVESTOCK_EXTENSION.dta` | `.dta` | 0.772 | 18,438 | 11 | OK |
| 103 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R250_LIVESTOCK_EXT_SERVICE.dta` | `.dta` | 0.385 | 7,902 | 13 | OK |
| 104 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R262_GOVT_REGULAT_CHALLENG.dta` | `.dta` | 0.061 | 1,197 | 8 | OK |
| 105 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R272_FISH_FARMING.dta` | `.dta` | 0.037 | 110 | 24 | OK |
| 106 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R281_BEE_KEEPING.dta` | `.dta` | 0.057 | 878 | 13 | OK |
| 107 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R291_LABOUR_USE.dta` | `.dta` | 27.022 | 858,200 | 8 | OK |
| 108 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R301_SUBSTANCE_NONSUBST.dta` | `.dta` | 13.343 | 367,800 | 10 | OK |
| 109 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R310_ACCESS_INFRASTUCTURE.dta` | `.dta` | 14.335 | 429,100 | 7 | OK |
| 110 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R311_OTHER_SERVICES.dta` | `.dta` | 6.503 | 183,900 | 9 | OK |
| 111 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R321_LIVELIHOOD_CNSTR_MOST.dta` | `.dta` | 4.588 | 92,245 | 8 | OK |
| 112 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R330_MARKET_INFORMATION.dta` | `.dta` | 8.43 | 275,850 | 7 | OK |
| 113 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R342_HOUSE_ASSETS.dta` | `.dta` | 15.913 | 521,050 | 7 | OK |
| 114 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R344_ACCESS_DRINKING_WATER.dta` | `.dta` | 2.352 | 61,300 | 9 | OK |
| 115 | `data/NCSA 2019_2020 Small_Scale_Farmers_Dataset_ACQI/R346_FOOD_SECURITY.dta` | `.dta` | 1.247 | 30,650 | 17 | OK |
| 116 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/EA.Offsets.dta` | `.dta` | 0.008 | 409 | 3 | OK |
| 117 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/HH.Geovariables_Y1.dta` | `.dta` | 0.49 | 2,990 | 49 | OK |
| 118 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/Plot.Geovariables_Y1_revised2.dta` | `.dta` | 0.02 | 862 | 3 | OK |
| 119 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_10A.dta` | `.dta` | 2.253 | 28,641 | 39 | OK |
| 120 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_10B.dta` | `.dta` | 0.575 | 16,209 | 12 | OK |
| 121 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_11_ALL.dta` | `.dta` | 1.236 | 30,021 | 18 | OK |
| 122 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_12A.dta` | `.dta` | 0.039 | 1,105 | 10 | OK |
| 123 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_12B.dta` | `.dta` | 0.019 | 691 | 8 | OK |
| 124 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_12C.dta` | `.dta` | 0.006 | 187 | 8 | OK |
| 125 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_12D.dta` | `.dta` | 0.048 | 2,321 | 5 | OK |
| 126 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_13A.dta` | `.dta` | 0.339 | 12,135 | 13 | OK |
| 127 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_13B.dta` | `.dta` | 0.391 | 19,432 | 5 | OK |
| 128 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_1_ALL.dta` | `.dta` | 0.235 | 12,923 | 5 | OK |
| 129 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_2A.dta` | `.dta` | 0.143 | 5,128 | 4 | OK |
| 130 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_2B.dta` | `.dta` | 0.003 | 86 | 4 | OK |
| 131 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_3A.dta` | `.dta` | 1.434 | 5,126 | 175 | OK |
| 132 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_3B.dta` | `.dta` | 1.346 | 5,182 | 169 | OK |
| 133 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_4A.dta` | `.dta` | 0.367 | 5,704 | 28 | OK |
| 134 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_4B.dta` | `.dta` | 0.122 | 2,028 | 28 | OK |
| 135 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_5A.dta` | `.dta` | 0.36 | 4,291 | 26 | OK |
| 136 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_5B.dta` | `.dta` | 0.081 | 1,029 | 26 | OK |
| 137 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_6A.dta` | `.dta` | 0.177 | 3,273 | 16 | OK |
| 138 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_6B.dta` | `.dta` | 0.14 | 2,435 | 16 | OK |
| 139 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_7A.dta` | `.dta` | 0.143 | 2,483 | 17 | OK |
| 140 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_7B.dta` | `.dta` | 0.089 | 1,522 | 17 | OK |
| 141 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_8A.dta` | `.dta` | 0.006 | 16 | 12 | OK |
| 142 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_8B.dta` | `.dta` | 0.005 | 4 | 12 | OK |
| 143 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_8C.dta` | `.dta` | 0.005 | 1 | 12 | OK |
| 144 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_9_ALL.dta` | `.dta` | 0.156 | 2,774 | 16 | OK |
| 145 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_A.dta` | `.dta` | 0.023 | 407 | 23 | OK |
| 146 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_A_T.dta` | `.dta` | 0.217 | 3,265 | 34 | OK |
| 147 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_B.dta` | `.dta` | 0.286 | 11,396 | 10 | OK |
| 148 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_B_C_D_E1_F_G1_U.dta` | `.dta` | 5.965 | - | - | ERROR |
| 149 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_C.dta` | `.dta` | 0.156 | 5,698 | 12 | OK |
| 150 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_D.dta` | `.dta` | 0.053 | 407 | 41 | OK |
| 151 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_E2.dta` | `.dta` | 0.016 | 114 | 31 | OK |
| 152 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_E_F_G.dta` | `.dta` | 0.04 | 407 | 49 | OK |
| 153 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_G2.dta` | `.dta` | 0.109 | 3,960 | 10 | OK |
| 154 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_H.dta` | `.dta` | 0.031 | 407 | 36 | OK |
| 155 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_H1_J_K2_O2_P1_Q1_S1.dta` | `.dta` | 0.295 | 3,265 | 68 | OK |
| 156 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_H2.dta` | `.dta` | 0.475 | 26,096 | 6 | OK |
| 157 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_H3.dta` | `.dta` | 0.266 | 16,313 | 4 | OK |
| 158 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_I.dta` | `.dta` | 0.227 | 3,620 | 49 | OK |
| 159 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_I_J1.dta` | `.dta` | 0.065 | 407 | 65 | OK |
| 160 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_J2.dta` | `.dta` | 0.497 | 19,159 | 10 | OK |
| 161 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_K1.dta` | `.dta` | 11.211 | 192,635 | 12 | OK |
| 162 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_L.dta` | `.dta` | 2.88 | 143,660 | 4 | OK |
| 163 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_M.dta` | `.dta` | 0.157 | 6,528 | 5 | OK |
| 164 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_N.dta` | `.dta` | 0.688 | 39,981 | 3 | OK |
| 165 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_NETWORK.dta` | `.dta` | 0.133 | 7,235 | 4 | OK |
| 166 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_O1.dta` | `.dta` | 0.524 | 19,572 | 6 | OK |
| 167 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_O3.dta` | `.dta` | 0.011 | 198 | 14 | OK |
| 168 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_P2.dta` | `.dta` | 0.012 | 228 | 13 | OK |
| 169 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_Q2.dta` | `.dta` | 0.037 | 909 | 14 | OK |
| 170 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_Q3.dta` | `.dta` | 0.015 | 287 | 14 | OK |
| 171 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_QNFLOW.dta` | `.dta` | 0.154 | 2,429 | 34 | OK |
| 172 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_R.dta` | `.dta` | 0.227 | 10,241 | 8 | OK |
| 173 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/SEC_S2.dta` | `.dta` | 0.018 | 334 | 17 | OK |
| 174 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/TZNPS_Geovariables_Y1.pdf` | `.pdf` | 0.431 | - | - | OK |
| 175 | `data/NPS Wave 1 2008_2009 TZA_2008_NPS1/TZA_2008_NPS1/TZY1.HH.Consumption.dta` | `.dta` | 0.468 | 3,265 | 41 | OK |
| 176 | `data/NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_FILTERS.dta` | `.dta` | 0.092 | 3,924 | 9 | OK |
| 177 | `data/NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_NETWORK.dta` | `.dta` | 0.18 | 8,884 | 4 | OK |
| 178 | `data/NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_SEC01.dta` | `.dta` | 0.315 | 15,666 | 5 | OK |
| 179 | `data/NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_SEC09.dta` | `.dta` | 0.244 | 4,713 | 16 | OK |
| 180 | `data/NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_SEC10A.dta` | `.dta` | 3.084 | 30,944 | 56 | OK |
| 181 | `data/NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_SEC10B.dta` | `.dta` | 0.955 | 23,208 | 14 | OK |
| 182 | `data/NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_SEC10C.dta` | `.dta` | 0.174 | 5,802 | 9 | OK |
| 183 | `data/NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_SEC11.dta` | `.dta` | 1.26 | 38,752 | 11 | OK |
| 184 | `data/NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_SEC12A.dta` | `.dta` | 0.743 | 13,845 | 14 | OK |
| 185 | `data/NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_SEC12B.dta` | `.dta` | 0.91 | 22,152 | 6 | OK |
| 186 | `data/NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_SEC2A.dta` | `.dta` | 0.192 | 6,038 | 8 | OK |
| 187 | `data/NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_SEC2B.dta` | `.dta` | 0.003 | 38 | 8 | OK |
| 188 | `data/NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_SEC3A.dta` | `.dta` | 1.646 | 6,038 | 166 | OK |
| 189 | `data/NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_SEC3B.dta` | `.dta` | 1.495 | 6,076 | 160 | OK |
| 190 | `data/NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_SEC4A.dta` | `.dta` | 0.509 | 8,206 | 29 | OK |
| 191 | `data/NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_SEC4B.dta` | `.dta` | 0.42 | 6,742 | 29 | OK |
| 192 | `data/NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_SEC5A.dta` | `.dta` | 0.421 | 4,621 | 41 | OK |
| 193 | `data/NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_SEC5B.dta` | `.dta` | 0.127 | 1,336 | 41 | OK |
| 194 | `data/NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_SEC6A.dta` | `.dta` | 0.265 | 4,796 | 16 | OK |
| 195 | `data/NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_SEC6B.dta` | `.dta` | 0.267 | 3,990 | 16 | OK |
| 196 | `data/NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_SEC7A.dta` | `.dta` | 0.24 | 4,110 | 17 | OK |
| 197 | `data/NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_SEC7B.dta` | `.dta` | 0.321 | 2,983 | 18 | OK |
| 198 | `data/NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_SEC8A.dta` | `.dta` | 0.007 | 28 | 15 | OK |
| 199 | `data/NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_SEC8B.dta` | `.dta` | 0.006 | 2 | 15 | OK |
| 200 | `data/NPS Wave 2 2010_2011  Agriculture/Agriculture/AG_SEC8C.dta` | `.dta` | 0.006 | 4 | 15 | OK |
| 201 | `data/NPS Wave 2 2010_2011  Agriculture/Agriculture/Plot.Geovariables_Y2.dta` | `.dta` | 0.15 | 4,724 | 4 | OK |
| 202 | `data/NPS Wave 2 2010_2011  Community/Community/COMSEC_CA.dta` | `.dta` | 0.009 | 393 | 13 | OK |
| 203 | `data/NPS Wave 2 2010_2011  Community/Community/COMSEC_CB.dta` | `.dta` | 0.475 | 11,816 | 9 | OK |
| 204 | `data/NPS Wave 2 2010_2011  Community/Community/COMSEC_CD.dta` | `.dta` | 0.056 | 392 | 38 | OK |
| 205 | `data/NPS Wave 2 2010_2011  Community/Community/COMSEC_CE.dta` | `.dta` | 0.017 | 360 | 22 | OK |
| 206 | `data/NPS Wave 2 2010_2011  Community/Community/COMSEC_CF.dta` | `.dta` | 0.01 | 393 | 14 | OK |
| 207 | `data/NPS Wave 2 2010_2011  Community/Community/COMSEC_CG.dta` | `.dta` | 0.011 | 393 | 17 | OK |
| 208 | `data/NPS Wave 2 2010_2011  Community/Community/COMSEC_CH.dta` | `.dta` | 0.014 | 393 | 17 | OK |
| 209 | `data/NPS Wave 2 2010_2011  Community/Community/COMSEC_CI.dta` | `.dta` | 0.162 | 2,531 | 28 | OK |
| 210 | `data/NPS Wave 2 2010_2011  Community/Community/COMSEC_CJ.dta` | `.dta` | 1.031 | 19,261 | 12 | OK |
| 211 | `data/NPS Wave 2 2010_2011  Community/Community/TZY2.EA.Offsets.dta` | `.dta` | 0.008 | 409 | 4 | OK |
| 212 | `data/NPS Wave 2 2010_2011  Household/Household/HH.Geovariables_Y2.dta` | `.dta` | 0.532 | 3,917 | 49 | OK |
| 213 | `data/NPS Wave 2 2010_2011  Household/Household/HH_SEC_A.dta` | `.dta` | 0.305 | 3,924 | 24 | OK |
| 214 | `data/NPS Wave 2 2010_2011  Household/Household/HH_SEC_B.dta` | `.dta` | 1.422 | 20,559 | 40 | OK |
| 215 | `data/NPS Wave 2 2010_2011  Household/Household/HH_SEC_C.dta` | `.dta` | 1.658 | 20,559 | 41 | OK |
| 216 | `data/NPS Wave 2 2010_2011  Household/Household/HH_SEC_D.dta` | `.dta` | 1.92 | 20,562 | 59 | OK |
| 217 | `data/NPS Wave 2 2010_2011  Household/Household/HH_SEC_E1.dta` | `.dta` | 3.32 | 20,559 | 99 | OK |
| 218 | `data/NPS Wave 2 2010_2011  Household/Household/HH_SEC_E2.dta` | `.dta` | 0.037 | 338 | 30 | OK |
| 219 | `data/NPS Wave 2 2010_2011  Household/Household/HH_SEC_F.dta` | `.dta` | 0.965 | 20,560 | 17 | OK |
| 220 | `data/NPS Wave 2 2010_2011  Household/Household/HH_SEC_FILTERS.dta` | `.dta` | 0.092 | 3,924 | 9 | OK |
| 221 | `data/NPS Wave 2 2010_2011  Household/Household/HH_SEC_G.dta` | `.dta` | 0.594 | 20,562 | 15 | OK |
| 222 | `data/NPS Wave 2 2010_2011  Household/Household/HH_SEC_H1.dta` | `.dta` | 1.798 | 31,392 | 6 | OK |
| 223 | `data/NPS Wave 2 2010_2011  Household/Household/HH_SEC_H2.dta` | `.dta` | 0.825 | 19,620 | 5 | OK |
| 224 | `data/NPS Wave 2 2010_2011  Household/Household/HH_SEC_H3.dta` | `.dta` | 0.806 | 19,620 | 4 | OK |
| 225 | `data/NPS Wave 2 2010_2011  Household/Household/HH_SEC_I1.dta` | `.dta` | 0.146 | 3,924 | 22 | OK |
| 226 | `data/NPS Wave 2 2010_2011  Household/Household/HH_SEC_I2.dta` | `.dta` | 0.202 | 3,924 | 37 | OK |
| 227 | `data/NPS Wave 2 2010_2011  Household/Household/HH_SEC_J1.dta` | `.dta` | 0.35 | 3,924 | 51 | OK |
| 228 | `data/NPS Wave 2 2010_2011  Household/Household/HH_SEC_J2.dta` | `.dta` | 1.26 | 54,936 | 7 | OK |
| 229 | `data/NPS Wave 2 2010_2011  Household/Household/HH_SEC_K1.dta` | `.dta` | 17.889 | 231,516 | 13 | OK |
| 230 | `data/NPS Wave 2 2010_2011  Household/Household/HH_SEC_K2.dta` | `.dta` | 1.985 | 39,240 | 4 | OK |
| 231 | `data/NPS Wave 2 2010_2011  Household/Household/HH_SEC_K3.dta` | `.dta` | 0.241 | 5,840 | 5 | OK |
| 232 | `data/NPS Wave 2 2010_2011  Household/Household/HH_SEC_L.dta` | `.dta` | 2.326 | 105,948 | 4 | OK |
| 233 | `data/NPS Wave 2 2010_2011  Household/Household/HH_SEC_M.dta` | `.dta` | 1.922 | 74,556 | 5 | OK |
| 234 | `data/NPS Wave 2 2010_2011  Household/Household/HH_SEC_N.dta` | `.dta` | 3.894 | 204,048 | 3 | OK |
| 235 | `data/NPS Wave 2 2010_2011  Household/Household/HH_SEC_O1.dta` | `.dta` | 1.866 | 23,544 | 10 | OK |
| 236 | `data/NPS Wave 2 2010_2011  Household/Household/HH_SEC_O2.dta` | `.dta` | 0.017 | 301 | 15 | OK |
| 237 | `data/NPS Wave 2 2010_2011  Household/Household/HH_SEC_P.dta` | `.dta` | 0.018 | 410 | 13 | OK |
| 238 | `data/NPS Wave 2 2010_2011  Household/Household/HH_SEC_Q.dta` | `.dta` | 0.467 | 3,924 | 40 | OK |
| 239 | `data/NPS Wave 2 2010_2011  Household/Household/HH_SEC_R.dta` | `.dta` | 1.78 | 74,537 | 8 | OK |
| 240 | `data/NPS Wave 2 2010_2011  Household/Household/HH_SEC_S.dta` | `.dta` | 0.023 | 295 | 19 | OK |
| 241 | `data/NPS Wave 2 2010_2011  Household/Household/HH_SEC_U.dta` | `.dta` | 0.61 | 20,559 | 9 | OK |
| 242 | `data/NPS Wave 2 2010_2011  Household/Household/HH_SEC_V2.dta` | `.dta` | 0.092 | 3,924 | 9 | OK |
| 243 | `data/NPS Wave 2 2010_2011  Household/Household/TZY1.HH.Consumption.dta` | `.dta` | 0.468 | 3,265 | 41 | OK |
| 244 | `data/NPS Wave 2 2010_2011  Household/Household/TZY2.HH.Consumption.dta` | `.dta` | 0.602 | 3,846 | 41 | OK |
| 245 | `data/NPS Wave 2 2010_2011 Fishery/Fishery/FS_B1.dta` | `.dta` | 0.007 | 150 | 14 | OK |
| 246 | `data/NPS Wave 2 2010_2011 Fishery/Fishery/FS_C1.dta` | `.dta` | 0.008 | 181 | 14 | OK |
| 247 | `data/NPS Wave 2 2010_2011 Fishery/Fishery/FS_D1.dta` | `.dta` | 0.005 | 150 | 6 | OK |
| 248 | `data/NPS Wave 2 2010_2011 Fishery/Fishery/FS_D2.dta` | `.dta` | 0.004 | 150 | 5 | OK |
| 249 | `data/NPS Wave 2 2010_2011 Fishery/Fishery/FS_D3.dta` | `.dta` | 0.01 | 150 | 14 | OK |
| 250 | `data/NPS Wave 2 2010_2011 Fishery/Fishery/FS_E1.dta` | `.dta` | 0.077 | 1,500 | 9 | OK |
| 251 | `data/NPS Wave 2 2010_2011 Fishery/Fishery/FS_E2.dta` | `.dta` | 0.055 | 900 | 14 | OK |
| 252 | `data/NPS Wave 2 2010_2011 Fishery/Fishery/FS_E3.dta` | `.dta` | 0.095 | 1,950 | 6 | OK |
| 253 | `data/NPS Wave 2 2010_2011 Fishery/Fishery/FS_F.dta` | `.dta` | 0.033 | 283 | 40 | OK |
| 254 | `data/NPS Wave 2 2010_2011 Fishery/Fishery/FS_FILTERS.dta` | `.dta` | 0.005 | 150 | 5 | OK |
| 255 | `data/NPS Wave 2 2010_2011 Fishery/Fishery/FS_G.dta` | `.dta` | 0.098 | 2,102 | 6 | OK |
| 256 | `data/NPS Wave 2 2010_2011 Fishery/Fishery/FS_H1.dta` | `.dta` | 0.015 | 209 | 18 | OK |
| 257 | `data/NPS Wave 2 2010_2011 Fishery/Fishery/FS_H2.dta` | `.dta` | 0.019 | 525 | 5 | OK |
| 258 | `data/NPS Wave 2 2010_2011 Fishery/Fishery/FS_H3.dta` | `.dta` | 0.003 | 112 | 3 | OK |
| 259 | `data/NPS Wave 2 2010_2011 Fishery/Fishery/FS_I.dta` | `.dta` | 0.006 | 122 | 14 | OK |
| 260 | `data/NPS Wave 2 2010_2011 Fishery/Fishery/FS_J1.dta` | `.dta` | 0.529 | 4,007 | 53 | OK |
| 261 | `data/NPS Wave 2 2010_2011 Fishery/Fishery/FS_J2.dta` | `.dta` | 0.004 | 150 | 5 | OK |
| 262 | `data/NPS Wave 2 2010_2011 Fishery/Fishery/FS_J3.dta` | `.dta` | 0.529 | 4,007 | 53 | OK |
| 263 | `data/NPS Wave 2 2010_2011 Fishery/Fishery/FS_K1.dta` | `.dta` | 0.058 | 1,120 | 9 | OK |
| 264 | `data/NPS Wave 2 2010_2011 Fishery/Fishery/FS_K2.dta` | `.dta` | 0.042 | 678 | 14 | OK |
| 265 | `data/NPS Wave 2 2010_2011 Fishery/Fishery/FS_K3.dta` | `.dta` | 0.071 | 1,456 | 6 | OK |
| 266 | `data/NPS Wave 2 2010_2011 Fishery/Fishery/FS_L.dta` | `.dta` | 0.025 | 234 | 39 | OK |
| 267 | `data/NPS Wave 2 2010_2011 Fishery/Fishery/FS_M.dta` | `.dta` | 0.097 | 1,606 | 6 | OK |
| 268 | `data/NPS Wave 2 2010_2011 Fishery/Fishery/FS_N1.dta` | `.dta` | 0.013 | 189 | 18 | OK |
| 269 | `data/NPS Wave 2 2010_2011 Fishery/Fishery/FS_N2.dta` | `.dta` | 0.01 | 420 | 4 | OK |
| 270 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_FILTERS.dta` | `.dta` | 0.093 | 5,010 | 10 | OK |
| 271 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_NETWORK.dta` | `.dta` | 0.241 | 8,372 | 6 | OK |
| 272 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_SEC_01.dta` | `.dta` | 0.535 | 18,654 | 7 | OK |
| 273 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_SEC_08.dta` | `.dta` | 0.229 | 5,930 | 16 | OK |
| 274 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_SEC_10.dta` | `.dta` | 0.418 | 7,316 | 22 | OK |
| 275 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_SEC_11.dta` | `.dta` | 2.558 | 51,532 | 13 | OK |
| 276 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_SEC_12A.dta` | `.dta` | 0.929 | 18,306 | 19 | OK |
| 277 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_SEC_12B.dta` | `.dta` | 0.918 | 28,271 | 7 | OK |
| 278 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_SEC_2A.dta` | `.dta` | 0.938 | 9,157 | 15 | OK |
| 279 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_SEC_2B.dta` | `.dta` | 0.51 | 5,013 | 16 | OK |
| 280 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_SEC_3A.dta` | `.dta` | 2.764 | 9,157 | 178 | OK |
| 281 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_SEC_3B.dta` | `.dta` | 2.371 | 9,173 | 173 | OK |
| 282 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_SEC_4A.dta` | `.dta` | 1.197 | 10,183 | 40 | OK |
| 283 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_SEC_4B.dta` | `.dta` | 0.755 | 6,450 | 40 | OK |
| 284 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_SEC_5A.dta` | `.dta` | 0.943 | 8,422 | 48 | OK |
| 285 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_SEC_5B.dta` | `.dta` | 0.623 | 5,884 | 48 | OK |
| 286 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_SEC_6A.dta` | `.dta` | 0.466 | 8,795 | 19 | OK |
| 287 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_SEC_6B.dta` | `.dta` | 0.477 | 7,726 | 19 | OK |
| 288 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_SEC_7A.dta` | `.dta` | 0.449 | 8,015 | 22 | OK |
| 289 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_SEC_7B.dta` | `.dta` | 0.402 | 6,581 | 23 | OK |
| 290 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_SEC_9A.dta` | `.dta` | 0.158 | 5,011 | 16 | OK |
| 291 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_SEC_9B.dta` | `.dta` | 0.153 | 5,010 | 16 | OK |
| 292 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_SEC_9C.dta` | `.dta` | 0.149 | 5,010 | 16 | OK |
| 293 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/AG_SEC_A.dta` | `.dta` | 1.082 | 5,010 | 31 | OK |
| 294 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/COM_SEC_A1A2.dta` | `.dta` | 0.088 | 401 | 43 | OK |
| 295 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/COM_SEC_CB.dta` | `.dta` | 0.832 | 12,431 | 11 | OK |
| 296 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/COM_SEC_CC.dta` | `.dta` | 0.297 | 5,614 | 12 | OK |
| 297 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/COM_SEC_CD.dta` | `.dta` | 0.063 | 400 | 39 | OK |
| 298 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/COM_SEC_CE.dta` | `.dta` | 0.047 | 401 | 43 | OK |
| 299 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/COM_SEC_CF.dta` | `.dta` | 1.355 | 20,852 | 13 | OK |
| 300 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/COM_SEC_CF_ID.dta` | `.dta` | 0.089 | 401 | 23 | OK |
| 301 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/COM_SEC_CG.dta` | `.dta` | 0.765 | 9,624 | 14 | OK |
| 302 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/ConsumptionNPS3.dta` | `.dta` | 0.614 | 4,883 | 35 | OK |
| 303 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/FILTERS.dta` | `.dta` | 0.148 | 4,845 | 22 | OK |
| 304 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_FILTERS.dta` | `.dta` | 0.079 | 5,010 | 9 | OK |
| 305 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_A.dta` | `.dta` | 1.36 | 5,010 | 52 | OK |
| 306 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_B.dta` | `.dta` | 2.8 | 25,412 | 45 | OK |
| 307 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_C.dta` | `.dta` | 1.854 | 25,412 | 42 | OK |
| 308 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_D.dta` | `.dta` | 1.881 | 25,412 | 45 | OK |
| 309 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_E.dta` | `.dta` | 6.439 | 25,412 | 103 | OK |
| 310 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_F.dta` | `.dta` | 1.047 | 25,412 | 19 | OK |
| 311 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_G.dta` | `.dta` | 0.564 | 25,412 | 16 | OK |
| 312 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_H.dta` | `.dta` | 0.329 | 5,010 | 59 | OK |
| 313 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_I.dta` | `.dta` | 0.269 | 5,010 | 31 | OK |
| 314 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_J1.dta` | `.dta` | 15.791 | 295,590 | 13 | OK |
| 315 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_J2.dta` | `.dta` | 0.308 | 20,040 | 8 | OK |
| 316 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_J3.dta` | `.dta` | 1.721 | 50,100 | 5 | OK |
| 317 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_J4.dta` | `.dta` | 0.708 | 20,040 | 6 | OK |
| 318 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_K.dta` | `.dta` | 2.114 | 130,260 | 6 | OK |
| 319 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_L.dta` | `.dta` | 2.487 | 130,260 | 6 | OK |
| 320 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_M.dta` | `.dta` | 7.346 | 265,530 | 7 | OK |
| 321 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_N.dta` | `.dta` | 0.615 | 5,759 | 40 | OK |
| 322 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_O1.dta` | `.dta` | 1.264 | 30,060 | 13 | OK |
| 323 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_O2.dta` | `.dta` | 0.268 | 5,045 | 17 | OK |
| 324 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_P.dta` | `.dta` | 0.219 | 5,117 | 15 | OK |
| 325 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_Q1.dta` | `.dta` | 0.462 | 5,010 | 33 | OK |
| 326 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_Q2.dta` | `.dta` | 0.283 | 5,474 | 24 | OK |
| 327 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_R.dta` | `.dta` | 1.912 | 95,190 | 12 | OK |
| 328 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_S.dta` | `.dta` | 0.236 | 5,027 | 20 | OK |
| 329 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_U2.dta` | `.dta` | 0.098 | 5,010 | 13 | OK |
| 330 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/HH_SEC_V.dta` | `.dta` | 0.731 | 25,412 | 12 | OK |
| 331 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/LF_FILTERS.dta` | `.dta` | 0.068 | 5,010 | 7 | OK |
| 332 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/LF_NETWORK.dta` | `.dta` | 0.084 | 2,771 | 6 | OK |
| 333 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/LF_SEC_01.dta` | `.dta` | 0.403 | 14,042 | 7 | OK |
| 334 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/LF_SEC_02.dta` | `.dta` | 3.639 | 34,609 | 45 | OK |
| 335 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/LF_SEC_03.dta` | `.dta` | 0.431 | 12,979 | 24 | OK |
| 336 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/LF_SEC_04.dta` | `.dta` | 0.69 | 12,979 | 42 | OK |
| 337 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/LF_SEC_05.dta` | `.dta` | 0.438 | 12,979 | 25 | OK |
| 338 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/LF_SEC_06.dta` | `.dta` | 0.672 | 12,979 | 20 | OK |
| 339 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/LF_SEC_07.dta` | `.dta` | 0.3 | 12,979 | 11 | OK |
| 340 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/LF_SEC_08.dta` | `.dta` | 0.275 | 8,653 | 15 | OK |
| 341 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/LF_SEC_09.dta` | `.dta` | 0.007 | 302 | 12 | OK |
| 342 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/LF_SEC_10.dta` | `.dta` | 0.007 | 100 | 20 | OK |
| 343 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/LF_SEC_11A.dta` | `.dta` | 0.165 | 3,404 | 12 | OK |
| 344 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/LF_SEC_11B.dta` | `.dta` | 0.122 | 3,162 | 7 | OK |
| 345 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/LF_SEC_12.dta` | `.dta` | 0.049 | 458 | 43 | OK |
| 346 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/LF_SEC_13A.dta` | `.dta` | 0.024 | 387 | 21 | OK |
| 347 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/LF_SEC_13B.dta` | `.dta` | 0.025 | 928 | 6 | OK |
| 348 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/LF_SEC_A.dta` | `.dta` | 0.531 | 2,298 | 31 | OK |
| 349 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/NPSY3.PANEL.KEY.dta` | `.dta` | 1.146 | 27,889 | 7 | OK |
| 350 | `data/NPS Wave 3 2012_2013 STATA_Y3_DATASETS/Y3_weights.dta` | `.dta` | 0.06 | 5,010 | 2 | OK |
| 351 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/LF_SEC_10.dta` | `.dta` | 0.116 | 3,360 | 19 | OK |
| 352 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/ag_filters.dta` | `.dta` | 0.043 | 3,352 | 6 | OK |
| 353 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/ag_network.dta` | `.dta` | 0.208 | 7,212 | 6 | OK |
| 354 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/ag_sec_01.dta` | `.dta` | 0.345 | 12,415 | 7 | OK |
| 355 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/ag_sec_10.dta` | `.dta` | 0.273 | 4,823 | 22 | OK |
| 356 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/ag_sec_11.dta` | `.dta` | 0.844 | 32,640 | 12 | OK |
| 357 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/ag_sec_12a.dta` | `.dta` | 0.34 | 11,724 | 20 | OK |
| 358 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/ag_sec_12b.dta` | `.dta` | 0.242 | 17,996 | 6 | OK |
| 359 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/ag_sec_2a.dta` | `.dta` | 0.563 | 5,537 | 15 | OK |
| 360 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/ag_sec_2b.dta` | `.dta` | 0.339 | 3,353 | 15 | OK |
| 361 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/ag_sec_3a.dta` | `.dta` | 1.598 | 5,537 | 171 | OK |
| 362 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/ag_sec_3b.dta` | `.dta` | 1.466 | 5,551 | 172 | OK |
| 363 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/ag_sec_4a.dta` | `.dta` | 0.943 | 7,126 | 39 | OK |
| 364 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/ag_sec_4b.dta` | `.dta` | 0.532 | 4,135 | 40 | OK |
| 365 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/ag_sec_5a.dta` | `.dta` | 0.692 | 5,978 | 52 | OK |
| 366 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/ag_sec_5b.dta` | `.dta` | 0.424 | 3,844 | 52 | OK |
| 367 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/ag_sec_6a.dta` | `.dta` | 0.26 | 5,540 | 19 | OK |
| 368 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/ag_sec_6b.dta` | `.dta` | 0.259 | 4,727 | 19 | OK |
| 369 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/ag_sec_7a.dta` | `.dta` | 0.321 | 5,128 | 27 | OK |
| 370 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/ag_sec_7b.dta` | `.dta` | 0.279 | 4,178 | 27 | OK |
| 371 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/ag_sec_a.dta` | `.dta` | 0.601 | 3,352 | 31 | OK |
| 372 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/com_sec_a1a2.dta` | `.dta` | 0.088 | 416 | 45 | OK |
| 373 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/com_sec_cb.dta` | `.dta` | 0.458 | 12,896 | 8 | OK |
| 374 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/com_sec_cc.dta` | `.dta` | 0.125 | 5,824 | 9 | OK |
| 375 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/com_sec_cd.dta` | `.dta` | 0.063 | 416 | 36 | OK |
| 376 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/com_sec_ce.dta` | `.dta` | 0.045 | 416 | 40 | OK |
| 377 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/com_sec_cf.dta` | `.dta` | 0.766 | 21,632 | 9 | OK |
| 378 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/com_sec_cf_id.dta` | `.dta` | 0.018 | 391 | 24 | OK |
| 379 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/com_sec_cg.dta` | `.dta` | 0.697 | 9,984 | 11 | OK |
| 380 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/consumptionNPS4.dta` | `.dta` | 0.486 | 3,344 | 45 | OK |
| 381 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_filters.dta` | `.dta` | 0.054 | 3,352 | 9 | OK |
| 382 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_sec_a.dta` | `.dta` | 0.804 | 3,352 | 57 | OK |
| 383 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_sec_b.dta` | `.dta` | 1.969 | 16,285 | 44 | OK |
| 384 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_sec_c.dta` | `.dta` | 1.192 | 16,285 | 42 | OK |
| 385 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_sec_d.dta` | `.dta` | 1.418 | 16,285 | 62 | OK |
| 386 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_sec_e.dta` | `.dta` | 3.215 | 16,285 | 74 | OK |
| 387 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_sec_f.dta` | `.dta` | 0.687 | 16,285 | 18 | OK |
| 388 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_sec_g.dta` | `.dta` | 0.426 | 16,285 | 20 | OK |
| 389 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_sec_h.dta` | `.dta` | 0.225 | 3,352 | 59 | OK |
| 390 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_sec_i.dta` | `.dta` | 0.237 | 3,352 | 41 | OK |
| 391 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_sec_j1.dta` | `.dta` | 10.938 | 201,120 | 14 | OK |
| 392 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_sec_j3.dta` | `.dta` | 0.353 | 33,511 | 4 | OK |
| 393 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_sec_j4.dta` | `.dta` | 0.155 | 13,405 | 5 | OK |
| 394 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_sec_k.dta` | `.dta` | 1.332 | 87,152 | 5 | OK |
| 395 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_sec_l.dta` | `.dta` | 1.665 | 87,152 | 6 | OK |
| 396 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_sec_m.dta` | `.dta` | 4.238 | 177,656 | 7 | OK |
| 397 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_sec_n.dta` | `.dta` | 0.414 | 3,823 | 40 | OK |
| 398 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_sec_o1.dta` | `.dta` | 0.847 | 20,112 | 13 | OK |
| 399 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_sec_o2.dta` | `.dta` | 0.18 | 3,358 | 17 | OK |
| 400 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_sec_p.dta` | `.dta` | 0.161 | 3,416 | 15 | OK |
| 401 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_sec_q1.dta` | `.dta` | 0.313 | 3,352 | 33 | OK |
| 402 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_sec_q2.dta` | `.dta` | 0.201 | 3,903 | 23 | OK |
| 403 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_sec_r.dta` | `.dta` | 0.873 | 56,984 | 8 | OK |
| 404 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_sec_s.dta` | `.dta` | 0.157 | 3,357 | 20 | OK |
| 405 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_sec_u2.dta` | `.dta` | 0.067 | 3,352 | 13 | OK |
| 406 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/hh_sec_v.dta` | `.dta` | 0.438 | 16,285 | 12 | OK |
| 407 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/lf_filters.dta` | `.dta` | 0.046 | 3,352 | 7 | OK |
| 408 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/lf_network.dta` | `.dta` | 0.11 | 3,664 | 6 | OK |
| 409 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/lf_sec_01.dta` | `.dta` | 0.287 | 10,332 | 7 | OK |
| 410 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/lf_sec_02.dta` | `.dta` | 2.12 | 23,798 | 43 | OK |
| 411 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/lf_sec_03.dta` | `.dta` | 0.33 | 10,167 | 23 | OK |
| 412 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/lf_sec_04.dta` | `.dta` | 0.405 | 10,167 | 28 | OK |
| 413 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/lf_sec_05.dta` | `.dta` | 0.344 | 10,160 | 25 | OK |
| 414 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/lf_sec_06.dta` | `.dta` | 0.557 | 10,167 | 20 | OK |
| 415 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/lf_sec_07.dta` | `.dta` | 0.216 | 10,167 | 11 | OK |
| 416 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/lf_sec_08.dta` | `.dta` | 0.206 | 6,077 | 15 | OK |
| 417 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/lf_sec_09.dta` | `.dta` | 0.064 | 3,387 | 12 | OK |
| 418 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/lf_sec_11a.dta` | `.dta` | 0.149 | 5,107 | 11 | OK |
| 419 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/lf_sec_11b.dta` | `.dta` | 0.078 | 4,972 | 6 | OK |
| 420 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/lf_sec_12.dta` | `.dta` | 0.286 | 3,419 | 42 | OK |
| 421 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/lf_sec_13a.dta` | `.dta` | 0.158 | 3,394 | 21 | OK |
| 422 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/lf_sec_13b.dta` | `.dta` | 0.056 | 3,817 | 5 | OK |
| 423 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/lf_sec_a.dta` | `.dta` | 0.697 | 3,352 | 32 | OK |
| 424 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/npsy4.child.anthro.dta` | `.dta` | 0.044 | 2,772 | 9 | OK |
| 425 | `data/NPS Wave 4 2014_2015 NPS-4-2014-STATA/npsy4.ea.offset.dta` | `.dta` | 0.012 | 419 | 5 | OK |
| 426 | `data/NPS Wave 5 2020_2021  Community-STATA-NPS-Wave5/CM_SEC_A.dta` | `.dta` | 0.095 | 488 | 23 | OK |
| 427 | `data/NPS Wave 5 2020_2021  Community-STATA-NPS-Wave5/CM_SEC_B.dta` | `.dta` | 1.057 | 15,128 | 7 | OK |
| 428 | `data/NPS Wave 5 2020_2021  Community-STATA-NPS-Wave5/CM_SEC_C.dta` | `.dta` | 1.23 | 6,832 | 17 | OK |
| 429 | `data/NPS Wave 5 2020_2021  Community-STATA-NPS-Wave5/CM_SEC_D.dta` | `.dta` | 0.061 | 488 | 21 | OK |
| 430 | `data/NPS Wave 5 2020_2021  Community-STATA-NPS-Wave5/CM_SEC_D2.dta` | `.dta` | 0.079 | 1,464 | 8 | OK |
| 431 | `data/NPS Wave 5 2020_2021  Community-STATA-NPS-Wave5/CM_SEC_E.dta` | `.dta` | 0.076 | 488 | 39 | OK |
| 432 | `data/NPS Wave 5 2020_2021  Community-STATA-NPS-Wave5/CM_SEC_F.dta` | `.dta` | 0.097 | 488 | 23 | OK |
| 433 | `data/NPS Wave 5 2020_2021  Community-STATA-NPS-Wave5/CM_SEC_F_ID.dta` | `.dta` | 1.407 | 25,376 | 9 | OK |
| 434 | `data/NPS Wave 5 2020_2021  Community-STATA-NPS-Wave5/CM_SEC_G.dta` | `.dta` | 2.665 | 21,960 | 18 | OK |
| 435 | `data/NPS Wave 5 2020_2021  Consumption_Aggregates/consumption_real_y4.dta` | `.dta` | 0.53 | 3,352 | 48 | OK |
| 436 | `data/NPS Wave 5 2020_2021  Consumption_Aggregates/consumption_real_y5.dta` | `.dta` | 0.779 | 4,709 | 48 | OK |
| 437 | `data/NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_A.dta` | `.dta` | 1.247 | 4,709 | 39 | OK |
| 438 | `data/NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_B.dta` | `.dta` | 2.743 | 23,592 | 46 | OK |
| 439 | `data/NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_C.dta` | `.dta` | 2.177 | 23,592 | 48 | OK |
| 440 | `data/NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_D.dta` | `.dta` | 3.248 | 23,592 | 64 | OK |
| 441 | `data/NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_E1.dta` | `.dta` | 11.393 | 23,592 | 97 | OK |
| 442 | `data/NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_E2.dta` | `.dta` | 0.73 | 23,592 | 12 | OK |
| 443 | `data/NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_E3.dta` | `.dta` | 1.432 | 23,592 | 20 | OK |
| 444 | `data/NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_F.dta` | `.dta` | 1.296 | 23,592 | 18 | OK |
| 445 | `data/NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_G.dta` | `.dta` | 0.941 | 23,592 | 21 | OK |
| 446 | `data/NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_H.dta` | `.dta` | 0.411 | 4,709 | 60 | OK |
| 447 | `data/NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_I.dta` | `.dta` | 0.452 | 4,709 | 47 | OK |
| 448 | `data/NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_I2.dta` | `.dta` | 0.122 | 4,709 | 6 | OK |
| 449 | `data/NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_J1.dta` | `.dta` | 1.598 | 25,140 | 14 | OK |
| 450 | `data/NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_J3.dta` | `.dta` | 1.081 | 47,090 | 4 | OK |
| 451 | `data/NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_J4.dta` | `.dta` | 0.49 | 18,836 | 6 | OK |
| 452 | `data/NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_JA1.dta` | `.dta` | 27.024 | 321,750 | 22 | OK |
| 453 | `data/NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_K.dta` | `.dta` | 3.394 | 122,434 | 5 | OK |
| 454 | `data/NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_L.dta` | `.dta` | 4.329 | 122,434 | 7 | OK |
| 455 | `data/NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_M.dta` | `.dta` | 10.321 | 263,704 | 8 | OK |
| 456 | `data/NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_N.dta` | `.dta` | 1.447 | 5,197 | 45 | OK |
| 457 | `data/NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_O1.dta` | `.dta` | 1.547 | 28,254 | 13 | OK |
| 458 | `data/NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_O2.dta` | `.dta` | 0.251 | 4,726 | 16 | OK |
| 459 | `data/NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_P.dta` | `.dta` | 0.281 | 4,753 | 17 | OK |
| 460 | `data/NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_Q1.dta` | `.dta` | 0.327 | 4,709 | 36 | OK |
| 461 | `data/NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_Q2.dta` | `.dta` | 0.335 | 5,083 | 24 | OK |
| 462 | `data/NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_R.dta` | `.dta` | 2.222 | 80,053 | 8 | OK |
| 463 | `data/NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_S.dta` | `.dta` | 0.34 | 4,719 | 24 | OK |
| 464 | `data/NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_U2.dta` | `.dta` | 0.133 | 4,709 | 9 | OK |
| 465 | `data/NPS Wave 5 2020_2021  Household-STATA-Wave5/HH_SEC_V.dta` | `.dta` | 1.225 | 23,592 | 13 | OK |
| 466 | `data/NPS Wave 5 2020_2021  NPSY5.CHILD.ANTHRO/NPSY5.CHILD.ANTHRO.dta` | `.dta` | 0.266 | 3,513 | 11 | OK |
| 467 | `data/NPS Wave 5 2020_2021  NPSY5.PANEL.KEY/NPSY5.PANEL.KEY.dta` | `.dta` | 0.585 | 26,511 | 5 | OK |
| 468 | `data/NPS Wave 5 2020_2021 Agriculture-STATA-NPS-Wave5/AG_FILTERS.dta` | `.dta` | 0.007 | 230 | 5 | OK |
| 469 | `data/NPS Wave 5 2020_2021 Agriculture-STATA-NPS-Wave5/AG_SEC_01.dta` | `.dta` | 0.72 | 6,560 | 24 | OK |
| 470 | `data/NPS Wave 5 2020_2021 Agriculture-STATA-NPS-Wave5/AG_SEC_02.dta` | `.dta` | 1.036 | 6,560 | 22 | OK |
| 471 | `data/NPS Wave 5 2020_2021 Agriculture-STATA-NPS-Wave5/AG_SEC_10.dta` | `.dta` | 0.362 | 3,817 | 35 | OK |
| 472 | `data/NPS Wave 5 2020_2021 Agriculture-STATA-NPS-Wave5/AG_SEC_11.dta` | `.dta` | 1.586 | 38,422 | 13 | OK |
| 473 | `data/NPS Wave 5 2020_2021 Agriculture-STATA-NPS-Wave5/AG_SEC_12A.dta` | `.dta` | 0.591 | 14,050 | 20 | OK |
| 474 | `data/NPS Wave 5 2020_2021 Agriculture-STATA-NPS-Wave5/AG_SEC_12B.dta` | `.dta` | 0.586 | 22,480 | 6 | OK |
| 475 | `data/NPS Wave 5 2020_2021 Agriculture-STATA-NPS-Wave5/AG_SEC_3A.dta` | `.dta` | 2.761 | 6,560 | 234 | OK |
| 476 | `data/NPS Wave 5 2020_2021 Agriculture-STATA-NPS-Wave5/AG_SEC_3B.dta` | `.dta` | 2.445 | 6,560 | 224 | OK |
| 477 | `data/NPS Wave 5 2020_2021 Agriculture-STATA-NPS-Wave5/AG_SEC_4A.dta` | `.dta` | 0.81 | 5,606 | 36 | OK |
| 478 | `data/NPS Wave 5 2020_2021 Agriculture-STATA-NPS-Wave5/AG_SEC_4B.dta` | `.dta` | 0.176 | 1,129 | 37 | OK |
| 479 | `data/NPS Wave 5 2020_2021 Agriculture-STATA-NPS-Wave5/AG_SEC_5A.dta` | `.dta` | 0.56 | 4,294 | 56 | OK |
| 480 | `data/NPS Wave 5 2020_2021 Agriculture-STATA-NPS-Wave5/AG_SEC_5B.dta` | `.dta` | 0.125 | 784 | 56 | OK |
| 481 | `data/NPS Wave 5 2020_2021 Agriculture-STATA-NPS-Wave5/AG_SEC_6A.dta` | `.dta` | 0.237 | 4,631 | 19 | OK |
| 482 | `data/NPS Wave 5 2020_2021 Agriculture-STATA-NPS-Wave5/AG_SEC_6B.dta` | `.dta` | 0.128 | 2,439 | 19 | OK |
| 483 | `data/NPS Wave 5 2020_2021 Agriculture-STATA-NPS-Wave5/AG_SEC_7A.dta` | `.dta` | 0.202 | 2,809 | 28 | OK |
| 484 | `data/NPS Wave 5 2020_2021 Agriculture-STATA-NPS-Wave5/AG_SEC_7B.dta` | `.dta` | 0.096 | 1,160 | 28 | OK |
| 485 | `data/NPS Wave 5 2020_2021 Livestock-STATA-Wave5/LF_SEC_02.dta` | `.dta` | 7.592 | 80,053 | 43 | OK |
| 486 | `data/NPS Wave 5 2020_2021 Livestock-STATA-Wave5/LF_SEC_03.dta` | `.dta` | 1.058 | 23,545 | 23 | OK |
| 487 | `data/NPS Wave 5 2020_2021 Livestock-STATA-Wave5/LF_SEC_04.dta` | `.dta` | 1.07 | 18,836 | 30 | OK |
| 488 | `data/NPS Wave 5 2020_2021 Livestock-STATA-Wave5/LF_SEC_04A.dta` | `.dta` | 0.547 | 12,981 | 19 | OK |
| 489 | `data/NPS Wave 5 2020_2021 Livestock-STATA-Wave5/LF_SEC_05.dta` | `.dta` | 0.976 | 18,836 | 27 | OK |
| 490 | `data/NPS Wave 5 2020_2021 Livestock-STATA-Wave5/LF_SEC_06.dta` | `.dta` | 0.727 | 9,418 | 20 | OK |
| 491 | `data/NPS Wave 5 2020_2021 Livestock-STATA-Wave5/LF_SEC_07.dta` | `.dta` | 0.842 | 23,545 | 11 | OK |
| 492 | `data/NPS Wave 5 2020_2021 Livestock-STATA-Wave5/LF_SEC_08.dta` | `.dta` | 0.661 | 14,127 | 15 | OK |
| 493 | `data/metadata/TZA-NBS.OCGS-AASS-2023-v01.json` | `.json` | 0.509 | 1 | 1 | OK |
| 494 | `data/metadata/TZA-NBS.OCGS-AASS-2023-v01.xml` | `.xml` | 0.576 | 26,223 | 1 | OK |
| 495 | `data/metadata/TZA-NBS.OCGS-AASS-2025-v01.json` | `.json` | 1.52 | 1 | 1 | OK |
| 496 | `data/metadata/TZA_AASS_2023-2024_v01.json` | `.json` | 0.707 | 1 | 1 | OK |
| 497 | `data/metadata/TZA_AASS_2023-2024_v01.xml` | `.xml` | 0.781 | 37,816 | 1 | OK |
| 498 | `data/metadata/ddi-documentation-english-52.pdf` | `.pdf` | 0.066 | - | - | OK |
| 499 | `data/metadata/ddi-documentation-english-60.pdf` | `.pdf` | 0.059 | - | - | OK |
| 500 | `data/metadata/ddi-documentation-english-69.pdf` | `.pdf` | 0.061 | - | - | OK |
| 501 | `data/nbs_aass_metadata/data_dictionary_catalog_52.csv` | `.csv` | 0.12 | 371 | 11 | OK |
| 502 | `data/nbs_aass_metadata/data_dictionary_catalog_52.json` | `.json` | 0.383 | 14,682 | 1 | OK |
| 503 | `data/nbs_aass_metadata/data_dictionary_catalog_52.xlsx` | `.xlsx` | 0.034 | 371 | 11 | OK |
| 504 | `data/ncsa_2019_metadata/data_dictionary_ncsa_2019.csv` | `.csv` | 0.477 | 925 | 11 | OK |
| 505 | `data/ncsa_2019_metadata/data_dictionary_ncsa_2019.json` | `.json` | 1.866 | 43,018 | 1 | OK |
| 506 | `data/ncsa_2019_metadata/data_dictionary_ncsa_2019.md` | `.md` | 0.102 | - | - | OK |
| 507 | `data/ncsa_2019_metadata/ncsa_2019_file_inventory.csv` | `.csv` | 0.012 | 56 | 7 | OK |
| 508 | `data/scan_ncsa_dictionary.py` | `.py` | 0.015 | - | - | OK |
| 509 | `data/tanzania_maps/TANZANIA_2022PHC_WARDS_SHAPEFILES.cpg` | `.cpg` | 0.0 | - | - | OK |
| 510 | `data/tanzania_maps/TANZANIA_2022PHC_WARDS_SHAPEFILES.dbf` | `.dbf` | 2.809 | 4,344 | 17 | OK |
| 511 | `data/tanzania_maps/TANZANIA_2022PHC_WARDS_SHAPEFILES.prj` | `.prj` | 0.0 | - | - | OK |
| 512 | `data/tanzania_maps/TANZANIA_2022PHC_WARDS_SHAPEFILES.sbn` | `.sbn` | 0.044 | - | - | OK |
| 513 | `data/tanzania_maps/TANZANIA_2022PHC_WARDS_SHAPEFILES.sbx` | `.sbx` | 0.003 | - | - | OK |
| 514 | `data/tanzania_maps/TANZANIA_2022PHC_WARDS_SHAPEFILES.shp` | `.shp` | 17.2 | 4,344 | 0 | OK |
| 515 | `data/tanzania_maps/TANZANIA_2022PHC_WARDS_SHAPEFILES.shp.xml` | `.xml` | 0.011 | 2 | 1 | OK |
| 516 | `data/tanzania_maps/TANZANIA_2022PHC_WARDS_SHAPEFILES.shx` | `.shx` | 0.033 | - | - | OK |
| 517 | `data/tanzania_maps/tanzania_regions_2022phc.geojson` | `.geojson` | 0.407 | 31 | 2 | OK |