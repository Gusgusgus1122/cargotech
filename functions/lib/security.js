"use strict";
/* Small crypto helpers. Nothing here ever logs or stores a staff code. */
const crypto = require("crypto");

const sha256 = (s) => crypto.createHash("sha256").update(String(s)).digest("hex");
const hmac = (key, s) => crypto.createHmac("sha256", key).update(String(s)).digest("hex");
const randToken = (bytes = 24) => crypto.randomBytes(bytes).toString("base64url");

/* No 0/O/1/I/L so a code read out loud over the phone is not misheard */
const CODE_ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789";
function genCode() {
  let out = "";
  const bytes = crypto.randomBytes(12);
  for (let i = 0; i < 12; i++) out += CODE_ALPHABET[bytes[i] % CODE_ALPHABET.length];
  return out.slice(0, 4) + "-" + out.slice(4, 8) + "-" + out.slice(8, 12);
}
const normalizeCode = (c) => String(c == null ? "" : c).toUpperCase().replace(/[^A-Z0-9]/g, "").slice(0, 32);

function safeEqual(a, b) {
  const x = Buffer.from(String(a)), y = Buffer.from(String(b));
  return x.length === y.length && crypto.timingSafeEqual(x, y);
}

/* Short-lived signed token: base64url(json).signature */
function signToken(payload, key, ttlSec) {
  const body = Buffer.from(JSON.stringify({ ...payload, exp: Math.floor(Date.now() / 1000) + ttlSec })).toString("base64url");
  return body + "." + hmac(key, body);
}
function verifyToken(token, key) {
  const parts = String(token || "").split(".");
  if (parts.length !== 2 || !safeEqual(parts[1], hmac(key, parts[0]))) return null;
  try {
    const p = JSON.parse(Buffer.from(parts[0], "base64url").toString("utf8"));
    return p.exp && p.exp > Math.floor(Date.now() / 1000) ? p : null;
  } catch (e) { return null; }
}

module.exports = { sha256, hmac, randToken, genCode, normalizeCode, safeEqual, signToken, verifyToken };
