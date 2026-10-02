#!/usr/bin/env python3
"""Build data/python.json + data/python_archetypes.json (weeks 1-4 only, Quiz 1 scope) from the classified PYQ set.
usage: build_python.py <classify_input.json> <cls_dir> <out_dir> <full_out.json>"""
import json, sys, re
inp = {x['id']: x for x in json.load(open(sys.argv[1]))}
cl = {}
for i in range(4):
    for r in json.load(open('%s/cls_%d.json' % (sys.argv[2], i))): cl[r['id']] = r
OUT = sys.argv[3]
full = []
for k, x in inp.items():
    r = cl[k]; pk, q = k.rsplit('-', 1)
    full.append({'id': k, 'pk': pk, 'q': q, 'p': x['p'], 'kind': x['kind'], 't': x['t'], 'm': x['m'], 'a': x['a'],
                 'w': r['w'], 'aw': r.get('aw', []), 'c': r['c'], 'd': r['d'], 's': r['s']})
json.dump(full, open(sys.argv[4], 'w'), ensure_ascii=False, indent=0)
rows = [{'p': f['p'], 'pk': f['pk'], 'q': f['q'], 't': f['t'], 'm': f['m'], 'w': f['w'], 'aw': [], 'c': f['c'],
         'd': f['d'], 'a': f['a'], 's': f['s']} for f in full if f['w'] <= 4]
rows.sort(key=lambda r: (r['w'], r['pk'], int(r['q'][1:])))
def ids(*xs):
    o = []
    for x in xs:
        pk, qs = x.split(':')
        o += ['%s-Q%s' % (pk, q) for q in qs.split(',')]
    return o
