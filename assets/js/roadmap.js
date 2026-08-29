/* Subject roadmap page renderer. Expects window.SUBJECT_KEY to be set before this loads. */
(function () {
  "use strict";
  var E = window.EndTerm;
  var subKey = window.SUBJECT_KEY;
  var sub = E.SUBJECTS.filter(function (s) { return s.key === subKey; })[0];
  if (!sub) return;

  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  async function main() {
    var state = E.loadState();
    var data = await E.loadSubjectData(sub);
    var dl = E.daysLeft();
    document.getElementById("navDays").innerHTML = dl > 0 ? ("<b>" + dl + "</b> days to end-term") : "End-term week";

    var st = E.subjectStats(sub, data, state);
    document.getElementById("overallStats").innerHTML =
      '<div class="stat"><b>' + st.totalQ + '</b><span>questions indexed</span></div>' +
      '<div class="stat"><b>' + Math.round(st.totalM) + '</b><span>marks total</span></div>' +
      '<div class="stat"><b>' + st.doneQ + '/' + st.totalQ + '</b><span>solved</span></div>' +
      '<div class="stat"><b>' + st.pctM + '%</b><span>marks banked</span></div>' +
      '<div class="stat"><b>' + (data.arch.length || 0) + '</b><span>archetypes</span></div>';

    // week badges
    var badges = E.weekBadges(sub, data, state);
    document.getElementById("badgeRow").innerHTML = badges.map(function (b) {
      return '<span class="badge' + (b.complete ? "" : " locked") + '">' + (b.complete ? "✓ " : "") + "W" + b.week + "</span>";
    }).join("");

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

    // toolbar chips
    var chipsHtml = '<button class="chip" data-w="all" aria-pressed="true">All weeks</button>';
    weeks.forEach(function (w) { chipsHtml += '<button class="chip" data-w="' + w + '" aria-pressed="false">W' + w + '</button>'; });
    document.getElementById("chips").innerHTML = chipsHtml;

    var done = state.doneQids[subKey];
    var learned = state.archetypesLearned[subKey];

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

      if (warch.length) {
        html += '<div class="archgrid">';
        warch.forEach(function (a) {
          var isLearned = !!learned[a.id];
          var coverChips = a.covers.map(function (qid) {
            return '<span class="qchip' + (done[qid] ? ' done' : '') + '">' + esc(qid.split("-").pop()) + '</span>';
          }).join("");
          html += '<div class="archcard' + (isLearned ? " learned" : "") + '" id="arch-' + a.id + '">' +
            '<div class="ahead"><span class="an">' + a.id + '</span><div style="flex:1">' +
            '<h4>' + esc(a.title) + '</h4>' +
            '<p class="trigger">' + esc(a.trigger) + '</p>' +
            '<p class="target">Solve with help: <b>' + esc(a.target) + '</b></p>' +
            '<div class="covers">' + coverChips + '</div>' +
            '</div><button class="learntgl" data-arch="' + a.id + '">' + (isLearned ? "✓ Learned" : "Mark learned") + '</button></div>' +
            '</div>';
        });
        html += '</div>';
      }

      html += '<table class="tbl"><thead><tr><th></th><th>Paper &middot; Q</th><th>Type</th><th class="h-mk">Mk</th><th>Diff</th><th>What it tests</th><th>Answer</th></tr></thead><tbody>';
      wrows.forEach(function (r) {
        var pillCls = r.t === "MSQ" ? "pill msq" : "pill";
        var archId = data.archByQid[r.qid];
        var archBadge = archId ? '<a class="arch" href="#arch-' + archId + '" data-jump="' + archId + '">' + archId + '</a>' : "";
        var depHtml = (r.aw || []).map(function (aw) { return '<span class="dep">W' + aw + '</span>'; }).join("");
        var isDone = !!done[r.qid];
        html += '<tr class="q' + (isDone ? " done" : "") + '" data-id="' + esc(r.qid) + '" data-d="' + r.d + '">' +
          '<td class="c-chk"><input type="checkbox" aria-label="mark ' + esc(r.p) + ' ' + esc(r.q) + ' solved"' + (isDone ? " checked" : "") + '></td>' +
          '<td class="c-ref"><span class="pap">' + esc(r.p) + '</span> <span class="qn">' + esc(r.q) + '</span></td>' +
          '<td><span class="' + pillCls + '">' + esc(r.t) + '</span></td>' +
          '<td class="c-mk h-mk">' + (r.m % 1 === 0 ? r.m : r.m.toFixed(1)) + '</td>' +
          '<td class="c-d d' + r.d + '"><span class="dbar"><i></i><i></i><i></i><i></i><i></i><b>' + r.d + '</b></span></td>' +
          '<td class="c-q"><span class="con">' + esc(r.c) + '</span>' + archBadge + depHtml + '<span class="stem">' + esc(r.s) + '</span></td>' +
          '<td class="c-a"><span>' + esc(r.a) + '</span></td></tr>';
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
      var cb = tr.querySelector("input");
      cb.addEventListener("change", function () {
        E.markDone(state, subKey, tr.dataset.id, cb.checked);
        tr.classList.toggle("done", cb.checked);
        document.querySelectorAll('.qchip').forEach(function (chip) {
          if (chip.textContent === tr.dataset.id.split("-").pop()) {
            // best-effort visual sync only within same archetype card scope; skip cross-matching
          }
        });
        prog();
        applyDone();
        renderStreak();
        var badges = E.weekBadges(sub, data, state);
        document.getElementById("badgeRow").innerHTML = badges.map(function (b) {
          return '<span class="badge' + (b.complete ? "" : " locked") + '">' + (b.complete ? "✓ " : "") + "W" + b.week + "</span>";
        }).join("");
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
    function applyDone() {
      document.querySelectorAll("tr.q").forEach(function (tr) {
        tr.style.display = (hideDone.checked && tr.classList.contains("done")) ? "none" : "";
      });
      filterWeek();
    }
    hideDone.addEventListener("change", applyDone);

    var hideAns = document.getElementById("hideAns");
    function ans() { document.body.classList.toggle("hide-ans", hideAns.checked); }
    hideAns.addEventListener("change", ans); ans();

    var cur = "all";
    function filterWeek() {
      document.querySelectorAll("section.week").forEach(function (s) {
        s.style.display = (cur === "all" || s.dataset.week === cur) ? "" : "none";
      });
    }
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

    // deep-link to an archetype (from dashboard "today's plan")
    if (location.hash.indexOf("#arch-") === 0) {
      var target = document.getElementById(location.hash.slice(1));
      if (target) {
        var weekEl = target.closest("section.week");
        if (weekEl) { cur = weekEl.dataset.week; document.querySelectorAll(".chip").forEach(function(c){c.setAttribute("aria-pressed", String(c.dataset.w===cur));}); filterWeek(); }
        setTimeout(function () { target.scrollIntoView({ behavior: "smooth", block: "center" }); target.style.outline = "2px solid var(--accent)"; }, 150);
      }
    }

    prog(); applyDone();
  }

  main();
})();
