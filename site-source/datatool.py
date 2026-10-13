# -*- coding: utf-8 -*-
TOOL_CSS = r"""
.itool { max-width: 760px; margin-inline: auto; }
.isearch { position: relative; }
.isearch label { display: block; font-weight: 800; color: var(--ink); margin-bottom: 8px; font-size: 1.05rem; }
.isearch .row { display: flex; gap: 8px; }
.isearch input { flex: 1; min-width: 0; min-height: 56px; padding: 12px 16px; font: 700 1.1rem inherit; font-family: inherit; border: 2px solid var(--line); border-radius: 12px; background: var(--surface); color: var(--fg); }
.isearch input:focus { outline: none; border-color: var(--ink); box-shadow: 0 0 0 3px rgba(79,195,236,.35); }
.isearch .btn { min-height: 56px; padding-inline: 22px; flex: none; }
.isug { list-style: none; margin: 8px 0 0; padding: 0; background: var(--surface); border: 1px solid var(--line); border-radius: 12px; overflow: hidden; box-shadow: 0 12px 28px rgba(12,58,95,.18); }
.isug li button { width: 100%; text-align: start; display: grid; gap: 2px; padding: 14px 16px; min-height: 56px; border: 0; border-bottom: 1px solid var(--line); background: transparent; cursor: pointer; font-family: inherit; color: var(--fg); }
.isug li:last-child button { border-bottom: 0; }
.isug li button:hover, .isug li button:focus-visible { background: var(--bg); outline: none; }
.isug b { font-size: 1rem; line-height: 1.4; }
.isug span { color: var(--muted); font-size: .88rem; direction: ltr; text-align: end; }
.ires { scroll-margin-top: 84px; }
.itool { margin-top: -40px; }
.istate { padding: 22px 8px; color: var(--muted); text-align: center; }
.ires { margin-top: 8px; }
.ihead { background: linear-gradient(160deg, var(--ink-2), var(--ink)); color: #fff; border-radius: 14px; padding: 20px 18px; }
.ihead small { color: var(--on-ink-muted); font-weight: 700; }
.ihead h2 { color: #fff; font-size: 1.4rem; line-height: 1.35; margin: 4px 0 10px; }
.ihead .code { display: inline-block; direction: ltr; background: rgba(255,255,255,.12); border-radius: 8px; padding: 6px 12px; font: 700 1.05rem "IBM Plex Mono", monospace; }
.iacc { margin-top: 14px; display: grid; gap: 10px; }
.iacc details { background: var(--surface); border: 1px solid var(--line); border-radius: 12px; }
.iacc summary { list-style: none; cursor: pointer; display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 16px; min-height: 58px; font-weight: 800; color: var(--ink); font-size: 1.05rem; }
.iacc summary::-webkit-details-marker { display: none; }
.iacc summary::after { content: "+"; font-size: 1.6rem; line-height: 1; color: var(--cyan); font-weight: 400; }
.iacc details[open] summary::after { content: "−"; }
.iacc .pb { padding: 0 16px 16px; display: grid; gap: 12px; line-height: 1.75; }
.ireq { border: 1px solid var(--line); border-radius: 10px; padding: 12px 14px; background: var(--bg); display: grid; gap: 4px; }
.ireq b { color: var(--ink); } .ireq span { color: var(--muted); font-size: .94rem; }
.icall { background: var(--sea-soft); border-radius: 12px; padding: 14px 16px; display: grid; gap: 10px; }
.icall p { margin: 0; font-weight: 700; color: var(--ink); }
.icall .acts { display: flex; flex-wrap: wrap; gap: 8px; }
.icall .acts .btn { flex: 1 1 140px; min-height: 48px; }
.inew { margin-top: 16px; display: grid; }
.inew .btn { min-height: 54px; }
@media (max-width: 560px) { .isearch .row { flex-direction: column; } .isearch .btn { width: 100%; } .ihead h2 { font-size: 1.2rem; } }
"""

