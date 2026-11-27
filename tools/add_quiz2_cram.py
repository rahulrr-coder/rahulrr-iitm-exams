#!/usr/bin/env python3
"""One-shot: append the Stat 1 week 5-9 lessons to cram.html for Quiz 2 (Sat 5 Dec 2026).

The lesson prose lives here; the past-paper pattern rows are generated from
data/stat1_archetypes.json. Refuses to run twice (W5 already present).
"""
import json, html, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "cram.html")
src = open(P).read()
if 'id="w-stat1-5"' in src:
    sys.exit("cram.html already has W5 - nothing to do")

rows = json.load(open(os.path.join(ROOT, "data/stat1.json")))
arch = json.load(open(os.path.join(ROOT, "data/stat1_archetypes.json")))
mk = {r["pk"] + "-" + r["q"]: r["m"] for r in rows}


def cn(w, i, title, prose, side=None):
    two = ' two' if side else ''
    s = '<section class="cn" id="w-stat1-%d-c%d"><h4><span class="cnum">%d.%d</span>%s</h4><div class="cbody%s"><div class="prose">%s</div>' % (w, i, w, i, title, two, prose)
    if side:
        lbl, body = side
        s += '<div class="side"><div class="fx"><span class="lbl">%s</span>%s</div></div>' % (lbl, body)
    return s + '</div></section>'


def drills(qs):
    out = '<div class="drills"><h4>Practice &mdash; solve on paper first, then open the answer</h4><div class="dqgrid">'
    for n, (q, a) in enumerate(qs, 1):
        out += '<div class="dq"><div class="dqq"><span class="qn">Q%d</span>%s</div><details><summary>Show answer</summary><div class="ans">%s</div></details></div>' % (n, q, a)
    return out + '</div></div>'


W = {}

W[5] = dict(title="Counting basics", ov=(
    "<p>Week 5 starts the probability half of the course with <b>counting</b>: how many ways something can happen. Every probability in weeks 7&ndash;9 is a count divided by a count, so this is the foundation.</p>"
    "<p>On the paper it shows up as short numeric answers: digit problems, grades per subject, outfits. Two rules do almost all of the work.</p>",
    ["Use the multiplication rule for a sequence of choices", "Use the addition rule for disjoint cases", "Handle leading-digit and no-repeat restrictions", "Work with factorials, including 0! = 1"], "About 6 min to read &middot; 3 practice problems"),
    cns=[
    ("Multiplication and addition rules",
     "<p><b>Multiplication rule:</b> if a task is a sequence of k steps with n&#8321;, n&#8322;, &hellip; n&#8342; choices each, there are n&#8321;&middot;n&#8322;&middot;&hellip;&middot;n&#8342; ways in total.</p><p><b>Addition rule:</b> if the outcomes split into <b>disjoint cases</b> (no outcome in two cases), add the counts of the cases.</p><p>Ask yourself: <i>&ldquo;and then&rdquo;</i> &rarr; multiply; <i>&ldquo;or else&rdquo;</i> &rarr; add.</p>",
     ("Worked", "<p>4 subjects, each passed with one of 6 grades (S, A, B, C, D, E): 6&times;6&times;6&times;6 = <b>1296</b>.</p>")),
    ("Digit problems",
     "<p>Fill the places one at a time and count the allowed digits for each. The <b>leading digit can't be 0</b>. Start with the most restricted place.</p><ul><li>No repeats allowed &rarr; each later place has one fewer option.</li><li>&ldquo;Even number&rdquo; &rarr; fix the units digit first.</li><li>&ldquo;At least one 4&rdquo; &rarr; total &minus; numbers with no 4.</li></ul>",
     ("Worked", "<p>3-digit numbers with no 4: hundreds 8 (not 0 or 4) &times; tens 9 &times; units 9 = <b>648</b>.<br>So 900 &minus; 648 = 252 contain at least one 4.</p>")),
    ("Factorials",
     "<p>n! = n&middot;(n&minus;1)&middot;&hellip;&middot;2&middot;1 counts the ways to arrange n distinct objects in a row. <b>0! = 1</b> by definition. Simplify ratios before multiplying out: 10!/8! = 10&middot;9 = 90.</p>"),
    ],
    recap=["<b>And then</b> &rarr; multiply &middot; <b>or else</b> &rarr; add", "Leading digit &ne; 0; fill the most restricted place first", "At least one = total &minus; none", "n! arranges n distinct objects; 0! = 1"],
    traps=["Forgetting the leading-digit-not-zero rule (900 three-digit numbers, not 1000).", "Using repeats when the question says <b>distinct</b> digits.", "Adding cases that overlap: the cases must be disjoint."],
    dq=[("How many 4-digit numbers have all digits distinct?", "9 &times; 9 &times; 8 &times; 7 = <b>4536</b> (first digit 1&ndash;9; then 9 left including 0, then 8, then 7)."),
        ("A menu has 3 starters, 5 mains and 2 desserts. How many 3-course meals? How many meals of a main plus <i>either</i> a starter or a dessert?", "3&times;5&times;2 = <b>30</b>. Main &times; (starter or dessert) = 5 &times; (3 + 2) = <b>25</b>."),
        ("How many 3-digit numbers contain at least one 7?", "900 &minus; 8&middot;9&middot;9 = 900 &minus; 648 = <b>252</b>.")])

