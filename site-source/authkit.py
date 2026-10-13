# -*- coding: utf-8 -*-
"""Shared sign-in kit (customers and staff). Firebase Authentication is loaded on demand from Google's CDN;
the web config comes from /__/firebase/init.json which Firebase Hosting serves for this project."""

AUTH_HTML = """
<dialog id="authdlg" class="dlg" aria-labelledby="auth-h">
  <div class="dlg-in">
    <button type="button" class="dlg-x" id="auth-x" aria-label="סגירה">×</button>
    <h2 id="auth-h">התחברות והרשמה</h2>
    <div class="atabs" role="tablist">
      <button type="button" role="tab" class="on" data-t="in" aria-selected="true">התחברות</button>
      <button type="button" role="tab" data-t="up" aria-selected="false">הרשמה</button>
    </div>
    <form id="auth-in" class="aform" novalidate>
      <div class="field"><label for="ai-mail">אימייל</label><input id="ai-mail" type="email" autocomplete="email" inputmode="email"></div>
      <div class="field"><label for="ai-pw">סיסמה</label><input id="ai-pw" type="password" autocomplete="current-password"></div>
      <p class="err" id="ai-err" role="alert" hidden></p>
      <button class="btn btn-go" type="submit">התחברות</button>
      <button class="btn-back" type="button" id="ai-forgot">שכחתי סיסמה</button>
    </form>
    <form id="auth-up" class="aform" hidden novalidate>
      <div class="row2">
        <div class="field"><label for="au-fn">שם פרטי</label><input id="au-fn" type="text" autocomplete="given-name"></div>
        <div class="field"><label for="au-ln">שם משפחה</label><input id="au-ln" type="text" autocomplete="family-name"></div>
      </div>
      <div class="row2">
        <div class="field"><label for="au-mail">אימייל</label><input id="au-mail" type="email" autocomplete="email" inputmode="email"></div>
        <div class="field"><label for="au-ph">טלפון</label><input id="au-ph" type="tel" autocomplete="tel" inputmode="tel"></div>
      </div>
      <div class="row2">
        <div class="field"><label for="au-pw">סיסמה (לפחות 6 תווים)</label><input id="au-pw" type="password" autocomplete="new-password"></div>
        <div class="field"><label for="au-pw2">אימות סיסמה</label><input id="au-pw2" type="password" autocomplete="new-password"></div>
      </div>
      <div class="field"><label for="au-use">אני משתמש בשירות עבור</label>
        <select id="au-use"><option value="">בחרו</option><option value="private">שימוש פרטי</option><option value="business">עסק</option></select></div>
      <div class="field"><label for="au-cp">קוד קופון (אופציונלי)</label><input id="au-cp" type="text" autocomplete="off"></div>
      <label class="chk-row"><input type="checkbox" id="au-mk"> אשמח לקבל עדכונים והודעות במייל</label>
      <p class="err" id="au-err" role="alert" hidden></p>
      <button class="btn btn-go" type="submit">הרשמה</button>
    </form>
    <div class="aor"><span>או</span></div>
    <button class="btn btn-line-dark" type="button" id="auth-g">המשך עם Google</button>
  </div>
</dialog>
"""

AUTH_CSS = r"""
.dlg { border: 0; border-radius: 16px; padding: 0; width: min(520px, calc(100vw - 24px)); max-height: calc(100vh - 24px); color: var(--fg); background: var(--surface); box-shadow: 0 30px 80px rgba(7, 26, 44, .45); }
.dlg::backdrop { background: rgba(7, 26, 44, .62); }
.dlg-in { padding: 24px 22px 22px; display: grid; gap: 14px; position: relative; overflow-y: auto; max-height: calc(100vh - 24px); }
.dlg-in h2 { font-size: 1.4rem; margin: 0; }
.dlg-x { position: absolute; inset-block-start: 10px; inset-inline-start: 12px; width: 40px; height: 40px; border-radius: 50%; border: 0; background: var(--bg); color: var(--ink); font-size: 1.5rem; cursor: pointer; }
.dlg .btn { width: 100%; margin-top: 4px; }
.atabs { display: grid; grid-template-columns: 1fr 1fr; border-bottom: 1px solid var(--line); }
.atabs button { min-height: 46px; background: none; border: 0; border-bottom: 3px solid transparent; font: 800 1rem inherit; font-family: inherit; color: var(--muted); cursor: pointer; }
.atabs button.on { color: var(--ink); border-bottom-color: var(--cyan); }
.aform { display: grid; gap: 12px; }
.aor { text-align: center; color: var(--muted); font-size: .9rem; position: relative; }
.aor span { background: var(--surface); padding: 0 12px; position: relative; }
.aor::before { content: ""; position: absolute; inset-inline: 0; top: 50%; border-top: 1px solid var(--line); }
.chk-row { display: flex; gap: 10px; align-items: flex-start; font-weight: 600; font-size: .95rem; line-height: 1.5; }
.chk-row input { width: 22px; height: 22px; margin-top: 2px; flex: none; accent-color: var(--ink); }
.row2 { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
@media (max-width: 480px) { .row2 { grid-template-columns: minmax(0, 1fr); } }
"""

