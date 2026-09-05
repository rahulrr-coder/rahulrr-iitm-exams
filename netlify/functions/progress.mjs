/* Progress sync.
 *
 * The site is static, and a browser cannot speak MongoDB's wire protocol — so this
 * function is the only thing that ever sees the connection string. It lives in the
 * MONGODB_URI environment variable on Netlify and is never shipped to the client
 * and never committed.
 *
 * Writes union rather than replace: ticks are only ever added, never removed. That
 * makes every write idempotent and order-independent, so two machines can sync in
 * any order without either clobbering the other's work — and a stale or hostile
 * POST cannot erase anything.
 */
import { MongoClient } from "mongodb";

const DB = "iitm_exams";
const COLLECTION = "progress";
const EMPTY = { doneQids: {}, archetypesLearned: {}, passes: {}, streak: { count: 0, lastDay: null } };

/* One client per warm container, reused across invocations.
   Fail fast: the driver's 30s default server-selection timeout outlives the
   function itself, so a blocked IP burned the whole budget and surfaced as an
   opaque 502 instead of saying what was wrong. And a rejected promise must not
   stay cached — otherwise one failed connect poisons every later invocation on
   that container until it recycles. */
let connecting;
function connect() {
  if (!connecting) {
    connecting = new MongoClient(process.env.MONGODB_URI, {
      maxPoolSize: 1,
      serverSelectionTimeoutMS: 5000,
      connectTimeoutMS: 5000
    }).connect().catch((err) => { connecting = null; throw err; });
  }
  return connecting;
}

function merge(base, incoming) {
  const out = {
    doneQids: { ...(base.doneQids || {}) },
    archetypesLearned: { ...(base.archetypesLearned || {}) },
    passes: { ...(base.passes || {}) },
    streak: base.streak || { count: 0, lastDay: null }
  };
  for (const field of ["doneQids", "archetypesLearned"]) {
    for (const [subject, ticks] of Object.entries(incoming[field] || {})) {
      out[field][subject] = { ...(out[field][subject] || {}) };
      for (const id of Object.keys(ticks || {})) if (ticks[id]) out[field][subject][id] = 1;
    }
  }
  for (const [id, on] of Object.entries(incoming.passes || {})) if (on) out.passes[id] = true;
  if ((incoming.streak?.count || 0) > (out.streak.count || 0)) out.streak = incoming.streak;
  return out;
}

export default async (req) => {
  if (!process.env.MONGODB_URI) {
    /* Names only, never values. Distinguishes "set under a different name" and
       "set but not scoped to Functions" from "never set at all", which otherwise
       look identical from out here. */
    const near = Object.keys(process.env).filter((k) => /mongo|progress|atlas|db/i.test(k));
    return Response.json({
      error: "MONGODB_URI is not visible to this function",
      similarVariablesThisFunctionCanSee: near,
      check: "Netlify → Site configuration → Environment variables: the variable must be scoped to Functions, set for the Production context, and followed by a redeploy."
    }, { status: 503 });
  }
  if (process.env.PROGRESS_KEY && req.headers.get("x-progress-key") !== process.env.PROGRESS_KEY) {
    return Response.json({ error: "bad key" }, { status: 401 });
  }

  const exam = new URL(req.url).searchParams.get("exam") || "End Term Sep 2026";

  let coll;
  try {
    coll = (await connect()).db(DB).collection(COLLECTION);
  } catch (err) {
    /* Atlas kills the TLS handshake for a non-allowlisted IP rather than refusing
       the connection, so it surfaces as "tlsv1 alert internal error" (SSL alert 80)
       and looks like a certificate problem. It isn't. */
    const msg = String(err && err.message);
    const blocked = /server selection|ETIMEDOUT|ECONNREFUSED|timed out|alert internal error|alert number 80|tlsv1/i.test(msg);
    return Response.json({
      error: "could not reach MongoDB",
      detail: msg.slice(0, 300),
      likelyCause: blocked
        ? "Atlas is refusing this connection. Netlify function IPs are dynamic, so Atlas → Network Access needs 0.0.0.0/0."
        : "Check the MONGODB_URI username and password."
    }, { status: 502 });
  }

  if (req.method === "GET") {
    const doc = await coll.findOne({ _id: exam });
    return Response.json(doc || { _id: exam, ...EMPTY });
  }

  if (req.method === "POST") {
    let incoming;
    try { incoming = await req.json(); }
    catch { return Response.json({ error: "body was not JSON" }, { status: 400 }); }
    if (!incoming || typeof incoming !== "object") {
      return Response.json({ error: "body was not a progress object" }, { status: 400 });
    }
    const base = (await coll.findOne({ _id: exam })) || EMPTY;
    const merged = merge(base, incoming);
    merged.updatedAt = new Date();
    await coll.updateOne({ _id: exam }, { $set: merged }, { upsert: true });
    return Response.json({ _id: exam, ...merged });
  }

  return Response.json({ error: "use GET or POST" }, { status: 405 });
};

export const config = { path: "/api/progress" };
