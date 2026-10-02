#!/usr/bin/env python3
"""Python (BSCS1002) PYQs -> redacted question images + raw question/answer records.

Reuses the geometry/redaction helpers from extract.py (same quizpractice.space layout as Stat 1).
Papers: <PY_ROOT>/Quiz1/Quiz1_YYYY-MM-DD.pdf and <PY_ROOT>/EndTerm/EndTerm_YYYY-MM-DD*.pdf
Outputs:
  questions/python/<pk>-Q<n>.webp        question image, answer + footer painted out
  <RAW_OUT>                              [{pk,p,kind,q,t,m,a,text,opts}, ...]  (answer keys read from the PDFs)
pk = P<seq>_<yyyy>_<mon>, seq = chronological over Quiz 1 + End Term papers.
"""
import json, os, re, sys, tempfile, glob
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract as X

PY_ROOT = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1
                             else "~/Documents/IITM-T2-Q1/Sep2026_Q1/Python/PYQs")
RAW_OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(PY_ROOT, "python_raw.json")
OUTDIR = os.path.join(X.ROOT, "questions", "python")
MON = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
HEAD_RE = re.compile(r"^Q\d+$")


def papers():
    out = []
    for kind, pat in (("Q1", "Quiz1/Quiz1_*.pdf"), ("ET", "EndTerm/EndTerm_*.pdf")):
        for f in glob.glob(os.path.join(PY_ROOT, pat)):
            m = re.search(r"(\d{4})-(\d\d)-(\d\d)", f)
            out.append(((m.group(1), m.group(2), m.group(3)), kind, f))
    out.sort(key=lambda x: x[0])
    res = []
    for i, ((y, mo, d), kind, f) in enumerate(out, 1):
        mon = MON[int(mo) - 1]
        pk = "P%02d_%s_%s" % (i, y, mon)
        label = "%s %s %s" % (kind, y, mon.capitalize())
        res.append((pk, label, kind, f))
    return res


def lines_for(words):
    """Group words into text lines (y clustering), reading order."""
    ws = sorted(words, key=lambda w: (round(w[1] / 3), w[0]))
    lines, cur, cy = [], [], None
    for w in sorted(words, key=lambda w: (w[1], w[0])):
        if cy is None or abs(w[1] - cy) <= 3.2:
            cur.append(w); cy = w[1] if cy is None else cy
        else:
            lines.append(cur); cur = [w]; cy = w[1]
    if cur:
        lines.append(cur)
    return [" ".join(t[4] for t in sorted(l, key=lambda w: w[0])) for l in lines]


def parse_question(qs, k, pages):
    qno, p0, y0 = qs[k]
    p1 = qs[k + 1][1] if k + 1 < len(qs) else len(pages) - 1
    y1 = qs[k + 1][2] if k + 1 < len(qs) else None
    words = []
    for p in range(p0, p1 + 1):
        foot = [w for w in pages[p] if w[4] == "Downloaded" or "quizpractice.space" in w[4]]
        fy = min([w[1] for w in foot], default=None)
        for w in pages[p]:
            # drop only the footer's own tokens: an answer value can share the footer's line
            if fy is not None and abs(w[1] - fy) < 4 and (
                    w[4] in ("Downloaded", "by", "RAHUL", "R") or "@" in w[4] or "quizpractice" in w[4]):
                continue
            if p == p0 and w[1] < y0 - 1:
                continue
            if p == p1 and y1 is not None and w[1] >= y1 - 1:
                continue
            words.append((w[0], w[1] + p * 10000, w[2], w[3], w[4]))
    lines = lines_for(words)
    head = lines[0] if lines else ""
    m = re.match(r"Q\d+\s+(\w+)\s+\[([\d.]+)\s+marks?\]", head)
    typ, marks = (m.group(1), float(m.group(2))) if m else ("?", 0.0)
    body = lines[1:]
    text, opts, ans, mode = [], [], None, "stem"
    for ln in body:
        if ln.strip() == "OPTIONS":
            mode = "opts"; continue
        if ln.strip() == "ANSWER":
            mode = "ans"; continue
        if mode == "stem":
            text.append(ln)
        elif mode == "opts":
            mm = re.match(r"^([A-Z])\.\s*(.*)$", ln)
            if mm:
                opts.append({"k": mm.group(1), "t": mm.group(2).replace("✓ Correct", "").strip(),
                             "ok": "✓ Correct" in ln})
            elif opts:
                opts[-1]["t"] += " " + ln.replace("✓ Correct", "").strip()
                opts[-1]["ok"] = opts[-1]["ok"] or ("✓ Correct" in ln)
        elif mode == "ans":
            ans = (ans + " " if ans else "") + ln
    if typ in ("MCQ", "MSQ"):
        a = ",".join(o["k"] for o in opts if o["ok"])
    else:
        a = re.sub(r"\s*\((Equal|Range|Contains)[^)]*\)?.*$", "", (ans or "").strip())
        a = re.sub(r"\s+", " ", a).strip()
    return {"q": qno, "t": typ, "m": marks, "a": a, "text": " ".join(text).strip(), "opts": opts}


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    total, short = 0, []
    # PAPERS="11-22" processes a slice (each call must finish inside a shell time limit);
    # results merge into RAW_OUT, replacing any earlier records for the same paper.
    lo, hi = 1, 10**6
    if os.environ.get("PAPERS"):
        a, _, b = os.environ["PAPERS"].partition("-")
        lo, hi = int(a), int(b or a)
    old = json.load(open(RAW_OUT)) if os.path.exists(RAW_OUT) else []
    raw = []
    for i, (pk, label, kind, pdf) in enumerate(papers(), 1):
        if not (lo <= i <= hi):
            continue
        pages = X.page_words(pdf)
        qs = X.find_questions(pages)
        with tempfile.TemporaryDirectory() as td:
            NOIMG = bool(os.environ.get("NOIMG"))
            imgs = [] if NOIMG else [X.flatten(Image.open(f).convert("RGB")) for f in X.render_pages(pdf, td)]
            if not NOIMG:
                X.neutralise_labels(imgs, pages)
            if not NOIMG and len(imgs) != len(pages):
                print("!! page mismatch", pdf); continue
            n = 0
            for k in range(len(qs)):
                rec = parse_question(qs, k, pages)
                if rec["m"] <= 0:
                    continue                       # instruction/"useful data" cards
                if not NOIMG:
                    boxes, _stray = X.redactions(qs, k, pages)
                    img = X.build_image(X.band_slices(qs, k, pages, imgs), boxes, imgs)
                    if img is None:
                        print("!! empty", pk, rec["q"]); continue
                    if img.height < 40:
                        short.append("%s-%s" % (pk, rec["q"]))
                    img.save(os.path.join(OUTDIR, "%s-%s.webp" % (pk, rec["q"])), "WEBP", quality=80, method=4)
                rec.update({"pk": pk, "p": label, "kind": kind, "file": os.path.basename(pdf)})
                raw.append(rec); n += 1; total += 1
        print("%s %-12s %2d questions" % (pk, label, n))
    done = {r["pk"] for r in raw}
    merged = [r for r in old if r["pk"] not in done] + raw
    merged.sort(key=lambda r: (r["pk"], int(r["q"][1:])))
    json.dump(merged, open(RAW_OUT, "w"), ensure_ascii=False, indent=0)
    print("wrote %d images; raw -> %s" % (total, RAW_OUT))
    if short:
        print("SHORT:", short)


if __name__ == "__main__":
    main()
