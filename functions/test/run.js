"use strict";
/* Integration tests for the order API using the in-memory store. Run: node test/run.js */
const assert = require("assert");
const { createApi } = require("../lib/api");
const { memoryStore } = require("../lib/store");
const { priceOffer, round2 } = require("../lib/pricing");

const store = memoryStore();
const users = {
  owner: { uid: "u-owner", email: "owner@example.com", emailVerified: true },
  emp: { uid: "u-emp", email: "emp@example.com", emailVerified: true },
  cust: { uid: "u-cust", email: "c@example.com", emailVerified: true },
};
let created = 0;
const revoked = [];
const api = createApi({
  store, ownerEmail: () => "owner@example.com",
  verifyIdToken: async (t) => { const u = users[String(t).replace("test:", "")]; if (!u) throw new Error("bad"); return u; },
  createAuthUser: async ({ email }) => "u-new" + (++created),
  createCustomToken: async (uid) => "custom:" + uid,
  revokeRefreshTokens: async (uid) => { revoked.push(uid); },
});

const call = async (method, path, { body, headers, query } = {}) => {
  let status = 200, payload = null;
  const res = { set() {}, status(s) { status = s; return this; }, json(p) { payload = p; return this; } };
  await api({ method, path: "/api/v1" + path, headers: headers || {}, query: query || {}, body: body || {}, ip: "1.2.3.4" }, res);
  return { status, ...payload };
};
const as = (u, extra) => ({ authorization: "Bearer test:" + u, ...(extra || {}) });

const parcel = { qty: 1, kg: 2, l: 20, w: 20, h: 20 };
const baseOrder = (over) => ({
  customerType: "business", from: "il", to: "de", type: "parcel", parcels: [parcel], selectedOffer: "test:express", signature: "none", step: 3,
  sender: { country: "il", city: "תל אביב", street: "הרצל", house: "1", zip: "6100000", name: "דנה", phone: "0501234567", email: "d@example.com" },
  recipient: { country: "de", city: "Berlin", street: "Strasse", house: "2", zip: "10115", name: "Hans", phone: "+4915112345" },
  ...(over || {}),
});

