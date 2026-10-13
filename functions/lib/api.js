"use strict";
/* CargoTech order API. All data access goes through "store"; all identity checks through "verifyIdToken".
   IMPORTANT RULE: a staff price code is read, checked and thrown away. It is never written to the database,
   never logged and never sent back. Only a one-way fingerprint (keyed hash) is kept so the code can be recognised. */
const { sha256, hmac, randToken, genCode, normalizeCode, signToken, verifyToken } = require("./security");
const { DEFAULT_SETTINGS, priceOffer, round2, chargeableKg } = require("./pricing");
const { getOffers } = require("./providers");
const { mainCity } = require("./defaults");
const { makeBackoffice } = require("./backoffice");
const { couponStatus } = require("./coupons");
const V = require("./validate");

const ID_ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789";
const STATUSES = ["draft", "new", "quote_sent", "booked", "picked_up", "in_transit", "delivered", "cancelled"];

function createApi(deps) {
  const { store, verifyIdToken, createAuthUser, createCustomToken, revokeRefreshTokens } = deps;
  const scope = deps.scope || "all";            /* "public" = customer server, "admin" = back-office server, "all" = tests only */
  const nowIso = deps.now || (() => new Date().toISOString());
  const ownerEmail = () => String(deps.ownerEmail ? deps.ownerEmail() : process.env.OWNER_EMAIL || "").trim().toLowerCase();

  class HttpError extends Error { constructor(status, msg, extra) { super(msg); this.status = status; this.extra = extra || {}; } }
  const bad = (m, extra) => new HttpError(400, m, extra);

  /* ---------- small helpers ---------- */
  let pepperCache = null;
  async function pepper() {
    if (pepperCache) return pepperCache;
    let d = await store.get("_system/security");
    if (!d || !d.pepper) {
      try { await store.create("_system/security", { pepper: randToken(32), createdAt: nowIso() }); } catch (e) { /* created by a parallel request */ }
      d = await store.get("_system/security");
    }
    pepperCache = d.pepper;
    return pepperCache;
  }
  async function settings() { return { ...DEFAULT_SETTINGS, ...((await store.get("settings/pricing")) || {}) }; }
  const audit = (type, actor, data) => store.add("audit", { type, actor: actor || null, data: data || {}, at: nowIso() }).catch(() => {});
  const clientKey = (req) => sha256("ip:" + String((req.headers["x-forwarded-for"] || req.ip || "")).split(",")[0].trim());

  async function authOf(req) {
    const h = String(req.headers.authorization || "");
    if (!h.startsWith("Bearer ")) return null;
    try { return await verifyIdToken(h.slice(7)); } catch (e) { return null; }
  }
  async function staffOf(req, needAdmin) {
    const a = await authOf(req);
    if (!a) throw new HttpError(401, "auth");
    const s = await store.get("staff/" + a.uid);
    if (!s || s.active === false) throw new HttpError(403, "not-staff");
    if (needAdmin && s.role !== "admin") throw new HttpError(403, "admin-only");
    return { uid: a.uid, email: a.email, ...s };
  }

  /* Rate limit for code attempts: 8 wrong tries per 15 minutes per visitor */
  async function rateOk(key) { const d = await store.get("rate/" + key); return !(d && d.resetAt > Date.now() && d.n >= 8); }
  async function rateFail(key) {
    const d = await store.get("rate/" + key);
    const live = d && d.resetAt > Date.now();
    await store.set("rate/" + key, { n: live ? d.n + 1 : 1, resetAt: live ? d.resetAt : Date.now() + 15 * 60 * 1000 });
  }

  /* ---------- order helpers ---------- */
  async function newOrderId(data) {
    for (let i = 0; i < 8; i++) {
      let s = "";
      for (let k = 0; k < 6; k++) s += ID_ALPHABET[Math.floor(Math.random() * ID_ALPHABET.length)];
      const id = "CT-" + s;
      try { await store.create("orders/" + id, data(id)); return id; } catch (e) { /* id taken, try again */ }
    }
    throw new HttpError(500, "id");
  }
  async function loadOrder(id, token, auth) {
    id = V.cut(id, 20);
    const o = id ? await store.get("orders/" + id) : null;
    if (!o) throw new HttpError(404, "order");
    const byToken = token && o.tokenHash && sha256(token) === o.tokenHash;
    const byUid = auth && o.uid && o.uid === auth.uid;
    if (!byToken && !byUid) throw new HttpError(404, "order");
    return o;
  }
  const publicQuote = (q) => q && {
    offerId: q.offerId || null, carrier: q.carrier || "", service: q.service || "", days: q.days || "", test: !!q.test, manual: !!q.manual,
    lines: (q.lines || []).map((l) => ({ key: l.key, label: l.label, price: l.price })), total: q.total == null ? null : q.total, originalTotal: q.originalTotal || null, currency: q.currency || "ILS",
  };
  const customerView = (o) => ({
    id: o.id, status: o.status, step: o.step, customerType: o.customerType, type: o.type, from: o.from, to: o.to, parcels: o.parcels, cont: o.cont,
    selectedOffer: o.selectedOffer || null, signature: o.signature, sender: o.sender, recipient: o.recipient, items: o.items, insurance: o.insurance,
    pickup: { date: o.pickup && o.pickup.date, time: o.pickup && o.pickup.time, trackingNumber: (o.pickup && o.pickup.trackingNumber) || "" },
    terms: o.terms, declarations: o.declarations, quote: publicQuote(o.quote), createdAt: o.createdAt, updatedAt: o.updatedAt,
  });

  /* ---------- quoting ---------- */
  function checkRoute(c) {
    if (!c.customerType) throw bad("בחרו אם השולח פרטי או עסקי.");
    if (!c.from || !c.to) throw bad("בחרו מדינת מוצא ומדינת יעד.");
    if (c.from === c.to) throw bad("מדינת המוצא והיעד זהות.");
    if (c.type === "parcel" && !c.parcels.some((p) => p.kg > 0)) throw bad("הוסיפו משקל לחבילה, גם הערכה מספיקה.");
  }
  /* the customer's own postal code wins; otherwise the main city of the country is used for the first price */
  function zipFor(cc, entered) {
    const z = String(entered || "").trim();
    if (z) return { zip: z, city: "", assumed: false };
    const d = mainCity(cc);
    return { zip: d ? d.zip : "", city: d ? d.city : "", assumed: true };
  }
  /* discountPct: a customer-level discount set on their profile (back office, User Details) - applied on top
     of the normal markup, same spirit as a per-shipment Pricing Override but automatic and customer-wide. */
  async function discountPctOf(auth) {
    if (!auth) return 0;
    const u = await store.get("users/" + auth.uid);
    const n = u && Number(u.discountPct);
    return Number.isFinite(n) && n > 0 ? n : 0;
  }
  async function buildOffers(c, s, discountPct) {
    const zf = zipFor(c.from, c.sender.zip), zt = zipFor(c.to, c.recipient.zip);
    const raw = await getOffers({ mode: "intl", from: c.from, to: c.to, type: c.type, parcels: c.parcels, zips: { from: zf.zip, to: zt.zip }, cities: { from: zf.city, to: zt.city }, entered: { from: c.sender.zip, to: c.recipient.zip } }, s);
    const res = raw.map((o) => {
      const priced = priceOffer(o, { customerType: c.customerType, signature: c.signature, settings: s });
      if (discountPct) { priced.originalTotal = priced.total; priced.total = round2(priced.total * (1 - discountPct / 100)); }
      return { raw: o, priced };
    });
    res.assumed = { from: zf.assumed ? zf.city : "", to: zt.assumed ? zt.city : "" };
    return res;
  }
  const offerView = ({ raw, priced }) => ({
    id: raw.id, carrier: raw.carrier, service: raw.service, days: raw.days, includes: raw.includes || [], test: !!raw.test,
    total: priced.total, originalTotal: priced.originalTotal || null, currency: priced.currency, lines: priced.lines.map((l) => ({ key: l.key, label: l.label, price: l.price })),
  });
  function changeInfo(prev, now, lines, prevKeys) {
    if (prev == null || now == null || Math.abs(prev - now) < 0.005) return null;
    const before = Array.isArray(prevKeys) ? prevKeys : null;
    const fresh = lines.map((l) => l.key).filter((k) => !before || !before.includes(k));
    const reasons = [];
    if (fresh.includes("remote")) reasons.push("remote");
    if (fresh.includes("signature")) reasons.push("signature");
    return { from: round2(prev), to: round2(now), delta: round2(now - prev), reasons };
  }

  async function postQuote(req, body) {
    const s = await settings();
    const c = V.order(body);
    checkRoute(c);
    const discountPct = await discountPctOf(await authOf(req));
    const priced = await buildOffers(c, s, discountPct);
    const offers = priced.map(offerView);
    const out = { ok: true, offers, manual: offers.length === 0, assumed: priced.assumed, testMode: !!s.testMode, currency: s.currency };
    if (body.selected) {
      const m = priced.find((p) => p.raw.id === V.cut(body.selected, 40));
      if (m) out.change = changeInfo(body.previousTotal == null ? null : Number(body.previousTotal), m.priced.total, m.priced.lines, (Array.isArray(body.previousKeys) ? body.previousKeys : null) && body.previousKeys.map((k) => V.cut(k, 20)));
    }
    return out;
  }

  /* ---------- save / submit an order ---------- */
  async function postOrderSave(req, body) {
    const s = await settings();
    const auth = await authOf(req);
    const c = V.order(body);
    const token = req.headers["x-order-token"] || "";
    let existing = null;
    if (body.orderId) existing = await loadOrder(body.orderId, token, auth);
    const submit = body.submit === true;
    if (submit) { const miss = V.missingForSubmit(c); if (miss.length) throw bad("missing", { errors: miss }); }
    if (!existing && !(c.sender.phone || c.sender.email || c.recipient.phone)) throw bad("נדרש לפחות טלפון או אימייל לשמירת הזמנה.");
    if (!c.customerType) throw bad("בחרו אם השולח פרטי או עסקי.");

    /* price: recomputed on the server, the browser only says which offer it picked */
    const discountPct = await discountPctOf(auth);
    let quote = existing && existing.quote ? existing.quote : null;
    if (c.from && c.to && c.from !== c.to) {
      const priced = await buildOffers(c, s, discountPct);
      const sel = c.selectedOffer && priced.find((p) => p.raw.id === c.selectedOffer);
      if (sel) {
        const prevHistory = (quote && quote.history) || [];
        const sameBasis = quote && quote.overridden && quote.offerId === sel.raw.id && quote.computedTotal === sel.priced.total;
        quote = {
          offerId: sel.raw.id, carrier: sel.raw.carrier, service: sel.raw.service, days: sel.raw.days, test: !!sel.raw.test, manual: false,
          lines: sameBasis ? quote.lines : sel.priced.lines, computedTotal: sel.priced.total, total: sameBasis ? quote.total : sel.priced.total, cost: sel.priced.cost,
          originalTotal: sel.priced.originalTotal || null, customerDiscountPct: discountPct || null, markupPct: sel.priced.markupPct, currency: sel.priced.currency, overridden: !!sameBasis,
          history: prevHistory.concat(!quote || quote.total !== sel.priced.total ? [{ at: nowIso(), total: sel.priced.total, by: "system" }] : []),
        };
      } else if (!c.selectedOffer && !(quote && quote.manualPrice != null)) {
        quote = priced.length ? null : { manual: true, total: null, lines: [], currency: s.currency, history: (quote && quote.history) || [] };
      }
    }

    const droppedOverride = !!(existing && existing.quote && existing.quote.overridden && !(quote && quote.overridden));
    const base = {
      ...c, ...(droppedOverride && existing.coupon ? { coupon: { ...existing.coupon, superseded: true } } : {}), uid: auth ? auth.uid : (existing && existing.uid) || null, quote,
      contact: { name: c.sender.name, email: c.sender.email, phone: c.sender.phone },
      updatedAt: nowIso(),
    };
    const out = { ok: true };
    if (!existing) {
      const tok = randToken(24);
      let created;
      const id = await newOrderId((oid) => (created = {
        id: oid, status: submit ? "new" : "draft", tokenHash: sha256(tok), createdAt: nowIso(), submittedAt: submit ? nowIso() : null,
        coupon: null, notes: [], ...base, pickup: { ...c.pickup, confirmation: "", callNumber: "", trackingNumber: "" },
      }));
      out.orderId = id; out.token = tok; out.status = created.status;
      out.quote = publicQuote(created.quote);
    } else {
      const patch = { ...base, pickup: { ...(existing.pickup || {}), ...c.pickup } };
      if (submit && existing.status === "draft") { patch.status = "new"; patch.submittedAt = nowIso(); }
      if (existing.step && c.step < existing.step && !submit) patch.step = existing.step;
      await store.update("orders/" + existing.id, patch);
      out.orderId = existing.id; out.status = patch.status || existing.status; out.quote = publicQuote(quote);
    }
    return out;
  }

  /* ---------- staff price code ---------- */
  async function postPromo(req, body) {
    const key = clientKey(req);
    if (!(await rateOk(key))) throw new HttpError(429, "נסיונות רבים מדי. נסו שוב בעוד כמה דקות.");
    const auth = await authOf(req);
    const order = await loadOrder(body.orderId, req.headers["x-order-token"] || "", auth);
    const s = await settings();
    const code = normalizeCode(body.code);
    const fail = async () => { await rateFail(key); throw bad("הקוד לא תקין."); };
    if (code.length < 8) return fail();
    const P = await pepper();
    const rec = await store.get("staffCodes/" + hmac(P, code));
    if (!rec || rec.active === false) return fail();
    const st = await store.get("staff/" + rec.staffId);
    if (!st || st.active === false) return fail();
    if (s.requireStaffLogin && !(auth && auth.uid === rec.staffId)) return fail();   /* same answer on purpose: no hints */
    if (!order.quote || order.quote.total == null) throw bad("בחרו שירות לפני שינוי מחיר.");
    await store.delete("rate/" + key).catch(() => {});
    return { ok: true, overrideToken: signToken({ o: order.id, s: rec.staffId }, P, 20 * 60), currentTotal: order.quote.total, currency: order.quote.currency };
  }

  async function postOverride(req, body) {
    const auth = await authOf(req);
    const order = await loadOrder(body.orderId, req.headers["x-order-token"] || "", auth);
    const P = await pepper();
    const t = verifyToken(body.overrideToken, P);
    if (!t || t.o !== order.id) throw new HttpError(403, "הרשאה פגה. הקלידו את הקוד שוב.");
    const st = await store.get("staff/" + t.s);
    if (!st || st.active === false) throw new HttpError(403, "הרשאה פגה. הקלידו את הקוד שוב.");
    const price = Number(body.price);
    if (!Number.isFinite(price) || price < 0 || price > 1000000) throw bad("מחיר לא תקין.");
    const reason = V.cut(body.reason, 200);
    if (reason.length < 2) throw bad("כתבו סיבה קצרה לשינוי המחיר.");
    const q = { ...order.quote };
    const original = q.computedTotal != null ? q.computedTotal : q.total;
    const baseLines = (q.lines || []).filter((l) => l.key !== "adjust");
    const baseSum = round2(baseLines.reduce((a, l) => a + l.price, 0));
    q.total = round2(price); q.overridden = true;
    q.lines = Math.abs(q.total - baseSum) < 0.005 ? baseLines : baseLines.concat([{ key: "adjust", label: "התאמת מחיר", cost: 0, price: round2(q.total - baseSum) }]);
    q.history = (q.history || []).concat([{ at: nowIso(), total: q.total, by: "staff:" + t.s, reason }]);
    const coupon = { type: "staff", staffId: t.s, staffName: st.name || "", at: nowIso(), originalPrice: original, newPrice: q.total, reason };
    await store.update("orders/" + order.id, { quote: q, coupon, updatedAt: nowIso() });
    await audit("price_override", t.s, { orderId: order.id, from: original, to: q.total, reason });
    return { ok: true, quote: publicQuote(q) };
  }

  /* ---------- customers ---------- */
  async function getMe(req) {
    const a = await authOf(req); if (!a) throw new HttpError(401, "auth");
    let profile = (await store.get("users/" + a.uid)) || null;
    if (!profile) { profile = { uid: a.uid, email: String(a.email || "").toLowerCase(), userNo: await store.incr("_system/counters", "user"), createdAt: nowIso() }; await store.set("users/" + a.uid, profile); }
    const addresses = await store.list("users/" + a.uid + "/addresses", { limit: 50 });
    const orders = (await store.list("orders", { where: [["uid", "==", a.uid]], limit: 100 })).sort((x, y) => (x.updatedAt < y.updatedAt ? 1 : -1)).map(customerView);
    return { ok: true, email: a.email || "", profile, addresses, orders };
  }
  async function putMe(req, body) {
    const a = await authOf(req); if (!a) throw new HttpError(401, "auth");
    const prev = (await store.get("users/" + a.uid)) || { createdAt: nowIso() };
    if (!prev.userNo) prev.userNo = await store.incr("_system/counters", "user");
    const p = {
      ...prev, uid: a.uid, email: String(a.email || "").toLowerCase(), firstName: V.cut(body.firstName, 40), lastName: V.cut(body.lastName, 40),
      phone: V.cut(body.phone, 30), useFor: V.oneOf(body.useFor, ["private", "business"], prev.useFor || "private"), marketing: body.marketing === true, updatedAt: nowIso(),
    };
    await store.set("users/" + a.uid, p);
    return { ok: true, profile: p };
  }
  /* a coupon a customer enters themselves (typically at signup) - the code was created in the back office in advance.
     "once" coupons bind to the first customer who redeems them; "multi" coupons can be redeemed by any number of
     customers within their valid window. Redeeming only records the link; nothing here changes a price yet. */
  async function postCouponRedeem(req, body) {
    const a = await authOf(req); if (!a) throw new HttpError(401, "auth");
    const code = V.cut(body.code, 20).trim().toUpperCase();
    if (!code) throw bad("חסר קוד קופון.");
    const rows = await store.list("coupons", { where: [["code", "==", code]], limit: 1 });
    const c = rows[0];
    const fail = () => { throw bad("קוד הקופון לא תקין או שפג תוקפו."); };
    if (!c || couponStatus(c, nowIso()) !== "active") return fail();
    if (c.uid && c.uid !== a.uid) return fail();
    await store.update("coupons/" + c.id, { uid: a.uid, usesCount: (c.usesCount || 0) + 1 });
    await audit("coupon_redeem", a.uid, { id: c.id, code });
    return { ok: true, pct: c.pct };
  }
  /* ---------- banners: admin builds them in the back office (lib/backoffice.js), the public site reads/shows them
     here. No auth - any visitor, logged in or not, can trigger a banner. */
  const bannerView = (p) => ({
    id: p.id, title: p.title, body: p.body, imageUrl: p.imageUrl || "", ctaText: p.ctaText || "", ctaType: p.ctaType || "none",
    ctaValue: p.ctaValue || "", template: p.template, anim: p.anim, delaySec: p.delaySec || 0, frequency: p.frequency || "always",
  });
  async function getActiveBanners(req) {
    const page = V.oneOf(req.query.page, ["home", "all"], "all");
    const today = nowIso().slice(0, 10);
    const rows = await store.list("banners", { where: [["enabled", "==", true]], limit: 100 });
    const live = rows.filter((p) => {
      if (p.page !== "all" && p.page !== page) return false;
      if (p.activeFrom && today < p.activeFrom) return false;
      if (p.activeTo && today > p.activeTo) return false;
      return true;
    });
    live.sort((a, b) => (a.page === b.page ? (b.updatedAt || "").localeCompare(a.updatedAt || "") : a.page === page ? -1 : 1));
    return { ok: true, banner: live[0] ? bannerView(live[0]) : null };
  }
  const BANNER_EVENT_FIELD = { show: "shows", click: "clicks", dismiss: "dismisses" };
  async function postBannerEvent(req, body) {
    const id = V.cut(body.id, 40);
    const field = BANNER_EVENT_FIELD[V.oneOf(body.kind, ["show", "click", "dismiss"], "")];
    if (!id || !field) throw bad("missing");
    if (!(await store.get("banners/" + id))) return { ok: true }; /* banner may have been deleted since - not an error */
    await store.incr("banners/" + id, field);
    return { ok: true };
  }
  async function postAddress(req, body) {
    const a = await authOf(req); if (!a) throw new HttpError(401, "auth");
    const addr = V.addr(body.address);
    if (!addr.country || !addr.city || !addr.street) throw bad("כתובת חסרה.");
    const id = await store.add("users/" + a.uid + "/addresses", { nickname: V.cut(body.nickname, 40) || addr.name || addr.street, ...addr, createdAt: nowIso() });
    return { ok: true, id };
  }
  async function deleteAddress(req, body) {
    const a = await authOf(req); if (!a) throw new HttpError(401, "auth");
    await store.delete("users/" + a.uid + "/addresses/" + V.cut(body.id, 40));
    return { ok: true };
  }

  /* ---------- back office ---------- */
  const profitOf = (q) => (q && q.total != null && q.cost != null ? round2(q.total - q.cost) : null);
  function adminView(o, st) {
    const isAdmin = st.role === "admin";
    const q = o.quote ? { ...publicQuote(o.quote), overridden: !!o.quote.overridden, markupPct: isAdmin ? o.quote.markupPct : undefined, customerDiscountPct: isAdmin ? (o.quote.customerDiscountPct || null) : undefined, history: o.quote.history || [] } : null;
    if (q && isAdmin) { q.cost = o.quote.cost == null ? null : o.quote.cost; q.profit = profitOf(o.quote); q.lines = (o.quote.lines || []).map((l) => ({ key: l.key, label: l.label, price: l.price, cost: l.cost })); }
    let coupon = null;
    if (o.coupon) coupon = isAdmin || o.coupon.staffId === st.uid ? o.coupon : { type: "staff", staffName: "", hidden: true };
    return {
      id: o.id, status: o.status, createdAt: o.createdAt, updatedAt: o.updatedAt, submittedAt: o.submittedAt || null, customerType: o.customerType, uid: o.uid || null,
      shipType: o.shipType || null,
      contact: o.contact, from: o.from, to: o.to, type: o.type, parcels: o.parcels, cont: o.cont, sender: o.sender, recipient: o.recipient, items: o.items,
      insurance: o.insurance, pickup: o.pickup, terms: o.terms, signature: o.signature, declarations: o.declarations, quote: q, coupon, notes: o.notes || [], step: o.step,
    };
  }
  const matchQ = (o, q) => !q || JSON.stringify([o.id, o.contact, o.sender && o.sender.city, o.recipient && o.recipient.city, o.from, o.to]).toLowerCase().includes(q);

  async function adminOrders(req) {
    const st = await staffOf(req);
    const status = V.cut(req.query.status, 20), q = V.cut(req.query.q, 60).toLowerCase();
    let rows = await store.list("orders", { orderBy: "updatedAt", dir: "desc", limit: 400 });
    if (status) rows = rows.filter((o) => o.status === status);
    rows = rows.filter((o) => matchQ(o, q));
    return { ok: true, role: st.role, orders: rows.map((o) => adminView(o, st)) };
  }
  async function adminOrderUpdate(req, body) {
    const st = await staffOf(req);
    const o = await store.get("orders/" + V.cut(body.id, 20));
    if (!o) throw new HttpError(404, "order");
    const patch = { updatedAt: nowIso() };
    if (body.status) { if (!STATUSES.includes(body.status)) throw bad("סטטוס לא תקין."); patch.status = body.status; }
    if (body.note) patch.notes = (o.notes || []).concat([{ at: nowIso(), by: st.name || st.email || st.uid, text: V.cut(body.note, 500) }]);
    if (body.pickup && typeof body.pickup === "object") {
      patch.pickup = { ...(o.pickup || {}), confirmation: V.cut(body.pickup.confirmation, 60), callNumber: V.cut(body.pickup.callNumber, 60), trackingNumber: V.cut(body.pickup.trackingNumber, 60),
        date: /^\d{4}-\d{2}-\d{2}$/.test(String(body.pickup.date || "")) ? body.pickup.date : (o.pickup && o.pickup.date) || "", time: V.cut(body.pickup.time != null ? body.pickup.time : o.pickup && o.pickup.time, 20) };
    }
    if (body.manualPrice != null && body.manualPrice !== "") {
      const mp = Number(body.manualPrice);
      if (!Number.isFinite(mp) || mp < 0 || mp > 1000000) throw bad("מחיר לא תקין.");
      const mc = body.manualCost === "" || body.manualCost == null ? null : Number(body.manualCost);
      const prev = o.quote || { history: [] };
      patch.quote = { ...prev, manual: true, manualPrice: round2(mp), total: round2(mp), cost: mc == null || !Number.isFinite(mc) ? (prev.cost == null ? null : prev.cost) : round2(mc),
        carrier: V.cut(body.carrier, 60) || prev.carrier || "", service: V.cut(body.service, 60) || prev.service || "", days: V.cut(body.days, 20) || prev.days || "",
        lines: [{ key: "manual", label: "שילוח", price: round2(mp), cost: mc == null || !Number.isFinite(mc) ? 0 : round2(mc) }], currency: (prev.currency || "ILS"),
        history: (prev.history || []).concat([{ at: nowIso(), total: round2(mp), by: "staff:" + st.uid }]) };
      if (!body.status && o.status === "new") patch.status = "quote_sent";
    }
    await store.update("orders/" + o.id, patch);
    await audit("order_update", st.uid, { orderId: o.id, fields: Object.keys(patch).filter((k) => k !== "updatedAt") });
    return { ok: true, order: adminView({ ...o, ...patch }, st) };
  }

  async function adminMe(req) {
    const a = await authOf(req); if (!a) throw new HttpError(401, "auth");
    const st = await store.get("staff/" + a.uid);
    if (!st || st.active === false) return { ok: true, staff: false, canBootstrap: !!(a.emailVerified && ownerEmail() && String(a.email || "").toLowerCase() === ownerEmail()), emailVerified: !!a.emailVerified };
    return { ok: true, staff: true, uid: a.uid, name: st.name || "", role: st.role, hasCode: !!st.codeKey };
  }
  async function adminBootstrap(req) {
    const a = await authOf(req); if (!a) throw new HttpError(401, "auth");
    const mail = String(a.email || "").toLowerCase();
    if (!a.emailVerified || !ownerEmail() || mail !== ownerEmail()) throw new HttpError(403, "not-owner");
    if (await store.get("staff/" + a.uid)) return { ok: true };
    await store.set("staff/" + a.uid, { name: V.cut(a.name, 60) || mail, email: mail, role: "admin", active: true, codeKey: "", createdAt: nowIso() });
    await audit("bootstrap_admin", a.uid, {});
    return { ok: true };
  }
  async function staffList(req) {
    await staffOf(req, true);
    const rows = await store.list("staff", { limit: 100 });
    return { ok: true, staff: rows.map((r) => ({ uid: r.id, name: r.name, email: r.email, role: r.role, active: r.active !== false, hasCode: !!r.codeKey })) };
  }
  async function staffCreate(req, body) {
    await staffOf(req, true);
    const email = V.cut(body.email, 80).toLowerCase(), name = V.cut(body.name, 60), password = String(body.password || "");
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) throw bad("אימייל לא תקין.");
    if (!name) throw bad("חסר שם.");
    if (password.length < 8) throw bad("הסיסמה הזמנית צריכה להיות באורך 8 תווים לפחות.");
    let uid;
    try { uid = await createAuthUser({ email, password, displayName: name }); } catch (e) { throw bad("לא ניתן ליצור משתמש. ייתכן שהאימייל כבר קיים."); }
    await store.set("staff/" + uid, { name, email, role: V.oneOf(body.role, ["admin", "staff"], "staff"), active: true, codeKey: "", createdAt: nowIso() });
    await audit("staff_create", null, { uid });
    return { ok: true, uid };
  }
  async function staffUpdate(req, body) {
    const me = await staffOf(req, true);
    const uid = V.cut(body.uid, 128);
    const st = await store.get("staff/" + uid);
    if (!st) throw new HttpError(404, "staff");
    const patch = {};
    if (body.role) patch.role = V.oneOf(body.role, ["admin", "staff"], st.role);
    if (body.active != null) patch.active = body.active === true;
    const isOwnerAccount = !!(st.email && ownerEmail() && String(st.email).toLowerCase() === ownerEmail());
    if (isOwnerAccount && (patch.active === false || (patch.role && patch.role !== "admin"))) throw bad("Cannot disable or demote the account owner.");
    if (uid === me.uid && (patch.active === false || (patch.role && patch.role !== "admin"))) throw bad("אי אפשר להוריד הרשאות לעצמך.");
    if (patch.active === false && st.codeKey) { await store.delete("staffCodes/" + st.codeKey).catch(() => {}); patch.codeKey = ""; }
    await store.update("staff/" + uid, patch);
    await audit("staff_update", me.uid, { uid, fields: Object.keys(patch) });
    return { ok: true };
  }
  /* signs out of every device at once (revokes all existing sessions) - not a lock: signing back in with the
     same email/password works immediately everywhere, on any device. Staff can do this to themselves; an admin
     can also do it to another staff member (e.g. someone who left, or a lost device) - except the account owner,
     who only ever signs themselves out, same protection as disabling/demoting that account. */
  async function staffSignOutAll(req, body) {
    const me = await staffOf(req);
    const uid = V.cut(body.uid, 128) || me.uid;
    if (uid !== me.uid) {
      if (me.role !== "admin") throw new HttpError(403, "admin-only");
      const target = await store.get("staff/" + uid);
      if (!target) throw new HttpError(404, "staff");
      const isOwnerAccount = !!(target.email && ownerEmail() && String(target.email).toLowerCase() === ownerEmail());
      if (isOwnerAccount) throw bad("Cannot sign out the account owner - only the owner can do that to themselves.");
    }
    if (!revokeRefreshTokens) throw new HttpError(500, "not-configured");
    await revokeRefreshTokens(uid);
    await audit("staff_signout_all", me.uid, { uid });
    return { ok: true };
  }
  /* "log in as this customer": lets an admin open the public site signed in as a given customer, without ever
     touching that customer's password (which this system never has access to - Firebase stores it one-way hashed).
     Every use is logged on the customer's own account, same as any other staff action on it. */
  async function adminImpersonate(req, body) {
    const me = await staffOf(req, true);
    const uid = V.cut(body.uid, 128);
    if (!(await store.get("users/" + uid))) throw new HttpError(404, "user");
    if (!createCustomToken) throw new HttpError(500, "not-configured");
    const token = await createCustomToken(uid);
    await store.add("logs", { uid, text: "Staff signed in as this account (" + (me.name || me.email || me.uid) + ")", by: me.name || me.email || me.uid, at: nowIso(), type: "impersonate" });
    await audit("impersonate", me.uid, { uid });
    return { ok: true, token };
  }
  /* the reset e-mail itself is sent client-side by the back office (Firebase's own sendPasswordResetEmail, no password
     ever touches our servers); this just records that staff asked for it, on the customer's own log. */
  async function adminResetPasswordLog(req, body) {
    const me = await staffOf(req);
    const uid = V.cut(body.uid, 128);
    if (!(await store.get("users/" + uid))) throw new HttpError(404, "user");
    await store.add("logs", { uid, text: "Password reset link sent (" + (me.name || me.email || me.uid) + ")", by: me.name || me.email || me.uid, at: nowIso(), type: "reset_password" });
    await audit("reset_password", me.uid, { uid });
    return { ok: true };
  }
  async function codeGenerate(req) {
    const me = await staffOf(req);
    const P = await pepper();
    const code = genCode();
    const key = hmac(P, normalizeCode(code));
    if (me.codeKey) await store.delete("staffCodes/" + me.codeKey).catch(() => {});
    await store.set("staffCodes/" + key, { staffId: me.uid, active: true, createdAt: nowIso() });
    await store.update("staff/" + me.uid, { codeKey: key });
    await audit("code_generated", me.uid, {});
    return { ok: true, code };              /* shown once, to the employee who asked. Not stored. */
  }
  async function codeRevoke(req, body) {
    const me = await staffOf(req, true);
    const uid = V.cut(body.uid, 128);
    const st = await store.get("staff/" + uid);
    if (!st) throw new HttpError(404, "staff");
    if (st.codeKey) await store.delete("staffCodes/" + st.codeKey).catch(() => {});
    await store.update("staff/" + uid, { codeKey: "" });
    await audit("code_revoked", me.uid, { uid });
    return { ok: true };
  }
  const SETTING_FIELDS = { markupBusinessPct: [0, 1000], markupPrivatePct: [0, 1000], signatureFeeUsd: [0, 1000], usdIls: [0.1, 100] };
  const SETTING_FLAGS = ["markupOnSurcharges", "markupOnSignature", "testMode", "requireStaffLogin"];
  async function getSettings(req) { await staffOf(req, true); return { ok: true, settings: await settings() }; }
  async function postSettings(req, body) {
    const me = await staffOf(req, true);
    const patch = {};
    Object.keys(SETTING_FIELDS).forEach((k) => { if (body[k] != null) { const n = Number(body[k]); if (!Number.isFinite(n) || n < SETTING_FIELDS[k][0] || n > SETTING_FIELDS[k][1]) throw bad("ערך לא תקין: " + k); patch[k] = n; } });
    SETTING_FLAGS.forEach((k) => { if (body[k] != null) patch[k] = body[k] === true; });
    await store.set("settings/pricing", { ...((await store.get("settings/pricing")) || {}), ...patch });
    await audit("settings_update", me.uid, patch);
    return { ok: true, settings: await settings() };
  }

  async function getConfig() {
    const s = await settings();
    const fee = round2(s.signatureFeeUsd * s.usdIls);
    const up = (p) => (s.markupOnSignature ? round2(fee * (1 + p / 100)) : fee);
    return { ok: true, testMode: !!s.testMode, signatureFee: { business: up(s.markupBusinessPct), private: up(s.markupPrivatePct) }, currency: s.currency };
  }

  /* ---------- router ---------- */
  const routes = {
    "GET /config": () => getConfig(),
    "POST /quote": postQuote,
    "POST /order/save": postOrderSave,
    "GET /order": async (req) => { const o = await loadOrder(req.query.id, req.headers["x-order-token"] || "", await authOf(req)); return { ok: true, order: customerView(o) }; },
    "POST /promo": postPromo,
    "POST /order/override": postOverride,
    "GET /me": getMe, "PUT /me": putMe, "POST /addresses": postAddress, "POST /addresses/delete": deleteAddress, "POST /coupon/redeem": postCouponRedeem,
    "GET /banners/active": getActiveBanners, "POST /banners/event": postBannerEvent,
    "GET /admin/me": adminMe, "POST /admin/bootstrap": adminBootstrap,
    "GET /admin/orders": adminOrders, "POST /admin/order/update": adminOrderUpdate,
    "GET /admin/staff": staffList, "POST /admin/staff/create": staffCreate, "POST /admin/staff/update": staffUpdate, "POST /admin/staff/signout": staffSignOutAll,
    "POST /admin/code/generate": codeGenerate, "POST /admin/code/revoke": codeRevoke,
    "POST /admin/user/impersonate": adminImpersonate, "POST /admin/user/reset_password_log": adminResetPasswordLog,
    "GET /admin/settings": getSettings, "POST /admin/settings": postSettings,
    ...makeBackoffice({ store, staffOf, audit, HttpError, bad, nowIso, round2, adminView, STATUSES, profitOf, settings, getOffers, priceOffer, chargeableKg }),
  };

  return async function handle(req, res) {
    res.set("Cache-Control", "no-store");
    try {
      const origin = req.headers.origin;
      if (origin && req.method !== "GET") {
        let host = ""; try { host = new URL(origin).host; } catch (e) { /* ignore */ }
        const own = String(req.headers["x-forwarded-host"] || req.headers.host || "").split(",")[0].trim();
        if (host !== own && !/^localhost(:\d+)?$/.test(host)) return res.status(403).json({ ok: false, error: "origin" });
      }
      const path = String(req.path || "").replace(/^\/api\/v1/, "").replace(/\/+$/, "") || "/";
      /* the public server never answers back-office routes, and the back-office server never answers customer routes */
      const isAdminPath = path === "/admin" || path.indexOf("/admin/") === 0;
      if ((scope === "public" && isAdminPath) || (scope === "admin" && !isAdminPath)) return res.status(404).json({ ok: false, error: "not-found" });
      const fn = routes[req.method + " " + path];
      if (!fn) return res.status(404).json({ ok: false, error: "not-found" });
      const body = req.body && typeof req.body === "object" ? req.body : {};
      const out = await fn(req, body);
      return res.status(200).json(out);
    } catch (e) {
      if (e instanceof HttpError) return res.status(e.status).json({ ok: false, error: e.message, ...e.extra });
      return res.status(500).json({ ok: false, error: "server" });         /* no details, no request data in any log */
    }
  };
}

module.exports = { createApi };
