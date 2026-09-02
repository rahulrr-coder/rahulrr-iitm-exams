/* rahulrr-iitm-exams — shared app logic.

   Everything about *which* exam this is lives in data/manifest.json, so
   swapping in the next quiz or end-term is a data change, not a code change.
   Call EndTerm.load() before touching SUBJECTS or EXAM_DATE. */
(function (global) {
  "use strict";

  var LEGACY_KEY = "endterm-app.v1";   // v1 stored everything under one key
  var MUST_SHARE = 0.6;                // ceiling on how much of an archetype is must-solve

  var EXAM_DATE = null, STATE_KEY = null, EXAM = "", SUBJECTS = [];

  async function load() {
    if (SUBJECTS.length) return EXAM;
    var m = await fetchJSON("data/manifest.json");
    EXAM = m.exam;
    EXAM_DATE = new Date(m.examDate + "T00:00:00");
    STATE_KEY = "rahulrr-iitm-exams." + m.exam;
    SUBJECTS = m.subjects.map(function (s) {
      s.file = "data/" + s.key + ".json";
      s.archFile = "data/" + s.key + "_archetypes.json";
      return s;
    });
    var E = global.EndTerm;
    E.SUBJECTS = SUBJECTS; E.EXAM_DATE = EXAM_DATE; E.EXAM = EXAM;
    return m;
  }

  function todayStr(d) {
    d = d || new Date();
    return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
  }

  function daysLeft() {
    var now = new Date();
    var ms = EXAM_DATE - now;
    return Math.max(0, Math.ceil(ms / (1000 * 60 * 60 * 24)));
  }

  function loadState() {
    var s;
    try {
      // fall back to the v1 key once, so existing progress carries over
      s = JSON.parse(localStorage.getItem(STATE_KEY) || localStorage.getItem(LEGACY_KEY) || "{}");
    } catch (e) {
      s = {};
    }
    if (!s.doneQids) s.doneQids = {};
    if (!s.archetypesLearned) s.archetypesLearned = {};
    if (!s.streak) s.streak = { count: 0, lastDay: null };
    SUBJECTS.forEach(function (sub) {
      if (!s.doneQids[sub.key]) s.doneQids[sub.key] = {};
      if (!s.archetypesLearned[sub.key]) s.archetypesLearned[sub.key] = {};
    });
    return s;
  }

  function saveState(s) {
    try {
      localStorage.setItem(STATE_KEY, JSON.stringify(s));
    } catch (e) {}
  }

  function touchStreak(s) {
    var today = todayStr();
    if (s.streak.lastDay === today) return; // already counted today
    var y = new Date();
    y.setDate(y.getDate() - 1);
    var yStr = todayStr(y);
    if (s.streak.lastDay === yStr) {
      s.streak.count = (s.streak.count || 0) + 1;
    } else {
      s.streak.count = 1;
    }
    s.streak.lastDay = today;
    saveState(s);
  }

  function markDone(s, subjectKey, qid, done) {
    if (done) {
      var wasNew = !s.doneQids[subjectKey][qid];
      s.doneQids[subjectKey][qid] = 1;
      if (wasNew) touchStreak(s);
    } else {
      delete s.doneQids[subjectKey][qid];
    }
    saveState(s);
  }

  function markLearned(s, subjectKey, archId, learned) {
    if (learned) {
      s.archetypesLearned[subjectKey][archId] = 1;
      touchStreak(s);
    } else {
      delete s.archetypesLearned[subjectKey][archId];
    }
    saveState(s);
  }

  async function fetchJSON(path) {
    var res = await fetch(path);
    if (!res.ok) throw new Error("failed to load " + path);
    return res.json();
  }

  /* Split each archetype's covered questions into must-solve and good-to-solve.

     Computed here rather than baked into the JSON: the inputs (difficulty and
     marks) are already in every row, so storing a derived tier would just be a
     second copy to keep in sync. Tweak the rule here and everything follows.

     The target is always must. Then the hardest / heaviest questions join it,
     capped at MUST_SHARE of the archetype, so "must" stays the subset actually
     worth marks rather than every repeat of the pattern.

     The target is also re-pointed at the hardest question in the archetype.
     The whole loop is "learn this one with help, then clear the rest cold", so
     the one you learn on has to be at least as hard as everything you then
     face alone -- otherwise you are being sent in under-prepared. With the
     archetypes as authored, 28-39% of must-solve questions were harder than
     their own target. The original pick is kept whenever it is already joint
     hardest, so the clustering's judgement survives where it does not clash. */
  function pickTarget(covered, byQid, stated) {
    var best = stated;
    covered.forEach(function (q) {
      if (!best || byQid[q].d > byQid[best].d ||
          (byQid[q].d === byQid[best].d && byQid[q].m > byQid[best].m)) best = q;
    });
    return best;
  }

  function assignTiers(rows, arch) {
    var byQid = {}, must = {};
    rows.forEach(function (r) { byQid[r.qid] = r; });
    arch.forEach(function (a) {
      var covered = a.covers.filter(function (q) { return byQid[q]; });
      a.target = pickTarget(covered, byQid, byQid[a.target] ? a.target : null) || a.target;
      var picked = {}, n = 0;
      if (byQid[a.target]) { picked[a.target] = 1; n = 1; }
      var cap = Math.max(1, Math.round(MUST_SHARE * covered.length));
      covered.slice().sort(function (x, y) {
        return byQid[y].d - byQid[x].d || byQid[y].m - byQid[x].m;
      }).forEach(function (q) {
        if (n >= cap || picked[q]) return;
        if (byQid[q].d >= 3 || byQid[q].m >= 4) { picked[q] = 1; n++; }
      });
      a.must = Object.keys(picked);
      a.must.forEach(function (q) { must[q] = 1; });
    });
    rows.forEach(function (r) { r.tier = must[r.qid] ? "must" : "good"; });
    return must;
  }

  async function loadSubjectData(sub) {
    var rows = await fetchJSON(sub.file);
    var arch = [];
    try {
      arch = await fetchJSON(sub.archFile);
    } catch (e) {
      arch = []; // archetypes not generated yet for this subject
    }
    rows.forEach(function (r) {
      r.qid = r.pk + "-" + r.q;
    });
    var archByQid = {};
    arch.forEach(function (a) {
      a.covers.forEach(function (qid) {
        archByQid[qid] = a.id;
      });
    });
    var mustQids = assignTiers(rows, arch);
    return { rows: rows, arch: arch, archByQid: archByQid, mustQids: mustQids,
             imgDir: "questions/" + sub.key + "/" };
  }

  function subjectStats(sub, data, state) {
    var done = state.doneQids[sub.key] || {};
    var totalQ = data.rows.length;
    var totalM = data.rows.reduce(function (a, r) { return a + r.m; }, 0);
    var doneQ = 0, doneM = 0, mustQ = 0, mustDone = 0, mustM = 0, mustDoneM = 0, goodLeft = 0;
    data.rows.forEach(function (r) {
      if (done[r.qid]) { doneQ++; doneM += r.m; }
      if (r.tier === "must") {
        mustQ++; mustM += r.m;
        if (done[r.qid]) { mustDone++; mustDoneM += r.m; }
      } else if (!done[r.qid]) {
        goodLeft++;
      }
    });
    return { totalQ: totalQ, totalM: totalM, doneQ: doneQ, doneM: doneM,
      pctQ: totalQ ? Math.round(100 * doneQ / totalQ) : 0,
      pctM: totalM ? Math.round(100 * doneM / totalM) : 0,
      remainingM: totalM - doneM,
      mustQ: mustQ, mustDone: mustDone, mustM: mustM, mustDoneM: mustDoneM,
      pctMust: mustQ ? Math.round(100 * mustDone / mustQ) : 0,
      mustRemainingM: mustM - mustDoneM, goodLeft: goodLeft };
  }

  /* Rank a subject's archetypes by the total marks they cover across all papers,
     weeks ignored. The scarce resource in the last stretch is distinct patterns
     held in your head, not questions solved, so ranking by marks-covered answers
     "what is the fewest patterns that reaches X% of this paper".

     cum is the share of the subject's marks covered by this archetype and every
     one above it. Cached on the data object — core.html re-ranks on every render. */
  function rankArchetypes(data) {
    if (data._ranked) return data._ranked;
    var mk = {};
    data.rows.forEach(function (r) { mk[r.qid] = r.m || 0; });
    var totalM = data.rows.reduce(function (a, r) { return a + (r.m || 0); }, 0);
    var ranked = data.arch.map(function (a) {
      var m = 0;
      a.covers.forEach(function (qid) { m += (mk[qid] || 0); });
      return { id: a.id, week: a.week, title: a.title, trigger: a.trigger, target: a.target,
               covers: a.covers, must: a.must || [], marks: m, n: a.covers.length, cum: 0 };
    }).sort(function (x, y) { return y.marks - x.marks || y.n - x.n; });
    var run = 0;
    ranked.forEach(function (r) { run += r.marks; r.cum = totalM ? run / totalM : 0; });
    data._ranked = { ranked: ranked, totalM: totalM };
    return data._ranked;
  }

  // How many of the ranked archetypes it takes to reach `target` share of marks.
  function coreCut(ranked, target) {
    for (var i = 0; i < ranked.length; i++) if (ranked[i].cum >= target) return i + 1;
    return ranked.length;
  }

  // Planner: for each subject, find priority actions for "today"
  function buildTodaysPlan(allData, state) {
    var dl = daysLeft();
    var items = [];
    SUBJECTS.forEach(function (sub) {
      var data = allData[sub.key];
      if (!data || !data.rows.length) return;
      var stats = subjectStats(sub, data, state);
      // pace against must-solve only; the good backlog is a deliberate deferral
      if (stats.mustRemainingM <= 0 && stats.remainingM <= 0) return;
      var learned = state.archetypesLearned[sub.key] || {};
      /* Next up is the unlearned archetype covering the most marks, not the one
         in the earliest week. With the exam close, week order spends the first
         hours on whatever happens to be in W1; marks order spends them on the
         patterns that actually carry the paper. core.html is the full list. */
      var ranked = rankArchetypes(data).ranked;
      var nextArch = null;
      for (var i = 0; i < ranked.length; i++) {
        if (!learned[ranked[i].id]) { nextArch = ranked[i]; break; }
      }
      var pacing = stats.mustRemainingM > 0 ? stats.mustRemainingM : stats.remainingM;
      var dailyMarksTarget = dl > 0 ? Math.ceil(pacing / dl) : pacing;
      items.push({
        subject: sub, stats: stats, nextArch: nextArch, dailyMarksTarget: dailyMarksTarget
      });
    });
    // prioritize: subjects with an unlearned archetype first, then by remaining marks desc
    items.sort(function (a, b) {
      var aHas = a.nextArch ? 1 : 0, bHas = b.nextArch ? 1 : 0;
      if (aHas !== bHas) return bHas - aHas;
      return b.stats.mustRemainingM - a.stats.mustRemainingM;
    });
    return { daysLeft: dl, items: items };
  }

  function weekBadges(sub, data, state) {
    var done = state.doneQids[sub.key] || {};
    var learned = state.archetypesLearned[sub.key] || {};
    var byWeek = {};
    data.rows.forEach(function (r) {
      byWeek[r.w] = byWeek[r.w] || { total: 0, done: 0 };
      if (r.tier !== "must") return;   // clearing must-solve is what finishes a week
      byWeek[r.w].total++;
      if (done[r.qid]) byWeek[r.w].done++;
    });
    var archByWeek = {};
    data.arch.forEach(function (a) {
      archByWeek[a.week] = archByWeek[a.week] || { total: 0, learned: 0 };
      archByWeek[a.week].total++;
      if (learned[a.id]) archByWeek[a.week].learned++;
    });
    var badges = [];
    Object.keys(byWeek).sort(function (a, b) { return a - b; }).forEach(function (w) {
      var qw = byWeek[w];
      var aw = archByWeek[w] || { total: 0, learned: 0 };
      var complete = qw.total > 0 && qw.done === qw.total && (aw.total === 0 || aw.learned === aw.total);
      badges.push({ week: w, complete: complete });
    });
    return badges;
  }

  global.EndTerm = {
    EXAM_DATE: EXAM_DATE, SUBJECTS: SUBJECTS, EXAM: EXAM, load: load,
    daysLeft: daysLeft, loadState: loadState, saveState: saveState,
    markDone: markDone, markLearned: markLearned,
    loadSubjectData: loadSubjectData, subjectStats: subjectStats,
    rankArchetypes: rankArchetypes, coreCut: coreCut,
    buildTodaysPlan: buildTodaysPlan, weekBadges: weekBadges, todayStr: todayStr
  };
})(window);
