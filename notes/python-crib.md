# Programming in Python (BSCS1002) — Quiz 1 Crib Sheet

*Built from `WEEK_MAP.md` (weeks 1–4) + the 70 week-1–4 questions tagged across 11 Quiz 1 papers and 8 End Term papers (2023 Feb → 2026 Sep). Exam: **Sun 15 Nov 2026, 2:00–6:00 PM**, weeks 1–4 only.*

Companion file: `Python_MustKnow_Before_Exam.md` — read that one last, right before you walk in.

---

## Part 1 — Exam pattern (from 19 papers in scope)

70 questions fall inside weeks 1–4, worth 186 marks. Split: **MCQ 63% · SA 20% · MSQ 17%**.

| Week | Topic | Questions | Marks | Share | Avg difficulty |
|---|---|---|---|---|---|
| W1 | Introduction to algorithms — expressions, types, `//` and `%` | 8 | 17 | 9% | 1.3 |
| W2 | Conditionals — single `if`/`else`, chained comparison | 4 | 12 | 6% | 1.5 |
| **W3** | **Conditionals (cont.) — boolean logic, `if`/`elif` chains, nesting** | **39** | **95** | **51%** | **2.4** |
| **W4** | **Iterations and ranges — `while` tracing, digit extraction** | **19** | **62** | **33%** | **2.3** |

**W3 + W4 = 84% of the marks.** Everything is code tracing — there is no theory to recite. The entire exam is "substitute the inputs, walk the lines, report what prints".

Recurring clusters, ranked by how often they appear:

| Frequency | Cluster | Week |
|---|---|---|
| 8 questions | Boolean expression evaluation (`not`/`and`/`or` precedence) | W3 |
| 9 questions | Digit extraction loop (`% 10` and `// 10`) | W4 |
| 16 questions | `if`/`elif`/`else` tracing and "which inputs give output X" | W3 |
| 5 questions | Separate `if`s vs `elif` — equivalence and possible outputs | W3 |
| 5 questions | Truthiness, `isinstance`, short-circuit | W3 |
| 4 questions | Pick the loop that prints/accumulates a series | W4 |
| 4 questions | `while`-loop final value / iteration count | W4 |
| 4 questions | "Choose the snippet that is actually correct" | W3 |
| 3 questions | Expression type inference | W1 |
| 2 questions | Two-pointer `while` loop | W4 |
| 2 questions | Chained comparison type | W2 |
| 2 questions | Unassigned-variable `NameError` trap | W2 |

**Takeaway:** 2 of the 4 hardest-rated questions in the whole pool (`Q1 2026 Mar` Q17, Q18) are the *same* archetype — `isinstance` + truthiness counters. Learn that one pattern and you own 8 marks of the hardest material on the paper.

---

## Part 2 — Concept Map by Week

### Week 1 — Algorithms, expressions and types

- **Type rules — the whole of W1 in five lines:**
  - `int op int` → `int`, **except** `/` (always `float`) and `**` with a negative exponent (`2**-3` → `0.125`, a float).
  - `int op float` → `float`. Any float anywhere in the expression poisons the result to float: `7.0 // 2` → `3.0`, not `3`.
  - A quoted literal is `str` even when it looks like a number: `"7" + "2"` is `"72"`, not `9`.
  - `+` joins `str` with `str` only. `"a" + 1` → `TypeError`. `"ab" * 3` → `"ababab"` (str × int is legal).
  - `int()`, `str()`, `float()`, `len()` change the type **before the next operator sees it** — that's the point of the question.
- **`//` and `%`:** `//` floors, `%` keeps the remainder. The classic decomposition: `years = n // 365`, `weeks = (n % 365) // 7`, `days = (n % 365) % 7`.
  - ⚠️ `//` **floors toward −∞**, it does not truncate: `-7 // 2` is `-4`, not `-3`. And `%` takes the **sign of the divisor**: `-7 % 2` is `1`, not `-1`.
- **String slicing:** `s[a:b]` includes `a`, excludes `b` → length `b − a` (clipped at the ends). `s[:k]` is the first `k` characters. Count spaces you concatenate in — they're characters too.
- **f-strings with a width:** `f"{5:3}"` pads to 3 columns → `"  5"` (two spaces). The width is part of the output length.
- **Work inside-out.** Every W1 question is one expression. Evaluate the innermost call first, note its type, then apply the next operator to *that*.

### Week 2 — Conditionals (single branch)

