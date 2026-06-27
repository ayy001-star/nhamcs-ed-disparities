# CODEBOOK — NHAMCS 2022 ED Wait Time Disparity Analysis

Variable documentation for all columns used in this project.
Source: **2022 NHAMCS Emergency Department Public Use Data File Documentation** (`doc22-ed-508.pdf`)
Published by: National Center for Health Statistics (NCHS/CDC), July 2024

---

## Outcome Variable

### `WAITTIME` — Waiting Time to First Provider Contact (minutes)
Item 4 · Field length 4 · File location 8–11

Calculated from date/time of ED arrival and time of first provider (physician, APRN, or PA) contact.

| Code | Meaning |
|------|---------|
| 0–1280 | Wait time in minutes (reported range in 2022) |
| -7 | Not applicable — patient not seen by a physician/APRN/PA |
| -9 | Blank |

**Cleaning:** `-9` replaced with `pd.NA`. `-7` flagged via `NOT_SEEN_WAITTIME` but **not yet excluded from model data** — see known issue below.
**Role:** Dependent variable in all OLS models. Also modeled as `log(WAITTIME + 1)` to address right skew.

---

## Primary Predictor

### `RACERETH` — Race/Ethnicity (imputed)
Item 15 · Field length 1 · File location 32

CDC-imputed variable combining race and Hispanic ethnicity. Preferred over `RACEUN`/`ETHUN` due to lower missingness.

| Code | Meaning |
|------|---------|
| 1 | Non-Hispanic White |
| 2 | Non-Hispanic Black |
| 3 | Hispanic |
| 4 | Non-Hispanic Other (Asian, Native Hawaiian/PI, AIAN, multiracial) |

**Cleaning:** No missing codes; complete across all rows.
**Role:** Primary independent variable; used as `C(RACERETH)` in OLS models. **RACERETH=1 (Non-Hispanic White) is the reference group** in the current models.

> ⚠️ **Note:** An earlier version of the project codebook incorrectly listed codes as 1=Hispanic, 2=Non-Hispanic White, 3=Non-Hispanic Black. The official ordering above is correct. Model intercepts and group coefficients should be interpreted accordingly.

---

## Covariates

### `IMMEDR` — Immediacy With Which Patient Should Be Seen (triage level)
Item 34 · Field length 2 · File location 67–68

Based on PRF Item Triage Level. **Not imputed since 2012** — use with caution when combining across years.

| Code | Meaning |
|------|---------|
| 1 | Immediate |
| 2 | Emergent |
| 3 | Urgent |
| 4 | Semi-urgent |
| 5 | Nonurgent |
| 0 | No triage recorded, but facility *does* conduct nursing triage |
| 7 | Visit occurred at a facility that does *not* conduct nursing triage |
| -8 | Unknown |
| -9 | Blank |

**Cleaning:** `-9`, `-8`, `0`, and `7` replaced with `pd.NA`. **~36% of rows (5,818/16,025) are missing after cleaning** — a notable limitation addressed by listwise deletion.
**Role:** Key confounder. Higher triage urgency (lower code) → shorter expected wait time. Adding this covariate is the next modeling step.

> **Note on codes 0 and 7:** Code `0` means no triage was recorded at a facility that *does* triage — effectively missing. Code `7` means the visit occurred at a facility that *doesn't* triage at all; these patients were structurally never triaged, which is distinct from unknown triage. Both are excluded from the model, but the distinction is worth acknowledging in the limitations section.

### `PAYTYPER` — Recoded Primary Expected Source of Payment
Item 27 · Field length 2 · File location 46–47

Assigned using a hierarchy: Medicare > Medicaid/CHIP > Private Insurance > Worker's Compensation > Self-Pay > No Charge/Charity > Other > Unknown. Hierarchy changed in 2008 (dual-eligible Medicare/Medicaid recipients moved from Medicaid to Medicare).

| Code | Meaning |
|------|---------|
| 1 | Private insurance |
| 2 | Medicare |
| 3 | Medicaid, CHIP, or other state-based program |
| 4 | Worker's compensation |
| 5 | Self-pay |
| 6 | No charge / Charity care |
| 7 | Other |
| -8 | Unknown |
| -9 | Blank |

**Cleaning:** `-9`, `-8` replaced with `pd.NA` (1,737 missing).
**Role:** Insurance status as a proxy for socioeconomic position and care access. To be added in next modeling step.

