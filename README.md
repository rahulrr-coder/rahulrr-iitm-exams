# End Term Roadmap

Archetype-based PYQ trainer for IITM BS end-term prep (Math 2, Stat 1, English 1, Computational Thinking).

Every classified PYQ across four subjects is clustered into a handful of **archetypes** per week — recurring
problem-solving patterns. Solve the flagged target question with AI help, internalise the trigger, then clear
every other question that matches it on your own.

## Structure

- `index.html` — dashboard: countdown to 13 Sep 2026, per-subject progress, an auto-adjusting "today's plan", streaks.
- `math2.html`, `stat1.html`, `english1.html`, `ct.html` — one roadmap page per subject: week-by-week archetype
  cards above the full PYQ ladder table, every row tagged back to its archetype.
- `assets/css/style.css` — shared design system (light/dark aware).
- `assets/js/app.js` — data loading, unified localStorage state, the daily planner algorithm, streak/badge logic.
- `assets/js/roadmap.js` — renders a subject's roadmap page from its data + archetype files.
- `data/<subject>.json` — classified PYQ rows (paper, question, marks, week, difficulty, concept, answer, stem).
- `data/<subject>_archetypes.json` — AI-generated archetype clusters (title, target question, trigger, covered qids).

No backend. Progress is stored in the browser's localStorage — per browser, not synced across devices.

## Run locally

```
python3 -m http.server 8000
```

then open http://localhost:8000

## Deploy

This site is already created on Netlify as `endterm-roadmap-rahulrr` (site id in `netlify.toml`'s comments / your
Netlify dashboard). From this folder:

```
npx netlify-cli deploy --prod --dir=. --site=fbebada3-431a-4a76-9394-6f0c0f6dfae9
```

First run will open a browser to log into Netlify — approve it, then the deploy proceeds.
