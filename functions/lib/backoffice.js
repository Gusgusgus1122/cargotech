"use strict";
/* Back-office routes (ShippingToGo-style): lists, user pages, order dialog actions, ledger, receipts, treatments, agents, messages, outbox.
   Mounted only on the back-office server. Money entries can only be made by an admin. Nothing here ever touches a staff price code. */
const V = require("./validate");
const { TABLES: FEDEX_TABLES } = require("./fedexRates");

function makeBackoffice(ctx) {
  const { store, staffOf, audit, HttpError, bad, nowIso, round2, adminView, STATUSES, profitOf, settings, getOffers, priceOffer, chargeableKg } = ctx;
  const PAGE = 100;
  const SHIP_TYPES = ["cargo", "sea", "courier", "domestic"];
  const TASK_TYPES = ["pickup", "security", "release_origin", "release_destination", "address", "shipping_return"];
  const TASK_CATEGORIES = ["operation", "finance"];
  const iso = (v) => (!v ? "" : typeof v === "string" ? v : v.toDate ? v.toDate().toISOString() : v._seconds ? new Date(v._seconds * 1000).toISOString() : String(v));
  const day = (v) => iso(v).slice(0, 10);
  const lc = (v) => String(v == null ? "" : v).toLowerCase();
  const who = (st) => st.name || st.email || st.uid;
  const nameOf = (u) => [u && u.firstName, u && u.lastName].filter(Boolean).join(" ");
  const needAdmin = (st) => { if (st.role !== "admin") throw new HttpError(403, "admin-only"); };

  /* ---------- customer coupons: admin creates a time-boxed percentage-off code; a customer redeems it (once or by many
     customers, admin's choice) on the public site at signup. See lib/coupons.js for the shared status logic. */
  const { couponStatus } = require("./coupons");
  const today = () => nowIso().slice(0, 10);
  const genCouponCode = () => Math.random().toString(36).slice(2, 8).toUpperCase();
  async function activeCouponOf(uid) {
    const rows = await store.list("coupons", { where: [["uid", "==", uid]], limit: 50 });
    return rows.map((c) => ({ ...c, status: couponStatus(c, nowIso()) })).find((c) => c.status === "active") || null;
  }
  async function couponCreate(req, body) {
    const st = await staffOf(req, true);
    const pct = Number(body.pct);
    if (!Number.isFinite(pct) || pct <= 0 || pct > 100) throw bad("Invalid discount percentage.");
    const usageType = V.oneOf(body.usageType, ["once", "multi"], "once");
    const validFrom = /^\d{4}-\d{2}-\d{2}$/.test(body.validFrom || "") ? body.validFrom : today();
    const validTo = /^\d{4}-\d{2}-\d{2}$/.test(body.validTo || "") ? body.validTo : "";
    if (!validTo) throw bad("Set an end date for the coupon.");
    if (validTo < validFrom) throw bad("End date is before the start date.");
    let code = V.cut(body.code, 20).trim().toUpperCase() || genCouponCode();
    if ((await store.list("coupons", { where: [["code", "==", code]], limit: 1 })).length) throw bad("This code already exists - choose another.");
    const row = { code, uid: V.cut(body.uid, 80) || null, pct, usageType, usesCount: 0, validFrom, validTo, cancelled: false, note: V.cut(body.note, 300), by: who(st), createdAt: nowIso() };
    row.id = await store.add("coupons", row);
    await audit("coupon_create", st.uid, { id: row.id, code, pct });
    if (row.uid) await store.add("logs", { uid: row.uid, text: "Coupon created: " + pct + "% (" + usageType + "), " + validFrom + " to " + validTo + (row.note ? " - " + row.note : ""), by: who(st), at: nowIso(), type: "coupon" });
    return { ok: true, coupon: { ...row, status: couponStatus(row, nowIso()) } };
  }
  async function couponCancel(req, body) {
    const st = await staffOf(req, true);
    const id = V.cut(body.id, 80);
    const c = await store.get("coupons/" + id);
    if (!c) throw new HttpError(404, "coupon");
    await store.update("coupons/" + id, { cancelled: true });
    if (c.uid) await store.add("logs", { uid: c.uid, text: "Coupon cancelled (" + c.pct + "%, code " + c.code + ")", by: who(st), at: nowIso(), type: "coupon" });
    await audit("coupon_cancel", st.uid, { id, code: c.code });
    return { ok: true };
  }
  async function couponReactivate(req, body) {
    const st = await staffOf(req, true);
    const id = V.cut(body.id, 80);
    const c = await store.get("coupons/" + id);
    if (!c) throw new HttpError(404, "coupon");
    if (!c.cancelled) throw bad("This coupon isn't cancelled.");
    await store.update("coupons/" + id, { cancelled: false });
    if (c.uid) await store.add("logs", { uid: c.uid, text: "Coupon reactivated (" + c.pct + "%, code " + c.code + ")", by: who(st), at: nowIso(), type: "coupon" });
    await audit("coupon_reactivate", st.uid, { id, code: c.code });
    return { ok: true };
  }

  /* ---------- price lists: admin uploads a carrier's rate card (CSV, parsed client-side) so it's stored and
     visible only to admins. Wiring an uploaded list into an actual quote (zones, weight-break logic) is still
     a code change per carrier - this just stores and manages the raw table. The FedEx tables baked into
     lib/fedexRates.js (already wired into real quotes) show up here too, read-only, for visibility. */
  const PRICE_KEY_RE = /^[a-z0-9_-]{2,40}$/;
  const FEDEX_TABLE_LABELS = { priority: "Priority", economy: "Economy", priorityFreight: "Priority Freight", economyFreight: "Economy Freight" };
  function builtinPriceLists() {
    return Object.keys(FEDEX_TABLES).map((key) => {
      const rows = FEDEX_TABLES[key];
      const cols = new Set(); rows.forEach((r) => Object.keys(r).forEach((k) => { if (k !== "kg") cols.add(k); }));
      return { key: "fedex_" + key, label: FEDEX_TABLE_LABELS[key] || key, catalog: "fedex_shipping", builtin: true, rowCount: rows.length, colCount: cols.size, updatedAt: null, by: "" };
    });
  }
  async function pricelistList(req) {
    const st = await staffOf(req); needAdmin(st);
    const rows = await store.list("priceLists", { limit: 200 });
    const uploaded = rows.map((r) => ({ key: r.id, label: r.label, catalog: r.catalog || "", builtin: false, rowCount: (r.rows || []).length, colCount: (r.headers || []).length - 1, updatedAt: r.updatedAt, by: r.by }));
    return { ok: true, lists: builtinPriceLists().concat(uploaded) };
  }
  function builtinPriceList(key) {
    const tKey = Object.keys(FEDEX_TABLES).find((k) => "fedex_" + k === key);
    if (!tKey) return null;
    const rows = FEDEX_TABLES[tKey];
    const cols = []; rows.forEach((r) => Object.keys(r).forEach((k) => { if (k !== "kg" && !cols.includes(k)) cols.push(k); }));
    cols.sort();
    const headers = ["kg"].concat(cols);
    return { label: FEDEX_TABLE_LABELS[tKey] || tKey, catalog: "fedex_shipping", headers, rows: rows.map((r) => headers.map((h) => (h === "kg" ? r.kg : r[h] == null ? null : r[h]))), builtin: true };
  }
  async function pricelistGet(req) {
    const st = await staffOf(req); needAdmin(st);
    const key = V.cut(req.query.key, 40);
    const builtin = builtinPriceList(key);
    if (builtin) return { ok: true, pricelist: builtin };
    const r = await store.get("priceLists/" + key);
    if (!r) throw new HttpError(404, "pricelist");
    return { ok: true, pricelist: r };
  }
  async function pricelistSave(req, body) {
    const st = await staffOf(req); needAdmin(st);
    const key = lc(V.cut(body.key, 40));
    if (!PRICE_KEY_RE.test(key)) throw bad("Key must be 2-40 lowercase letters, numbers, - or _.");
    const label = V.cut(body.label, 80); if (!label) throw bad("Label is required.");
    const headers = Array.isArray(body.headers) ? body.headers.map((h) => V.cut(h, 40)).filter(Boolean) : [];
    if (headers.length < 2) throw bad("Needs at least two columns (e.g. kg + one zone).");
    if (headers.length > 60) throw bad("Too many columns (max 60).");
    const rows = Array.isArray(body.rows) ? body.rows : [];
    if (!rows.length) throw bad("The file has no data rows.");
    if (rows.length > 3000) throw bad("Too many rows (max 3000).");
    const cleanRows = rows.map((r) => {
      if (!Array.isArray(r) || r.length !== headers.length) throw bad("A row doesn't match the number of columns.");
      return r.map((v) => { if (v === "" || v == null) return null; const n = Number(v); return Number.isFinite(n) ? n : null; });
    });
    const catalog = V.cut(body.catalog, 40);
    const row = { label, catalog, headers, rows: cleanRows, by: who(st), updatedAt: nowIso() };
    await store.set("priceLists/" + key, row);
    await audit("pricelist_save", st.uid, { key, rows: cleanRows.length, cols: headers.length });
    return { ok: true, key };
  }
  async function pricelistDelete(req, body) {
    const st = await staffOf(req); needAdmin(st);
    const key = V.cut(body.key, 40);
    if (!(await store.get("priceLists/" + key))) throw new HttpError(404, "pricelist");
    await store.delete("priceLists/" + key);
    await audit("pricelist_delete", st.uid, { key });
    return { ok: true };
  }

  /* ---------- banners: marketing / contact banners the admin builds here; the public site (lib/api.js) reads
     and shows them. A "contact" CTA submits straight into the existing leads flow - no separate inbox. */
  const BANNER_TEMPLATES = ["center", "bottom", "side", "full"];
  const BANNER_ANIMS = ["fade-up", "scale", "slide-side"];
  const BANNER_CTA_TYPES = ["none", "link", "whatsapp", "phone", "contact"];
  const BANNER_PAGES = ["all", "home"];
  const BANNER_FREQ = ["always", "session", "once"];
  const dateOrEmpty = (v) => (/^\d{4}-\d{2}-\d{2}$/.test(String(v || "")) ? v : "");
  async function bannerList(req) {
    const st = await staffOf(req); needAdmin(st);
    const rows = await store.list("banners", { orderBy: "updatedAt", dir: "desc", limit: 200 });
    return { ok: true, banners: rows.map((p) => ({ ...p, id: p.id, shows: p.shows || 0, clicks: p.clicks || 0, dismisses: p.dismisses || 0 })) };
  }
  async function bannerSave(req, body) {
    const st = await staffOf(req); needAdmin(st);
    const title = V.cut(body.title, 100); if (!title) throw bad("Title is required.");
    const row = {
      title, body: V.cut(body.body, 500), imageUrl: V.cut(body.imageUrl, 400),
      ctaText: V.cut(body.ctaText, 40), ctaType: V.oneOf(body.ctaType, BANNER_CTA_TYPES, "none"),
      ctaValue: V.cut(body.ctaValue, 300), template: V.oneOf(body.template, BANNER_TEMPLATES, "center"),
      anim: V.oneOf(body.anim, BANNER_ANIMS, "fade-up"), page: V.oneOf(body.page, BANNER_PAGES, "all"),
      delaySec: V.num(body.delaySec, 0, 120, 0), frequency: V.oneOf(body.frequency, BANNER_FREQ, "always"),
      activeFrom: dateOrEmpty(body.activeFrom), activeTo: dateOrEmpty(body.activeTo), enabled: body.enabled !== false,
      by: who(st), updatedAt: nowIso(),
    };
    if (row.activeFrom && row.activeTo && row.activeTo < row.activeFrom) throw bad("End date is before the start date.");
    const id = V.cut(body.id, 40);
    if (id) {
      if (!(await store.get("banners/" + id))) throw new HttpError(404, "banner");
      await store.update("banners/" + id, row);
      await audit("banner_save", st.uid, { id });
      return { ok: true, id };
    }
    row.shows = 0; row.clicks = 0; row.dismisses = 0; row.createdAt = nowIso();
    const newId = await store.add("banners", row);
    await audit("banner_save", st.uid, { id: newId });
    return { ok: true, id: newId };
  }
  async function bannerDelete(req, body) {
    const st = await staffOf(req); needAdmin(st);
    const id = V.cut(body.id, 40);
    if (!(await store.get("banners/" + id))) throw new HttpError(404, "banner");
    await store.delete("banners/" + id);
    await audit("banner_delete", st.uid, { id });
    return { ok: true };
  }

  /* non-admin-safe: just enough to populate a "handled by" picker, including inactive/past staff */
  async function staffNames(req) {
    await staffOf(req);
    const rows = await store.list("staff", { limit: 200 });
    return { ok: true, staff: rows.map((r) => ({ uid: r.id, name: r.name || r.email, active: r.active !== false })) };
  }

  /* ---------- Agent Tasks, standalone (not nested under a specific order's action dispatcher) ----------
     A task needs at least one of a pickup (orderId) or a customer (uid) - not necessarily both, e.g. "this
     customer needs their balance recharged" has no specific shipment. If both are given they must agree. */
  async function taskCreate(req, body) {
    const st = await staffOf(req);
    const t = V.cut(body.text, 500); if (!t) throw bad("Describe the treatment.");
    if (!TASK_TYPES.includes(body.type)) throw bad("Invalid task type.");
    if (!TASK_CATEGORIES.includes(body.category)) throw bad("Invalid task category.");
    const orderId = V.cut(body.orderId, 20), uidIn = V.cut(body.uid, 80);
    if (!orderId && !uidIn) throw bad("Give at least a Pickup ID or a User ID.");
    let uid = uidIn || null;
    if (orderId) {
      const o = await store.get("orders/" + orderId);
      if (!o) throw new HttpError(404, "order");
      if (!o.uid) throw bad("This pickup has no registered customer (guest order) - a task needs a user_id. Ask the customer to register, or link the order to an account first.");
      if (uidIn && uidIn !== o.uid) throw bad("User ID does not match this Pickup ID's customer.");
      uid = o.uid;
    }
    if (!(await store.get("users/" + uid))) throw new HttpError(404, "user");
    let handledByUid = st.uid;
    if (body.handledByUid && body.handledByUid !== st.uid) { if (!(await store.get("staff/" + body.handledByUid))) throw bad("Unknown staff member."); handledByUid = body.handledByUid; }
    const row = { orderId: orderId || null, uid, type: body.type, category: body.category, text: t, awb: V.cut(body.awb, 60), status: "open", openedByUid: st.uid, handledByUid, by: who(st), createdAt: nowIso() };
    row.id = await store.add("treatments", row);
    await store.add("logs", { orderId: orderId || "", uid, treatmentId: row.id, text: "Task opened (" + body.type + "/" + body.category + "): " + t, by: who(st), at: nowIso(), type: body.type });
    await audit("task_create", st.uid, { id: row.id, uid, orderId });
    return { ok: true, task: row };
  }
  async function taskClose(req, body) {
    const st = await staffOf(req);
    const id = V.cut(body.treatmentId, 40);
    const tDoc = await store.get("treatments/" + id);
    if (!tDoc) throw new HttpError(404, "task");
    const patch = { status: "closed", closedAt: nowIso(), closedBy: who(st), result: V.cut(body.text, 300) };
    await store.update("treatments/" + id, patch);
    await store.add("logs", { uid: tDoc.uid, orderId: tDoc.orderId || "", treatmentId: id, text: "Task closed" + (patch.result ? ": " + patch.result : ""), by: who(st), at: nowIso(), type: "task" });
    return { ok: true };
  }
  async function taskReassign(req, body) {
    const st = await staffOf(req);
    const id = V.cut(body.treatmentId, 40);
    const tDoc = await store.get("treatments/" + id);
    if (!tDoc) throw new HttpError(404, "task");
    const target = V.cut(body.handledByUid, 128);
    const ts = await store.get("staff/" + target);
    if (!ts) throw bad("Unknown staff member.");
    await store.update("treatments/" + id, { handledByUid: target });
    await store.add("logs", { uid: tDoc.uid, orderId: tDoc.orderId || "", treatmentId: id, text: "Task reassigned to " + (ts.name || ts.email), by: who(st), at: nowIso(), type: "task" });
    return { ok: true };
  }
  /* an open task's running log: free-text updates over time (not just one closing result), plus the AWB
     field staff asked to be able to set/change whenever, same spirit as everything else here - append, don't overwrite. */
  async function taskUpdate(req, body) {
    const st = await staffOf(req);
    const id = V.cut(body.treatmentId, 40);
    const tDoc = await store.get("treatments/" + id);
    if (!tDoc) throw new HttpError(404, "task");
    const patch = {};
    if (body.awb != null) patch.awb = V.cut(body.awb, 60);
    if (body.desc != null) { const d = V.cut(body.desc, 500); if (!d) throw bad("Treatment description can't be empty."); patch.text = d; }
    if (Object.keys(patch).length) await store.update("treatments/" + id, patch);
    const note = V.cut(body.text, 500);
    if (note) await store.add("logs", { uid: tDoc.uid, orderId: tDoc.orderId || "", treatmentId: id, text: note, by: who(st), at: nowIso(), type: "task" });
    else if (!Object.keys(patch).length) throw bad("Nothing to update.");
    return { ok: true };
  }
  async function taskGet(req) {
    await staffOf(req);
    const id = V.cut(req.query.id, 40);
    const tDoc = await store.get("treatments/" + id);
    if (!tDoc) throw new HttpError(404, "task");
    const [u, logs, staff] = await Promise.all([
      tDoc.uid ? store.get("users/" + tDoc.uid) : null,
      store.list("logs", { where: [["treatmentId", "==", id]], limit: 500 }),
      store.list("staff", { limit: 200 }),
    ]);
    const staffName = (uid) => { const s = staff.find((x) => x.id === uid); return s ? s.name || s.email : ""; };
    return {
      ok: true,
      task: { ...tDoc, id, userNo: u ? u.userNo : null, userName: u ? nameOf(u) || u.email : "", handledByName: staffName(tDoc.handledByUid), openedByName: staffName(tDoc.openedByUid) },
      log: logs.sort((a, b) => (a.at < b.at ? 1 : -1)),
    };
  }

  /* ---------- users ---------- */
  async function ensureUserNo(uid, patch) {
    const u = (await store.get("users/" + uid)) || { uid, createdAt: nowIso() };
    if (!u.userNo) { u.userNo = await store.incr("_system/counters", "user"); await store.set("users/" + uid, { ...u, ...(patch || {}) }); } else if (patch) { await store.update("users/" + uid, patch); Object.assign(u, patch); }
    return u;
  }
  async function allUsers() {
    const rows = await store.list("users", { limit: 2000 });
    for (const u of rows) if (!u.userNo) { const f = await ensureUserNo(u.id || u.uid); u.userNo = f.userNo; }
    return rows.map((u) => ({ ...u, uid: u.uid || u.id }));
  }
  /* a coupon a customer has actually redeemed (uses_count >= 1) stays shown on their row even after the coupon
     itself turns "used"/"expired" for everyone else - that status describes whether it's still redeemable,
     not whether this particular customer benefited from it. Only a cancelled coupon drops off the row. */
  async function couponFlags() {
    const coupons = await store.list("coupons", { limit: 5000 });
    const byUid = {};
    coupons.forEach((c) => { if (c.uid && (c.usesCount || 0) >= 1 && !c.cancelled) byUid[c.uid] = { code: c.code, pct: c.pct, by: c.by }; });
    return byUid;
  }
  const ledgerOf = (order, rows) => rows.filter((l) => l.orderId === order.id);
  const sum = (rows, k) => round2(rows.reduce((a, l) => a + (Number(l[k]) || 0), 0));
  function payOf(o, ledger) {
    const lg = ledgerOf(o, ledger);
    const charged = sum(lg, "debit"), paid = sum(lg, "credit");
    const expected = charged || (o.quote && o.quote.total) || 0;
    const status = o.status === "cancelled" ? "cancelled" : paid <= 0 ? "unpaid" : paid + 0.005 >= expected ? "paid" : "partial";
    return { charged, paid, expected: round2(expected), due: round2(Math.max(0, expected - paid)), status };
  }
  const orderRow = (o, users, ledger, treat) => {
    const u = o.uid && users.find((x) => x.uid === o.uid);
    const p = payOf(o, ledger);
    return {
      id: o.id, status: o.status, createdAt: o.submittedAt || o.createdAt, updatedAt: o.updatedAt, userNo: u ? u.userNo : null, uid: o.uid || null, shipType: o.shipType || null,
      name: (o.contact && o.contact.name) || nameOf(u), email: (o.contact && o.contact.email) || (u && u.email) || "", phone: (o.contact && o.contact.phone) || "",
      from: o.from, to: o.to, fromCity: o.sender && o.sender.city, toCity: o.recipient && o.recipient.city, type: o.type, customerType: o.customerType,
      carrier: (o.quote && o.quote.carrier) || "", total: o.quote && o.quote.total != null ? o.quote.total : null, currency: (o.quote && o.quote.currency) || "ILS",
      tracking: (o.pickup && o.pickup.trackingNumber) || "", pickupDate: (o.pickup && o.pickup.date) || "", pay: p.status, paid: p.paid, due: p.due,
      treatment: treat ? treat.filter((t) => t.orderId === o.id && t.status === "open").length : 0, coupon: !!o.coupon,
    };
  };
  const inRange = (v, q) => (!q.from || day(v) >= q.from) && (!q.to || day(v) <= q.to);
  const cutQ = (r) => ({ q: lc(V.cut(r.query.q, 60)), status: V.cut(r.query.status, 20), from: /^\d{4}-\d{2}-\d{2}$/.test(r.query.from || "") ? r.query.from : "", to: /^\d{4}-\d{2}-\d{2}$/.test(r.query.to || "") ? r.query.to : "", uid: V.cut(r.query.uid, 80), page: Math.max(0, parseInt(r.query.page, 10) || 0), pay: V.cut(r.query.pay, 12), kind: V.cut(r.query.kind, 20), type: V.cut(r.query.type, 12), shipType: V.cut(r.query.shipType, 12), openedBy: V.cut(r.query.openedBy, 128) });
  const hay = (x) => lc(JSON.stringify(x));
  const pageOf = (rows, q) => ({ total: rows.length, page: q.page, pageSize: PAGE, rows: rows.slice(q.page * PAGE, q.page * PAGE + PAGE) });

  async function listModule(req) {
    const st = await staffOf(req);
    const m = V.cut(req.query.m, 20), q = cutQ(req);
    const out = { ok: true, m };
    const orders = async () => store.list("orders", { orderBy: "updatedAt", dir: "desc", limit: 1000 });
    if (m === "orders" || m === "quotes" || m === "payments") {
      const [os, users, ledger, treat] = await Promise.all([orders(), allUsers(), store.list("ledger", { limit: 5000 }), store.list("treatments", { limit: 2000 })]);
      let rows = os.filter((o) => o.status !== "draft" || m === "quotes").map((o) => orderRow(o, users, ledger, treat));
      if (m === "quotes") rows = rows.filter((r) => ["draft", "new", "quote_sent"].includes(r.status));
      if (m === "payments") rows = rows.filter((r) => !["draft", "cancelled"].includes(r.status));
      if (q.status) rows = rows.filter((r) => r.status === q.status);
      if (q.pay) rows = rows.filter((r) => r.pay === q.pay);
      if (q.uid) rows = rows.filter((r) => r.uid === q.uid);
      if (q.type) rows = rows.filter((r) => r.customerType === q.type);
      if (q.shipType) rows = rows.filter((r) => r.shipType === q.shipType);
      rows = rows.filter((r) => inRange(r.createdAt, q) && (!q.q || hay([r.id, r.name, r.email, r.phone, r.tracking, r.userNo, r.fromCity, r.toCity]).includes(q.q)));
      if (st.role !== "admin") rows = rows.map((r) => ({ ...r }));
      const totals = { count: rows.length, total: round2(rows.reduce((a, r) => a + (r.total || 0), 0)), paid: round2(rows.reduce((a, r) => a + r.paid, 0)), due: round2(rows.reduce((a, r) => a + r.due, 0)) };
      return { ...out, ...pageOf(rows, q), totals };
    }
    if (m === "users") {
      const [users, os, ledger, coupons] = await Promise.all([allUsers(), orders(), store.list("ledger", { limit: 5000 }), couponFlags()]);
      let rows = users.map((u) => {
        const mine = os.filter((o) => o.uid === u.uid && o.status !== "draft"); const lg = ledger.filter((l) => l.uid === u.uid);
        return { uid: u.uid, userNo: u.userNo, name: nameOf(u), email: u.email || "", phone: u.phone || "", type: u.useFor || "", createdAt: u.createdAt || "", orders: mine.length, balance: round2(sum(lg, "debit") - sum(lg, "credit")), blocked: !!u.blocked, coupon: coupons[u.uid] || null };
      });
      rows = rows.filter((r) => inRange(r.createdAt, q) && (!q.q || hay([r.userNo, r.name, r.email, r.phone]).includes(q.q))).sort((a, b) => b.userNo - a.userNo);
      return { ...out, ...pageOf(rows, q) };
    }
    if (m === "ledger") {
      const [lg, users] = await Promise.all([store.list("ledger", { orderBy: "at", dir: "desc", limit: 3000 }), allUsers()]);
      let rows = lg.map((l) => { const u = users.find((x) => x.uid === l.uid); return { ...l, userNo: u ? u.userNo : null, userName: nameOf(u) || (u && u.email) || "" }; });
      if (q.uid) rows = rows.filter((r) => r.uid === q.uid);
      if (q.kind) rows = rows.filter((r) => r.kind === q.kind);
      rows = rows.filter((r) => inRange(r.at, q) && (!q.q || hay([r.orderId, r.userNo, r.userName, r.note, r.method]).includes(q.q)));
      return { ...out, ...pageOf(rows, q), totals: { debit: sum(rows, "debit"), credit: sum(rows, "credit") } };
    }
    if (m === "receipts") {
      const [rc, users] = await Promise.all([store.list("receipts", { orderBy: "at", dir: "desc", limit: 3000 }), allUsers()]);
      let rows = rc.map((r) => { const u = users.find((x) => x.uid === r.uid); return { ...r, userNo: u ? u.userNo : null, userName: nameOf(u) || (u && u.email) || r.name || "" }; });
      if (q.uid) rows = rows.filter((r) => r.uid === q.uid);
      rows = rows.filter((r) => inRange(r.at, q) && (!q.q || hay([r.no, r.orderId, r.userNo, r.userName]).includes(q.q)));
      return { ...out, ...pageOf(rows, q), totals: { amount: sum(rows, "amount") } };
    }
    if (m === "treatments") {
      const [tr, users, os, staff] = await Promise.all([store.list("treatments", { orderBy: "createdAt", dir: "desc", limit: 2000 }), allUsers(), orders(), store.list("staff", { limit: 200 })]);
      const staffName = (uid) => { const s = staff.find((x) => x.id === uid); return s ? s.name || s.email : ""; };
      let rows = tr.map((t) => { const o = t.orderId && os.find((x) => x.id === t.orderId); const u = users.find((x) => x.uid === t.uid); return { ...t, userNo: u ? u.userNo : null, name: (o && o.contact && o.contact.name) || nameOf(u) || (u && u.email) || "", orderStatus: o ? o.status : "", handledByName: staffName(t.handledByUid), openedByName: staffName(t.openedByUid) }; });
      if (q.status) rows = rows.filter((r) => r.status === q.status);
      if (q.type) rows = rows.filter((r) => r.type === q.type);
      if (q.openedBy) rows = rows.filter((r) => r.openedByUid === q.openedBy);
      rows = rows.filter((r) => inRange(r.createdAt, q) && (!q.q || hay([r.orderId, r.text, r.handledByName, r.openedByName, r.name]).includes(q.q)));
      return { ...out, ...pageOf(rows, q) };
    }
    if (m === "messages") {
      const ms = (await store.list("leads", { limit: 2000 })).map((l) => ({ ...l, createdAt: iso(l.createdAt), status: l.status || "new" }));
      let rows = ms.sort((a, b) => (a.createdAt < b.createdAt ? 1 : -1));
      if (q.status) rows = rows.filter((r) => r.status === q.status);
      rows = rows.filter((r) => inRange(r.createdAt, q) && (!q.q || hay([r.name, r.phone, r.route, r.cargo, r.service]).includes(q.q)));
      return { ...out, ...pageOf(rows, q) };
    }
    if (m === "agents") {
      const rows = (await store.list("agents", { limit: 500 })).sort((a, b) => lc(a.name).localeCompare(lc(b.name))).filter((a) => !q.q || hay(a).includes(q.q));
      return { ...out, ...pageOf(rows, q) };
    }
    if (m === "outbox") {
      let rows = await store.list("outbox", { orderBy: "at", dir: "desc", limit: 1000 });
      rows = rows.filter((r) => !q.q || hay([r.to, r.subject, r.orderId]).includes(q.q));
      return { ...out, ...pageOf(rows, q) };
    }
    if (m === "coupons") {
      const [coupons, users] = await Promise.all([store.list("coupons", { orderBy: "createdAt", dir: "desc", limit: 1000 }), allUsers()]);
      let rows = coupons.map((c) => { const u = c.uid && users.find((x) => x.uid === c.uid); return { ...c, status: couponStatus(c, nowIso()), userNo: u ? u.userNo : null, userName: u ? nameOf(u) || u.email : "" }; });
      rows = rows.filter((r) => !q.q || hay([r.code, r.userNo, r.userName, r.note]).includes(q.q));
      return { ...out, ...pageOf(rows, q) };
    }
    throw bad("unknown module");
  }

  async function counts(req) {
    await staffOf(req);
    const [os, tr, ms] = await Promise.all([store.list("orders", { limit: 1000 }), store.list("treatments", { limit: 2000 }), store.list("leads", { limit: 2000 })]);
    return { ok: true, newOrders: os.filter((o) => o.status === "new").length, openTreatments: tr.filter((t) => t.status === "open").length, newMessages: ms.filter((l) => (l.status || "new") === "new").length };
  }

  /* finance panel: revenue (cash received), refunds (cash paid back) and profit/loss, bucketed by day or month.
     Admin-only - this is the same cost/profit data adminView already restricts to admins. */
  async function finance(req) {
    await staffOf(req, true);
    const group = V.oneOf(req.query.group, ["day", "month"], "day");
    const q = { from: /^\d{4}-\d{2}-\d{2}$/.test(req.query.from || "") ? req.query.from : "", to: /^\d{4}-\d{2}-\d{2}$/.test(req.query.to || "") ? req.query.to : "" };
    const bucket = (v) => (group === "month" ? day(v).slice(0, 7) : day(v));
    const [ledger, orders] = await Promise.all([store.list("ledger", { limit: 5000 }), store.list("orders", { limit: 1000 })]);
    const rows = {};
    const row = (k) => (rows[k] = rows[k] || { date: k, revenue: 0, refunds: 0, profit: 0 });
    ledger.filter((l) => inRange(l.at, q)).forEach((l) => {
      const k = bucket(l.at);
      if (l.kind === "refund") row(k).refunds = round2(row(k).refunds + (l.debit || 0));
      else if (l.credit) row(k).revenue = round2(row(k).revenue + l.credit);
    });
    orders.filter((o) => !["draft", "cancelled"].includes(o.status) && inRange(o.submittedAt || o.createdAt, q)).forEach((o) => {
      const p = profitOf(o.quote || {});
      if (p == null) return;
      const k = bucket(o.submittedAt || o.createdAt);
      row(k).profit = round2(row(k).profit + p);
    });
    const list = Object.keys(rows).map((k) => rows[k]).sort((a, b) => (a.date < b.date ? -1 : 1));
    const totals = { revenue: round2(list.reduce((a, r) => a + r.revenue, 0)), refunds: round2(list.reduce((a, r) => a + r.refunds, 0)), profit: round2(list.reduce((a, r) => a + r.profit, 0)) };
    return { ok: true, rows: list, totals };
  }

  /* quick search of the sidebar: user id, e-mail, pickup id, shipping authorization (tracking number) */
  async function search(req) {
    await staffOf(req);
    const q = V.cut(req.query.q, 80).trim(), by = V.cut(req.query.by, 30);
    if (!q) throw bad("missing");
    const users = await allUsers();
    if (by === "userId") { const u = users.find((x) => String(x.userNo) === q); return { ok: true, found: !!u, kind: "user", id: u && u.uid }; }
    if (by === "email") { const u = users.find((x) => lc(x.email) === lc(q)); if (u) return { ok: true, found: true, kind: "user", id: u.uid }; const o = (await store.list("orders", { limit: 1000 })).find((x) => lc(x.contact && x.contact.email) === lc(q)); return { ok: true, found: !!o, kind: "order", id: o && o.id }; }
    if (by === "pickupId") { const o = await store.get("orders/" + q.toUpperCase()); return { ok: true, found: !!o, kind: "order", id: o && o.id }; }
    if (by === "shippingAuthorization") { const o = (await store.list("orders", { limit: 1000 })).find((x) => x.pickup && x.pickup.trackingNumber && lc(x.pickup.trackingNumber) === lc(q)); return { ok: true, found: !!o, kind: "order", id: o && o.id }; }
    throw bad("unknown search");
  }

  /* ---------- one user ---------- */
  async function getUser(req) {
    const st = await staffOf(req);
    const uid = V.cut(req.query.uid, 80);
    const u0 = await store.get("users/" + uid);
    if (!u0) throw new HttpError(404, "user");
    const u = await ensureUserNo(uid);
    const [os, ledger, receipts, treat, logs, coupon] = await Promise.all([store.list("orders", { where: [["uid", "==", uid]], limit: 500 }), store.list("ledger", { where: [["uid", "==", uid]], limit: 2000 }), store.list("receipts", { where: [["uid", "==", uid]], limit: 1000 }), store.list("treatments", { limit: 2000 }), store.list("logs", { where: [["uid", "==", uid]], limit: 500 }), activeCouponOf(uid)]);
    os.sort((a, b) => (a.updatedAt < b.updatedAt ? 1 : -1));
    const users = [u];
    const rows = os.map((o) => orderRow(o, users, ledger, treat));
    const docs = []; os.forEach((o) => (o.docs || []).forEach((d) => docs.push({ ...d, orderId: o.id })));
    return {
      ok: true, role: st.role,
      user: { uid, userNo: u.userNo, firstName: u.firstName || "", lastName: u.lastName || "", email: u.email || "", phone: u.phone || "", useFor: u.useFor || "", userType: u.userType || "", marketing: !!u.marketing, description: u.description || "", blocked: !!u.blocked, isActive: u.isActive || "yes", discountPct: u.discountPct == null ? "" : u.discountPct, debtAmountLimit: u.debtAmountLimit == null ? "" : u.debtAmountLimit, createdAt: u.createdAt || "",
        ...Object.keys(USER_TEXT_FIELDS).reduce((o, k) => ((o[k] = u[k] || ""), o), {}) },
      balance: round2(sum(ledger, "debit") - sum(ledger, "credit")), charged: sum(ledger, "debit"), paid: sum(ledger, "credit"),
      orders: rows.filter((r) => r.status !== "draft"), quotes: rows.filter((r) => ["draft", "new", "quote_sent"].includes(r.status)), payments: rows.filter((r) => !["draft", "cancelled"].includes(r.status)),
      ledger: ledger.sort((a, b) => (a.at < b.at ? 1 : -1)), receipts: receipts.sort((a, b) => (a.at < b.at ? 1 : -1)), documents: docs,
      log: logs.sort((a, b) => (a.at < b.at ? 1 : -1)), coupon,
    };
  }
  /* extra profile fields modelled on the ShippingToGo reference screen; CargoTech doesn't act on most of these yet
     (no agent commissions, affiliates, per-carrier preference, power of attorney, debt limits or accounting-email routing
     exist anywhere else in the code) - they're stored as plain text/numbers for now, nothing downstream reads them. */
  const USER_TEXT_FIELDS = { company: 80, country: 60, city: 60, address: 120, zip: 20, commission: 40, permission: 60, brand: 60, couriers: 60, powerOfAttorney: 60, defaultLang: 20, accountingEmail: 120, sdrAgent: 60, userReturnTime: 20, affiliateId: 40, handleByAgent: 60, socialMediaShare: 60 };
  const USER_FIELD_LABELS = { firstName: "First name", lastName: "Last name", phone: "Phone", useFor: "Account type", userType: "UserType", isActive: "IsActive", discountPct: "Discount", debtAmountLimit: "DebtAmountLimit", blocked: "Blocked", marketing: "Marketing opt-in", company: "Company", country: "Country", city: "City", address: "Address", zip: "Zip", commission: "Commission", permission: "Permission", brand: "Brand", couriers: "Couriers", powerOfAttorney: "PowerOfAttorney", defaultLang: "DefaultLang", accountingEmail: "AccountingEmail", sdrAgent: "SdrAgent", userReturnTime: "UserReturnTime", affiliateId: "AffiliateId", handleByAgent: "HandleByAgent", socialMediaShare: "SocialMediaShare" };
  async function updateUser(req, body) {
    const st = await staffOf(req);
    const uid = V.cut(body.uid, 80);
    const u0 = await store.get("users/" + uid);
    if (!u0) throw new HttpError(404, "user");
    /* validate into "raw" first, then only keep fields that actually differ from what's stored today -
       the UpdateDetails form always submits every field, but the log should say what really changed, not just what was sent. */
    const raw = {};
    ["firstName", "lastName"].forEach((k) => { if (body[k] != null) raw[k] = V.cut(body[k], 40); });
    if (body.phone != null) raw.phone = V.cut(body.phone, 30);
    if (body.useFor != null) raw.useFor = V.oneOf(body.useFor, ["private", "business"], "private");
    if (body.userType != null) raw.userType = V.cut(body.userType, 40);
    if (body.description != null) raw.description = V.cut(body.description, 1000);
    if (body.marketing != null) raw.marketing = body.marketing === true;
    if (body.isActive != null) raw.isActive = V.oneOf(body.isActive, ["yes", "no"], "yes");
    if (body.discountPct != null) { const n = Number(body.discountPct); if (!Number.isFinite(n) || n < 0 || n > 100) throw bad("Invalid discount."); raw.discountPct = n; }
    if (body.debtAmountLimit != null) { const n = Number(body.debtAmountLimit); if (!Number.isFinite(n) || n < 0) throw bad("Invalid debt limit."); raw.debtAmountLimit = n; }
    Object.keys(USER_TEXT_FIELDS).forEach((k) => { if (body[k] != null) raw[k] = V.cut(body[k], USER_TEXT_FIELDS[k]); });
    if (body.blocked != null) { needAdmin(st); raw.blocked = body.blocked === true; }

    const norm = (v) => (v == null ? "" : v);
    const patch = {};
    Object.keys(raw).forEach((k) => { if (norm(raw[k]) !== norm(u0[k])) patch[k] = raw[k]; });
    if (!Object.keys(patch).length) return getUser({ ...req, query: { uid } });
    patch.updatedAt = nowIso();
    await store.update("users/" + uid, patch);
    const changes = Object.keys(patch).filter((k) => k !== "updatedAt").map((k) => {
      if (k === "description") return "Description updated";
      const label = USER_FIELD_LABELS[k] || k;
      const before = norm(u0[k]) === "" ? "-" : String(u0[k]);
      const after = norm(patch[k]) === "" ? "-" : String(patch[k]);
      return label + ": " + before + " → " + after;
    });
    await store.add("logs", { uid, text: "User details updated: " + changes.join("; "), by: who(st), at: nowIso(), type: "user" });
    await audit("user_update", st.uid, { uid, fields: Object.keys(patch) });
    return getUser({ ...req, query: { uid } });
  }
  /* a manual note on the customer's own log, not tied to any order or ledger entry - the "Add" link under Log */
  async function logAdd(req, body) {
    const st = await staffOf(req);
    const uid = V.cut(body.uid, 80);
    if (!(await store.get("users/" + uid))) throw new HttpError(404, "user");
    const text = V.cut(body.text, 500);
    if (!text) throw bad("Write something to log.");
    await store.add("logs", { uid, text, by: who(st), at: nowIso(), type: "note" });
    return getUser({ ...req, query: { uid } });
  }

  /* ---------- one order (the ShipDetails dialog) ---------- */
  async function loadFull(id, st) {
    const o = await store.get("orders/" + V.cut(id, 20));
    if (!o) throw new HttpError(404, "order");
    const [ledger, receipts, treat, logs, outbox, users] = await Promise.all([
      store.list("ledger", { where: [["orderId", "==", o.id]], limit: 500 }), store.list("receipts", { where: [["orderId", "==", o.id]], limit: 200 }),
      store.list("treatments", { where: [["orderId", "==", o.id]], limit: 200 }), store.list("logs", { where: [["orderId", "==", o.id]], limit: 500 }),
      store.list("outbox", { where: [["orderId", "==", o.id]], limit: 100 }), o.uid ? store.get("users/" + o.uid) : null,
    ]);
    const view = adminView(o, st);
    return {
      ok: true, role: st.role, order: { ...view, label: o.label || null, invoice: o.invoice || null, docs: o.docs || [], returned: !!o.returned, completedAt: o.completedAt || "", actualKg: o.actualKg == null ? null : o.actualKg,
        commissionPctOverride: o.commissionPctOverride == null ? null : o.commissionPctOverride, discountPct: o.discountPct || 0 },
      user: users ? { uid: o.uid, userNo: users.userNo || null, name: nameOf(users), email: users.email || "", phone: users.phone || "" } : null,
      pay: payOf(o, ledger), ledger: ledger.sort((a, b) => (a.at < b.at ? 1 : -1)), receipts: receipts.sort((a, b) => (a.at < b.at ? 1 : -1)),
      treatments: treat.sort((a, b) => (a.createdAt < b.createdAt ? 1 : -1)), log: logs.sort((a, b) => (a.at < b.at ? 1 : -1)), outbox: outbox.sort((a, b) => (a.at < b.at ? 1 : -1)),
    };
  }
  const getOrder = async (req) => loadFull(req.query.id, await staffOf(req));

  const money = (v) => { const n = Number(v); if (!Number.isFinite(n) || n <= 0 || n > 1000000) throw bad("Invalid amount."); return round2(n); };
  const METHODS = ["credit_card", "bank_transfer", "cash", "system", "check", "other"];
  async function addLedger(st, o, e) {
    const row = { orderId: o ? o.id : "", uid: (o && o.uid) || e.uid || "", kind: e.kind, debit: e.debit || 0, credit: e.credit || 0, method: e.method || "", note: V.cut(e.note, 300), by: who(st), at: nowIso(), currency: (o && o.quote && o.quote.currency) || "ILS" };
    row.id = await store.add("ledger", row);
    return row;
  }
  async function addReceipt(st, o, amount, method, note, uid) {
    const no = await store.incr("_system/counters", "receipt");
    const r = { no, orderId: o ? o.id : "", uid: (o && o.uid) || uid || "", amount, method, note: V.cut(note, 200), name: (o && o.contact && o.contact.name) || "", by: who(st), at: nowIso(), currency: (o && o.quote && o.quote.currency) || "ILS" };
    r.id = await store.add("receipts", r);
    return r;
  }
  async function queueMail(st, o, to, subject, text, kind) {
    to = V.cut(to, 120);
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(to)) throw bad("A valid e-mail address is required.");
    await store.add("outbox", { to, subject: V.cut(subject, 160), body: V.cut(text, 4000), kind, orderId: o ? o.id : "", by: who(st), at: nowIso(), status: "queued" });
  }
  const summaryText = (o, pay) => [
    "Shipment " + o.id, "From: " + (o.sender && o.sender.city) + ", " + String(o.from).toUpperCase() + "  To: " + (o.recipient && o.recipient.city) + ", " + String(o.to).toUpperCase(),
    "Status: " + o.status, "Pickup: " + ((o.pickup && o.pickup.date) || "-") + " " + ((o.pickup && o.pickup.time) || ""), "Tracking: " + ((o.pickup && o.pickup.trackingNumber) || "-"),
    "Price: " + (o.quote && o.quote.total != null ? o.quote.total + " " + (o.quote.currency || "ILS") : "-"), "Paid: " + pay.paid + "  Due: " + pay.due,
  ].join("\n");

  /* Re-price an order from the carrier's own rate card (same carrier/service already selected), at a new
     billable weight and/or a per-shipment commission or discount override. Never below the original
     dimensional weight, since that's what the carrier would charge regardless of what was declared.
     Best-effort: an order with no automatic offer behind it (e.g. a hand-typed manual price) just keeps
     its price as-is - staff edit that directly instead. */
  async function recomputeQuote(o, { actualKg, commissionPctOverride, discountPct }) {
    if (!o.quote || !o.quote.offerId) return null;
    const s = await settings();
    const vol = chargeableKg(o.parcels).vol;
    const billable = actualKg != null ? Math.max(actualKg, vol) : null;
    const weightParcels = billable != null ? [{ qty: 1, kg: billable, l: 0, w: 0, h: 0 }] : o.parcels;
    const raw = await getOffers({ mode: "intl", from: o.from, to: o.to, type: o.type, parcels: weightParcels, zips: {}, cities: {}, entered: {} }, s);
    const match = raw.find((r) => r.id === o.quote.offerId);
    if (!match) return null;
    const priced = priceOffer(match, { customerType: o.customerType, signature: o.signature, settings: s, pctOverride: commissionPctOverride });
    const total = round2(priced.total * (1 - (discountPct || 0) / 100));
    return {
      ...o.quote, carrier: match.carrier, service: match.service, days: match.days, manual: false,
      lines: priced.lines, computedTotal: priced.total, total, cost: priced.cost, markupPct: priced.markupPct, overridden: false,
    };
  }

  async function orderAction(req, body) {
    const st = await staffOf(req);
    const id = V.cut(body.id, 20), act = V.cut(body.action, 30);
    const o = await store.get("orders/" + id);
    if (!o) throw new HttpError(404, "order");
    const log = (text) => store.add("logs", { orderId: id, uid: o.uid || "", text: V.cut(text, 400), by: who(st), at: nowIso(), type: act });
    const patch = {};
    const ledger = () => store.list("ledger", { where: [["orderId", "==", id]], limit: 500 });
    let extra = {};
    switch (act) {
      case "comment": { const t = V.cut(body.text, 500); if (!t) throw bad("Write a comment."); await log(t); break; }
      case "treatment_add": {
        const t = V.cut(body.text, 500); if (!t) throw bad("Describe the treatment.");
        if (!TASK_TYPES.includes(body.type)) throw bad("Invalid task type.");
        if (!TASK_CATEGORIES.includes(body.category)) throw bad("Invalid task category.");
        if (!o.uid) throw bad("This pickup has no registered customer (guest order) - a task needs a user_id. Ask the customer to register, or link the order to an account first.");
        if (body.userNo != null && String(body.userNo).trim() !== "") {
          const cu = await store.get("users/" + o.uid);
          if (!cu || String(cu.userNo) !== String(body.userNo).trim()) throw bad("User ID does not match this Pickup ID's customer.");
        }
        let handledByUid = st.uid;
        if (body.handledByUid && body.handledByUid !== st.uid) { if (!(await store.get("staff/" + body.handledByUid))) throw bad("Unknown staff member."); handledByUid = body.handledByUid; }
        await store.add("treatments", { orderId: id, uid: o.uid, type: body.type, category: body.category, text: t, status: "open", openedByUid: st.uid, handledByUid, by: who(st), createdAt: nowIso() });
        await log("Task opened (" + body.type + "/" + body.category + "): " + t);
        break;
      }
      case "treatment_close": { const tid = V.cut(body.treatmentId, 40); const t = await store.get("treatments/" + tid); if (!t || t.orderId !== id) throw new HttpError(404, "treatment"); await store.update("treatments/" + tid, { status: "closed", closedAt: nowIso(), closedBy: who(st), result: V.cut(body.text, 300) }); await log("Treatment closed" + (body.text ? ": " + V.cut(body.text, 200) : "")); break; }
      case "treatment_reassign": { const tid = V.cut(body.treatmentId, 40); const t = await store.get("treatments/" + tid); if (!t || t.orderId !== id) throw new HttpError(404, "treatment"); const target = V.cut(body.handledByUid, 128); const ts = await store.get("staff/" + target); if (!ts) throw bad("Unknown staff member."); await store.update("treatments/" + tid, { handledByUid: target }); await log("Task reassigned to " + (ts.name || ts.email)); break; }
      case "status": { if (!STATUSES.includes(body.status)) throw bad("Invalid status."); patch.status = body.status; if (body.status === "delivered") patch.completedAt = nowIso(); await log("Status → " + body.status); break; }
      case "ship_type": { if (!SHIP_TYPES.includes(body.shipType)) throw bad("Invalid shipment type."); patch.shipType = body.shipType; await log("Shipment type → " + body.shipType); break; }
      case "pickup_time": { const d = String(body.date || ""); if (!/^\d{4}-\d{2}-\d{2}$/.test(d)) throw bad("Invalid date."); patch.pickup = { ...(o.pickup || {}), date: d, time: V.cut(body.time, 20) }; await log("Pickup time changed to " + d + " " + V.cut(body.time, 20)); break; }
      case "pickup_details": { const p = o.pickup || {}; patch.pickup = { ...p, confirmation: V.cut(body.confirmation != null ? body.confirmation : p.confirmation, 60), callNumber: V.cut(body.callNumber != null ? body.callNumber : p.callNumber, 60), trackingNumber: V.cut(body.trackingNumber != null ? body.trackingNumber : p.trackingNumber, 60) }; await log("Pickup details updated"); break; }
      case "manage_pickup": { const p = o.pickup || {}; patch.pickup = { ...p, confirmation: V.cut(body.confirmation, 60), callNumber: V.cut(body.callNumber, 60), pickupStatus: V.oneOf(body.pickupStatus, ["scheduled", "confirmed", "missed", "done", "cancelled"], "scheduled") }; await log("Pickup managed: " + patch.pickup.pickupStatus); break; }
      case "user_details": { const s = V.addr(body.sender || o.sender), r = V.addr(body.recipient || o.recipient); patch.sender = s; patch.recipient = r; patch.contact = { name: s.name, email: s.email, phone: s.phone }; await log("Sender / recipient details updated"); break; }
      case "label": case "change_label": { patch.label = { url: V.cut(body.url, 400), note: V.cut(body.note, 200), carrier: V.cut(body.carrier, 60) || (o.quote && o.quote.carrier) || "", updatedAt: nowIso(), by: who(st) }; if (body.trackingNumber) patch.pickup = { ...(o.pickup || {}), trackingNumber: V.cut(body.trackingNumber, 60) }; await log(act === "label" ? "Label saved" : "Label changed"); break; }
      case "invoice": { if (o.invoice) { extra.invoice = o.invoice; break; } const p = payOf(o, await ledger()); const no = await store.incr("_system/counters", "invoice"); patch.invoice = { no, at: nowIso(), amount: p.expected, currency: (o.quote && o.quote.currency) || "ILS" }; await log("Invoice " + no + " created"); break; }
      case "return": { patch.returned = true; patch.status = "cancelled"; await log("Shipment marked as returned" + (body.text ? ": " + V.cut(body.text, 200) : "")); break; }
      case "cancel": { patch.status = "cancelled"; await log("Order cancelled"); break; }
      case "actual_weight": {
        patch.actualKg = V.num(body.kg, 0, 5000, 0);
        const requote = await recomputeQuote(o, { actualKg: patch.actualKg, commissionPctOverride: o.commissionPctOverride, discountPct: o.discountPct });
        if (requote) { patch.quote = requote; await log("Actual weight: " + patch.actualKg + " kg - price recalculated to " + requote.total + " " + requote.currency); }
        else await log("Actual weight: " + patch.actualKg + " kg");
        break;
      }
      case "pricing_override": {
        needAdmin(st);
        const commissionPctOverride = body.commissionPctOverride === "" || body.commissionPctOverride == null ? null : V.num(body.commissionPctOverride, 0, 1000, null);
        const discountPct = V.num(body.discountPct, 0, 100, 0);
        patch.commissionPctOverride = commissionPctOverride;
        patch.discountPct = discountPct;
        const requote = await recomputeQuote(o, { actualKg: o.actualKg, commissionPctOverride, discountPct });
        if (requote) patch.quote = requote;
        await log("Pricing override: commission " + (commissionPctOverride == null ? "default" : commissionPctOverride + "%") + ", discount " + discountPct + "%" + (requote ? " - price recalculated to " + requote.total + " " + requote.currency : ""));
        break;
      }
      case "doc_add": { const n = V.cut(body.name, 80), u = V.cut(body.url, 400); if (!n) throw bad("Document name is required."); if (u && !/^https?:\/\//i.test(u)) throw bad("Link must start with http."); patch.docs = (o.docs || []).concat([{ id: Math.random().toString(36).slice(2, 9), name: n, url: u, at: nowIso(), by: who(st) }]); await log("Document added: " + n); break; }
      case "doc_remove": { patch.docs = (o.docs || []).filter((d) => d.id !== body.docId); await log("Document removed"); break; }
      case "deposit": case "add_money": {
        needAdmin(st); const amt = money(body.amount); const method = act === "deposit" ? "credit_card" : "system";
        await addLedger(st, o, { kind: act, credit: amt, method, note: body.note || (act === "deposit" ? "Deposit (credit card, entered manually)" : "Money added by system") });
        const r = await addReceipt(st, o, amt, method, body.note, o.uid); extra.receipt = r; await log((act === "deposit" ? "Deposit " : "Added ") + amt); break;
      }
      case "additional_charge": { needAdmin(st); const amt = money(body.amount); await addLedger(st, o, { kind: "additional_charge", debit: amt, note: body.note || "Additional charge" }); await log("Additional charge " + amt + (body.note ? ": " + V.cut(body.note, 100) : "")); break; }
      case "charge_order": { needAdmin(st); const led = await ledger(); if (led.some((l) => l.kind === "charge")) throw bad("This order was already charged."); const amt = round2((o.quote && o.quote.total) || 0); if (!amt) throw bad("The order has no price."); await addLedger(st, o, { kind: "charge", debit: amt, note: "Order charge" }); await log("Order charged " + amt); break; }
      case "refund": { needAdmin(st); const amt = money(body.amount); await addLedger(st, o, { kind: "refund", debit: amt, method: V.oneOf(body.method, METHODS, "other"), note: body.note || "Refund" }); await log("Refund " + amt); break; }
      case "receipt": { needAdmin(st); const p = payOf(o, await ledger()); const rc = await store.list("receipts", { where: [["orderId", "==", id]], limit: 50 }); if (rc.length) { extra.receipt = rc[0]; break; } if (p.paid <= 0) throw bad("No payment recorded for this order."); extra.receipt = await addReceipt(st, o, p.paid, "other", "", o.uid); await log("Receipt " + extra.receipt.no + " created"); break; }
      case "email_user": case "resend": case "summary": {
        const p = payOf(o, await ledger()); const to = body.to || (o.contact && o.contact.email) || (o.sender && o.sender.email);
        const text = act === "summary" || act === "resend" ? summaryText(o, p) + (body.text ? "\n\n" + V.cut(body.text, 1000) : "") : V.cut(body.text, 3000);
        if (!text) throw bad("Write a message.");
        await queueMail(st, o, to, V.cut(body.subject, 160) || (act === "email_user" ? "Your CargoTech shipment " : "Shipment summary ") + o.id, text, act); await log("E-mail queued to " + V.cut(to, 80) + " (" + act + ")"); break;
      }
      case "email_agent": {
        const ag = body.agentId ? await store.get("agents/" + V.cut(body.agentId, 40)) : null; const to = body.to || (ag && ag.email);
        const p = payOf(o, await ledger()); const text = V.cut(body.text, 3000) || summaryText(o, p);
        await queueMail(st, o, to, V.cut(body.subject, 160) || "Shipment " + o.id, text, "email_agent"); await log("E-mail queued to agent " + V.cut(to, 80)); break;
      }
      case "whatsapp": {
        const phone = String(body.phone || (o.contact && o.contact.phone) || (o.sender && o.sender.phone) || "").replace(/[^\d]/g, "").replace(/^00/, "").replace(/^0/, "972");
        if (phone.length < 8) throw bad("No phone number for this customer.");
        const text = V.cut(body.text, 800) || summaryText(o, payOf(o, await ledger()));
        extra.url = "https://wa.me/" + phone + "?text=" + encodeURIComponent(text); await log("WhatsApp message opened"); break;
      }
      default: throw bad("Unknown action.");
    }
    if (Object.keys(patch).length) { patch.updatedAt = nowIso(); await store.update("orders/" + id, patch); }
    await audit("order_action", st.uid, { orderId: id, action: act });
    return { ...(await loadFull(id, st)), ...extra };
  }

  /* ---------- manual accounting entry (not tied to an order) ---------- */
  async function ledgerAdd(req, body) {
    const st = await staffOf(req); needAdmin(st);
    const uid = V.cut(body.uid, 80);
    if (!(await store.get("users/" + uid))) throw new HttpError(404, "user");
    const amt = money(body.amount); const kind = V.oneOf(body.kind, ["credit", "debit"], "credit");
    const method = V.oneOf(body.method, METHODS, "other");
    const row = await addLedger(st, null, { uid, kind: kind === "credit" ? "payment" : "charge", [kind]: amt, method, note: body.note || (kind === "credit" ? "Payment received" : "Charge") });
    let receipt = null;
    if (kind === "credit" && body.receipt !== false) receipt = await addReceipt(st, null, amt, method, body.note, uid);
    await store.add("logs", { uid, text: (kind === "credit" ? "Payment " : "Charge ") + amt, by: who(st), at: nowIso(), type: "ledger" });
    await audit("ledger_add", st.uid, { uid, kind, amt });
    return { ok: true, row, receipt };
  }

  /* ---------- agents, messages ---------- */
  async function agentSave(req, body) {
    const st = await staffOf(req); needAdmin(st);
    const name = V.cut(body.name, 80); if (!name) throw bad("Name is required.");
    const d = { name, kind: V.oneOf(body.kind, ["carrier", "agent", "other"], "agent"), email: V.cut(body.email, 120).toLowerCase(), phone: V.cut(body.phone, 30), country: V.cut(body.country, 2).toLowerCase(), notes: V.cut(body.notes, 500), active: body.active !== false, updatedAt: nowIso() };
    const id = V.cut(body.id, 40);
    if (id) { if (!(await store.get("agents/" + id))) throw new HttpError(404, "agent"); await store.update("agents/" + id, d); return { ok: true, id }; }
    return { ok: true, id: await store.add("agents", { ...d, createdAt: nowIso() }) };
  }
  async function agentDelete(req, body) { const st = await staffOf(req); needAdmin(st); await store.delete("agents/" + V.cut(body.id, 40)); return { ok: true }; }
  async function messageUpdate(req, body) {
    const st = await staffOf(req);
    const id = V.cut(body.id, 60); const m = await store.get("leads/" + id); if (!m) throw new HttpError(404, "message");
    const patch = { status: V.oneOf(body.status, ["new", "read", "done"], m.status || "new") };
    if (body.note != null) patch.note = V.cut(body.note, 500);
    patch.handledBy = who(st); await store.update("leads/" + id, patch);
    return { ok: true };
  }

  return {
    "GET /admin/list": listModule, "GET /admin/counts": counts, "GET /admin/search": search, "GET /admin/finance": finance,
    "GET /admin/user": getUser, "POST /admin/user/update": updateUser, "POST /admin/user/log/add": logAdd,
    "POST /admin/coupon/create": couponCreate, "POST /admin/coupon/cancel": couponCancel, "POST /admin/coupon/reactivate": couponReactivate, "GET /admin/staff/names": staffNames,
    "POST /admin/task/create": taskCreate, "POST /admin/task/close": taskClose, "POST /admin/task/reassign": taskReassign,
    "GET /admin/task": taskGet, "POST /admin/task/update": taskUpdate,
    "GET /admin/order": getOrder, "POST /admin/order/action": orderAction, "POST /admin/ledger/add": ledgerAdd,
    "POST /admin/agent/save": agentSave, "POST /admin/agent/delete": agentDelete, "POST /admin/message/update": messageUpdate,
    "GET /admin/pricelist/list": pricelistList, "GET /admin/pricelist": pricelistGet, "POST /admin/pricelist/save": pricelistSave, "POST /admin/pricelist/delete": pricelistDelete,
    "GET /admin/banner/list": bannerList, "POST /admin/banner/save": bannerSave, "POST /admin/banner/delete": bannerDelete,
  };
}

module.exports = { makeBackoffice };