- **Chained comparison:** `a < b < c` means `(a < b) and (b < c)` — and `b` is evaluated only once. The result is `bool`.
- **`bool` *is* an `int`:** `True == 1`, `False == 0`, `True + True == 2`. So `type(1 < 2)` is `bool`, but `(1 < 2) + 1` is `2`, an `int`. A comparison stays `bool` *unless an arithmetic operator is applied afterwards*.
- **Single `if`/`else` tracing:** substitute the inputs, follow exactly **one** branch, print. Write the variable values in the margin — don't do it in your head.
- **The unassigned-variable trap:** if a name is assigned *only* inside an `if` body and then used after the block, the code raises `NameError` **exactly when every guarding condition is False**. The question is almost always "for which inputs does this error?" — answer: the inputs that satisfy none of the conditions.

### Week 3 — Conditionals continued (the half of the paper)

- **Operator precedence — memorize cold:** comparisons (`<`, `==`, …) → `not` → `and` → `or`.
  - So `not True and False` is `(not True) and False` = `False`.
  - And `True or False and False` is `True or (False and False)` = `True`.
  - Parenthesise mentally before you substitute, then reduce innermost first.
  - For "deduce the variable" questions: **`not not x` is `x`** — undo `not` by `not`.
- **`if`/`elif`/`else` chains: the FIRST true condition runs, every later one is skipped.** This is the single most-tested fact in the course.
- **Separate `if`s vs `elif` — the difference that the MSQs live on:**
  - Separate `if`s are each tested independently → **several can fire, or none**. Output can print twice.
  - `elif`/`else` makes branches **mutually exclusive** → exactly one fires (with an `else`), at most one (without).
  - To find where two versions differ: **look for an input that satisfies two conditions at once.** That input is the answer.
- **"Which inputs give output X" questions:** write down the interval each branch actually owns, remembering that earlier conditions **carve out** later ones. `if x > 10` then `elif x > 5` means the second branch owns `5 < x <= 10`, not `x > 5`. Then test boundary values explicitly: the threshold itself, and ±1.
- **Counting inputs:** for a nested-range question ("how many integer pairs print Yes"), count integers in the rectangle/interval **inclusive of both ends** — `a <= x <= b` has `b − a + 1` integers.
- **Truthiness:** falsy values are `0`, `0.0`, `""`, `[]`, `{}`, `()`, `None`. **Everything else is truthy** — including `"0"`, `" "`, `"False"`, `-1`, and `[0]`.
- **Short-circuit returns the operand, not a bool:**
  - `a or b` → the **first truthy** operand (or the last one if all falsy): `0 or "x"` is `"x"`, `3 or 5` is `3`.
  - `a and b` → the **first falsy** operand (or the last one if all truthy): `"" and 5` is `""`, `3 and 5` is `5`.
- **`isinstance`:** `isinstance(True, int)` is **`True`** (bool subclasses int) but `isinstance(1, bool)` is **`False`**. This asymmetry is the whole point of the two hardest questions in the pool.
- **Bitwise `&`/`|` are not `and`/`or`:** they operate on the integer bits — `5 & 3` is `1`. On two bools they do behave like logical ops (`True & False` is `False`) and return `bool`, but they **do not short-circuit** and they bind *tighter* than comparisons would suggest. If you see `&` or `|`, slow down.
- **`return` inside an `if` exits the function immediately** — nothing after it in the function runs, including later `elif`s.
- **"Choose the snippet that is correct" questions:** don't read for elegance, **test each candidate with the nasty inputs** — equal values (ties), exactly on the threshold, and a negative. The bugs planted are always one of: independent `if`s printing twice, an `elif` chain in the wrong order, `>` where `>=` is needed, or a missing `else`.

### Week 4 — Iterations and ranges

- **`range(start, stop, step)` excludes `stop`.** `range(1, 11)` yields 10 values, 1 through 10. `range(10, 0, -2)` yields `10, 8, 6, 4, 2`. Number of values = `ceil((stop − start) / step)`.
- **"First hundred powers of two" means 100 iterations**, with the multiplier updated every pass. Check three things on every candidate loop: the **first** value printed, the **last** value printed, and the **number** of iterations. One of the distractors is always off by one at exactly one of those three.
- **The digit-extraction skeleton — this is 9 questions:**
  ```python
  while n > 0:
      d = n % 10        # peel the last digit
      # <<< the only line that changes between questions >>>
      n = n // 10       # drop it
  ```
  What sits in the middle is sum (`s += d`), product (`p *= d`), reverse (`r = r*10 + d`), positional weight (`t += d * w; w *= 10`), or a filter (`if d % 2: s += d`).
  - ⚠️ **Start the accumulator at the identity: `0` for a sum, `1` for a product.** A product started at `0` returns `0` for every input — that is the standard planted trap, and `Q1 2023 Jul` Q11 is exactly it.
  - ⚠️ `while n > 0` means **input `0` runs the body zero times** → you get the accumulator's initial value back.
  - ⚠️ Digit loops assume a positive `n`. On a negative input the loop body never runs.
