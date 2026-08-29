/* End Term Roadmap — shared app logic */
(function (global) {
  "use strict";

  var EXAM_DATE = new Date("2026-09-13T00:00:00");
  var STATE_KEY = "endterm-app.v1";
  var SUBJECTS = [
    { key: "math2", label: "Math 2", emoji: "📐", file: "data/math2.json", archFile: "data/math2_archetypes.json", weeks: 12 },
    { key: "stat1", label: "Stat 1", emoji: "📊", file: "data/stat1.json", archFile: "data/stat1_archetypes.json", weeks: 12 },
    { key: "english1", label: "English 1", emoji: "📖", file: "data/english1.json", archFile: "data/english1_archetypes.json", weeks: 12 },
    { key: "ct", label: "CT", emoji: "🧮", file: "data/ct.json", archFile: "data/ct_archetypes.json", weeks: 9 }
  ];

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
      s = JSON.parse(localStorage.getItem(STATE_KEY) || "{}");
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
    return { rows: rows, arch: arch, archByQid: archByQid };
  }

  function subjectStats(sub, data, state) {
    var done = state.doneQids[sub.key] || {};
    var totalQ = data.rows.length;
    var totalM = data.rows.reduce(function (a, r) { return a + r.m; }, 0);
    var doneQ = 0, doneM = 0;
    data.rows.forEach(function (r) {
      if (done[r.qid]) { doneQ++; doneM += r.m; }
    });
    return { totalQ: totalQ, totalM: totalM, doneQ: doneQ, doneM: doneM,
      pctQ: totalQ ? Math.round(100 * doneQ / totalQ) : 0,
      pctM: totalM ? Math.round(100 * doneM / totalM) : 0,
      remainingM: totalM - doneM };
  }

  // Planner: for each subject, find priority actions for "today"
  function buildTodaysPlan(allData, state) {
    var dl = daysLeft();
    var items = [];
    SUBJECTS.forEach(function (sub) {
      var data = allData[sub.key];
      if (!data || !data.rows.length) return;
      var stats = subjectStats(sub, data, state);
      if (stats.remainingM <= 0) return;
      var learned = state.archetypesLearned[sub.key] || {};
      // find first archetype (in week order) not yet learned
      var nextArch = null;
      for (var i = 0; i < data.arch.length; i++) {
        if (!learned[data.arch[i].id]) { nextArch = data.arch[i]; break; }
      }
      var dailyMarksTarget = dl > 0 ? Math.ceil(stats.remainingM / dl) : stats.remainingM;
      items.push({
        subject: sub, stats: stats, nextArch: nextArch, dailyMarksTarget: dailyMarksTarget
      });
    });
    // prioritize: subjects with an unlearned archetype first, then by remaining marks desc
    items.sort(function (a, b) {
      var aHas = a.nextArch ? 1 : 0, bHas = b.nextArch ? 1 : 0;
      if (aHas !== bHas) return bHas - aHas;
      return b.stats.remainingM - a.stats.remainingM;
    });
    return { daysLeft: dl, items: items };
  }

  function weekBadges(sub, data, state) {
    var done = state.doneQids[sub.key] || {};
    var learned = state.archetypesLearned[sub.key] || {};
    var byWeek = {};
    data.rows.forEach(function (r) {
      byWeek[r.w] = byWeek[r.w] || { total: 0, done: 0 };
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
    EXAM_DATE: EXAM_DATE, SUBJECTS: SUBJECTS,
    daysLeft: daysLeft, loadState: loadState, saveState: saveState,
    markDone: markDone, markLearned: markLearned,
    loadSubjectData: loadSubjectData, subjectStats: subjectStats,
    buildTodaysPlan: buildTodaysPlan, weekBadges: weekBadges, todayStr: todayStr
  };
})(window);
