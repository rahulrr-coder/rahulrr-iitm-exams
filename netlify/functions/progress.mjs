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

// one client per warm container, reused across invocations
let connecting;
function connect() {
  if (!connecting) connecting = new MongoClient(process.env.MONGODB_URI, { maxPoolSize: 1 }).connect();
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
    return Response.json({ error: "MONGODB_URI is not set" }, { status: 503 });
  }
  if (process.env.PROGRESS_KEY && req.headers.get("x-progress-key") !== process.env.PROGRESS_KEY) {
    return Response.json({ error: "bad key" }, { status: 401 });
  }

  const exam = new URL(req.url).searchParams.get("exam") || "End Term Sep 2026";
  const coll = (await connect()).db(DB).collection(COLLECTION);

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
