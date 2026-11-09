#!/usr/bin/env python3
"""Rebuild notes.html from the markdown crib sheets in notes/.

The sheets are the source of truth; this renders them into the site shell so they
are readable on the deployed link (a browser shows raw .md as plain text).
Run after editing anything in notes/:  python3 tools/build_notes.py
"""
import os, re, html, markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "notes.html")

# order on the page: read the must-know sheet last, so the crib sheet comes first
SHEETS = [
    ("python-crib",     "python", "🐍 Python",  "Crib sheet",  "Pattern, weeks 1-4 concept map, formula page, curated practice"),
    ("python-mustknow", "python", "🐍 Python",  "Must-know",   "The 10 traps - read this one last"),
    ("stat1-crib",      "stat1",  "📊 Stat 1",  "Crib sheet",  "Pattern, weeks 1-4 concept map, formula page, curated practice"),
    ("stat1-mustknow",  "stat1",  "📊 Stat 1",  "Must-know",   "The 8 traps - read this one last"),
]

NAV = """<nav class="topnav"><div class="inner">
<a class="brand" href="index.html">IITM Exams</a>
<a class="tab" href="index.html">Dashboard</a>
<a class="tab" href="core.html">Core</a>
<a class="tab" href="cram.html">Cram</a>
<a class="tab" href="stat1.html">Stat 1</a>
<a class="tab" href="python.html">Python</a>
<a class="tab active" href="notes.html">Notes</a>
<div class="spacer"></div>
<div class="daysleft" id="navDays">&mdash; days to Quiz 1</div>
</div></nav>"""

# page-local: long-form prose, read top to bottom and on a phone. The rest of the
# site is cards and tables, so none of these element styles live in style.css.
CSS = """
.wrap.notes{max-width:900px}
.noteshead{padding:30px 0 10px}
.noteshead h1{font-size:clamp(30px,5.4vw,44px);margin:0 0 10px;line-height:1.05;text-wrap:balance}
.noteshead .lede{font-size:17px;color:var(--ink-2);max-width:66ch;margin:0 0 16px}
.notesctl{position:sticky;top:53px;z-index:30;background:var(--ground);border-bottom:1px solid var(--line);
  padding:9px 0;margin:10px 0 0;display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.notesctl a,.notesctl button{font-family:"IBM Plex Mono",monospace;font-size:12px;text-decoration:none;cursor:pointer;
  color:var(--accent);border:1px solid var(--accent-line);background:var(--accent-soft);border-radius:4px;padding:5px 10px}
.notesctl .sp{flex:1}
.sheet{margin:30px 0 0;scroll-margin-top:104px}
.sheeth{display:flex;flex-wrap:wrap;gap:10px;align-items:baseline;padding:0 0 6px;border-bottom:2px solid var(--accent);margin:0 0 4px}
.sheeth h2{font-size:21px;margin:0}
.sheeth .kind{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--accent);background:var(--accent-soft);border:1px solid var(--accent-line);border-radius:4px;padding:3px 7px}
.sheeth .sp{flex:1}
.sheeth .src{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--ink-3)}
.sheeth .blurb{font-size:13px;color:var(--ink-3);flex-basis:100%}
/* the rendered markdown */
.md{font-size:16px;line-height:1.62;color:var(--ink-2)}
.md h1{display:none}            /* the sheet band already names it */
.md h2{font-size:19px;color:var(--ink);margin:30px 0 10px;padding-top:6px;border-top:1px solid var(--line-soft)}
.md h3{font-size:16px;color:var(--ink);margin:22px 0 8px;font-family:"IBM Plex Sans",sans-serif;font-weight:600}
.md h4{font-size:14px;color:var(--ink);margin:18px 0 6px}
.md p{margin:0 0 12px;max-width:74ch}
.md strong{color:var(--ink);font-weight:600}
.md em{color:var(--ink)}
.md hr{border:0;border-top:1px solid var(--line);margin:26px 0}
.md a{color:var(--accent)}
.md ul,.md ol{margin:0 0 14px;padding-left:22px;max-width:74ch}
.md li{margin:0 0 6px}
.md li>ul,.md li>ol{margin:6px 0 0}
.md code{font-family:"IBM Plex Mono",monospace;font-size:.88em;background:var(--panel-2);
  border:1px solid var(--line-soft);border-radius:4px;padding:1px 4px;color:var(--ink)}
.md pre{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);
  padding:13px 15px;overflow-x:auto;margin:0 0 16px;box-shadow:var(--shadow)}
.md pre code{background:none;border:0;padding:0;font-size:13px;line-height:1.55;white-space:pre}
.md blockquote{margin:0 0 14px;padding:2px 0 2px 14px;border-left:3px solid var(--accent-line);color:var(--ink-3)}
.md table{border-collapse:collapse;width:100%;margin:0 0 16px;font-size:14px;display:block;overflow-x:auto}
.md thead th{text-align:left;font-weight:600;color:var(--ink);background:var(--panel-2);
  border-bottom:1px solid var(--line);padding:7px 10px;white-space:nowrap}
.md tbody td{border-bottom:1px solid var(--line-soft);padding:7px 10px;vertical-align:top}
.md tbody tr:last-child td{border-bottom:0}
/* practice checklists: "- [ ] item" in the markdown */
.md li.task{list-style:none;margin-left:-16px}
.md li.task::before{content:"\\2610";font-family:"IBM Plex Mono",monospace;color:var(--ink-3);margin-right:7px}
@media (max-width:620px){
  .md{font-size:15px}
  .md pre code{font-size:12px}
  /* the jump links wrap to four rows on a phone; sticky would eat the screen
     and hide the heading you just jumped to */
  .notesctl{position:static}
  .sheet{scroll-margin-top:60px}
}
@media print{
  nav.topnav,.notesctl,.noteshead .lede{display:none}
  .sheet{break-before:page}
  .md{font-size:11pt;color:#000}
}
"""


