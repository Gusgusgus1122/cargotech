"use strict";
/* Pricing rules (set by the owner):
   - business customer: carrier price + 110%      (50 -> 105)
   - private customer:  carrier price + 210%      (50 -> 155)
   - no VAT on international shipping
   - signature confirmation: fixed fee in USD, converted with a rate the owner sets
   All percentages and fees live in settings/pricing, editable in the back office. */

const DEFAULT_SETTINGS = {
  markupBusinessPct: 110,
  markupPrivatePct: 210,
  markupOnSurcharges: true,     /* remote-area etc. get the same percentage (owner to confirm) */
  markupOnSignature: false,     /* signature fee passed on as is (owner to confirm) */
  signatureFeeUsd: 5,
  usdIls: 3.6,                  /* UPDATE in the back office - placeholder rate */
  testMode: true,               /* sample prices from the built-in test provider; switch off when a real carrier API is connected */
  requireStaffLogin: true,      /* a staff code only works while that employee is logged in to the back office */
  currency: "ILS",
};

const round2 = (n) => Math.round((Number(n) + Number.EPSILON) * 100) / 100;

function chargeableKg(parcels, divisor = 5000) {
  let real = 0, vol = 0;
  (parcels || []).forEach((p) => {
    const q = Math.max(1, Number(p.qty) || 1);
    real += (Number(p.kg) || 0) * q;
    vol += ((Number(p.l) || 0) * (Number(p.w) || 0) * (Number(p.h) || 0) * q) / divisor;
  });
  return { real: round2(real), vol: round2(vol), billable: round2(Math.max(real, vol)) };
}

function markupPct(customerType, s) {
  if (customerType === "business") return Number(s.markupBusinessPct);
  if (customerType === "private") return Number(s.markupPrivatePct);
  throw new Error("customer-type");
}

const SIGNATURE = { none: "ללא חתימה", standard: "חתימה בקבלה", adult: "חתימת מבוגר בקבלה" };

/* offer: { base, surcharges:[{code,label,amount}], currency }  ->  { lines, total, cost, markupPct }
   pctOverride: a per-order commission override set by an admin, used instead of the customerType-based
   markupBusinessPct/markupPrivatePct (e.g. after the carrier's actual weight at pickup changes the price). */
function priceOffer(offer, { customerType, signature, settings, pctOverride }) {
  const s = { ...DEFAULT_SETTINGS, ...(settings || {}) };
  const pct = pctOverride != null ? Number(pctOverride) : markupPct(customerType, s);
  const up = (x) => round2(x * (1 + pct / 100));
  const lines = [{ key: "shipping", label: "שילוח", cost: round2(offer.base), price: up(offer.base) }];
  (offer.surcharges || []).forEach((c) => {
    lines.push({ key: c.code, label: c.label, cost: round2(c.amount), price: s.markupOnSurcharges ? up(c.amount) : round2(c.amount) });
  });
  if (signature && signature !== "none") {
    const fee = round2(s.signatureFeeUsd * s.usdIls);
    lines.push({ key: "signature", label: SIGNATURE[signature] || "חתימה", cost: fee, price: s.markupOnSignature ? up(fee) : fee });
  }
  const total = round2(lines.reduce((a, l) => a + l.price, 0));
  const cost = round2(lines.reduce((a, l) => a + l.cost, 0));
  return { lines, total, cost, markupPct: pct, currency: s.currency };
}

module.exports = { DEFAULT_SETTINGS, round2, chargeableKg, markupPct, priceOffer, SIGNATURE };