A = [
 (1, 'pyexpr', 'Expression type and operator tracing', 'P21_2026_jul-Q2',
  'Any "what type / what value / what output" on straight-line code: work inside-out. int op int is int except / (float) and ** with a negative power; int op float is float; a quoted literal is str even if it looks like a number; // floors, % keeps the remainder (days = n // 7, rest = n % 7); + joins str only with str; int(), str(), len() change the type BEFORE the next operator sees it.',
  None),
 (2, 'pybool', 'Chained comparison and bool-as-type results', 'P13_2025_feb-Q5',
  'The question asks for the TYPE or value of a comparison expression. a < b < c means (a < b) and (b < c); any comparison gives bool, and bool is an int (True == 1, True + True == 2). Evaluate each link, then combine; the result is bool unless an arithmetic operator is applied afterwards.',
  ids('P09_2024_jul:5', 'P13_2025_feb:5')),
 (2, 'pyflow', 'Single if/else trace and unassigned-variable trap', 'P01_2023_feb-Q3',
  'One or two ifs with assignments inside. Substitute the inputs, follow ONE branch, print. If a name is assigned only inside an if and then used outside, it raises NameError exactly when every guarding condition is False.',
  ids('P01_2023_feb:3', 'P09_2024_jul:9')),
 (3, 'pybool', 'Boolean expression evaluation: not before and before or', 'P02_2023_apr-Q28',
  'Printed boolean expressions mixing not/and/or. Precedence is not, then and, then or; parenthesise mentally, substitute True/False, reduce innermost first. For "deduce the variable" questions, undo not by not: not not x is x.',
  ids('P02_2023_apr:25,26,27,28', 'P04_2023_sep:14,15,16,17', 'P01_2023_feb:2')),
 (3, 'pyflow', 'if / elif / else tracing and input-set questions', 'P15_2025_jul-Q8',
  'Given inputs (or asked for which inputs), walk the chain top to bottom: the FIRST true condition runs and the rest are skipped. For "which inputs give output X", write the interval each branch owns (earlier conditions carve out later ones) and test boundary values (=, +-1) explicitly. For a count of inputs, count integers in the rectangle/interval, inclusive of ends.',
  ids('P01_2023_feb:16,17,18,19', 'P03_2023_jul:3,6,7', 'P05_2023_oct:13', 'P09_2024_jul:6', 'P11_2024_oct:9', 'P12_2024_dec:7',
      'P13_2025_feb:9,12,13', 'P14_2025_apr:15', 'P15_2025_jul:8')),
 (3, 'pycode', 'Choose the snippet that is actually correct', 'P07_2024_feb-Q5',
  'Four or five candidate programs for one spec (min of three, age/marks bands, abs value). Test each with the boundary and tie inputs (equal values, exactly on a threshold, negative). The common bugs: independent ifs that print twice, an elif chain with the wrong order, > where >= is needed, a missing else.',
  ids('P07_2024_feb:5', 'P10_2024_sep:3', 'P14_2025_apr:8', 'P11_2024_oct:6')),
 (3, 'pyflow', 'Separate ifs vs elif: equivalence and possible outputs', 'P13_2025_feb-Q6',
  'Compare two blocks or list the possible outputs. Separate ifs are tested independently (several can fire, or none); elif/else makes the branches mutually exclusive. Look for inputs that satisfy two conditions at once — that is where the two versions differ.',
  ids('P05_2023_oct:9', 'P06_2023_dec:10', 'P12_2024_dec:3', 'P13_2025_feb:6', 'P17_2025_oct:9')),
 (3, 'pybool', 'Truthiness, isinstance and short-circuit', 'P19_2026_mar-Q17',
  'Conditions on non-boolean values. Falsy: 0, 0.0, "", empty collections, None; everything else truthy. a or b returns the first truthy operand, a and b the first falsy one (not necessarily a bool). isinstance(True, int) is True. Trace the counter line by line.',
  ids('P16_2025_aug:3', 'P17_2025_oct:4', 'P19_2026_mar:17,18', 'P22_2026_sep:1')),
 (4, 'pydigit', 'Digit extraction loop (% 10 and // 10)', 'P19_2026_mar-Q5',
  'While n > 0: d = n % 10 peels the last digit, n = n // 10 drops it. Whatever sits between those two lines (sum, product, reverse via r = r*10 + d, position weights, odd-digit filter) is the only part that changes. Start the accumulator at the identity (0 for sum, 1 for product) — a wrong start is the standard trap.',
  ids('P02_2023_apr:3,18', 'P03_2023_jul:11', 'P04_2023_sep:8', 'P09_2024_jul:11', 'P13_2025_feb:11', 'P19_2026_mar:5,6', 'P21_2026_jul:10')),
 (4, 'pyloop', 'Pick the loop that prints or accumulates a series', 'P03_2023_jul-Q10',
  'Match the loop bounds to the count: range(1, 11) gives 10 values (stop is exclusive), "first hundred powers" means 100 iterations with the multiplier updated every pass. Check the first value, the last value and the number of iterations of each option.',
  ids('P01_2023_feb:6', 'P03_2023_jul:10', 'P05_2023_oct:15', 'P13_2025_feb:4')),
 (4, 'pyloop', 'While-loop tracing: final value and iteration count', 'P07_2024_feb-Q8',
  'Make a table: one row per iteration with every variable. Stop when the condition first fails and report the value requested (loop variable after exit, count of passes, last term). The exit value is the first value that violates the condition.',
  ids('P05_2023_oct:16', 'P07_2024_feb:8', 'P12_2024_dec:10', 'P22_2026_sep:10')),
 (4, 'pyloop', 'Two-pointer while loop', 'P12_2024_dec-Q17',
  'i starts at the left end, j at the right end; compare the pair sum with the target and move the pointer that can fix it (sum too big -> j -= 1, too small -> i += 1). Trace both pointers per iteration; None/False is returned when they cross.',
  ids('P12_2024_dec:17,18')),
]
byw = {}
arch = []
used = set()
rowids = {r['pk'] + '-' + r['q']: r for r in rows}
# week 1 takes every w1 row
for w, fam, title, target, trig, cov in A:
    if cov is None: cov = [k for k, r in rowids.items() if r['w'] == w]
    for c in cov:
        assert c in rowids, c
        assert c not in used, 'dup ' + c
        used.add(c)
    byw[w] = byw.get(w, 0) + 1
    arch.append({'title': title, 'target': target, 'trigger': trig, 'covers': cov, 'id': 'W%d-A%d' % (w, byw[w]),
                 'week': w, 'family': fam})
missing = [k for k in rowids if k not in used]
assert not missing, missing
json.dump(rows, open(OUT + '/python.json', 'w'), ensure_ascii=False, indent=0)
json.dump(arch, open(OUT + '/python_archetypes.json', 'w'), ensure_ascii=False, indent=0)
print(len(rows), 'rows;', len(arch), 'archetypes')
