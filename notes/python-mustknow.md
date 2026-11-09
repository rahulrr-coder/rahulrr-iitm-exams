# Python Quiz 1 — Must-Know List (read this last, right before you walk in)

One screen. No new material — just the things that show up in nearly every paper and the places this exam takes marks off people who actually know Python.

## Highest-probability topics (weeks 1–4, 70 questions across 19 papers)
1. **`if`/`elif`/`else` tracing + "which inputs give output X"** — 16 questions, the biggest cluster in the course.
2. **Digit extraction loops (`% 10`, `// 10`)** — 9 questions.
3. **Boolean expression evaluation (`not`/`and`/`or` precedence)** — 8 questions.
4. **Separate `if`s vs `elif`** — 5 questions, nearly always MSQ.
5. **Truthiness / `isinstance` / short-circuit** — 5 questions, including both difficulty-4 questions on record.

W3 + W4 are **84% of the marks**. If time runs out, W1 and W2 are what you drop.

## The 10 traps that cost the most marks

1. **Precedence is `not` → `and` → `or`.** `not True and False` is `(not True) and False` = `False`. `True or False and False` is `True`. Parenthesise on paper *before* substituting.
2. **In an `elif` chain the FIRST true condition wins and the rest are skipped.** Separate `if`s are each tested independently — several can fire, or none. The exam's favourite MSQ is an input that satisfies **two** conditions, because that's the only place the two versions differ.
3. **Earlier conditions carve out later ones.** `if x > 10` / `elif x > 5` means branch two owns `5 < x <= 10`, not `x > 5`. Always test the threshold itself and ±1.
4. **Accumulator identity: `0` for a sum, `1` for a product.** A product started at `0` returns `0` for every input — that's the planted bug, and it's an exam question twice.
5. **`while n > 0` never runs on input `0`** — you get the initial accumulator value straight back.
6. **Falsy is exactly `0`, `0.0`, `""`, `[]`, `{}`, `()`, `None`.** `"0"`, `" "`, `"False"`, `-1` and `[0]` are all **truthy**.
7. **`a or b` returns the first truthy operand, `a and b` the first falsy one — not a bool.** `0 or "x"` is `"x"`. `3 and 5` is `5`.
8. **`isinstance(True, int)` is `True`, but `isinstance(1, bool)` is `False`.** That asymmetry is the whole content of the two hardest questions in the pool.
9. **`/` always returns a float, even `4/2`.** And `//` **floors toward −∞** (`-7 // 2` is `-4`, not `-3`), while `%` takes the **sign of the divisor** (`-7 % 2` is `1`).
10. **`range(a, b)` excludes `b`** → `range(1, 11)` is ten values. The "final value of the loop variable" is the **first value that breaks the condition**, not the last one that passed.

## Quick-hit reference
```
not True and False -> False          True or False and False -> True
7/2 -> 3.5 (float)    7//2 -> 3    -7//2 -> -4    -7%2 -> 1    2**-1 -> 0.5
True + True -> 2      type(1<2<3) -> bool      a<b<c  ==  (a<b) and (b<c)
0 or "x" -> "x"       "" and 5 -> ""           3 and 5 -> 5     3 or 5 -> 3
isinstance(True,int) -> True         isinstance(1,bool) -> False
range(1,11) -> 10 values             range(10,0,-2) -> 10,8,6,4,2

while n > 0:            # input 0 -> body never runs
    d = n % 10          # peel
    s += d              # 0 for sum, 1 for product  <-- the trap
    n = n // 10         # drop
```

## The two rules that matter more than any fact above

- **Make the table.** Every `while` question: one row per iteration, one column per variable, plus the condition's truth value. Stop when it first fails. Never trace a loop in your head — that is where the marks actually go.
- **Test the boundaries.** For every "choose the correct snippet" question, run each candidate on the tie (equal values), the exact threshold, and a negative. The four planted bugs are always: independent `if`s printing twice, an `elif` chain in the wrong order, `>` where `>=` was needed, or a missing `else`.

## Last check before you open the paper
- `return` inside an `if` exits the function — later `elif`s never run.
- A variable assigned only inside an `if` raises `NameError` exactly when **every** condition is False.
- `&` and `|` are bitwise, not logical: `5 & 3` is `1`. If you see them, slow down.
- SA answers are exact numeric entry — do the arithmetic once carefully rather than twice fast.
- Read every MSQ option word by word. Most wrong options are one flipped token from correct (`if`↔`elif`, `>`↔`>=`, `and`↔`or`, `//`↔`/`).

63% MCQ · 20% SA · 17% MSQ. It's a tracing exam, and you've traced them all. Go.