W[6] = dict(title="Permutations &amp; combinations", ov=(
    "<p>Week 6 is the heaviest counting week on the paper (13 questions, 37 marks across the end terms). The whole week is about one question: <b>does order matter?</b> Yes &rarr; permutation. No &rarr; combination.</p>"
    "<p>Exam questions are teams with must-include/must-exclude people, words with repeated letters, people who must sit together or apart, and MSQs on the identities.</p>",
    ["Choose between nPr and nCr from the wording", "Count arrangements with repeated letters", "Handle together/apart restrictions", "Solve nPr = k type equations and check the identities"], "About 12 min to read &middot; 4 practice problems"),
    cns=[
    ("Permutations: order matters",
     "<p>Arranging r of n distinct objects in order: <b>nPr = n!/(n&minus;r)!</b>. Cue words: <i>arrange, rank, positions, captain and vice-captain, 1st/2nd/3rd prize, PIN, password</i>.</p><p>Around a circle the rotations are the same arrangement, so n people sit in <b>(n&minus;1)!</b> ways.</p>",
     ("Worked", "<p>Captain and vice-captain can be filled in 42 ways: n(n&minus;1) = 42 &rArr; <b>n = 7</b>.</p>")),
    ("Combinations: order doesn't matter",
     "<p>Choosing r of n: <b>nCr = n!/(r!(n&minus;r)!) = nPr / r!</b>. Cue words: <i>select, team, committee, group, handshakes, subset</i>.</p><ul><li><b>Must include</b> k given people &rarr; fix them and choose the rest from the others: C(n&minus;k, r&minus;k).</li><li><b>Must exclude</b> k people &rarr; C(n&minus;k, r).</li><li><b>At least one</b> &rarr; total &minus; none, or add the disjoint &ldquo;exactly&rdquo; cases.</li><li><b>Two pools</b> (men/women) &rarr; multiply within a case, add across cases.</li></ul>",
     ("Worked", "<p>Team of 4 from 8, two given people compulsory: C(6,2) = <b>15</b>.<br>20 men and 10 women shake hands only within gender: C(20,2) + C(10,2) = 190 + 45 = <b>235</b>.</p>")),
    ("Repeated letters",
     "<p>n objects where one kind repeats p times, another q times, &hellip;: <b>n!/(p!&middot;q!&middot;&hellip;)</b>. Count the letters carefully: write each letter with its frequency.</p>",
     ("Worked", "<p>COMMITTEE: 9 letters, M&times;2, T&times;2, E&times;2 &rarr; 9!/(2!2!2!) = <b>45360</b>.<br>ARRANGEMENT: 11 letters, A, R, N, E twice each &rarr; 11!/(2!)&#8308; = <b>2494800</b>.</p>")),
    ("Together and apart",
     "<p><b>Together:</b> glue the group into one block. Arrange the blocks, then multiply by the arrangements inside the block.</p><p><b>Apart:</b> total &minus; together. Or, for &ldquo;no two of these adjacent&rdquo;, arrange the others and put the restricted items into the gaps.</p><p><b>Dictionary rank:</b> go left to right. At each position, count the unused letters smaller than the actual letter &times; (letters left)!. Add these up, then add 1.</p>",
     ("Worked", "<p>LEADING, vowels E, A, I together: 5 units &rarr; 5!&middot;3! = <b>720</b>.<br>7 in a row, A&amp;B together, D&amp;E apart: 6!&middot;2 &minus; 5!&middot;2&middot;2 = 1440 &minus; 480 = <b>960</b>.<br>Rank of SACHIN = <b>601</b>.</p>")),
    ("Identities the MSQs test",
     "<ul><li>nPr = nCr &middot; r! &nbsp;(so nPr/nCr = r!) &#10004;</li><li>nCr = nC(n&minus;r) &#10004; &nbsp;&middot;&nbsp; nC0 = nCn = 1 &#10004;</li><li>nCr + nC(r&minus;1) = (n+1)Cr &#10004;</li><li>&ldquo;nPr = nCr / r!&rdquo; &#10008; &nbsp;&middot;&nbsp; &ldquo;permutations ignore order&rdquo; &#10008;</li></ul><p>For an unknown n (e.g. n&#8319; &minus; n! = 21), test small values: n = 3 gives 27 &minus; 6 = 21.</p>"),
    ],
    recap=["Order matters &rarr; nPr; it doesn't &rarr; nCr = nPr/r!", "Include k &rarr; C(n&minus;k, r&minus;k); exclude k &rarr; C(n&minus;k, r)", "Repeats &rarr; n!/(p!q!&hellip;)", "Together &rarr; glue &times; inside!; apart &rarr; total &minus; together", "Circle &rarr; (n&minus;1)!"],
    traps=["<b>&ldquo;At least one&rdquo; by picking one and then choosing freely</b> double counts. Use total &minus; none.", "Missing a repeated letter (ARRANGEMENT has four repeated pairs).", "Forgetting the internal arrangement of a glued block (&times; k!).", "Using P for a committee or C for officer roles."],
    dq=[("From 6 men and 4 women, how many committees of 5 have at least 2 women?", "Total C(10,5) = 252. Subtract 0 women: C(6,5) = 6, and 1 woman: C(4,1)C(6,4) = 60. 252 &minus; 66 = <b>186</b>."),
        ("How many arrangements of BANANA?", "6!/(3!&middot;2!) = 720/12 = <b>60</b>."),
        ("5 boys and 3 girls in a row so that no two girls are adjacent?", "Arrange the boys: 5! = 120. There are 6 gaps; place the 3 girls: 6P3 = 120. 120 &times; 120 = <b>14400</b>."),
        ("If nC2 = 28, find n and nP2.", "n(n&minus;1)/2 = 28 &rArr; n = <b>8</b>; 8P2 = <b>56</b>.")])

