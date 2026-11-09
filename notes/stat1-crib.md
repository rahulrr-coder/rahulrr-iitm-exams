# Stat 1 (IITM BS Foundation) — Exam Crib Sheet
*Built from Weeks 1–4 PPTs/Transcripts + 9 PYQ practice papers. Exam: tomorrow.*

---

## Part 1 — Exam pattern (from 9 practice papers)

Every paper: 17–23 questions, 36–40 marks, mix of MCQ (single answer), MSQ (multi-select), SA (numeric entry, often with a decimal-accuracy tolerance). First question is always the "confirm your subject" dummy (0 marks). Recurring topic clusters, ranked by how often they appear across the 9 papers:

| Frequency | Topic cluster |
|---|---|
| Every paper | Descriptive vs. inferential stats; population vs. sample (representativeness) |
| Every paper | Scales of measurement (nominal/ordinal/interval/ratio) + categorical vs. numerical, discrete vs. continuous, cross-sectional vs. time series |
| Almost every paper | Mean/median/mode + effect of transformations (add/multiply constant) |
| Almost every paper | Variance & SD (population vs. sample) + effect of transformations |
| Most papers | Percentiles, quartiles, IQR, outliers |
| Most papers | Contingency tables & association (row/column relative frequency) |
| Most papers | Covariance & correlation coefficient (r) |
| ~4 of 9 | Point bi-serial correlation coefficient |
| Frequent as MCQ/MSQ | Charts: pie/bar/Pareto/stacked bar, area principle, misleading graphs |
| Occasional | Stem-and-leaf plots, frequency/relative-frequency tables |

**Takeaway:** Weeks 1, 3, and 4 dominate the marks. Week 2 (charts) shows up mostly as quick conceptual MCQs, not calculations. Prioritize accordingly if time gets tight.

---

## Part 2 — Concept Map by Week

### Week 1 — Foundations of Data

