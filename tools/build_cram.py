#!/usr/bin/env python3
"""Rebuild cram.html for the Quiz 1 scope: Stat 1 weeks 1-4 (kept from the existing sheet) + Python weeks 1-4 (generated)."""
import json, re, html, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "cram.html")).read()
head = src[:src.index('<div class="wrap cram">')]
head = head.replace("assets/css/style.css?v=9", "assets/css/style.css?v=10")
s1 = src[src.index('<section class="sub s-stat1"'):src.index('<div class="wk" id="w-stat1-5">')] + "</section>\n"
s1 = s1.replace('<span class="slot">Paper 1 · morning</span>\n', '<span class="slot">Quiz 1 · wk 1–4</span>\n')
s1 = re.sub(r'<span class="cov">.*?</span>', '<span class="cov">34 questions &middot; 14 archetypes</span>', s1)
s1 = s1.replace('<div class="ar have">', '<div class="ar gap">').replace('<span class="tick">&check;</span>', '<span class="tick">&times;</span>')
s1 = re.sub(r'\d+/(\d+) learned', r'0/\1 learned', s1)
rows = json.load(open(os.path.join(ROOT, "data/python.json")))
arch = json.load(open(os.path.join(ROOT, "data/python_archetypes.json")))
mk = {r["pk"] + "-" + r["q"]: r["m"] for r in rows}
CAP = {
 1: ("Intro to algorithms", [
  ("Operators", "<b>/</b> always gives float · <b>//</b> floors · <b>%</b> remainder (days = n // 7, rest = n % 7) · <b>**</b> power · int op float → float"),
  ("Types", "<b>int float str bool</b> · a quoted number is str · <b>int('5')+1 = 6</b>, <b>'5'+1</b> is a TypeError · str + str joins, str * int repeats"),
  ("Output formats", "<b>len(s)</b> counts characters · f-string width <b>f'{x:5}'</b> right-aligns numbers in 5 columns · print(a, b) puts a space between")]),
 2: ("Conditionals", [
  ("Comparisons", "== != &lt; &lt;= &gt; &gt;= give <b>bool</b> · chained <b>a &lt; b &lt; c</b> = (a &lt; b) and (b &lt; c) · bool is an int: True + True = 2"),
  ("Branch tracing", "Substitute inputs, follow ONE branch. A name assigned only inside an if raises <b>NameError</b> when no guarding condition held")]),
 3: ("Conditionals (continued)", [
  ("Precedence", "<b>not</b> then <b>and</b> then <b>or</b> · reduce innermost brackets first · not not x = x"),
  ("elif vs if", "elif chain: FIRST true branch runs, the rest are skipped · separate ifs are each tested, several (or none) can fire · test boundary values (=, ±1)"),
  ("Truthiness", "Falsy: 0, 0.0, '', [], None · <b>a or b</b> = first truthy · <b>a and b</b> = first falsy · isinstance(True, int) is True")]),
 4: ("Iterations and ranges", [
  ("range", "<b>range(a, b, step)</b>: stop is exclusive · range(1, 11) has 10 values · range(n) = 0..n-1"),
  ("while template", "init → test → body → update · trace one row per pass · exit value is the first value that fails the test"),
  ("Digits", "<b>d = n % 10</b> peels the last digit, <b>n = n // 10</b> drops it · reverse: r = r*10 + d · start sum at 0, product at 1")]),
}
out = ['<section class="sub s-python" id="s-python">\n<div class="subband">\n<h2>🐍 Python</h2>\n<span class="slot">Quiz 1 · wk 1–4</span>\n<span class="cov">%d questions &middot; %d archetypes</span>\n</div>\n' % (len(rows), len(arch))]
for w in (1, 2, 3, 4):
    t, caps = CAP[w]
    A = [a for a in arch if a["week"] == w]
    wm = sum(mk[c] for a in A for c in a["covers"])
    out.append('<div class="wk" id="w-python-%d">\n<div class="wkh">\n<span class="wn">W%d</span>\n<h3>%s</h3>\n<span class="wm">0/%d learned &middot; %d marks</span>\n</div>\n' % (w, w, html.escape(t), len(A), wm))
    out.append('<div class="cap"><dl>\n' + "\n".join('<dt>%s</dt><dd>%s</dd>' % c for c in caps) + '\n</dl></div>\n<div class="arows">\n')
    for a in sorted(A, key=lambda a: -sum(mk[c] for c in a["covers"])):
        m = sum(mk[c] for c in a["covers"])
        out.append('<div class="ar gap">\n<span class="tick">&times;</span>\n<a class="aid" href="python.html#arch-%s">%s</a>\n<span class="at">%s</span>\n<div class="meta"><span class="am">%g marks</span><span class="am">%d Q</span></div>\n<p class="ab">%s</p>\n</div>\n' % (a["id"], a["id"], html.escape(a["title"]), m, len(a["covers"]), html.escape(a["trigger"])))
    out.append('</div></div>\n')
out.append('</section>\n')
body = '''<div class="wrap cram">
<header class="cramhead">
<h1>Quiz 1 Cram Sheet</h1>
<p class="lede">Weeks 1–4 of Stat 1 and Python, in exam order (Sun 15 Nov 2026): the formulas first, then every archetype underneath with the trigger that fires it. Built from every Quiz 1 and End Term PYQ since 2023 that falls inside weeks 1–4.</p>
<div class="howto"><b>How to use it.</b> Read a week's formula box, cover it, write the formulas out, then check. The archetype rows below each box tell you which pattern each formula is actually tested by &mdash; <b>&check;</b> is one you have ticked, <b>&times;</b> is a gap. Hit <b>Gaps only</b> to strip it down to what you have never marked learned.</div>
</header>
<div class="cramctl">
<button id="tGaps" type="button">Gaps only</button>
<a href="#s-stat1">📊 Stat 1</a>
<a href="#s-python">🐍 Python</a>
<span class="sp"></span>
<button id="tPrint" type="button">Print</button>
</div>
'''
tail = src[src.index('</div>\n<script>'):] if '</div>\n<script>' in src else src[src.rindex('<script>'):]
tail = tail.replace('2026-09-13T09:00:00', '2026-11-15T14:00:00')
open(os.path.join(ROOT, "cram.html"), "w").write(head + body + s1 + "".join(out) + tail)
