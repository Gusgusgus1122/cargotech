"use strict";
/* Cleans everything that comes from a browser. Never trust the client. */
const cut = (v, n) => String(v == null ? "" : v).replace(/[\u0000-\u001f\u007f]/g, " ").trim().slice(0, n);
const num = (v, min, max, d = 0) => { const x = Number(v); return Number.isFinite(x) ? Math.min(Math.max(x, min), max) : d; };
const oneOf = (v, list, d) => (list.includes(v) ? v : d);
const cc = (v) => { const s = cut(v, 2).toLowerCase(); return /^[a-z]{2}$/.test(s) ? s : ""; };

function addr(a) {
  a = a || {};
  return {
    country: cc(a.country), city: cut(a.city, 60), state: cut(a.state, 40), street: cut(a.street, 35), house: cut(a.house, 12),
    zip: cut(a.zip, 12), details: cut(a.details, 35), name: cut(a.name, 60), company: cut(a.company, 35),
    email: cut(a.email, 80).toLowerCase(), phone: cut(a.phone, 30), residential: a.residential === true,
  };
}

const TYPES = ["parcel", "doc", "pallet", "cont"];

function route(b) {
  return { mode: oneOf(b.mode, ["intl"], "intl"), from: cc(b.from), to: cc(b.to), type: oneOf(b.type, TYPES, "parcel") };
}

function parcels(list, type) {
  const arr = (Array.isArray(list) ? list : []).slice(0, 20).map((p) => ({
    qty: Math.round(num(p && p.qty, 1, 999, 1)), kg: num(p && p.kg, 0, 5000, 0),
    l: num(p && p.l, 0, 1000, 0), w: num(p && p.w, 0, 1000, 0), h: num(p && p.h, 0, 1000, 0),
  }));
  return arr.length ? arr : [{ qty: 1, kg: 0, l: 0, w: 0, h: 0 }];
}

function items(list) {
  return (Array.isArray(list) ? list : []).slice(0, 100).map((i) => ({
    desc: cut(i && i.desc, 200), value: num(i && i.value, 0, 10000000, 0), currency: oneOf(i && i.currency, ["USD", "EUR", "ILS", "GBP"], "USD"),
    qty: Math.round(num(i && i.qty, 1, 100000, 1)), hs: cut(i && i.hs, 20), origin: cc(i && i.origin), madeOf: cut(i && i.madeOf, 80),
  }));
}

function order(b) {
  b = b && typeof b === "object" ? b : {};
  const r = route(b);
  const sender = addr(b.sender), recipient = addr(b.recipient);
  sender.country = sender.country || r.from; recipient.country = recipient.country || r.to;
  return {
    customerType: oneOf(b.customerType, ["private", "business"], ""),
    ...r,
    parcels: parcels(b.parcels, r.type),
    cont: { size: cut(b.cont && b.cont.size, 60), qty: Math.round(num(b.cont && b.cont.qty, 1, 999, 1)) },
    selectedOffer: cut(b.selectedOffer, 40) || null,
    signature: oneOf(b.signature, ["none", "standard", "adult"], "none"),
    sender, recipient,
    items: items(b.items),
    insurance: { requested: !!(b.insurance && b.insurance.requested), amount: num(b.insurance && b.insurance.amount, 0, 10000000, 0) },
    pickup: { date: /^\d{4}-\d{2}-\d{2}$/.test(cut(b.pickup && b.pickup.date, 10)) ? b.pickup.date : "", time: cut(b.pickup && b.pickup.time, 20) },
    terms: {
      incoterm: oneOf(b.terms && b.terms.incoterm, ["", "DAP", "DDP", "EXW"], ""), vat: cut(b.terms && b.terms.vat, 30),
      reason: cut(b.terms && b.terms.reason, 40), shortDesc: cut(b.terms && b.terms.shortDesc, 120),
    },
    declarations: { dangerous: !!(b.declarations && b.declarations.dangerous), terms: !!(b.declarations && b.declarations.terms), dims: !!(b.declarations && b.declarations.dims) },
    step: Math.round(num(b.step, 1, 6, 1)),
  };
}

/* Required before the order can be submitted. Returns a list of Hebrew messages. */
function missingForSubmit(o) {
  const e = [];
  if (!o.customerType) e.push("בחרו אם השולח פרטי או עסקי.");
  if (!o.from || !o.to) e.push("חסרים מדינת מוצא או יעד.");
  if (o.type === "parcel" && !o.parcels.some((p) => p.kg > 0)) e.push("חסר משקל לחבילה.");
  ["sender", "recipient"].forEach((k) => {
    const a = o[k], t = k === "sender" ? "שולח" : "נמען";
    if (!a.city || !a.street) e.push("חסרה כתובת " + t + " (עיר ורחוב).");
    if (!a.name) e.push("חסר שם איש קשר " + t + ".");
    if (a.phone.replace(/\D/g, "").length < 7) e.push("חסר טלפון " + t + ".");
  });
  if (!o.pickup.date) e.push("בחרו תאריך איסוף.");
  if (!(o.declarations.dangerous && o.declarations.terms && o.declarations.dims)) e.push("יש לאשר את שלוש ההצהרות.");
  return e;
}

module.exports = { cut, num, oneOf, cc, order, addr, missingForSubmit };