- **`while`-loop tracing — do not do it in your head. Make a table**, one row per iteration, one column per variable, plus a column for the condition's truth value. Stop when the condition **first fails**.
  - "Final value of the loop variable" = the **first value that violates the condition**, not the last one that satisfied it.
  - "Iteration count" = the number of rows in your table. Count rows, don't estimate.
- **Two-pointer loop:** `i` starts at the left end, `j` at the right end, and you compare `a[i] + a[j]` with the target:
  - sum too **big** → `j -= 1` (shrink from the right)
  - sum too **small** → `i += 1` (grow from the left)
  - loop runs `while i < j`; when the pointers **cross**, nothing was found → returns `None`/`False`. The "for which arguments does it return None" question is asking you to find the input with no valid pair.
- **Fibonacci-style loops** (`a, b = b, a + b`): the simultaneous assignment uses the **old** values of both on the right-hand side. Write both variables per row or you will get it wrong.

---

## Part 3 — One-Page Reference

```
PRECEDENCE (low to high):   or  <  and  <  not  <  comparisons  <  arithmetic
                            not True and False  ==  (not True) and False  ==  False
                            True or False and False  ==  True or (False and False)  ==  True

TYPES    int/int -> float ALWAYS        7/2 = 3.5
         int//int -> int                7//2 = 3        -7//2 = -4   (floors, not truncates)
         int%int  -> sign of DIVISOR    -7%2 = 1
         int**neg -> float              2**-1 = 0.5
         any float in -> float out      7.0//2 = 3.0
         bool IS int                    True+True = 2    isinstance(True,int) -> True
                                                          isinstance(1,bool)  -> False

FALSY (exactly these)   0   0.0   ""   []   {}   ()   None
TRUTHY (watch out)      "0"   " "   "False"   -1   [0]   0.1

SHORT-CIRCUIT returns an OPERAND, not a bool
         a or  b  -> first TRUTHY (else last)     0 or "x" -> "x"     3 or 5 -> 3
         a and b  -> first FALSY  (else last)     "" and 5 -> ""      3 and 5 -> 5

RANGE    range(a, b)        -> b-a values, a .. b-1          range(1,11) -> 10 values
         range(a, b, s)     -> ceil((b-a)/s) values          range(10,0,-2) -> 10,8,6,4,2

DIGIT LOOP                            SERIES LOOP CHECKLIST
  s = 0        # 1 for product          1. first value printed?
  while n > 0:                          2. last value printed?
      d = n % 10                        3. how many iterations?
      s += d   # the variable line
      n = n // 10

BRANCHES  elif chain  -> FIRST true wins, rest skipped, at most one fires
          separate ifs -> each tested independently, MANY or NONE can fire
          difference shows up only on inputs satisfying TWO conditions
          name assigned only inside an if -> NameError when all conditions False
          return inside an if -> function exits, later elifs never run
```

**Paper label → file map** (for the pointers in Part 4):