(async () => {
  /* pricing rule */
  assert.strictEqual(priceOffer({ base: 50, surcharges: [] }, { customerType: "business" }).total, 105);
  assert.strictEqual(priceOffer({ base: 50, surcharges: [] }, { customerType: "private" }).total, 155);

  /* quote: business vs private from the same carrier price */
  let b = await call("POST", "/quote", { body: baseOrder() });
  let p = await call("POST", "/quote", { body: baseOrder({ customerType: "private" }) });
  assert.ok(b.ok && p.ok && b.offers.length === 2);
  assert.ok(Math.abs(p.offers[0].total / b.offers[0].total - 3.1 / 2.1) < 0.01, "private = 3.1x, business = 2.1x of carrier price");
  assert.strictEqual((await call("POST", "/quote", { body: baseOrder({ customerType: "" }) })).status, 400);

  /* remote area changes the price and says why */
  let r = await call("POST", "/quote", { body: { ...baseOrder({ recipient: { country: "de", zip: "99999" } }), selected: "test:express", previousTotal: b.offers[0].total } });
  assert.ok(r.change && r.change.reasons.includes("remote") && r.change.delta > 0, "remote-area change reported");

  /* signature adds a fee */
  let sg = await call("POST", "/quote", { body: { ...baseOrder({ signature: "standard" }), selected: "test:express", previousTotal: b.offers[0].total } });
  assert.ok(sg.change && sg.change.reasons.includes("signature"));
  let sg2 = await call("POST", "/quote", { body: { ...baseOrder({ signature: "standard", recipient: { country: "de", zip: "99999" } }), selected: "test:express", previousTotal: r.offers ? 1 : 1, previousKeys: ["shipping", "remote"] } });
  assert.ok(sg2.change && sg2.change.reasons.length === 1 && sg2.change.reasons[0] === "signature", "only the NEW reason is reported");

  /* guest saves an order, gets id + secret, can resume it, strangers cannot */
  let s1 = await call("POST", "/order/save", { body: baseOrder() });
  assert.ok(s1.ok && /^CT-[A-Z0-9]{6}$/.test(s1.orderId) && s1.token && s1.quote.total > 0);
  assert.strictEqual(s1.status, "draft");
  assert.strictEqual((await call("GET", "/order", { query: { id: s1.orderId }, headers: { "x-order-token": s1.token } })).ok, true);
  assert.strictEqual((await call("GET", "/order", { query: { id: s1.orderId }, headers: { "x-order-token": "nope" } })).status, 404);
  const sub = await call("POST", "/order/save", { headers: { "x-order-token": s1.token }, body: { ...baseOrder(), orderId: s1.orderId, pickup: { date: "2026-10-12" }, declarations: { dangerous: true, terms: true, dims: true }, submit: true } });
  assert.ok(sub.ok && sub.status === "new", JSON.stringify(sub));
  const miss = await call("POST", "/order/save", { headers: { "x-order-token": s1.token }, body: { ...baseOrder(), orderId: s1.orderId, submit: true } });
  assert.strictEqual(miss.status, 400);

  /* no price available -> manual quote */
  const man = await call("POST", "/order/save", { body: baseOrder({ type: "pallet", selectedOffer: null }) });
  assert.ok(man.ok && man.quote && man.quote.manual === true);

  /* back office: first login of the owner becomes admin; others cannot */
  assert.strictEqual((await call("POST", "/admin/bootstrap", { headers: as("emp") })).status, 403);
  assert.ok((await call("POST", "/admin/bootstrap", { headers: as("owner") })).ok);
  /* admin creates an employee (stand-in uid), employee makes a personal code */
  const cr = await call("POST", "/admin/staff/create", { headers: as("owner"), body: { email: "emp@example.com", name: "עובד", password: "Passw0rd!", role: "staff" } });
  assert.ok(cr.ok);
  await store.set("staff/u-emp", { name: "עובד", email: "emp@example.com", role: "staff", active: true, codeKey: "", createdAt: "x" });
  const gen = await call("POST", "/admin/code/generate", { headers: as("emp") });
  assert.ok(gen.ok && /^[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$/.test(gen.code));
  const CODE = gen.code;

  /* code works only for that employee while logged in */
  const hdr = { "x-order-token": s1.token };
  assert.strictEqual((await call("POST", "/promo", { headers: hdr, body: { orderId: s1.orderId, code: CODE } })).status, 400, "no login -> rejected");
  assert.strictEqual((await call("POST", "/promo", { headers: { ...hdr, ...as("cust") }, body: { orderId: s1.orderId, code: CODE } })).status, 400, "other user -> rejected");
  const pr = await call("POST", "/promo", { headers: { ...hdr, ...as("emp") }, body: { orderId: s1.orderId, code: CODE.toLowerCase().replace(/-/g, " ") } });
  assert.ok(pr.ok && pr.overrideToken, JSON.stringify(pr));
  assert.strictEqual((await call("POST", "/order/override", { headers: hdr, body: { orderId: s1.orderId, overrideToken: "x.y", price: 10, reason: "ab" } })).status, 403);
  assert.strictEqual((await call("POST", "/order/override", { headers: hdr, body: { orderId: s1.orderId, overrideToken: pr.overrideToken, price: 10, reason: "" } })).status, 400);
  const ov = await call("POST", "/order/override", { headers: hdr, body: { orderId: s1.orderId, overrideToken: pr.overrideToken, price: 99.5, reason: "הנחה ללקוח קבוע" } });
  assert.ok(ov.ok && ov.quote.total === 99.5);
  assert.ok(Math.abs(ov.quote.lines.reduce((a, l) => a + l.price, 0) - 99.5) < 0.01, "lines add up to the staff price");

  /* THE RULE: the code is nowhere in the database, nor in any response */
  const dump = JSON.stringify(store._dump());
  assert.ok(!dump.includes(CODE) && !dump.includes(CODE.replace(/-/g, "")), "code must never be stored");
  assert.ok(!JSON.stringify([pr, ov, sub, s1]).includes(CODE.replace(/-/g, "")), "code must never be returned");

  /* the order shows who used a code (name), not the code */
  const list = await call("GET", "/admin/orders", { headers: as("owner") });
  const row = list.orders.find((o) => o.id === s1.orderId);
  assert.strictEqual(row.coupon.staffName, "עובד");
  assert.ok(row.quote.cost > 0 && row.quote.profit !== undefined, "admin sees cost and profit");
  const empList = await call("GET", "/admin/orders", { headers: as("emp") });
  assert.strictEqual(empList.orders.find((o) => o.id === s1.orderId).quote.cost, undefined, "employee does not see cost");

  /* re-sending / re-saving the order keeps the staff price only while price inputs are unchanged, never copies a code */
  const re = await call("POST", "/order/save", { headers: hdr, body: { ...baseOrder(), orderId: s1.orderId, code: CODE, promo: CODE } });
  assert.ok(re.ok && re.quote.total === 99.5);
  assert.ok(!JSON.stringify(store._dump()).includes(CODE), "code in request body still not stored");
  const re2 = await call("POST", "/order/save", { headers: hdr, body: { ...baseOrder({ parcels: [{ qty: 1, kg: 9, l: 20, w: 20, h: 20 }] }), orderId: s1.orderId } });
  assert.ok(re2.quote.total !== 99.5, "price recalculated when inputs change");
  const after = await call("GET", "/admin/orders", { headers: as("owner") });
  assert.strictEqual(after.orders.find((o) => o.id === s1.orderId).coupon.superseded, true, "coupon marked as superseded when price recalculated");

  /* wrong codes get rate limited */
  for (let i = 0; i < 8; i++) await call("POST", "/promo", { headers: hdr, body: { orderId: s1.orderId, code: "WRONGCODE" + i } });
  assert.strictEqual((await call("POST", "/promo", { headers: { ...hdr, ...as("emp") }, body: { orderId: s1.orderId, code: CODE } })).status, 429);

  /* revoked code stops working; employees cannot use admin endpoints */
  assert.strictEqual((await call("GET", "/admin/settings", { headers: as("emp") })).status, 403);
  assert.ok((await call("POST", "/admin/code/revoke", { headers: as("owner"), body: { uid: "u-emp" } })).ok);

  /* settings change the markup */
  assert.ok((await call("POST", "/admin/settings", { headers: as("owner"), body: { markupBusinessPct: 50 } })).ok);
  const b2 = await call("POST", "/quote", { body: baseOrder() });
  assert.ok(Math.abs(b2.offers[0].total / b.offers[0].total - 1.5 / 2.1) < 0.01);

  /* first price is based on the main city of each country; the real zip replaces it later */
  const qa = await call("POST", "/quote", { body: baseOrder({ from: "il", to: "us", sender: {}, recipient: {} }) });
  assert.ok(qa.ok && qa.assumed.from === "תל אביב" && qa.assumed.to === "ניו יורק", "main cities assumed when no zip");
  const qb = await call("POST", "/quote", { body: baseOrder({ from: "il", to: "us", sender: { zip: "6100000" }, recipient: { zip: "90210" } }) });
  assert.ok(qb.assumed.from === "" && qb.assumed.to === "", "no assumption when real zips are given");
  const it = await call("POST", "/quote", { body: baseOrder({ from: "il", to: "it", sender: {}, recipient: {} }) });
  assert.ok(!it.offers[0].lines.some((l) => l.key === "remote"), "assumed zip never causes a remote surcharge in test mode");
  assert.strictEqual(Object.keys(require("../lib/defaults").MAIN_CITY).length, 167);

  /* customer account */
  assert.ok((await call("PUT", "/me", { headers: as("cust"), body: { firstName: "דנה", lastName: "כהן", phone: "050", useFor: "business" } })).ok);
  const me = await call("GET", "/me", { headers: as("cust") });
  assert.strictEqual(me.profile.useFor, "business");
  
  /* two servers, one database: the public server has no back-office routes, the back-office server has no customer routes,
     and a staff code made on the back-office side is recognised on the public side */
  const mk = (scope) => createApi({ store, scope, ownerEmail: () => "owner@example.com", verifyIdToken: async (t) => { const u = users[String(t).replace("test:", "")]; if (!u) throw new Error("bad"); return u; }, createAuthUser: async () => "u-x", createCustomToken: async (uid) => "custom:" + uid, revokeRefreshTokens: async (uid) => { revoked.push(uid); } });
  const callOn = async (server, method, path, { body, headers, query } = {}) => { let status = 200, payload = null; const res = { set() {}, status(s) { status = s; return this; }, json(p) { payload = p; return this; } }; await server({ method, path: "/api/v1" + path, headers: headers || {}, query: query || {}, body: body || {}, ip: "9.9.9.9" }, res); return { status, ...payload }; };
  const pub = mk("public"), adm = mk("admin");
  assert.strictEqual((await callOn(pub, "GET", "/admin/orders", { headers: as("owner") })).status, 404, "public server has no admin routes");
  assert.strictEqual((await callOn(adm, "POST", "/quote", { body: baseOrder() })).status, 404, "admin server has no customer routes");
  assert.strictEqual((await callOn(adm, "POST", "/order/save", { body: baseOrder() })).status, 404);
  assert.ok((await callOn(adm, "GET", "/admin/orders", { headers: as("owner") })).ok, "admin server serves the back office");
  const qs = await callOn(pub, "POST", "/quote", { body: baseOrder() }); assert.ok(qs.ok, "public server serves quotes");
  const sv = await callOn(pub, "POST", "/order/save", { body: { ...baseOrder(), submit: true, step: 5, items: [{ desc: "ספרים", value: 40, qty: 1, hs: "", origin: "il", originName: "ישראל" }], pickup: { date: "2099-12-01", time: "morning" }, terms: { incoterm: "DAP", reason: "מכירה" }, declarations: { dangerous: true, terms: true, dims: true } } });
  assert.ok(sv.ok, "order saved on the public server");
  assert.ok((await callOn(adm, "GET", "/admin/orders", { headers: as("owner") })).orders.some((o) => o.id === sv.orderId), "back-office server sees the order saved on the public server");
  const svRow = (await callOn(adm, "GET", "/admin/orders", { headers: as("owner") })).orders.find((o) => o.id === sv.orderId);
  assert.strictEqual(svRow.uid, null, "a guest (not logged in) order has no uid, so the back office can flag it");
  assert.strictEqual(svRow.shipType, null, "shipType defaults to null until staff sets it");
  await callOn(adm, "POST", "/admin/staff/update", { headers: as("owner"), body: { uid: "u-emp", active: true } });
  const gen2 = await callOn(adm, "POST", "/admin/code/generate", { headers: as("emp") });
  assert.ok(gen2.ok, "employee can create a personal code on the back-office server");
  {
    const chk = await callOn(pub, "POST", "/promo", { headers: as("emp", { "x-order-token": sv.token }), body: { orderId: sv.orderId, code: gen2.code } });
    assert.ok(chk.ok && chk.overrideToken, "code created in the back office is recognised on the public server");
    assert.ok(!JSON.stringify(store._dump()).includes(gen2.code), "the code itself is stored nowhere");
  }

  /* ---------- ShippingToGo-style back office ---------- */
  {
    const A = (m, pth, o) => callOn(adm, m, pth, o);
    const qy = (pth, query, who) => { let status = 200, payload = null; const res = { set() {}, status(x) { status = x; return this; }, json(pp) { payload = pp; return this; } }; return adm({ method: "GET", path: "/api/v1" + pth, headers: as(who || "owner"), query, body: {}, ip: "1.1.1.1" }, res).then(() => ({ status, ...payload })); };
    await callOn(pub, "PUT", "/me", { headers: as("cust"), body: { firstName: "דנה", lastName: "כהן", phone: "0501234567", useFor: "business" } });
    const mine = await callOn(pub, "POST", "/order/save", { headers: as("cust"), body: { ...baseOrder(), submit: true, step: 5, pickup: { date: "2099-12-01", time: "morning" }, items: [{ desc: "x", value: 5, qty: 1, hs: "", origin: "il" }], terms: { incoterm: "DAP", reason: "מכירה" }, declarations: { dangerous: true, terms: true, dims: true } } });
    assert.ok(mine.ok);
    const lo = await qy("/admin/list", { m: "orders" });
    assert.ok(lo.ok && lo.rows.some((r) => r.id === mine.orderId && r.userNo >= 1), "orders list has user number");
    const guestRow = lo.rows.find((r) => r.id === sv.orderId);
    assert.strictEqual(guestRow.uid, null, "the orders list exposes uid:null for a guest order, for the back office to highlight");
    const lu = await qy("/admin/list", { m: "users" });
    const cu = lu.rows.find((r) => r.email || r.name === "דנה כהן"); assert.ok(cu && cu.userNo >= 1);
    const uid = lu.rows.find((r) => r.name === "דנה כהן").uid;
    assert.strictEqual((await qy("/admin/search", { by: "userId", q: String(cu.userNo) })).found, true);
    assert.strictEqual((await qy("/admin/search", { by: "pickupId", q: mine.orderId.toLowerCase() })).kind, "order");
    /* money: staff cannot, admin can; payment status follows the ledger */
    assert.strictEqual((await A("POST", "/admin/order/action", { headers: as("emp"), body: { id: mine.orderId, action: "deposit", amount: 10 } })).status, 403);
    const total = (await qy("/admin/order", { id: mine.orderId })).order.quote.total;
    let r1 = await A("POST", "/admin/order/action", { headers: as("owner"), body: { id: mine.orderId, action: "charge_order" } });
    assert.ok(r1.ok && r1.pay.charged === total && r1.pay.status === "unpaid");
    r1 = await A("POST", "/admin/order/action", { headers: as("owner"), body: { id: mine.orderId, action: "deposit", amount: 10 } });
    assert.ok(r1.pay.status === "partial" && r1.receipt.no === 1);
    r1 = await A("POST", "/admin/order/action", { headers: as("owner"), body: { id: mine.orderId, action: "add_money", amount: total - 10 } });
    assert.strictEqual(r1.pay.status, "paid");
    r1 = await A("POST", "/admin/order/action", { headers: as("owner"), body: { id: mine.orderId, action: "additional_charge", amount: 20, note: "remote" } });
    assert.strictEqual(r1.pay.due, 20);
    assert.strictEqual((await A("POST", "/admin/order/action", { headers: as("owner"), body: { id: mine.orderId, action: "deposit", amount: -5 } })).status, 400);
    /* finance panel: admin-only, aggregates revenue (payments received) and refunds from the ledger.
       Uses its own separate order so it doesn't disturb mine.orderId's ledger, which later assertions depend on. */
    assert.strictEqual((await qy("/admin/finance", {}, "emp")).status, 403, "finance panel is admin-only");
    let fin = await qy("/admin/finance", { group: "day" });
    assert.ok(fin.ok && fin.rows.length >= 1 && fin.totals.revenue >= 10, JSON.stringify(fin.totals));
    const revenueBefore = fin.totals.revenue, refundsBefore = fin.totals.refunds;
    const finOrd = await callOn(pub, "POST", "/order/save", { body: baseOrder() });
    await A("POST", "/admin/order/action", { headers: as("owner"), body: { id: finOrd.orderId, action: "refund", amount: 15, method: "bank_transfer" } });
    fin = await qy("/admin/finance", { group: "day" });
    assert.strictEqual(fin.totals.refunds, round2(refundsBefore + 15), "refund shows up in the finance totals");
    assert.strictEqual(fin.totals.revenue, revenueBefore, "a refund does not change revenue (cash already received)");
    /* treatments / Agent Tasks, comments, email queue, whatsapp, docs, label, pickup */
    assert.strictEqual((await A("POST", "/admin/order/action", { headers: as("emp"), body: { id: mine.orderId, action: "treatment_add", type: "nope", text: "x" } })).status, 400, "invalid task type rejected");
    assert.strictEqual((await A("POST", "/admin/order/action", { headers: as("emp"), body: { id: mine.orderId, action: "treatment_add", type: "address", category: "nope", text: "x" } })).status, 400, "invalid category rejected");
    assert.strictEqual((await A("POST", "/admin/order/action", { headers: as("emp"), body: { id: sv.orderId, action: "treatment_add", type: "pickup", category: "operation", text: "x" } })).status, 400, "a task needs a registered user_id - guest orders are rejected");
    assert.strictEqual((await A("POST", "/admin/order/action", { headers: as("emp"), body: { id: mine.orderId, action: "treatment_add", type: "address", category: "operation", userNo: String(cu.userNo + 999), text: "x" } })).status, 400, "user_id must match this pickup's actual customer, not just be non-empty");
    r1 = await A("POST", "/admin/order/action", { headers: as("emp"), body: { id: mine.orderId, action: "treatment_add", type: "address", category: "operation", userNo: String(cu.userNo), text: "Customer asked to change address" } });
    assert.strictEqual(r1.treatments.length, 1);
    assert.strictEqual(r1.treatments[0].type, "address");
    assert.strictEqual(r1.treatments[0].category, "operation");
    assert.strictEqual(r1.treatments[0].uid, uid, "the task records the customer's user_id");
    assert.strictEqual(r1.treatments[0].handledByUid, "u-emp", "a new task defaults handledBy to whoever opened it");
    assert.strictEqual((await qy("/admin/counts", {})).openTreatments, 1);
    const r1b = await A("POST", "/admin/order/action", { headers: as("emp"), body: { id: mine.orderId, action: "treatment_add", type: "security", category: "finance", handledByUid: "u-owner", text: "handled-by set at creation" } });
    assert.strictEqual(r1b.treatments.find((t) => t.text === "handled-by set at creation").handledByUid, "u-owner", "handled-by can be set explicitly at creation, not only by default");
    const reassign = await A("POST", "/admin/order/action", { headers: as("emp"), body: { id: mine.orderId, action: "treatment_reassign", treatmentId: r1.treatments[0].id, handledByUid: "u-owner" } });
    assert.strictEqual(reassign.treatments[0].handledByUid, "u-owner", "reassigned to another staff member");
    const tasksList = await qy("/admin/list", { m: "treatments", type: "address" });
    assert.ok(tasksList.rows.some((t) => t.orderId === mine.orderId && t.handledByName), JSON.stringify(tasksList.rows[0]));
    assert.ok((await qy("/admin/list", { m: "treatments", openedBy: "u-emp" })).rows.some((t) => t.orderId === mine.orderId), "filter by who opened it");
    const closedId = r1.treatments[0].id;
    r1 = await A("POST", "/admin/order/action", { headers: as("emp"), body: { id: mine.orderId, action: "treatment_close", treatmentId: closedId, text: "done" } });
    assert.strictEqual(r1.treatments.find((t) => t.id === closedId).status, "closed");
    assert.ok((await A("POST", "/admin/order/action", { headers: as("emp"), body: { id: mine.orderId, action: "comment", text: "called customer" } })).log.some((l) => l.text === "called customer"));
    r1 = await A("POST", "/admin/order/action", { headers: as("emp"), body: { id: mine.orderId, action: "summary", to: "x@example.com" } });
    assert.ok(r1.outbox.length === 1 && r1.outbox[0].status === "queued");
    assert.strictEqual((await A("POST", "/admin/order/action", { headers: as("emp"), body: { id: mine.orderId, action: "email_user", to: "bad", text: "hi" } })).status, 400);
    assert.ok((await A("POST", "/admin/order/action", { headers: as("emp"), body: { id: mine.orderId, action: "whatsapp", phone: "050-123-4567" } })).url.startsWith("https://wa.me/972501234567"));
    r1 = await A("POST", "/admin/order/action", { headers: as("emp"), body: { id: mine.orderId, action: "doc_add", name: "Packing list", url: "https://example.com/p.pdf" } });
    assert.strictEqual(r1.order.docs.length, 1);
    assert.strictEqual((await A("POST", "/admin/order/action", { headers: as("emp"), body: { id: mine.orderId, action: "doc_add", name: "x", url: "javascript:alert(1)" } })).status, 400);
    r1 = await A("POST", "/admin/order/action", { headers: as("emp"), body: { id: mine.orderId, action: "label", url: "https://example.com/l.pdf", trackingNumber: "794600000001" } });
    assert.strictEqual(r1.order.pickup.trackingNumber, "794600000001");
    { const sh = await qy("/admin/search", { by: "shippingAuthorization", q: "794600000001" }); assert.strictEqual(sh.id, mine.orderId, JSON.stringify(sh)); }
    r1 = await A("POST", "/admin/order/action", { headers: as("emp"), body: { id: mine.orderId, action: "pickup_time", date: "2099-12-05", time: "afternoon" } });
    assert.strictEqual(r1.order.pickup.date, "2099-12-05");
    r1 = await A("POST", "/admin/order/action", { headers: as("emp"), body: { id: mine.orderId, action: "invoice" } });
    const inv = r1.order.invoice.no; r1 = await A("POST", "/admin/order/action", { headers: as("emp"), body: { id: mine.orderId, action: "invoice" } });
    assert.strictEqual(r1.order.invoice.no, inv, "invoice is idempotent");
    /* shipment type: cargo / sea / courier / domestic, set from the back office, filterable in the orders list */
    r1 = await A("POST", "/admin/order/action", { headers: as("emp"), body: { id: mine.orderId, action: "ship_type", shipType: "sea" } });
    assert.strictEqual(r1.order.shipType, "sea");
    assert.strictEqual((await A("POST", "/admin/order/action", { headers: as("emp"), body: { id: mine.orderId, action: "ship_type", shipType: "bogus" } })).status, 400, "only cargo/sea/courier/domestic are accepted");
    assert.ok((await qy("/admin/list", { m: "orders", shipType: "sea" })).rows.some((r) => r.id === mine.orderId), "orders list is filterable by shipType");
    assert.strictEqual((await qy("/admin/list", { m: "orders", shipType: "cargo" })).rows.some((r) => r.id === mine.orderId), false);
    /* user page + reports, manual ledger, agents, messages */
    const up = await qy("/admin/user", { uid });
    assert.ok(up.ok && up.orders.length >= 1 && up.ledger.length >= 4 && up.receipts.length >= 1 && up.documents.length === 1 && up.balance === 20);
    assert.ok((await A("POST", "/admin/user/update", { headers: as("emp"), body: { uid, description: "VIP", phone: "0529999999" } })).user.description === "VIP");
    assert.strictEqual((await A("POST", "/admin/user/update", { headers: as("emp"), body: { uid, blocked: true } })).status, 403);
    /* "log in as this customer": admin-only, never touches the password, and is logged on the customer's own account */
    assert.strictEqual((await A("POST", "/admin/user/impersonate", { headers: as("emp"), body: { uid } })).status, 403, "staff cannot impersonate, admin only");
    const imp = await A("POST", "/admin/user/impersonate", { headers: as("owner"), body: { uid } });
    assert.ok(imp.ok && imp.token === "custom:" + uid);
    assert.strictEqual((await A("POST", "/admin/user/impersonate", { headers: as("owner"), body: { uid: "no-such-uid" } })).status, 404);
    assert.ok((await qy("/admin/user", { uid })).log.some((l) => l.type === "impersonate"), "impersonation is logged on the customer's account");
    /* password reset: any staff can log that a reset link was sent (the e-mail itself is sent client-side, never a password) */
    assert.ok((await A("POST", "/admin/user/reset_password_log", { headers: as("emp"), body: { uid } })).ok);
    assert.strictEqual((await A("POST", "/admin/user/reset_password_log", { headers: as("owner"), body: { uid: "no-such-uid" } })).status, 404);
    assert.ok((await qy("/admin/user", { uid })).log.some((l) => l.type === "reset_password"), "password reset is logged on the customer's account");
    /* the extra ShippingToGo-style profile fields: stored and returned, with basic validation on the numeric ones */
    const updWide = await A("POST", "/admin/user/update", { headers: as("emp"), body: { uid, company: "Acme", country: "il", city: "Tel Aviv", brand: "shippingtogo", discountPct: 30, debtAmountLimit: 5000, isActive: "no", userType: "Agency" } });
    assert.ok(updWide.ok && updWide.user.company === "Acme" && updWide.user.discountPct === 30 && updWide.user.isActive === "no" && updWide.user.userType === "Agency");
    /* the log says exactly what changed (old -> new), not just a dump of every submitted field name */
    assert.ok(updWide.log[0].text.indexOf("Company: - → Acme") > -1 && updWide.log[0].text.indexOf("Phone") === -1, updWide.log[0].text);
    const logCountBefore = updWide.log.length;
    const noOp = await A("POST", "/admin/user/update", { headers: as("emp"), body: { uid, company: "Acme", country: "il", city: "Tel Aviv", brand: "shippingtogo", discountPct: 30, debtAmountLimit: 5000, isActive: "no", userType: "Agency" } });
    assert.strictEqual(noOp.log.length, logCountBefore, "saving unchanged values does not add a new log entry");
    const oneField = await A("POST", "/admin/user/update", { headers: as("emp"), body: { uid, company: "Acme", country: "il", city: "Tel Aviv", brand: "shippingtogo", discountPct: 30, debtAmountLimit: 5000, isActive: "no", userType: "Agency", phone: "0501112222" } });
    assert.strictEqual(oneField.log[0].text, "User details updated: Phone: 0529999999 → 0501112222", "only the field that actually changed is named in the log");
    assert.strictEqual((await A("POST", "/admin/user/update", { headers: as("emp"), body: { uid, discountPct: 200 } })).status, 400, "discount must be 0-100");
    /* manual log note via the "Add" link under Log */
    const noteRes = await A("POST", "/admin/user/log/add", { headers: as("emp"), body: { uid, text: "Called customer about a doc" } });
    assert.ok(noteRes.ok && noteRes.log.some((l) => l.text === "Called customer about a doc" && l.type === "note"));
    assert.strictEqual((await A("POST", "/admin/user/log/add", { headers: as("emp"), body: { uid, text: "" } })).status, 400, "empty note rejected");
    assert.ok((await A("POST", "/admin/ledger/add", { headers: as("owner"), body: { uid, kind: "credit", amount: 20, method: "bank_transfer" } })).receipt.no >= 2);
    assert.strictEqual((await qy("/admin/user", { uid })).balance, 0);
    const ag = await A("POST", "/admin/agent/save", { headers: as("owner"), body: { name: "FedEx IL", kind: "carrier", email: "ops@fedex.example" } });
    assert.ok(ag.ok); assert.strictEqual((await qy("/admin/list", { m: "agents" })).rows.length, 1);
    r1 = await A("POST", "/admin/order/action", { headers: as("emp"), body: { id: mine.orderId, action: "email_agent", agentId: ag.id, text: "pls pickup" } });
    assert.ok(r1.outbox.some((m) => m.to === "ops@fedex.example"));
    await store.add("leads", { name: "Lead", phone: "05", service: "x", route: "r", cargo: "c", status: "new", createdAt: "2026-10-01T00:00:00Z" });
    const ms = await qy("/admin/list", { m: "messages" }); assert.strictEqual(ms.rows.length, 1);
    assert.ok((await A("POST", "/admin/message/update", { headers: as("emp"), body: { id: ms.rows[0].id, status: "done" } })).ok);
    const pay = await qy("/admin/list", { m: "payments", pay: "partial" }); assert.ok(pay.rows.length >= 1 && pay.totals.paid > 0);
    assert.ok((await qy("/admin/list", { m: "ledger" })).totals.credit > 0);
    assert.strictEqual((await qy("/admin/list", { m: "receipts" })).rows.length >= 3, true);
    assert.strictEqual((await qy("/admin/list", { m: "nope" })).status, 400);
    assert.strictEqual((await callOn(pub, "GET", "/admin/list", { headers: as("owner") })).status, 404);
    assert.strictEqual((await qy("/admin/list", { m: "orders" }, "cust")).status, 403, "customers cannot use the back office");

    /* coupons: admin-only to create/cancel, percent discount, time-boxed, "once" binds to the first redeemer */
    assert.strictEqual((await A("POST", "/admin/coupon/create", { headers: as("emp"), body: { pct: 10, usageType: "once", validTo: "2099-01-01" } })).status, 403, "staff cannot create coupons, admin only");
    const badPct = await A("POST", "/admin/coupon/create", { headers: as("owner"), body: { pct: 150, usageType: "once", validTo: "2099-01-01" } });
    assert.strictEqual(badPct.status, 400, "percentage must be 0-100");
    const cp = await A("POST", "/admin/coupon/create", { headers: as("owner"), body: { pct: 15, usageType: "once", validTo: "2099-01-01", code: "WELCOME15", note: "First order" } });
    assert.ok(cp.ok && cp.coupon.code === "WELCOME15" && cp.coupon.status === "active");
    assert.strictEqual((await A("POST", "/admin/coupon/create", { headers: as("owner"), body: { pct: 5, usageType: "once", validTo: "2099-01-01", code: "welcome15" } })).status, 400, "duplicate code (case-insensitive) rejected");
    /* a customer redeems it on the public site */
    assert.strictEqual((await callOn(pub, "POST", "/coupon/redeem", { headers: as("cust"), body: { code: "nope-no-such-code" } })).status, 400);
    const redeemed = await callOn(pub, "POST", "/coupon/redeem", { headers: as("cust"), body: { code: "welcome15" } });
    assert.ok(redeemed.ok && redeemed.pct === 15, JSON.stringify(redeemed));
    /* the Users list shows who issued the coupon and the discount it carries, for anyone who registered with one */
    const custRow = (await qy("/admin/list", { m: "users" })).rows.find((r) => r.uid === "u-cust");
    assert.ok(custRow && custRow.coupon && custRow.coupon.code === "WELCOME15" && custRow.coupon.pct === 15 && custRow.coupon.by, JSON.stringify(custRow));
    /* a "once" coupon cannot be redeemed again, including by the same customer */
    assert.strictEqual((await callOn(pub, "POST", "/coupon/redeem", { headers: as("cust"), body: { code: "WELCOME15" } })).status, 400, "once-coupon already used");
    const cpList = await qy("/admin/list", { m: "coupons" });
    assert.strictEqual(cpList.rows.find((r) => r.code === "WELCOME15").status, "used");
    /* admin cancels a still-active coupon */
    const cp2 = await A("POST", "/admin/coupon/create", { headers: as("owner"), body: { pct: 20, usageType: "multi", validTo: "2099-01-01", code: "SUMMER20" } });
    assert.ok((await A("POST", "/admin/coupon/cancel", { headers: as("emp"), body: { id: cp2.coupon.id } })).status === 403, "staff cannot cancel either");
    assert.ok((await A("POST", "/admin/coupon/cancel", { headers: as("owner"), body: { id: cp2.coupon.id } })).ok);
    assert.strictEqual((await callOn(pub, "POST", "/coupon/redeem", { headers: as("cust"), body: { code: "SUMMER20" } })).status, 400, "cancelled coupon cannot be redeemed");
    /* admin can reactivate a cancelled coupon */
    assert.strictEqual((await A("POST", "/admin/coupon/reactivate", { headers: as("emp"), body: { id: cp2.coupon.id } })).status, 403, "staff cannot reactivate either");
    assert.strictEqual((await A("POST", "/admin/coupon/reactivate", { headers: as("owner"), body: { id: "no-such-id" } })).status, 404);
    assert.strictEqual((await A("POST", "/admin/coupon/reactivate", { headers: as("owner"), body: { id: cp.coupon.id } })).status, 400, "cannot reactivate a coupon that isn't cancelled");
    assert.ok((await A("POST", "/admin/coupon/reactivate", { headers: as("owner"), body: { id: cp2.coupon.id } })).ok);
    assert.strictEqual((await qy("/admin/list", { m: "coupons" })).rows.find((r) => r.code === "SUMMER20").status, "active", "reactivated coupon is active again");
    assert.ok((await callOn(pub, "POST", "/coupon/redeem", { headers: as("cust"), body: { code: "SUMMER20" } })).ok, "reactivated coupon can be redeemed again");
    /* price lists: admin-only CSV-parsed rate cards, stored for visibility/management; the built-in FedEx
       tables already wired into real quotes show up read-only alongside anything an admin uploads */
    assert.strictEqual((await A("GET", "/admin/pricelist/list", { headers: as("emp") })).status, 403, "staff cannot see price lists, admin only");
    const pl0 = await A("GET", "/admin/pricelist/list", { headers: as("owner") });
    assert.ok(pl0.ok && pl0.lists.length === 4 && pl0.lists.every((l) => l.builtin), "the 4 built-in FedEx tables are listed");
    const plBuiltin = await qy("/admin/pricelist", { key: "fedex_priorityFreight" });
    assert.ok(plBuiltin.ok && plBuiltin.pricelist.builtin && plBuiltin.pricelist.catalog === "fedex_shipping");
    assert.strictEqual(plBuiltin.pricelist.headers[0], "kg");
    const caRow = plBuiltin.pricelist.rows.find((r) => r[0] === 70);
    assert.strictEqual(caRow[plBuiltin.pricelist.headers.indexOf("A")], 1038.69, "a built-in price list's actual numbers can be fetched/viewed, matching the real rate card");
    assert.strictEqual((await A("POST", "/admin/pricelist/save", { headers: as("emp"), body: { key: "dhl_priority", label: "DHL Priority", headers: ["kg", "A"], rows: [[1, 10]] } })).status, 403, "staff cannot upload a price list, admin only");
    assert.strictEqual((await A("POST", "/admin/pricelist/save", { headers: as("owner"), body: { key: "Bad Key!", label: "x", headers: ["kg", "A"], rows: [[1, 10]] } })).status, 400, "invalid key rejected");
    assert.strictEqual((await A("POST", "/admin/pricelist/save", { headers: as("owner"), body: { key: "dhl_priority", label: "DHL Priority", headers: ["kg"], rows: [[1]] } })).status, 400, "needs at least two columns");
    assert.strictEqual((await A("POST", "/admin/pricelist/save", { headers: as("owner"), body: { key: "dhl_priority", label: "DHL Priority", headers: ["kg", "A", "B"], rows: [[1, 10]] } })).status, 400, "row/column mismatch rejected");
    const plSave = await A("POST", "/admin/pricelist/save", { headers: as("owner"), body: { key: "dhl_priority", label: "DHL Priority", headers: ["kg", "A", "B"], rows: [[1, 10, 12], [2, "", 20]] } });
    assert.ok(plSave.ok && plSave.key === "dhl_priority");
    const pl1 = await A("GET", "/admin/pricelist/list", { headers: as("owner") });
    assert.strictEqual(pl1.lists.length, 5, "built-ins plus the new upload");
    const uploaded1 = pl1.lists.find((l) => l.key === "dhl_priority");
    assert.ok(uploaded1 && !uploaded1.builtin && uploaded1.rowCount === 2 && uploaded1.colCount === 2);
    const plGet = await qy("/admin/pricelist", { key: "dhl_priority" });
    assert.ok(plGet.ok && plGet.pricelist.rows[0][2] === 12 && plGet.pricelist.rows[1][1] === null, "blank cell stored as null, not 0");
    const plResave = await A("POST", "/admin/pricelist/save", { headers: as("owner"), body: { key: "dhl_priority", label: "DHL Priority v2", headers: ["kg", "A", "B"], rows: [[1, 11, 13]] } });
    assert.ok(plResave.ok);
    assert.strictEqual((await qy("/admin/pricelist", { key: "dhl_priority" })).pricelist.label, "DHL Priority v2", "re-saving the same key upserts (replaces), doesn't duplicate");
    assert.strictEqual((await A("POST", "/admin/pricelist/delete", { headers: as("emp"), body: { key: "dhl_priority" } })).status, 403, "staff cannot delete a price list, admin only");
    assert.strictEqual((await A("POST", "/admin/pricelist/delete", { headers: as("owner"), body: { key: "no-such-key" } })).status, 404);
    assert.ok((await A("POST", "/admin/pricelist/delete", { headers: as("owner"), body: { key: "dhl_priority" } })).ok);
    assert.strictEqual((await A("GET", "/admin/pricelist/list", { headers: as("owner") })).lists.length, 4, "back to just the built-ins after delete");
    /* banners: admin builds them in the back office, the public site shows them with no auth required */
    assert.strictEqual((await A("POST", "/admin/banner/save", { headers: as("emp"), body: { title: "x", body: "y" } })).status, 403, "staff cannot create a banner, admin only");
    assert.strictEqual((await callOn(pub, "GET", "/banners/active")).banner, null, "nothing active yet");
    const bn1 = await A("POST", "/admin/banner/save", { headers: as("owner"), body: { title: "10% on your first order", body: "Sign up today", ctaText: "Sign up", ctaType: "link", ctaValue: "/signup.html", template: "center", anim: "fade-up", page: "all", delaySec: 3, frequency: "once", enabled: true } });
    assert.ok(bn1.ok && bn1.id);
    const act1 = await callOn(pub, "GET", "/banners/active");
    assert.ok(act1.ok && act1.banner && act1.banner.id === bn1.id && act1.banner.title === "10% on your first order");
    assert.strictEqual(act1.banner.shows, undefined, "internal stats are never sent to the public site");
    /* a "home" page banner outranks an "all pages" one when both qualify */
    const bn2 = await A("POST", "/admin/banner/save", { headers: as("owner"), body: { title: "Home only", body: "x", template: "bottom", anim: "scale", page: "home", enabled: true } });
    const actHome = await callOn(pub, "GET", "/banners/active", { query: { page: "home" } });
    assert.strictEqual(actHome.banner && actHome.banner.id, bn2.id, "a page-specific banner wins over a generic one on that page");
    const actAllPages = await callOn(pub, "GET", "/banners/active", { query: { page: "all" } });
    assert.strictEqual(actAllPages.banner && actAllPages.banner.id, bn1.id, "elsewhere, only the all-pages banner qualifies");
    /* disabled or outside its active date range never shows */
    assert.ok((await A("POST", "/admin/banner/save", { headers: as("owner"), body: { id: bn2.id, title: "Home only", body: "x", template: "bottom", anim: "scale", page: "home", enabled: false } })).ok);
    assert.strictEqual((await callOn(pub, "GET", "/banners/active", { query: { page: "home" } })).banner.id, bn1.id, "disabled banner no longer shows; falls back to the all-pages one");
    assert.ok((await A("POST", "/admin/banner/save", { headers: as("owner"), body: { title: "Future sale", body: "x", template: "center", anim: "fade-up", page: "all", activeFrom: "2099-01-01", enabled: true } })).ok);
    assert.strictEqual((await callOn(pub, "GET", "/banners/active")).banner.id, bn1.id, "a banner scheduled for the future doesn't show yet");
    /* show/click/dismiss events */
    assert.ok((await callOn(pub, "POST", "/banners/event", { body: { id: bn1.id, kind: "show" } })).ok);
    assert.ok((await callOn(pub, "POST", "/banners/event", { body: { id: bn1.id, kind: "click" } })).ok);
    assert.ok((await callOn(pub, "POST", "/banners/event", { body: { id: bn1.id, kind: "dismiss" } })).ok);
    assert.strictEqual((await callOn(pub, "POST", "/banners/event", { body: { id: bn1.id, kind: "bogus" } })).status, 400);
    assert.ok((await callOn(pub, "POST", "/banners/event", { body: { id: "no-such-id", kind: "show" } })).ok, "an already-deleted popup's stray event is ignored, not an error");
    const pl = await A("GET", "/admin/banner/list", { headers: as("owner") });
    const bn1row = pl.banners.find((p) => p.id === bn1.id);
    assert.ok(bn1row.shows === 1 && bn1row.clicks === 1 && bn1row.dismisses === 1, "admin sees the real counts");
    assert.strictEqual((await A("POST", "/admin/banner/delete", { headers: as("emp"), body: { id: bn1.id } })).status, 403, "staff cannot delete a banner, admin only");
    assert.ok((await A("POST", "/admin/banner/delete", { headers: as("owner"), body: { id: bn1.id } })).ok);
    assert.strictEqual((await A("POST", "/admin/banner/delete", { headers: as("owner"), body: { id: bn1.id } })).status, 404);
    /* staff names for the "handled by" picker: any logged-in staff can read it, includes inactive/past staff */
    await A("POST", "/admin/staff/update", { headers: as("owner"), body: { uid: "u-emp", active: false } });
    const names = await A("GET", "/admin/staff/names", { headers: as("owner") });
    assert.ok(names.ok && names.staff.some((s) => s.uid === "u-emp" && s.active === false), "inactive staff still listed");
    await A("POST", "/admin/staff/update", { headers: as("owner"), body: { uid: "u-emp", active: true } });
    /* "sign out everywhere": any staff member can do it to themselves; a non-admin cannot do it to someone else */
    assert.ok((await A("POST", "/admin/staff/signout", { headers: as("emp"), body: {} })).ok, "any staff can sign themselves out everywhere");
    assert.ok(revoked.includes("u-emp"));
    assert.strictEqual((await A("POST", "/admin/staff/signout", { headers: as("emp"), body: { uid: "u-owner" } })).status, 403, "non-admin staff cannot sign out someone else");
    /* the account-owner's staff record can't be disabled or demoted by ANY admin, not even another admin - only self-protection existed before */
    await A("POST", "/admin/staff/update", { headers: as("owner"), body: { uid: "u-emp", role: "admin" } });
    assert.strictEqual((await A("POST", "/admin/staff/signout", { headers: as("emp"), body: { uid: "u-owner" } })).status, 400, "another admin cannot sign out the account owner either");
    assert.ok((await A("POST", "/admin/staff/signout", { headers: as("owner"), body: { uid: "u-owner" } })).ok, "the owner can sign themselves out");
    assert.ok(revoked.includes("u-owner"));
    assert.strictEqual((await A("POST", "/admin/staff/update", { headers: as("emp"), body: { uid: "u-owner", active: false } })).status, 400, "another admin cannot disable the owner account");
    assert.strictEqual((await A("POST", "/admin/staff/update", { headers: as("emp"), body: { uid: "u-owner", role: "staff" } })).status, 400, "another admin cannot demote the owner account");
    assert.ok((await store.get("staff/u-owner")).active !== false, "owner stayed active");
    await A("POST", "/admin/staff/update", { headers: as("owner"), body: { uid: "u-emp", role: "staff" } });
    /* standalone Agent Tasks: a task needs at least a pickup OR a customer, not necessarily both */
    assert.strictEqual((await A("POST", "/admin/task/create", { headers: as("emp"), body: { type: "address", category: "operation", text: "x" } })).status, 400, "neither pickup nor user given");
    const taskByUserOnly = await A("POST", "/admin/task/create", { headers: as("emp"), body: { type: "address", category: "finance", uid, text: "Needs a balance recharge, not tied to a shipment" } });
    assert.ok(taskByUserOnly.ok && !taskByUserOnly.task.orderId, "a user-only task has no pickup");
    const taskByPickupOnly = await A("POST", "/admin/task/create", { headers: as("emp"), body: { type: "security", category: "operation", orderId: mine.orderId, text: "x" } });
    assert.ok(taskByPickupOnly.ok && taskByPickupOnly.task.uid === "u-cust", "pickup-only task still resolves the customer from the order");
    assert.strictEqual((await A("POST", "/admin/task/create", { headers: as("emp"), body: { type: "address", category: "operation", orderId: mine.orderId, uid: "u-owner", text: "x" } })).status, 400, "mismatched pickup and user rejected");
    const closeRes = await A("POST", "/admin/task/close", { headers: as("emp"), body: { treatmentId: taskByUserOnly.task.id, text: "handled" } });
    assert.ok(closeRes.ok);
    assert.strictEqual((await store.get("treatments/" + taskByUserOnly.task.id)).status, "closed");
    const reassignRes = await A("POST", "/admin/task/reassign", { headers: as("emp"), body: { treatmentId: taskByPickupOnly.task.id, handledByUid: "u-owner" } });
    assert.ok(reassignRes.ok);
    assert.strictEqual((await store.get("treatments/" + taskByPickupOnly.task.id)).handledByUid, "u-owner");
    const uOnlyRow = (await qy("/admin/list", { m: "treatments" })).rows.find((r) => r.id === taskByUserOnly.task.id);
    assert.ok(uOnlyRow && uOnlyRow.userNo === cu.userNo, "a user-only task still shows the right user in the list");
    /* task detail view: AWB and a running log of free-text updates (not just a one-time close result) */
    const tg1 = await qy("/admin/task", { id: taskByPickupOnly.task.id });
    assert.ok(tg1.ok && tg1.task.id === taskByPickupOnly.task.id && Array.isArray(tg1.log));
    assert.ok(tg1.log.some((l) => l.text.indexOf("Task opened") === 0), "creation shows up in the task's own log");
    assert.ok((await A("POST", "/admin/task/update", { headers: as("emp"), body: { treatmentId: taskByPickupOnly.task.id, awb: "AWB-12345" } })).ok);
    assert.ok((await A("POST", "/admin/task/update", { headers: as("emp"), body: { treatmentId: taskByPickupOnly.task.id, text: "Called the carrier, waiting on their reply" } })).ok);
    assert.strictEqual((await A("POST", "/admin/task/update", { headers: as("emp"), body: { treatmentId: taskByPickupOnly.task.id } })).status, 400, "nothing to update rejected");
    const tg2 = await qy("/admin/task", { id: taskByPickupOnly.task.id });
    assert.strictEqual(tg2.task.awb, "AWB-12345");
    assert.ok(tg2.log.some((l) => l.text === "Called the carrier, waiting on their reply"), "free-text update added to the open task's log");
    assert.strictEqual(tg2.log.length, tg1.log.length + 1, "only the text update added a log line, not the AWB-only save");
    assert.ok((await A("POST", "/admin/task/update", { headers: as("emp"), body: { treatmentId: taskByPickupOnly.task.id, desc: "Updated treatment description" } })).ok);
    assert.strictEqual((await A("POST", "/admin/task/update", { headers: as("emp"), body: { treatmentId: taskByPickupOnly.task.id, desc: "" } })).status, 400, "empty description rejected");
    const tg3 = await qy("/admin/task", { id: taskByPickupOnly.task.id });
    assert.strictEqual(tg3.task.text, "Updated treatment description", "treatment description is editable");
    assert.strictEqual(tg3.log.length, tg2.log.length, "editing the description alone does not add a log line");
    /* real FedEx international rates (the carrier's own price lists) take over from the test provider once
       the owner turns test mode off in Settings; above 68kg a parcel becomes freight - same carrier, different table */
    assert.ok((await A("POST", "/admin/settings", { headers: as("owner"), body: { testMode: false, markupBusinessPct: 110, markupPrivatePct: 210 } })).ok);
    const fx1 = await callOn(pub, "POST", "/quote", { body: baseOrder({ to: "ca", parcels: [{ qty: 1, kg: 2, l: 20, w: 20, h: 20 }] }) });
    assert.ok(fx1.ok && fx1.offers.length === 2 && fx1.offers.every((o) => o.carrier === "FedEx"), "fedex priority+economy replace the test provider once testMode is off");
    const fx1p = fx1.offers.find((o) => o.id === "fedex:priority");
    assert.strictEqual(fx1p.service, "Priority");
    assert.ok(Math.abs(fx1p.total - round2(37.7 * 2.1)) < 0.01, "priced from the real FedEx Priority rate card, zone A (Canada) at 2kg");
    const fx2 = await callOn(pub, "POST", "/quote", { body: baseOrder({ to: "ca", parcels: [{ qty: 1, kg: 68, l: 10, w: 10, h: 10 }] }) });
    const fx2p = fx2.offers.find((o) => o.id === "fedex:priority");
    assert.strictEqual(fx2p.service, "Priority", "68kg exactly still prices as a parcel");
    assert.ok(Math.abs(fx2p.total - round2(934.09 * 2.1)) < 0.01);
    const fx3 = await callOn(pub, "POST", "/quote", { body: baseOrder({ to: "ca", parcels: [{ qty: 1, kg: 68.5, l: 10, w: 10, h: 10 }] }) });
    const fx3p = fx3.offers.find((o) => o.id === "fedex:priority");
    assert.strictEqual(fx3p.service, "Priority Freight", "just over 68kg switches to freight pricing");
    assert.ok(Math.abs(fx3p.total - round2(1038.69 * 2.1)) < 0.01, "freight rounds up to the 70kg bracket, not a pro-rated 68.5kg");
    const fx4 = await callOn(pub, "POST", "/quote", { body: baseOrder({ to: "zz", parcels: [{ qty: 1, kg: 2, l: 10, w: 10, h: 10 }] }) });
    assert.ok(fx4.ok && fx4.offers.length === 0, "a destination with no FedEx zone mapping gets no FedEx offer - falls back to a manual quote");
    /* an envelope/document always prices at the 0.5kg bracket, same as the test provider already did */
    const fx5 = await callOn(pub, "POST", "/quote", { body: baseOrder({ to: "ca", type: "doc", parcels: [{ qty: 1, kg: 0.5, l: 2, w: 2, h: 2 }] }) });
    const fx5p = fx5.offers.find((o) => o.id === "fedex:priority");
    assert.ok(fx5p, "a document/envelope also gets a real FedEx offer, not just the test provider");
    assert.ok(Math.abs(fx5p.total - round2(28.28 * 2.1)) < 0.01, "priced at the 0.5kg bracket, zone A (Canada)");
    /* a per-customer discount (set on their profile, User Details) applies automatically on top of the normal
       markup; the site shows both the pre-discount and the final price so the saving is visible */
    assert.ok((await A("POST", "/admin/user/update", { headers: as("owner"), body: { uid, discountPct: 0 } })).ok);
    const fxNoDisc = await callOn(pub, "POST", "/quote", { headers: as("cust"), body: baseOrder({ to: "ca", parcels: [{ qty: 1, kg: 2, l: 20, w: 20, h: 20 }] }) });
    const fxNoDiscP = fxNoDisc.offers.find((o) => o.id === "fedex:priority");
    assert.strictEqual(fxNoDiscP.originalTotal, null, "no discount on the customer's profile -> no struck-through price");
    assert.ok((await A("POST", "/admin/user/update", { headers: as("owner"), body: { uid, discountPct: 20 } })).ok);
    const fxDisc = await callOn(pub, "POST", "/quote", { headers: as("cust"), body: baseOrder({ to: "ca", parcels: [{ qty: 1, kg: 2, l: 20, w: 20, h: 20 }] }) });
    const fxDiscP = fxDisc.offers.find((o) => o.id === "fedex:priority");
    assert.ok(Math.abs(fxDiscP.originalTotal - round2(37.7 * 2.1)) < 0.01, "originalTotal is the normal (pre-discount) price");
    assert.ok(Math.abs(fxDiscP.total - round2(fxDiscP.originalTotal * 0.8)) < 0.01, "total is 20% off the original");
    const fxDiscGuest = await callOn(pub, "POST", "/quote", { body: baseOrder({ to: "ca", parcels: [{ qty: 1, kg: 2, l: 20, w: 20, h: 20 }] }) });
    assert.strictEqual(fxDiscGuest.offers.find((o) => o.id === "fedex:priority").originalTotal, null, "a guest (not logged in as this customer) never gets their discount");
    const fxOrderDisc = await callOn(pub, "POST", "/order/save", { headers: as("cust"), body: { ...baseOrder({ to: "ca", parcels: [{ qty: 1, kg: 2, l: 20, w: 20, h: 20 }], selectedOffer: "fedex:priority" }), submit: true, step: 5, pickup: { date: "2099-12-01", time: "morning" }, items: [{ desc: "x", value: 5, qty: 1, hs: "", origin: "il" }], terms: { incoterm: "DAP", reason: "מכירה" }, declarations: { dangerous: true, terms: true, dims: true } } });
    assert.ok(fxOrderDisc.ok && Math.abs(fxOrderDisc.quote.total - round2(fxDiscP.originalTotal * 0.8)) < 0.01, "the discount also applies when the order is actually saved, not just the live preview");
    const adminViewDisc = await qy("/admin/order", { id: fxOrderDisc.orderId });
    assert.strictEqual(adminViewDisc.order.quote.customerDiscountPct, 20, "admin can see this was an automatic customer discount, not a manual override");
    assert.ok((await A("POST", "/admin/user/update", { headers: as("owner"), body: { uid, discountPct: 0 } })).ok);
    /* actual weight at pickup can differ from the customer's declared weight; recording it recalculates the
       price from the same carrier/service's rate card at the new weight (same "actual_weight" action as before) */
    const fxOrder = await callOn(pub, "POST", "/order/save", { body: { ...baseOrder({ to: "ca", parcels: [{ qty: 1, kg: 2, l: 20, w: 20, h: 20 }], selectedOffer: "fedex:priority" }), submit: true, step: 5, pickup: { date: "2099-12-01", time: "morning" }, items: [{ desc: "x", value: 5, qty: 1, hs: "", origin: "il" }], terms: { incoterm: "DAP", reason: "מכירה" }, declarations: { dangerous: true, terms: true, dims: true } } });
    assert.ok(fxOrder.ok && fxOrder.quote && fxOrder.quote.carrier === "FedEx", "order saved with the real FedEx offer selected");
    const aw1 = await A("POST", "/admin/order/action", { headers: as("owner"), body: { id: fxOrder.orderId, action: "actual_weight", kg: 68.5 } });
    assert.ok(aw1.ok && aw1.order.actualKg === 68.5);
    assert.ok(Math.abs(aw1.order.quote.cost - 1038.69) < 0.01, "actual weight crossing 68kg recalculates cost from the Freight table");
    assert.strictEqual(aw1.order.quote.service, "Priority Freight");
    /* a per-shipment commission/discount override (admin only), recomputed on top of the same rate */
    assert.strictEqual((await A("POST", "/admin/order/action", { headers: as("emp"), body: { id: fxOrder.orderId, action: "pricing_override", commissionPctOverride: 50, discountPct: 10 } })).status, 403, "staff cannot set a pricing override, admin only");
    const po1 = await A("POST", "/admin/order/action", { headers: as("owner"), body: { id: fxOrder.orderId, action: "pricing_override", commissionPctOverride: 50, discountPct: 10 } });
    assert.ok(po1.ok && po1.order.commissionPctOverride === 50 && po1.order.discountPct === 10);
    const expected = round2(round2(1038.69 * 1.5) * 0.9);
    assert.ok(Math.abs(po1.order.quote.total - expected) < 0.01, "total reflects the per-shipment 50% commission and 10% discount, not the global markup");
    await A("POST", "/admin/settings", { headers: as("owner"), body: { testMode: true, markupBusinessPct: 50 } });
  }
  console.log("ALL TESTS PASSED");
})().catch((e) => { console.error("FAIL:", e.message); process.exit(1); });
