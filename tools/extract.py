#!/usr/bin/env python3
"""Crop each PYQ out of its source PDF as a self-contained image, answer redacted.

Needs only poppler (pdftoppm, pdftotext) and Pillow -- both already present.

The source PDFs have no usable text for the questions themselves (formulas are
rasterised), but the *labels* are real text: "Q12", "OPTIONS", "Correct",
"ANSWER". So we locate questions by their label bounding boxes and crop the
rendered page image between them.

Two things get painted over before saving:
  * the answer markers -- "checkmark Correct" sits inline beside the right option
    (MCQ/MSQ), while SA papers use an "ANSWER" heading followed by the value.
  * the page footer, which carries the downloader's name and email on every
    page. These crops go to a public site.

The papers also tint the correct option's row pale green, so removing only the
text would still hand over the answer. Every near-white background is therefore
flattened to pure white -- that kills the green wash and the zebra striping
together -- and the redaction boxes are painted white too, so their position
gives nothing away either.
"""
import json, os, re, subprocess, tempfile
from PIL import Image, ImageChops, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_ROOT = os.path.expanduser("~/Documents/IITM-T2-Q1/End Term PYQs")
SUBJECTS = {"Math2": "math2", "Stat1": "stat1", "CT": "ct", "Eng1": "english1"}

DPI = 150
SCALE = DPI / 72.0
LABEL_X_MAX = 80      # question labels live in the left margin; body text starts right of this
TOP_MARGIN = 30       # where a continuation slice starts on a fresh page
LABEL_PAD = 6         # keep a little air above the "Q12" label
END_PAD = 16          # ...and cut above the next question's card border
SA_MARGIN = 14        # the SA answer card's top edge and green bar sit above "ANSWER"
REDACT_PAD = 2
FILL = (255, 255, 255)   # match the flattened background: an invisible redaction
FLATTEN_MIN = 235        # any pixel this pale is background, whatever its hue

MONTHS = "jan feb mar apr may jun jul aug sep oct nov dec".split()
WORD_RE = re.compile(
    r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>')


def paper_token(filename):
    """Pull a 'YYYY_mon' key out of a portal filename, whichever style it uses."""
    b = os.path.basename(filename).lower()
    m = re.search(r"(20\d\d)_(" + "|".join(MONTHS) + r")", b)          # 2023_dec24_iit_m...
    if m:
        return "%s_%s" % (m.group(1), m.group(2))
    m = re.search(r"_(\d{1,2})_(" + "|".join(MONTHS) + r")_(\d\d)", b)  # maths2_06_may_26
    if m:
        return "20%s_%s" % (m.group(3), m.group(2))
    return None


def page_words(pdf):
    """[[(x0,y0,x1,y1,text), ...], ...] in PDF points, one list per page."""
    xml = subprocess.run(["pdftotext", "-bbox-layout", pdf, "-"],
                         capture_output=True, text=True, check=True).stdout
    pages = []
    for chunk in xml.split("<page ")[1:]:
        pages.append([(float(a), float(b), float(c), float(d),
                       w.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">"))
                      for a, b, c, d, w in WORD_RE.findall(chunk)])
    return pages


def footer_y(words, page_h):
    """Top of the 'Downloaded by ... <email>' footer, or the page bottom."""
    ys = [w[1] for w in words if w[4] == "Downloaded" or "quizpractice.space" in w[4]]
    return (min(ys) - 4) if ys else (page_h - 30)


def flatten(img):
    """Repaint every near-white pixel pure white.

    The correct option is highlighted with a pale green wash (240,255,243) and
    the other options are zebra-striped (248,250,251); both are well above
    FLATTEN_MIN while real content -- text, rules, formula glyphs -- is far
    below it. Flattening leaves the page readable and colour-blind to answers.
    """
    r, g, b = img.split()
    darkest = ImageChops.darker(ImageChops.darker(r, g), b)
    mask = darkest.point(lambda v: 255 if v >= FLATTEN_MIN else 0)
    img.paste((255, 255, 255), mask=mask)
    return img


def render_pages(pdf, outdir):
    subprocess.run(["pdftoppm", "-r", str(DPI), "-png", pdf, os.path.join(outdir, "pg")],
                   check=True, capture_output=True)
    return sorted(os.path.join(outdir, f) for f in os.listdir(outdir) if f.endswith(".png"))


def find_questions(pages):
    """[(qno, page_index, y_of_label)] in document order."""
    out = []
    for i, words in enumerate(pages):
        for x0, y0, _x1, _y1, text in words:
            if x0 < LABEL_X_MAX and re.fullmatch(r"Q\d+", text):
                out.append((text, i, y0))
    return out


def band_slices(qs, k, pages, page_imgs):
    """Vertical slices (page_index, y_top, y_bottom) in points covering question k."""
    _q, p0, y0 = qs[k]
    y0 = max(0, y0 - LABEL_PAD)
    if k + 1 < len(qs):
        p1, y1 = qs[k + 1][1], qs[k + 1][2] - END_PAD
    else:
        p1, y1 = len(pages) - 1, None
    out = []
    for p in range(p0, p1 + 1):
        page_h = page_imgs[p].height / SCALE
        top = y0 if p == p0 else TOP_MARGIN
        bottom = y1 if (p == p1 and y1 is not None) else footer_y(pages[p], page_h)
        bottom = min(bottom, footer_y(pages[p], page_h))
        if bottom - top > 4:
            out.append((p, top, bottom))
    return out


