# -*- coding: utf-8 -*-
import os, re, html, shutil

SCR = os.path.dirname(os.path.abspath(__file__))
SRC = SCR + "/cargotech-orig.html"
OUT = os.environ.get("OUT_DIR", os.path.join(SCR, "..", "public-draft"))
ADMIN_OUT = os.environ.get("ADMIN_OUT_DIR", OUT.rstrip("/") + "-admin")
ADMIN_URL = os.environ.get("ADMIN_URL", "https://cargotech-admin.web.app")
SITE_URL = os.environ.get("SITE_URL", "https://cargotech-site.web.app")

src = open(SRC, encoding="utf-8").read()
BASE_CSS = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
MAIN_HTML = re.search(r"<main id=\"top\">(.*?)</main>", src, re.S).group(1)

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700;800&family=Secular+One&family=Heebo:wght@500;800;900&family=IBM+Plex+Mono:wght@500&display=swap">')

RESET = ":root{color-scheme:light;padding:env(safe-area-inset-top,0px) 0 env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}\n"

EXTRA_CSS = r"""
/* ---- Site-wide additions ---- */
.nav { gap: 22px; }
.nav a.nl[aria-current="page"] { color: var(--on-ink); box-shadow: inset 0 -3px 0 var(--accent); padding-block: 6px; }
.mnav { display: none; position: relative; }
.mnav summary { list-style: none; cursor: pointer; min-height: 44px; display: inline-flex; align-items: center; padding: 0 16px; border: 1.5px solid rgba(234, 241, 247, .45); border-radius: 10px; font-weight: 800; color: var(--on-ink); }
.mnav summary::-webkit-details-marker { display: none; }
.mnav .panel { position: absolute; inset-inline-end: 0; top: calc(100% + 8px); min-width: 230px; background: var(--ink-2); border: 1px solid rgba(234, 241, 247, .2); border-radius: 12px; padding: 8px; display: grid; }
.mnav .panel a { display: flex; align-items: center; min-height: 46px; padding: 0 14px; text-decoration: none; color: var(--on-ink); font-weight: 700; border-radius: 8px; }
.mnav .panel a:hover, .mnav .panel a[aria-current="page"] { background: rgba(234, 241, 247, .1); }
@media (max-width: 900px) { .mnav { display: block; } }

.phero { background: repeating-linear-gradient(90deg, transparent 0 79px, rgba(169, 188, 207, .07) 79px 80px), repeating-linear-gradient(0deg, transparent 0 79px, rgba(169, 188, 207, .07) 79px 80px), var(--ink); color: var(--on-ink); padding-block: 44px 52px; }
.phero .wrap { display: grid; gap: 16px; justify-items: start; }
.phero h1 { font-size: clamp(2rem, 4.8vw, 3.3rem); max-width: 20em; }
.phero .lead { color: var(--on-ink-muted); font-size: 1.2rem; max-width: 38em; }
.phero .cta-row { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 8px; }
.crumbs { font-size: .92rem; color: var(--on-ink-muted); }
.crumbs a { color: var(--on-ink); text-underline-offset: 3px; }

.checks { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px 32px; }
.checks li { position: relative; padding-inline-start: 36px; font-size: 1.08rem; }
.checks li::before { content: ""; position: absolute; inset-inline-start: 0; top: .28em; width: 22px; height: 22px; border-radius: 50%; background: var(--ok); }
.checks li::after { content: ""; position: absolute; inset-inline-start: 8px; top: .48em; width: 6px; height: 10px; border: solid var(--surface); border-width: 0 2.5px 2.5px 0; transform: rotate(45deg); }

.more { font-weight: 800; color: var(--sea); text-underline-offset: 4px; }
.more:hover { color: var(--fg); }

.tscroll { overflow-x: auto; border: 1px solid var(--line); border-radius: 12px; }
table.cmp { border-collapse: collapse; width: 100%; min-width: 560px; background: var(--surface); }
.cmp th, .cmp td { padding: 14px 16px; text-align: right; border-bottom: 1px solid var(--line); vertical-align: top; }
.cmp tr:last-child td, .cmp tr:last-child th { border-bottom: 0; }
.cmp thead th { font-family: var(--font-display); font-weight: 400; font-size: 1.1rem; color: var(--sea); background: var(--bg); }
.cmp tbody th { font-weight: 800; }

.rel { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }
.rel a { display: grid; gap: 6px; align-content: start; padding: 20px 22px; background: var(--surface); border: 1px solid var(--line); border-radius: 12px; text-decoration: none; color: var(--fg); transition: border-color .15s; }
.rel a:hover { border-color: var(--sea); }
.rel b { font-family: var(--font-display); font-weight: 400; font-size: 1.2rem; color: var(--sea); }
.rel span { color: var(--muted); font-size: .98rem; }

.prose { max-width: 42em; }
.prose h2 { font-size: 1.7rem; margin: 44px 0 12px; }
.prose p { margin: 0 0 16px; font-size: 1.08rem; }
.prose ul, .prose ol { padding-inline-start: 24px; margin: 0 0 18px; display: grid; gap: 8px; font-size: 1.08rem; }
.prose a { color: var(--sea); text-underline-offset: 3px; font-weight: 700; }
.tldr { background: var(--sea-soft); border-radius: 12px; padding: 20px 22px; margin: 0 0 12px; max-width: 42em; }
.tldr b { display: block; margin-bottom: 6px; color: var(--sea); font-family: var(--font-display); font-weight: 400; font-size: 1.15rem; }
.callout { background: var(--surface); border: 1px solid var(--line); border-inline-start: 5px solid var(--accent); padding: 20px 22px; border-radius: 10px; margin-block: 30px; display: grid; gap: 14px; justify-items: start; }
.callout p { margin: 0; font-weight: 700; font-size: 1.1rem; }
.meta { color: var(--muted); font-size: .95rem; }

.calc { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 28px; align-items: start; }
.calc .inputs { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; background: var(--surface); border: 1px solid var(--line); border-radius: 14px; padding: 22px; }
.calc .inputs .full { grid-column: 1 / -1; }
.calc .ex { grid-column: 1 / -1; font-size: .9rem; color: var(--muted); }
.result { background: var(--ink); color: var(--on-ink); border-radius: 14px; padding: 26px; display: grid; gap: 14px; }
.result .big { font-family: var(--font-display); font-size: clamp(2.2rem, 6vw, 3rem); line-height: 1.1; color: var(--accent); }
.result .big small { font-family: var(--font-body); font-size: 1rem; color: var(--on-ink-muted); margin-inline-start: 6px; }
.result dl { margin: 0; display: grid; gap: 8px; }
.result dl div { display: flex; justify-content: space-between; gap: 16px; border-bottom: 1px solid var(--ink-2); padding-bottom: 8px; }
.result dt { color: var(--on-ink-muted); }
.result dd { margin: 0; font-weight: 800; font-variant-numeric: tabular-nums; }
.result .why { color: var(--on-ink-muted); font-size: .98rem; }

.quote-sec { background: var(--ink); color: var(--on-ink); padding-block: 64px; }
.quote-sec .wrap { display: grid; grid-template-columns: minmax(0, .9fr) minmax(0, 1.1fr); gap: 44px; align-items: start; }
.quote-sec h2 { font-size: clamp(1.8rem, 4vw, 2.6rem); }
.quote-sec .side { display: grid; gap: 16px; }
.quote-sec .side p { color: var(--on-ink-muted); font-size: 1.12rem; }
.quote-sec .contact-lines { margin-top: 6px; }

.foot { background: var(--ink); color: var(--on-ink-muted); border-top: 1px solid var(--ink-2); padding-block: 44px 24px; font-size: .95rem; }
.foot .cols { display: grid; grid-template-columns: 1.3fr 1fr 1fr 1fr; gap: 28px; }
.foot h4 { margin: 0 0 8px; color: var(--on-ink); font-size: 1.02rem; font-weight: 800; }
.foot a { display: block; padding: 9px 0; color: var(--on-ink-muted); text-decoration: none; }
.foot a:hover { color: var(--on-ink); }
.foot .brandline { font-family: var(--font-display); font-size: 1.4rem; color: var(--on-ink); margin-bottom: 8px; }
.foot .legal { margin-top: 26px; padding-top: 18px; border-top: 1px solid var(--ink-2); display: flex; flex-wrap: wrap; justify-content: space-between; gap: 8px 24px; }

@media (max-width: 900px) {
  .checks { grid-template-columns: minmax(0, 1fr); }
  .rel { grid-template-columns: minmax(0, 1fr); }
  .calc, .quote-sec .wrap { grid-template-columns: minmax(0, 1fr); }
  .foot .cols { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (max-width: 600px) {
  .calc .inputs { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .phero { padding-block: 32px 40px; }
  .quote-sec { padding-block: 48px; }
  .foot .cols { grid-template-columns: minmax(0, 1fr); }
}
"""

SKIN_CSS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "skin.css"), encoding="utf-8").read()
import wizard
SKIN_CSS += wizard.WIZ_CSS

