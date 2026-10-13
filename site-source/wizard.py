# -*- coding: utf-8 -*-
from countries_full import ALL as _ALL, TOP as _TOP
_EXC = {"co","tn","so"}
_items = [x.strip() for x in _ALL.split("|") if x.strip() and x.split()[0] not in _EXC]
_d = {x.split()[0]: x for x in _items}
COUNTRIES = "|".join([_d[c] for c in _TOP] + sorted([v for k, v in _d.items() if k not in _TOP], key=lambda v: v.split(" ", 1)[1]))
CITIES = ["תל אביב","ירושלים","חיפה","באר שבע","ראשון לציון","פתח תקווה","אשדוד","נתניה","חולון","בני ברק","רמת גן","אשקלון","רחובות","הרצליה","כפר סבא","רעננה","מודיעין","חדרה","נצרת","אילת","קריית שמונה","טבריה","עכו","כרמיאל","לוד","רמלה","בית שמש","נס ציונה","יבנה","עפולה"]

WIZ_HTML = """
<div class="qcard wiz" id="quote">
  <div class="wtabs" role="tablist" aria-label="סוג שילוח">
    <button type="button" role="tab" class="on" aria-selected="true" data-mode="intl">שילוח בינלאומי</button>
    <button type="button" role="tab" aria-selected="false" data-mode="dom">שילוח בארץ</button>
    <button type="button" role="tab" aria-selected="false" data-mode="reloc">הובלת דירה</button>
  </div>
  <form class="qform" id="qform" novalidate>
    <input type="hidden" id="f-service" value="שילוח בינלאומי"><input type="hidden" id="f-route"><input type="hidden" id="f-cargo">
    <div class="step" id="st1">
      <div class="route" id="r-intl">
        <div class="cpick" data-key="from"><span class="lbl">מאיפה</span></div>
        <button type="button" class="swap" id="swap" aria-label="החלפת כיוון">⇅</button>
        <div class="cpick" data-key="to"><span class="lbl">לאן</span></div>
      </div>
      <div class="route" id="r-dom" hidden>
        <div class="field"><label for="d-from">מאיזו עיר</label><input id="d-from" list="cities" type="text" placeholder="לדוגמה: תל אביב"></div>
        <div class="field"><label for="d-to">לאיזו עיר</label><input id="d-to" list="cities" type="text" placeholder="לדוגמה: חיפה"></div>
        <datalist id="cities">%(cities)s</datalist>
      </div>
      <div class="cg" id="cargo-group">
        <span class="lbl">מה שולחים</span>
        <div class="chips" id="ctype" role="group" aria-label="סוג מטען">
          <button type="button" class="chip on" data-t="parcel" aria-pressed="true"><i>▢</i>חבילה</button>
          <button type="button" class="chip" data-t="doc" aria-pressed="false"><i>▤</i>מסמך</button>
          <button type="button" class="chip" data-t="pallet" aria-pressed="false"><i>▦</i>משטח</button>
          <button type="button" class="chip" data-t="cont" aria-pressed="false" id="chip-cont"><i>▬</i>מכולה</button>
        </div>
        <div class="cfields" id="cf-parcel">
          <div class="row3">
            <div class="field"><label for="p-n">כמות</label><input id="p-n" type="number" min="1" value="1" inputmode="numeric"></div>
            <div class="field"><label for="p-kg">משקל (ק״ג)</label><input id="p-kg" type="number" min="0" step="0.1" inputmode="decimal" placeholder="0"></div>
          </div>
          <div class="row3">
            <div class="field"><label for="p-l">אורך (ס״מ)</label><input id="p-l" type="number" min="0" inputmode="decimal" placeholder="0"></div>
            <div class="field"><label for="p-w">רוחב (ס״מ)</label><input id="p-w" type="number" min="0" inputmode="decimal" placeholder="0"></div>
            <div class="field"><label for="p-h">גובה (ס״מ)</label><input id="p-h" type="number" min="0" inputmode="decimal" placeholder="0"></div>
          </div>
          <p class="calcline" id="p-calc" aria-live="polite"></p>
        </div>
        <div class="cfields" id="cf-doc" hidden><p class="qnote">מעטפה או מסמכים עד כחצי קילו. אין צורך במידות.</p></div>
        <div class="cfields" id="cf-pallet" hidden>
          <div class="row3">
            <div class="field"><label for="q-n">כמות משטחים</label><input id="q-n" type="number" min="1" value="1" inputmode="numeric"></div>
            <div class="field"><label for="q-kg">משקל למשטח (ק״ג)</label><input id="q-kg" type="number" min="0" inputmode="decimal" placeholder="0"></div>
          </div>
          <div class="row3">
            <div class="field"><label for="q-l">אורך (ס״מ)</label><input id="q-l" type="number" min="0" inputmode="decimal" placeholder="120"></div>
            <div class="field"><label for="q-w">רוחב (ס״מ)</label><input id="q-w" type="number" min="0" inputmode="decimal" placeholder="80"></div>
            <div class="field"><label for="q-h">גובה (ס״מ)</label><input id="q-h" type="number" min="0" inputmode="decimal" placeholder="0"></div>
          </div>
        </div>
        <div class="cfields" id="cf-cont" hidden>
          <span class="lbl sm">איזו מכולה</span>
          <div class="chips" id="feet" role="group" aria-label="גודל מכולה">
            <button type="button" class="chip on" data-v="מכולה 20 פיט" aria-pressed="true">20 פיט</button>
            <button type="button" class="chip" data-v="מכולה 40 פיט" aria-pressed="false">40 פיט</button>
            <button type="button" class="chip" data-v="מכולה 40 פיט HC (גבוהה)" aria-pressed="false">40 פיט HC</button>
            <button type="button" class="chip" data-v="חלק ממכולה (LCL)" aria-pressed="false">חלק ממכולה</button>
          </div>
          <div class="field" style="max-width:150px"><label for="c-n2">כמות מכולות</label><input id="c-n2" type="number" min="1" value="1" inputmode="numeric"></div>
        </div>
      </div>
      <div class="cg" id="reloc-group" hidden>
        <span class="lbl">גודל ההובלה</span>
        <div class="chips" id="rsize" role="group" aria-label="גודל ההובלה">
          <button type="button" class="chip on" data-v="קרטונים ומעט רהיטים" aria-pressed="true">קרטונים ומעט רהיטים</button>
          <button type="button" class="chip" data-v="דירת 1-3 חדרים" aria-pressed="false">דירת 1 עד 3 חדרים</button>
          <button type="button" class="chip" data-v="דירת 4 חדרים ומעלה" aria-pressed="false">דירת 4 חדרים ומעלה</button>
          <button type="button" class="chip" data-v="בית או משרד" aria-pressed="false">בית או משרד</button>
        </div>
      </div>
      <p class="err" id="werr" role="alert" hidden></p>
      <button type="button" class="btn btn-go" id="wnext">קבלת מחיר</button>
    </div>
    <div class="step" id="st2" hidden>
      <div class="sum" id="wsum"></div>
      <div class="row2">
        <div class="field"><label for="f-name">שם</label><input id="f-name" type="text" autocomplete="name" placeholder="השם שלכם"></div>
        <div class="field"><label for="f-phone">טלפון</label><input id="f-phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="05X-XXX-XXXX"></div>
      </div>
      <a class="btn btn-go" id="send-wa" href="https://wa.me/" target="_blank" rel="noopener">שלחו לנו בוואטסאפ</a>
      <button type="button" class="btn-back" id="wback">→ חזרה לעריכת המסלול</button>
      <p class="qnote">הפרטים נפתחים כהודעה מוכנה בוואטסאפ, ונשמרים אצלנו רק כדי לחזור אליכם.</p>
    </div>
  </form>
</div>
"""

