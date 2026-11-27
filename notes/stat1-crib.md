# Stat 1 (IITM BS Foundation) — Quiz 2 Crib Sheet

*Quiz 2: Sat 5 Dec 2026, in centre. New material is weeks 5–8; weeks 1–4 can reappear as review. Built from the 58 week 5–9 questions (157 marks) in the 11 End Term papers, 2022 Aug → 2026 May. Now also includes 10 real Quiz 2 papers from Apr 2023 to Aug 2026 (141 questions, 410 marks).*

**What the real Quiz 2 papers look like (10 papers, 2023–2026):** 40 marks in 11–18 questions. Share of all marks by week: W5 12%, **W6 31%**, W7 20%, **W8 29%**, and W1–4 review 7%. There is **no W9 in any paper**. The papers before Mar 2024 carried 3–14 marks of W1–4 review (IQR, quartiles, association), but none have since Aug 2024. Almost every paper has a Bayes or total-probability question worth 3–5 marks.

**Week labels follow the lecture PDFs.** W5 = lectures 5.1–5.2 (counting), W6 = 5.3–5.6 (permutations, combinations), W7 = 6.x (probability), W8 = 7.x (conditional probability, Bayes), W9 = 8.x (random variables, PMF, CDF). **W9 is probably out:** none of the 10 real Quiz 2 papers asked about it. Confirm on the portal; if the syllabus doesn't list it, skip it.

---

## Part 1 — What the questions look like

| Week | Topic | Q | Marks | What gets asked |
|---|---|---|---|---|
| W5 | Counting rules | 2 | 7 | Multiply choices slot by slot |
| W6 | Permutations & combinations | 13 | 37 | nPr/nCr equations, include/exclude teams, repeated letters, together/apart |
| W7 | Probability basics | 8 | 21 | Counting probability with nCr, unions, small sample spaces |
| W8 | Conditional probability & Bayes | 14 | 42 | **Total probability and Bayes (6 Q, 18 marks)**, independence, tables |
| W9 | Random variables, PMF, CDF | 21 | 50 | Support of X, PMF by counting, CDF jumps, unknown constant |

- **Mostly SA (numeric entry) and MCQ.** Write every intermediate number down; SA tolerances are tight.
- **The biggest pattern on the paper is the two-stage "pick a box, then pick a ball" question.** It never says "Bayes". Spot it from a partition (boxes, coins, machines, groups) plus a conditional rate in each part.
- **Counting is the engine for W7–W9.** A probability question is usually nCr ÷ nCr. If counting is shaky, three weeks fall over.

---

## Part 2 — Concept map by week

### W5 — Basic counting

- **Multiplication rule:** k independent slots with n₁, n₂, … choices → n₁·n₂·… ways.
- **Addition rule:** disjoint cases → add the counts.
- **Factorial:** n! = n·(n−1)·…·1, with 0! = 1.
- **Digit problems:** count the allowed digits place by place. The leading digit can't be 0.
  - *3-digit numbers with no 4:* hundreds 8 (not 0, not 4) × tens 9 × units 9 = **648**.
  - *4 subjects, each passed with one of 6 grades (S, A, B, C, D, E):* 6⁴ = **1296**.

### W6 — Permutations and combinations

| Situation | Formula |
|---|---|
| Order matters, r from n distinct | nPr = n! / (n−r)! |
| Order doesn't matter | nCr = n! / (r!(n−r)!) = nPr / r! |
| All n, with repeats p, q, r… | n! / (p!·q!·r!…) |
| Circular arrangement of n | (n−1)! |
| Symmetry | nCr = nC(n−r), nC0 = nCn = 1 |

**How to spot each pattern:**
- **"Captain and vice-captain", "1st/2nd/3rd prize", "arrange"** → order matters → **P**. *nP2 = 42 → n(n−1) = 42 → n = 7.*
- **"Committee", "team", "select", "handshakes"** → order doesn't matter → **C**.
  - *Must include 2 given people in a team of 4 from 8:* fix them, choose 2 from the other 6 → C(6,2) = **15**.
  - *Must exclude those 2:* choose all 4 from the other 6 → C(6,4) = **15**.
  - *20 men and 10 women shake hands only within their own gender:* C(20,2) + C(10,2) = 190 + 45 = **235**.
  - *"At least one":* use total − none, or add the disjoint cases (exactly 1 + exactly 2 + …). Don't do "pick one, then pick the rest", because it double counts.