def tool_html(esc):
    return (
    '<div class="itool">'
    '<form class="isearch" id="i-form" role="search" autocomplete="off">'
    '<label for="i-q">איזה מוצר רוצים להביא?</label>'
    '<div class="row"><input id="i-q" type="search" inputmode="search" enterkeyhint="search" placeholder="לדוגמה: חולצות, טלפון, צעצועים" aria-controls="i-sug">'
    '<button class="btn btn-go" type="submit">חיפוש</button></div>'
    '<ul class="isug" id="i-sug" role="listbox" hidden></ul></form>'
    '<div class="istate" id="i-state" aria-live="polite">הקלידו שם מוצר, ובחרו מהרשימה כדי לראות מה נדרש ליבוא שלו.</div>'
    '<div class="ires" id="i-res" hidden>'
    '<div class="ihead"><small>תוצאת חיפוש</small><h2 id="i-title"></h2><span class="code" id="i-code"></span></div>'
    '<div class="iacc">'
    '<details open><summary>כללי יבוא אישי</summary><div class="pb">'
    '<p>ליבוא אישי יש כללים משלו: כמות מותרת ליחידות או לערך מסוים, ולעיתים תנאים נוספים, והם שונים מוצר מוצר. את הכמות המותרת למוצר שבחרתם נבדוק יחד.</p>'
    '<div class="icall"><p>לבדיקת הכמות המותרת ליבוא אישי של המוצר, פנו אלינו לשיחה.</p><div class="acts">'
    '<a class="btn btn-go" data-wa="שלום CargoTech, אני רוצה לברר כללי יבוא אישי למוצר." href="https://wa.me/" target="_blank" rel="noopener">שיחה בוואטסאפ</a></div></div></div></details>'
    '<details><summary>דרישות חוקיות החלות על המוצר</summary><div class="pb" id="i-reqs"></div></details>'
    '<details><summary>מיסי יבוא</summary><div class="pb">'
    '<p>על יבוא מוצרים חלים בדרך כלל מכס, מס קנייה בחלק מהמוצרים ומע״מ. הסכום תלוי בסוג המוצר, במדינת המוצא, בערך העסקה ובעלויות השילוח, ולכן אי אפשר לדעת אותו בלי בדיקה של המקרה שלכם.</p>'
    '<div class="icall"><p>לחישוב מדויק של המיסים על המוצר שלכם, פנו אלינו לשיחה.</p><div class="acts">'
    '<a class="btn btn-go" data-wa="שלום CargoTech, אני רוצה לברר מיסי יבוא על מוצר." href="https://wa.me/" target="_blank" rel="noopener">שיחה בוואטסאפ</a>'
    '<a class="btn btn-line-dark top-phone latin" data-phone href="contact.html">05X-XXX-XXXX</a></div></div></div></details>'
    '<details><summary>שירותי שילוח</summary><div class="pb"><p>אנחנו מטפלים בכל הדרך: איסוף מהספק, שילוח אווירי או ימי, שחרור במכס ומסירה עד הדלת. כך גם הדרישות החוקיות מטופלות מראש ולא נתקעים בנמל.</p>'
    '<div class="icall"><p>רוצים הצעת מחיר למוצר הזה? פנו אלינו לשיחה.</p><div class="acts"><a class="btn btn-go" href="#quote">קבלו הצעת מחיר</a></div></div></div></details>'
    '<details><summary>מדריכים וכלי סיוע</summary><div class="pb"><p>עדיין לא ברור מה אומר פרט מכס או איזה אישור צריך? המדריכים שלנו מסבירים את זה בעברית פשוטה.</p>'
    '<div class="acts" style="display:flex;flex-wrap:wrap;gap:8px"><a class="btn btn-line-dark" href="hs-code-guide.html">מהו פרט מכס</a><a class="btn btn-line-dark" href="import-step-by-step.html">יבוא צעד אחר צעד</a><a class="btn btn-line-dark" href="articles.html">כל המדריכים</a></div></div></details>'
    '</div>'
    '<div class="inew"><button class="btn btn-go" type="button" id="i-new">חיפוש חדש</button></div>'
    '</div></div>')