- **Statistics**: "the art of learning from data" (collection → description → analysis → conclusions).
- **Descriptive vs. inferential**: descriptive = summarize; inferential = generalize from sample to population (needs probability). A study on a *sample* can still be purely descriptive if you don't generalize beyond it.
- **Population vs. sample**: sample must be *representative* — missing an entire subgroup breaks representativeness even if it's technically a subset.
- **Data**: facts/figures collected & summarized; doesn't "speak" by itself. Comments, likes, multimedia all count as data.
- **Structured vs. unstructured data**: structured = organized rows/columns; unstructured = scattered, no context.
- **Variables & cases (tidy data rules)**: each variable → one column; each case → one row; consistent unit per variable column. A column constant across all cases is *not* a variable.
- **Missing (NA) ≠ 0**: a bowler who never bowled → NA; a bowler who bowled and took 0 wickets → 0. Don't conflate.
- **Categorical vs. numerical**: categorical = group membership (gender, blood group); numerical = has measurement units (marks, height). Gotcha: jersey number / mobile number *look* numeric but are categorical (arithmetic on them is meaningless).
- **Discrete vs. continuous** (numerical only): discrete = whole-number counts; continuous = any fractional value.
- **Measurement units**: must be consistent across all observations of a variable (don't mix cm and feet).
- **Cross-sectional vs. time series**: time series = same variable tracked over time (→ timeplot); cross-sectional = observed at one point in time.
- **Scales of measurement** (the single most-tested Week 1 concept):
  - **Nominal**: labels only, no order (gender, blood group, jersey number).
  - **Ordinal**: labels + order, but unequal/undefined gaps between ranks (poor/good/excellent).
  - **Interval**: order + meaningful differences (subtraction valid), but **no true zero** → ratios meaningless. Classic example: °C/°F — 40°C is *not* twice as hot as 20°C (only Kelvin has an absolute zero).
  - **Ratio**: interval + true zero → ratios *are* meaningful; full arithmetic valid (height, weight, marks, runs). 300 runs really is twice 150 runs.
  - Categorical data → nominal/ordinal only. Numerical data → interval/ratio only.

### Week 2 — Describing Categorical Data (single variable)

- **Frequency distribution**: count per distinct category. **Relative frequency** = frequency ÷ total n; always sums to 1 (used to compare datasets of different sizes).
- **Pie chart**: wedge angle = relative frequency × 360°. Shows **share of a whole**. Avoid exploding/3D slices.
- **Bar chart**: bar height = frequency; bars equal width, **not touching**. Shows **comparison across groups**, not proportions of a whole.
- **Pareto chart**: bar chart sorted by frequency (descending) — but **only valid for nominal data**. If the variable is ordinal (e.g., S/M/L), you must keep the natural order instead of sorting by frequency.
- **Area principle**: area shown must be proportional to the data it represents. Violations: *decorated graphics* (icons of uneven size) and *truncated graphs* (non-zero baseline exaggerates differences) — if you must truncate, explicitly mark the axis break.
- **Round-off errors**: individually-rounded percentages may not sum to exactly 100% — always check totals (matters for pie chart degrees summing to 360°).
- **Mode**: highest-frequency category; works for nominal *and* ordinal. Can be bimodal/multimodal.
- **Median (ordinal data only)**: middle value once ranked; undefined for nominal data. **Mode ≠ median in general** — mode = most frequent, median = middle-ranked; they need not coincide.
- **Best practice**: use "Other" bucket for many small categories instead of silently dropping them; always label axes/title/legend.

### Week 3 — Describing Numerical Data (the calculation-heavy core)

- **Frequency tables**: discrete data with few distinct values → one class per value. Continuous data → grouped into classes (5–20 classes, rule of thumb); convention: interval includes its **left** end, excludes its **right** end (e.g., "30–40" includes 30, not 40).
- **Histogram**: bars touch (no gaps) since data is continuous — this is the key visual difference from a bar chart.
- **Stem-and-leaf plot**: stem = all digits except last, leaf = last digit; leaves sorted ascending within each stem row. Retains actual values (unlike histogram).
- **Mean**: x̄ = Σx/n (sample), μ = Σx/N (population). Grouped discrete: x̄ = Σfᵢxᵢ/n (exact). Grouped continuous: x̄ = Σfᵢmᵢ/n using class **midpoints** (approximation only).
  - ⚠️ Mean is **highly sensitive to outliers**.
- **Median**: middle of sorted data. n odd → the ((n+1)/2)-th value. n even → average of the two middle values.
  - ⚠️ Median is **NOT** sensitive to outliers.
- **Mode**: most frequent value; may not exist, may be multiple.
- **Transformation rules** (memorize this table cold — tested constantly):

| Transform yᵢ = xᵢ + c | Transform yᵢ = xᵢ × c |
|---|---|
| Mean: ȳ = x̄ + c | Mean: ȳ = x̄ × c |
| Median: +c | Median: ×c |
| Mode: +c | Mode: ×c |
| Variance: **unchanged** | Variance: × c² |
| SD: **unchanged** | SD: × c (not c²) |

- **Why dispersion measures matter**: {3,3,3,3,3} and {1,2,3,4,5} have identical mean/median/mode but obviously different spread.
- **Range** = Max − Min. Extremely outlier-sensitive (uses only 2 points).
- **Variance**: uses *all* points, squared deviations from the mean.
  - Population: σ² = Σ(xᵢ−μ)²/N
  - Sample: s² = Σ(xᵢ−x̄)²/**(n−1)** ← don't forget n−1 for sample variance.
- **SD** = √variance. Restores original units (variance has squared units).
- **Percentiles** — two different valid algorithms give different answers, know both:
  - *Manual*: sort data; compute n·p. If not integer → round **up**, take that ranked value. If integer → average that rank and the next.
  - *Google Sheets* `PERCENTILE()`: rank = p(n−1)+1; interpolate between the integer and fractional parts.
- **Quartiles**: Q1 = 25th pct, Q2 = median, Q3 = 75th pct. **Five-number summary**: Min, Q1, Q2, Q3, Max.
- **IQR** = Q3 − Q1. More outlier-robust than range/SD.

### Week 4 — Association Between Two Variables

- **Association ≠ causality** — course only ever claims association.
- **Contingency table**: rows/columns = category levels, cells = counts, margins = row/column totals. Preserve natural order for ordinal variables (don't let software alphabetize).
- **Row/column relative frequency**: divide cell by its row (or column) total.
  - **Rule**: if relative frequencies are ~same across all rows → **no association**. If they differ noticeably → **associated**. (Row-wise and column-wise checks agree.)
- **Stacked bar chart** (raw counts) vs. **100% stacked bar chart** (normalized proportions — best for comparing shares across groups).
- **Scatter plot**: explanatory variable (x) vs. response variable (y). Describe using **D-C-V-O**: Direction, Curvature, Variation, Outliers. Course only quantifies **linear** association.
- **Covariance**: Cov(x,y) = Σ(xᵢ−x̄)(yᵢ−ȳ)/(n−1) [sample] or /N [population]. Sign tells direction; magnitude hard to interpret (has mixed units).
- **Correlation (Pearson's r)** = Cov(x,y)/(sₓ·sᵥ). Unitless, always in [−1, +1]. |r| near 1 → strong linear association; near 0 → weak/none. Sign = direction, doesn't depend on axis choice.
- **Best-fit line**: y = mx + c. Sign of slope m = direction. **R² = r²** (proportion of variance explained); R² tells fit *strength*, not direction.
- **Point bi-serial correlation** (numerical variable X vs. **dichotomous** categorical Y, coded 0/1):
  rpb = (Ȳ₀ − Ȳ₁)/sₓ × √(p₀p₁) — split by group, use group means and group proportions.
  - ⚠️ Sign flips if you swap which category is coded 0 vs 1 — only |rpb| indicates strength.
  - Line-fitting doesn't apply here (x only takes two values).

---

## Part 3 — One-Page Formula Sheet

```
Mean (sample):        x̄ = Σx / n
Mean (grouped):        x̄ = Σ(f·x) / n   [exact, discrete]  or  Σ(f·midpoint) / n  [approx, continuous]
Median:                n odd → ((n+1)/2)-th value; n even → avg of two middle values
Sample variance:        s² = Σ(x − x̄)² / (n − 1)
Population variance:    σ² = Σ(x − μ)² / N
SD:                    s = √s²
Percentile (manual):    n·p not integer → round up, take that rank; integer → avg that rank & next
IQR:                    Q3 − Q1  (Q1, Q3 via percentile method, p = 0.25, 0.75)
Sample covariance:      Σ(x−x̄)(y−ȳ) / (n − 1)
Correlation r:          Cov(x,y) / (sx · sy)      [always −1 ≤ r ≤ 1]
R²:                    r²
Point bi-serial:        rpb = (Ȳ0 − Ȳ1)/sx × √(p0·p1)
Pie slice angle:        relative frequency × 360°

Transform y = x + c:    mean/median/mode shift by c; variance & SD UNCHANGED
Transform y = c·x:      mean/median/mode scale by c; variance scales by c²; SD scales by c
```

---

## Part 4 — Curated Practice (aim: 60–90 min)

Papers are in your `PYQs` folder. Short codes used below:

| Code | File |
|---|---|
| P1 | 2023_july_iit_m_foundation_an4_exam... |
| P2 | 2023_oct_iit_m_qualifier_exam_qpq2... |
| P3 | 2024_feb25_iit_m_an4_exam_qdf4... (1) |
| P4 | 2024_july07_iit_m_an_exam_qdf4... |
| P5 | 2024_oct27_iit_m_an_exam_qdd2... |
| P6 | 2025_feb23_iit_m_an_exam_qip4... (1) |
| P7 | 2025_jul13_iit_m_an_exam_qio4... |
| P8 | 2025_oct26_iit_m_an_exam_qim4... |
| P9 | statistics1_15_mar_26... (most recent — closest in style to your exam) |

### A. Calculation problems — solve by hand, then check the answer key in that PDF

Fully self-contained (all numbers given in the question, no missing table/image needed). Do these first — together they cover mean/median/mode, transformations, variance/SD, percentiles/IQR, and correlation.

- [ ] **P1 Q6** — mean/variance correction after a mis-recorded value; find corrected sample SD.
- [ ] **P1 Q14–16** — t-shirt prices; Q1, Q3, outlier count.
- [ ] **P2 Q15** — 5-value dataset; IQR.
- [ ] **P2 Q13** — t-shirt sizes; effect of adding a value on median/mode.
- [ ] **P4 Q13–15** — two students' marks related by a constant shift; mean and correlation.
- [ ] **P6 Q8** — 6-value dataset; range, median, 25th percentile, IQR.
- [ ] **P6 Q10–11** — snack prices; Q1, Q3, IQR.
- [ ] **P7 Q2** — adding a 7th test score; effect on mean/median/mode.
- [ ] **P7 Q7** — two small datasets; compare variability (range & variance).
- [ ] **P7 Q8** — solve for a missing value from the mean, then SD after a shift.
- [ ] **P7 Q9** — test times; percentile cutoff for top 20%.
- [ ] **P8 Q12** — mean & population variance given; solve for two unknown values.
- [ ] **P9 Q12** — 9-value dataset; IQR.
- [ ] **P9 Q15** — 10-value dataset; median.

### B. Conceptual pattern-recognition — flip to these in the PDFs (5–10 sec each, just check you'd pick the right option)

Go fast here — you already know the concepts from Part 2, this is just pattern-matching practice on how IITM phrases the traps.

**Descriptive vs. inferential / population vs. sample**:
  - [ ] P1 Q2
  - [ ] P2 Q3
  - [ ] P2 Q4
  - [ ] P3 Q6
  - [ ] P4 Q9
  - [ ] P5 Q2
  - [ ] P6 Q6
  - [ ] P7 Q3
  - [ ] P7 Q5
  - [ ] P8 Q6
  - [ ] P9 Q4
**Scales of measurement / data types (nominal/ordinal/interval/ratio, discrete/continuous, cross-sectional/time-series)**:
  - [ ] P1 Q3
  - [ ] P1 Q10
  - [ ] P1 Q11
  - [ ] P2 Q12
  - [ ] P3 Q7
  - [ ] P4 Q3
  - [ ] P4 Q8
  - [ ] P6 Q2
  - [ ] P6 Q5
  - [ ] P7 Q3
  - [ ] P7 Q4
  - [ ] P8 Q5
  - [ ] P8 Q7
  - [ ] P9 Q2
  - [ ] P9 Q5
**Mode/median on categorical or small datasets (traps around "not defined")**:
  - [ ] P1 Q4
  - [ ] P2 Q6
  - [ ] P2 Q13
  - [ ] P3 Q8
  - [ ] P3 Q9
  - [ ] P4 Q2
**Contingency tables & association (row/column relative frequency)**:
  - [ ] P3 Q2
  - [ ] P3 Q10
  - [ ] P4 Q6
  - [ ] P4 Q7
  - [ ] P7 Q6
  - [ ] P9 Q7
  - [ ] P9 Q8
**Covariance/correlation conceptual (sign, ranking scatter plots by r, unitless-ness)**:
  - [ ] P1 Q12
  - [ ] P1 Q13
  - [ ] P4 Q10
  - [ ] P4 Q12
  - [ ] P9 Q6
  - [ ] P9 Q13
  - [ ] P9 Q16
**Point bi-serial correlation**:
  - [ ] P2 Q7
  - [ ] P2 Q8
  - [ ] P7 Q11
  - [ ] P9 Q6
**Charts / area principle / Pareto / stacked bar (mostly Week 2, quick MCQs)**:
  - [ ] P5 Q4
  - [ ] P5 Q14
  - [ ] P9 Q1
  - [ ] P9 Q3
**Transformation-effect questions (add/multiply constant → mean/variance/SD)**:
  - [ ] P2 Q9
  - [ ] P2 Q10
  - [ ] P6 Q14
  - [ ] P6 Q15
  - [ ] P7 Q10

### Suggested order for your 1–2 hours
1. Skim Part 2 concept map once, top to bottom (~15–20 min).
2. Do all 14 problems in Section A, then check each against the answer key at the end of its source PDF (~35–45 min).
3. Blitz through Section B's pointer list in the actual PDFs — don't re-derive, just confirm you instantly see the right answer (~20–25 min).
4. Re-read the transformation table and the scales-of-measurement bullets one more time right before the exam — these two are the highest-frequency "free marks" across all 9 papers.

You've got this — the pattern across 9 papers is extremely consistent, and you now have it mapped end to end.