W[7] = dict(title="Probability", ov=(
    "<p>Week 7 turns counts into <b>probabilities</b>: sample spaces, events, the axioms, and the addition rule. With equally likely outcomes, P(E) is just favourable &divide; total, and both counts usually come from week 6.</p>"
    "<p>The paper asks for unions of categories, &ldquo;all the same colour&rdquo; draws, and small experiments you can list by hand.</p>",
    ["Write a sample space and the events in it", "Compute equally-likely probabilities with nCr", "Use the addition rule and complements", "Tell mutually exclusive events from independent ones"], "About 8 min to read &middot; 3 practice problems"),
    cns=[
    ("Sample spaces and events",
     "<p>The <b>sample space</b> S lists every outcome. An <b>event</b> is a subset of it. With 2&ndash;3 coins or a 3-child family, <b>write S out</b> (8 outcomes for 3 tosses); don't reach for a formula.</p><p>Events are combined with &cup; (or), &cap; (and) and complement A&#7580; (not).</p>",
     ("Worked", "<p>Toss a coin until two in a row match. The game stops on toss 3 for HTT and THH only &rarr; 2/8 = <b>0.25</b>.</p>")),
    ("Equally likely outcomes",
     "<p><b>P(E) = |E| / |S|</b>. For draws of several items, count both with combinations: P = C(favourable)&middot;C(rest) / C(total).</p><p>&ldquo;All the same colour&rdquo; = all red <b>or</b> all blue: add the two counts.</p>",
     ("Worked", "<p>4 red, 5 blue, draw 3. P(all same) = (C(4,3) + C(5,3)) / C(9,3) = (4 + 10)/84 = <b>0.167</b>.</p>")),
    ("Axioms and the addition rule",
     "<p>0 &le; P(A) &le; 1, P(S) = 1, and P(A&#7580;) = 1 &minus; P(A).</p><p><b>P(A &cup; B) = P(A) + P(B) &minus; P(A &cap; B).</b> If A and B are <b>mutually exclusive</b> (they can't both happen), the overlap is 0 and you just add.</p><p>For three events: P(A&cup;B&cup;C) = &Sigma;P &minus; &Sigma;(pairwise &cap;) + P(A&cap;B&cap;C).</p>",
     ("Worked", "<p>Everyone is exactly one of F, D, Deg. P(F or D) = 0.8 and P(D or Deg) = 0.6. Adding: F + 2D + Deg = 1.4, and F + D + Deg = 1, so <b>P(D) = 0.4</b>.</p>")),
    ],
    recap=["P(E) = favourable / total; count draws with nCr", "Complement: P(not A) = 1 &minus; P(A)", "Union = sum &minus; overlap; exclusive &rarr; overlap 0", "Small experiment &rarr; list the sample space"],
    traps=["Adding P(A) + P(B) when the events overlap.", "<b>Exclusive is not independent.</b> Two exclusive events with P &gt; 0 are dependent.", "Counting ordered outcomes on top and unordered ones on the bottom. Be consistent."],
    dq=[("A box has 10 red, 8 blue and 12 green balls. One is drawn. P(red or green)?", "(10 + 12)/30 = <b>0.733</b>."),
        ("P(A) = 0.5, P(B) = 0.4, P(A &cup; B) = 0.7. Find P(A &cap; B) and P(neither).", "0.5 + 0.4 &minus; 0.7 = <b>0.2</b>; neither = 1 &minus; 0.7 = <b>0.3</b>."),
        ("A team of 5 is chosen from 6 boys and 4 girls. P(exactly 3 girls)?", "C(4,3)C(6,2)/C(10,5) = 4&middot;15/252 = <b>0.238</b>.")])