AUTH_JS = r"""
(function () {
  var CT = window.CT = window.CT || {};
  var listeners = [], SDK = "https://www.gstatic.com/firebasejs/10.14.1/", fb = null;
  CT.user = null; CT.ready = false;
  var isLocal = /^(localhost|127\.0\.0\.1)$/.test(location.hostname);
  function emit() { listeners.forEach(function (f) { try { f(CT.user); } catch (e) {} }); }
  CT.onAuth = function (f) { listeners.push(f); if (CT.ready) f(CT.user); };
  CT.init = function () {
    if (CT._p) return CT._p;
    CT._p = (async function () {
      if (isLocal) { var tu = null; try { tu = localStorage.getItem("ct_test_user"); } catch (e) {} if (tu) { CT.user = { uid: tu, email: tu + "@example.com", test: true }; CT.ready = true; emit(); return; } }
      try {
        var cfg = await (await fetch("/__/firebase/init.json")).json();
        if (!cfg || !cfg.apiKey) throw new Error("no config");
        var app = await import(SDK + "firebase-app.js"), au = await import(SDK + "firebase-auth.js");
        var a = app.initializeApp(cfg, "cargotech"), auth = au.getAuth(a); auth.languageCode = "he";
        fb = { au: au, auth: auth };
        au.onAuthStateChanged(auth, function (u) { CT.user = u ? { uid: u.uid, email: u.email || "", name: u.displayName || "", emailVerified: u.emailVerified, fb: u } : null; CT.ready = true; emit(); });
        /* staff "log in as this customer" link: ?as=<one-time custom token>. Sign in with it once, then drop it
           from the address bar immediately so it doesn't linger visibly in the URL or browser history. */
        var asTok = new URLSearchParams(location.search).get("as");
        if (asTok) {
          var url = new URL(location.href); url.searchParams.delete("as"); history.replaceState(null, "", url);
          try { await au.signInWithCustomToken(auth, asTok); } catch (e) { /* expired or already used; user just stays signed out */ }
        }
      } catch (e) { CT.failed = true; CT.ready = true; emit(); }
    })();
    return CT._p;
  };
  CT.token = async function () {
    if (CT.user && CT.user.test) return "test:" + CT.user.uid;
    if (CT.user && CT.user.fb) { try { return await CT.user.fb.getIdToken(); } catch (e) { return null; } }
    return null;
  };
  CT.api = async function (method, path, body, headers) {
    var h = { "Content-Type": "application/json" }; Object.keys(headers || {}).forEach(function (k) { h[k] = headers[k]; });
    if (!h.Authorization) { var t = await CT.token(); if (t) h.Authorization = "Bearer " + t; }
    var r, j = {};
    try { r = await fetch("/api/v1" + path, { method: method, headers: h, body: body && method !== "GET" ? JSON.stringify(body) : undefined }); } catch (e) { return { ok: false, error: "network", _status: 0 }; }
    try { j = await r.json(); } catch (e) { j = { ok: false }; }
    j._status = r.status; return j;
  };
  var MSG = { "auth/invalid-credential": "אימייל או סיסמה שגויים.", "auth/wrong-password": "אימייל או סיסמה שגויים.", "auth/user-not-found": "אימייל או סיסמה שגויים.",
    "auth/email-already-in-use": "האימייל הזה כבר רשום. נסו להתחבר.", "auth/weak-password": "הסיסמה חלשה מדי. השתמשו ב-6 תווים לפחות.", "auth/invalid-email": "כתובת האימייל לא תקינה.",
    "auth/too-many-requests": "יותר מדי נסיונות. נסו שוב בעוד כמה דקות.", "auth/network-request-failed": "אין חיבור לרשת. נסו שוב." };
  CT.errText = function (e) { return MSG[e && e.code] || "משהו השתבש. נסו שוב."; };
  function need() { if (!fb) throw { code: "auth/network-request-failed" }; return fb; }
  CT.signIn = async function (m, p) { var f = need(); return f.au.signInWithEmailAndPassword(f.auth, m, p); };
  CT.signUp = async function (m, p) { var f = need(); return f.au.createUserWithEmailAndPassword(f.auth, m, p); };
  CT.google = async function () { var f = need(); return f.au.signInWithPopup(f.auth, new f.au.GoogleAuthProvider()); };
  CT.reset = async function (m) { var f = need(); return f.au.sendPasswordResetEmail(f.auth, m); };
  CT.verifyMail = async function () { var f = need(); return f.au.sendEmailVerification(f.auth.currentUser); };
  CT.signOut = async function () { if (CT.user && CT.user.test) { try { localStorage.removeItem("ct_test_user"); } catch (e) {} CT.user = null; emit(); return; } var f = need(); return f.au.signOut(f.auth); };

  /* sign-in dialog */
  CT.openAuth = function (tab) {
    var d = document.getElementById("authdlg"); if (!d) return;
    setTab(tab || "in"); if (!d.open) d.showModal();
  };
  function setTab(t) {
    document.querySelectorAll("#authdlg .atabs button").forEach(function (b) { var on = b.getAttribute("data-t") === t; b.classList.toggle("on", on); b.setAttribute("aria-selected", on); });
    document.getElementById("auth-in").hidden = t !== "in"; document.getElementById("auth-up").hidden = t !== "up";
  }
  document.addEventListener("DOMContentLoaded", function () {
    var d = document.getElementById("authdlg"); if (!d) return;
    var $ = function (id) { return document.getElementById(id); };
    var say = function (id, m) { var e = $(id); e.textContent = m || ""; e.hidden = !m; };
    d.querySelectorAll(".atabs button").forEach(function (b) { b.addEventListener("click", function () { setTab(b.getAttribute("data-t")); }); });
    $("auth-x").addEventListener("click", function () { d.close(); });
    $("auth-in").addEventListener("submit", async function (e) {
      e.preventDefault(); say("ai-err", "");
      try { await CT.init(); await CT.signIn($("ai-mail").value.trim(), $("ai-pw").value); $("ai-pw").value = ""; d.close(); } catch (x) { say("ai-err", CT.errText(x)); }
    });
    $("ai-forgot").addEventListener("click", async function () {
      var m = $("ai-mail").value.trim(); if (!m) { say("ai-err", "כתבו את האימייל ואז לחצו שוב על שכחתי סיסמה."); return; }
      try { await CT.init(); await CT.reset(m); say("ai-err", "שלחנו קישור לאיפוס הסיסמה לאימייל."); } catch (x) { say("ai-err", CT.errText(x)); }
    });
    $("auth-up").addEventListener("submit", async function (e) {
      e.preventDefault(); say("au-err", "");
      var m = $("au-mail").value.trim(), p = $("au-pw").value;
      if (!$("au-fn").value.trim() || !m) return say("au-err", "מלאו שם ואימייל.");
      if (p.length < 6) return say("au-err", "הסיסמה צריכה להיות באורך 6 תווים לפחות.");
      if (p !== $("au-pw2").value) return say("au-err", "הסיסמאות אינן זהות.");
      if (!$("au-use").value) return say("au-err", "בחרו שימוש פרטי או עסק.");
      try {
        await CT.init();
        var cred = await CT.signUp(m, p);
        /* the global sign-in state (CT.user) is set by an async onAuthStateChanged callback that can still be
           in flight right after signUp() resolves; asking it for a token here would race it and silently send
           this request with no Authorization header. Get the token straight from the fresh credential instead. */
        var tok = await cred.user.getIdToken();
        var pr = await CT.api("PUT", "/me", { firstName: $("au-fn").value, lastName: $("au-ln").value, phone: $("au-ph").value, useFor: $("au-use").value, marketing: $("au-mk").checked }, { Authorization: "Bearer " + tok });
        if (!pr.ok) { say("au-err", "החשבון נוצר, אך הפרטים (שם/טלפון) לא נשמרו. אפשר להשלים אותם ב\"האזור האישי\" אחרי ההתחברות."); }
        var cp = $("au-cp").value.trim();
        if (cp) { try { await CT.api("POST", "/coupon/redeem", { code: cp }, { Authorization: "Bearer " + tok }); } catch (e) { /* invalid/expired code: signup still succeeds, just no discount */ } }
        $("au-pw").value = ""; $("au-pw2").value = ""; d.close();
        if (CT.afterSignUp) CT.afterSignUp();
      } catch (x) { say("au-err", CT.errText(x)); }
    });
    $("auth-g").addEventListener("click", async function () {
      try { await CT.init(); await CT.google(); d.close(); } catch (x) { if (!x || x.code !== "auth/popup-closed-by-user") say(!$("auth-in").hidden ? "ai-err" : "au-err", CT.errText(x)); }
    });
  });
})();
"""
