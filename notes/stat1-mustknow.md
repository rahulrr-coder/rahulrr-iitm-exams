# Stat 1 Quiz 2 — Must-Know List (read this last, right before you walk in)

One screen. No new material: just the patterns that carry the paper and the places where easy marks get lost.

## Where the marks are (weeks 5–9, 11 End Term papers)
1. **Two-stage "pick a box, then a ball"** → total probability, then Bayes. The biggest single pattern.
2. **Teams and committees** → nCr with include/exclude, or split into cases and add.
3. **nCr ÷ nCr probability** → favourable draws ÷ all draws.
4. **Independent events** → multiply; "at least one" = 1 − P(none).
5. **CDF questions (if W9 is in scope)** → P(X = a) is the jump at a.

## The 8 traps that cost the most marks
1. **P vs C:** roles, positions or prizes → P. Groups → C. "Captain and vice-captain" is P.
2. **"At least one" = total − none.** Never "choose one, then choose the rest freely": it double counts.
3. **Repeated letters:** divide by the factorial of **each** repeated letter's count.
4. **Exclusive ≠ independent.** Exclusive means P(A∩B) = 0. Independent means P(A∩B) = P(A)P(B).
5. **Conditional = shrink the total.** P(A | B) divides by P(B), not by 1, and not by P(A).
6. **The Bayes denominator is the whole total-probability sum,** not just the branch you care about.
7. **Without replacement:** update the counts after every draw. The draws are **not** independent.
8. **CDF strictness:** P(X ≥ a) = 1 − F(a⁻), not 1 − F(a). P(X < a) = F(a⁻).

## Formula quick-hit
```
nPr = n!/(n−r)!      nCr = nPr/r!      repeats: n!/(p!q!…)      together: glue × inside!
P(A∪B) = P(A)+P(B)−P(A∩B)              P(A|B) = P(A∩B)/P(B)
P(A) = Σ P(A|Bi)P(Bi)                  P(Bi|A) = P(A|Bi)P(Bi)/P(A)
at least one (indep.) = 1 − Π(1 − pi)  exactly one of two = p1(1−p2) + (1−p1)p2
Σ p(x) = 1    P(X=a) = F(a) − F(a⁻)    P(X>a) = 1 − F(a)
```

## Last check before you open the exam
- Draw the tree for every two-stage question, even an easy one. It takes 20 seconds and stops the most common slip.
- For SA answers, keep 4 decimals while you work and round only at the end.
- Read "with / without replacement", "at least / exactly / at most" and "given" in every stem before you touch a formula.
- Weeks 1–4 can come back: n−1 for sample variance, and Q1/Q3 by the percentile rule.

You've done 60 on Quiz 1 with less. Go get the 80.