JS = r"""
var CONFIG = {
  whatsapp: "",               /* international format, digits only, e.g. 972501234567 */
  phoneDisplay: "05X-XXX-XXXX",
  email: "office@your-domain.co.il",
  leadApi: "/api/lead",       /* Firebase Function that stores quote requests in Firestore; leave empty to disable */
  measurementId: "G-FCV82YGNTB"           /* Firebase / GA4 measurement ID, e.g. G-XXXXXXXXXX; leave empty to disable analytics */
};
(function () {
  var base = CONFIG.whatsapp ? "https://wa.me/" + CONFIG.whatsapp : "https://wa.me/";
  function wa(text) { return base + "?text=" + encodeURIComponent(text); }
  document.querySelectorAll("[data-phone]").forEach(function (el) { el.textContent = CONFIG.phoneDisplay; });
  document.querySelectorAll("[data-email]").forEach(function (el) { el.textContent = CONFIG.email; });
  document.querySelectorAll("[data-wa]").forEach(function (el) { el.href = wa(el.getAttribute("data-wa")); });

  /* Analytics (Firebase / GA4) - loaded only when a measurement ID is set */
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  var track = function (name, params) { if (CONFIG.measurementId) { try { gtag("event", name, params || {}); } catch (e) {} } };
  if (CONFIG.measurementId && /^https?:$/.test(location.protocol)) {
    var gs = document.createElement("script"); gs.async = true; gs.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(CONFIG.measurementId);
    document.head.appendChild(gs); gtag("js", new Date()); gtag("config", CONFIG.measurementId);
  }
  document.querySelectorAll("[data-wa]").forEach(function (el) { el.addEventListener("click", function () { track("whatsapp_click", { page: location.pathname }); }); });
  document.querySelectorAll('a[href="#quote"]').forEach(function (el) { el.addEventListener("click", function () { track("quote_cta_click", { page: location.pathname }); }); });

  var form = document.getElementById("qform");
  if (form) {
    var f = {
      service: document.getElementById("f-service"), route: document.getElementById("f-route"),
      cargo: document.getElementById("f-cargo"), name: document.getElementById("f-name"), phone: document.getElementById("f-phone")
    };
    var send = document.getElementById("send-wa");
    var preset = form.getAttribute("data-default");
    if (preset) f.service.value = preset;
    var compose = function () {
      var lines = ["שלום CargoTech, אני רוצה הצעת מחיר."];
      if (f.service.value) lines.push("שירות: " + f.service.value);
      if (f.route.value.trim()) lines.push("מסלול: " + f.route.value.trim());
      if (f.cargo.value.trim()) lines.push("מטען: " + f.cargo.value.trim());
      if (f.name.value.trim()) lines.push("שם: " + f.name.value.trim());
      if (f.phone.value.trim()) lines.push("טלפון: " + f.phone.value.trim());
      send.href = wa(lines.join("\n"));
    };
    Object.keys(f).forEach(function (k) { f[k].addEventListener("input", compose); f[k].addEventListener("change", compose); });
    form.addEventListener("submit", function (e) { e.preventDefault(); });
    var hp = document.createElement("input"); hp.type = "text"; hp.name = "website"; hp.tabIndex = -1; hp.autocomplete = "off"; hp.setAttribute("aria-hidden", "true"); hp.style.cssText = "position:absolute;left:-9999px;width:1px;height:1px;opacity:0"; form.appendChild(hp);
    send.addEventListener("click", function () {
      track("generate_lead", { service: f.service.value || "none", page: location.pathname });
      if (!CONFIG.leadApi || !/^https?:$/.test(location.protocol)) return;
      if (!f.name.value.trim() && !f.phone.value.trim() && !f.route.value.trim() && !f.cargo.value.trim()) return;
      try {
        fetch(CONFIG.leadApi, { method: "POST", headers: { "Content-Type": "application/json" }, keepalive: true,
          body: JSON.stringify({ service: f.service.value, route: f.route.value, cargo: f.cargo.value, name: f.name.value, phone: f.phone.value, page: location.pathname, website: hp.value }) }).catch(function () {});
      } catch (e) {}
    });
    compose();
    document.querySelectorAll("[data-service]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        f.service.value = btn.getAttribute("data-service");
        compose();
        var q = document.getElementById("quote");
        if (q) q.scrollIntoView({ block: "center" });
        setTimeout(function () { f.route.focus({ preventScroll: true }); }, 350);
      });
    });
  }

  /* Chargeable weight calculator */
  var calc = document.getElementById("calc");
  if (calc) {
    var g = function (id) { return document.getElementById(id); };
    var fmt = function (n, d) { return n.toLocaleString("he-IL", { minimumFractionDigits: 0, maximumFractionDigits: d }); };
    var run = function () {
      var L = parseFloat(g("c-l").value) || 0, W = parseFloat(g("c-w").value) || 0, H = parseFloat(g("c-h").value) || 0;
      var n = parseFloat(g("c-n").value) || 0, kg = parseFloat(g("c-kg").value) || 0, div = parseFloat(g("c-div").value) || 5000;
      var vol = L * W * H * n / div, real = kg * n, cbm = L * W * H * n / 1000000;
      var charge = Math.max(vol, real);
      g("r-charge").firstChild.nodeValue = fmt(charge, 1) + " ";
      g("r-vol").textContent = fmt(vol, 1) + " ק\"ג";
      g("r-real").textContent = fmt(real, 1) + " ק\"ג";
      g("r-cbm").textContent = fmt(cbm, 2) + " מ\"ק";
      var why = "מחייבים לפי המשקל האמיתי.";
      if (vol > real) why = "מחייבים לפי המשקל הנפחי, כי המטען גדול ביחס למשקלו.";
      if (!charge) why = "מלאו מידות ומשקל כדי לראות את התוצאה.";
      g("r-why").textContent = why;
      var msg = "שלום CargoTech, אני רוצה הצעת מחיר לשילוח.\nמטען: " + n + " קרטונים, " + L + "x" + W + "x" + H + " ס\"מ, " + kg + " ק\"ג לקרטון.\nמשקל מחייב מחושב: " + fmt(charge, 1) + " ק\"ג.";
      var a = g("calc-cta"); a.href = wa(msg);
    };
    calc.querySelectorAll("input,select").forEach(function (el) { el.addEventListener("input", run); el.addEventListener("change", run); });
    run();
  }

  var mn = document.querySelector(".mnav");
  if (mn) { mn.querySelectorAll("a").forEach(function (a) { a.addEventListener("click", function () { mn.removeAttribute("open"); }); }); }

  if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    document.querySelectorAll(".routemap .pkg").forEach(function (p) { p.parentNode.removeChild(p); });
  }
})();

/* ---------- marketing / contact banners (built in the back office, "Banners") ---------- */
(function () {
  if (!/^https?:$/.test(location.protocol)) return;
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var page = (location.pathname === "/" || /\/index\.html$/.test(location.pathname)) ? "home" : "all";
  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };

  var CSS = ".ctbn-back{position:fixed;inset:0;background:rgba(10,20,30,.42);z-index:9000;opacity:0;transition:opacity .25s}"
    + ".ctbn-back.in{opacity:1}"
    + ".ctbn{position:fixed;z-index:9001;background:var(--surface,#fff);color:var(--fg,#172532);border:1px solid var(--line,#dde2e6);box-shadow:0 20px 50px rgba(10,20,30,.25);border-radius:16px;max-width:380px;padding:22px 22px 20px;opacity:0}"
    + ".ctbn.anim-in{transition:opacity .35s,transform .35s}"
    + ".ctbn[data-t=center]{top:50%;left:50%;transform:translate(-50%,calc(-50% + 14px))}"
    + ".ctbn[data-t=center].in{opacity:1;transform:translate(-50%,-50%)}"
    + ".ctbn[data-t=full]{top:50%;left:50%;max-width:520px;width:92vw;transform:translate(-50%,calc(-50% + 14px))}"
    + ".ctbn[data-t=full].in{opacity:1;transform:translate(-50%,-50%)}"
    + ".ctbn[data-t=side]{bottom:18px;left:18px;transform:translateY(14px)}"
    + ".ctbn[data-t=side].in{opacity:1;transform:translateY(0)}"
    + ".ctbn[data-t=bottom]{left:0;right:0;bottom:0;max-width:none;border-radius:16px 16px 0 0;display:flex;align-items:center;gap:16px;flex-wrap:wrap;transform:translateY(100%)}"
    + ".ctbn[data-t=bottom].in{opacity:1;transform:translateY(0)}"
    + ".ctbn.anim-scale{transform:scale(.92)!important}.ctbn.anim-scale.in{transform:scale(1)!important}"
    + ".ctbn.anim-slide{transform:translateX(36px)!important}.ctbn.anim-slide.in{transform:translateX(0)!important}"
    + ".ctbn-x{position:absolute;top:8px;left:8px;width:30px;height:30px;border:0;background:none;color:var(--muted,#5a6f7e);font-size:1.3rem;line-height:1;cursor:pointer;border-radius:50%}"
    + ".ctbn-x:hover{background:var(--bg,#f3f6f9)}"
    + ".ctbn img{max-width:100%;border-radius:10px;margin-bottom:10px;display:block}"
    + ".ctbn h3{margin:0 0 8px;font-size:1.2rem;font-family:var(--font-display,inherit)}"
    + ".ctbn p{margin:0 0 14px;color:var(--muted,#5a6f7e);font-size:.98rem}"
    + ".ctbn[data-t=bottom] h3{margin:0;font-size:1.05rem}.ctbn[data-t=bottom] p{margin:0}"
    + ".ctbn-cta{display:inline-flex;min-height:46px;align-items:center;justify-content:center;padding:0 22px;border-radius:9px;background:var(--accent,#ff6b2c);color:var(--on-accent,#0b1f33);font-weight:800;text-decoration:none;border:0;cursor:pointer;white-space:nowrap}"
    + ".ctbn-form{display:grid;gap:8px;margin-top:4px}"
    + ".ctbn-form input{min-height:42px;padding:8px 10px;border:1.5px solid var(--line,#dde2e6);border-radius:8px;font:inherit}"
    + ".ctbn-done{font-weight:700;color:var(--ok,#1f8a5b)}";

  function fireEvent(id, kind) { try { fetch("/api/v1/banners/event", { method: "POST", headers: { "Content-Type": "application/json" }, keepalive: true, body: JSON.stringify({ id: id, kind: kind }) }).catch(function () {}); } catch (e) {} }
  function seen(p) {
    if (p.frequency === "once") return !!localStorage.getItem("ctbn_once_" + p.id);
    if (p.frequency === "session") return !!sessionStorage.getItem("ctbn_sess_" + p.id);
    return false;
  }
  function markSeen(p) {
    if (p.frequency === "once") try { localStorage.setItem("ctbn_once_" + p.id, "1"); } catch (e) {}
    if (p.frequency === "session") try { sessionStorage.setItem("ctbn_sess_" + p.id, "1"); } catch (e) {}
  }

  function render(p) {
    if (seen(p)) return;
    var st = document.createElement("style"); st.textContent = CSS; document.head.appendChild(st);
    var back = null;
    if (p.template === "center" || p.template === "full") { back = document.createElement("div"); back.className = "ctbn-back"; document.body.appendChild(back); }
    var el = document.createElement("div");
    el.className = "ctbn" + (reduceMotion ? "" : " anim-in" + (p.anim === "scale" ? " anim-scale" : p.anim === "slide-side" ? " anim-slide" : "")); el.setAttribute("data-t", p.template);
    var ctaHtml = "";
    if (p.ctaType === "contact") ctaHtml = '<button type="button" class="ctbn-cta" data-ctbn-contact>' + esc(p.ctaText || "יצירת קשר") + "</button>";
    else if (p.ctaType !== "none" && p.ctaText) ctaHtml = '<a class="ctbn-cta" href="#" data-ctbn-go>' + esc(p.ctaText) + "</a>";
    el.innerHTML = '<button type="button" class="ctbn-x" aria-label="סגירה">×</button>' +
      (p.imageUrl ? '<img src="' + esc(p.imageUrl) + '" alt="">' : "") +
      (p.title ? "<h3>" + esc(p.title) + "</h3>" : "") + (p.body ? "<p>" + esc(p.body) + "</p>" : "") +
      '<div class="ctbn-body">' + ctaHtml + "</div>";
    document.body.appendChild(el);
    function close(kind) {
      fireEvent(p.id, kind || "dismiss"); markSeen(p);
      el.classList.remove("in"); if (back) back.classList.remove("in");
      setTimeout(function () { el.remove(); if (back) back.remove(); }, reduceMotion ? 0 : 320);
    }
    el.querySelector(".ctbn-x").addEventListener("click", function () { close("dismiss"); });
    if (back) back.addEventListener("click", function () { close("dismiss"); });
    var go = el.querySelector("[data-ctbn-go]");
    if (go) go.addEventListener("click", function (e) {
      e.preventDefault(); fireEvent(p.id, "click");
      if (p.ctaType === "whatsapp") { window.open("https://wa.me/" + p.ctaValue.replace(/[^\d]/g, ""), "_blank", "noopener"); }
      else if (p.ctaType === "phone") { location.href = "tel:" + p.ctaValue; }
      else if (p.ctaValue) { location.href = p.ctaValue; }
    });
    var cf = el.querySelector("[data-ctbn-contact]");
    if (cf) cf.addEventListener("click", function () {
      fireEvent(p.id, "click");
      el.querySelector(".ctbn-body").innerHTML =
        '<div class="ctbn-form"><input type="text" placeholder="שם" id="ctbn-name"><input type="tel" placeholder="טלפון" id="ctbn-phone">'
        + '<button type="button" class="ctbn-cta" id="ctbn-send">שליחה</button></div>';
      document.getElementById("ctbn-send").addEventListener("click", function () {
        var name = document.getElementById("ctbn-name").value.trim(), phone = document.getElementById("ctbn-phone").value.trim();
        if (!name && !phone) return;
        try { fetch(CONFIG.leadApi, { method: "POST", headers: { "Content-Type": "application/json" }, keepalive: true,
          body: JSON.stringify({ name: name, phone: phone, service: "banner", cargo: p.title, page: location.pathname, website: "" }) }).catch(function () {}); } catch (e) {}
        el.querySelector(".ctbn-body").innerHTML = '<span class="ctbn-done">תודה! ניצור קשר בקרוב.</span>';
        setTimeout(function () { close("click"); }, 1800);
      });
    });
    requestAnimationFrame(function () { requestAnimationFrame(function () {
      el.classList.add("in"); if (back) back.classList.add("in"); fireEvent(p.id, "show");
    }); });
  }

  fetch("/api/v1/banners/active?page=" + page).then(function (r) { return r.json(); }).then(function (j) {
    if (!j || !j.ok || !j.banner) return;
    var p = j.banner;
    setTimeout(function () { render(p); }, Math.max(0, (p.delaySec || 0) * 1000));
  }).catch(function () {});
})();
"""

NAV = [("import.html", "יבוא", "import"), ("export.html", "יצוא", "export"), ("shipping.html", "שילוח", "shipping"),
       ("pricing.html", "מחירון", "pricing"), ("articles.html", "מדריכים", "articles"), ("contact.html", "צור קשר", "contact")]

SERVICE_OPTIONS = ["יבוא", "יצוא", "שילוח אווירי או ימי", "קורייר", 'מזון לארה"ב (FDA)', "עמילות מכס", "עדיין לא יודע"]

def esc(s): return html.escape(s, quote=True)

LOGO_OLD = ('<svg viewBox="0 0 34 34" aria-hidden="true"><rect x="2" y="2" width="30" height="30" rx="7" fill="#FF6B2C"/>'
        '<path d="M8 13l9-5 9 5v10l-9 5-9-5z" fill="none" stroke="#0B1F33" stroke-width="2.2" stroke-linejoin="round"/>'
        '<path d="M8 13l9 5 9-5M17 18v10" fill="none" stroke="#0B1F33" stroke-width="2.2" stroke-linejoin="round"/></svg>')

