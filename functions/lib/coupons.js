"use strict";
/* Shared by both servers: back office creates/cancels coupons, the public server lets a customer redeem one by code at signup.
   A coupon is a percentage discount, time-boxed, either "once" (a single customer, ever) or "multi" (any number of customers
   within the valid window). Nothing here recomputes order prices yet - this is the coupon record and its status only. */
function couponStatus(c, nowIso) {
  const today = String(nowIso || new Date().toISOString()).slice(0, 10);
  if (c.cancelled) return "cancelled";
  if (c.validTo && today > c.validTo) return "expired";
  if (c.validFrom && today < c.validFrom) return "scheduled";
  if (c.usageType === "once" && (c.usesCount || 0) >= 1) return "used";
  return "active";
}
module.exports = { couponStatus };
