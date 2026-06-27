# NHAMCS 2022 — ED Wait Time Disparity Analysis

Analysis of racial and ethnic disparities in emergency department wait times using the **National Hospital Ambulatory Medical Care Survey (NHAMCS) 2022** federal dataset.

## Research Question
Do ED wait times differ significantly by race/ethnicity, and does triage urgency or insurance type explain that gap?

## Key Finding
Hispanic patients waited approximately **14.8% less** than Non-Hispanic White patients after full adjustment for triage urgency, insurance type, age, sex, arrival mode, and time of day (β = -0.161, 95% CI [-0.246, -0.076], p = 0.0002). Triage urgency functioned as a suppressor variable rather than a confounder, consistent with potential under triage of Hispanic patients relative to clinical need.
 
## Notebooks
- `NHAMCS/01_data_cleaning.ipynb` — Data cleaning and EDA
- `NHAMCS/02_stat_tests.ipynb` — 4-model OLS regression sequence
- `NHAMCS/03_ml_modeling.ipynb` - Random forest classifier + SHAP analysis

## Documentation
- `NHAMCS/CODEBOOK.md` — Variable definitions and official CDC codes
- `NHAMCS_Abstract.md` — Structured abstract (background, methods, results, 
  conclusions, limitations)
- `NHAMCS_2022_ED_Disparities_AmyYu.pdf` — PDF version of abstract

## Tools
Python · Pandas · Statsmodels · Seaborn · Matplotlib · NumPy · Scikit-learn · SHAP

## Data Source
[NHAMCS 2022 — CDC/NCHS](https://www.cdc.gov/nchs/ahcd/ahcd_questionnaires.htm)
Raw data not included in this repo — download directly from CDC.

## Status
Complete - covariate analysis, ML extension, and write-up finalized