WIZ_CSS = r"""
.wiz { padding: 0; overflow: visible; }
.wtabs { display: grid; grid-template-columns: repeat(3, 1fr); background: var(--bg); border-radius: 14px 14px 0 0; border-bottom: 1px solid var(--line); }
.wtabs button { padding: 15px 8px; font: 800 .95rem var(--font-display, inherit); color: var(--muted); background: transparent; border: 0; border-bottom: 3px solid transparent; cursor: pointer; min-height: 52px; }
.wtabs button:first-child { border-top-right-radius: 14px; } .wtabs button:last-child { border-top-left-radius: 14px; }
.wtabs button.on { color: var(--ink); background: var(--surface); border-bottom-color: var(--cyan); }
.wtabs button:hover:not(.on) { color: var(--ink); }
.wiz .qform { padding: 22px 24px 24px; margin-top: 0; gap: 16px; }
.wiz .step { display: grid; gap: 16px; }
.wiz [hidden] { display: none !important; }
.route { display: grid; gap: 10px; position: relative; }
.lbl { display: block; font-weight: 800; font-size: .92rem; color: var(--ink); margin-bottom: 6px; }
.lbl.sm { font-size: .86rem; color: var(--muted); }
.cpick { position: relative; }
.cbtn { width: 100%; min-height: 54px; display: flex; align-items: center; gap: 12px; padding: 8px 14px; border: 1.5px solid var(--line); border-radius: 12px; background: var(--bg); color: var(--fg); font: 700 1.05rem inherit; font-family: inherit; cursor: pointer; text-align: start; }
.cbtn:hover { border-color: var(--muted); }
.cbtn:focus-visible, .cbtn[aria-expanded="true"] { border-color: var(--ink); outline: none; box-shadow: 0 0 0 3px rgba(79, 195, 236, .35); }
.cbtn .cname { flex: 1; } .cbtn .cname.ph { color: var(--muted); font-weight: 600; }
.cbtn .chev { width: 9px; height: 9px; border-inline-end: 2px solid var(--muted); border-bottom: 2px solid var(--muted); transform: rotate(45deg); margin-top: -4px; }
.flg { width: 28px; height: 20px; border-radius: 3px; object-fit: cover; box-shadow: 0 0 0 1px rgba(16, 71, 114, .18); flex: none; background: var(--line); }
.flg.em { box-shadow: none; background: none; font-size: 1.35rem; line-height: 1; width: auto; height: auto; }
.cpanel { position: absolute; inset-inline: 0; top: calc(100% + 6px); z-index: 30; background: var(--surface); border: 1px solid var(--line); border-radius: 12px; box-shadow: 0 18px 40px rgba(12, 58, 95, .28); overflow: hidden; }
.cpanel input { width: 100%; border: 0; border-bottom: 1px solid var(--line); padding: 13px 14px; font: 600 1rem inherit; font-family: inherit; background: var(--surface); color: var(--fg); outline: none; }
.cpanel ul { list-style: none; margin: 0; padding: 4px; max-height: 260px; overflow-y: auto; }
.cpanel li button { width: 100%; display: flex; align-items: center; gap: 12px; padding: 10px 12px; border: 0; background: transparent; border-radius: 8px; cursor: pointer; font: 600 1rem inherit; font-family: inherit; color: var(--fg); text-align: start; }
.cpanel li button:hover, .cpanel li button:focus-visible { background: var(--bg); outline: none; }
.cpanel li.sel button { color: var(--ink); font-weight: 800; }
.cpanel .none { padding: 14px; color: var(--muted); }
.swap { justify-self: center; width: 40px; height: 40px; border-radius: 50%; border: 1.5px solid var(--line); background: var(--surface); color: var(--ink); font-size: 1.2rem; cursor: pointer; margin: -2px 0; }
.swap:hover { background: var(--ink); color: #fff; border-color: var(--ink); }
.chips { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 12px; }
.chip { display: inline-flex; align-items: center; gap: 6px; min-height: 44px; padding: 8px 13px; border: 1.5px solid var(--line); border-radius: 999px; background: var(--surface); color: var(--fg); font: 700 .98rem inherit; font-family: inherit; cursor: pointer; }
.chip i { font-style: normal; color: var(--muted); font-size: 1.05rem; }
.chip:hover { border-color: var(--muted); }
.chip.on { background: var(--ink); border-color: var(--ink); color: #fff; }
.chip.on i { color: var(--cyan); }
.row3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(96px, 1fr)); gap: 10px; margin-bottom: 10px; }
.cfields { display: block; }
.calcline { font-size: .9rem; color: var(--muted); min-height: 1.3em; }
.calcline b { color: var(--ink); }
.err { color: #B3261E; font-weight: 700; font-size: .92rem; }
.sum { background: var(--bg); border: 1px solid var(--line); border-radius: 12px; padding: 14px 16px; font-weight: 700; line-height: 1.7; }
.sum span { display: block; color: var(--muted); font-weight: 600; font-size: .92rem; }
.btn-back { background: none; border: 0; color: var(--ink); font: 700 .95rem inherit; font-family: inherit; text-decoration: underline; cursor: pointer; padding: 6px; justify-self: center; }
.wiz .field input[type=number] { -moz-appearance: textfield; }
@media (max-width: 560px) { .wiz .qform { padding: 18px 16px 20px; } .wtabs button { font-size: .86rem; padding: 12px 4px; } }
@media (prefers-reduced-motion: no-preference) { .cpanel { animation: pop .12s ease-out; } @keyframes pop { from { opacity: 0; transform: translateY(-4px); } } }
"""