W[8] = dict(title="Conditional probability &amp; Bayes", ov=(
    "<p>Week 8 is the <b>highest-scoring probability week</b> (14 questions, 42 marks across the end terms), and one pattern dominates it: <b>pick a box, then pick a ball</b>. That is the law of total probability, and reversing the question is Bayes' rule.</p>"
    "<p>The questions never say &ldquo;Bayes&rdquo;. They describe two bags, two machines, a fair and a biased coin, or a diagnostic test.</p>",
    ["Compute P(A | B) from a definition, a table or a PMF", "Test independence and use it for &ldquo;at least one&rdquo;", "Draw a probability tree and apply the law of total probability", "Reverse the tree with Bayes' rule"], "About 12 min to read &middot; 4 practice problems"),
    cns=[
    ("Conditional probability",
     "<p><b>P(A | B) = P(A &cap; B) / P(B)</b>. &ldquo;Given B&rdquo; means B is your new total.</p><ul><li><b>From a table:</b> take the row (or column) of the condition and divide the cell by that row's total.</li><li><b>From a PMF:</b> sum the values in both events, then divide by the sum over the given event.</li></ul><p><b>Multiplication rule:</b> P(A &cap; B) = P(B)&middot;P(A | B). Use it for draws without replacement, updating the counts each time.</p>",
     ("Formula", "<p>P(A|B) = P(A&cap;B) / P(B)<br>P(A&cap;B) = P(A)&middot;P(B|A)</p>")),
    ("Independence",
     "<p>A and B are <b>independent</b> if P(A &cap; B) = P(A)&middot;P(B), or equivalently P(A | B) = P(A).</p><ul><li>At least one of several independent events: <b>1 &minus; &Pi;(1 &minus; p&#7522;)</b>.</li><li>Exactly one of two: p&#8321;(1 &minus; p&#8322;) + (1 &minus; p&#8321;)p&#8322;.</li><li>Draws <b>without replacement</b> are not independent. Check by comparing P(A&cap;B) with P(A)P(B).</li></ul>",
     ("Worked", "<p>Forecasters are right with probability 4/7 and 2/3, independently. P(they contradict) = (4/7)(1/3) + (3/7)(2/3) = 10/21 = <b>0.48</b>.</p>")),
    ("Law of total probability",
     "<p>If B&#8321;, &hellip;, B&#8342; split the sample space (boxes, machines, groups) then</p><p style='text-align:center;font-size:18px'><b>P(A) = &Sigma; P(A | B&#7522;)&middot;P(B&#7522;)</b></p><p>Draw a tree: the first branches are the B&#7522; with their priors, the second branches are A within each. Multiply along each path to A and add the paths.</p>",
     ("Worked", "<p>A coin is chosen at random: fair, or P(H) = 3/4.<br>P(H) = &frac12;&middot;&frac12; + &frac12;&middot;&frac34; = <b>0.625</b>.</p>")),
    ("Bayes' rule",
     "<p>Reverse the tree: &ldquo;given A happened, which branch did it come from?&rdquo;</p><p style='text-align:center;font-size:18px'><b>P(B&#7522; | A) = P(A | B&#7522;)&middot;P(B&#7522;) / P(A)</b></p><p>The numerator is one path. The denominator is <b>all</b> paths to A, which is the total-probability sum you just computed.</p><p><b>Diagnostic tests:</b> P(D | +) = P(+|D)P(D) / [P(+|D)P(D) + P(+|D&#7580;)P(D&#7580;)]. For rare diseases this is small, even when the test is good.</p>",
     ("Worked", "<p>Same coins. Given heads, P(fair) = 0.25/0.625 = <b>0.4</b>.</p>")),
    ],
    recap=["P(A|B) = P(A&cap;B)/P(B): the condition is the new total", "Independent &rArr; multiply; at least one = 1 &minus; &Pi;(1 &minus; p)", "Two-stage question &rarr; tree &rarr; total probability", "&ldquo;Given the result, which source?&rdquo; &rarr; Bayes = one path / all paths", "Without replacement &rArr; dependent; update the counts"],
    traps=["Dividing by P(A) instead of P(B) in P(A | B).", "Using only one branch in the Bayes denominator.", "Treating draws without replacement as independent.", "Confusing P(+ | D), which the question gives you, with P(D | +), which it asks for."],
    dq=[("Bag A (chosen w.p. 1/3) has 3 red and 2 blue; bag B (w.p. 2/3) has 1 red and 4 blue. A ball is drawn. P(red)? Given red, P(bag A)?", "P(R) = (1/3)(3/5) + (2/3)(1/5) = 3/15 + 2/15 = <b>1/3</b>. P(A | R) = (3/15)/(5/15) = <b>0.6</b>."),
        ("1% of people have a disease. The test detects it 95% of the time and gives a false positive 5% of the time. P(disease | positive)?", "0.0095 / (0.0095 + 0.0495) = <b>0.161</b>."),
        ("Three students solve a problem independently with probabilities 1/2, 1/3, 1/4. P(at least one solves it)?", "1 &minus; (1/2)(2/3)(3/4) = 1 &minus; 1/4 = <b>0.75</b>."),
        ("Two cards are drawn without replacement from a standard deck. P(both aces)? Are &ldquo;first ace&rdquo; and &ldquo;second ace&rdquo; independent?", "(4/52)(3/51) = <b>0.0045</b>. Not independent: P(2nd ace | 1st ace) = 3/51 &ne; 4/52.")])

