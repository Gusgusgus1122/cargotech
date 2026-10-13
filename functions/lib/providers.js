"use strict";
/* Carrier price providers. Each provider: { name, enabled(settings), quote(ctx) -> [offer] }.
   offer = { id, carrier, service, days, includes:[...], base, surcharges:[{code,label,amount}], currency, test }
   To connect a real carrier API: add an object to PROVIDERS that calls it inside quote().
   If no provider returns an offer, the order continues as a "manual quote" priced by your team. */
const { chargeableKg, round2 } = require("./pricing");
const { ZONE_OF_COUNTRY, TABLES } = require("./fedexRates");

const EUROPE = new Set("al ad at by be ba bg hr cy cz dk ee fi fr de gr hu is ie it lv li lt lu mt md mc me nl mk no pl pt ro ru sm rs sk si es se ch ua gb va xk".split(" "));
const NEAR = new Set("us ca".split(" "));

/* Sample prices ONLY for checking the flow while settings.testMode is on. Not real carrier prices. */
const testProvider = {
  name: "test",
  enabled: (s) => s.testMode === true,
  quote(ctx) {
    if (ctx.mode !== "intl" || !(ctx.type === "parcel" || ctx.type === "doc")) return [];
    const kg = ctx.type === "doc" ? 0.5 : Math.max(0.5, chargeableKg(ctx.parcels).billable);
    const zone = EUROPE.has(ctx.to) ? 1 : NEAR.has(ctx.to) ? 1.3 : 1.8;
    const express = (60 + 28 * Math.pow(kg, 0.85)) * zone;
    const surcharges = [];
    const remote = (z) => /^(99|00)/.test(String(z || "").replace(/\s/g, ""));
    if (remote(ctx.entered && ctx.entered.from) || remote(ctx.entered && ctx.entered.to)) surcharges.push({ code: "remote", label: "אזור מרוחק", amount: 48 });
    return [
      { id: "test:express", carrier: "ספק בדיקה א׳", service: "אקספרס", days: zone === 1 ? "2-4" : zone === 1.3 ? "3-5" : "4-8", includes: ["ביטוח בסיסי", "מעקב"], base: round2(express), surcharges, currency: "ILS", test: true },
      { id: "test:economy", carrier: "ספק בדיקה ב׳", service: "חסכוני", days: zone === 1 ? "5-9" : zone === 1.3 ? "7-12" : "9-16", includes: ["מעקב"], base: round2(express * 0.72), surcharges, currency: "ILS", test: true },
    ];
  },
};

/* FedEx international rates, from the carrier's own price lists (cost; the 110%/210% markup is applied
   generically afterwards in priceOffer). Above 68kg a shipment stops being a parcel and becomes freight -
   same threshold for every carrier/shipment in the system, not just FedEx. */
const FREIGHT_SWITCH_KG = 68;

function lookupRate(table, kg, zone) {
  const row = table.find((r) => r.kg >= kg);
  const rate = row && row[zone];
  return typeof rate === "number" && rate > 0 ? rate : null;
}

const fedexProvider = {
  name: "fedex",
  enabled: (s) => s.testMode !== true, /* real prices take over once the owner turns test mode off in Settings */
  quote(ctx) {
    if (ctx.mode !== "intl" || !(ctx.type === "parcel" || ctx.type === "doc")) return [];
    const zone = ZONE_OF_COUNTRY[String(ctx.to || "").toLowerCase()];
    if (!zone) return [];
    const kg = ctx.type === "doc" ? 0.5 : Math.max(0.5, chargeableKg(ctx.parcels).billable);
    const freight = kg > FREIGHT_SWITCH_KG;
    const priP = lookupRate(freight ? TABLES.priorityFreight : TABLES.priority, kg, zone);
    const priE = lookupRate(freight ? TABLES.economyFreight : TABLES.economy, kg, zone);
    const out = [];
    if (priP != null) out.push({ id: "fedex:priority", carrier: "FedEx", service: freight ? "Priority Freight" : "Priority", days: freight ? "3-7" : "2-5", includes: ["מעקב"], base: round2(priP), surcharges: [], currency: "ILS" });
    if (priE != null) out.push({ id: "fedex:economy", carrier: "FedEx", service: freight ? "Economy Freight" : "Economy", days: freight ? "6-12" : "4-8", includes: ["מעקב"], base: round2(priE), surcharges: [], currency: "ILS" });
    return out;
  },
};

const PROVIDERS = [testProvider, fedexProvider];

async function getOffers(ctx, settings) {
  const out = [];
  for (const p of PROVIDERS) {
    if (!p.enabled(settings)) continue;
    try { (await p.quote(ctx)).forEach((o) => out.push(o)); } catch (e) { /* a failing provider must not block the order */ }
  }
  return out;
}

module.exports = { getOffers, PROVIDERS };