LOGO = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 721 100" role="img" aria-label="CargoTech"><defs><mask id="sh"><rect x="-10" y="-5" width="741" height="110" fill="#fff"/><rect x="462" y="46" width="150" height="6" fill="#000"/></mask></defs><g transform="translate(25 0) skewX(-14)"><g fill="#FFFFFF"><path transform="translate(0 0)" fill-rule="evenodd" d="M12 0H70V22H26V78H70V100H12L0 88V12Z"/><path transform="translate(78 0)" fill-rule="evenodd" d="M0 100L22 0H50L72 100H48L45 82H27L24 100ZM31 62H41L36 30Z"/><path transform="translate(158 0)" fill-rule="evenodd" d="M0 0H56L70 14V46L58 58L72 100H47L36 62H24V100H0ZM24 20V42H46V20Z"/><path transform="translate(236 0)" fill-rule="evenodd" d="M12 0H70V22H26V78H46V62H34V44H70V100H12L0 88V12Z"/><path transform="translate(314 0)" fill-rule="evenodd" d="M12 0H58L70 12V88L58 100H12L0 88V12ZM24 22V78H46V22Z"/></g><g fill="#4FC3EC" mask="url(#sh)"><path transform="translate(392 0)" fill-rule="evenodd" d="M0 0H72V22H48V100H24V22H0Z"/><path transform="translate(472 0)" fill-rule="evenodd" d="M0 0H66V22H24V38H58V58H24V78H66V100H0Z"/><path transform="translate(546 0)" fill-rule="evenodd" d="M12 0H70V22H26V78H70V100H12L0 88V12Z"/><path transform="translate(624 0)" fill-rule="evenodd" d="M0 0H24V38H48V0H72V100H48V62H24V100H0Z"/></g></g></svg>'

MENU = [
 ("שירותים", "import", [("import.html","יבוא"),("export.html","יצוא"),("shipping.html","שילוח אווירי וימי"),("courier.html","קורייר"),("fda-food.html",'מזון לארה"ב (FDA)'),("customs.html","עמילות מכס")]),
 ("יעדים", "dest", [("europe.html","אירופה"),("usa.html",'ארה"ב')]),
 ("כלים", "tools", [("data.html","בדיקת יבוא לפי מוצר"),("pricing.html","מחשבון משקל ומחירון"),("commercial-invoice.html","חשבונית מסחרית"),("proforma-invoice.html","חשבונית פרופורמה"),("packing-list.html","רשימת אריזה"),("hs-code-guide.html","איתור פרט מכס"),("import-taxes-israel.html","מיסי יבוא"),("postal-codes-country-codes.html","קודי מדינות ומיקודים"),("tracking-shipments.html","מעקב משלוחים"),("glossary.html","מילון מונחים")]),
 ("מידע", "info", [("pricing.html","מחירון ומחשבון משקל"),("glossary.html","מילון מונחים ושאלות"),("articles.html","כל המדריכים")] ),
]
def header(active):
    def cur(h, k=None): return ' aria-current="page"' if (k == active or h.split(".")[0] == active) else ""
    items = ""
    for title, key, links in MENU:
        if key == "info": links = links + [(a_["file"], a_["short"]) for a_ in GUIDES[:8]]
        if key == "dest": links = links + [(a_["file"], a_["short"]) for a_ in DEST]
        on = any(h.split(".")[0] == active for h, _ in links) or (active == "articles" and key == "info")
        cols = " dd-2" if len(links) > 9 else ""
        sub = "".join('<a href="%s"%s>%s</a>' % (h, cur(h), t) for h, t in links)
        items += ('<div class="dd%s"><button class="nl dd-b" type="button" aria-haspopup="true" aria-expanded="false">%s<i aria-hidden="true"></i></button>'
                  '<div class="dd-p%s">%s</div></div>') % (" on" if on else "", title, " dd-2" if len(links) > 9 else "", sub)
    items += '<a class="nl" href="order.html"%s>הזמנת משלוח</a>' % cur("order.html")
    items += '<a class="nl" href="data.html"%s>בדיקת יבוא</a>' % cur("data.html")
    items += '<a class="nl" href="contact.html"%s>צור קשר</a>' % cur("contact.html")
    panel = '<a href="order.html"%s><b>הזמנת משלוח</b></a>' % cur("order.html") + '<a href="data.html"%s><b>בדיקת יבוא לפי מוצר</b></a>' % cur("data.html") + "".join('<a href="%s"%s>%s</a>' % (h, cur(h), t) for _, _, ls in MENU for h, t in ls) + '<a href="contact.html">צור קשר</a>' + '<a href="account.html" data-authbtn><b>התחברות / הרשמה</b></a>'
    return ('<header class="top"><div class="wrap">'
            '<a class="brand" href="index.html" aria-label="CargoTech, לדף הראשי">%s</a>'
            '<nav class="nav" aria-label="ניווט ראשי">%s'
            '<a class="top-phone latin" data-phone href="contact.html">05X-XXX-XXXX</a>'
            '<a class="btn btn-line-dark btn-sm top-auth" href="account.html" data-authbtn>כניסה</a>'
            '<a class="btn btn-go btn-sm" href="#quote">הצעת מחיר</a>'
            '<details class="mnav"><summary>תפריט</summary><div class="panel">%s</div></details>'
            '</nav></div></header>') % (LOGO, items, panel)

def footer():
    svc = list(MENU[0][2])
    routes = [("europe.html", "אירופה"), ("usa.html", 'ארה"ב')] + [(a_["file"], a_["short"]) for a_ in DEST]
    guides = [(a_["file"], a_["short"]) for a_ in GUIDES[:14]] + [("articles.html#guides", "כל המדריכים ←")]
    info = [("pricing.html", "מחירון ומחשבון משקל"), ("glossary.html", "מילון מונחים ושאלות"), ("data.html", "בדיקת יבוא לפי מוצר"), ("contact.html", "צור קשר")]
    col = lambda title, items, cls="": '<div class="fcol" tabindex="0"><h4>%s</h4><div class="fl%s">%s</div></div>' % (title, cls, "".join('<a href="%s">%s</a>' % (h, t) for h, t in items))
    return ('<footer class="foot"><div class="wrap"><div class="cols">'
            '<div class="fbrand"><a class="brandline" href="index.html">CargoTech</a><p>יבוא, יצוא ושילוח בינלאומי. המילים קשות, הדרך פשוטה, הכל אפשרי.</p></div>'
            + col("שירותים", svc) + col("שילוח לפי יעד", routes, " fl-2") + col("מדריכים", guides, " fl-2") + col("כלים", list(MENU[2][2]), " fl-2") + col("מידע", info) +
            '</div><p class="fhint">העבירו את העכבר על נושא כדי לראות את הדפים שלו</p>'
            '<div class="legal"><span>© CargoTech · <a class="teamlink" href="' + ADMIN_URL + '" rel="nofollow noopener">כניסת צוות</a></span><span><b class="latin" data-phone>05X-XXX-XXXX</b> · <span class="latin" data-email>office@your-domain.co.il</span></span></div></div></footer>')

BAR = ('<div class="bar"><a class="btn btn-go" href="#quote">הצעת מחיר</a>'
       '<a class="btn btn-line" data-wa="שלום CargoTech, אני רוצה לבדוק שילוח." href="https://wa.me/" target="_blank" rel="noopener">וואטסאפ</a></div>')

def quote_section(service, heading, sub):
    opts = '<option value="">בחרו שירות</option>' + "".join("<option>%s</option>" % esc(o) for o in SERVICE_OPTIONS)
    return ('<section class="quote-sec"><div class="wrap">'
            '<div class="side"><h2>%s</h2><p>%s</p>'
            '<a class="btn btn-line" data-wa="שלום CargoTech, יש לי שאלה על שילוח." href="https://wa.me/" target="_blank" rel="noopener">או שאלו בוואטסאפ</a>'
            '<div class="contact-lines"><div><span>טלפון</span><b class="latin" data-phone>05X-XXX-XXXX</b></div></div></div>'
            '<div class="qcard" id="quote"><h2>ספרו לנו מה שולחים</h2><p class="hint">ארבע שורות, פחות מדקה. את השאר נשלים יחד.</p>'
            '<form class="qform" id="qform" data-default="%s">'
            '<div class="field"><label for="f-service">מה אתם צריכים?</label><select id="f-service">%s</select></div>'
            '<div class="field"><label for="f-route">מאיפה לאן?</label><input id="f-route" type="text" placeholder="לדוגמה: מילאנו לתל אביב"></div>'
            '<div class="field"><label for="f-cargo">מה המטען, וכמה?</label><input id="f-cargo" type="text" placeholder="לדוגמה: 12 קרטונים, כ-150 ק&quot;ג"></div>'
            '<div class="row2"><div class="field"><label for="f-name">שם</label><input id="f-name" type="text" autocomplete="name" placeholder="השם שלכם"></div>'
            '<div class="field"><label for="f-phone">טלפון</label><input id="f-phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="05X-XXX-XXXX"></div></div>'
            '<a class="btn btn-go" id="send-wa" href="https://wa.me/" target="_blank" rel="noopener">שלחו לנו בוואטסאפ</a>'
            '<p class="qnote">הפרטים נפתחים כהודעה מוכנה בוואטסאפ, ונשמרים אצלנו רק כדי לחזור אליכם. לוחצים שלח, ואנחנו חוזרים.</p>'
            '</form></div></div></section>') % (heading, sub, esc(service), opts)

HEADER_AUTH_JS = """
(function(){var CT=window.CT;if(!CT)return;
function paint(u){document.querySelectorAll("[data-authbtn]").forEach(function(a){var b=a.querySelector("b")||a;b.textContent=u?"האזור שלי":"התחברות / הרשמה";a.setAttribute("data-in",u?"1":"");});}
document.addEventListener("click",function(e){var a=e.target.closest("[data-authbtn]");if(!a)return;if(a.getAttribute("data-in"))return;if(!document.getElementById("authdlg"))return;e.preventDefault();var d=document.querySelector("details.mnav");if(d)d.open=false;CT.init().then(function(){CT.openAuth("in");});});
var reg={};CT.onAuth(function(u){paint(u);if(u&&!reg[u.uid]){reg[u.uid]=1;CT.api("GET","/me");}});CT.init();})();
"""
def doc(title, desc, active, body, full=True, extra_head="", bar=True, noindex=False, css_extra="", js_extra="", bare=False):
    if not bare and 'id="authdlg"' not in body:
        import authkit as _ak
        body = body + _ak.AUTH_HTML
        css_extra = _ak.AUTH_CSS + css_extra
        js_extra = "<script>" + _ak.AUTH_JS + "</script>" + js_extra
    if not bare:
        js_extra = js_extra + "<script>" + HEADER_AUTH_JS + "</script>"
    css = BASE_CSS + EXTRA_CSS + SKIN_CSS + css_extra
    back = '' if 'class="hero"' in body else '<div class="backbar"><div class="wrap"><a class="btn btn-line-dark" href="index.html">→ חזרה לדף הראשי</a></div></div>'
    inner = ('<div dir="rtl" lang="he"><a class="skip" href="#top">דלגו לתוכן הראשי</a>' + header(active) +
             '<main id="top">' + body + back + '</main>' + footer() + (BAR if bar else '') + '</div><script>' + JS + '</script>' + js_extra)
    if bare:   # the back-office site: no public menu, footer or site scripts
        inner = ('<div dir="rtl" lang="he"><main id="top">' + body + '</main></div>' + js_extra)
    if full:
        return ('<!doctype html>\n<html lang="he" dir="rtl"><head><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
                '<title>%s</title><meta name="description" content="%s">'
                '<meta property="og:type" content="website"><meta property="og:locale" content="he_IL"><meta property="og:site_name" content="CargoTech">'
                '<meta property="og:title" content="%s"><meta property="og:description" content="%s"><meta name="twitter:card" content="summary">%s%s\n<style>%s%s</style></head><body>%s</body></html>'
                % (esc(title), esc(desc), esc(title), esc(desc), '<meta name="robots" content="noindex, nofollow">' if noindex else '', FONTS, RESET, css, inner))
    return '<title>%s</title>\n%s\n<style>%s</style>\n%s' % (esc(title), FONTS, css, inner)

# ------------- components -------------
def crumbs(label):
    return '<div class="crumbs"><a class="backlink" href="index.html">→ חזרה לדף הראשי</a><span> / %s</span></div>' % label

def phero(label, h1, lead, service):
    return ('<section class="phero"><div class="wrap">%s<h1>%s</h1><p class="lead">%s</p>'
            '<div class="cta-row"><a class="btn btn-go" href="#quote">קבלו הצעת מחיר</a>'
            '<a class="btn btn-line" data-wa="שלום CargoTech, אני מעוניין ב%s." href="https://wa.me/" target="_blank" rel="noopener">וואטסאפ</a></div></div></section>'
            % (crumbs(label), h1, lead, esc(service)))

