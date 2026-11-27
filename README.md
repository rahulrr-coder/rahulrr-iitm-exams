# IITM Quiz 2 trainer — Stat 1 (Sat 5 Dec 2026, weeks 5–8 + review) and Python weeks 1–4

Static site (no build step). Every past question that falls inside Quiz 1 scope is clustered into **archetypes**
(solving techniques), split into **must-solve** and **good-to-solve**, and shown as the real question image with the
answer hidden until you ask. Progress is stored in the browser (and synced by the optional Netlify function).

| Subject | Questions | Archetypes | Source |
|---|---|---|---|
| Stat 1 weeks 1–9 | 92 | 40 | End Term PYQs (quizpractice.space); W9 kept in case Quiz 2 covers random variables |
| Python weeks 1–4 | 70 | 12 | all Quiz 1 + End Term PYQs since 2023 that need only weeks 1–4 |

## Pages
- `index.html` dashboard and daily plan · `core.html` every archetype ranked by marks (the minimum set)
- `cram.html` week-by-week formula sheet · `stat1.html`, `python.html` week ladders, archetype cards, question view

## Data
`data/<subject>.json` rows (`pk,q,t,m,w,c,d,a,s`) · `data/<subject>_archetypes.json` · `data/manifest.json` (exam name, date, subjects).
Images are in `questions/<subject>/`; option letters are neutralised and the answer key and footer are painted out.

## Tools (run from the repo root)
- `tools/extract.py` — Stat 1 PDFs → images + rows. `PDF_ROOT=<folder with Stat 1 papers>`
- `tools/extract_python.py <PYQ root> <raw.json>` — Python PDFs → images + raw answer keys (`PAPERS=a-b` to run a slice)
- `tools/build_python.py` — classified Python questions → `data/python*.json`
- `tools/build_cram.py` — one-shot Quiz 1 cram migration (refuses to rerun)
- `tools/add_quiz2_cram.py` — one-shot: appends the Stat 1 W5–W9 lessons to `cram.html`
- `tools/build_notes.py` — renders `notes/*.md` into `notes.html`

Archetypes and week tags are AI-generated judgement calls, not an official grouping.