| Label | File | Label | File |
|---|---|---|---|
| Q1 2023 Feb | `PYQs/Quiz1/Quiz1_2023-02-26.pdf` | ET 2023 Apr | `PYQs/EndTerm/EndTerm_2023-04-30.pdf` |
| Q1 2023 Jul | `PYQs/Quiz1/Quiz1_2023-07-16.pdf` | ET 2023 Sep | `PYQs/EndTerm/EndTerm_2023-09-03.pdf` |
| Q1 2023 Oct | `PYQs/Quiz1/Quiz1_2023-10-29.pdf` | ET 2023 Dec | `PYQs/EndTerm/EndTerm_2023-12-24.pdf` |
| Q1 2024 Feb | `PYQs/Quiz1/Quiz1_2024-02-25.pdf` | ET 2024 Sep | `PYQs/EndTerm/EndTerm_2024-09-01.pdf` |
| Q1 2024 Jul | `PYQs/Quiz1/Quiz1_2024-07-07.pdf` | ET 2024 Dec | `PYQs/EndTerm/EndTerm_2024-12-22.pdf` |
| Q1 2024 Oct | `PYQs/Quiz1/Quiz1_2024-10-27.pdf` | ET 2025 Apr | `PYQs/EndTerm/EndTerm_2025-04-13.pdf` |
| Q1 2025 Feb | `PYQs/Quiz1/Quiz1_2025-02-23.pdf` | ET 2025 Aug | `PYQs/EndTerm/EndTerm_2025-08-31.pdf` |
| Q1 2025 Jul | `PYQs/Quiz1/Quiz1_2025-07-13.pdf` | ET 2026 Sep | `PYQs/EndTerm/EndTerm_2026-09-13_session2.pdf` |
| Q1 2025 Oct | `PYQs/Quiz1/Quiz1_2025-10-26.pdf` | | |
| Q1 2026 Mar | `PYQs/Quiz1/Quiz1_2026-03-15.pdf` | | |
| Q1 2026 Jul | `PYQs/Quiz1/Quiz1_2026-07-16.pdf` | | |

Or skip the PDFs and use the trainer: `python3 -m http.server 8000` in `rahulrr-iitm-exams/`, then `python.html` — same questions as images with the answer hidden until you ask, and tick-off tracking.

---

## Part 4 — Curated Practice (aim: 90–120 min)

Ordered by marks bought per minute. **Trace with a pen — one table per loop, one margin note per branch.** Guessing from the shape of the code is how this paper gets you.

### A. The two big archetypes — do these first (≈60 min, 100+ marks of pattern)

**A1. `if`/`elif`/`else` tracing and input-set questions** — 16 questions, the largest single cluster:
- [ ] **Q1 2023 Feb Q16, Q17, Q18, Q19** — four 1-mark warm-ups on the same chain. Start here, they calibrate you.
- [ ] **Q1 2023 Jul Q6** — if/elif/else comparison result.
- [ ] **Q1 2023 Jul Q3** — find the inputs where nested ifs print **nothing**.
- [ ] **Q1 2024 Jul Q6** — MSQ: which inputs produce a given category (boundary hunting).
- [ ] **Q1 2024 Oct Q9** — SA: nested if with integer division.
- [ ] **Q1 2025 Feb Q9** — SA: conditional using `min()`.
- [ ] **Q1 2025 Feb Q12 + Q13** — MSQ pair: which boolean inputs print True / print False.
- [ ] **Q1 2023 Oct Q13** — SA: **count** the integer points satisfying nested range conditions.
- [ ] **ET 2025 Apr Q15** — MSQ: verify statements about temperature-band output.
- [ ] **Q1 2025 Jul Q8** — MSQ: parity output of a function with an if/elif chain.
- [ ] **Q1 2025 Oct Q9** — MSQ: possible outputs of a nested conditional over all inputs.
- [ ] **Q1 2023 Jul Q7** — identify the correct statement about nested if/else outputs.
- [ ] **ET 2024 Dec Q7** — which `return` executes when the arguments are equal.

**A2. Digit extraction (`% 10` / `// 10`)** — 9 questions, and once you've seen the skeleton they're free marks:
- [ ] **Q1 2024 Jul Q11** — SA: trace a digit-sum loop.
- [ ] **Q1 2025 Feb Q11** — SA: product of digits.
- [ ] **Q1 2026 Jul Q10** — SA: sum of **odd** digits only (the filter variant).
- [ ] **Q1 2026 Mar Q5 + Q6** — pair: each digit weighted by its position.
- [ ] **ET 2023 Apr Q3** and **ET 2023 Sep Q8** — pick the loop computing the product of digits (same question, two papers).
- [ ] **Q1 2023 Jul Q11** — digit reversal traced with a **wrong initial value**. This is the accumulator-identity trap; get it wrong once here, never again.
- [ ] **ET 2023 Apr Q18** — MSQ: pick the snippets that correctly reverse an integer.

### B. Boolean logic blitz — 8 questions, 5 seconds each once precedence is reflex (≈15 min)

Two papers ask the **same four questions**. Do one set, then use the other as a self-test.
- [ ] **ET 2023 Apr Q25, Q26, Q27, Q28**
- [ ] **ET 2023 Sep Q14, Q15, Q16, Q17**
- [ ] **Q1 2023 Feb Q2** — deduce the variable from repeated `not` (`not not x` is `x`).