def sec(head, sub, inner, cls="sec", style=""):
    s = '<section class="%s"%s><div class="wrap"><div class="sec-head"><h2>%s</h2>%s</div>%s</div></section>'
    return s % (cls, (' style="%s"' % style) if style else "", head, ("<p>%s</p>" % sub) if sub else "", inner)

def checks(items): return '<ul class="checks">' + "".join("<li>%s</li>" % i for i in items) + "</ul>"

def cta(label="קבלו הצעת מחיר", href="#quote"):
    return '<div style="margin-top:32px"><a class="btn btn-go" href="%s">%s</a></div>' % (href, label)

def terms(items, service):
    out = ""
    for w, p, latin in items:
        out += ('<article class="term"><div class="w%s">%s</div><p>%s</p>'
                '<button class="ask" data-service="%s" type="button">צריך את זה? נבדוק</button></article>') % (" latin" if latin else "", w, p, esc(service))
    return '<div class="dict">%s</div>' % out

def steps(items):
    return '<ol class="steps">' + "".join("<li><h3>%s</h3><p>%s</p></li>" % (h, p) for h, p in items) + "</ol>"

def faq(items):
    out = ""
    for i, (q, a) in enumerate(items):
        out += '<details%s><summary>%s</summary><div class="ans">%s</div></details>' % (" open" if i == 0 else "", q, a)
    return '<div class="faq">%s</div>' % out

def related(items):
    return '<div class="rel">' + "".join('<a href="%s"><b>%s</b><span>%s</span></a>' % x for x in items) + "</div>"

STD_STEPS = lambda a, b, c, d: [("1. " + a[0], a[1]), ("2. " + b[0], b[1]), ("3. " + c[0], c[1]), ("4. " + d[0], d[1])]

# ------------- content -------------
ARTICLES = [
  dict(file="article-customs-broker.html", short="מה זה עמילות מכס", title="מה זה עמילות מכס ולמה צריך אותה | CargoTech",
       desc="עמיל מכס מטפל מול המכס בשמכם: סיווג, חישוב מסים ושחרור. הסבר בעברית פשוטה ורשימת המסמכים שכדאי להכין.",
       h1="מה זה עמילות מכס ולמה צריך אותה", lead="בקצרה: עמיל מכס הוא מי שמדבר עם המכס במקומכם. הוא מסווג את המוצר, מחשב מסים ומשחרר את הסחורה.",
       tldr="עמיל מכס מורשה מגיש את הדיווחים למכס, מסווג את המוצר ומחשב את המס. מי שמייבא או מייצא בלי להבין את הנהלים משלם על טעויות בכסף ובזמן. המסמכים הבסיסיים: חשבונית, רשימת אריזה ושטר מטען.",
       service="עמילות מכס", minutes="3 דקות קריאה",
       body="""<h2>מה עמיל מכס עושה בפועל</h2>
<p>כשסחורה נכנסת לישראל או יוצאת ממנה, צריך להגיש למכס דיווח. הדיווח כולל מה הסחורה, מה ערכה ומאיפה היא מגיעה. עמיל המכס מגיש את הדיווח בשמכם, ומוודא שהמס מחושב נכון.</p>
<ul><li>מסווג את המוצר לפי קוד HS, שממנו נגזרים המכס והמסים.</li><li>מחשב את המכס ואת המע"מ לפני שהסחורה מגיעה, כדי שלא יהיו הפתעות.</li><li>בודק אם המוצר דורש אישור או עמידה בתקן.</li><li>משחרר את הסחורה ומתאם את ההובלה ממסוף הנמל או שדה התעופה.</li></ul>
<h2>אילו מסמכים כדאי להכין</h2>
<ul><li><b>חשבונית מסחרית:</b> מי מוכר, מי קונה, מה נשלח ובכמה.</li><li><b>רשימת אריזה:</b> כמה קרטונים, מה בכל אחד וכמה הוא שוקל.</li><li><b>שטר מטען:</b> באוויר AWB ובים BL. המסמך שמוכיח מי זכאי לקבל את הסחורה.</li><li><b>תעודת מקור:</b> נדרשת לפעמים, ויכולה להוזיל מכס לפי הסכמי סחר.</li></ul>
<h2>הטעות הנפוצה</h2>
<p>מזמינים סחורה ורק אחר כך בודקים מה עולה המכס. כדאי לעשות את ההפך: לסווג את המוצר ולבדוק דרישות לפני ההזמנה. אז מחירה המלא ידוע מראש.</p>""",
       rel=["customs.html", "import.html", "article-fcl-lcl.html"]),
  dict(file="article-fcl-lcl.html", short="FCL או LCL: איך בוחרים", title="FCL או LCL: איך בוחרים בין מכולה שלמה למטען משותף | CargoTech",
       desc="ההבדל בין FCL ל-LCL בשילוח ימי, מתי כדאי כל אחד, וכלל אצבע פשוט להחלטה לפי נפח המטען.",
       h1="FCL או LCL: איך בוחרים", lead="בקצרה: FCL היא מכולה שלמה רק לכם. LCL היא מכולה משותפת, ואתם משלמים על הנפח שתפסתם.",
       tldr="מכולה של 20 רגל מכילה בערך 33 מטר מעוקב, ושל 40 רגל בערך 67. כשהנפח קטן, LCL חוסכת. כשהוא מתקרב לחצי מכולה ומעלה, כדאי להשוות גם מחיר FCL.",
       service="שילוח אווירי או ימי", minutes="3 דקות קריאה",
       body="""<h2>מה ההבדל</h2>
<p><b>FCL</b> (Full Container Load) היא מכולה שלמה שמיועדת רק למטען שלכם. <b>LCL</b> (Less than Container Load) היא מטען שנארז במכולה יחד עם מטענים של אחרים, ומחירה נקבע לפי הנפח במטר מעוקב (CBM).</p>
<h2>מתי LCL מתאימה</h2>
<ul><li>המטען קטן ולא ממלא מכולה.</li><li>אין לחץ זמן, כי אריזה משותפת והפרדה ביעד לוקחות קצת יותר.</li><li>רוצים לשלם רק על המקום שבו השתמשו.</li></ul>
<h2>מתי FCL מתאימה</h2>
<ul><li>הנפח גדול, וכלל האצבע הוא חצי מכולה ומעלה.</li><li>הסחורה רגישה, ופחות מגע וטיפול הם יתרון.</li><li>רוצים שהמטען יוסע ישר, בלי להמתין לאיסוף של מטענים אחרים.</li></ul>
<h2>איך מחליטים בפועל</h2>
<p>מחשבים את הנפח הכולל: אורך כפול רוחב כפול גובה של כל קרטון, כפול מספר הקרטונים. את המחשבון עשינו בשבילכם, בעמוד המחירון. אחר כך משווים הצעות גם ל-LCL וגם ל-FCL, כי ההפרש תלוי במסלול ובעונה.</p>""",
       rel=["shipping.html", "pricing.html", "article-volumetric-weight.html"]),
  dict(file="article-volumetric-weight.html", short="משקל נפחי", title="משקל נפחי: למה קרטון גדול וקל עולה כמו כבד | CargoTech",
       desc="איך מחשבים משקל נפחי ומשקל מחייב בקורייר ובהובלה אווירית, עם דוגמה מחושבת וטיפים להוזיל את המשלוח.",
       h1="משקל נפחי: למה קרטון גדול וקל עולה כמו כבד", lead="בקצרה: חברות ההובלה מחייבות לפי הגדול מבין המשקל האמיתי למשקל הנפחי.",
       tldr="משקל נפחי = אורך × רוחב × גובה בס״מ, חלקי 5000 בקורייר (ובהובלה אווירית רגילה לרוב חלקי 6000). המשקל המחייב הוא הגדול מבין המשקל האמיתי למשקל הנפחי.",
       service="קורייר", minutes="3 דקות קריאה",
       body="""<h2>למה זה קיים</h2>
<p>מטוס מוגבל גם במשקל וגם במקום. קרטון גדול וקל תופס הרבה מקום ומרוויח מעט, ולכן מחייבים אותו כאילו שקל יותר.</p>
<h2>הנוסחה</h2>
<p>אורך × רוחב × גובה (בסנטימטרים) ÷ מחלק. בקורייר המחלק לרוב 5000, ובהובלה אווירית רגילה לרוב 6000. המחלק מופיע בתנאי החברה, ולכן שווה לוודא.</p>
<h2>דוגמה</h2>
<p>שלושה קרטונים בגודל 60×40×40 ס"מ, כל אחד בן 8 ק"ג. המשקל האמיתי הוא 24 ק"ג. המשקל הנפחי הוא 57.6 ק"ג (96,000 × 3 ÷ 5000). מחייבים לפי 57.6.</p>
<h2>איך מוזילים</h2>
<ul><li>אורזים בקרטון שמתאים לסחורה, בלי חלל ריק.</li><li>מאחדים כמה חבילות קטנות לקרטון אחד כשאפשר.</li><li>משווים בין חברות, כי המחלק והתעריף שונים.</li></ul>
<div class="callout"><p>רוצים לראות את המספרים של המטען שלכם? המחשבון בעמוד המחירון עושה את זה בשניות.</p><a class="btn btn-go" href="pricing.html#calc">למחשבון המשקל</a></div>""",
       rel=["pricing.html", "courier.html", "article-fcl-lcl.html"]),
  dict(file="article-fda-prior-notice.html", short="Prior Notice של FDA", title="Prior Notice של FDA: מה זה ומי צריך להגיש | CargoTech",
       desc="הסבר על ההודעה המוקדמת ל-FDA עבור מזון שנשלח לארה״ב: מה זה, למה היא חשובה ומה כדאי להכין לפני המשלוח.",
       h1="Prior Notice של FDA: מה זה ומי צריך להגיש", lead="בקצרה: זו הודעה שמוגשת לרשות המזון האמריקאית לפני שמזון מגיע לארה״ב.",
       tldr="מזון שנכנס לארה״ב כפוף לדרישות ה-FDA, כולל הודעה מוקדמת שמוגשת לפני ההגעה. בלי הודעה המשלוח עלול להיעצר בגבול. הדרישות המדויקות משתנות לפי סוג המוצר ונבדקות לפני כל משלוח.",
       service='מזון לארה"ב (FDA)', minutes="3 דקות קריאה",
       body="""<h2>מה זה Prior Notice</h2>
<p>Prior Notice היא הודעה אלקטרונית שמוגשת ל-FDA על משלוח מזון לפני שהוא מגיע לארה״ב. היא מפרטת מה המוצר, מי היצרן, מי השולח ומי מקבל אותו.</p>
<h2>למה היא חשובה</h2>
<p>משלוח מזון שהגיע בלי הודעה מוקדמת עלול להיעצר בגבול או להידחות. לכן מגישים אותה בזמן, לפני שהמטען נוחת.</p>
<h2>מה עוד בודקים</h2>
<ul><li>האם נדרש רישום של מתקן המזון ב-FDA.</li><li>האם התיוג של המוצר עומד בדרישות האמריקאיות.</li><li>מי היבואן בארה״ב, שלעיתים נושא בחובות משלו, כמו תוכנית אימות ספקים (FSVP).</li></ul>
<h2>מתי להתחיל</h2>
<p>לפני שמזמינים הובלה. ככה סוגרים תיוג ואישורים בלי לחץ, והמשלוח לא מחכה בגבול.</p>
<div class="callout"><p>התקנות מתעדכנות, ולכן אנחנו בודקים את הדרישות מול המוצר שלכם לפני כל משלוח.</p><a class="btn btn-go" href="fda-food.html">לדף מזון לארה"ב</a></div>""",
       rel=["fda-food.html", "usa.html", "customs.html"]),
]
import json, glob
for _a in ARTICLES: _a.setdefault("cat", "guide")
for _f in sorted(glob.glob(os.path.join(SCR, "content", "part*.json"))):
    ARTICLES.extend(json.load(open(_f, encoding="utf-8")))
DEST = [a for a in ARTICLES if a["cat"] == "dest"]
GUIDES = [a for a in ARTICLES if a["cat"] == "guide"]
ART_BY_FILE = {a["file"]: a for a in ARTICLES}