def redactions(qs, k, pages):
    """Boxes to paint, in points, as {page_index: [(x0,y0,x1,y1), ...]}."""
    _q, p0, y0 = qs[k]
    p1 = qs[k + 1][1] if k + 1 < len(qs) else len(pages) - 1
    y1 = qs[k + 1][2] if k + 1 < len(qs) else None
    boxes, stray = {}, 0
    for p in range(p0, p1 + 1):
        for x0, wy0, x1, wy1, text in pages[p]:
            if p == p0 and wy0 < y0 - 1:
                continue
            if p == p1 and y1 is not None and wy0 >= y1 - 1:
                continue
            if text in ("✓", "Correct"):
                boxes.setdefault(p, []).append((x0, wy0, x1, wy1))
                if text == "Correct" and not any(
                        w[4] == "✓" and abs(w[1] - wy0) < 4 and 0 < x0 - w[2] < 40
                        for w in pages[p]):
                    stray += 1
            elif text == "ANSWER" and x0 < 120:
                # SA: the value sits under the heading, so kill everything below
                # it -- starting above the heading, because the answer card's
                # top edge and green accent bar are drawn there.
                page_h = 841.89
                end = y1 if (p == p1 and y1 is not None) else footer_y(pages[p], page_h)
                boxes.setdefault(p, []).append((0, wy0 - SA_MARGIN, 10000, end))
    return boxes, stray


def build_image(slices, boxes, page_imgs):
    parts = []
    for p, top, bottom in slices:
        img = page_imgs[p].crop((0, int(top * SCALE), page_imgs[p].width,
                                 int(bottom * SCALE))).convert("RGB")
        d = ImageDraw.Draw(img)
        for x0, y0, x1, y1 in boxes.get(p, []):
            ry0, ry1 = (y0 - top) * SCALE - REDACT_PAD, (y1 - top) * SCALE + REDACT_PAD
            if ry1 > 0 and ry0 < img.height:
                d.rectangle([x0 * SCALE - REDACT_PAD, ry0, x1 * SCALE + REDACT_PAD, ry1], fill=FILL)
        parts.append(img)
    if not parts:
        return None
    if len(parts) == 1:
        out = parts[0]
    else:
        w, h = max(p.width for p in parts), sum(p.height for p in parts)
        out = Image.new("RGB", (w, h), (255, 255, 255))
        y = 0
        for p in parts:
            out.paste(p, (0, y)); y += p.height
    return trim_bottom(out)


def trim_bottom(img):
    """Drop trailing blank rows -- redacting an SA answer can leave half a page."""
    bbox = ImageChops.difference(img, Image.new("RGB", img.size, (255, 255, 255))).getbbox()
    if bbox and bbox[3] + 12 < img.height:
        return img.crop((0, 0, img.width, bbox[3] + 12))
    return img


def main():
    total, skipped, strays, short = 0, 0, 0, []
    for folder, subject in SUBJECTS.items():
        rows = json.load(open(os.path.join(ROOT, "data", "%s.json" % subject)))
        want = {}
        for r in rows:
            want.setdefault(r["pk"], set()).add(r["q"])
        by_token = {pk[4:]: pk for pk in want}
        outdir = os.path.join(ROOT, "questions", subject)
        os.makedirs(outdir, exist_ok=True)
        src = os.path.join(PDF_ROOT, folder)
        for fn in sorted(os.listdir(src)):
            if not fn.endswith(".pdf"):
                continue
            pk = by_token.get(paper_token(fn))
            if not pk:
                print("  ?? no paper key for", fn); continue
            pdf = os.path.join(src, fn)
            pages = page_words(pdf)
            qs = find_questions(pages)
            with tempfile.TemporaryDirectory() as td:
                page_imgs = [flatten(Image.open(f).convert("RGB"))
                             for f in render_pages(pdf, td)]
                if len(page_imgs) != len(pages):
                    print("  !! page count mismatch", fn, len(page_imgs), len(pages)); continue
                n = 0
                for k, (qno, _p, _y) in enumerate(qs):
                    if qno not in want[pk]:
                        skipped += 1; continue
                    boxes, stray = redactions(qs, k, pages)
                    strays += stray
                    img = build_image(band_slices(qs, k, pages, page_imgs), boxes, page_imgs)
                    if img is None:
                        print("  !! empty band", pk, qno); continue
                    if img.height < 40:
                        short.append("%s-%s" % (pk, qno))
                    img.save(os.path.join(outdir, "%s-%s.webp" % (pk, qno)),
                             "WEBP", quality=80, method=4)
                    n += 1; total += 1
            print("  %-13s %-4s %2d/%2d questions" % (subject, pk[:3], n, len(want[pk])))
    print("\nwrote %d images, skipped %d unindexed labels" % (total, skipped))
    print("'Correct' without an adjacent checkmark: %d" % strays)
    if short:
        print("SUSPICIOUSLY SHORT:", short)


if __name__ == "__main__":
    main()
