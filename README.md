# rahulrr-iitm-exams

Archetype-based PYQ trainer for IITM BS exams. Currently loaded with the **End Term Sep 2026**
set: Math 2, Stat 1, English 1, Computational Thinking — 1302 classified past questions in 329
archetypes.

Every past question is clustered into an **archetype** — a recurring solving pattern. Solve the
flagged target question with AI help, internalise the trigger, then clear the rest of that pattern
cold. Each question opens on its own page showing the **real question cropped from the source PDF**,
with the answer redacted from the image and revealed only when you click.

## The loop it encodes

Per week, two rounds:

1. **Round 1 — learn.** Work the archetype cards in order, solving each target question with help,
   until every archetype in the week is marked learned.
2. **Round 2 — solo.** Switch the filter to **Must-solve** and clear those with no help.
3. When must-solve is empty, the week badge goes green — **move to the next week.** Do not stop to
   clear *good-to-solve*; that is deferred on purpose.
4. **Final week before the exam:** one revision pass over the cross-week good-to-solve backlog,
   linked from the dashboard.

**When there is not enough time left for week order.** `core.html` drops the weeks entirely and
ranks every archetype by the total marks it covers, so working down it buys the most marks per
pattern learned. Pick a coverage target (50 / 65 / 80% of the paper) and it draws the line at the
archetype that reaches it; the tail below is collapsed. The order within a subject never changes
with the target, so a lost day means stopping higher up the same list, not replanning. The
dashboard's daily plan picks from the top of these lists too.

Must vs good is computed, not hand-labelled: an archetype's target is always must, joined by its
hardest and heaviest questions (difficulty ≥ 3 or marks ≥ 4, highest first) up to 60% of the
archetype. The rule lives in `assignTiers()` in `assets/js/app.js` — change it there and every
view follows.

## Structure

```
index.html                     dashboard: countdown, must-solve progress, today's plan, good backlog
core.html                      every archetype ranked by marks covered, weeks ignored — the minimum set
math2.html stat1.html …        one page per subject (week ladder + archetype cards + question view)
ct-datasets.html               the five sample datasets CT pseudocode runs over — a pop-out reference sheet
data/manifest.json             THE file that defines the current exam
data/<subject>.json            classified questions
data/<subject>_archetypes.json archetype clusters
questions/<subject>/<qid>.webp cropped, answer-redacted question images
tools/extract.py               builds those images from the source PDFs
tools/check.py                 verifies every one of them
assets/js/app.js               state, tiering, planner
assets/js/roadmap.js           subject page + single-question view
```

No build step, no dependencies, no backend. Progress lives in `localStorage`, per browser.

CSS and JS are referenced with a `?v=N` query. **Bump that number in every HTML file
whenever you change `style.css`, `app.js`, or `roadmap.js`** — otherwise browsers keep serving the
cached copy and your change appears not to have deployed.

## The CT datasets sheet

CT pseudocode questions do not carry their own data: they loop over five datasets — **Scores,
Words, Library, Olympics, Shopping Bills** — printed once as a reference sheet with the paper and
then referred to by name for the rest of it. Solving a question without the sheet in front of you
means guessing which columns exist.

`ct-datasets.html` is that sheet, transcribed from the scan the site already carries
(`questions/ct/C01_2022_aug-Q2.webp`, still linked at the bottom of the page as the source of
truth). It is a standalone page with no dependency on the roadmap: open it in a second window and
leave it there. Each dataset shows the columns in paper order, the first and last row — the only
rows the paper prints — the row count taken from the last `SeqNo`, and notes on the derived
columns (`Total` = M+P+C, `LetterCount` counts letters not characters, `Cost` = Qty × Price), all
checked against every printed row. **Compact** shrinks it for a narrow side window and the choice
sticks.

Each section also lists the PYQs in the current set that run over that dataset. Those are matched
on the classified cluster and stem at load time rather than hand-listed, so swapping in a new exam
rewires them with no edit here. It is reachable from the **CT Data** nav tab on every page, from
the CT roadmap masthead, and from a `Datasets ↗` link on every CT question page — all of which
open it in a new window.

## Run locally

```
python3 -m http.server 8000
```

## Swapping in the next exam

The app is subject- and exam-agnostic; nothing in the HTML, CSS, or JS names a specific exam.
To point it at a different quiz or end-term:

1. Drop the new papers in `~/Documents/IITM-T2-Q1/End Term PYQs/<Folder>/` and set `PDF_ROOT` /
   `SUBJECTS` in `tools/extract.py` if the folders differ.
2. Replace `data/<subject>.json` and `data/<subject>_archetypes.json`.
3. Edit `data/manifest.json` — exam name, exam date, subject list. A new exam name gives you a
   fresh progress bucket, so old progress is not mixed in.
4. `python3 tools/extract.py && python3 tools/check.py`
5. `git push` — Netlify redeploys on its own.

Paper keys are matched to PDFs by the date in the filename, so new papers need no manual mapping.

## How the question images are made

Math and stats PDFs have no copy-pasteable question text — formulas are rasterised. But the
*labels* are real text, so `tools/extract.py` uses `pdftotext -bbox-layout` (poppler) to find every
`Q<n>` label's bounding box, renders the page with `pdftoppm`, and crops the band between one
question and the next, stitching across page breaks.

Three things are removed before saving:

- **the answer text** — `✓ Correct` sits inline beside the right option (MCQ/MSQ); SA papers put
  the value under an `ANSWER` heading.
- **the answer highlight** — the correct option's row is washed pale green, which would give the
  answer away on its own. Every near-white pixel is flattened to white, killing the wash and the
  zebra striping together. Redactions are painted white too, so their *position* reveals nothing.
- **the page footer** — it carries the downloader's name and email on every page, and this site
  is public. It is painted over rather than cropped away: the papers stamp it at a fixed height,
  so on a full page the last option can sit *below* it, and cutting there silently truncated
  real questions.

`tools/audit_weeks.py` is a separate, optional sanity check on week assignments: it confirms weeks
are coherent groupings, then flags any question whose nearest neighbours sit in a different week.
Its output is candidates for human review, not errors — a question can legitimately straddle two
weeks, which is what `aw` records. Run it after swapping in a new exam.

`tools/check.py` re-derives the geometry and verifies all 1302 images: coverage both ways, every
answer marker and footer region blank, and no surviving highlight band. It exits non-zero on any
failure — run it after any change to the pipeline.

## Deploy

Pushing to `main` redeploys via Netlify (site `endterm-roadmap-rahulrr`). `netlify.toml` publishes
the repo root as-is; there is no build command.