### `AGE` — Patient Age (years)
Item 6 · Field length 3 · File location 16–18

Derived from date of visit and date of birth. Outlier values top-coded per NCHS confidentiality requirements.

| Code | Meaning |
|------|---------|
| 0 | Under 1 year |
| 1–93 | Age in years |
| 94 | 94 years or older (top-coded) |

**Cleaning:** No missing codes; no transformation applied.
**Role:** Potential covariate in future models.

### `SEX` — Patient Sex
Item 10 · Field length 1 · File location 25

| Code | Meaning |
|------|---------|
| 1 | Female |
| 2 | Male |

**Cleaning:** No missing codes in this dataset.
**Role:** Potential covariate in future models.

### `ARREMS` — Arrival by Ambulance
Item 16 · Field length 2 · File location 33–34

| Code | Meaning |
|------|---------|
| 1 | Yes — arrived by EMS/ambulance |
| 2 | No |
| -8 | Unknown |
| -9 | Blank |

**Cleaning:** `-9` replaced with `pd.NA` (106 missing).
**Role:** EMS arrivals are typically triaged immediately, reducing wait times independently of race. Potential covariate.

---

## Engineered Variables

### `ARRTIME` → `arrival_hour`
Item 3 · Field length 4 · File location 4–7

Raw variable `ARRTIME` is arrival time in military HHMM format (e.g., 1430 = 2:30 PM). Stored as string in `.dta` file; `-9` appears as the string `"-9"`.

**Derivation:**
```python
df["ARRTIME"] = pd.to_numeric(df["ARRTIME"], errors="coerce")
df["ARRTIME"] = df["ARRTIME"].replace([-9], pd.NA)   # 243 missing
df["arrival_hour"] = (df["ARRTIME"] // 100).astype("Int64")  # 0–23
```

**Role:** Controls for time-of-day effects on ED crowding and wait times.

### `NOT_SEEN_WAITTIME` — Patient Not Seen Flag
Boolean column: `True` if original `WAITTIME == -7`.

| Value | Meaning |
|-------|---------|
| True | Patient was not seen by a physician/APRN/PA (580 rows) |
| False | Patient was seen |

**Derivation:** `df["NOT_SEEN_WAITTIME"] = df["WAITTIME"] == -7`

> ⚠️ **Known issue:** These 580 rows have `WAITTIME = -7` and currently survive `dropna()` into the modeling dataset, because only `-9` was replaced with `pd.NA` in the cleaning step. The `-7` values are treated as a numeric wait time of −7 minutes in OLS, and cause `RuntimeWarning: invalid value encountered in log` in the log-transform model (where they're silently dropped, explaining the N drop from 8,247 → 7,971). **Fix:** add `-7` to the `replace()` call in `NHAMCS.ipynb` cell 7, or filter before modeling.

---

## Excluded Variables (Checked for Missingness Only)

### `ETHUN` — Ethnicity (unimputed)
Item 11 · Field length 2 · File location 26–27

| Code | Meaning |
|------|---------|
| 1 | Hispanic or Latino |
| 2 | Not Hispanic or Latino |
| -9 | Blank |

~14.6% missing. Use `RACERETH` (imputed) instead.

### `RACEUN` — Race (unimputed)
Item 13 · Field length 2 · File location 29–30

| Code | Meaning |
|------|---------|
| 1 | White |
| 2 | Black/African American |
| 3 | Asian |
| 4 | Native Hawaiian/Other Pacific Islander |
| 5 | American Indian/Alaska Native |
| 6 | More than one race reported |
| -9 | Blank |

~18.9% missing. Use `RACERETH` (imputed) instead.

---

## Sample Size Summary

| Stage | N |
|-------|---|
| Raw dataset | 16,025 |
| After listwise deletion (WAITTIME, IMMEDR, ARREMS, ARRTIME, PAYTYPER) | 8,247 |
| After log-transform (WAITTIME = −7 dropped as invalid) | 7,971 |

---

## Source Document

`doc22-ed-508.pdf` — *2022 National Hospital Ambulatory Medical Care Survey: Emergency Department Public Use Data File Documentation*
National Center for Health Statistics, CDC. Published July 2024.
[Download from CDC](https://www.cdc.gov/nchs/ahcd/ahcd_questionnaires.htm)

*Last updated: 2026-06-23*