SERVICES = {
 "import": dict(file="import.html", label="יבוא", title='יבוא מאירופה ומארה"ב | CargoTech', service="יבוא",
   desc="יבוא מאירופה ומארה״ב עם טיפול במסמכים, במכס ובהובלה עד הדלת. מסבירים בעברית פשוטה ומחשבים את העלות מראש.",
   h1="יבוא בלי הפתעות במכס", lead="מהספק בחו״ל ועד הכתובת שלכם: הובלה, מסמכים, מכס ותיאום. אתם מחליטים מה להזמין, אנחנו דואגים שזה יגיע.",
   inc_head="מה כלול ביבוא", inc_sub="הכל מתחיל לפני ההזמנה אצל הספק, כי שם נחסכות רוב הטעויות.",
   inc=["תיאום מול הספק בחו״ל ואיסוף הסחורה", "בחירת דרך ההובלה: אוויר, ים או קורייר", "הכנת המסמכים: חשבונית, רשימת אריזה ושטר מטען",
        "סיווג המוצר וחישוב מכס ומע״מ מראש", "בדיקת תקינה ואישורים לפני שמזמינים", "שחרור מהמכס והובלה עד הכתובת שלכם"],
   terms=[("HS Code", "מספר שמגדיר מה המוצר שלכם בעיני המכס. ממנו נגזרים המכס והמסים.", True),
          ("Incoterms", "כלל קצר שקובע מי משלם על מה ועד איפה: הובלה, ביטוח ומכס.", True),
          ("שטר מטען", "המסמך שמוכיח שהסחורה נמסרה להובלה ומי זכאי לקבל אותה. באוויר AWB, בים BL.", False)],
   steps=STD_STEPS(("שולחים פרטי הזמנה", "מה הוזמן, מאיפה, כמה, ומתי צריך אותו."), ("בודקים לפני שמזמינים", "דרישות תקינה, סיווג המוצר ועלות כוללת."),
                   ("מובילים ומשחררים", "איסוף מהספק, הובלה ושחרור מהמכס."), ("מוסרים לכתובת", "המטען מגיע אליכם ואתם מקבלים את המסמכים.")),
   faq=[("צריך רישיון או אישור כדי לייבא?", "זה תלוי במוצר. חלקם דורשים אישור או עמידה בתקן. בודקים את זה לפני ההזמנה, כדי לא לגלות אחרי שהסחורה כבר בדרך."),
        ("איך אדע כמה מס אשלם?", "המכס והמע״מ נקבעים לפי סוג המוצר וערכו. אחרי שמקבלים את פרטי המוצר מחשבים מראש, כדי שתדעו את העלות המלאה."),
        ("מה ההבדל בין יבוא אישי ליבוא מסחרי?", "ביבוא מסחרי מייבאים כדי למכור, והנהלים והמסמכים מחמירים יותר. נעזור לסווג נכון ולהכין את מה שצריך.")],
   rel=[("pricing.html", "מחירון ומחשבון משקל", "מה משפיע על המחיר, ואיך מחשבים משקל מחייב."), ("article-customs-broker.html", "מה זה עמילות מכס", "ההסבר הקצר, עם רשימת מסמכים."), ("customs.html", "עמילות מכס", "שחרור, סיווג וחישוב מסים.")]),
 "export": dict(file="export.html", label="יצוא", title='יצוא ללקוחות באירופה ובארה"ב | CargoTech', service="יצוא",
   desc="יצוא ללקוחות באירופה ובארה״ב: תיעוד, הובלה ותיאום עם הצוות בצד השני, בשפה פשוטה ובלי הפתעות.",
   h1="יצוא ללקוחות באירופה ובארה״ב", lead="אתם מוכרים, אנחנו דואגים שהסחורה תגיע. התיעוד, ההובלה והמכס ביעד מטופלים יחד עם הצוות בכל מדינה.",
   inc_head="מה כלול ביצוא", inc_sub="הלקוח בחו״ל מצפה לקבל את הסחורה בלי טפסים מיותרים. כך מגיעים לזה.",
   inc=["תיעוד יצוא: חשבונית, רשימת אריזה ותעודת מקור לפי הצורך", "בחירת הובלה: אוויר, ים או קורייר", "בדיקת הדרישות בארץ היעד לפני השילוח",
        "תיאום עם הצוות בצד השני: קבלה, מכס מקומי ומסירה", "הנחיות אריזה שמגינות על הסחורה בדרך", "מעקב ועדכונים עד המסירה"],
   terms=[("EORI", "מספר שמזהה עסק מול מכס האיחוד האירופי. לרוב הצד המייבא באירופה צריך אותו, ואנחנו בודקים מה נדרש בכל משלוח.", True),
          ("תעודת מקור", "מסמך שמוכיח איפה הסחורה יוצרה. הוא יכול להוזיל מכס ביעד לפי הסכמי סחר.", False),
          ("חשבונית מסחרית", "מפרטת מה נשלח, מי המוכר, מי הקונה ומה הערך. המכס ביעד מחשב ממנה מסים.", False)],
   steps=STD_STEPS(("מספרים מה ולאן", "מה המוצר, מי הקונה ולאיזו מדינה."), ("בודקים דרישות ביעד", "מסמכים, אישורים ומי משלם את המכס."),
                   ("שולחים ומשחררים", "הובלה, דיווח ושחרור בשני הצדדים."), ("מוסרים ללקוח", "הסחורה מגיעה ואתם מקבלים עדכון.")),
   faq=[("איך יודעים אילו מסמכים צריך?", "זה תלוי במוצר ובמדינת היעד. אחרי שמקבלים ממכם את הפרטים אנחנו מגדירים את רשימת המסמכים המלאה."),
        ("מי משלם את המכס ביעד?", "תלוי בתנאי המכירה (Incoterms). קובעים את זה מראש, כדי שלא יהיו הפתעות לאף צד."),
        ("אפשר לשלוח דוגמאות ללקוח?", "כן, אבל גם דוגמאות עוברות מכס וצריכות חשבונית. נסביר איך להצהיר נכון.")],
   rel=[("europe.html", "שילוח לאירופה", "מכס, מע״מ ו-EORI באיחוד האירופי."), ("usa.html", 'שילוח לארה"ב', "דרישות המכס האמריקאי."), ("shipping.html", "שילוח אווירי וימי", "איך בוחרים דרך הובלה.")]),
 "shipping": dict(file="shipping.html", label="שילוח אווירי וימי", title='שילוח אווירי וימי | CargoTech', service="שילוח אווירי או ימי",
   desc="שילוח אווירי, ימי וקורייר: השוואה בין הדרכים, הסבר על FCL ו-LCL ועל משקל נפחי, והצעה לפי המטען שלכם.",
   h1="שילוח אווירי וימי, לפי מה שחשוב לכם", lead="מחיר, מהירות או שילוב ביניהם. משווים בין אוויר, ים וקורייר לפי המטען שלכם, ובוחרים יחד.",
   inc_head="מה כלול בשילוח", inc_sub="הבחירה בדרך ההובלה היא ההחלטה שמשפיעה הכי הרבה על המחיר.",
   inc=["השוואה בין אוויר, ים וקורייר לפי משקל, נפח ודחיפות", "מכולה שלמה (FCL) או מטען משותף (LCL)", "איסוף והובלה עד הנמל או שדה התעופה",
        "מסמכי הובלה ושחרור במכס", "ביטוח מטען לפי ערך הסחורה", "מעקב ועדכונים עד המסירה"],
   terms=[("FCL / LCL", "FCL היא מכולה שלמה רק לכם. LCL היא מכולה משותפת, ואתם משלמים על הנפח שתפסתם.", True),
          ("משקל נפחי", "חברות אוויר מחייבות לפי הגדול מבין המשקל האמיתי לנפח. קרטון גדול וקל עולה כמו כבד.", False),
          ("CBM", "מטר מעוקב, היחידה שבה מודדים נפח של מטען בים.", True)],
   steps=STD_STEPS(("מספרים מה ולאן", "משקל, נפח, מסלול ותאריך שחשוב לכם."), ("מקבלים השוואה", "אוויר מול ים, FCL מול LCL, עם מחיר לכל אפשרות."),
                   ("בוחרים ואנחנו מטפלים", "הובלה, מסמכים ושחרור."), ("מעקב עד המסירה", "עדכונים לאורך הדרך.")),
   faq=[("מתי עדיף אוויר ומתי ים?", "אוויר כשהמטען קל, יקר ודחוף. ים כשהמטען כבד או גדול ולא לחוץ בזמן. בהצעה נציג את שתי האפשרויות אחת ליד השנייה."),
        ("האם כדאי לבטח?", "ביטוח מכסה נזק ואובדן בהובלה, ובדרך כלל כדאי לבטח סחורה בערך משמעותי. נציע לפי הערך."),
        ("כמה זמן זה לוקח?", "זה תלוי במסלול ובעונה. באוויר מדברים על ימים ובים על שבועות. בהצעה תקבלו הערכה למסלול שלכם.")],
   table=True,
   rel=[("article-fcl-lcl.html", "FCL או LCL", "איך בוחרים בין מכולה שלמה למטען משותף."), ("article-volumetric-weight.html", "משקל נפחי", "למה קרטון גדול וקל עולה כמו כבד."), ("pricing.html", "מחשבון משקל", "חישוב מהיר של משקל מחייב ונפח.")]),
 "courier": dict(file="courier.html", label="קורייר", title="קורייר לחבילות ומסמכים | CargoTech", service="קורייר",
   desc="קורייר לחבילות ומסמכים עם השוואה בין DHL, FedEx, UPS ו-Aramex, הכנת חשבונית מסחרית וחישוב משקל מחייב.",
   h1="קורייר לחבילות ומסמכים, עם השוואה בין החברות", lead="עובדים מול כל חברות הקורייר, ולכן בוחרים לפי מחיר ומהירות. אנחנו גם מכינים את המסמכים.",
   inc_head="מה כלול בקורייר", inc_sub="חבילה קטנה עדיין צריכה מסמכים נכונים. אנחנו דואגים לזה.",
   inc=["השוואה בין DHL, FedEx, UPS ו-Aramex", "תיאום איסוף מהכתובת ומסירה לנמען", "הכנת חשבונית מסחרית למשלוחים מסחריים",
        "חישוב משקל מחייב לפני שמזמינים", "מעקב בזמן אמת", "טיפול כשיש עיכוב או בעיה במכס"],
   terms=[("משקל מחייב", "הגדול מבין המשקל האמיתי למשקל הנפחי. לפיו מחושב המחיר.", False),
          ("חשבונית מסחרית", "מסמך שמפרט מה בחבילה ומה ערכו. בלעדיו משלוח מסחרי עלול להיתקע.", False),
          ("DAP / DDP", "ב-DAP הנמען משלם מכס ומסים בקבלה. ב-DDP השולח משלם מראש והנמען מקבל בלי הפתעות.", True)],
   steps=STD_STEPS(("מספרים מה שולחים", "מה בחבילה, לאן, כמה שוקל ומה המידות."), ("משווים ובוחרים", "מחיר וזמן מכל חברה."), ("מתאמים איסוף", "מכינים מסמכים ואורזים."), ("עוקבים עד המסירה", "עדכונים עד שהחבילה אצל הנמען.")),
   faq=[("מה ההבדל בין מסמכים לחבילה?", "מסמכים ללא ערך מסחרי עוברים בדרך כלל בלי מכס. חבילה עם מוצרים דורשת חשבונית מסחרית."),
        ("כמה זה עולה?", "תלוי במשקל המחייב, ביעד ובחברה. אחרי שמקבלים את הפרטים מציגים מחיר מכל חברה."),
        ("אפשר לשלוח נוזלים או סוללות?", "חלק מהפריטים מוגבלים או מסווגים כסחורה מסוכנת, כמו סוללות ליתיום ונוזלים. בודקים לפני האריזה.")],
   rel=[("article-volumetric-weight.html", "משקל נפחי", "למה קרטון גדול וקל עולה כמו כבד."), ("pricing.html", "מחשבון משקל", "חישוב משקל מחייב בשניות."), ("shipping.html", "שילוח אווירי וימי", "כשהמטען גדול יותר.")]),
 "fda": dict(file="fda-food.html", label='מזון לארה"ב', title='מזון לארה"ב: אישורי FDA והודעה מוקדמת | CargoTech', service='מזון לארה"ב (FDA)',
   desc="שולחים מזון לארה״ב? בדיקת דרישות FDA, הגשת הודעה מוקדמת (Prior Notice), תיוג ושילוח, עם ליווי בעברית.",
   h1='מזון לארה"ב: אישורי FDA והודעה מוקדמת', lead="מזון שנכנס לארה״ב כפוף לדרישות מיוחדות. אנחנו מטפלים באישורים ובהגשות, כדי שהמשלוח יגיע ולא ייתקע בגבול.",
   inc_head="מה כלול במשלוח מזון", inc_sub="הדרישות משתנות לפי המוצר, ולכן מתחילים בבדיקה.",
   inc=["בדיקת הדרישות לפי סוג המזון", "הגשת הודעה מוקדמת (Prior Notice) לפני שהמשלוח מגיע", "בירור רישום מתקן ותיוג לפי דרישות ה-FDA",
        "תיאום מול היבואן או הנמען בארה״ב", "מסמכי הובלה ושילוח לארה״ב", "מעקב עד המסירה"],
   terms=[("FDA", "רשות המזון והתרופות של ארה״ב. היא מפקחת על מזון שנכנס למדינה.", True),
          ("Prior Notice", "הודעה מוקדמת ל-FDA על משלוח מזון. בלעדיה המשלוח עלול להיעצר בגבול.", True),
          ("FSVP", "תוכנית אימות ספקים שהיבואן בארה״ב אחראי עליה. כדאי לתאם אותה איתו.", True)],
   steps=STD_STEPS(("מספרים מה המוצר", "סוג המזון, היצרן והיעד בארה״ב."), ("בודקים דרישות", "רישום, תיוג והודעה מוקדמת."), ("מגישים ומובילים", "הגשה לפני ההגעה, והובלה."), ("מוסרים ליעד", "המטען מגיע והמסמכים אצלכם.")),
   faq=[("מה קורה אם לא הוגשה הודעה מוקדמת?", "משלוח מזון בלי הודעה מוקדמת עלול להיעצר בגבול או להידחות. לכן מגישים לפני ההגעה."),
        ("אילו מזונות כפופים?", "באופן כללי מזון ומשקאות לצריכה, עם חריגים ודרישות נוספות לפי המוצר. בודקים לפי מה שאתם שולחים."),
        ("מתי כדאי להתחיל?", "לפני שמזמינים הובלה. כך סוגרים דרישות ותיוג בלי לחץ.")],
   callout="התקנות מתעדכנות, ולכן הדרישות המדויקות נבדקות מול המוצר שלכם לפני כל משלוח.",
   rel=[("article-fda-prior-notice.html", "Prior Notice של FDA", "ההסבר הקצר, בעברית."), ("usa.html", 'שילוח לארה"ב', "המכס האמריקאי, בקצרה."), ("customs.html", "עמילות מכס", "סיווג ומסמכים.")]),
 "customs": dict(file="customs.html", label="עמילות מכס", title="עמילות מכס: שחרור, סיווג וחישוב מסים | CargoTech", service="עמילות מכס",
   desc="עמילות מכס ליבוא וליצוא: סיווג המוצר, חישוב מכס ומע״מ, ייצוג מול המכס ושחרור הסחורה, עם הסבר בעברית פשוטה.",
   h1="עמילות מכס: מי שמדבר עם המכס במקומכם", lead="מסמכים, סיווג ותשלומים ללא כאב ראש. אתם מקבלים מחיר מראש ושחרור בזמן.",
   inc_head="מה כלול בעמילות מכס", inc_sub="הטעות הכי יקרה בתחום היא סיווג שגוי. מונעים אותה לפני שהסחורה יוצאת.",
   inc=["סיווג המוצר לפי HS Code", "חישוב מכס ומע״מ לפני ההגעה", "ייצוג מול רשויות המכס", "בדיקת תקינה ואישורים", "הכנת מסמכי יבוא ויצוא", "שחרור הסחורה ותיאום הובלה"],
   terms=[("סיווג HS", "קוד שמגדיר מה המוצר בעיני המכס. ממנו נגזרים המכס והמסים.", True),
          ("ייפוי כוח", "מסמך שמאשר לעמיל לפעול מול המכס בשמכם.", False),
          ("תעודת מקור", "מוכיחה איפה הסחורה יוצרה, ויכולה להוזיל מכס לפי הסכמי סחר.", False)],
   steps=STD_STEPS(("שולחים מסמכים", "חשבונית, רשימת אריזה ושטר מטען."), ("מסווגים ומחשבים", "קוד HS, מכס ומע״מ."), ("מגישים ומשחררים", "דיווח למכס ושחרור."), ("מוסרים", "תיאום הובלה אל הכתובת.")),
   faq=[("האם חייבים עמיל מכס?", "רוב היבואנים והיצואנים עובדים עם עמיל מורשה, כי הנהלים והדיווחים מורכבים וטעות עולה כסף."),
        ("אילו מסמכים מכינים?", "חשבונית מסחרית, רשימת אריזה ושטר מטען. לפעמים גם תעודת מקור ואישורי תקינה."),
        ("מה אם הסיווג שגוי?", "סיווג שגוי עלול להוביל לתשלום מסים שונה, לעיכוב ולקנס. לכן מסווגים לפני שהסחורה יוצאת.")],
   rel=[("article-customs-broker.html", "מה זה עמילות מכס", "ההסבר הקצר."), ("import.html", "יבוא", "מהספק ועד הדלת."), ("export.html", "יצוא", "תיעוד והובלה ללקוחות בחו״ל.")]),
 "europe": dict(file="europe.html", label="אירופה", title="שילוח לאירופה ומאירופה | CargoTech", service="עדיין לא יודע",
   desc="יבוא ויצוא לכל אירופה עם צוות מקומי בכל מדינה: מכס, מע״מ, EORI ותעודת מקור, בהסבר פשוט.",
   h1="שילוח לאירופה ומאירופה", lead="בכל מדינה עובדים אתנו הצוותים הנכונים: מי שמקבל את המטען, מטפל במכס המקומי ומוסר ליעד.",
   inc_head="מה כלול באירופה", inc_sub="אירופה היא כמה מדינות עם כללים שונים. את זה אנחנו מנהלים בשבילכם.",
   inc=["צוות מקומי בכל מדינה: קבלה, מכס מקומי ומסירה", "יבוא מספקים באירופה לישראל", "יצוא לקונים באיחוד האירופי",
        "בדיקת דרישות: מע״מ, EORI ותעודת מקור", "קורייר, אוויר וים לפי הצורך", "מעקב ועדכונים עד המסירה"],
   terms=[("EORI", "מספר שמזהה עסק מול מכס האיחוד האירופי. בודקים מי צריך אותו בכל משלוח.", True),
          ("VAT", "מע״מ אירופי. מחושב בכניסת הסחורה, ושיעורו שונה בכל מדינה.", True),
          ("תעודת מקור", "יכולה להוזיל מכס לפי הסכם הסחר בין ישראל לאיחוד האירופי, כשהמוצר עומד בתנאים.", False)],
   steps=STD_STEPS(("מספרים מאיפה לאן", "מדינת מוצא, מדינת יעד ומה המטען."), ("בודקים דרישות", "מסמכים, מע״מ ואישורים."), ("מובילים ומשחררים", "עם הצוות המקומי."), ("מוסרים", "המטען מגיע והמסמכים אצלכם.")),
   faq=[("צריך להירשם כדי לייצא לאירופה?", "לרוב הצד המייבא צריך מספר EORI. בודקים מה נדרש בכל משלוח ומי אחראי עליו."),
        ("מי משלם מע״מ באירופה?", "בדרך כלל מחושב בכניסה, ומי שמשלם תלוי בתנאי המכירה. קובעים מראש."),
        ("אפשר לשלוח לכמה מדינות יחד?", "כן. נבנה תוכנית לפי המטען והיעדים, ונציג מחיר לכל מסלול.")],
   rel=[("export.html", "יצוא", "תיעוד והובלה ללקוחות בחו״ל."), ("import.html", "יבוא", "מהספק ועד הדלת."), ("pricing.html", "מחשבון משקל", "חישוב מהיר.")]),
 "usa": dict(file="usa.html", label='ארה"ב', title='שילוח לארה"ב ומארה"ב | CargoTech', service="עדיין לא יודע",
   desc="יבוא ויצוא בין ישראל לארה״ב: מכס אמריקאי, ISF בהובלה ימית, ואישורי FDA למזון, עם ליווי בעברית.",
   h1='שילוח לארה"ב ומארה"ב', lead="יבוא, יצוא ומזון לארה״ב, עם צוות שמכיר את הדרישות בשני הצדדים.",
   inc_head='מה כלול בארה"ב', inc_sub="שוק גדול עם כללים מדויקים. מכינים אותם מראש.",
   inc=["יבוא מספקים בארה״ב לישראל", "יצוא ללקוחות בארה״ב", "אישורי FDA והודעה מוקדמת למזון", "דרישות המכס האמריקאי והצהרות נדרשות",
        "אוויר, ים וקורייר לפי הצורך", "תיאום מול הצוות בארה״ב"],
   terms=[("CBP", "רשות המכס וההגנה על הגבולות של ארה״ב. מולה מתבצע השחרור.", True),
          ("ISF", "הצהרה מוקדמת שהיבואן בארה״ב מגיש על מטען ימי, לפני שהוא יוצא לדרך.", True),
          ("Prior Notice", "הודעה מוקדמת ל-FDA על מזון שמגיע לארה״ב.", True)],
   steps=STD_STEPS(("מספרים מה ולאן", "מה המטען, מי היבואן ומה המסלול."), ("בודקים דרישות", "מכס, ISF למטען ימי, ו-FDA למזון."), ("מובילים ומשחררים", "הובלה ושחרור בארה״ב."), ("מוסרים", "המטען מגיע ליעד.")),
   faq=[("אפשר לשלוח מזון לארה״ב?", "כן, בכפוף לדרישות ה-FDA. אנחנו מטפלים באישורים ובהודעה המוקדמת."),
        ("מה זה ISF?", "הצהרה מוקדמת למכס האמריקאי על מטען ימי. היבואן בארה״ב מגיש אותה לפני שהסחורה יוצאת לדרך."),
        ("כמה זמן לוקח המשלוח?", "תלוי בדרך ההובלה ובעונה. נציג הערכה לכל מסלול בהצעה.")],
   rel=[("fda-food.html", 'מזון לארה"ב', "FDA והודעה מוקדמת."), ("export.html", "יצוא", "תיעוד והובלה."), ("shipping.html", "שילוח אווירי וימי", "איך בוחרים.")]),
}

