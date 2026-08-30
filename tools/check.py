#!/usr/bin/env python3
"""Verify every extracted question image. Exits non-zero if anything is wrong.

This is the gate that matters: it re-derives the geometry from the source PDFs
and checks all ~1300 images, rather than trusting a hand-picked sample. It
proves three things that would each silently break the app:

  * coverage      -- every indexed question has an image, and vice versa
  * redaction     -- every answer marker's region in the saved image is blank.
                     This also covers the SA answer card's green accent bar,
                     which sits inside that region -- so there is no separate
                     colour check to false-positive on CT's syntax-highlighted
                     pseudocode.
  * data truth    -- each record's type and marks match the labels printed on
                     the paper it came from. This caught a question v1 had
                     typed SA that the paper prints as MCQ.
  * no leakage    -- no green answer-highlight band, and the page footer
                     (which carries the downloader's email) painted out
                     wherever it falls inside a crop
"""
import json, os, re, sys
from PIL import Image, ImageChops

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract as E

ROOT = E.ROOT
GREEN_ROW_MAX = 50    # a real highlight band is ~1000px wide; glyph noise is <10
GREEN_BAND_ROWS = 3   # ...and is many rows deep, unlike a compression artifact
INK = 200             # darker than this is real content, not compression noise


def _mask(img, delta, pale):
    """255 where a pixel is green, 0 elsewhere. All C-speed PIL ops.

    Pure-Python per-pixel loops over 1300 full-page images take half an hour;
    band arithmetic does the same work in a couple of minutes.
    """
    r, g, b = img.split()
    hit = ImageChops.multiply(
        ImageChops.subtract(g, r).point(lambda v: 255 if v >= delta else 0),
        ImageChops.subtract(g, b).point(lambda v: 255 if v >= delta else 0))
    if pale:
        darkest = ImageChops.darker(ImageChops.darker(r, g), b)
        hit = ImageChops.multiply(hit, darkest.point(lambda v: 255 if v > 200 else 0))
    return hit


def green_rows(img):
    """Rows carrying enough green to be an answer highlight rather than noise.

    A real highlight is a solid band tens of rows deep; a stray row or two is
    WebP ringing introduced after the flatten pass, so require a run.
    """
    m = _mask(img, 5, True)
    w, h = img.size
    # box-resizing to one column gives the mean of each row in a single call
    profile = m.resize((1, h), Image.BOX).load()
    cutoff = 255.0 * GREEN_ROW_MAX / w
    bad = [(y, int(profile[0, y] / 255.0 * w)) for y in range(h) if profile[0, y] > cutoff]
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


def main():
    fails, checked = [], 0
    for folder, subject in E.SUBJECTS.items():
        rows = json.load(open(os.path.join(ROOT, "data", "%s.json" % subject)))
        want = {}
        for r in rows:
            want.setdefault(r["pk"], {})[r["q"]] = r
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
            for k, (qno, p_idx, y_lbl) in enumerate(qs):
                if qno not in want[pk]:
                    continue
                rec = want[pk][qno]
                line = [w for w in pages[p_idx] if abs(w[1] - y_lbl) < 6]
                typ = next((w[4] for w in line if w[4] in ("MCQ", "MSQ", "SA")), None)
                txt = " ".join(w[4] for w in sorted(line, key=lambda w: w[0]))
                mm = re.search(r"\[(\d+(?:\.\d+)?)\s*marks?\]", txt)
                if typ and typ != rec["t"]:
                    fails.append("%s-%s: paper prints %s, data says %s" % (pk, qno, typ, rec["t"]))
                if mm and abs(float(mm.group(1)) - rec["m"]) > 0.01:
                    fails.append("%s-%s: paper prints %s marks, data says %s"
                                 % (pk, qno, mm.group(1), rec["m"]))
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
                    offsets[p] = (acc, top, bottom)
                    acc += int(bottom * E.SCALE) - int(top * E.SCALE)

                # every answer marker -- and the name/email footer, which
                # redactions() also returns -- must land on blank pixels
                boxes, _stray = E.redactions(qs, k, pages)
                for p, bs in boxes.items():
                    if p not in offsets:
                        continue
                    base, top, bottom = offsets[p]
                    for x0, y0, x1, y1 in bs:
                        # A marker can sit below where this page was cut (the
                        # footer line), so it never reaches the image. Check the
                        # part that actually landed in the crop, and nothing else
                        # -- mapping the whole box would run into the next page's
                        # rows and report a leak that is not there.
                        cy0, cy1 = max(y0, top), min(y1, bottom)
                        if cy1 <= cy0:
                            continue
                        ix0 = max(0, int(x0 * E.SCALE))
                        ix1 = min(img.width, int(x1 * E.SCALE))
                        iy0 = max(0, base + int((cy0 - top) * E.SCALE))
                        iy1 = min(img.height, base + int((cy1 - top) * E.SCALE))
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

    print("checked %d images" % checked)
    if fails:
        print("\n%d PROBLEM(S):" % len(fails))
        for f in fails[:40]:
            print("  -", f)
        if len(fails) > 40:
            print("  ... and %d more" % (len(fails) - 40))
        return 1
    print("all good: coverage, redaction, no highlight, no footer, data matches the papers")
    return 0


if __name__ == "__main__":
    sys.exit(main())