- **Repeated letters:** *COMMITTEE* (9 letters; M, T, E twice each) → 9! / (2!·2!·2!) = **45360**. *ARRANGEMENT* (11 letters; A, R, N, E twice each) → 11! / (2!)⁴ = **2494800**.
- **Together:** glue the group into one block, arrange the blocks, then multiply by the arrangements inside the block. *LEADING with all vowels (E, A, I) together:* 5 units → 5! × 3! = **720**.
- **Not together:** total − together, or arrange the others first and put the restricted items in the gaps. *7 people in a row with A, B together and D, E apart:* (AB together) 6!·2 = 1440, minus (AB together and DE together) 5!·2·2 = 480, gives **960**.
- **Dictionary rank:** at each position, count the unused letters smaller than the actual letter × (remaining letters)!, add these up, then add 1. *SACHIN* → **601**.
- **Identity MSQs:** nPr / nCr = r! ✔ · nCr = nC(n−r) ✔ · "nPr = nCr / r!" ✘ (it is nCr · r!) · "permutations ignore order" ✘.
- **Solve for n:** test small n. *nⁿ − n! = 21 → n = 3 (27 − 6).*

### W7 — Probability

- **Equally likely outcomes:** P(E) = favourable / total. With draws, both are nCr counts.
  - *4 red, 5 blue, draw 3, all the same colour:* (C(4,3) + C(5,3)) / C(9,3) = 14/84 = **0.167**.
- **Axioms:** 0 ≤ P ≤ 1, P(S) = 1, P(Aᶜ) = 1 − P(A).
- **Union:** P(A ∪ B) = P(A) + P(B) − P(A ∩ B). Drop the last term only if A and B are **mutually exclusive**.
- **Three exclusive categories that cover everyone (F, D, Deg):** you are given P(F ∪ D) = 0.8 and P(D ∪ Deg) = 0.6. Since F + D + Deg = 1, D = 0.8 + 0.6 − 1 = **0.4**.
- **Small sample spaces:** write them out. *3-child family:* 8 outcomes. *Toss until two in a row match, stops on toss 3:* HTT, THH → 2/8 = **0.25**.
- **Mutually exclusive ≠ independent.** Two exclusive events with nonzero probability are always dependent.

### W8 — Conditional probability, independence, Bayes

- **Definition:** P(A | B) = P(A ∩ B) / P(B). "Given B" means **B is your new total**.
- **From a table:** take the row or column of the condition, then divide the cell by that row or column total.
- **From a PMF:** P(X ≤ 3 | X > 1) = [P(2) + P(3)] / [P(2) + P(3) + …]. Sum the values that satisfy both conditions and divide by the sum of the values that satisfy the given condition.
- **Multiplication rule:** P(A ∩ B) = P(A)·P(B | A). Use it for sequential draws without replacement: (r/N)·((r−1)/(N−1))…
- **Independence:** P(A ∩ B) = P(A)·P(B) ⇔ P(A | B) = P(A). Draws without replacement are **not** independent.
- **Independent events, quick results:**
  - At least one of n happens: 1 − Π(1 − pᵢ).
  - Exactly one of two: p₁(1 − p₂) + (1 − p₁)p₂. *Forecasters right with 4/7 and 2/3; contradict:* (4/7)(1/3) + (3/7)(2/3) = 10/21 = **0.48**.
- **Law of total probability** (partition B₁…Bₖ): P(A) = Σ P(A | Bᵢ)·P(Bᵢ).
- **Bayes:** P(Bᵢ | A) = P(A | Bᵢ)·P(Bᵢ) / P(A). The denominator is the total-probability sum you just computed.
  - *Pick one of two coins at random, fair or P(H) = 3/4. P(H) = ½·½ + ½·¾ = **0.625**. Given heads, P(fair) = 0.25 / 0.625 = **0.4**.*
- **Diagnostic test:** P(D | +) = P(+ | D)P(D) / [P(+ | D)P(D) + P(+ | Dᶜ)P(Dᶜ)]. Rare diseases give small answers, even with good tests.

### W9 — Random variables, PMF, CDF (check it's in the syllabus)

- **Random variable:** a number attached to every outcome. **Discrete** = countable values; **continuous** = an interval.
- **Support when drawing n from (good g, bad b):** X runs from max(0, n − b) to min(n, g). *10 white + 3 black, draw 4, X = whites:* {1, 2, 3, 4}.
- **PMF by counting (hypergeometric):** P(X = k) = C(g, k)·C(b, n−k) / C(g+b, n).
- **PMF rules:** p(x) ≥ 0 and Σ p(x) = 1. Use the second to find an unknown constant: *p(x) = kx for x = 1..4 → 10k = 1 → k = 0.1.*
- **CDF:** F(x) = P(X ≤ x). It never decreases, goes from 0 to 1, and is a right-continuous step function for discrete X.
  - Unknown constant: F(largest value) = 1. *F(x) = (x² + k)/99 on 1..8 → 64 + k = 99 → k = 35.*
  - **P(X = a) = jump at a** = F(a) − F(a⁻).
  - P(X ≤ a) = F(a) · P(X > a) = 1 − F(a) · **P(X ≥ a) = 1 − F(a⁻)** · P(a < X ≤ b) = F(b) − F(a).
  - Conditional from a CDF: P(X > 1 | X < 3) = [F(2) − F(1)] / F(2) for integer X.
