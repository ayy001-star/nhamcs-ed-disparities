# NHAMCS 2022 — ED Wait Time Disparity Analysis

Analysis of racial and ethnic disparities in emergency department wait times using the **National Hospital Ambulatory Medical Care Survey (NHAMCS) 2022** federal dataset.

## Research Question
Do ED wait times differ significantly by race/ethnicity, and does triage urgency or insurance type explain that gap?

## Notebooks
- `NHAMCS.ipynb` — Data cleaning and exploratory data analysis
- `02_model.ipynb` — OLS regression modeling (WAITTIME ~ RACERETH)

## Tools
Python · Pandas · Statsmodels · Seaborn · Matplotlib · NumPy

## Data Source
[NHAMCS 2022 — CDC/NCHS](https://www.cdc.gov/nchs/ahcd/ahcd_questionnaires.htm)
Raw data not included in this repo — download directly from CDC.

## Status
In progress — covariate analysis (triage urgency, insurance type) coming next.
