"use strict";
/* Two interchangeable stores: Firestore (production) and in-memory (tests / local preview). Paths look like "orders/CT-ABC123". */

function firestoreStore(admin) {
  const db = admin.firestore();
  const doc = (p) => db.doc(p);
  return {
    async get(p) { const s = await doc(p).get(); return s.exists ? s.data() : null; },
    async set(p, data) { await doc(p).set(data); },
    async update(p, patch) { await doc(p).update(patch); },
    async create(p, data) { await doc(p).create(data); },
    async delete(p) { await doc(p).delete(); },
    async add(col, data) { const r = await db.collection(col).add(data); return r.id; },
    /* atomic counter: returns the new value of field "field" in document p */
    async incr(p, field, by = 1) {
      return db.runTransaction(async (t) => { const r = doc(p); const s = await t.get(r); const v = ((s.exists && s.data()[field]) || 0) + by; t.set(r, { [field]: v }, { merge: true }); return v; });
    },
    async list(col, o = {}) {
      let q = db.collection(col);
      (o.where || []).forEach(([f, op, v]) => { q = q.where(f, op, v); });
      if (o.orderBy) q = q.orderBy(o.orderBy, o.dir || "asc");
      if (o.limit) q = q.limit(o.limit);
      const s = await q.get();
      return s.docs.map((d) => ({ id: d.id, ...d.data() }));
    },
  };
}

function memoryStore() {
  const m = new Map();
  const clone = (x) => JSON.parse(JSON.stringify(x));
  const split = (p) => { const i = p.lastIndexOf("/"); return [p.slice(0, i), p.slice(i + 1)]; };
  return {
    _dump: () => clone([...m.entries()]),
    async get(p) { return m.has(p) ? clone(m.get(p)) : null; },
    async set(p, data) { m.set(p, clone(data)); },
    async update(p, patch) { if (!m.has(p)) throw new Error("not-found"); m.set(p, { ...m.get(p), ...clone(patch) }); },
    async create(p, data) { if (m.has(p)) throw new Error("already-exists"); m.set(p, clone(data)); },
    async delete(p) { m.delete(p); },
    async add(col, data) { const id = "m" + Math.random().toString(36).slice(2, 12); m.set(col + "/" + id, clone(data)); return id; },
    async incr(p, field, by = 1) { const cur = m.has(p) ? m.get(p) : {}; const v = (cur[field] || 0) + by; m.set(p, { ...cur, [field]: v }); return v; },
    async list(col, o = {}) {
      let rows = [];
      for (const [p, v] of m) { const [c, id] = split(p); if (c === col) rows.push({ id, ...clone(v) }); }
      (o.where || []).forEach(([f, op, val]) => { if (op === "==") rows = rows.filter((r) => r[f] === val); });
      if (o.orderBy) rows.sort((a, b) => (a[o.orderBy] > b[o.orderBy] ? 1 : a[o.orderBy] < b[o.orderBy] ? -1 : 0) * (o.dir === "desc" ? -1 : 1));
      return o.limit ? rows.slice(0, o.limit) : rows;
    },
  };
}

module.exports = { firestoreStore, memoryStore };
