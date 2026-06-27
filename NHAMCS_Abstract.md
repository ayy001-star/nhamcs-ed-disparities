# Racial and Ethnic Disparities in Emergency Department Wait Times: An Analysis of the 2022 National Hospital Ambulatory Medical Care Survey

*Amy Yu · UCSD, Public Health / Medical Sciences*
*Draft — 2026-06-24*

---

## Background
Emergency department (ED) wait times are a key indicator of care access and quality. Racial and ethnic disparities in ED wait times may reflect structural inequities in triage practices, insurance coverage, and resource allocation. This study examines whether wait times differ significantly by race/ethnicity in a nationally representative ED sample, and whether triage urgency and insurance type explain any observed differences.

---

## Methods
Data were drawn from the 2022 National Hospital Ambulatory Medical Care Survey (NHAMCS) Emergency Department Public Use File (N = 16,025). The analytic sample was restricted to visits with complete data on wait time, triage immediacy (IMMEDR), insurance type (PAYTYPER), and arrival characteristics, yielding a final sample of 7,971 visits. Wait time was log-transformed (log[WAITTIME + 1]) to address right skew. Race/ethnicity was measured using the CDC-imputed RACERETH variable (1 = Non-Hispanic White [reference], 2 = Non-Hispanic Black, 3 = Hispanic, 4 = Non-Hispanic Other). A sequential OLS regression was conducted across four models: bivariate (race only), plus triage urgency, plus insurance type, and a full model additionally adjusting for age, sex, arrival by EMS, and hour of arrival. Confidence intervals and p-values are reported for all RACERETH coefficients. A supplementary random forest classifier with SHAP feature importance analysis was conducted to assess the relative predictive contribution of race/ethnicity alongside clinical and operational features.

---

## Results
The analytic sample comprised 4,491 Non-Hispanic White (56.3%), 1,821 Non-Hispanic Black (22.8%), 1,314 Hispanic (16.5%), and 345 Non-Hispanic Other (4.3%) visits. Hispanic patients waited significantly less than Non-Hispanic White patients in the bivariate model (β = −0.120, 95% CI [−0.204, −0.037], p = 0.005), corresponding to approximately 11.3% shorter wait times. This effect strengthened after adjustment for triage urgency (M2: β = −0.135, p = 0.001), insurance type (M3: β = −0.139, p = 0.002), and all covariates (M4: β = −0.161, 95% CI [−0.246, −0.076], p = 0.0002), representing approximately 14.8% shorter wait times in the fully adjusted model.

The amplification of the Hispanic coefficient upon entry of triage urgency suggests that IMMEDR functioned as a suppressor variable rather than a confounder, consistent with potential undertriage of Hispanic patients relative to clinical need. No significant disparity was observed for Non-Hispanic Black patients across any model specification (M4: β = −0.008, 95% CI [−0.082, 0.067], p = 0.843). Non-Hispanic Other patients showed a non-significant trend toward shorter wait times (M4: β = −0.127, 95% CI [−0.274, 0.019], p = 0.089); the wide confidence interval likely reflects limited statistical power in this subgroup (n = 345), which also pools heterogeneous racial categories. Model R² increased from 0.001 (race only) to 0.032 (full model), with triage urgency accounting for the largest incremental gain.

SHAP analysis confirmed that race/ethnicity ranked last among predictors of long versus short wait, behind age, arrival hour, triage level, insurance type, sex, and EMS arrival, suggesting that while the racial disparity is statistically robust, its magnitude is modest relative to operational and demographic determinants of wait time.

---

## Conclusions
Hispanic patients experienced significantly shorter ED wait times than Non-Hispanic White patients in this nationally representative sample, an effect that persisted and strengthened after adjustment for triage urgency and insurance type. The suppressor pattern observed for triage urgency is consistent with the hypothesis that Hispanic patients may be systematically assigned less urgent triage codes relative to their clinical presentations, warranting further investigation into undertriage as a potential mechanism. These findings highlight the complexity of interpreting racial disparities in ED operations and underscore the value of examining both statistical significance and clinical mechanism when analyzing health equity data.

---

## Limitations
- Cross-sectional design precludes causal inference
- Triage urgency (IMMEDR) was missing for approximately 36% of the original sample prior to listwise deletion
- The Non-Hispanic Other category is heterogeneous (pools Asian, AIAN, NHPI, and multiracial patients)
- Hospital-level clustering effects were not modeled
- NHAMCS data do not include acuity measures beyond triage level, limiting the ability to directly test undertriage as a mechanism

---

## Data & Code
- **Dataset:** NHAMCS 2022 Emergency Department Public Use File (CDC/NCHS)
- **Repository:** [github.com/ayy001-star/nhamcs-ed-disparities](https://github.com/ayy001-star/nhamcs-ed-disparities)
- **Notebooks:** `NHAMCS.ipynb` (cleaning), `02_model.ipynb` (OLS), `03_ml.ipynb` (ML/SHAP)
- **Variable documentation:** `CODEBOOK.md`
- **Source documentation:** `doc22-ed-508.pdf` (CDC/NCHS, July 2024)