# ------------- page builders -------------
def service_page(s):
    b = phero(s["label"], s["h1"], s["lead"], s["service"])
    inc = checks(s["inc"]) + cta()
    b += sec(s["inc_head"], s["inc_sub"], inc)
    if s.get("table"):
        t = ('<div class="tscroll"><table class="cmp"><thead><tr><th>דרך הובלה</th><th>מהירות</th><th>עלות</th><th>מתאימה ל</th></tr></thead><tbody>'
             '<tr><th>אוויר</th><td>הכי מהירה, מדברים על ימים</td><td>גבוהה יותר לק״ג</td><td>מטען קל, יקר ודחוף</td></tr>'
             '<tr><th>ים</th><td>איטית יותר, מדברים על שבועות</td><td>חסכונית לכמויות ולמטען כבד</td><td>נפח גדול, בלי לחץ זמן</td></tr>'
             '<tr><th>קורייר</th><td>מהירה, מדלת לדלת</td><td>מתאימה לחבילות קטנות</td><td>חבילות ומסמכים</td></tr></tbody></table></div>')
        b += sec("אוויר, ים או קורייר", "שלוש דרכים, ולכל אחת מקום. הנה ההבדל בקצרה.", t + cta("בדקו מה מתאים למטען שלכם"), cls="sec services")
    b += sec("במילים פשוטות", "שלושה מונחים שכדאי להכיר לפני שמתחילים.", terms(s["terms"], s["service"]), cls=("sec" if s.get("table") else "sec services"))
    if s.get("callout"):
        b += '<section class="sec" style="padding-block:0 8px"><div class="wrap"><div class="callout" style="margin:0"><p>%s</p><a class="btn btn-go" href="#quote">בדקו את המוצר שלכם</a></div></div></section>' % s["callout"]
    b += sec("ארבעה שלבים, בלי הפתעות", "את השלב השלישי עושים אנחנו.", steps(s["steps"]) + cta(), cls=("sec services" if s.get("table") else "sec"))
    b += sec("שאלות נפוצות", "", faq(s["faq"]) + '<div class="faq-cta"><p>יש שאלה אחרת?</p><a class="btn btn-go" data-wa="שלום CargoTech, יש לי שאלה על %s." href="https://wa.me/" target="_blank" rel="noopener">שאלו אותנו בוואטסאפ</a></div>' % esc(s["service"]), cls=("sec" if s.get("table") else "sec services"), style="border-bottom:0")
    b += sec("עוד שירותים ומדריכים", "", related(s["rel"]))
    b += quote_section(s["service"], "יש לכם מטען? מתחילים בשיחה.", "ספרו לנו מה אתם רוצה להעביר, ונחזור עם הצעה ועם הסבר על כל מה שצריך לדעת.")
    return doc(s["title"], s["desc"], {"import": "import", "export": "export", "shipping": "shipping"}.get(s["file"].split(".")[0], ""), b)

