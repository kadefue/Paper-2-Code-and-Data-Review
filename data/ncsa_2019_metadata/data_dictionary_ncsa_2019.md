# NCSA 2019/2020 Small-Scale Farmers Data Dictionary

**Generated automatically from Stata binary `.dta` metadata.**

- **Total Tables / Files:** 56
- **Total Variables:** 925
- **Cumulative Observations:** 6,614,861

## Table of Contents

1. [R000_SOV.dta](#r000-sovdta) (137 vars, 30,650 rows)
2. [R031_HHRECORD.dta](#r031-hhrecorddta) (22 vars, 163,217 rows)
3. [R041_LAND_OWNERSHIP.dta](#r041-land-ownershipdta) (7 vars, 214,550 rows)
4. [R051_LAND_USE.dta](#r051-land-usedta) (7 vars, 398,450 rows)
5. [R062_FARMING_METHODS.dta](#r062-farming-methodsdta) (7 vars, 66,462 rows)
6. [R071_DISTANCE_TO_FIELDS.dta](#r071-distance-to-fieldsdta) (9 vars, 50,023 rows)
7. [R072_COMMUNIAL_RESOURCES.dta](#r072-communial-resourcesdta) (9 vars, 245,200 rows)
8. [R081_SHORT_RAINY_SEASON.dta](#r081-short-rainy-seasondta) (63 vars, 26,799 rows)
9. [R082_LONG_RAINY_SEASON.dta](#r082-long-rainy-seasondta) (63 vars, 53,278 rows)
10. [R083_PERMANENT_CROPS.dta](#r083-permanent-cropsdta) (61 vars, 23,138 rows)
11. [R102_AGROPROCESSING.dta](#r102-agroprocessingdta) (21 vars, 4,460 rows)
12. [R112_CROP_STORAGE.dta](#r112-crop-storagedta) (12 vars, 223,399 rows)
13. [R121_FARM_IMPLEMENTS.dta](#r121-farm-implementsdta) (8 vars, 490,400 rows)
14. [R122_USE_TRACTOR_ANIMALS.dta](#r122-use-tractor-animalsdta) (9 vars, 63,372 rows)
15. [R123_USE_ORGANIC_FERTILIZER.dta](#r123-use-organic-fertilizerdta) (8 vars, 13,028 rows)
16. [R124_ACCESS_FARM_INPUTS.dta](#r124-access-farm-inputsdta) (13 vars, 183,900 rows)
17. [R126_SOIL_EROSION.dta](#r126-soil-erosiondta) (9 vars, 25,544 rows)
18. [R141_EXTENSION_MESSAGES.dta](#r141-extension-messagesdta) (10 vars, 28,548 rows)
19. [R152_CATTLE_POPULATION.dta](#r152-cattle-populationdta) (11 vars, 61,369 rows)
20. [R153_CATTLE_INTAKE.dta](#r153-cattle-intakedta) (12 vars, 61,369 rows)
21. [R154_CATTLE_OFFTAKE.dta](#r154-cattle-offtakedta) (14 vars, 61,369 rows)
22. [R155_CATTLE_DISEASES.dta](#r155-cattle-diseasesdta) (14 vars, 78,903 rows)
23. [R157_CATTLE_MILK_PRODUCTION.dta](#r157-cattle-milk-productiondta) (14 vars, 19,208 rows)
24. [R162_GOAT_POPULATION.dta](#r162-goat-populationdta) (13 vars, 36,620 rows)
25. [R163_GOAT_INTAKE.dta](#r163-goat-intakedta) (12 vars, 36,620 rows)
26. [R164_GOAT_OFFTAKE.dta](#r164-goat-offtakedta) (14 vars, 36,620 rows)
27. [R165_GOAT_DISEASES.dta](#r165-goat-diseasesdta) (14 vars, 58,592 rows)
28. [R166_GOAT_MILK_PRODUCTION.dta](#r166-goat-milk-productiondta) (14 vars, 426 rows)
29. [R172_SHEEP_POPULATION.dta](#r172-sheep-populationdta) (11 vars, 15,335 rows)
30. [R173_SHEEP_INTAKE.dta](#r173-sheep-intakedta) (12 vars, 15,335 rows)
31. [R174_SHEEP_OFFTAKE.dta](#r174-sheep-offtakedta) (14 vars, 15,335 rows)
32. [R175_SHEEP_DISEASES.dta](#r175-sheep-diseasesdta) (14 vars, 24,536 rows)
33. [R182_PIG_POPULATION.dta](#r182-pig-populationdta) (8 vars, 11,544 rows)
34. [R183_PIG_INTAKE.dta](#r183-pig-intakedta) (12 vars, 11,544 rows)
35. [R184_PIG_OFFTAKE.dta](#r184-pig-offtakedta) (14 vars, 11,544 rows)
36. [R185_PIG_DISEASES.dta](#r185-pig-diseasesdta) (14 vars, 13,468 rows)
37. [R192_POULTRY_POPULATION.dta](#r192-poultry-populationdta) (11 vars, 108,744 rows)
38. [R193_POULTRY_DISEASES.dta](#r193-poultry-diseasesdta) (13 vars, 108,744 rows)
39. [R202_OTHER_LIVESTOCK_POP.dta](#r202-other-livestock-popdta) (11 vars, 30,252 rows)
40. [R203_OTHER_LIVESTOCK_PROD.dta](#r203-other-livestock-proddta) (11 vars, 153,160 rows)
41. [R210_OUTLET_SALES_LIVEST.dta](#r210-outlet-sales-livestdta) (12 vars, 31,436 rows)
42. [R220_LIVEST_STUCTURES_AC.dta](#r220-livest-stuctures-acdta) (10 vars, 459,750 rows)
43. [R241_LIVESTOCK_EXTENSION.dta](#r241-livestock-extensiondta) (11 vars, 18,438 rows)
44. [R250_LIVESTOCK_EXT_SERVICE.dta](#r250-livestock-ext-servicedta) (13 vars, 7,902 rows)
45. [R262_GOVT_REGULAT_CHALLENG.dta](#r262-govt-regulat-challengdta) (8 vars, 1,197 rows)
46. [R272_FISH_FARMING.dta](#r272-fish-farmingdta) (24 vars, 110 rows)
47. [R281_BEE_KEEPING.dta](#r281-bee-keepingdta) (13 vars, 878 rows)
48. [R291_LABOUR_USE.dta](#r291-labour-usedta) (8 vars, 858,200 rows)
49. [R301_SUBSTANCE_NONSUBST.dta](#r301-substance-nonsubstdta) (10 vars, 367,800 rows)
50. [R310_ACCESS_INFRASTUCTURE.dta](#r310-access-infrastucturedta) (7 vars, 429,100 rows)
51. [R311_OTHER_SERVICES.dta](#r311-other-servicesdta) (9 vars, 183,900 rows)
52. [R321_LIVELIHOOD_CNSTR_MOST.dta](#r321-livelihood-cnstr-mostdta) (8 vars, 92,245 rows)
53. [R330_MARKET_INFORMATION.dta](#r330-market-informationdta) (7 vars, 275,850 rows)
54. [R342_HOUSE_ASSETS.dta](#r342-house-assetsdta) (7 vars, 521,050 rows)
55. [R344_ACCESS_DRINKING_WATER.dta](#r344-access-drinking-waterdta) (9 vars, 61,300 rows)
56. [R346_FOOD_SECURITY.dta](#r346-food-securitydta) (17 vars, 30,650 rows)

---

## 1. R000_SOV.dta

- **File size:** 7.304 MB
- **Observations ($N$):** 30,650
- **Variables ($K$):** 137
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `q2_1` | 2.1 Type of Agricultural activities of  the household | `double` | `%22.0g` | 1 = Crops only; 2 = Livestock only; 3 = Fish farming; 4 = Pastoralist; 5 = Cr... |
| 6 | `q4_1_8` | 4.1.8 Total area (Land Access/Ownership) | `byte` | `%10.0g` |  |
| 7 | `q4_2` | 4.2 Was total land mentioned  (Qs 4.1) available to the household used  during a | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 8 | `q4_3` | 4.3 Do you Consider that you have sufficient agricultural land for your househol | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 9 | `q4_4` | 4.4 Do any Female Members of the Hh own or have customary right to agricultural | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 10 | `q4_5a` | 4.5 In what Region is the majority of Agricultural production? | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 11 | `q4_5b` | 4.5 In what District is the majority of Agricultural production? | `double` | `%8.0g` |  |
| 12 | `q5_1_13` | 5.1.13 Total Area (Land Use) | `int` | `%9.0g` |  |
| 13 | `q6_1` | 6.1 Does this household practice Conservational Farming? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 14 | `q8_1` | 8.1 Did the Hh plant any crops 2019/20 during Short Rainy Season? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 15 | `q8_2` | 8.2 Did the Hh plant any crop during 2019/20 Long Rainy Season? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 16 | `q8_3` | 8.3 Does your Household have any Permanent / Perennial Crops of Fruit Tree? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 17 | `q9_1` | 9.1 Did you use Secondary Products from any of your crops during the 2019/20 yea | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 18 | `q10_1` | 10.1 Did the household process any of the crops harvested on the farm during 201 | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 19 | `q11_1` | 11.1 Do  you currently have any crops in storage ? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 20 | `q12_2` | 12.2 Did you useTractors/Draft animals to cultivate? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 21 | `q12_3_1` | 12.3.1 Did you apply organic fertiliser during 2019/20? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 22 | `q12_5_1` | 12.5.1 Does the household practice irrigation? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 23 | `q12_6_1` | 12.6.1 Does the household have any erosion problem on their farming land ? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 24 | `q12_6_2` | 12.6.2 Does the household have any erosion control/water harvesting facilities | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 25 | `q13_1` | 13.1 During the year 2019/20 did any of the household members borrow money for a | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 26 | `q13_3` | 13.3 If the answer to question 13.1 above is 'NO' what is the main reason for no | `double` | `%35.0g` | 1 = Not needed; 2 = Not available; 3 = Did not want to go into debt; 4 = Inte... |
| 27 | `q14_1` | 14.1 Did your household receive any extension advice for crop production during | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 28 | `q14_2` | 14.2 Did the household or any member of the household participate in Out Grower | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 29 | `q14_3` | 14.3 Did the household or any member of the household participate in contracting | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 30 | `q15_1` | 15.1 Did the household own, raise or manage any CATTLE during 2019/20 agricultur | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 31 | `q15_2_8` | 15.2.8 Grand Total (CATTLE) | `long` | `%12.0g` |  |
| 32 | `q15_3_8` | 15.3.8 Total Intake (CATTLE) | `long` | `%12.0g` |  |
| 33 | `q15_4_8` | 15.4.8 Total Offtake (CATTLE) | `long` | `%12.0g` |  |
| 34 | `q15_6_1` | 15.6.1   Which method do you use to identify your cattle? | `double` | `%18.0g` | 1 = Branding; 2 = Cattle clan; 3 = Ear notching; 4 = Colour; 5 = Earings; 8 =... |
| 35 | `q15_7_1` | 15.7.1 Did the household produce any cattle milk during 2019/20 agriculture year | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 36 | `q16_1` | 16.1 Did the household own, raise or manage any GOATS during the 2019/20 agricul | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 37 | `q16_2_6` | 16.2.6 Grand Total (GOAT) | `long` | `%12.0g` |  |
| 38 | `q16_3_6` | 16.3.6 Total Intake (GOAT) | `long` | `%12.0g` |  |
| 39 | `q16_4_6` | 16.4.6 Total Offtake (GOAT) | `long` | `%12.0g` |  |
| 40 | `q16_6_1` | 16.6.1 Did the household produce any milk during 2019/20 agriculture year? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 41 | `q17_1` | 17.1 Did the household own, raise or manage any SHEEP during the 2019/20 agricul | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 42 | `q17_2_6` | 17.2.6 Grand Total (SHEEP) | `long` | `%12.0g` |  |
| 43 | `q17_3_6` | 17.3.6 Total Intake (SHEEP) | `long` | `%12.0g` |  |
| 44 | `q17_4_6` | 17.4.6 Total Offtake (SHEEP) | `long` | `%12.0g` |  |
| 45 | `q18_1` | 18.1 Did the household own, raise or manage any PIGS during the 2019/20 agricult | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 46 | `q18_2_6` | 18.2.6 Grand Total (PIG) | `long` | `%12.0g` |  |
| 47 | `q18_3_6` | 18.3.6 Total Intake (PIG) | `long` | `%12.0g` |  |
| 48 | `q18_4_6` | 18.4.6 Total Offtake (PIG) | `long` | `%12.0g` |  |
| 49 | `q19_1` | 19.1 Did the household own, raise or manage any POUTRY during the 2019/20 agricu | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 50 | `q20_1` | 20.1 Did the household own, raise or manage any OTHER LIVESTOCK during the 2019/ | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 51 | `q23_1` | 23.1 Did this household participate in any livestock pest and parasite control? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 52 | `q23_2` | 23.2 Did you deworm your animals during 2019/20? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 53 | `q23_3_1` | 23.3.1 Dewormed Cattles | `double` | `%17.0g` | 1 = Dewormed; 2 = NOT dewormed; 9 = Not Applicable |
| 54 | `q23_3_2` | 23.3.2 Dewormed Goats | `double` | `%17.0g` | 1 = Dewormed; 2 = NOT dewormed; 9 = Not Applicable |
| 55 | `q23_3_3` | 23.3.3 Dewormed Sheep | `double` | `%17.0g` | 1 = Dewormed; 2 = NOT dewormed; 9 = Not Applicable |
| 56 | `q23_3_4` | 23.3.4 Dewormed Pigs | `double` | `%17.0g` | 1 = Dewormed; 2 = NOT dewormed; 9 = Not Applicable |
| 57 | `q23_3_5` | 23.3.5 Dewormed Chicken | `double` | `%17.0g` | 1 = Dewormed; 2 = NOT dewormed; 9 = Not Applicable |
| 58 | `q23_4` | 23.4 Do you normally encounter a  tick problem? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 59 | `q23_5` | 23.5 Which methods of tick control did you use? | `double` | `%11.0g` | 1 = Dipping; 2 = Spraying; 3 = Smearing; 4 = None; 8 = Other |
| 60 | `q23_6` | 23.6 Do you normally encounter a  tsetse fly problem? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 61 | `q23_7` | 23.7 Which methods of control did you use? | `double` | `%11.0g` | 1 = Dipping; 2 = Spraying; 3 = Trapping; 4 = None; 8 = Other |
| 62 | `q23_8` | 23.8 Do you normally encounter a  Newcastle Disease problem on your chicken? if | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 63 | `q23_9` | 23.9 Which methods of control did you use? | `double` | `%21.0g` | 1 = Vaccination Method; 2 = Local Herbs; 3 = None; 8 = Others (Specify) |
| 64 | `q23_10` | 23.10 Do you normally encounter Fowl Typhoid problem on your chicken during 2019 | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 65 | `q23_11` | 23.11  Which methods of control did you use? | `double` | `%21.0g` | 1 = Vaccination Method; 2 = Local Herbs; 3 = None; 8 = Others (Specify) |
| 66 | `q23_12_1` | 23.12.1 Vacination on  Foot and mouth disease | `double` | `%17.0g` | 1 = Yes; 2 = No; 9 = Not applicable |
| 67 | `q23_12_2` | 23.12.2 Vacination on Lumpyskin | `double` | `%17.0g` | 1 = Yes; 2 = No; 9 = Not applicable |
| 68 | `q23_12_3` | 23.12.3 Vacination on Rabies | `double` | `%17.0g` | 1 = Yes; 2 = No; 9 = Not applicable |
| 69 | `q23_12_4` | 23.12.4 Vacination on Black Quarter | `double` | `%17.0g` | 1 = Yes; 2 = No; 9 = Not applicable |
| 70 | `q23_12_5` | 23.12.5 Vacination on  Anthranx | `double` | `%17.0g` | 1 = Yes; 2 = No; 9 = Not applicable |
| 71 | `q23_12_6` | 23.12.6 Vacination on CBPP | `double` | `%17.0g` | 1 = Yes; 2 = No; 9 = Not applicable |
| 72 | `q24_1` | 24.1 Did you receive any livestock extension advice? if no GO to section 26 | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 73 | `q26_1` | 26.1 Did you face problems with government regulations during 2019/20? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 74 | `q27_1` | 27.1 Was fish farming carried out by this household during 2019/20? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 75 | `q28_1` | 28.1 Did your household practised Bee keeping? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 76 | `q34_1_1` | 34.1.1 Roof | `double` | `%18.0g` | 1 = Iron Sheets; 2 = Tiles; 3 = Concrete; 4 = Asbestos; 5 = Grass/leaves; 6 =... |
| 77 | `q34_1_2` | 34.1.2 Floor | `double` | `%28.0g` | 1 = Earth, Sand, Dung; 2 = Wood Planks, Bamboo, Palm; 3 = Parquet Or Polished... |
| 78 | `q34_1_3` | 34.1.3 Walls | `double` | `%19.0g` | 1 = Grass; 2 = Poles And Mud; 3 = Sun-Dried Bricks; 4 = Baked Bricks; 5 = Woo... |
| 79 | `q34_1_4` | 34.1.4 Number of rooms | `double` | `%8.0g` |  |
| 80 | `q34_3_1` | 34.3.1 Main source of energy for Lighting | `double` | `%28.0g` | 1 = Mains electricity; 2 = Solar; 3 = Biogas; 4 = Hurricane Lamp; 5 = Pressur... |
| 81 | `q34_3_2` | 34.3.2 Main source of energy for Cooking | `double` | `%28.0g` | 1 = Mains electricity; 2 = Solar; 3 = Gas (hh biogas); 4 = Gas (Industrial); ... |
| 82 | `q34_5_1` | 34.5.1 What type of toilet does your household use? | `double` | `%38.0g` | 1 = No toilet/bush; 2 = Pit latrine without slab/Open pit; 3 = Pit latrine wi... |
| 83 | `q34_6_1` | 34.6.1 Number of meals the hh normally take per day | `double` | `%8.0g` |  |
| 84 | `q34_6_2` | 34.6.2 Number of days hh consumed meat in the last seven days | `double` | `%8.0g` |  |
| 85 | `q34_6_3` | 34.6.3 Number of days hh consumed Fish in the last seven days | `double` | `%8.0g` |  |
| 86 | `q34_6_4` | 34.6.4 How often did the hh had problems in satisfying the food needs of the hh | `double` | `%12.0g` | 1 = Never; 2 = Seldom; 3 = Sometimes; 4 = Often; 5 = Always |
| 87 | `q34_7_1` | 34.7.1 What is the household main source of cash income? | `double` | `%30.0g` | 1 = Sale of food crops; 2 = Sale of Livestock; 3 = Sale of livestock products... |
| 88 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 89 | `livestock_wgt` | Livestock Weight | `byte` | `%10.0g` |  |
| 90 | `fish_weights` | Fish weights | `byte` | `%10.0g` |  |
| 91 | `cattle_weigts` | Cattle Weigts | `byte` | `%10.0g` |  |
| 92 | `q1252c1` | Main Source of Irrigation Water | `double` | `%17.0g` | 1 = River; 2 = Lake; 3 = Dam; 4 = Well; 5 = Borehole; 6 = Canal; 7 = Tap Wate... |
| 93 | `q1252c2` | Main method of  Obtaining Water | `double` | `%18.0g` | 1 = Gravity; 2 = Hand bucket; 3 = Hand pump; 4 = Motor pump; 5 = Drip; 6 = Sp... |
| 94 | `q1252c3` | Irrigatable Area (Acrea) | `int` | `%9.0g` |  |
| 95 | `q1252c4` | Area of irrigated Land agriculture year 2019/20 (acres) | `int` | `%9.0g` |  |
| 96 | `q132_1c1_use_credit_source_a` | Use of credit (source a) | `double` | `%29.0g` | 1 = Family, friend or relative; 2 = Bank; 3 = Cooperative; 4 = Savings & cred... |
| 97 | `q132_1c2_provided_to_source_a` | provided to (a) | `double` | `%9.0g` | 1 = Male; 2 = Female |
| 98 | `q132_1_labour_source_a` | Labour (a) | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 99 | `q132_2_seeds_source_a` | Seeds(a) | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 100 | `q132_3_fertilzers_source_a` | Fertilizers(a) | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 101 | `q132_4_agrochemicals_source_a` | Agrochemicals (a) | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 102 | `q132_5_tools_source__a` | Tools/Equipments(a) | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 103 | `q132_6_irrigation_source_a` | Irrigation Structures (a) | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 104 | `q132_7_fish_farming_source_a` | Fish farming (a) | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 105 | `q132_8_beekeeping_source_a` | Bee keeping (a) | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 106 | `q132_9_livestock_source_a` | Livestock (a) | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 107 | `q132_10_other_source_a` | Other (a) | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 108 | `q132_11_credit_tshs_source_a` | Value of credit(Tshs) (a) | `long` | `%12.0g` |  |
| 109 | `q132_12_payment_tshs_source_a` | Value of Payment(Tshs) (a) | `long` | `%12.0g` |  |
| 110 | `q132_1c1_use_credit_source_b` | Use of credit (source b) | `double` | `%29.0g` | 1 = Family, friend or relative; 2 = Bank; 3 = Cooperative; 4 = Savings & cred... |
| 111 | `q132_1c2_provided_to_source_b` | provided to (b) | `double` | `%9.0g` | 1 = Male; 2 = Female |
| 112 | `q132_1_labour_source_b` | Labour (b) | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 113 | `q132_2_seeds_source_b` | Seeds(b) | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 114 | `q132_3_fertilzers_source_b` | Fertilizers(b) | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 115 | `q132_4_agrochemicals_source_b` | Agrochemicals (b) | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 116 | `q132_5_tools_source_b` | Tools/Equipments(b) | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 117 | `q132_6_irrigation_source_b` | Irrigation Structures (b) | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 118 | `q132_7_fish_farming_source_b` | Fish farming (b) | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 119 | `q132_8_beekeeping_source_b` | Bee keeping (b) | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 120 | `q132_9_livestock_source_b` | Livestock (b) | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 121 | `q132_10_other_source_b` | Other (b) | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 122 | `q132_11_credit_tshs_source_b` | Value of credit(Tshs) (b) | `long` | `%12.0g` |  |
| 123 | `q132_12_payment_tshs_source_b` | Value of Payment(Tshs) (b) | `long` | `%12.0g` |  |
| 124 | `q132_1c1_use_credit_source_c` | Use of credit (source c) | `double` | `%29.0g` | 1 = Family, friend or relative; 2 = Bank; 3 = Cooperative; 4 = Savings & cred... |
| 125 | `q132_1c2_provided_to_source_c` | provided to (c) | `double` | `%9.0g` | 1 = Male; 2 = Female |
| 126 | `q132_1_labour_source_c` | Labour (c) | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 127 | `q132_2_seeds_source_c` | Seeds(c) | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 128 | `q132_3_fertilzers_source_c` | Fertilizers(c) | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 129 | `q132_4_agrochemicals_source_c` | Agrochemicals (c) | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 130 | `q132_5_tools_source_c` | Tools/Equipments(c) | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 131 | `q132_6_irrigation_source_c` | Irrigation Structures (c) | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 132 | `q132_7_fish_farming_source_c` | Fish farming (c) | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 133 | `q132_8_beekeeping_source_c` | Bee keeping (c) | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 134 | `q132_9_livestock_source_c` | Livestock (c) | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 135 | `q132_10_other_source_c` | Other (c) | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 136 | `q132_11_credit_tshs_source_c` | Value of credit(Tshs) (c) | `long` | `%12.0g` |  |
| 137 | `q132_12_payment_tshs_source_c` | Value of Payment(Tshs) (c) | `long` | `%12.0g` |  |


## 2. R031_HHRECORD.dta

- **File size:** 6.252 MB
- **Observations ($N$):** 163,217
- **Variables ($K$):** 22
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `q3_1c0` | Q3(0) Serial Number | `double` | `%8.0g` |  |
| 7 | `q3_1c2` | Q3(2) What is the relationship of (NAME) to the head of the household ? | `double` | `%25.0g` | 1 = Head of household; 2 = Spouse; 3 = Son/daughter; 4 = Father/Mother; 5 = G... |
| 8 | `q3_1c3` | Q3(3) Is (NAME) male or female? | `double` | `%9.0g` | 1 = Male; 2 = Female |
| 9 | `q3_1c4` | Q3(4) How old is (NAME) ? | `double` | `%8.0g` |  |
| 10 | `q3_1c5` | Q3(5) Is (NAME) 's biological mother alive? | `double` | `%13.0g` | 1 = Yes; 2 = No; 3 = Don't know |
| 11 | `q3_1c6` | Q3(6) Is (NAME) 's biological father alive? | `double` | `%13.0g` | 1 = Yes; 2 = No; 3 = Don't know |
| 12 | `q3_1c7` | Q3(7) Does (NAME) knows how to read and write in english or kiswahili or both? | `double` | `%21.0g` | 1 = Swahili; 2 = English; 3 = Swahili & English; 4 = Any other language; 5 = ... |
| 13 | `q3_1c8` | Q3(8) What is the schooling status of (NAME)? | `double` | `%24.0g` | 1 = Attending School; 2 = Drop out; 3 = Completed; 4 = Never attended School |
| 14 | `q3_1c9` | Q3(9) What is the highest level of school (NAME) has reached? | `double` | `%41.0g` | 0 = Under Standard One; 1 = Standard One; 2 = Standard Two; 3 = Standard Thre... |
| 15 | `q3_1c10` | Q3(10) How involved is (NAME)    in farming activities ? | `double` | `%26.0g` | 1 = Works full time on farm; 2 = Works part-time on farm; 3 = Rarely works on... |
| 16 | `q3_1c11` | Q3(11) What is the main activity of (NAME) ? | `double` | `%49.0g` | 1 = Crop Farming; 2 = Livestock Keeping/Herding; 3 = Livestock/Pastoralism; 4... |
| 17 | `q3_1c12` | Q3(12) Is  (NAME)  involved in value addition? | `double` | `%17.0g` | 1 = Yes; 2 = No; 9 = Not applicable |
| 18 | `q3_1c13` | Q3(13) Does (NAME) own any piece of agricultural land ? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 19 | `q3_1c14` | Q3(14) Does (NAME) have a Title deed of the agricultural land ? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 20 | `q3_1c15` | Q3(15) What Type of Tenure does [NAME] have on the agricultural land? | `double` | `%83.0g` | 1 = Customary Right of Occupancy With certificate of customary right of occup... |
| 21 | `q3_1c16` | Q3(16) Is (NAME) a member of co-operative or  farmers organization or both? | `double` | `%28.0g` | 1 = Yes, Cooperative; 2 = Yes, Farmers Organisation; 3 = Yes, Both; 4 = No; 9... |
| 22 | `q3_1c17` | Q3(17) Does (NAME) generates any off-farm income? | `double` | `%8.0g` | 1 = Yes; 2 = No |


## 3. R041_LAND_OWNERSHIP.dta

- **File size:** 5.742 MB
- **Observations ($N$):** 214,550
- **Variables ($K$):** 7
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `q4_1_c0` | 4.1 Land Access SN | `double` | `%39.0g` | 1 = Land Leased/Certificate of ownership; 2 = Land owned under Customary Law;... |
| 7 | `q4_1_c2` | 4.1 Area in Acres | `int` | `%9.0g` |  |


## 4. R051_LAND_USE.dta

- **File size:** 10.652 MB
- **Observations ($N$):** 398,450
- **Variables ($K$):** 7
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `q5_1_c0` | 5.1 Land Use S/N | `double` | `%54.0g` | 1 = Area under Temporary Mono Crops; 2 = Area under Temporary Mixed Crops; 3 ... |
| 7 | `q5_1_c2` | 5.1 Area in Acres | `int` | `%9.0g` |  |


## 5. R062_FARMING_METHODS.dta

- **File size:** 1.597 MB
- **Observations ($N$):** 66,462
- **Variables ($K$):** 7
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `q6_2c0` | 6.2 S/N | `double` | `%63.0g` | 1 = Contour farming (for sloped lands); 2 = Planting of legumes and other soi... |
| 7 | `q6_2c2` | 6.2 Yes/No | `double` | `%8.0g` | 1 = Yes; 2 = No |


## 6. R071_DISTANCE_TO_FIELDS.dta

- **File size:** 1.303 MB
- **Observations ($N$):** 50,023
- **Variables ($K$):** 9
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `q7_1c1` | 7.1 Field Number | `double` | `%8.0g` |  |
| 7 | `q7_1c2` | 7.1 Distance to Homestead | `double` | `%23.0g` | 1 = less than 100m; 2 = between 100 and 300m; 3 = between 300 and 500m; 4 = b... |
| 8 | `q7_1c3` | 7.1 Distance to Nearest road | `double` | `%23.0g` | 1 = less than 100m; 2 = between 100 and 300m; 3 = between 300 and 500m; 4 = b... |
| 9 | `q7_1c4` | 7.1 Distance to Nearest Market | `double` | `%23.0g` | 1 = less than 100m; 2 = between 100 and 300m; 3 = between 300 and 500m; 4 = b... |


## 7. R072_COMMUNIAL_RESOURCES.dta

- **File size:** 7.731 MB
- **Observations ($N$):** 245,200
- **Variables ($K$):** 9
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `q7_2_c0` | 7.2 S/N | `double` | `%26.0g` | 1 = Water for domestic use; 2 = Water for livestock; 3 = Communal Grazing; 4 ... |
| 7 | `q7_2_c2` | 7.2. Distance (Dry Season) | `int` | `%19.0g` | 999 = Not applicable |
| 8 | `q7_2_c3` | 7.2 Distance (Wet Season) | `int` | `%19.0g` | 999 = Not applicable |
| 9 | `q7_2_c4` | 7.2 Main Hh in Use | `double` | `%39.0g` | 1 = Home or farm Consumption/utilisation; 2 = Sold to Neighbours; 3 = Sold to... |


## 8. R081_SHORT_RAINY_SEASON.dta

- **File size:** 7.132 MB
- **Observations ($N$):** 26,799
- **Variables ($K$):** 63
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%16.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%30.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `ward_shehia` | Ward/Shehia | `float` | `%8.0g` |  |
| 4 | `village` | Village | `double` | `%8.0g` |  |
| 5 | `ea` | EA | `float` | `%8.0g` |  |
| 6 | `rural_urban` | Rural_Urban | `double` | `%8.0g` | 1 = Rural; 2 = Urban |
| 7 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 8 | `q811c1` | Field number | `double` | `%8.0g` |  |
| 9 | `q811c2` | Total Field Area (Acres) | `byte` | `%10.0g` |  |
| 10 | `q811c3` | Plot | `double` | `%8.0g` |  |
| 11 | `q811c4` | Crop Code | `float` | `%19.0g` | 11 = Maize; 12 = Paddy; 13 = Sorghum; 14 = Bulrush Millet; 15 = Finger Millet... |
| 12 | `q811c5` | Crop Name | `str30` | `%30s` |  |
| 13 | `q811c6` | Land preparation costs (TZS) | `long` | `%12.0g` |  |
| 14 | `q811c7a` | Planted area (Acres) | `byte` | `%10.0g` |  |
| 15 | `q811c7b` | Planting costs (TZS) | `long` | `%12.0g` |  |
| 16 | `q811c8a` | Was this (CROP) irrigated? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 17 | `q811c8b` | Area Irrigated (Acres) | `byte` | `%10.0g` |  |
| 18 | `q811c8c` | Main Source of Water for Irrigation | `double` | `%14.0g` | 1 = River; 2 = Lake; 3 = Dam; 4 = Well; 5 = Borehole; 6 = Canal; 7 = Tap Wate... |
| 19 | `q811c8d` | Method of irrigation | `double` | `%15.0g` | 1 = Gravity; 2 = Bucket; 3 = Hand/leg pump; 4 = Water pump; 5 = Drip irrigati... |
| 20 | `q811c8e` | Irrigation costs | `long` | `%12.0g` |  |
| 21 | `q811c8f` | Weeding costs (TZS) | `long` | `%12.0g` |  |
| 22 | `q811c9a` | Harvested Area (Acres) | `byte` | `%10.0g` |  |
| 23 | `q811c9b` | Quantity Harvested | `byte` | `%10.0g` |  |
| 24 | `q811c9c` | Unit | `double` | `%11.0g` | 1 = Bags; 2 = Bunch; 3 = Tins/Bucket; 4 = Number; 5 = Kilogram |
| 25 | `q811c9d` | Kg/Unit | `byte` | `%10.0g` |  |
| 26 | `q811c9e` | Total Kg | `byte` | `%10.0g` |  |
| 27 | `q811c9f` | Harvesting Costs(TZS) | `long` | `%12.0g` |  |
| 28 | `q811c9g` | Reasons for not harvesting | `double` | `%23.0g` | 1 = Crops not harvested yet; 2 = Drought; 3 = Rain/flood damage; 4 = Fire dam... |
| 29 | `q811c10a` | Quantity Stored (kgs) | `byte` | `%10.0g` |  |
| 30 | `q811c10b` | Method of Storage | `double` | `%37.0g` | 1 = In locally made traditional structure; 2 = In Improved locally made struc... |
| 31 | `q811c10c` | Transport cost from farm to storage place | `long` | `%12.0g` |  |
| 32 | `q811c11` | What type of seed was used for this [CROP]? | `double` | `%29.0g` | 1 = Local seed; 2 = Improved seed; 3 = Both Local and Improved seeds |
| 33 | `q811c12` | What was the area [COL 11] planted with  Seed? | `byte` | `%10.0g` |  |
| 34 | `q811c13` | Quantity of improved Seeds Unit | `double` | `%9.0g` | 1 = Kilogram; 2 = Seedlings; 3 = Cuttings |
| 35 | `q811c14` | Seeds Quantity used | `byte` | `%10.0g` |  |
| 36 | `q811c15` | Seeds Cost (Tshs) | `long` | `%12.0g` |  |
| 37 | `q811c16` | Did you use Fertilizer for this [CROP]? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 38 | `q811c17` | Area Applied with Fertilizer | `byte` | `%10.0g` |  |
| 39 | `q811c18` | Type of Fertilizer Used | `double` | `%9.0g` | 1 = Inorganic; 2 = Organic |
| 40 | `q811c19a` | Fertilizer Unit | `double` | `%8.0g` | 1 = Kilogram; 2 = Litre |
| 41 | `q811c19b` | Fertilizer Quantity (kg) | `byte` | `%10.0g` |  |
| 42 | `q811c20` | Fertilizer Cost (TZS) | `long` | `%12.0g` |  |
| 43 | `q811c21` | Did you use Herbicides for this [CROP]? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 44 | `q811c22` | Area Applied with Herbicides | `byte` | `%10.0g` |  |
| 45 | `q811c23` | Herbicides Unit | `double` | `%8.0g` | 1 = Kilogram; 2 = Litre |
| 46 | `q811c24` | Herbicides Quantity used | `byte` | `%10.0g` |  |
| 47 | `q811c25` | Herbicides Cost (TZS) | `long` | `%12.0g` |  |
| 48 | `q811c26` | Did you use Fungicides for this [CROP]? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 49 | `q811c27` | Area Applied with Fungicides | `byte` | `%10.0g` |  |
| 50 | `q811c28` | Fungicides Unit | `double` | `%8.0g` | 1 = Kilogram; 2 = Litre |
| 51 | `q811c29` | Fungicides Quantity used | `byte` | `%10.0g` |  |
| 52 | `q811c30` | Fungicides Cost (TZS) | `long` | `%12.0g` |  |
| 53 | `q811c31` | Did you use insectcides (Pesticides) for this [CROP]? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 54 | `q811c32` | Area Applied with Insectides | `byte` | `%10.0g` |  |
| 55 | `q811c33` | Insecticides Unit | `double` | `%8.0g` | 1 = Kilogram; 2 = Litre |
| 56 | `q811c34` | Insecticides Quantity used | `byte` | `%10.0g` |  |
| 57 | `q811c35` | Insecticides Cost (TZS) | `long` | `%12.0g` |  |
| 58 | `q811c36` | Any other Costs | `long` | `%12.0g` |  |
| 59 | `q811c37` | Did you sell the harvested [CROP]? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 60 | `q811c38` | Quantity Sold (Kgs) | `byte` | `%10.0g` |  |
| 61 | `q811c39` | Average price (TZS) per Kg | `long` | `%12.0g` |  |
| 62 | `q811c40` | Reason for not selling | `double` | `%21.0g` | 1 = Low market price; 2 = Household consumption; 98 = Other; 99 = Not Applicable |
| 63 | `q811c41` | Marketing challenges | `double` | `%36.0g` | 1 = Low market price; 2 = No transport; 3 = Transport cost too high; 4 = No b... |


## 9. R082_LONG_RAINY_SEASON.dta

- **File size:** 14.127 MB
- **Observations ($N$):** 53,278
- **Variables ($K$):** 63
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%16.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%30.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `ward_shehia` | Ward/Shehia | `float` | `%8.0g` |  |
| 4 | `village` | Village | `double` | `%8.0g` |  |
| 5 | `ea` | EA | `float` | `%8.0g` |  |
| 6 | `rural_urban` | Rural_Urban | `double` | `%8.0g` | 1 = Rural; 2 = Urban |
| 7 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 8 | `q821c1` | Field number | `double` | `%8.0g` |  |
| 9 | `q821c2` | Total Field Area (Acres) | `byte` | `%10.0g` |  |
| 10 | `q821c3` | Plot | `double` | `%8.0g` |  |
| 11 | `q821c4` | Crop Code | `float` | `%19.0g` | 11 = Maize; 12 = Paddy; 13 = Sorghum; 14 = Bulrush Millet; 15 = Finger Millet... |
| 12 | `q821c5` | Crop Name | `str30` | `%30s` |  |
| 13 | `q821c6` | Land preparation costs (TZS) | `long` | `%12.0g` |  |
| 14 | `q821c7a` | Planted area (Acres) | `byte` | `%10.0g` |  |
| 15 | `q821c7b` | Planting costs (TZS) | `long` | `%12.0g` |  |
| 16 | `q821c8a` | Was this (CROP) irrigated? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 17 | `q821c8b` | Area Irrigated (Acres) | `byte` | `%10.0g` |  |
| 18 | `q821c8c` | Source of Water for rrigation | `double` | `%14.0g` | 1 = River; 2 = Lake; 3 = Dam; 4 = Well; 5 = Borehole; 6 = Canal; 7 = Tap Wate... |
| 19 | `q821c8d` | Method of irrigation | `double` | `%16.0g` | 1 = Gravity; 2 = Bucket; 3 = Hand/leg pump; 4 = Motor Water pump; 5 = Drip ir... |
| 20 | `q821c8e` | Irrigation costs | `long` | `%12.0g` |  |
| 21 | `q821c8f` | Weeding costs (TZS) | `long` | `%12.0g` |  |
| 22 | `q821c9a` | Harvested Area (Acres) | `byte` | `%10.0g` |  |
| 23 | `q821c9b` | Quantity Harvested | `byte` | `%10.0g` |  |
| 24 | `q821c9c` | Unit | `double` | `%11.0g` | 1 = Bags; 2 = Bunch; 3 = Tins/Bucket; 4 = Number; 5 = Kilogram |
| 25 | `q821c9d` | Kg/Unit | `byte` | `%10.0g` |  |
| 26 | `q821c9e` | Total Kg | `byte` | `%10.0g` |  |
| 27 | `q821c9f` | Harvesting Costs(TZS) | `long` | `%12.0g` |  |
| 28 | `q821c9g` | Reasons for not harvesting | `double` | `%23.0g` | 1 = Crops not harvested yet; 2 = Drought; 3 = Rain/flood damage; 4 = Fire dam... |
| 29 | `q821c10a` | Quantity Stored (kgs) | `byte` | `%10.0g` |  |
| 30 | `q821c10b` | Method of Storage | `double` | `%37.0g` | 1 = In locally made traditional structure; 2 = In Improved locally made struc... |
| 31 | `q821c10c` | Transport Costs from farm to storage | `long` | `%12.0g` |  |
| 32 | `q821c11` | What type of seed was used for this [CROP]? | `double` | `%29.0g` | 1 = Local seed; 2 = Improved seed; 3 = Both Local and Improved seeds |
| 33 | `q821c12` | What was the area [COL 11] planted with  Seed? | `byte` | `%10.0g` |  |
| 34 | `q821c13` | Quantity of Improved Seeds Unit | `double` | `%9.0g` | 1 = Kilogram; 2 = Seedlings; 3 = Cuttings |
| 35 | `q821c14` | Seeds Quantity used | `byte` | `%10.0g` |  |
| 36 | `q821c15` | Seeds Cost (Tshs) | `long` | `%12.0g` |  |
| 37 | `q821c16` | Did you use fertilizer for this [CROP]? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 38 | `q821c17` | Area Applied with Fertilizer | `byte` | `%10.0g` |  |
| 39 | `q821c18` | Type of Fertilizer Used | `double` | `%9.0g` | 1 = Inorganic; 2 = Organic |
| 40 | `q821c19a` | Fertilizer Unit | `double` | `%8.0g` | 1 = Kilogram; 2 = Litre |
| 41 | `q821c19b` | Fertilizer Quantity (kg) | `byte` | `%10.0g` |  |
| 42 | `q821c20` | Fertilizer Cost (TZS) | `long` | `%12.0g` |  |
| 43 | `q821c21` | Did you use Herbicides for this [CROP]? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 44 | `q821c22` | Area Applied with Herbicides | `byte` | `%10.0g` |  |
| 45 | `q821c23` | Herbicides Unit | `double` | `%8.0g` | 1 = Kilogram; 2 = Litre |
| 46 | `q821c24` | Herbicides Quantity used | `byte` | `%10.0g` |  |
| 47 | `q821c25` | Herbicides Cost (TZS) | `long` | `%12.0g` |  |
| 48 | `q821c26` | Did you use fungicides for this [CROP]? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 49 | `q821c27` | Area Applied with Fungicides | `byte` | `%10.0g` |  |
| 50 | `q821c28` | Fungicides Unit | `double` | `%8.0g` | 1 = Kilogram; 2 = Litre |
| 51 | `q821c29` | Fungicides Quantity used | `byte` | `%10.0g` |  |
| 52 | `q821c30` | Fungicides Cost (TZS) | `long` | `%12.0g` |  |
| 53 | `q821c31` | Did you use insectcides (Pesticides) for this [CROP]? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 54 | `q821c32` | Area Applied with Insectides | `byte` | `%10.0g` |  |
| 55 | `q821c33` | Insecticides Unit | `double` | `%8.0g` | 1 = Kilogram; 2 = Litre |
| 56 | `q821c34` | Insecticides Quantity used | `byte` | `%10.0g` |  |
| 57 | `q821c35` | Insecticides Cost (TZS) | `long` | `%12.0g` |  |
| 58 | `q821c36` | Any other Costs | `long` | `%12.0g` |  |
| 59 | `q821c37` | Did you sell the harvested [CROP]? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 60 | `q821c38` | Quantity Sold (Kgs) | `byte` | `%10.0g` |  |
| 61 | `q821c39` | Average price (TZS) per Kg | `long` | `%12.0g` |  |
| 62 | `q821c40` | Reason for not selling | `double` | `%21.0g` | 1 = Low market price; 2 = Household consumption; 98 = Other (specify); 99 = N... |
| 63 | `q821c41` | Marketing challenges | `double` | `%36.0g` | 1 = Low market price; 2 = No transport; 3 = Transport cost too high; 4 = No b... |


## 10. R083_PERMANENT_CROPS.dta

- **File size:** 6.075 MB
- **Observations ($N$):** 23,138
- **Variables ($K$):** 61
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%16.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%30.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `ward_shehia` | Ward/Shehia | `float` | `%8.0g` |  |
| 4 | `village` | Village | `double` | `%8.0g` |  |
| 5 | `ea` | EA | `float` | `%8.0g` |  |
| 6 | `rural_urban` | Rural_Urban | `double` | `%8.0g` | 1 = Rural; 2 = Urban |
| 7 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 8 | `q831c1` | Field number | `double` | `%8.0g` |  |
| 9 | `q831c2` | Total Field Area (Acres) | `byte` | `%10.0g` |  |
| 10 | `q831c3` | Plot | `double` | `%8.0g` |  |
| 11 | `q831c4` | Permanent Crop Code | `float` | `%19.0g` | 11 = Maize; 12 = Paddy; 13 = Sorghum; 14 = Bulrush Millet; 15 = Finger Millet... |
| 12 | `q831c5` | Permanent  Crop Name | `str30` | `%30s` |  |
| 13 | `q831c6` | Area of Plants in MONO CROP (acres) | `byte` | `%10.0g` |  |
| 14 | `q831c7` | Area covered by permanent crop in MIXED CROP (acres) | `byte` | `%10.0g` |  |
| 15 | `q831c8a` | Was this (CROP) irrigated  in 2019/20 Agriculture year? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 16 | `q831c8b` | Area Irrigated | `byte` | `%10.0g` |  |
| 17 | `q831c8c` | Source of Water for Irrigation | `double` | `%14.0g` | 1 = River; 2 = Lake; 3 = Dam; 4 = Well; 5 = Borehole; 6 = Canal; 7 = Tap Wate... |
| 18 | `q831c8d` | Method of Irrigation | `double` | `%16.0g` | 1 = Gravity; 2 = Bucket; 3 = Hand/leg pump; 4 = Motor Water pump; 5 = Drip ir... |
| 19 | `q831c8e` | Irrigation Costs | `long` | `%12.0g` |  |
| 20 | `q831c9a` | Area Harvested (Acres) | `byte` | `%10.0g` |  |
| 21 | `q831c9b` | Quantity Harvested(kgs) | `byte` | `%10.0g` |  |
| 22 | `q831c9c` | Unit | `double` | `%11.0g` | 1 = Bags; 2 = Bunch; 3 = Tins/Bucket; 4 = Number; 5 = Kilogram |
| 23 | `q831c9d` | Harvested (Kg/Unit) | `byte` | `%10.0g` |  |
| 24 | `q831c9e` | Total Kgs | `byte` | `%10.0g` |  |
| 25 | `q831c9f` | Harvesting Cost (TZS) | `long` | `%12.0g` |  |
| 26 | `q831c9g` | Reasons for not harvesting | `double` | `%23.0g` | 1 = Crops not harvested yet; 2 = Drought; 3 = Rain/flood damage; 4 = Fire dam... |
| 27 | `q831c10a` | Quantity Stored | `byte` | `%10.0g` |  |
| 28 | `q831c10b` | Method of Storage | `double` | `%37.0g` | 1 = In locally made traditional structure; 2 = In Improved locally made struc... |
| 29 | `q831c10c` | Number of Mature Trees | `long` | `%12.0g` |  |
| 30 | `q831c11` | What type of seed was used for this [CROP]? | `double` | `%29.0g` | 1 = Local seed; 2 = Improved seed; 3 = Both Local and Improved seeds |
| 31 | `q831c12` | What was the area planted with   seed/ seedling ? | `byte` | `%10.0g` |  |
| 32 | `q831c13` | Seeds use Unit | `double` | `%9.0g` | 1 = Kilogram; 2 = Seedlings; 3 = Cuttings |
| 33 | `q831c14` | Seeds Quantity used | `byte` | `%10.0g` |  |
| 34 | `q831c15` | Cost of Seeds (TZS) | `long` | `%12.0g` |  |
| 35 | `q831c16` | Did you use fertilizer for this [CROP]? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 36 | `q831c17` | Fertilizer Area Applied | `byte` | `%10.0g` |  |
| 37 | `q831c18` | Type of Fertilizer Used | `double` | `%9.0g` | 1 = Inorganic; 2 = Organic |
| 38 | `q831c19a` | Fertilizer Unit | `double` | `%8.0g` | 1 = Kilogram; 2 = Litre |
| 39 | `q831c19b` | Fertilizer Use Quantity (kg) | `byte` | `%10.0g` |  |
| 40 | `q831c20` | Fertilizer Cost (TZS) | `long` | `%12.0g` |  |
| 41 | `q831c21` | Did you use Herbicides for this [CROP]? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 42 | `q831c22` | Herbicides Area Applied | `byte` | `%10.0g` |  |
| 43 | `q831c23` | Herbicides Quantity Unit | `double` | `%8.0g` | 1 = Kilogram; 2 = Litre |
| 44 | `q831c24` | Herbicides Quantity used | `byte` | `%10.0g` |  |
| 45 | `q831c25` | Herbicides Cost (TZS) | `long` | `%12.0g` |  |
| 46 | `q831c26` | Did you use fungicides for this [CROP]? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 47 | `q831c27` | Fungicides Area Applied | `byte` | `%10.0g` |  |
| 48 | `q831c28` | Fungicides use Unit | `double` | `%8.0g` | 1 = Kilogram; 2 = Litre |
| 49 | `q831c29` | Fungicides Quantity used | `byte` | `%10.0g` |  |
| 50 | `q831c30` | Fungicides Cost (TZS) | `long` | `%12.0g` |  |
| 51 | `q831c31` | Did you use insecticides for this [CROP]? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 52 | `q831c32` | Insecticides Use Area Applied | `byte` | `%10.0g` |  |
| 53 | `q831c33` | Insecticides use Unit | `double` | `%8.0g` | 1 = Kilogram; 2 = Litre |
| 54 | `q831c34` | Insecticides Quantity used | `byte` | `%10.0g` |  |
| 55 | `q831c35` | Insecticides Cost (TZS) | `long` | `%12.0g` |  |
| 56 | `q831c36` | Any Other costs | `long` | `%12.0g` |  |
| 57 | `q831c37` | Did you sell the crop? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 58 | `q831c38` | Quantity Sold (kgs) | `byte` | `%10.0g` |  |
| 59 | `q831c39` | Average Price/Kg (TZS) | `long` | `%12.0g` |  |
| 60 | `q831c40` | Reason for not selling | `double` | `%21.0g` | 1 = Low market price; 2 = Household consumption; 98 = Other (specify); 99 = N... |
| 61 | `q831c41` | Marketing challenges | `double` | `%36.0g` | 1 = Low market price; 2 = No transport; 3 = Transport cost too high; 4 = No b... |


## 11. R102_AGROPROCESSING.dta

- **File size:** 0.272 MB
- **Observations ($N$):** 4,460
- **Variables ($K$):** 21
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `q102c1` | Crop code | `float` | `%24.0g` | 11 = Maize; 12 = Paddy; 13 = Sorghum; 14 = Bulrush Millet; 15 = Finger Millet... |
| 7 | `q102c3` | Where Processed | `double` | `%25.0g` | 1 = On farm by hand; 2 = On farm by machine; 3 = By neighbours machine; 4 = B... |
| 8 | `q102c4` | Main Product code | `double` | `%17.0g` | 1 = Flour/meal; 2 = Grain; 3 = Oil; 4 = Juice; 5 = Fiber; 6 = Pulp; 7 = Sheet... |
| 9 | `q102c5` | Used for | `double` | `%24.0g` | 1 = Household consumption; 2 = Fuel for cooking; 3 = Selling; 4 = Animal cons... |
| 10 | `q102c6` | Quantity of Main product | `long` | `%12.0g` |  |
| 11 | `q102c7` | Unit | `double` | `%24.0g` | 1 = Loose bundle/bunch; 2 = Compressed bunch/bail; 3 = Tin; 4 = Bucket; 5 = K... |
| 12 | `q102c8` | KG/Litre unit | `int` | `%9.0g` |  |
| 13 | `q102c9` | Main type of packaging | `double` | `%21.0g` | 1 = Leno bags; 2 = Sacks; 3 = Box; 4 = Hermetic bags; 5 = Plastic containers;... |
| 14 | `q102c10` | Quantity Sold of Main product | `long` | `%12.0g` |  |
| 15 | `q102c11` | Where sold | `double` | `%27.0g` | 1 = Neighbour; 2 = Local market/trade store; 3 = Secondary Market; 4 = Market... |
| 16 | `q102c12` | By product code | `double` | `%20.0g` | 1 = Bran; 2 = Cake; 3 = Husk; 4 = Juice; 5 = Fiber; 6 = Pulp; 7 = Oil; 8 = Sh... |
| 17 | `q102c13` | Used for | `double` | `%24.0g` | 1 = Household consumption; 2 = Fuel for cooking; 3 = Selling; 4 = Animal cons... |
| 18 | `q102c14` | Unit | `double` | `%24.0g` | 1 = Loose bundle/bunch; 2 = Compressed bunch/bail; 3 = Tin; 4 = Bucket; 5 = K... |
| 19 | `q102c15` | Quantity of by product | `long` | `%12.0g` |  |
| 20 | `q102c16` | KG/Unit | `int` | `%9.0g` |  |
| 21 | `q102c17` | Quantity sold (By product) | `long` | `%12.0g` |  |


## 12. R112_CROP_STORAGE.dta

- **File size:** 7.047 MB
- **Observations ($N$):** 223,399
- **Variables ($K$):** 12
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `q112c0` | Crop Name SN | `double` | `%17.0g` | 1 = Maize; 2 = Paddy; 3 = Sorghum/Millet; 4 = Beans,peas,etc; 5 = Wheat; 6 = ... |
| 7 | `q112c2` | Stored | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 8 | `q112c3` | Current Quantity Stored (kg) | `long` | `%12.0g` |  |
| 9 | `q112c4` | Main Storage structure | `double` | `%48.0g` | 1 = Locally made traditional structure; 2 = Improved locally made structure; ... |
| 10 | `q112c5` | Duration of Storage | `double` | `%25.0g` | 1 = Less than 3 months; 2 = Between 3 and 6 months; 3 = Over 6 months |
| 11 | `q112c6` | Main purpose | `double` | `%27.0g` | 1 = Food for the household; 2 = To sell for higher price; 3 = Seed for planti... |
| 12 | `q112c7` | Estimate Storage  loss | `double` | `%31.0g` | 1 = No loss; 2 = Up to 1/4 loss of the stored; 3 = Above 1/4 up to 1/2 loss; ... |


## 13. R121_FARM_IMPLEMENTS.dta

- **File size:** 12.173 MB
- **Observations ($N$):** 490,400
- **Variables ($K$):** 8
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `q121c0` | Equipment SN | `double` | `%23.0g` | 1 = Panga; 2 = Hand Hoe; 3 = Hand Sprayer; 4 = Oxen; 5 = Ox Plough; 6 = Ox Se... |
| 7 | `q121c2` | Used | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 8 | `q121c3` | Number owned | `double` | `%8.0g` |  |


## 14. R122_USE_TRACTOR_ANIMALS.dta

- **File size:** 1.827 MB
- **Observations ($N$):** 63,372
- **Variables ($K$):** 9
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `q122c0` | SN | `double` | `%15.0g` | 1 = Oxen; 2 = Bulls; 3 = Cows; 4 = Donkeys; 5 = Tractor; 6 = Power Tiller |
| 7 | `q122c2` | Number owned out of number used | `double` | `%8.0g` |  |
| 8 | `q122c3` | Number Used | `double` | `%8.0g` |  |
| 9 | `q122c4` | Area Cultivated (Acres) | `int` | `%9.0g` |  |


## 15. R123_USE_ORGANIC_FERTILIZER.dta

- **File size:** 0.41 MB
- **Observations ($N$):** 13,028
- **Variables ($K$):** 8
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `q123c0` | SN | `double` | `%25.0g` | 1 = Farm Yard Manure (FYM); 2 = Compost Manure |
| 7 | `q123c2` | Quantity used (kg) | `long` | `%12.0g` |  |
| 8 | `q123c3` | Area applied (acres) | `int` | `%9.0g` |  |


## 16. R124_ACCESS_FARM_INPUTS.dta

- **File size:** 5.455 MB
- **Observations ($N$):** 183,900
- **Variables ($K$):** 13
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `q124c0` | Input SN | `double` | `%24.0g` | 1 = Chemical Fertiliser; 2 = Farm Yard Manure; 3 = Compost Manure; 4 = Insect... |
| 7 | `q124c2` | Used | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 8 | `q124c3` | Source of input | `double` | `%32.0g` | 1 = Government; 2 = Local Farmers Group; 3 = Local Market /Trade Store; 4 = S... |
| 9 | `q124c4` | Distance to Source | `double` | `%32.0g` | 1 = Less than 1 km; 2 = From 1 km to less than 3 km; 3 = From 3 km to less th... |
| 10 | `q124c5` | Source of finance | `double` | `%37.0g` | 1 = Sales of farm products; 2 = Other Income generating activities; 3 = Remit... |
| 11 | `q124c6` | Quality of input | `double` | `%17.0g` | 1 = Excellent; 2 = Good; 3 = Average; 4 = Poor; 5 = Does not work; 9 = Not ap... |
| 12 | `q124c7` | Reasons for not using | `double` | `%27.0g` | 1 = Not available; 2 = Price too high; 3 = No money to buy; 4 = Too much labo... |
| 13 | `q124c8` | Plan to use next year | `double` | `%8.0g` | 1 = Yes; 2 = No |


## 17. R126_SOIL_EROSION.dta

- **File size:** 0.72 MB
- **Observations ($N$):** 25,544
- **Variables ($K$):** 9
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `q1262c0` | Soil Erosion SN | `double` | `%35.0g` | 1 = Terraces; 2 = Erosion control bunds; 3 = Gabions/Sandbags; 4 = Cover plan... |
| 7 | `q1262c2` | Used (Yes=1 ,No=2) | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 8 | `q1262c3` | Number of structures | `float` | `%8.0g` |  |
| 9 | `q1262c4` | Year of construction | `float` | `%8.0g` |  |


## 18. R141_EXTENSION_MESSAGES.dta

- **File size:** 0.778 MB
- **Observations ($N$):** 28,548
- **Variables ($K$):** 10
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `q141c0` | Ext SN | `double` | `%40.0g` | 1 = Spacing; 2 = Use of agrochemicals; 3 = Erosion control; 4 = Organic ferti... |
| 7 | `q141c2` | Received advice | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 8 | `q141c3` | Source of crop extension | `double` | `%34.0g` | 1 = Government; 2 = NGO/Dev project; 3 = Cooperative; 4 = Large scale farmer;... |
| 9 | `q141c4` | How was the advice receiived | `double` | `%38.0g` | 1 = Mobile phone; 2 = Email; 3 = Face to face with extension officer; 4 = Tel... |
| 10 | `q141c5` | Messages adopted | `double` | `%8.0g` | 1 = Yes; 2 = No |


## 19. R152_CATTLE_POPULATION.dta

- **File size:** 2.473 MB
- **Observations ($N$):** 61,369
- **Variables ($K$):** 11
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `cattle_weigts` | Cattle Weigts | `byte` | `%10.0g` |  |
| 7 | `q152c0` | Cattle SN | `double` | `%24.0g` | 1 = Castrated Bulls(Oxen); 2 = Uncastred Bulls; 3 = Cows; 4 = Steers; 5 = Hei... |
| 8 | `q152c2` | Number of Indigenous | `float` | `%8.0g` |  |
| 9 | `q152c3` | Number of Improved Beef | `float` | `%8.0g` |  |
| 10 | `q152c4` | Number of Improved Dairy | `float` | `%8.0g` |  |
| 11 | `q152c5` | Total Cattle | `long` | `%12.0g` |  |


## 20. R153_CATTLE_INTAKE.dta

- **File size:** 2.708 MB
- **Observations ($N$):** 61,369
- **Variables ($K$):** 12
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `cattle_weigts` | Cattle Weigts | `byte` | `%10.0g` |  |
| 7 | `q153_c0` | Cattle Intake SN | `double` | `%24.0g` | 1 = Castrated Bulls(Oxen); 2 = Uncastred Bulls; 3 = Cows; 4 = Steers; 5 = Hei... |
| 8 | `q153_c6` | Number Purchased | `float` | `%8.0g` |  |
| 9 | `q153_c7` | Number given/obtained | `float` | `%8.0g` |  |
| 10 | `q153_c8` | Number born | `float` | `%8.0g` |  |
| 11 | `q153_c9` | Total Intake of Cattle | `long` | `%12.0g` |  |
| 12 | `q153_c10` | Average price per head | `long` | `%12.0g` |  |


## 21. R154_CATTLE_OFFTAKE.dta

- **File size:** 2.943 MB
- **Observations ($N$):** 61,369
- **Variables ($K$):** 14
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `cattle_weigts` | Cattle Weigts | `byte` | `%10.0g` |  |
| 7 | `q154c0` | Cattle offtake SN | `double` | `%24.0g` | 1 = Castrated Bulls(Oxen); 2 = Uncastred Bulls; 3 = Cows; 4 = Steers; 5 = Hei... |
| 8 | `q154c2` | Number sold/traded | `float` | `%8.0g` |  |
| 9 | `q154c3` | Number consumed by hh | `float` | `%8.0g` |  |
| 10 | `q154c4` | Number given away | `float` | `%8.0g` |  |
| 11 | `q154c5` | Number stolen | `float` | `%8.0g` |  |
| 12 | `q154c6` | Number died | `float` | `%8.0g` |  |
| 13 | `q154c7` | Total Cattle of Offtake | `long` | `%12.0g` |  |
| 14 | `q154c8` | Average price per head | `long` | `%12.0g` |  |


## 22. R155_CATTLE_DISEASES.dta

- **File size:** 3.253 MB
- **Observations ($N$):** 78,903
- **Variables ($K$):** 14
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `cattle_weigts` | Cattle Weigts | `byte` | `%10.0g` |  |
| 7 | `q155c0` | Diseases SN | `double` | `%27.0g` | 1 = Tick Borne diseases; 2 = CBPP; 3 = Trypanosomiasis; 4 = Lumpy Skin Diseas... |
| 8 | `q155c2` | Did Cattle got any disease in 2019/20? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 9 | `q155c3` | Number Infected | `float` | `%8.0g` |  |
| 10 | `q155c4` | Number Treated | `float` | `%8.0g` |  |
| 11 | `q155c5` | Number Recovered | `float` | `%8.0g` |  |
| 12 | `q155c6` | Number Died | `float` | `%8.0g` |  |
| 13 | `q155c7` | Last Vaccinated | `double` | `%17.0g` | 1 = 2020; 2 = 2019; 3 = 2018; 4 = 2017; 5 = 2016; 6 = 2015; 7 = Before 2015; ... |
| 14 | `q155c8` | Main source of vaccine | `double` | `%43.0g` | 1 = Private Vet Facilities; 2 = District Vet Office; 3 = NGO/Project; 4 = Tan... |


## 23. R157_CATTLE_MILK_PRODUCTION.dta

- **File size:** 0.915 MB
- **Observations ($N$):** 19,208
- **Variables ($K$):** 14
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `cattle_weigts` | Cattle Weigts | `byte` | `%10.0g` |  |
| 7 | `q157c1` | Season | `double` | `%31.0g` | 1 = Wet Season (Improved Diary); 2 = Wet Season (Indigenous); 3 = Dry Season ... |
| 8 | `q157c3` | Number of milked cows | `float` | `%8.0g` |  |
| 9 | `q157c4` | Average milk production per cow per day | `int` | `%9.0g` |  |
| 10 | `q157c5` | Average number of days for cows on milked | `float` | `%8.0g` |  |
| 11 | `q157c6` | Milk consumed by the Hh (Litres) | `float` | `%8.0g` |  |
| 12 | `q157c7` | Amount of milk sold (Litres) | `long` | `%12.0g` |  |
| 13 | `q157c8` | Average price per litre per season | `float` | `%8.0g` |  |
| 14 | `q157c9` | Where Sold | `double` | `%47.0g` | 1 = Neighbour; 2 = Local market/trade store; 3 = Private Milk Collection Cent... |


## 24. R162_GOAT_POPULATION.dta

- **File size:** 2.042 MB
- **Observations ($N$):** 36,620
- **Variables ($K$):** 13
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `livestock_wgt` | Livestock Weight | `byte` | `%10.0g` |  |
| 7 | `fish_weights` | Fish weights | `byte` | `%10.0g` |  |
| 8 | `cattle_weigts` | Cattle Weigts | `byte` | `%10.0g` |  |
| 9 | `q162c0` | Goat SN | `double` | `%17.0g` | 1 = Billy Goat; 2 = Castrated Goat; 3 = She Goat; 4 = Male Kid; 5 = She Kid |
| 10 | `q162c2` | Number of Indigenous | `float` | `%8.0g` |  |
| 11 | `q162c3` | Number of Improved for Meat | `float` | `%8.0g` |  |
| 12 | `q162c4` | Number of Improved Dairy | `float` | `%8.0g` |  |
| 13 | `q162c5` | Total Goat | `long` | `%12.0g` |  |


## 25. R163_GOAT_INTAKE.dta

- **File size:** 1.622 MB
- **Observations ($N$):** 36,620
- **Variables ($K$):** 12
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `livestock_wgt` | Livestock Weight | `byte` | `%10.0g` |  |
| 7 | `q163c0` | Goat Intake SN | `double` | `%17.0g` | 1 = Billy Goat; 2 = Castrated Goat; 3 = She Goat; 4 = Male Kid; 5 = She Kid |
| 8 | `q163c6` | Number Purchased | `float` | `%8.0g` |  |
| 9 | `q163c7` | Number given/obtained | `float` | `%8.0g` |  |
| 10 | `q163c8` | Number born | `float` | `%8.0g` |  |
| 11 | `q163c9` | Total Intake of Goat | `long` | `%12.0g` |  |
| 12 | `q16310` | Average price per head | `long` | `%12.0g` |  |


## 26. R164_GOAT_OFFTAKE.dta

- **File size:** 1.763 MB
- **Observations ($N$):** 36,620
- **Variables ($K$):** 14
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `livestock_wgt` | Livestock Weight | `byte` | `%10.0g` |  |
| 7 | `q164c0` | Goat Offtake SN | `double` | `%17.0g` | 1 = Billy Goat; 2 = Castrated Goat; 3 = She Goat; 4 = Male Kid; 5 = She Kid |
| 8 | `q164c2` | Number sold/traded | `float` | `%8.0g` |  |
| 9 | `q164c3` | Number consumed by hh | `float` | `%8.0g` |  |
| 10 | `q164c4` | Number given away | `float` | `%8.0g` |  |
| 11 | `q164c5` | Number given stolen | `float` | `%8.0g` |  |
| 12 | `q164c6` | Number died | `float` | `%8.0g` |  |
| 13 | `q164c7` | Total Goat Offtake | `long` | `%12.0g` |  |
| 14 | `q164c8` | Average price per head | `long` | `%12.0g` |  |


## 27. R165_GOAT_DISEASES.dta

- **File size:** 2.42 MB
- **Observations ($N$):** 58,592
- **Variables ($K$):** 14
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `livestock_wgt` | Livestock Weight | `byte` | `%10.0g` |  |
| 7 | `q165c0` | Goat Disease SN | `double` | `%30.0g` | 1 = Foot Rot; 2 = CCPP; 3 = Helminthiosis; 4 = Tetanus; 5 = Mange; 6 = Brucel... |
| 8 | `q165c2` | Disease in 2019/20 | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 9 | `q165c3` | Number Infected | `float` | `%8.0g` |  |
| 10 | `q165c4` | Number Treated | `float` | `%8.0g` |  |
| 11 | `q165c5` | Number Recovered | `float` | `%8.0g` |  |
| 12 | `q165c6` | Number Died | `float` | `%8.0g` |  |
| 13 | `q165c7` | Last Vaccinated | `double` | `%17.0g` | 1 = 2020; 2 = 2019; 3 = 2018; 4 = 2017; 5 = 2016; 6 = 2015; 7 = Before 2015; ... |
| 14 | `q165c8` | Main source of vaccine | `double` | `%43.0g` | 1 = Private Vet Facilities; 2 = District Vet Office; 3 = NGO/Project; 4 = Tan... |


## 28. R166_GOAT_MILK_PRODUCTION.dta

- **File size:** 0.035 MB
- **Observations ($N$):** 426
- **Variables ($K$):** 14
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `livestock_wgt` | Livestock Weight | `byte` | `%10.0g` |  |
| 7 | `q166c0` | Goat Season SN | `double` | `%13.0g` | 1 = Wet Season; 2 = Dry Season |
| 8 | `q166c2` | Number of Milked goat | `float` | `%8.0g` |  |
| 9 | `q166c3` | Average milk production per goat per day | `double` | `%8.0g` |  |
| 10 | `q166c4` | Average number of days for goats on milked | `float` | `%8.0g` |  |
| 11 | `q166c5` | Milk consumed by the Hh (Litres) | `float` | `%8.0g` |  |
| 12 | `q166c6` | Amount of milk sold (Litres) | `float` | `%8.0g` |  |
| 13 | `q166c7` | Average price per litre per season | `float` | `%8.0g` |  |
| 14 | `q166c8` | Where Sold | `double` | `%48.0g` | 1 = Neighbour; 2 = Local market/trade store; 3 = Private Milk Collection cent... |


## 29. R172_SHEEP_POPULATION.dta

- **File size:** 0.629 MB
- **Observations ($N$):** 15,335
- **Variables ($K$):** 11
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `livestock_wgt` | Livestock Weight | `byte` | `%10.0g` |  |
| 7 | `q172c0` | Sheep type SN | `double` | `%18.0g` | 1 = Ram; 2 = Castrated Sheep; 3 = Ewe (She Sheep); 4 = Male Lamb; 5 = She Lamb |
| 8 | `q172c2` | Number of Indigenous | `float` | `%8.0g` |  |
| 9 | `q172c3` | Number of Improved for Mutton | `float` | `%8.0g` |  |
| 10 | `q172c4` | Number of Improved for Diary | `float` | `%8.0g` |  |
| 11 | `q172c5` | Total Sheep | `long` | `%12.0g` |  |


## 30. R173_SHEEP_INTAKE.dta

- **File size:** 0.688 MB
- **Observations ($N$):** 15,335
- **Variables ($K$):** 12
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `livestock_wgt` | Livestock Weight | `byte` | `%10.0g` |  |
| 7 | `q173c0` | Sheep Intake SN | `double` | `%18.0g` | 1 = Ram; 2 = Castrated Sheep; 3 = She Sheep; 4 = Male Lamb; 5 = She Lamb |
| 8 | `q173c6` | Number Purchased | `float` | `%8.0g` |  |
| 9 | `q173c7` | Number given/obtained | `float` | `%8.0g` |  |
| 10 | `q173c8` | Number born | `float` | `%8.0g` |  |
| 11 | `q173c9` | Total Intake of Sheep | `long` | `%12.0g` |  |
| 12 | `q173c10` | Average price per head | `long` | `%12.0g` |  |


## 31. R174_SHEEP_OFFTAKE.dta

- **File size:** 0.748 MB
- **Observations ($N$):** 15,335
- **Variables ($K$):** 14
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `livestock_wgt` | Livestock Weight | `byte` | `%10.0g` |  |
| 7 | `q174c0` | Sheep Offtake SN | `double` | `%18.0g` | 1 = Ram; 2 = Castrated Sheep; 3 = She Sheep; 4 = Male Lamb; 5 = She Lamb |
| 8 | `q174c2` | Number sold/traded | `float` | `%8.0g` |  |
| 9 | `q174c3` | Number consumed by hh | `float` | `%8.0g` |  |
| 10 | `q174c4` | Number given away | `float` | `%8.0g` |  |
| 11 | `q174c5` | Number given stolen | `float` | `%8.0g` |  |
| 12 | `q174c6` | Number died | `float` | `%8.0g` |  |
| 13 | `q174c7` | Total Sheep Offtake | `long` | `%12.0g` |  |
| 14 | `q174c8` | Average price per head | `long` | `%12.0g` |  |


## 32. R175_SHEEP_DISEASES.dta

- **File size:** 1.024 MB
- **Observations ($N$):** 24,536
- **Variables ($K$):** 14
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `livestock_wgt` | Livestock Weight | `byte` | `%10.0g` |  |
| 7 | `q175c0` | Sheep Disease Sn | `double` | `%18.0g` | 1 = Foot Rot; 2 = CCPP; 3 = Helminthiosis; 4 = Trypanosomiasis; 5 = FMD; 6 = ... |
| 8 | `q175c2` | Disease in 2019/20 | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 9 | `q175c3` | Number Infected | `float` | `%8.0g` |  |
| 10 | `q175c4` | Number Treated | `float` | `%8.0g` |  |
| 11 | `q175c5` | Number Recovered | `float` | `%8.0g` |  |
| 12 | `q175c6` | Number Died | `float` | `%8.0g` |  |
| 13 | `q175c7` | Last Vaccinated | `double` | `%17.0g` | 1 = 2020; 2 = 2019; 3 = 2018; 4 = 2017; 5 = 2016; 6 = 2015; 7 = Before 2015; ... |
| 14 | `q175c8` | Main source of vaccine | `double` | `%43.0g` | 1 = Private Vet Facilities; 2 = District Vet Office; 3 = NGO/Project; 4 = Tan... |


## 33. R182_PIG_POPULATION.dta

- **File size:** 0.387 MB
- **Observations ($N$):** 11,544
- **Variables ($K$):** 8
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `livestock_wgt` | Livestock Weight | `byte` | `%10.0g` |  |
| 7 | `q182c0` | Pig SN | `double` | `%17.0g` | 1 = Boar; 2 = Castrated Male; 3 = Sow; 4 = Gilt; 5 = Male Piglet; 6 = She Piglet |
| 8 | `q182c2` | Number of Pig | `float` | `%8.0g` |  |


## 34. R183_PIG_INTAKE.dta

- **File size:** 0.522 MB
- **Observations ($N$):** 11,544
- **Variables ($K$):** 12
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `livestock_wgt` | Livestock Weight | `byte` | `%10.0g` |  |
| 7 | `q183c0` | Pig Intake SN | `double` | `%17.0g` | 1 = Boar; 2 = Castrated Male; 3 = Sow; 4 = Gilt; 5 = Male Piglet; 6 = She Piglet |
| 8 | `q183c3` | Number Purchased | `float` | `%8.0g` |  |
| 9 | `q183c4` | Number given/obtained | `float` | `%8.0g` |  |
| 10 | `q183c5` | Number born | `float` | `%8.0g` |  |
| 11 | `q183c6` | Total Pig increase | `long` | `%12.0g` |  |
| 12 | `q183c7` | Average price per head | `long` | `%12.0g` |  |


## 35. R184_PIG_OFFTAKE.dta

- **File size:** 0.567 MB
- **Observations ($N$):** 11,544
- **Variables ($K$):** 14
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `livestock_wgt` | Livestock Weight | `byte` | `%10.0g` |  |
| 7 | `q184c0` | Pig Offtake SN | `double` | `%17.0g` | 1 = Boar; 2 = Castrated Male; 3 = Sow; 4 = Gilt; 5 = Male Piglet; 6 = She Piglet |
| 8 | `q184c2` | Number sold/traded | `float` | `%8.0g` |  |
| 9 | `q184c3` | Number consumed by hh | `float` | `%8.0g` |  |
| 10 | `q184c4` | Number given away | `float` | `%8.0g` |  |
| 11 | `q184c5` | Number given stolen | `float` | `%8.0g` |  |
| 12 | `q184c6` | Number died | `float` | `%8.0g` |  |
| 13 | `q184c7` | Total Pig Offtake | `long` | `%12.0g` |  |
| 14 | `q184c8` | Average price per head | `long` | `%12.0g` |  |


## 36. R185_PIG_DISEASES.dta

- **File size:** 0.57 MB
- **Observations ($N$):** 13,468
- **Variables ($K$):** 14
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `byte` | `%10.0g` | [Household_ID] |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `livestock_wgt` | Livestock Weight | `byte` | `%10.0g` |  |
| 7 | `q185c0` | Pig disease SN | `double` | `%26.0g` | 1 = Anthrax; 2 = African Swan Fever(ASF); 3 = Anemia; 4 = Helmenthiosis; 5 = ... |
| 8 | `q185c2` | Disease in 2019/20 | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 9 | `q185c3` | Number Infected | `float` | `%8.0g` |  |
| 10 | `q185c4` | Number Treated | `float` | `%8.0g` |  |
| 11 | `q185c5` | Number Recovered | `float` | `%8.0g` |  |
| 12 | `q185c6` | Number Died | `float` | `%8.0g` |  |
| 13 | `q185c7` | Last Vaccinated | `double` | `%17.0g` | 1 = 2020; 2 = 2019; 3 = 2018; 4 = 2017; 5 = 2016; 6 = 2015; 7 = Before 2015; ... |
| 14 | `q185c8` | Main source of vaccine | `double` | `%43.0g` | 1 = Private Vet Facilities; 2 = District Vet Office; 3 = NGO/Project; 4 = Tan... |


## 37. R192_POULTRY_POPULATION.dta

- **File size:** 5.718 MB
- **Observations ($N$):** 108,744
- **Variables ($K$):** 11
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `str15` | `%15s` |  |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `livestock_wgt` | Livestock Weight | `byte` | `%10.0g` |  |
| 7 | `q192c0` | Poulty SN | `double` | `%21.0g` | 1 = Indigenous Chicken; 2 = Layer; 3 = Broiler; 4 = Ducks; 5 = Turkey; 6 = Gu... |
| 8 | `q192c2` | as of 1st october 2019 (Number) | `long` | `%12.0g` |  |
| 9 | `q192c3` | Sold (Number) | `long` | `%12.0g` |  |
| 10 | `q192c4` | Sold ( Average Value/head) | `long` | `%12.0g` |  |
| 11 | `q192c5` | Consumed (Number) | `long` | `%12.0g` |  |


## 38. R193_POULTRY_DISEASES.dta

- **File size:** 6.238 MB
- **Observations ($N$):** 108,744
- **Variables ($K$):** 13
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `str15` | `%15s` |  |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `livestock_wgt` | Livestock Weight | `byte` | `%10.0g` |  |
| 7 | `q193c0` | Poultry Disease SN | `double` | `%20.0g` | 1 = Newcastle Disease; 2 = Gumboro; 3 = Coccidiosis; 4 = Coryza; 5 = Fowl pox... |
| 8 | `q193c2` | Disease in 2019/20 | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 9 | `q193c3` | Number Vaccinated | `long` | `%12.0g` |  |
| 10 | `q193c4` | Number Infected | `long` | `%12.0g` |  |
| 11 | `q193c5` | Number Treated | `long` | `%12.0g` |  |
| 12 | `q193c6` | Number Died | `long` | `%12.0g` |  |
| 13 | `q193c7` | Number Recovered | `long` | `%12.0g` |  |


## 39. R202_OTHER_LIVESTOCK_POP.dta

- **File size:** 1.428 MB
- **Observations ($N$):** 30,252
- **Variables ($K$):** 11
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `str15` | `%15s` |  |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `livestock_wgt` | Livestock Weight | `byte` | `%10.0g` |  |
| 7 | `q2021c0` | Animal SN | `double` | `%14.0g` | 1 = Rabbits; 2 = Donkeys; 3 = Horses; 4 = Dogs; 5 = Guinea pigs; 6 = Other |
| 8 | `q2021c2` | as of 1st october 2019 (Number) | `float` | `%8.0g` |  |
| 9 | `q2021c3` | Sold (Number) | `float` | `%8.0g` |  |
| 10 | `q2021c4` | Sold ( Average Price/head) | `long` | `%12.0g` |  |
| 11 | `q2021c5` | Consumed (Number) | `float` | `%8.0g` |  |


## 40. R203_OTHER_LIVESTOCK_PROD.dta

- **File size:** 8.048 MB
- **Observations ($N$):** 153,160
- **Variables ($K$):** 11
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `str15` | `%15s` |  |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `livestock_wgt` | Livestock Weight | `byte` | `%10.0g` |  |
| 7 | `q2031c0` | Product SN | `double` | `%28.0g` | 1 = Eggs (Indigenous Chicken); 2 = Eggs (Improved Chicken); 3 = Hides; 4 = Go... |
| 8 | `q2031c2` | Production | `long` | `%12.0g` |  |
| 9 | `q2031c3` | Sold (Number) | `long` | `%12.0g` |  |
| 10 | `q2031c4` | Sold ( Average Value/head) | `long` | `%12.0g` |  |
| 11 | `q2031c5` | Consumed (Number) | `long` | `%12.0g` |  |


## 41. R210_OUTLET_SALES_LIVEST.dta

- **File size:** 1.696 MB
- **Observations ($N$):** 31,436
- **Variables ($K$):** 12
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `str15` | `%15s` |  |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `q211c0` | Outlet SN | `double` | `%8.0g` | 1 = 1st; 2 = 2nd; 3 = 3rd; 4 = 4th; 5 = 5th |
| 7 | `q211c1` | Importance of outlet | `str20` | `%20s` |  |
| 8 | `q211c2` | Outlet for Cattle | `double` | `%27.0g` | 1 = Trader at farm; 2 = Primary Market; 3 = Secondary market/auction; 4 = Nei... |
| 9 | `q211c3` | Outlet for Goats | `double` | `%27.0g` | 1 = Trader at farm; 2 = Primary Market; 3 = Secondary market/auction; 4 = Nei... |
| 10 | `q211c4` | Outlet for Sheep | `double` | `%27.0g` | 1 = Trader at farm; 2 = Primary Market; 3 = Secondary market/auction; 4 = Nei... |
| 11 | `q211c5` | Outlet for Pig | `double` | `%27.0g` | 1 = Trader at farm; 2 = Primary Market; 3 = Secondary market/auction; 4 = Nei... |
| 12 | `q211c6` | Outlet for Chicken | `double` | `%27.0g` | 1 = Trader at farm; 2 = Primary Market; 3 = Secondary market/auction; 4 = Nei... |


## 42. R220_LIVEST_STUCTURES_AC.dta

- **File size:** 19.745 MB
- **Observations ($N$):** 459,750
- **Variables ($K$):** 10
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `str15` | `%15s` |  |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `livestock_wgt` | Livestock Weight | `byte` | `%10.0g` |  |
| 7 | `q221c0` | Type Structure SN | `double` | `%26.0g` | 1 = Cattle Dip; 2 = Spray Race; 3 = Hand sprayer; 4 = Cattle crush; 5 = Prima... |
| 8 | `q221c2` | Accesibility | `double` | `%12.0g` | 1 = Yes; 2 = No; 3 = Dont know |
| 9 | `q221c3` | Source of Structure | `double` | `%28.0g` | 1 = Self Owned; 2 = Cooperative; 3 = Local farmers association; 4 = Gov exten... |
| 10 | `q221c4` | Distance to structure (km) | `int` | `%9.0g` |  |


## 43. R241_LIVESTOCK_EXTENSION.dta

- **File size:** 0.772 MB
- **Observations ($N$):** 18,438
- **Variables ($K$):** 11
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `str15` | `%15s` |  |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `livestock_wgt` | Livestock Weight | `byte` | `%10.0g` |  |
| 7 | `q241c0` | Livestock Extension SN | `double` | `%48.0g` | 1 = Feeds and Proper feeding; 2 = Housing; 3 = Proper Milking and Milk Hygene... |
| 8 | `q241c2` | Received Advice | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 9 | `q241c3` | Source of Livestock Extension | `double` | `%39.0g` | 1 = Government; 2 = NGO/Development project; 3 = Cooperative; 4 = Large scale... |
| 10 | `q241c4` | How was the advice received? | `double` | `%38.0g` | 1 = Mobile phone; 2 = Email; 3 = Face to face with extension officer; 4 = Tel... |
| 11 | `q241c5` | Advice adopted | `double` | `%8.0g` | 1 = Yes; 2 = No |


## 44. R250_LIVESTOCK_EXT_SERVICE.dta

- **File size:** 0.385 MB
- **Observations ($N$):** 7,902
- **Variables ($K$):** 13
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `str15` | `%15s` |  |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `livestock_wgt` | Livestock Weight | `byte` | `%10.0g` |  |
| 7 | `q251c0` | Extension SN | `double` | `%39.0g` | 1 = Government; 2 = NGO/Dev project; 3 = Registered private vets and paravets... |
| 8 | `q251c2a` | Did you receive exte | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 9 | `q251c2b` | If you pay for extension, what is the cost/yr | `long` | `%12.0g` |  |
| 10 | `q251c3` | Contact farmer/group member | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 11 | `q251c4` | No. of visits by extension agency year 2019/20 | `double` | `%8.0g` |  |
| 12 | `q251c5` | No. of messages adopted in the last 3 yrs | `float` | `%8.0g` |  |
| 13 | `q251c6` | Quality of Service | `double` | `%17.0g` | 1 = Very good; 2 = Good; 3 = Average; 4 = Poor; 5 = Very poor; 9 = Not Applic... |


## 45. R262_GOVT_REGULAT_CHALLENG.dta

- **File size:** 0.061 MB
- **Observations ($N$):** 1,197
- **Variables ($K$):** 8
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `str15` | `%15s` |  |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `q26211c0` | Order SN | `double` | `%8.0g` | 1 = 1st; 2 = 2nd; 3 = 3rd |
| 7 | `q26211c1` | Order of importance | `str10` | `%10s` |  |
| 8 | `q26211c2` | Challange code | `double` | `%49.0g` | 1 = Land ownership by government; 2 = Restrictions of livestock sale between ... |


## 46. R272_FISH_FARMING.dta

- **File size:** 0.037 MB
- **Observations ($N$):** 110
- **Variables ($K$):** 24
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `str15` | `%15s` |  |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `fish_weights` | Fish weights | `byte` | `%10.0g` |  |
| 7 | `q2711c1` | Production Unit Number | `double` | `%19.0g` | 1 = Production Unit1 |
| 8 | `q2711c2` | Aquaculture system | `double` | `%21.0g` | 1 = Deep Water Cage; 2 = Shallow Water Cage; 3 = Natural Pond; 4 = Dug Out po... |
| 9 | `q2711c3` | Size of Unit/pond | `float` | `%8.0g` |  |
| 10 | `q2711c4` | Type of Water | `double` | `%17.0g` | 1 = Fresh water; 2 = Salt water; 3 = Brackish water |
| 11 | `q2711c5` | Source of Water | `double` | `%17.0g` | 1 = Rainwater; 2 = Ground water; 3 = River water; 4 = Lakes water; 5 = Dams w... |
| 12 | `q2711c6` | Source of fingerling | `double` | `%34.0g` | 1 = Own fish hatchery; 2 = Neighbour fish hatchery; 3 = Government institutio... |
| 13 | `q2711c7` | Frequency of stocking(No./ Year) | `double` | `%8.0g` | 1 = 1; 2 = 2; 3 = 3; 4 = 4; 5 = 5; 6 = 6; 7 = 7; 8 = 8 |
| 14 | `q2711c8` | Type of Stocked Fish | `double` | `%20.0g` | 1 = Tilapia; 2 = Milkfish; 3 = African Catchfish; 4 = Prawns; 8 = Other |
| 15 | `q2711c8_other` | Type of stoked fish Other type (Specify)….. | `str40` | `%40s` |  |
| 16 | `q2711c9` | Number of stocked Fish | `long` | `%12.0g` |  |
| 17 | `q2711c10` | Number of fish harvested | `long` | `%12.0g` |  |
| 18 | `q2711c11` | Weight of fish harvested | `byte` | `%10.0g` |  |
| 19 | `q2711c12` | Weight of fish sold | `byte` | `%10.0g` |  |
| 20 | `q2711c13` | Average price of fish sold (TZS) | `float` | `%8.0g` |  |
| 21 | `q2711c14` | Mainly sold to | `double` | `%22.0g` | 1 = Neighbour; 2 = Landing site; 3 = Fish market; 4 = Processing industry; 5 ... |
| 22 | `q2711c15` | Source of Fish Feeds | `double` | `%30.0g` | 1 = Home made feeds; 2 = Locally compounded  feeds; 3 = Imported manufactured... |
| 23 | `q2711c16` | Amount Used /Purchased in Kg | `long` | `%12.0g` |  |
| 24 | `q2711c17` | average Price per kg | `float` | `%8.0g` |  |


## 47. R281_BEE_KEEPING.dta

- **File size:** 0.057 MB
- **Observations ($N$):** 878
- **Variables ($K$):** 13
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `str15` | `%15s` |  |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `q2811c0` | Bees SN | `double` | `%30.0g` | 1 = Small bees (Stingless Bees); 2 = Large bees |
| 7 | `q2811c2` | Number of Local Bee Hives | `float` | `%8.0g` |  |
| 8 | `q2811c3` | Number of improved Bee hives | `float` | `%8.0g` |  |
| 9 | `q2811c4` | Harvesting done? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 10 | `q2811c5` | Amount Produced per year (Litre) | `long` | `%12.0g` |  |
| 11 | `q2811c6` | Amount of honey Sold (Litre) | `long` | `%12.0g` |  |
| 12 | `q2811c7` | Average Price per Litre | `long` | `%12.0g` |  |
| 13 | `q2811c8` | Main Market | `double` | `%29.0g` | 1 = Neighbour; 2 = Auction; 3 = Large Scale Farmers; 4 = Open market; 5 = Hon... |


## 48. R291_LABOUR_USE.dta

- **File size:** 27.022 MB
- **Observations ($N$):** 858,200
- **Variables ($K$):** 8
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `str15` | `%15s` |  |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `q2911c0` | Activity SN | `double` | `%32.0g` | 1 = Land Clearing; 2 = Land tilling (by hand); 3 = Land tilling (oxen/tractor... |
| 7 | `q2911c2` | Is your household  involved in  [..]? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 8 | `q2911c3` | Main responsible person(s) | `double` | `%24.0g` | 1 = Hosehold head alone; 2 = Adult Males; 3 = Adult Females; 4 = Adults; 5 = ... |


## 49. R301_SUBSTANCE_NONSUBST.dta

- **File size:** 13.343 MB
- **Observations ($N$):** 367,800
- **Variables ($K$):** 10
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `str15` | `%15s` |  |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `q301c0` | Activity SN | `double` | `%40.0g` | 1 = Crop production; 2 = Livestock production; 3 = Vegetable production; 4 = ... |
| 7 | `q301c2` | Is your household  involved in [….]? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 8 | `q301c3` | Estimate % used for subsistance | `float` | `%8.0g` |  |
| 9 | `q301c4` | Estimate % used for non subsistance | `float` | `%8.0g` |  |
| 10 | `q301c5` | Check Total | `float` | `%12.0g` | 100 = Percent |


## 50. R310_ACCESS_INFRASTUCTURE.dta

- **File size:** 14.335 MB
- **Observations ($N$):** 429,100
- **Variables ($K$):** 7
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `str15` | `%15s` |  |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `q310c0` | Type of Service SN | `double` | `%20.0g` | 1 = Primary School; 2 = Secondary School; 3 = Dispensary; 4 = Health Centre; ... |
| 7 | `q310c2` | Distance in Km | `int` | `%29.0g` | 998 = Don't Know; 999 = Service is Not Available |


## 51. R311_OTHER_SERVICES.dta

- **File size:** 6.503 MB
- **Observations ($N$):** 183,900
- **Variables ($K$):** 9
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `str15` | `%15s` |  |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `q311c0` | Type of Other Serv SN | `double` | `%29.0g` | 1 = Extension Centre; 2 = Research Station; 3 = Plant protection Lab; 4 = Lan... |
| 7 | `q311c2` | Distance in Km | `int` | `%29.0g` | 998 = Don't Know; 999 = Service is Not Available |
| 8 | `q311c3` | Number of visits/year | `double` | `%8.0g` |  |
| 9 | `q311c4` | Satisfied with service | `double` | `%17.0g` | 1 = Very good; 2 = Good; 3 = Average; 4 = Poor; 5 = No good; 9 = Not applicable |


## 52. R321_LIVELIHOOD_CNSTR_MOST.dta

- **File size:** 4.588 MB
- **Observations ($N$):** 92,245
- **Variables ($K$):** 8
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `str15` | `%15s` |  |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `q321c0` | Order MOST SN | `double` | `%21.0g` | 1 = Most important; 2 = 2nd most important; 3 = 3rd most important; 4 = 4th m... |
| 7 | `q321c1` | Order of most importance | `str20` | `%20s` |  |
| 8 | `q321c2` | Constraint | `double` | `%59.0g` | 1 = Access to land; 2 = Land Ownership; 3 = Soil fertility; 4 = Availability ... |


## 53. R330_MARKET_INFORMATION.dta

- **File size:** 8.43 MB
- **Observations ($N$):** 275,850
- **Variables ($K$):** 7
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `str15` | `%15s` |  |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `q330c0` | Market Info SN | `double` | `%23.0g` | 1 = Television; 2 = Radio; 3 = News papers; 4 = Mobile Phones; 5 = Local Auth... |
| 7 | `q330c2` | Yes=1,No=2 | `double` | `%8.0g` | 1 = Yes; 2 = No |


## 54. R342_HOUSE_ASSETS.dta

- **File size:** 15.913 MB
- **Observations ($N$):** 521,050
- **Variables ($K$):** 7
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `str15` | `%15s` |  |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `q342c0` | Asset SN | `double` | `%35.0g` | 1 = Radio / cassette, (music system); 2 = Telephone (landline); 3 = Telephone... |
| 7 | `q342c2` | Yes=1, No=2 | `double` | `%8.0g` | 1 = Yes; 2 = No |


## 55. R344_ACCESS_DRINKING_WATER.dta

- **File size:** 2.352 MB
- **Observations ($N$):** 61,300
- **Variables ($K$):** 9
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `str15` | `%15s` |  |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |
| 6 | `q344c0` | Access Source Sn | `double` | `%13.0g` | 1 = Wet Season; 2 = Dry Season |
| 7 | `q344c2` | Main source of drinking water | `double` | `%42.0g` | 1 = Piped water; 2 = Protected well; 3 = Protected/covered spring; 4 = Unprot... |
| 8 | `q344c3` | Distance to source (in km) | `int` | `%9.0g` |  |
| 9 | `q344c4` | Time to and from source (Hour : minute) | `int` | `%9.0g` |  |


## 56. R346_FOOD_SECURITY.dta

- **File size:** 1.247 MB
- **Observations ($N$):** 30,650
- **Variables ($K$):** 17
- **Stata Format:** Release 118

| # | Variable | Label / Description | Type | Format | Value Labels / Codes |
|---|---|---|---|---|---|
| 1 | `region` | Region | `double` | `%20.0g` | 1 = Dodoma; 2 = Arusha; 3 = Kilimanjaro; 4 = Tanga; 5 = Morogoro; 6 = Pwani; ... |
| 2 | `district` | District | `int` | `%36.0g` | 101 = Kondoa District Council; 102 = Mpwapwa District Council; 103 = Kongwa D... |
| 3 | `HHID` | Household_ID | `str15` | `%15s` |  |
| 4 | `hh_number` | Household Number | `float` | `%8.0g` |  |
| 5 | `q34_6_1` | 34.6.1 Number of meals the hh normally take per day | `double` | `%8.0g` |  |
| 6 | `q34_6_2` | 34.6.2 Number of days hh consumed meat in the last seven days | `double` | `%8.0g` |  |
| 7 | `q34_6_3` | 34.6.3 Number of days hh consumed Fish in the last seven days | `double` | `%8.0g` |  |
| 8 | `q34_6_4` | 34.6.4 How often did the hh had problems in satisfying the food needs of the hh | `double` | `%12.0g` | 1 = Never; 2 = Seldom; 3 = Sometimes; 4 = Often; 5 = Always |
| 9 | `q34_6_5` | 34.6.5 Did you or any other member in  your household were worried you could not | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 10 | `q34_6_6` | 34.6.6 Did you or any other member in  your household were unable to eat healthy | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 11 | `q34_6_7` | 34.6.7 Did you or any other member in  your household ate only a few kinds of fo | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 12 | `q34_6_8` | 34.6.8 Did you or any other member in  your household had to skip a meal? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 13 | `q34_6_9` | 34.6.9 Did you or any other member in  your household ate less than you thought | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 14 | `q34_6_10` | 34.6.10 Did your  household ran out of food? | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 15 | `q34_6_11` | 34.6.11 Did you or any other member in  your household were hungry but did not e | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 16 | `q34_6_12` | 34.6.12 Did you or any other member in  your household went without eating for a | `double` | `%8.0g` | 1 = Yes; 2 = No |
| 17 | `finalweight_hh` | Households Weight | `byte` | `%10.0g` |  |