TOOL_JS = r"""
(function () {
  var CFG = { proxy: "/api/govdata", api: "https://data.gov.il/api/3/action/datastore_search", resource: "a36db570-09f2-4521-8e3d-0290eb839c68" };
  var q = document.getElementById("i-q"); if (!q) return;
  var form = document.getElementById("i-form"), sug = document.getElementById("i-sug"), st = document.getElementById("i-state"),
      res = document.getElementById("i-res"), tt = document.getElementById("i-title"), cd = document.getElementById("i-code"), rq = document.getElementById("i-reqs");
  var timer = 0, ticket = 0;
  function get(qs) {
    var f = function (u) { return fetch(u).then(function (r) { if (!r.ok) throw new Error("http " + r.status); return r.json(); }); };
    return (/^https?:$/.test(location.protocol) ? f(CFG.proxy + qs).catch(function () { return f(CFG.api + qs); }) : f(CFG.api + qs));
  }
  function url(term, limit) { return "?resource_id=" + encodeURIComponent(CFG.resource) + "&limit=" + limit + (term ? "&q=" + encodeURIComponent(term) : ""); }
  function clean(s) { return String(s || "").replace(/\s*-->\s*/g, " › ").replace(/[-:]+\s*›/g, "›").trim(); }
  function setState(t) { st.textContent = t; st.hidden = !t; }
  function hideSug() { sug.hidden = true; sug.innerHTML = ""; }
  function search() {
    var term = q.value.trim(); var my = ++ticket;
    if (term.length < 1) { hideSug(); setState("הקלידו שם מוצר."); return; }
    setState("מחפש..."); res.hidden = true;
    get(url(term, 100)).then(function (j) {
      if (my !== ticket) return;
      var recs = (j.result && j.result.records) || [], seen = {}, list = [];
      recs.forEach(function (r) { var c = r.CustomsItemFullClassification; if (c && !seen[c]) { seen[c] = 1; list.push(r); } });
      hideSug();
      if (!list.length) { setState("לא נמצא מוצר בשם הזה. נסו מילה אחרת, או פנו אלינו לשיחה ונבדוק בשבילכם."); return; }
      setState(list.length > 8 ? "מוצגות 8 התוצאות הראשונות. דייקו את החיפוש כדי לצמצם." : "בחרו את המוצר המתאים:");
      list.slice(0, 8).forEach(function (r) {
        var li = document.createElement("li"), b = document.createElement("button"), t = document.createElement("b"), c = document.createElement("span");
        b.type = "button"; t.textContent = clean(r.FullGoodsDescription); c.textContent = r.CustomsItemFullClassification; b.appendChild(t); b.appendChild(c);
        b.addEventListener("click", function () { show(r.CustomsItemFullClassification, recs); }); li.appendChild(b); sug.appendChild(li);
      });
      sug.hidden = false;
    }).catch(function () { if (my === ticket) setState("אירעה תקלה בטעינה. נסו שוב, או פנו אלינו לשיחה."); });
  }
  function show(code, recs) {
    var rows = recs.filter(function (r) { return r.CustomsItemFullClassification === code; });
    hideSug(); setState("");
    tt.textContent = clean(rows[0].FullGoodsDescription); cd.textContent = code; rq.innerHTML = "";
    var seen = {};
    rows.forEach(function (r) {
      var k = [r.RegularityRequirement_Authority, r.ConfirmationType, r.RegularityRequirement_GoodsDescription].join("|"); if (seen[k]) return; seen[k] = 1;
      var d = document.createElement("div"); d.className = "ireq";
      var b = document.createElement("b"); b.textContent = r.RegularityRequirement_Authority ? "גורם מאשר: " + r.RegularityRequirement_Authority : "דרישה";
      d.appendChild(b);
      [r.ConfirmationType ? "סוג אישור: " + r.ConfirmationType : "", r.RegularityPublication ? "מקור: " + r.RegularityPublication : "", r.RegularityRequirement_GoodsDescription ? "חל על: " + r.RegularityRequirement_GoodsDescription : ""].forEach(function (t) { if (t) { var s = document.createElement("span"); s.textContent = t; d.appendChild(s); } });
      rq.appendChild(d);
    });
    if (!rq.children.length) { var p = document.createElement("p"); p.textContent = "לא נמצאו במאגר דרישות למוצר הזה. פנו אלינו לשיחה כדי שנוודא."; rq.appendChild(p); }
    var n = document.createElement("p"); n.style.color = "var(--muted)"; n.style.fontSize = ".9rem"; n.textContent = "המידע מבוסס על מאגר ממשלתי פתוח ועשוי להשתנות. לווידוא סופי פנו אלינו לשיחה."; rq.appendChild(n);
    res.hidden = false; res.scrollIntoView({ behavior: "smooth", block: "start" });
  }
  form.addEventListener("submit", function (e) { e.preventDefault(); search(); });
  q.addEventListener("input", function () { clearTimeout(timer); timer = setTimeout(search, 250); });
  document.getElementById("i-new").addEventListener("click", function () { res.hidden = true; q.value = ""; hideSug(); setState("הקלידו שם מוצר, ובחרו מהרשימה כדי לראות מה נדרש ליבוא שלו."); q.focus(); window.scrollTo({ top: form.getBoundingClientRect().top + scrollY - 90, behavior: "smooth" }); });
})();
"""