def article_page(a):
    rel = [(r, ART_BY_FILE[r]["short"], ART_BY_FILE[r]["lead"]) if r in ART_BY_FILE else None for r in a["rel"]]
    rel = [x for x in rel if x]
    other = {"customs.html": ("customs.html", "עמילות מכס", "שחרור, סיווג וחישוב מסים."), "import.html": ("import.html", "יבוא", "מהספק ועד הדלת."),
             "shipping.html": ("shipping.html", "שילוח אווירי וימי", "איך בוחרים דרך הובלה."), "pricing.html": ("pricing.html", "מחשבון משקל", "חישוב מהיר."),
             "courier.html": ("courier.html", "קורייר", "חבילות ומסמכים."), "fda-food.html": ("fda-food.html", 'מזון לארה"ב', "FDA והודעה מוקדמת."),
             "usa.html": ("usa.html", 'שילוח לארה"ב', "המכס האמריקאי."),
             "europe.html": ("europe.html", "שילוח לאירופה", "צוות בכל מדינה."), "export.html": ("export.html", "יצוא", "מהארץ אל העולם."),
             "glossary.html": ("glossary.html", "מילון מונחים", "המילים הקשות בעברית פשוטה.")}
    rel = []
    for r in a["rel"]:
        if r in ART_BY_FILE: rel.append((r, ART_BY_FILE[r]["short"], ART_BY_FILE[r]["lead"]))
        elif r in other: rel.append(other[r])
    b = ('<section class="phero"><div class="wrap">%s<h1>%s</h1><p class="lead">%s</p><span class="meta" style="color:var(--on-ink-muted)">%s</span></div></section>'
         % ('<div class="crumbs"><a class="backlink" href="index.html">→ חזרה לדף הראשי</a><span> / <a href="articles.html%s">%s</a></span></div>' % (("#dest", "יעדים") if a["cat"] == "dest" else ("#guides", "מדריכים")), a["h1"], a["lead"], a["minutes"]))
    b += '<section class="sec"><div class="wrap"><div class="tldr"><b>בקצרה</b>%s</div><div class="prose">%s</div>' % (a["tldr"], a["body"])
    b += '<div class="callout" style="max-width:42em"><p>רוצים שנבדוק את זה בשביל המטען שלכם?</p><a class="btn btn-go" href="#quote">קבלו הצעת מחיר</a></div></div></section>'
    faq = a.get("faq") or []
    if faq:
        items = "".join('<details class="qa"><summary>%s</summary><p>%s</p></details>' % (esc(f["q"]), esc(f["a"])) for f in faq)
        b = b.replace('<div class="callout" style="max-width:42em">', '<div class="prose faq"><h2>שאלות נפוצות</h2>%s</div><div class="callout" style="max-width:42em">' % items, 1)
    b += sec("עוד לקריאה", "", related(rel), cls="sec services")
    b += quote_section(a["service"], "יש שאלה? נענה עליה.", "ספרו לנו מה המטען, ונחזור עם תשובה והצעה.")
    d = doc(a["title"], a["desc"], "articles", b)
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": a["h1"], "description": a["desc"], "inLanguage": "he",
           "author": {"@type": "Organization", "name": "CargoTech"}, "publisher": {"@type": "Organization", "name": "CargoTech"}}]
    if faq:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": "he",
                   "mainEntity": [{"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in faq]})
    tag = "".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in ld)
    return d.replace("</head>", tag + "</head>", 1)

def articles_page():
    card = lambda a: '<a href="%s"><b>%s</b><span>%s</span></a>' % (a["file"], esc(a["short"]), a["lead"])
    b = ('<section class="phero"><div class="wrap">%s<h1>מדריכים ויעדים בעברית פשוטה</h1><p class="lead">כל יעד וכל מונח שמפחיד בתחום, בהסבר של כמה דקות.</p></div></section>'
         % '<div class="crumbs"><a class="backlink" href="index.html">→ חזרה לדף הראשי</a><span> / מדריכים</span></div>')
    b += '<div id="dest"></div>' + sec("שילוח לפי יעד", "לאן שולחים, מה המכס שם ומה כדאי להכין.", '<div class="rel">%s</div>' % "".join(card(a) for a in DEST))
    b += '<div id="guides"></div>' + sec("מדריכים", "מסמכים, מכס, שילוח ומזון לארה\"ב.", '<div class="rel">%s</div>' % "".join(card(a) for a in GUIDES) + cta("יש שאלה שלא מופיעה כאן? שאלו אותנו"))
    b += quote_section("עדיין לא יודע", "מה עוד תרצו להבין?", "ספרו לנו על השאלה שלכם, ונענה בעברית פשוטה.")
    return doc("מדריכים ויעדי שילוח בעברית פשוטה | CargoTech", "מדריכים על יבוא, יצוא, מכס, FDA ושילוח לפי יעד, בעברית פשוטה וללא מונחים מפחידים.", "articles", b)

def pricing_page():
    b = ('<section class="phero"><div class="wrap">%s<h1>מחירון: מה משפיע על המחיר, ואיך מחשבים משקל מחייב</h1>'
         '<p class="lead">במקום מחירון קבוע שמתיישן, אתם מקבלים הצעה ברורה לפי המטען. ובינתיים, המחשבון הזה אומר לכם לפי מה יחייבו אתכם.</p>'
         '<div class="cta-row"><a class="btn btn-go" href="#quote">קבלו הצעת מחיר</a><a class="btn btn-line" href="#calc">למחשבון</a></div></div></section>') % '<div class="crumbs"><a href="index.html">דף הבית</a> / מחירון</div>'
    b += sec("מה משפיע על המחיר", "אלה הגורמים שמופיעים בכל הצעה.", checks([
        "משקל ונפח של המטען", "מסלול: ממה לאן", "דרך ההובלה: אוויר, ים או קורייר", "דחיפות ותאריך יעד",
        "סוג הסחורה: מזון, שביר או מסוכן", "שירותים נוספים: מכס, ביטוח ואישורים"]) + cta())
    calc = ('<div class="calc" id="calc"><div class="inputs">'
            '<div class="field"><label for="c-l">אורך (ס״מ)</label><input id="c-l" type="number" inputmode="decimal" min="0" value="60"></div>'
            '<div class="field"><label for="c-w">רוחב (ס״מ)</label><input id="c-w" type="number" inputmode="decimal" min="0" value="40"></div>'
            '<div class="field"><label for="c-h">גובה (ס״מ)</label><input id="c-h" type="number" inputmode="decimal" min="0" value="40"></div>'
            '<div class="field"><label for="c-n">מספר קרטונים</label><input id="c-n" type="number" inputmode="numeric" min="1" value="3"></div>'
            '<div class="field"><label for="c-kg">משקל לקרטון (ק״ג)</label><input id="c-kg" type="number" inputmode="decimal" min="0" value="8"></div>'
            '<div class="field"><label for="c-div">מחלק</label><select id="c-div"><option value="5000">5000 (קורייר)</option><option value="6000">6000 (אוויר)</option></select></div>'
            '<p class="ex">הערכים שמולאו הם דוגמה. החליפו אותם במידות של המטען שלכם. המחלק המדויק מופיע בתנאי החברה שמובילה.</p></div>'
            '<div class="result" aria-live="polite"><div><span class="meta" style="color:var(--on-ink-muted)">משקל מחייב</span>'
            '<div class="big" id="r-charge">0 <small>ק״ג</small></div></div>'
            '<dl><div><dt>משקל נפחי</dt><dd id="r-vol">0</dd></div><div><dt>משקל אמיתי</dt><dd id="r-real">0</dd></div><div><dt>נפח</dt><dd id="r-cbm">0</dd></div></dl>'
            '<p class="why" id="r-why"></p>'
            '<a class="btn btn-go" id="calc-cta" href="https://wa.me/" target="_blank" rel="noopener">שלחו לנו את החישוב וקבלו הצעה</a></div></div>')
    b += sec("מחשבון משקל מחייב", "משקל נפחי מול משקל אמיתי, ונפח במטר מעוקב.", calc, cls="sec services", style="scroll-margin-top:80px")
    b += sec("מה תקבלו בהצעה", "", checks(["מחיר ברור לכל אפשרות הובלה", "מה כלול ומה לא", "זמן משוער למסלול שלכם", "הסבר על המסמכים שצריך להכין"]) + cta())
    b += sec("עוד לקריאה", "", related([("article-volumetric-weight.html", "משקל נפחי", "הנוסחה, עם דוגמה."), ("article-fcl-lcl.html", "FCL או LCL", "איך בוחרים."), ("shipping.html", "שילוח אווירי וימי", "השוואה בין הדרכים.")]), cls="sec services")
    b += quote_section("עדיין לא יודע", "רוצים מחיר למטען שלכם?", "שלחו את הפרטים ונחזור עם הצעה ברורה.")
    return doc("מחירון ומחשבון משקל מחייב | CargoTech", "מה משפיע על מחיר שילוח בינלאומי, ומחשבון חינמי למשקל נפחי, משקל מחייב ונפח במטר מעוקב.", "pricing", b)

def contact_page():
    b = ('<section class="phero"><div class="wrap">%s<h1>יש לכם מטען? מתחילים בשיחה</h1><p class="lead">המילים קשות. הדרך פשוטה. הכל אפשרי. ספרו לנו מה אתם רוצה להעביר, ונחזור עם הצעה.</p></div></section>'
         % '<div class="crumbs"><a href="index.html">דף הבית</a> / צור קשר</div>')
    b += quote_section("עדיין לא יודע", "נשמח לשמוע מכם", "טופס קצר, וואטסאפ או טלפון. בחרו מה נוח לכם.")
    b += sec("פרטי קשר", "", '<div class="contact-lines" style="color:var(--fg)"><div><span style="color:var(--muted)">טלפון</span><b class="latin" data-phone>05X-XXX-XXXX</b></div><div><span style="color:var(--muted)">אימייל</span><b class="latin" data-email>office@your-domain.co.il</b></div></div>')
    return doc("צור קשר | CargoTech", "צרו קשר עם CargoTech לקבלת הצעת מחיר ליבוא, יצוא ושילוח בינלאומי לאירופה ולארה״ב.", "contact", b)

def glossary_page():
    parts = [p for p in re.split(r'(?=<section)', MAIN_HTML) if p.strip()]
    mid = "".join([parts[1], parts[3], parts[5], parts[6]])
    hero = ('<section class="phero"><div class="wrap">%s<h1>המילים קשות, הדרך פשוטה</h1><p class="lead">מילון מונחים, ארבעת השלבים ושאלות שכולם שואלים.</p>'
            '<div class="cta-row"><a class="btn btn-go" href="#quote">קבלו הצעת מחיר</a></div></div></section>') % crumbs("מילון")
    return doc("מילון מונחי שילוח ושאלות נפוצות | CargoTech", "מונחים כמו Incoterms, HS Code ו-FCL בעברית פשוטה, ארבעת שלבי התהליך ותשובות לשאלות נפוצות.", "glossary", hero + mid + quote_section("עדיין לא יודע", "עדיין לא ברור? נסביר", "ספרו מה שולחים ואנחנו נתרגם הכל לעברית."))

VIDEO_URL = os.environ.get("HERO_VIDEO", "")
POSTER_URL = os.environ.get("HERO_POSTER", "https://d8j0ntlcm91z4.cloudfront.net/user_37HsBZKzp3azVbNUBQIhUBwn3eG/hf_20260930_190759_42bd3539-b232-41b8-9565-33675ecfe640.png")

def index_page(full):
    body = MAIN_HTML
    # service cards -> add page links
    links = {"יבוא": "import.html", "יצוא": "export.html", "שילוח אווירי או ימי": "shipping.html", "קורייר": "courier.html",
             'מזון לארה&quot;ב (FDA)': "fda-food.html", "עמילות מכס": "customs.html"}
    for k, h in links.items():
        body = body.replace('<button class="go" data-service="%s" type="button">' % k, '<a class="more" href="%s">לפרטים נוספים</a><button class="go" data-service="%s" type="button">' % (h, k))
    # destination links
    body = body.replace('<a class="btn btn-go" href="#quote">בדקו את המסלול שלכם</a>',
                        '<a class="btn btn-go" href="#quote">בדקו את המסלול שלכם</a> <a class="more" style="color:var(--on-ink);margin-inline-start:16px" href="europe.html">אירופה</a> <a class="more" style="color:var(--on-ink)" href="usa.html">ארה"ב</a>')
    # remove the original header's anchors (header replaced by doc()), add teaser before final
    cards = "".join('<a href="%s"><b>%s</b><span>%s</span></a>' % (a["file"], esc(a["short"]), a["lead"]) for a in ARTICLES)
    teaser = ('<section class="sec"><div class="wrap"><div class="sec-head"><h2>מדריכים בעברית פשוטה</h2><p>כל מונח שמפחיד בתחום, בהסבר של שתי דקות.</p></div>'
              '<div class="rel" style="grid-template-columns:repeat(2,minmax(0,1fr))">%s</div>'
              '<div style="margin-top:28px"><a class="btn btn-line-dark" href="articles.html">לכל המדריכים</a></div></div></section>') % cards
    wiz_html = wizard.WIZ_HTML.replace('%(cities)s', "".join('<option value="%s">' % c for c in wizard.CITIES))
    body = re.sub(r'<div class="qcard" id="quote">.*?</form>\s*</div>', lambda m: wiz_html, body, count=1, flags=re.S)
    body += '<script>' + wizard.WIZ_JS.replace('%(countries)s', json.dumps(wizard.COUNTRIES, ensure_ascii=False)) + '</script>'
    parts = [p for p in re.split(r'(?=<section|<script)', body) if p.strip()]
    wsc = parts.pop() if parts[-1].startswith('<script') else ''
    check = ('<section class="sec"><div class="wrap"><div class="chk"><div><h2>רוצים להביא מוצר? בדקו מה נדרש</h2>'
             '<p>הקלידו שם מוצר וראו אילו דרישות חוקיות חלות עליו. את המיסים נחשב יחד.</p></div>'
             '<a class="btn btn-go" href="data.html">בדיקת יבוא לפי מוצר</a></div></div></section>')
    keep = [parts[0], check, parts[2], parts[4], parts[-1]]   # hero, services, destinations, final CTA
    body = "".join(keep) + wsc
    if VIDEO_URL:
        body = body.replace('<section class="hero">', '<section class="hero"><video class="hero-video" autoplay muted loop playsinline preload="metadata" poster="%s" aria-hidden="true" tabindex="-1"><source src="%s" type="video/mp4"></video><span class="hero-shade" aria-hidden="true"></span>' % (POSTER_URL, VIDEO_URL), 1)
    lanes = ('<div class="lanes"><div class="wrap"><a href="import.html"><i>01</i><span>יבוא</span></a>'
             '<a href="export.html"><i>02</i><span>יצוא</span></a><a href="shipping.html"><i>03</i><span>שילוח אווירי וימי</span></a></div></div>')
    body = body.replace('</section>', lanes + '</section>', 1)
    return doc("CargoTech", "יבוא, יצוא ושילוח בינלאומי לאירופה ולארה״ב, עם הסברים בעברית פשוטה וטיפול מלא במכס, במסמכים ובאישורי FDA.", "", body, full=full)

DATA_CSS = r"""
.dtools { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 12px; align-items: end; margin-bottom: 16px; }
.dtools .btn { min-height: 48px; }
.dmeta { color: var(--muted); font-size: .95rem; margin-bottom: 12px; min-height: 1.6em; }
.dtable-wrap { overflow-x: auto; border: 1px solid var(--line); border-radius: 12px; background: var(--surface); max-height: 70vh; }
table.dt { border-collapse: collapse; width: 100%; min-width: 640px; }
.dt th, .dt td { padding: 12px 14px; text-align: right; border-bottom: 1px solid var(--line); vertical-align: top; font-size: .98rem; }
.dt thead th { position: sticky; top: 0; background: var(--bg); color: var(--sea); font-weight: 800; white-space: nowrap; z-index: 1; }
.dt td { font-variant-numeric: tabular-nums; }
.dpager { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 12px; margin-top: 16px; }
.dstate { padding: 28px 22px; text-align: center; color: var(--muted); }
.dstate b { display: block; color: var(--fg); margin-bottom: 6px; font-size: 1.1rem; }
.dstate .btn { margin-top: 14px; }
@media (max-width: 600px) { .dtools { grid-template-columns: minmax(0, 1fr); } }
"""

DATA_JS = r"""
(function () {
  var CFG = { proxy: "/api/govdata", api: "https://data.gov.il/api/3/action/datastore_search", resource: "a36db570-09f2-4521-8e3d-0290eb839c68", pageSize: 20 };
  var head = document.getElementById("d-head"), body = document.getElementById("d-body"), meta = document.getElementById("d-meta"),
      state = document.getElementById("d-state"), q = document.getElementById("d-q"), form = document.getElementById("d-form"),
      prev = document.getElementById("d-prev"), next = document.getElementById("d-next"), pos = document.getElementById("d-pos"), wrap = document.getElementById("d-wrap");
  var offset = 0, total = 0, cols = null, ticket = 0;
  function showState(title, text, retry) {
    wrap.hidden = true; state.hidden = false; state.innerHTML = "";
    var b = document.createElement("b"); b.textContent = title; state.appendChild(b);
    var p = document.createElement("span"); p.textContent = text; state.appendChild(p);
    if (retry) { var r = document.createElement("button"); r.type = "button"; r.className = "btn btn-go btn-sm"; r.textContent = "נסו שוב"; r.addEventListener("click", load); state.appendChild(document.createElement("br")); state.appendChild(r); }
  }
  function load() {
    var my = ++ticket;
    meta.textContent = "טוען נתונים...";
    showState("טוען נתונים", "זה לוקח כמה שניות.", false);
    var qs = "?resource_id=" + encodeURIComponent(CFG.resource) + "&limit=" + CFG.pageSize + "&offset=" + offset + (q.value.trim() ? "&q=" + encodeURIComponent(q.value.trim()) : "");
    var get = function (u) { return fetch(u).then(function (r) { if (!r.ok) throw new Error("http " + r.status); return r.json(); }); };
    (/^https?:$/.test(location.protocol) ? get(CFG.proxy + qs).catch(function () { return get(CFG.api + qs); }) : get(CFG.api + qs)).then(function (j) {
      if (my !== ticket) return;
      if (!j.success || !j.result) throw new Error("bad payload");
      var res = j.result, recs = res.records || [];
      total = res.total || 0;
      if (!cols) cols = (res.fields || []).map(function (f) { return f.id; }).filter(function (id) { return id !== "_id" && id !== "_full_text"; });
      if (!cols.length && recs.length) cols = Object.keys(recs[0]).filter(function (id) { return id !== "_id" && id !== "_full_text"; });
      if (!recs.length) { showState("לא נמצאו תוצאות", "נסו מילת חיפוש אחרת.", false); meta.textContent = ""; pos.textContent = ""; prev.disabled = true; next.disabled = true; return; }
      head.innerHTML = ""; var tr = document.createElement("tr");
      cols.forEach(function (c) { var th = document.createElement("th"); th.scope = "col"; th.textContent = c; tr.appendChild(th); });
      head.appendChild(tr);
      body.innerHTML = "";
      recs.forEach(function (rec) { var row = document.createElement("tr"); cols.forEach(function (c) { var td = document.createElement("td"); var v = rec[c]; td.textContent = (v === null || v === undefined) ? "" : String(v); row.appendChild(td); }); body.appendChild(row); });
      state.hidden = true; wrap.hidden = false;
      var from = offset + 1, to = offset + recs.length;
      meta.textContent = "מציג " + from.toLocaleString("he-IL") + " עד " + to.toLocaleString("he-IL") + " מתוך " + total.toLocaleString("he-IL") + " רשומות";
      pos.textContent = "עמוד " + (Math.floor(offset / CFG.pageSize) + 1).toLocaleString("he-IL");
      prev.disabled = offset === 0; next.disabled = to >= total;
    }).catch(function () {
      if (my !== ticket) return;
      meta.textContent = "";
      showState("לא הצלחנו לטעון את הנתונים", "ייתכן שהמקור לא זמין כרגע. אפשר לנסות שוב בעוד רגע.", true);
    });
  }
  form.addEventListener("submit", function (e) { e.preventDefault(); offset = 0; load(); });
  prev.addEventListener("click", function () { offset = Math.max(0, offset - CFG.pageSize); load(); });
  next.addEventListener("click", function () { offset += CFG.pageSize; load(); });
  load();
})();
"""

import datatool
def data_page():
    h = ('<section class="phero"><div class="wrap">%s<h1>בדיקת יבוא לפי מוצר</h1><p class="lead">הקלידו מה רוצים להביא, וראו אילו דרישות חוקיות חלות עליו. את השאר, כולל המיסים, נבדוק יחד.</p></div></section>'
         % crumbs("בדיקת יבוא"))
    b = h + '<section class="sec"><div class="wrap">' + datatool.tool_html(esc) + '</div></section>'
    b += quote_section("עדיין לא יודע", "צריכים עזרה עם הבדיקה?", "ספרו לנו מה אתם מחפשים, ונעזור לכם להבין מה נדרש.")
    d = doc("בדיקת יבוא לפי מוצר | CargoTech", "חיפוש מוצר וראיית הדרישות החוקיות ליבוא שלו, מתוך מאגר ממשלתי, בעברית פשוטה.", "", b)
    d = d.replace("</style>", datatool.TOOL_CSS + "</style>", 1).replace("</script></body>", "</script><script>" + datatool.TOOL_JS + "</script></body>")
    return d


import authkit, orderflow, backoffice, bo2
AUTH_BITS = authkit.AUTH_HTML
def private_page(title, desc, body, css, js, noindex=True):
    d = doc(title, desc, "", body + authkit.AUTH_HTML, bar=False, noindex=noindex, css_extra=authkit.AUTH_CSS + css,
            js_extra="<script>" + authkit.AUTH_JS + "</script><script>" + js + "</script>")
    return d

def order_page():
    body = orderflow.ORDER_HTML.replace("%(crumbs)s", crumbs("הזמנת משלוח"))
    js = orderflow.ORDER_JS.replace("%(countries)s", json.dumps(wizard.COUNTRIES, ensure_ascii=False))
    return private_page("הזמנת משלוח בינלאומי | CargoTech", "קבלו מחיר למשלוח בינלאומי, מלאו פרטים ושלחו הזמנה. אפשר להזמין בלי להירשם.", body, orderflow.ORDER_CSS, js, noindex=False)

def admin_page():
    # the back office lives on its own site (its own address); it has no public menu, no public footer and no public scripts
    brand = '<div class="bo-top"><div class="wrap"><b class="bo-brand">CARGO<span>TECH</span></b><span class="bo-tag">בק-אופיס</span></div></div>'
    body = bo2.BX_HTML
    css = bo2.BX_CSS + "#authdlg .atabs{display:none}"
    d = doc("Back office | CargoTech", "Orders, users, payments and settings.", "", body + authkit.AUTH_HTML, bar=False, noindex=True, bare=True,
            css_extra=authkit.AUTH_CSS + css,
            js_extra="<script>" + authkit.AUTH_JS + "</script><script>var SITE_URL=" + json.dumps(SITE_URL) + ";</script><script>" + bo2.BX_JS + "</script>")
    return d

def account_page():
    body = backoffice.ACCOUNT_HTML.replace("%(crumbs)s", crumbs("האזור שלי"))
    return private_page("האזור שלי | CargoTech", "ההזמנות והכתובות השמורות שלכם.", body, backoffice.ACCOUNT_CSS, backoffice.ACCOUNT_JS)

# ------------- write -------------
if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(OUT)
pages = {}
pages["index.html"] = index_page(True)
for k, s in SERVICES.items(): pages[s["file"]] = service_page(s)
for a in ARTICLES: pages[a["file"]] = article_page(a)
pages["articles.html"] = articles_page()
pages["pricing.html"] = pricing_page()
pages["contact.html"] = contact_page()
pages["data.html"] = data_page()
pages["glossary.html"] = glossary_page()
pages["order.html"] = order_page()
pages["account.html"] = account_page()
for name, content in pages.items():
    open(os.path.join(OUT, name), "w", encoding="utf-8").write(content)
if os.path.exists(ADMIN_OUT): shutil.rmtree(ADMIN_OUT)
os.makedirs(ADMIN_OUT)
open(os.path.join(ADMIN_OUT, "index.html"), "w", encoding="utf-8").write(admin_page())
open(os.path.join(ADMIN_OUT, "robots.txt"), "w").write("User-agent: *\nDisallow: /\n")
open(os.path.join(SCR, "cargotech-index-fragment.html"), "w", encoding="utf-8").write(index_page(False))
open(os.path.join(OUT, "robots.txt"), "w").write("User-agent: *\nAllow: /\nDisallow: /account.html\nDisallow: /api/\n")
print(len(pages), "pages:", sorted(pages))
