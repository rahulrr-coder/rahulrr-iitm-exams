#!/usr/bin/env python3
"""Verify every extracted question image. Exits non-zero if anything is wrong.

This is the gate that matters: it re-derives the geometry from the source PDFs
and checks all ~1300 images, rather than trusting a hand-picked sample. It
proves three things that would each silently break the app:

  * coverage      -- every indexed question has an image, and vice versa
  * redaction     -- every answer marker's region in the saved image is blank
  * no leakage    -- no green answer-highlight band, no page footer (which
                     carries the downloader's email) inside any crop
"""
import json, os, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract as E

ROOT = E.ROOT
GREEN_ROW_MAX = 50    # a real highlight band is ~1000px wide; glyph noise is <10
GREEN_BAND_ROWS = 3   # ...and is many rows deep, unlike a compression artifact
SAT_GREEN_MAX = 24    # the answer card's accent bar; a few px is codec ringing
INK = 200             # darker than this is real content, not compression noise


def green_rows(img):
    """Rows carrying enough green to be an answer highlight rather than noise."""
    w, h = img.size
    px = img.load()
    bad = []
    for y in range(h):
        n = 0
        for x in range(0, w, 3):
            r, g, b = px[x, y]
            if g > r + 4 and g > b + 4 and min(r, g, b) > 200:
                n += 1
        if n * 3 > GREEN_ROW_MAX:
            bad.append((y, n * 3))
    # A real highlight is a solid band tens of rows deep. A stray row or two is
    # WebP ringing introduced after the flatten pass, so require a run.
    runs, run = [], []
    for item in bad:
        if run and item[0] == run[-1][0] + 1:
            run.append(item)
        else:
            if len(run) >= GREEN_BAND_ROWS:
                runs.extend(run)
            run = [item]
    if len(run) >= GREEN_BAND_ROWS:
        runs.extend(run)
    return runs


def saturated_green(img):
    """Count strong green pixels -- the answer card's accent bar and tick glyph.

    Nothing else in these papers is green; question figures are greyscale or
    blue. A handful of pixels is codec ringing, a bar is dozens.
    """
    w, h = img.size
    px = img.load()
    n = 0
    for y in range(h):
        for x in range(0, w, 2):
            r, g, b = px[x, y]
            if g > r + 30 and g > b + 30:
                n += 1
    return n * 2


def main():
    fails, checked = [], 0
    for folder, subject in E.SUBJECTS.items():
        rows = json.load(open(os.path.join(ROOT, "data", "%s.json" % subject)))
        want = {}
        for r in rows:
            want.setdefault(r["pk"], set()).add(r["q"])
        by_token = {pk[4:]: pk for pk in want}
        outdir = os.path.join(ROOT, "questions", subject)

        # coverage: files on disk vs qids in the data
        on_disk = {f[:-5] for f in os.listdir(outdir) if f.endswith(".webp")}
        expected = {"%s-%s" % (pk, q) for pk, qs in want.items() for q in qs}
        for qid in sorted(expected - on_disk):
            fails.append("%s: no image for %s" % (subject, qid))
        for qid in sorted(on_disk - expected):
            fails.append("%s: orphan image %s" % (subject, qid))

        src = os.path.join(E.PDF_ROOT, folder)
        for fn in sorted(os.listdir(src)):
            if not fn.endswith(".pdf"):
                continue
            pk = by_token.get(E.paper_token(fn))
            if not pk:
                fails.append("%s: no paper key for %s" % (subject, fn)); continue
            pages = E.page_words(os.path.join(src, fn))
            qs = E.find_questions(pages)
            for k, (qno, _p, _y) in enumerate(qs):
                if qno not in want[pk]:
                    continue
                qid = "%s-%s" % (pk, qno)
                path = os.path.join(outdir, qid + ".webp")
                if not os.path.exists(path):
                    continue
                img = Image.open(path).convert("RGB")
                checked += 1

                if img.height < 40:
                    fails.append("%s: only %dpx tall" % (qid, img.height))

                # geometry, recomputed against a stand-in for the page renders
                stub = [type("P", (), {"height": 841.89 * E.SCALE})() for _ in pages]
                slices = E.band_slices(qs, k, pages, stub)
                offsets, acc = {}, 0
                for p, top, bottom in slices:
                    page_h = 841.89
                    if bottom > E.footer_y(pages[p], page_h) + 1:
                        fails.append("%s: slice on page %d runs into the footer" % (qid, p + 1))
                    offsets[p] = (acc, top)
                    acc += int(bottom * E.SCALE) - int(top * E.SCALE)

                # every answer marker must land on blank pixels
                boxes, _stray = E.redactions(qs, k, pages)
                for p, bs in boxes.items():
                    if p not in offsets:
                        continue
                    base, top = offsets[p]
                    for x0, y0, x1, y1 in bs:
                        ix0 = max(0, int(x0 * E.SCALE))
                        ix1 = min(img.width, int(x1 * E.SCALE))
                        iy0 = max(0, base + int((y0 - top) * E.SCALE))
                        iy1 = min(img.height, base + int((y1 - top) * E.SCALE))
                        if ix1 <= ix0 or iy1 <= iy0:
                            continue
                        region = img.crop((ix0, iy0, ix1, iy1))
                        # real ink is 40-90; lossy WebP leaves blank areas at 240+
                        if min(e[0] for e in region.getextrema()) < INK:
                            fails.append("%s: answer marker still visible at %d,%d"
                                         % (qid, ix0, iy0))
                            break

                bad = green_rows(img)
                if bad:
                    fails.append("%s: answer highlight survives on %d rows (worst %s)"
                                 % (qid, len(bad), max(bad, key=lambda t: t[1])))
                sg = saturated_green(img)
                if sg > SAT_GREEN_MAX:
                    fails.append("%s: %d green answer-marker pixels survive" % (qid, sg))

    print("checked %d images" % checked)
    if fails:
        print("\n%d PROBLEM(S):" % len(fails))
        for f in fails[:40]:
            print("  -", f)
        if len(fails) > 40:
            print("  ... and %d more" % (len(fails) - 40))
        return 1
    print("all good: coverage, redaction, no highlight, no footer")
    return 0


if __name__ == "__main__":
    sys.exit(main())
