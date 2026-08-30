#!/usr/bin/env python3
"""Sanity-check week assignments without trusting whoever made them.

Two independent tests, neither needing the course PDFs:

  1. Are weeks real groupings at all? Questions in the same week should look
     more like each other than like other weeks' questions. (They do: 3.4-5.6x.)

  2. Does any individual question disagree with its neighbours? For each
     question, look at the 6 most similar questions in the subject; if a clear
     majority sit in a different week AND none sit in its own, flag it.

Flags are candidates for review, not errors -- a question can legitimately
straddle two weeks, which is what the 'aw' (also-weeks) field records, so
anything already declaring the neighbours' week there is filtered out.

Run after swapping in a new exam's data. Judgement still required on what it
prints; this narrows 1300 questions to a handful.
"""
import collections, json, os, random, re, statistics, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STOP = set("""this that with from have been they will your what when which there their
given find each both only also more most such other value values using""".split())
NEIGHBOURS = 6
MIN_SIM = 0.20        # below this two questions aren't really comparable
MIN_TOP_SIM = 0.25    # nothing similar enough to judge against
MIN_VOTES = 4         # of NEIGHBOURS, how many must agree on another week


def toks(t):
    return set(w for w in re.findall(r"[a-z]+", t.lower()) if len(w) > 3 and w not in STOP)


def jac(a, b):
    u = a | b
    return len(a & b) / len(u) if u else 0.0


def main():
    subjects = [s["key"] for s in json.load(
        open(os.path.join(ROOT, "data", "manifest.json")))["subjects"]]
    random.seed(1)
    flagged = 0
    for s in subjects:
        rows = json.load(open(os.path.join(ROOT, "data", "%s.json" % s)))
        T = [(r, toks(r["c"] + " " + r["s"])) for r in rows]

        # test 1 -- are weeks coherent groupings?
        same, cross = [], []
        for _ in range(20000):
            (r1, a), (r2, b) = random.sample(T, 2)
            (same if r1["w"] == r2["w"] else cross).append(jac(a, b))
        ratio = statistics.mean(same) / (statistics.mean(cross) or 1e-9)

        # test 2 -- per-question disagreement
        hits = []
        for i, (r, a) in enumerate(T):
            sims = sorted(((jac(a, b), o["w"]) for j, (o, b) in enumerate(T) if j != i),
                          reverse=True)[:NEIGHBOURS]
            if not sims or sims[0][0] < MIN_TOP_SIM:
                continue
            votes = collections.Counter(w for sc, w in sims if sc >= MIN_SIM)
            if not votes:
                continue
            top, n = votes.most_common(1)[0]
            if top != r["w"] and n >= MIN_VOTES and votes.get(r["w"], 0) == 0 \
                    and top not in (r["aw"] or []):
                hits.append((n, r, top))
        flagged += len(hits)
        print("%-9s %4d questions | weeks %.1fx more coherent than chance | %d to review"
              % (s, len(rows), ratio, len(hits)))
        for n, r, top in sorted(hits, key=lambda x: -x[0]):
            print("    %s-%s  W%d -> neighbours say W%d (%d/%d)  aw=%s"
                  % (r["pk"], r["q"], r["w"], top, n, NEIGHBOURS, r["aw"]))
            print("        %s | %s" % (r["c"], r["s"][:70]))
    print("\n%d questions to review by hand." % flagged)
    return 0


if __name__ == "__main__":
    sys.exit(main())