LIST = re.compile(r"^\s*(?:[-*+] |\d+\. )")
ROW = re.compile(r"^\s*\|")


def normalise(text):
    """Python-Markdown needs a blank line before a list or table; CommonMark does not.

    The sheets are written CommonMark-style ("intro line:" straight into the list),
    which Python-Markdown otherwise swallows into the paragraph. Insert the blank
    line the parser wants, without touching anything inside a fenced code block.
    """
    out, fence, prev = [], False, ""
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fence = not fence
        elif not fence and prev.strip():
            starts_list = LIST.match(line) and not LIST.match(prev)
            starts_table = ROW.match(line) and not ROW.match(prev)
            # a column-0 line straight after a list item ends the list: without a
            # blank line the parser folds the heading into the last <li>
            ends_list = (LIST.match(prev) and line.strip()
                         and not LIST.match(line) and not line[:1].isspace())
            if starts_list or starts_table or ends_list:
                out.append("")
        out.append(line)
        prev = line
    return "\n".join(out)


def render(path):
    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "attr_list"])
    body = md.convert(normalise(open(path, encoding="utf-8").read()))
    # "- [ ] x" renders as a literal "[ ] x" list item; turn those into box glyphs.
    # Static on purpose: tick-off tracking already lives on the question pages.
    body = re.sub(r'<li>\s*(?:<p>\s*)?\[[ xX]\]\s*', '<li class="task">', body)
    return body


def main():
    parts = [
        "<!doctype html>", '<html lang="en">', "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>Crib Sheets</title>",
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,400;0,600;0,700;1,400&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap">',
        '<link rel="icon" href="favicon.svg" type="image/svg+xml">',
        '<link rel="stylesheet" href="assets/css/style.css?v=10">',
        "<style>" + CSS + "</style>",
        "</head>", "<body>", NAV,
        '<div class="wrap notes">',
        '<header class="noteshead">',
        '<p class="kicker">IITM BS &middot; Quiz 1 &middot; 15 Nov 2026 &middot; weeks 1&ndash;4</p>',
        "<h1>Crib sheets</h1>",
        '<p class="lede">The four revision sheets, rendered from the markdown in <code>notes/</code>. '
        'Read the crib sheet while you revise; read the <strong>must-know</strong> sheet last, right before you walk in.</p>',
        "</header>",
        '<div class="notesctl">',
    ]
    for slug, _, subject, kind, _ in SHEETS:
        parts.append('<a href="#%s">%s &middot; %s</a>' % (slug, html.escape(subject), kind.lower()))
    parts += ['<span class="sp"></span>', '<button id="tPrint">Print</button>', "</div>"]

    for slug, key, subject, kind, blurb in SHEETS:
        src = os.path.join(ROOT, "notes", slug + ".md")
        parts += [
            '<section class="sheet s-%s" id="%s">' % (key, slug),
            '<div class="sheeth">',
            "<h2>%s</h2>" % html.escape(subject),
            '<span class="kind">%s</span>' % html.escape(kind),
            '<span class="sp"></span>',
            '<span class="src">notes/%s.md</span>' % slug,
            '<span class="blurb">%s</span>' % html.escape(blurb),
            "</div>",
            '<div class="md">', render(src), "</div>",
            "</section>",
        ]

    parts += [
        "</div>",
        "<script>",
        '(function(){',
        '  var b=document.getElementById("tPrint");',
        '  if(b) b.addEventListener("click",function(){window.print();});',
        '  var d=new Date("2026-11-15T14:00:00"), n=new Date();',
        '  var dl=Math.ceil((d-n)/864e5), el=document.getElementById("navDays");',
        '  if(el) el.innerHTML = dl>0 ? ("<b>"+dl+"</b> days to Quiz 1") : "Quiz day";',
        "})();",
        "</script>",
        "</body>", "</html>",
    ]
    open(OUT, "w", encoding="utf-8").write("\n".join(parts) + "\n")
    print("wrote %s (%d bytes) from %d sheets" % (OUT, os.path.getsize(OUT), len(SHEETS)))


if __name__ == "__main__":
    main()