W[9] = dict(title="Random variables, PMF &amp; CDF", ov=(
    "<p>Week 9 (lectures 8.x) attaches a <b>number</b> to each outcome: a random variable X. Its <b>PMF</b> gives P(X = x) and its <b>CDF</b> gives P(X &le; x). <b>Check the portal's Quiz 2 syllabus</b> before studying this week; it may only be in the End Term.</p>"
    "<p>If it is in scope, it is quick marks: the support of X, a PMF by counting, an unknown constant, and reading values off a step CDF.</p>",
    ["Classify a random variable as discrete or continuous and list its support", "Build a PMF by counting and find an unknown constant", "Move between a PMF and a step CDF", "Compute tail and conditional probabilities from a CDF"], "About 8 min to read &middot; 3 practice problems"),
    cns=[
    ("Random variables and their support",
     "<p>A <b>discrete</b> random variable takes countable values (a number of heads, a count of defects). A <b>continuous</b> one takes any value in an interval (time, height).</p><p>When drawing n items from g good and b bad, X = number of good runs from <b>max(0, n &minus; b)</b> to <b>min(n, g)</b>.</p>",
     ("Worked", "<p>10 white, 3 black, draw 4. X = whites &isin; <b>{1, 2, 3, 4}</b>: at most 3 of the 4 can be black.</p>")),
    ("PMF",
     "<p>p(x) = P(X = x), with p(x) &ge; 0 and <b>&Sigma; p(x) = 1</b>. The second rule finds unknown constants.</p><p>By counting (without replacement): <b>P(X = k) = C(g,k)&middot;C(b,n&minus;k)/C(g+b,n)</b>.</p><p>For a sum of two independent throws, list the pairs and add P(a)&middot;P(b) over a + b = s.</p>",
     ("Worked", "<p>p(x) = kx for x = 1..4: k(1+2+3+4) = 1 &rArr; <b>k = 0.1</b>.</p>")),
    ("CDF",
     "<p><b>F(x) = P(X &le; x)</b>. For discrete X it is a step function: it never decreases, it starts at 0 and ends at 1, and it is right-continuous.</p><ul><li>P(X = a) = <b>the jump at a</b> = F(a) &minus; F(a&#8315;)</li><li>P(X &gt; a) = 1 &minus; F(a) &nbsp;&middot;&nbsp; P(X &ge; a) = 1 &minus; F(a&#8315;)</li><li>P(a &lt; X &le; b) = F(b) &minus; F(a)</li><li>Unknown constant: F(largest value) = 1</li></ul>",
     ("Worked", "<p>F(x) = (x&sup2; + k)/99 on x = 1..8: F(8) = 1 &rArr; 64 + k = 99 &rArr; <b>k = 35</b>.</p>")),
    ],
    recap=["Support of draws: max(0, n&minus;b) to min(n, g)", "&Sigma; p(x) = 1 finds k", "F(x) = P(X &le; x); P(X = a) = jump at a", "&ge; and &lt; need F(a&#8315;): watch strict inequalities", "Conditional from a CDF: P(A&cap;B)/P(B), each from F"],
    traps=["P(X &ge; a) = 1 &minus; F(a) is wrong. It is 1 &minus; F(a&#8315;).", "Reading F(a) as P(X = a).", "Listing support values that can't happen (more whites than there are)."],
    dq=[("X has F(0) = 0.2, F(1) = 0.5, F(2) = 0.85, F(3) = 1. Find P(X = 2), P(X &ge; 1) and P(X &gt; 1 | X &lt; 3).", "P(X=2) = 0.85 &minus; 0.5 = <b>0.35</b>. P(X &ge; 1) = 1 &minus; 0.2 = <b>0.8</b>. P(X&gt;1 | X&lt;3) = P(X=2)/F(2) = 0.35/0.85 = <b>0.412</b>."),
        ("A box has 3 red and 3 blue balls; pick 3 without replacement. X = reds. Find the PMF.", "C(3,k)C(3,3&minus;k)/20: P(0) = <b>1/20</b>, P(1) = <b>9/20</b>, P(2) = <b>9/20</b>, P(3) = <b>1/20</b>."),
        ("p(x) = c(x + 1) for x = 0, 1, 2, 3. Find c and P(X &le; 1).", "c(1+2+3+4) = 1 &rArr; <b>c = 0.1</b>; P(X &le; 1) = 0.1 + 0.2 = <b>0.3</b>.")])


