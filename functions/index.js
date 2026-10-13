"use strict";
const { onRequest } = require("firebase-functions/v2/https");
const admin = require("firebase-admin");
const { createApi } = require("./lib/api");
const { firestoreStore } = require("./lib/store");

admin.initializeApp();
const REGION = "europe-west1";

/* Only this data.gov.il resource may be proxied. Add more IDs here when you add more tables. */
const ALLOWED_RESOURCES = new Set(["a36db570-09f2-4521-8e3d-0290eb839c68", "9411b540-6791-40ce-93f7-4cb0068c264d"]);
const CKAN = "https://data.gov.il/api/3/action/datastore_search";

/* GET /api/govdata?resource_id=...&limit=...&offset=...&q=...  -> forwards to data.gov.il (server to server, no CORS issues) */
exports.govdata = onRequest({ region: REGION, cors: false, timeoutSeconds: 30, memory: "256MiB" }, async (req, res) => {
  if (req.method !== "GET") return res.status(405).json({ success: false, error: "method" });
  const resource = String(req.query.resource_id || "");
  if (!ALLOWED_RESOURCES.has(resource)) return res.status(400).json({ success: false, error: "resource" });
  const limit = Math.min(Math.max(parseInt(req.query.limit, 10) || 20, 1), 100);
  const offset = Math.max(parseInt(req.query.offset, 10) || 0, 0);
  const params = new URLSearchParams({ resource_id: resource, limit: String(limit), offset: String(offset) });
  const q = String(req.query.q || "").slice(0, 100).trim();
  if (q) params.set("q", q);
  try {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), 20000);
    const r = await fetch(CKAN + "?" + params.toString(), { signal: ctrl.signal, headers: { Accept: "application/json" } });
    clearTimeout(timer);
    if (!r.ok) return res.status(502).json({ success: false, error: "upstream " + r.status });
    const body = await r.json();
    res.set("Cache-Control", "public, max-age=300, s-maxage=600");
    return res.status(200).json(body);
  } catch (e) {
    return res.status(502).json({ success: false, error: "upstream" });
  }
});

/* POST /api/lead  -> stores a quote request in Firestore collection "leads" (clients cannot read or write Firestore directly) */
const cut = (v, n) => String(v == null ? "" : v).replace(/[\u0000-\u001f\u007f]/g, " ").trim().slice(0, n);
exports.lead = onRequest({ region: REGION, cors: false, timeoutSeconds: 15, memory: "256MiB" }, async (req, res) => {
  if (req.method !== "POST") return res.status(405).json({ ok: false });
  const origin = req.get("origin");
  if (origin) {
    let host = "";
    try { host = new URL(origin).host; } catch (e) { /* ignore */ }
    const own = (req.get("x-forwarded-host") || req.get("host") || "").split(",")[0].trim();
    if (host !== own && !/^localhost(:\d+)?$/.test(host)) return res.status(403).json({ ok: false });
  }
  const b = req.body && typeof req.body === "object" ? req.body : {};
  if (cut(b.website, 50)) return res.status(200).json({ ok: true });            /* honeypot: pretend success */
  const lead = {
    service: cut(b.service, 80), route: cut(b.route, 160), cargo: cut(b.cargo, 300),
    name: cut(b.name, 80), phone: cut(b.phone, 30), page: cut(b.page, 120),
  };
  if (!lead.name && !lead.phone && !lead.route && !lead.cargo) return res.status(400).json({ ok: false });
  try {
    await admin.firestore().collection("leads").add({ ...lead, status: "new", createdAt: admin.firestore.FieldValue.serverTimestamp() });
    return res.status(200).json({ ok: true });
  } catch (e) {
    return res.status(500).json({ ok: false });
  }
});

/* ---------- two servers, one database ----------
   api       : the CUSTOMER server. Serves /api/v1/** on the public site. Quotes, orders, accounts and the staff price code check.
               It answers nothing under /admin.
   adminapi  : the BACK-OFFICE server. Serves /api/v1/** on the separate back-office site. Orders management, employees, codes, settings.
               It answers only /admin routes.
   They never call each other over the internet. They talk through the shared database (Firestore, closed to browsers):
   an order saved by the customer server is read and managed by the back-office server, a status or tracking number set in the
   back office is what the customer server shows, and a personal staff code created in the back office is recognised by the
   customer server (only a keyed fingerprint is shared, never the code). */
const common = {
  store: firestoreStore(admin),
  verifyIdToken: async (t) => { const d = await admin.auth().verifyIdToken(t); return { uid: d.uid, email: d.email || "", emailVerified: d.email_verified === true, name: d.name || "" }; },
  createAuthUser: async ({ email, password, displayName }) => (await admin.auth().createUser({ email, password, displayName, emailVerified: true })).uid,
  createCustomToken: async (uid) => admin.auth().createCustomToken(uid),
  revokeRefreshTokens: async (uid) => admin.auth().revokeRefreshTokens(uid),
};
const handlePublic = createApi({ ...common, scope: "public" });
const handleAdmin = createApi({ ...common, scope: "admin" });
exports.api = onRequest({ region: REGION, cors: false, timeoutSeconds: 30, memory: "256MiB", maxInstances: 20 }, (req, res) => handlePublic(req, res));
exports.adminapi = onRequest({ region: REGION, cors: false, timeoutSeconds: 30, memory: "256MiB", maxInstances: 5 }, (req, res) => handleAdmin(req, res));