### C. The separate-`if`s-vs-`elif` family — where the MSQ marks hide (≈20 min)

- [ ] **Q1 2023 Oct Q9** — MSQ: which inputs produce the *fourth* output, because the `if`s are independent.
- [ ] **ET 2024 Dec Q3** — compare outputs when the second condition is `if` vs `elif`.
- [ ] **ET 2023 Dec Q10** — MSQ: is an if/else block equivalent to sequential prints?
- [ ] **Q1 2025 Feb Q6** — MSQ: which **lines execute** across separate if blocks.
- [ ] **Q1 2024 Oct Q6** — MSQ: correct statements about an abs/add branch.

### D. Truthiness, `isinstance`, short-circuit — the 4-mark hard end (≈20 min)

Do these even if they feel slow. They are the only difficulty-4 questions in the pool and they repeat.
- [ ] **Q1 2026 Mar Q17 + Q18** — SA, 4 marks each: counter after `isinstance` checks combined with truthiness. **The two hardest questions on record, same pattern.**
- [ ] **Q1 2025 Oct Q4** — `or`/`and` over strings and integers (short-circuit returns an operand).
- [ ] **ET 2025 Aug Q3** — elif chain driven by falsy values.
- [ ] **ET 2026 Sep Q1** — bool/int conversions mixed with logical **and bitwise** operators.

### E. `while`-loop tracing and series selection (≈20 min)

- [ ] **Q1 2023 Oct Q16** — SA: loop variable's value after the loop ends (the easiest of the group — start here).
- [ ] **ET 2024 Dec Q10** — SA: count the iterations.
- [ ] **ET 2026 Sep Q10** — SA: count iterations of a loop that halves evens and decrements odds.
- [ ] **Q1 2024 Feb Q8** — SA: Fibonacci-like `while`; print the final term. (Write both variables per row.)
- [ ] **Q1 2023 Oct Q15** and **Q1 2025 Feb Q4** — select the loop printing the first hundred powers of two / of three.
- [ ] **Q1 2023 Feb Q6** — MSQ: which loops print the first ten positive even numbers.
- [ ] **Q1 2023 Jul Q10** — sum of a concatenated-digit series.
- [ ] **ET 2024 Dec Q17 + Q18** — the two-pointer pair: trace it, then find the arguments returning `None`.

### F. "Choose the correct snippet" + W1/W2 mop-up (≈15 min)

Cheap marks. Leave them to last but don't skip them — 29 marks sit in W1+W2 alone.
- [ ] **Q1 2024 Feb Q5** — minimum of three integers (test with ties).
- [ ] **ET 2024 Sep Q3** — age categorisation (test on the boundaries).
- [ ] **ET 2025 Apr Q8** — marks into ranges.
- [ ] **Q1 2023 Feb Q13, Q14, Q15** — expression type inference, 1 mark each.
- [ ] **Q1 2023 Jul Q5** — days → years/weeks/days via `//` and `%`.
- [ ] **Q1 2023 Oct Q8** — output of concatenated string literals.
- [ ] **Q1 2025 Feb Q8** — SA: length of a string built from slices plus a space.
- [ ] **Q1 2025 Oct Q5** — type conversions through list operations.
- [ ] **Q1 2026 Jul Q2** — f-string with a width after `int()` and `len()`.
- [ ] **Q1 2024 Jul Q5** and **Q1 2025 Feb Q5** — type produced by a chained comparison.
- [ ] **Q1 2023 Feb Q3** — when does conditionally-assigned-variable code raise an error.
- [ ] **Q1 2024 Jul Q9** — SA: trace a conditional on two numbers.

### Suggested order for your session
1. Skim Part 2's W3 and W4 sections only (~15 min). W1/W2 you can read at the end — they're small and easy.
2. **Section B** (boolean blitz) first — 15 minutes, and it makes every W3 question afterwards faster.
3. **Section A1**, starting with the four 1-mark `Q1 2023 Feb` warm-ups, then the MSQs (~35 min).
4. **Section A2** (digit loops) — write the skeleton from memory once before you start (~25 min).
5. **Section C**, then **E**, then **D**. Stop at D if you run out of time; it's 16 marks and the hardest.
6. **Section F** last, fast.
7. Re-read Part 3's precedence line, the falsy list and the digit-loop skeleton right before the exam.

Log every slip — what you thought, what it actually was — in `Stat1/error_log.md` (or start a `Python/error_log.md` beside it). Tracing errors repeat unless they're written down.