def week(w):
    d = W[w]
    A = sorted([a for a in arch if a["week"] == w], key=lambda a: -sum(mk[c] for c in a["covers"]))
    wm = sum(mk[c] for a in A for c in a["covers"])
    ovp, goals, tm = d["ov"]
    s = ['<div class="wk" id="w-stat1-%d">\n<div class="wkh">\n<span class="wn">W%d</span>\n<h3>%s</h3>\n<span class="wm">0/%d learned &middot; %g marks</span>\n</div>\n' % (w, w, d["title"], len(A), wm)]
    s.append('<div class="lesson">\n<div class="ov"><h4>Week overview</h4>%s<p class="goal"><b>After this week you can:</b></p><ul>%s</ul><p class="time">%s</p></div>\n' % (ovp, "".join("<li>%s</li>" % g for g in goals), tm))
    for i, c in enumerate(d["cns"], 1):
        s.append(cn(w, i, *c) + "\n")
    s.append('<div class="recap"><h4>Recap &mdash; read this the night before</h4><ul>%s</ul></div>\n' % "".join("<li>%s</li>" % r for r in d["recap"]))
    s.append('<div class="traps"><h4>Traps that cost marks</h4><ol>%s</ol></div>\n' % "".join("<li>%s</li>" % t for t in d["traps"]))
    s.append(drills(d["dq"]) + "\n</div>\n")
    s.append('<h4 class="arh">Past-paper patterns for this week</h4>\n<div class="arows">\n')
    for a in A:
        m = sum(mk[c] for c in a["covers"])
        s.append('<div class="ar gap">\n<span class="tick">&times;</span>\n<a class="aid" href="stat1.html#arch-%s">%s</a>\n<span class="at">%s</span>\n<div class="meta"><span class="am">%g marks</span><span class="am">%d Q</span></div>\n<p class="ab">%s</p>\n</div>\n'
                 % (a["id"], a["id"], html.escape(a["title"]), m, len(a["covers"]), html.escape(a["trigger"])))
    s.append('</div></div>\n')
    return "".join(s)


