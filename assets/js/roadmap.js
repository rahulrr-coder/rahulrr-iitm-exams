/* Subject roadmap page renderer. Expects window.SUBJECT_KEY to be set before this loads. */
(function () {
  "use strict";
  var E = window.EndTerm;
  var subKey = window.SUBJECT_KEY;
  var sub = null;

  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  async function main() {
    await E.load();
    sub = E.SUBJECTS.filter(function (s) { return s.key === subKey; })[0];
    if (!sub) return;
    var state = E.loadState();
    var data = await E.loadSubjectData(sub);
    var dl = E.daysLeft();
    document.getElementById("navDays").innerHTML = dl > 0 ? ("<b>" + dl + "</b> days to end-term") : "End-term week";

    function renderStats() {
      var st = E.subjectStats(sub, data, state);
      document.getElementById("overallStats").innerHTML =
        '<div class="stat"><b>' + st.mustDone + '/' + st.mustQ + '</b><span>must-solve cleared</span></div>' +
        '<div class="stat"><b>' + st.pctMust + '%</b><span>must-solve progress</span></div>' +
        '<div class="stat"><b>' + st.goodLeft + '</b><span>good backlog</span></div>' +
        '<div class="stat"><b>' + st.doneQ + '/' + st.totalQ + '</b><span>solved overall</span></div>' +
        '<div class="stat"><b>' + (data.arch.length || 0) + '</b><span>archetypes</span></div>';
    }
    renderStats();

    // week badges -- a week goes green once its must-solve set is cleared
    function renderBadges() {
      document.getElementById("badgeRow").innerHTML =
        E.weekBadges(sub, data, state).map(function (b) {
          return '<span class="badge' + (b.complete ? "" : " locked") + '">' +
            (b.complete ? "✓ " : "") + "W" + b.week + "</span>";
        }).join("");
    }
    renderBadges();

    // keep an archetype's cover chips in step with the ladder (v1 left this
    // as an empty loop, so chips never updated when you ticked a row)
    function syncCovers() {
      document.querySelectorAll(".qchip[data-qid]").forEach(function (chip) {
        chip.classList.toggle("done", !!state.doneQids[subKey][chip.dataset.qid]);
      });
    }

    function renderStreak() {
      var streak = state.streak || { count: 0 };
      document.getElementById("streakBar").innerHTML =
        '<span class="flame">' + (streak.count > 0 ? "🔥" : "💤") + '</span><span>' +
        (streak.count > 0 ? (streak.count + "-day streak") : "No streak yet — tick a question to start one") + '</span>';
    }
    renderStreak();

    // group by week
    var byWeek = {};
    data.rows.forEach(function (r) { (byWeek[r.w] = byWeek[r.w] || []).push(r); });
    var archByWeek = {};
    data.arch.forEach(function (a) { (archByWeek[a.week] = archByWeek[a.week] || []).push(a); });
    var weeks = Object.keys(byWeek).map(Number).sort(function (a, b) { return a - b; });

    // how many questions in OTHER weeks name this week as a dependency -- the
    // honest measure of what breaks later if you skip a week now
    var leanedOn = {};
    data.rows.forEach(function (r) {
      (r.aw || []).forEach(function (w) {
        if (w !== r.w) leanedOn[w] = (leanedOn[w] || 0) + 1;
      });
    });

    // toolbar chips
    var chipsHtml = '<button class="chip" data-w="all" aria-pressed="true">All weeks</button>';
    weeks.forEach(function (w) { chipsHtml += '<button class="chip" data-w="' + w + '" aria-pressed="false">W' + w + '</button>'; });
    document.getElementById("chips").innerHTML = chipsHtml;

    var tierBar = document.createElement("div");
    tierBar.className = "chips tierchips";
    tierBar.id = "tierChips";
    tierBar.innerHTML =
      '<button class="chip tier-must" data-t="must" aria-pressed="true">Must-solve</button>' +
      '<button class="chip tier-good" data-t="good" aria-pressed="false">Good-to-solve</button>' +
      '<button class="chip" data-t="all" aria-pressed="false">All</button>';
    document.getElementById("chips").after(tierBar);

    var sortWrap = document.createElement("label");
    sortWrap.className = "sortby";
    sortWrap.innerHTML = 'Sort <select id="sortBy">' +
      '<option value="d-">Hardest first</option>' +
      '<option value="d+">Easiest first</option>' +
      '<option value="m-">Most marks</option>' +
      '<option value="m+">Fewest marks</option>' +
      '<option value="type">Type (SA, MSQ, MCQ)</option>' +
      '<option value="paper">Paper, newest first</option>' +
      '</select>';
    tierBar.after(sortWrap);

    var done = state.doneQids[subKey];
    var learned = state.archetypesLearned[subKey];
    var rowTier = {}, byQidRow = {};
    data.rows.forEach(function (r) { rowTier[r.qid] = r.tier; byQidRow[r.qid] = r; });

    var html = "";
    weeks.forEach(function (w) {
      var wrows = byWeek[w].slice().sort(function (a, b) { return b.d - a.d || (a.pk < b.pk ? -1 : 1); });
      var warch = archByWeek[w] || [];
      var n = wrows.length, m = wrows.reduce(function (a, r) { return a + r.m; }, 0);
      var avgd = n ? wrows.reduce(function (a, r) { return a + r.d; }, 0) / n : 0;
      var hi = wrows.filter(function (r) { return r.d >= 4; }).length;
      var npap = new Set(wrows.map(function (r) { return r.pk; })).size;
      var alltotal = new Set(data.rows.map(function(r){return r.pk;})).size;

      html += '<section class="week" id="w' + w + '" data-week="' + w + '">';
      html += '<div class="wk-head"><span class="wk-n">W' + w + '</span><h2 class="wk-t">Week ' + w + '</h2>' +
        '<div class="wk-meta"><span><b>' + n + '</b> questions</span><span><b>' + Math.round(m) + '</b> marks</span>' +
        '<span>avg difficulty <b>' + avgd.toFixed(1) + '</b></span><span><b>' + hi + '</b> at 4&ndash;5</span>' +
        '<span>in <b>' + npap + '</b>/' + alltotal + ' papers</span></div></div>';
      html += '<div class="wk-prog"><i data-prog="' + w + '"></i></div>';

      // What's tested: the week's patterns, heaviest first, so with limited
      // days you can see where the marks actually are before opening a card.
      var mustByArch = {};
      wrows.forEach(function (r) {
        if (r.tier !== "must") return;
        var id = data.archByQid[r.qid];
        if (id) mustByArch[id] = (mustByArch[id] || 0) + r.m;
      });
      var ranked = warch.slice().sort(function (x, y) {
        return (mustByArch[y.id] || 0) - (mustByArch[x.id] || 0);
      });
      var mix = { MCQ: 0, MSQ: 0, SA: 0 };
      wrows.forEach(function (r) { mix[r.t] = (mix[r.t] || 0) + 1; });
      var mustN = wrows.filter(function (r) { return r.tier === "must"; }).length;
      var mustM = wrows.reduce(function (a, r) { return a + (r.tier === "must" ? r.m : 0); }, 0);

      if (ranked.length) {
        html += '<div class="wk-brief"><h3>What this week tests</h3><ol class="topics">';
        ranked.forEach(function (a) {
          var mm = Math.round(mustByArch[a.id] || 0);
          html += '<li><a href="#arch-' + a.id + '">' + esc(a.title) + '</a>' +
            '<span class="tm">' + (mm ? mm + ' must-marks' : 'good only') + '</span></li>';
        });
        html += '</ol><p class="wk-facts">' +
          '<b>' + ranked.length + '</b> patterns to learn &middot; ' +
          '<b>' + mustN + '</b> must-solve (' + Math.round(mustM) + ' marks) &middot; ' +
          mix.SA + ' SA / ' + mix.MSQ + ' MSQ / ' + mix.MCQ + ' MCQ' +
          (leanedOn[w] ? ' &middot; <b class="gates">later questions leaning on this week: ' +
            leanedOn[w] + '</b>' : '') +
          '</p></div>';
      }

      if (warch.length) {
        html += '<div class="archgrid">';
        warch.forEach(function (a) {
          var isLearned = !!learned[a.id];
          var nMust = a.covers.filter(function (q) { return rowTier[q] === "must"; }).length;
          var coverChips = a.covers.slice().sort(function (x, y) {
            var mx = rowTier[x] === "must" ? 0 : 1, my = rowTier[y] === "must" ? 0 : 1;
            return mx - my || (byQidRow[y] ? byQidRow[y].d : 0) - (byQidRow[x] ? byQidRow[x].d : 0);
          }).map(function (qid) {
            var r = byQidRow[qid];
            var t = rowTier[qid] === "must" ? " must" : "";
            return '<a class="qchip' + (done[qid] ? ' done' : '') + t + '" data-qid="' + esc(qid) +
              '" href="#q/' + esc(qid) + '" title="' + esc(qid) + '">' +
              (r ? '<span class="cp">' + esc(r.p) + '</span> ' : '') +
              esc(qid.split("-").pop()) + '</a>';
          }).join("");
          html += '<div class="archcard' + (isLearned ? " learned" : "") + '" id="arch-' + a.id + '">' +
            '<div class="ahead"><span class="an">' + a.id + '</span><div style="flex:1">' +
            '<h4>' + esc(a.title) + '</h4>' +
            '<p class="trigger">' + esc(a.trigger) + '</p>' +
            '<p class="target">Solve with help: <a class="tlink" href="#q/' + esc(a.target) + '">' +
            esc(byQidRow[a.target] ? (byQidRow[a.target].p + " " + byQidRow[a.target].q) : a.target) +
            '</a> <span class="hint">opens the question</span></p>' +
            '<div class="coverhead">Then solve cold &mdash; <b>' + nMust + ' must</b>' +
            (a.covers.length - nMust ? ', ' + (a.covers.length - nMust) + ' good' : '') + '</div>' +
            '<div class="covers">' + coverChips + '</div>' +
            '</div><button class="learntgl" data-arch="' + a.id + '">' + (isLearned ? "✓ Learned" : "Mark learned") + '</button></div>' +
            '</div>';
        });
        html += '</div>';
      }

      html += '<table class="tbl"><thead><tr><th></th><th>Paper &middot; Q</th><th>Type</th><th class="h-mk">Mk</th><th>Diff</th><th>Tier</th><th>What it tests</th></tr></thead><tbody>';
      wrows.forEach(function (r) {
        var pillCls = r.t === "MSQ" ? "pill msq" : "pill";
        var archId = data.archByQid[r.qid];
        var archBadge = archId ? '<a class="arch" href="#arch-' + archId + '" data-jump="' + archId + '">' + archId + '</a>' : "";
        var depHtml = (r.aw || []).map(function (aw) { return '<span class="dep">W' + aw + '</span>'; }).join("");
        var isDone = !!done[r.qid];
        html += '<tr class="q' + (isDone ? " done" : "") + '" data-id="' + esc(r.qid) + '" data-d="' + r.d + '" data-tier="' + r.tier +
          '" data-m="' + r.m + '" data-t="' + esc(r.t) + '" data-pk="' + esc(r.pk) + '">' +
          '<td class="c-chk"><input type="checkbox" aria-label="mark ' + esc(r.p) + ' ' + esc(r.q) + ' solved"' + (isDone ? " checked" : "") + '></td>' +
          '<td class="c-ref"><a class="qlink" href="#q/' + esc(r.qid) + '"><span class="pap">' + esc(r.p) + '</span> <span class="qn">' + esc(r.q) + '</span></a></td>' +
          '<td><span class="' + pillCls + '">' + esc(r.t) + '</span></td>' +
          '<td class="c-mk h-mk">' + (r.m % 1 === 0 ? r.m : r.m.toFixed(1)) + '</td>' +
          '<td class="c-d d' + r.d + '"><span class="dbar"><i></i><i></i><i></i><i></i><i></i><b>' + r.d + '</b></span></td>' +
          '<td class="c-t"><span class="tier t-' + r.tier + '">' + (r.tier === "must" ? "must" : "good") + '</span></td>' +
          '<td class="c-q"><span class="con">' + esc(r.c) + '</span>' + archBadge + depHtml + '<span class="stem">' + esc(r.s) + '</span></td></tr>';
      });
      html += '</tbody></table></section>';
    });
    document.getElementById("ladderRoot").innerHTML = html;

    // interactions
    function prog() {
      document.querySelectorAll("section.week").forEach(function (s) {
        var rs = s.querySelectorAll("tr.q"), d = s.querySelectorAll("tr.q.done").length;
        var bar = s.querySelector("[data-prog]");
        if (bar) bar.style.width = (rs.length ? 100 * d / rs.length : 0) + "%";
        var chip = document.querySelector('.chip[data-w="' + s.dataset.week + '"]');
        if (chip) chip.classList.toggle("done-all", rs.length > 0 && d === rs.length);
      });
    }

    document.querySelectorAll("tr.q").forEach(function (tr) {
      tr.querySelector("input").addEventListener("change", function () {
        setDone(tr.dataset.id, this.checked);
      });
    });

    document.querySelectorAll(".learntgl").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var archId = btn.dataset.arch;
        var card = document.getElementById("arch-" + archId);
        var nowLearned = !card.classList.contains("learned");
        E.markLearned(state, subKey, archId, nowLearned);
        card.classList.toggle("learned", nowLearned);
        btn.textContent = nowLearned ? "✓ Learned" : "Mark learned";
        renderStreak();
      });
    });

    var hideDone = document.getElementById("hideDone");
    var curTier = "must";
    function applyDone() {
      document.querySelectorAll("tr.q").forEach(function (tr) {
        var hidden = (hideDone.checked && tr.classList.contains("done")) ||
                     (curTier !== "all" && tr.dataset.tier !== curTier);
        tr.style.display = hidden ? "none" : "";
      });
      // archetype cards are a Round-1 tool; they only clutter the good backlog
      document.querySelectorAll(".archgrid").forEach(function (g) {
        g.style.display = curTier === "good" ? "none" : "";
      });
      filterWeek();
    }
    hideDone.addEventListener("change", applyDone);

    var cur = "all";
    function filterWeek() {
      document.querySelectorAll("section.week").forEach(function (s) {
        var onWeek = (cur === "all" || s.dataset.week === cur);
        // with a tier filter on, an empty week is noise -- this is what makes
        // "Good-to-solve + All weeks" read as the cross-week backlog
        var anyRows = s.querySelectorAll("tr.q:not([style*='none'])").length > 0;
        s.style.display = (onWeek && (curTier === "all" || anyRows)) ? "" : "none";
      });
    }

    // Re-order rows in place rather than re-rendering, so ticks and listeners survive
    var TYPE_ORDER = { SA: 0, MSQ: 1, MCQ: 2 };
    function applySort() {
      var mode = document.getElementById("sortBy").value;
      document.querySelectorAll("section.week tbody").forEach(function (tb) {
        var rows = Array.prototype.slice.call(tb.querySelectorAll("tr.q"));
        rows.sort(function (a, b) {
          var ad = +a.dataset.d, bd = +b.dataset.d, am = +a.dataset.m, bm = +b.dataset.m;
          switch (mode) {
            case "d+": return ad - bd || bm - am;
            case "m-": return bm - am || bd - ad;
            case "m+": return am - bm || bd - ad;
            case "type": return (TYPE_ORDER[a.dataset.t] - TYPE_ORDER[b.dataset.t]) || bd - ad;
            case "paper": return (a.dataset.pk < b.dataset.pk ? 1 : -1);
            default: return bd - ad || (a.dataset.pk < b.dataset.pk ? -1 : 1);
          }
        });
        rows.forEach(function (r) { tb.appendChild(r); });
      });
    }
    document.getElementById("sortBy").addEventListener("change", applySort);

    document.getElementById("tierChips").addEventListener("click", function (e) {
      var b = e.target.closest(".chip");
      if (!b) return;
      curTier = b.dataset.t;
      document.querySelectorAll("#tierChips .chip").forEach(function (c) {
        c.setAttribute("aria-pressed", String(c === b));
      });
      applyDone();
    });
    document.getElementById("chips").addEventListener("click", function (e) {
      var b = e.target.closest(".chip");
      if (!b) return;
      cur = b.dataset.w;
      document.querySelectorAll(".chip").forEach(function (c) { c.setAttribute("aria-pressed", String(c === b)); });
      filterWeek();
      if (cur !== "all") {
        var s = document.getElementById("w" + cur);
        if (s) s.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });

    /* ---- single-question view ------------------------------------------
       Routed off the hash so it stays a plain static site: no build step, no
       router, and every question is still a shareable, bookmarkable URL. */

    var rowByQid = {};
    data.rows.forEach(function (r) { rowByQid[r.qid] = r; });

    // same ordering the ladder uses, so prev/next matches what you see
    var weekOrder = {};
    weeks.forEach(function (w) {
      weekOrder[w] = byWeek[w].slice().sort(function (a, b) {
        return b.d - a.d || (a.pk < b.pk ? -1 : 1);
      }).map(function (r) { return r.qid; });
    });

    var qview = document.createElement("div");
    qview.id = "qview";
    qview.hidden = true;
    document.getElementById("ladderRoot").before(qview);

    var pageFurniture = [".toolbar", ".note", ".badges", "h2.sec"];

    function setBrowseVisible(on) {
      document.getElementById("ladderRoot").hidden = !on;
      pageFurniture.forEach(function (sel) {
        var el = document.querySelector(sel);
        if (el) el.hidden = !on;
      });
      qview.hidden = on;
    }

    function renderQuestion(qid) {
      var r = rowByQid[qid];
      if (!r) { location.hash = ""; return; }
      var order = weekOrder[r.w] || [];
      var i = order.indexOf(qid);
      var prev = i > 0 ? order[i - 1] : null;
      var next = i >= 0 && i < order.length - 1 ? order[i + 1] : null;
      var archId = data.archByQid[qid];
      var isDone = !!state.doneQids[subKey][qid];

      qview.innerHTML =
        '<div class="qpage">' +
          '<div class="qnav">' +
            '<a class="back" href="#w' + r.w + '">&larr; Week ' + r.w + ' ladder</a>' +
            '<span class="spacer"></span>' +
            (prev ? '<a class="pn" href="#q/' + esc(prev) + '">&larr; Prev</a>'
                  : '<span class="pn off">&larr; Prev</span>') +
            (next ? '<a class="pn" href="#q/' + esc(next) + '">Next &rarr;</a>'
                  : '<span class="pn off">Next &rarr;</span>') +
          '</div>' +
          '<div class="qhead">' +
            '<span class="tier t-' + r.tier + '">' + r.tier + '</span>' +
            '<span class="pap">' + esc(r.p) + '</span><span class="qn">' + esc(r.q) + '</span>' +
            '<span class="pill' + (r.t === "MSQ" ? " msq" : "") + '">' + esc(r.t) + '</span>' +
            '<span class="mk">' + (r.m % 1 === 0 ? r.m : r.m.toFixed(1)) + ' marks</span>' +
            '<span class="wk">W' + r.w + '</span>' +
            '<span class="dd d' + r.d + '">difficulty ' + r.d + '</span>' +
            (archId ? '<a class="arch" href="#arch-' + archId + '">' + archId + '</a>' : "") +
          '</div>' +
          '<figure class="qimg"><img src="' + data.imgDir + encodeURIComponent(qid) + '.webp" ' +
            'alt="' + esc(r.p + " " + r.q) + ' as printed in the question paper">' +
            '<figcaption>Cropped from the original paper. The answer is redacted in the image.</figcaption>' +
          '</figure>' +
          '<div class="qtests"><b>What it tests:</b> ' + esc(r.c) + ' &mdash; ' + esc(r.s) + '</div>' +
          '<div class="qans"><button class="reveal" type="button">Reveal answer</button>' +
            '<span class="ansval" hidden>' + esc(r.a) + '</span></div>' +
          '<label class="qdone"><input type="checkbox"' + (isDone ? " checked" : "") + '> ' +
            'Solved this one' + '</label>' +
        '</div>';

      qview.querySelector(".reveal").addEventListener("click", function () {
        this.hidden = true;
        qview.querySelector(".ansval").hidden = false;
      });
      qview.querySelector(".qdone input").addEventListener("change", function () {
        setDone(qid, this.checked);
      });
      setBrowseVisible(false);
      window.scrollTo(0, 0);
    }

    // one place that ticks a question, so the table and the question page agree
    function setDone(qid, done) {
      E.markDone(state, subKey, qid, done);
      var tr = document.querySelector('tr.q[data-id="' + qid + '"]');
      if (tr) {
        tr.classList.toggle("done", done);
        var cb = tr.querySelector("input");
        if (cb) cb.checked = done;
      }
      syncCovers();
      prog(); applyDone(); renderStreak(); renderBadges(); renderStats();
    }

    function route() {
      var h = location.hash;
      if (h.indexOf("#q/") === 0) { renderQuestion(decodeURIComponent(h.slice(3))); return; }
      setBrowseVisible(true);
      if (h.indexOf("#arch-") === 0) {
        var target = document.getElementById(h.slice(1));
        if (target) {
          var weekEl = target.closest("section.week");
          if (weekEl) {
            cur = weekEl.dataset.week;
            document.querySelectorAll("#chips .chip").forEach(function (c) {
              c.setAttribute("aria-pressed", String(c.dataset.w === cur));
            });
            filterWeek();
          }
          setTimeout(function () {
            target.scrollIntoView({ behavior: "smooth", block: "center" });
            target.style.outline = "2px solid var(--accent)";
          }, 150);
        }
      } else if (/^#w\d+$/.test(h)) {
        var sec = document.getElementById(h.slice(1));
        if (sec) setTimeout(function () { sec.scrollIntoView({ block: "start" }); }, 50);
      }
    }

    window.addEventListener("hashchange", route);

    syncCovers(); prog(); applyDone(); applySort(); route();
  }

  main();
})();
