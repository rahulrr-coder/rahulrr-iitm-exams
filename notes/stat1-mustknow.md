# Stat 1 — Must-Know List (read this last, right before you walk in)

One screen. No new material, no derivations — just the things that show up in nearly every paper and are the most common places to lose an otherwise-easy mark.

## Highest-probability topics (appear in 8-9 of 9 papers)
1. Descriptive vs. inferential + population vs. sample
2. Scales of measurement (nominal/ordinal/interval/ratio) + data types
3. Mean/median/mode + transformation effects (+c, ×c)
4. Variance & SD (population vs sample) + transformation effects

## The 8 traps that cost the most marks (from every paper reviewed)
1. **Sample variance uses n−1, population variance uses n.** Mixing these up is the single most common silent error.
2. **Transformation rules** — memorize cold:
   - `+c`: mean/median/mode shift by c · variance & SD **unchanged**
   - `×c`: mean/median/mode scale by c · variance scales by **c²** · SD scales by **c** (not c²)
3. **Percentile rule**: sort → compute n·p → not integer = round **up**, take that rank → integer = average that rank and the next.
4. **"Sample" ≠ automatically inferential.** A study is only inferential if it generalizes BEYOND the sample to a larger population. Analyzing the sample itself = descriptive.
5. **Interval vs ratio**: the only question that matters is "does zero mean true absence, and are ratios meaningful?" (40°C isn't twice 20°C — no true zero → interval. 300 runs is twice 150 runs — true zero → ratio.)
6. **Mode works on nominal data; median does NOT** (median needs order, nominal has none). This nominal/ordinal swap is the most repeated wrong-option trap across every paper.
7. **Mean is never valid for categorical data** — only mode (any categorical) and median (ordinal only). "Mean, median, mode can all summarize a categorical variable" is a recurring false MSQ option.
8. **y = x + c always gives correlation r = 1** (or −1 for y = −x + c) — don't recompute, just recognize the shape.

## Formula quick-hit
```
Sample variance: s² = Σ(x−x̄)²/(n−1)         Population variance: σ² = Σ(x−μ)²/N
SD = √variance
IQR = Q3 − Q1                                 Outlier fences = Q1−1.5·IQR, Q3+1.5·IQR
Correlation r = Cov(x,y)/(sx·sy)              R² = r²
Point bi-serial: pairs ONE numeric + ONE binary (0/1) categorical variable — nothing else
Pie slice angle = relative frequency × 360°
```

## Contingency table association — the one-line rule
Row (or column) relative frequencies **similar across all rows** → NOT associated. **Different across rows** → associated. Check either direction, they agree.

## Last check before you open the exam
- Read every option letter-by-letter — most wrong options are one flipped word away from correct (nominal↔ordinal, n↔n−1, Q1↔Q2, "at least"↔"at most").
- For SA questions with decimal tolerance, do the arithmetic once carefully rather than fast twice — most tolerance bands are narrow (±0.02 to ±0.05).
- If a question gives mean+variance instead of raw numbers, it wants you to work backward through Σx and Σx² — that's not a sign you're missing information.

You know this. Go.