block = "".join(week(w) for w in (5, 6, 7, 8, 9))
marker = '</section>\n<section class="sub s-python"'
assert src.count(marker) == 1
src = src.replace(marker, block + marker)
src = src.replace('<span class="slot">Quiz 1 · wk 1–4</span>\n<span class="cov">34 questions &middot; 14 archetypes</span>',
                  '<span class="slot">Quiz 2 · wk 5–8 (+ 1–4, 9)</span>\n<span class="cov">%d questions &middot; %d archetypes</span>' % (len(rows), len(arch)), 1)
src = src.replace("<h1>Quiz 1 Cram Sheet</h1>", "<h1>Quiz 2 Cram Sheet</h1>")
i = src.index('<p class="lede">', src.index("<h1>Quiz 2 Cram Sheet</h1>"))
j = src.index("</p>", i) + 4
src = src[:i] + ('<p class="lede">Stat 1 Quiz 2 on Sat 5 Dec 2026. <b>Weeks 5&ndash;8 are new:</b> counting, permutations and combinations, probability, and conditional probability with Bayes. W9 (random variables) is included in case the syllabus lists it. Weeks 1&ndash;4 stay as review, and the Python weeks 1&ndash;4 stay for OPPE 2. Each week opens with an overview, teaches each concept with a worked example, then gives a recap, the traps, practice problems, and the past-paper patterns from every End Term PYQ since 2022.</p>') + src[j:]
open(P, "w").write(src)
print("added W5-W9: %d bytes" % len(block))