WIZ_JS = r"""
(function () {
  var wiz = document.getElementById("quote"); if (!wiz || !wiz.classList.contains("wiz")) return;
  var COUNTRIES = %(countries)s.split("|").map(function (s) { var i = s.indexOf(" "); return { c: s.slice(0, i), n: s.slice(i + 1) }; });
  var $ = function (id) { return document.getElementById(id); };
  var mode = "intl", ctype = "parcel", sel = { from: "il", to: "" };
  var emoji = function (c) { return String.fromCodePoint.apply(null, c.toUpperCase().split("").map(function (ch) { return 127397 + ch.charCodeAt(0); })); };
  var byCode = {}; COUNTRIES.forEach(function (o) { byCode[o.c] = o; });
  function flag(c) {
    var im = document.createElement("img"); im.className = "flg"; im.alt = ""; im.width = 28; im.height = 20; im.loading = "lazy";
    im.src = "https://flagcdn.com/w40/" + c + ".png";
    im.onerror = function () { var s = document.createElement("span"); s.className = "flg em"; s.textContent = emoji(c); if (im.parentNode) im.parentNode.replaceChild(s, im); };
    return im;
  }
  function fire(el) { el.dispatchEvent(new Event("input", { bubbles: true })); }
  var pickers = {};
  document.querySelectorAll(".cpick").forEach(function (box) {
    var key = box.getAttribute("data-key"), btn = document.createElement("button"), panel = document.createElement("div"), open = false;
    btn.type = "button"; btn.className = "cbtn"; btn.setAttribute("aria-haspopup", "listbox"); btn.setAttribute("aria-expanded", "false");
    panel.className = "cpanel"; panel.hidden = true;
    var inp = document.createElement("input"); inp.type = "search"; inp.placeholder = "חיפוש מדינה"; inp.setAttribute("aria-label", "חיפוש מדינה"); inp.autocomplete = "off";
    var ul = document.createElement("ul"); ul.setAttribute("role", "listbox");
    panel.appendChild(inp); panel.appendChild(ul); box.appendChild(btn); box.appendChild(panel);
    function paint() {
      btn.innerHTML = ""; var c = sel[key], nm = document.createElement("span"); nm.className = "cname";
      if (c) { btn.appendChild(flag(c)); nm.textContent = byCode[c].n; } else { nm.className += " ph"; nm.textContent = "בחרו מדינה"; }
      btn.appendChild(nm); var ch = document.createElement("i"); ch.className = "chev"; btn.appendChild(ch);
    }
    function list() {
      var q = inp.value.trim(); ul.innerHTML = ""; var n = 0;
      COUNTRIES.forEach(function (o) {
        if (q && o.n.indexOf(q) < 0) return; n++;
        var li = document.createElement("li"); li.setAttribute("role", "option"); if (sel[key] === o.c) { li.className = "sel"; li.setAttribute("aria-selected", "true"); }
        var b = document.createElement("button"); b.type = "button"; b.appendChild(flag(o.c)); var t = document.createElement("span"); t.textContent = o.n; b.appendChild(t);
        b.addEventListener("click", function () { sel[key] = o.c; close(); paint(); update(); }); li.appendChild(b); ul.appendChild(li);
      });
      if (!n) { var d = document.createElement("li"); d.className = "none"; d.textContent = "לא נמצאה מדינה בשם הזה."; ul.appendChild(d); }
    }
    function close() { open = false; panel.hidden = true; btn.setAttribute("aria-expanded", "false"); }
    function show() { Object.keys(pickers).forEach(function (k) { if (k !== key) pickers[k].close(); }); open = true; inp.value = ""; list(); panel.hidden = false; btn.setAttribute("aria-expanded", "true"); inp.focus(); var s = ul.querySelector(".sel"); if (s) s.scrollIntoView({ block: "nearest" }); }
    btn.addEventListener("click", function () { open ? close() : show(); });
    inp.addEventListener("input", list);
    inp.addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); var f = ul.querySelector("button"); if (f) f.click(); } if (e.key === "ArrowDown") { e.preventDefault(); var f2 = ul.querySelector("button"); if (f2) f2.focus(); } });
    panel.addEventListener("keydown", function (e) { if (e.key === "Escape") { close(); btn.focus(); } if (e.target.tagName === "BUTTON" && (e.key === "ArrowDown" || e.key === "ArrowUp")) { e.preventDefault(); var all = Array.prototype.slice.call(ul.querySelectorAll("button")), i = all.indexOf(e.target) + (e.key === "ArrowDown" ? 1 : -1); if (i < 0) inp.focus(); else if (all[i]) all[i].focus(); } });
    pickers[key] = { close: close, paint: paint };
    paint();
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".cpick")) Object.keys(pickers).forEach(function (k) { pickers[k].close(); }); });
  $("swap").addEventListener("click", function () { var t = sel.from; sel.from = sel.to; sel.to = t; pickers.from.paint(); pickers.to.paint(); update(); });

  var num = function (id) { return parseFloat($(id).value) || 0; };
  function cargoText() {
    if (mode === "reloc") return "הובלת דירה: " + document.querySelector("#rsize .on").getAttribute("data-v");
    if (ctype === "doc") return "מסמך";
    if (ctype === "parcel") { var s = "חבילה: " + (num("p-n") || 1) + " יח׳"; if (num("p-kg")) s += ", " + num("p-kg") + " ק״ג"; if (num("p-l") || num("p-w") || num("p-h")) s += ", " + num("p-l") + "×" + num("p-w") + "×" + num("p-h") + " ס״מ"; return s; }
    if (ctype === "pallet") { var p = "משטח: " + (num("q-n") || 1) + " יח׳"; if (num("q-kg")) p += ", " + num("q-kg") + " ק״ג למשטח"; if (num("q-l") || num("q-w") || num("q-h")) p += ", " + num("q-l") + "×" + num("q-w") + "×" + num("q-h") + " ס״מ"; return p; }
    return document.querySelector("#feet .on").getAttribute("data-v") + ", כמות: " + (num("c-n2") || 1);
  }
  function routeText() {
    if (mode === "dom") return ($("d-from").value.trim() || "?") + " ← " + ($("d-to").value.trim() || "?");
    return (sel.from ? byCode[sel.from].n : "?") + " ← " + (sel.to ? byCode[sel.to].n : "?");
  }
  function update() {
    $("f-service").value = { intl: "שילוח בינלאומי", dom: "שילוח בארץ", reloc: "הובלת דירה (רילוקיישן)" }[mode];
    $("f-route").value = routeText(); $("f-cargo").value = cargoText();
    ["f-service", "f-route", "f-cargo"].forEach(function (id) { fire($(id)); });
    var v = num("p-l") * num("p-w") * num("p-h") * (num("p-n") || 1) / 5000, r = num("p-kg") * (num("p-n") || 1);
    $("p-calc").innerHTML = (v || r) ? "משקל לחיוב משוער: <b>" + (Math.round(Math.max(v, r) * 10) / 10) + " ק״ג</b> (המחושב הגבוה מבין המשקל האמיתי והנפחי)" : "";
  }
  function setMode(m) {
    mode = m;
    document.querySelectorAll(".wtabs button").forEach(function (b) { var on = b.getAttribute("data-mode") === m; b.classList.toggle("on", on); b.setAttribute("aria-selected", on); });
    $("r-intl").hidden = m === "dom"; $("r-dom").hidden = m !== "dom";
    $("cargo-group").hidden = m === "reloc"; $("reloc-group").hidden = m !== "reloc";
    $("chip-cont").hidden = m !== "intl";
    if (m !== "intl" && ctype === "cont") setType("parcel");
    if (m === "reloc") { if (!sel.to) sel.to = ""; }
    if (m === "dom") sel = { from: "il", to: "il" }; else if (sel.from === "il" && sel.to === "il") sel.to = "";
    pickers.from.paint(); pickers.to.paint(); $("werr").hidden = true; update();
  }
  document.querySelectorAll(".wtabs button").forEach(function (b) { b.addEventListener("click", function () { setMode(b.getAttribute("data-mode")); }); });
  function setType(t) {
    ctype = t;
    document.querySelectorAll("#ctype .chip").forEach(function (b) { var on = b.getAttribute("data-t") === t; b.classList.toggle("on", on); b.setAttribute("aria-pressed", on); });
    ["parcel", "doc", "pallet", "cont"].forEach(function (k) { $("cf-" + k).hidden = k !== t; }); update();
  }
  document.querySelectorAll("#ctype .chip").forEach(function (b) { b.addEventListener("click", function () { setType(b.getAttribute("data-t")); }); });
  ["feet", "rsize"].forEach(function (id) { document.querySelectorAll("#" + id + " .chip").forEach(function (b) { b.addEventListener("click", function () { document.querySelectorAll("#" + id + " .chip").forEach(function (x) { x.classList.toggle("on", x === b); x.setAttribute("aria-pressed", x === b); }); update(); }); }); });
  wiz.querySelectorAll("input[type=number], #d-from, #d-to").forEach(function (el) { el.addEventListener("input", update); });
  $("wnext").addEventListener("click", function () {
    var er = $("werr"), msg = "";
    if (mode === "dom") { if (!$("d-from").value.trim() || !$("d-to").value.trim()) msg = "כתבו עיר מוצא ועיר יעד."; }
    else if (!sel.from || !sel.to) msg = "בחרו מדינת מוצא ומדינת יעד.";
    else if (sel.from === sel.to) msg = "מדינת המוצא והיעד זהות. בחרו יעד אחר.";
    if (!msg && mode === "intl" && ctype === "parcel" && !num("p-kg")) msg = "הוסיפו משקל לחבילה, גם הערכה מספיקה.";
    if (msg) { er.textContent = msg; er.hidden = false; return; }
    er.hidden = true; update();
    if (mode === "intl") {
      var seed = { from: sel.from, to: sel.to, type: ctype };
      if (ctype === "parcel") seed.parcels = [{ qty: num("p-n") || 1, kg: num("p-kg") || "", l: num("p-l") || "", w: num("p-w") || "", h: num("p-h") || "" }];
      if (ctype === "pallet") seed.parcels = [{ qty: num("q-n") || 1, kg: num("q-kg") || "", l: num("q-l") || "", w: num("q-w") || "", h: num("q-h") || "" }];
      if (ctype === "cont") seed.cont = { size: document.querySelector("#feet .on").getAttribute("data-v"), qty: num("c-n2") || 1 };
      try { sessionStorage.setItem("ct_seed", JSON.stringify(seed)); } catch (e) {}
      location.href = "order.html"; return;
    }
    $("wsum").innerHTML = "<b>" + $("f-service").value + "</b><span>" + $("f-route").value + "</span><span>" + $("f-cargo").value + "</span>";
    $("st1").hidden = true; $("st2").hidden = false; $("f-name").focus({ preventScroll: true });
  });
  $("wback").addEventListener("click", function () { $("st2").hidden = true; $("st1").hidden = false; });
  update();
})();
"""