- **Sum of two independent throws:** list the pairs. P(S = s) = Σ P(a)·P(b) over pairs with a + b = s.

---

## Part 3 — One-page formula sheet (Quiz 2)

```
COUNTING
  multiplication rule      n1 · n2 · … · nk
  nPr = n!/(n−r)!          nCr = n!/(r!(n−r)!) = nPr/r!        nCr = nC(n−r)
  repeated letters         n!/(p!·q!·…)                        circular  (n−1)!
  together  → glue block, ×(inside arrangements)      apart → total − together
  at least one             total − none

PROBABILITY
  P(E) = favourable/total     P(Aᶜ) = 1 − P(A)
  P(A∪B) = P(A)+P(B)−P(A∩B)   exclusive → P(A∩B) = 0
  P(A∪B∪C) = ΣP − Σpairs + P(A∩B∩C)

CONDITIONAL
  P(A|B) = P(A∩B)/P(B)        P(A∩B) = P(A)·P(B|A)
  independent ⇔ P(A∩B) = P(A)P(B)
  at least one (indep.)      1 − Π(1 − pi)
  total probability          P(A) = Σ P(A|Bi)·P(Bi)
  Bayes                      P(Bi|A) = P(A|Bi)P(Bi) / P(A)

RANDOM VARIABLES (W9)
  Σ p(x) = 1,  p(x) ≥ 0        F(x) = P(X ≤ x)
  P(X = a) = F(a) − F(a⁻)      P(X > a) = 1 − F(a)      P(X ≥ a) = 1 − F(a⁻)
  hypergeometric             P(X=k) = C(g,k)·C(b,n−k)/C(g+b,n)
  support                    max(0, n−b) … min(n, g)
```

### Weeks 1–4 review (they can come back on Quiz 2)

```
Mean x̄ = Σx/n     sample var s² = Σ(x−x̄)²/(n−1)     population var σ² = Σ(x−μ)²/N
Median: n odd → ((n+1)/2)th; n even → average of the two middle values
Percentile: n·p not an integer → round up, take that rank; an integer → average that rank and the next
IQR = Q3 − Q1      fences Q1 − 1.5·IQR, Q3 + 1.5·IQR
Cov = Σ(x−x̄)(y−ȳ)/(n−1)      r = Cov/(sx·sy)      R² = r²
y = x + c : centre shifts by c, spread unchanged      y = c·x : centre ×c, var ×c², SD ×|c|
Scales: nominal < ordinal < interval (no true zero) < ratio (true zero)
```

---

## Part 4 — Curated practice (all on the Stat 1 page; the answer is hidden until you reveal it)

Do them in this order. The ★ question is the archetype's target: solve it with help first, then do the rest cold.

| # | Archetype | Questions | Marks |
|---|---|---|---|
| 1 | **W8-A4 Total probability + Bayes** | ★2023 Dec Q7, 2023 Dec Q6, 2023 Sep Q5, 2025 Apr Q9, 2025 Dec Q13, 2022 Dec Q8 | 18 |
| 2 | W6-A2 Include/exclude teams | ★2025 Dec Q12, 2024 Dec Q7, Q8, 2023 Sep Q13 | 11 |
| 3 | W6-A1 nPr/nCr equations, identities | ★2022 Dec Q10, 2024 Sep Q6, Q13, 2025 Apr Q4 | 10 |
| 4 | W7-A2 nCr ÷ nCr probability | ★2025 Aug Q15, 2023 Sep Q12 | 7 |
| 5 | W8-A5 Without replacement, independence | ★2024 Dec Q11, 2025 Aug Q16 | 7 |
| 6 | W5-A1 Multiplication rule | ★2024 Apr Q9, 2026 May Q12 | 7 |
| 7 | W8-A2 / W8-A3 Tables, independent events | 2022 Aug Q8, 2024 Apr Q20, ★2024 Sep Q4, 2025 Aug Q9 | 12 |
| 8 | W6-A3 / A5 / A4 Letters, together/apart, rank | 2023 Sep Q10, 2025 Aug Q2, ★2024 Dec Q9, 2025 Apr Q8, 2022 Aug Q10 | 16 |
| 9 | W7-A3 / A4 / A6 Unions, sample spaces | 2024 Dec Q10, 2024 Sep Q5, 2026 May Q13, 2023 Dec Q11 | 10 |
| 10 | W9 (if it's in the syllabus) — CDF jumps, unknown k, support, PMF by counting | W9-A5, A4, A1, A2 first | 31 |

**Pass mark for yourself:** every ★ solved cold, plus 80% of rows 1–7, by Thursday 3 Dec.
