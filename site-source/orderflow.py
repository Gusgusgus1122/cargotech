# -*- coding: utf-8 -*-
"""Customer order flow page (order.html): route -> service/price -> addresses -> goods -> terms -> sent."""

ORDER_HTML = """
<section class="phero"><div class="wrap">%(crumbs)s<h1>הזמנת משלוח בינלאומי</h1>
<p class="lead">מחיר בדקה, מילוי פרטים ושליחה. אפשר להזמין בלי להירשם, וההזמנה נשמרת כדי שלא תצטרכו להתחיל מחדש.</p></div></section>
<section class="sec ord"><div class="wrap">
  <div id="resume" class="resume" hidden>
    <span id="resume-t"></span>
    <button type="button" class="btn btn-go btn-sm" id="resume-go">המשך הזמנה</button>
    <button type="button" class="btn btn-line-dark btn-sm" id="resume-no">התחלה חדשה</button>
  </div>
  <div class="ord-top">
    <ol class="prog" id="prog" aria-label="שלבי ההזמנה">
      <li data-s="1">מסלול</li><li data-s="2">שירות ומחיר</li><li data-s="3">כתובות</li><li data-s="4">סחורה</li><li data-s="5">תנאים</li>
    </ol>
    <div class="acct" id="acct"></div>
  </div>
  <div class="ord-grid">
    <div class="ord-main">
      <form id="oform" novalidate>
        <section class="ostep" id="s1" aria-labelledby="h1s">
          <h2 id="h1s" tabindex="-1">מאיפה לאיפה, ומה שולחים</h2>
          <span class="lbl">מי השולח</span>
          <div class="chips" id="o-ct" role="group" aria-label="סוג שולח">
            <button type="button" class="chip" data-v="private" aria-pressed="false">שולח פרטי</button>
            <button type="button" class="chip" data-v="business" aria-pressed="false">שולח עסקי</button>
          </div>
          <div class="route">
            <div class="cpick" data-key="from"><span class="lbl">מאיפה</span></div>
            <button type="button" class="swap" id="o-swap" aria-label="החלפת כיוון">⇅</button>
            <div class="cpick" data-key="to"><span class="lbl">לאן</span></div>
          </div>
          <span class="lbl">מה שולחים</span>
          <div class="chips" id="o-type" role="group" aria-label="סוג מטען">
            <button type="button" class="chip on" data-t="parcel" aria-pressed="true"><i>▢</i>חבילה</button>
            <button type="button" class="chip" data-t="doc" aria-pressed="false"><i>▤</i>מסמך</button>
            <button type="button" class="chip" data-t="pallet" aria-pressed="false"><i>▦</i>משטח</button>
            <button type="button" class="chip" data-t="cont" aria-pressed="false"><i>▬</i>מכולה</button>
          </div>
          <div id="o-parcels"></div>
          <button type="button" class="btn-add" id="o-addp">+ הוספת חבילה</button>
          <p class="calcline" id="o-calc" aria-live="polite"></p>
          <div id="o-cont" hidden>
            <span class="lbl sm">איזו מכולה</span>
            <div class="chips" id="o-feet" role="group" aria-label="גודל מכולה">
              <button type="button" class="chip on" data-v="מכולה 20 פיט" aria-pressed="true">20 פיט</button>
              <button type="button" class="chip" data-v="מכולה 40 פיט" aria-pressed="false">40 פיט</button>
              <button type="button" class="chip" data-v="מכולה 40 פיט HC (גבוהה)" aria-pressed="false">40 פיט HC</button>
              <button type="button" class="chip" data-v="חלק ממכולה (LCL)" aria-pressed="false">חלק ממכולה</button>
            </div>
            <div class="field" style="max-width:160px"><label for="o-cq">כמות מכולות</label><input id="o-cq" type="number" min="1" value="1" inputmode="numeric"></div>
          </div>
          <p class="err" id="e1" role="alert" hidden></p>
          <button type="button" class="btn btn-go" id="go1">חישוב מחיר</button>
          <div class="quote-wait" id="go1-wait" hidden role="status" aria-live="polite"><span class="spin"></span><span id="go1-wait-t"></span></div>
        </section>

        <section class="ostep" id="s2" hidden aria-labelledby="h2s">
          <h2 id="h2s" tabindex="-1">בחירת שירות</h2>
          <p class="testbar" id="testbar" hidden>מצב בדיקה: המחירים להמחשה בלבד ואינם מחירי אמת.</p>
          <p class="note-assumed" id="assumed" hidden></p>
          <div id="offers" class="offers"></div>
          <div id="manual" class="manual" hidden>
            <b>למסלול הזה אין לנו מחיר אוטומטי כרגע.</b>
            <p>אפשר להמשיך למילוי הפרטים בלי לבחור שירות, ואנחנו נחזור אליכם עם מחיר.</p>
            <button type="button" class="btn btn-go" id="go-manual">המשך בלי לבחור שירות</button>
          </div>
          <button type="button" class="btn-back" id="b2">→ חזרה לשינוי המסלול</button>
        </section>

        <section class="ostep" id="s3" hidden aria-labelledby="h3s">
          <h2 id="h3s" tabindex="-1">שולח ונמען</h2>
          <div class="pair">
            <fieldset class="party" id="p-sender"><legend>שולח</legend></fieldset>
            <fieldset class="party" id="p-recipient"><legend>נמען</legend></fieldset>
          </div>
          <p class="err" id="e3" role="alert" hidden></p>
          <div class="nav2"><button type="button" class="btn btn-go" id="go3">המשך לפרטי הסחורה</button><button type="button" class="btn-back" id="b3">→ חזרה</button></div>
        </section>

        <section class="ostep" id="s4" hidden aria-labelledby="h4s">
          <h2 id="h4s" tabindex="-1">פרטי הסחורה</h2>
          <div id="items"></div>
          <button type="button" class="btn-add" id="o-addi">+ הוספת פריט</button>
          <p class="calcline" id="o-tv" aria-live="polite"></p>
          <label class="chk-row"><input type="checkbox" id="o-ins"> אני רוצה לבטח את הסחורה</label>
          <div class="field" id="o-insbox" hidden style="max-width:260px"><label for="o-insv">שווי לביטוח</label><input id="o-insv" type="number" min="0" inputmode="decimal"></div>
          <h3>איסוף</h3>
          <div class="row2">
            <div class="field"><label for="o-pd">תאריך איסוף</label><input id="o-pd" type="date"></div>
            <div class="field"><label for="o-pt">שעות</label><select id="o-pt"><option value="">בחרו</option><option>08:00 עד 12:00</option><option>12:00 עד 16:00</option><option>16:00 עד 19:00</option><option>כל היום</option></select></div>
          </div>
          <p class="note2">המחירים אינם כוללים מכס ומיסים בארץ היעד, אם יחולו.</p>
          <p class="err" id="e4" role="alert" hidden></p>
          <div class="nav2"><button type="button" class="btn btn-go" id="go4">המשך לתנאים</button><button type="button" class="btn-back" id="b4">→ חזרה</button></div>
        </section>

        <section class="ostep" id="s5" hidden aria-labelledby="h5s">
          <h2 id="h5s" tabindex="-1">תנאים ואישור</h2>
          <div class="row2">
            <div class="field"><label for="t-inc">מי משלם מכס ומיסים ביעד</label><select id="t-inc"><option value="">בחרו</option><option value="DAP">המקבל משלם (DAP)</option><option value="DDP">השולח משלם (DDP)</option></select></div>
            <div class="field"><label for="t-vat">מספר עוסק או ח.פ. (אם יש)</label><input id="t-vat" type="text" autocomplete="off"></div>
          </div>
          <div class="row2">
            <div class="field"><label for="t-rs">סיבת המשלוח</label><select id="t-rs"><option value="">בחרו</option><option>מכירה</option><option>מתנה</option><option>דוגמה ללא תשלום</option><option>החזרה</option><option>תיקון</option><option>שימוש אישי</option><option>אחר</option></select></div>
            <div class="field"><label for="t-sd">תיאור קצר של המשלוח</label><input id="t-sd" type="text" maxlength="120"></div>
          </div>
          <div class="field"><label for="t-sg">חתימה בקבלה</label><select id="t-sg"></select></div>
          <h3>חשוב לדעת</h3>
          <label class="chk-row"><input type="checkbox" id="d-1"><span>אני מצהיר שהמשלוח אינו כולל חומרים מסוכנים או פריטים אסורים להובלה על ידי חברת השילוח או מדינת היעד. אם הצהרתי לא נכון, האחריות עליי, והמשלוח עלול להיעצר או להיהרס, בלי החזר.</span></label>
          <label class="chk-row"><input type="checkbox" id="d-2"><span>קראתי ואני מסכים לתנאי השימוש ולמדיניות הפרטיות.</span></label>
          <label class="chk-row"><input type="checkbox" id="d-3"><span>אני מסכים שאם המשקל או המידות שהזנתי שגויים, יתווסף חיוב לפי המדידה של חברת השילוח.</span></label>
          <p class="err" id="e5" role="alert" hidden></p>
          <div class="nav2"><button type="button" class="btn btn-go" id="go5">שליחת ההזמנה</button><button type="button" class="btn-back" id="b5">→ חזרה</button></div>
          <button type="button" class="btn-save" id="save-later">שמירה והמשך מאוחר יותר</button>
        </section>

        <section class="ostep" id="s6" hidden aria-labelledby="h6s">
          <h2 id="h6s" tabindex="-1">ההזמנה התקבלה</h2>
          <p class="bigid">מספר הזמנה: <b class="latin" id="oid"></b></p>
          <p id="done-t"></p>
          <a class="btn btn-go" id="done-wa" href="https://wa.me/" target="_blank" rel="noopener">שליחת מספר ההזמנה בוואטסאפ</a>
          <a class="btn btn-line-dark" href="index.html">חזרה לדף הראשי</a>
        </section>
        <div class="later" id="later" hidden>
          <b>ההזמנה נשמרה.</b>
          <p>כדי להמשיך מאוחר יותר, שמרו את הקישור הזה. הוא פותח את ההזמנה שלכם בדיוק איפה שעצרתם:</p>
          <div class="linkrow"><input id="later-url" type="text" readonly aria-label="קישור להמשך ההזמנה"><button type="button" class="btn btn-go btn-sm" id="later-copy">העתקה</button></div>
        </div>
      </form>
    </div>

    <aside class="ord-sum" aria-label="סיכום הזמנה">
      <details id="sumd" open><summary><span>סיכום הזמנה</span><b id="sum-top"></b></summary>
        <div class="sum-in">
          <div id="sum-route" class="sum-route"></div>
          <div id="sum-cargo" class="sum-line"></div>
          <div id="sum-svc" class="sum-svc"></div>
          <dl id="sum-lines" class="sum-dl"></dl>
          <div class="sum-total"><span>סה״כ</span><b id="sum-total">-</b></div>
          <div class="promo" id="promo" hidden>
            <label for="pm-code" class="plbl">קוד קופון</label>
            <div class="prow2"><input id="pm-code" type="password" autocomplete="off" spellcheck="false" autocapitalize="off" aria-describedby="pm-msg"><button type="button" class="btn btn-sm" id="pm-go">אימות</button></div>
            <div id="pm-ov" class="pm-ov" hidden>
              <div class="field"><label for="pm-price">מחיר חדש</label><input id="pm-price" type="number" min="0" step="0.01" inputmode="decimal"></div>
              <div class="field"><label for="pm-why">סיבה</label><input id="pm-why" type="text" maxlength="200" autocomplete="off"></div>
              <button type="button" class="btn btn-go btn-sm" id="pm-apply">עדכון מחיר</button>
            </div>
            <p id="pm-msg" class="pmsg" role="status"></p>
          </div>
        </div>
      </details>
    </aside>
  </div>
</div></section>

<dialog id="chg" class="dlg" aria-labelledby="chg-h">
  <div class="dlg-in">
    <h2 id="chg-h">המחיר עודכן</h2>
    <p id="chg-t"></p>
    <div class="chg-nums"><span>מחיר קודם <s id="chg-from"></s></span><span>מחיר חדש <b id="chg-to"></b></span></div>
    <p id="chg-why" class="chg-why"></p>
    <button type="button" class="btn btn-go" id="chg-ok">אישור והמשך</button>
    <button type="button" class="btn btn-line-dark" id="chg-back">חזרה לשינוי הכתובת</button>
  </div>
</dialog>
"""

ORDER_CSS = r"""
.ord { padding-top: 8px; }
.ord h2 { font-size: 1.6rem; margin: 0 0 12px; } .ord h3 { font-size: 1.15rem; margin: 22px 0 8px; }
.ord .ostep { display: grid; gap: 14px; background: var(--surface); border: 1px solid var(--line); border-radius: 14px; padding: 22px 20px; }
.ord-top { display: flex; flex-wrap: wrap; gap: 12px 24px; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.prog { list-style: none; margin: 0; padding: 0; display: flex; gap: 6px; counter-reset: p; flex-wrap: wrap; }
.prog li { counter-increment: p; display: inline-flex; align-items: center; gap: 8px; padding: 6px 12px 6px 10px; border-radius: 999px; background: var(--bg); color: var(--muted); font-weight: 800; font-size: .88rem; border: 1px solid var(--line); }
.prog li::before { content: counter(p); display: inline-grid; place-items: center; width: 22px; height: 22px; border-radius: 50%; background: var(--line); color: var(--ink); font-size: .8rem; }
.prog li.on { background: var(--ink); color: #fff; border-color: var(--ink); } .prog li.on::before { background: var(--cyan); color: var(--ink-deep); }
.prog li.done { color: var(--ink); } .prog li.done::before { content: "✓"; background: var(--cyan); }
.acct { font-size: .95rem; color: var(--muted); display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
.acct button { background: none; border: 0; color: var(--ink); font: 800 .95rem inherit; font-family: inherit; text-decoration: underline; cursor: pointer; padding: 6px; }
.ord-grid { display: grid; grid-template-columns: minmax(0, 1fr) 340px; gap: 22px; align-items: start; }
.ord-grid.nosum { grid-template-columns: minmax(0, 1fr); }
.ord-sum { position: sticky; top: 84px; background: var(--surface); border: 1px solid var(--line); border-radius: 14px; overflow: hidden; }
.ord-sum summary { display: flex; justify-content: space-between; align-items: center; gap: 10px; padding: 14px 16px; cursor: pointer; font-weight: 900; background: var(--bg); list-style: none; }
.ord-sum summary::-webkit-details-marker { display: none; }
.ord-sum summary b { color: var(--ink); font-variant-numeric: tabular-nums; }
.sum-in { padding: 14px 16px 16px; display: grid; gap: 10px; }
.sum-route { font-weight: 800; } .sum-line { color: var(--muted); font-size: .95rem; }
.sum-svc { font-weight: 800; color: var(--ink); } .sum-svc small { display: block; color: var(--muted); font-weight: 600; }
.sum-dl { margin: 0; display: grid; gap: 6px; } .sum-dl div { display: flex; justify-content: space-between; gap: 10px; font-size: .95rem; }
.sum-dl dd { margin: 0; font-weight: 700; font-variant-numeric: tabular-nums; }
.sum-total { display: flex; justify-content: space-between; border-top: 1px solid var(--line); padding-top: 10px; font-size: 1.15rem; font-weight: 900; }
.promo { border-top: 1px dashed var(--line); padding-top: 12px; display: grid; gap: 8px; }
.plbl { font-weight: 700; font-size: .9rem; } .prow2 { display: flex; gap: 8px; } .prow2 input { flex: 1; min-width: 0; min-height: 44px; padding: 8px 12px; border: 1.5px solid var(--line); border-radius: 8px; background: var(--bg); font: 600 1rem inherit; font-family: inherit; color: var(--fg); }
.prow2 .btn { width: auto; margin: 0; padding-inline: 16px; background: var(--ink); color: #fff; }
.pm-ov { display: grid; gap: 8px; padding: 10px; background: var(--bg); border-radius: 10px; } .pmsg { font-size: .9rem; min-height: 1.2em; color: var(--muted); }
.pmsg.bad { color: #B3261E; } .pmsg.good { color: #1B7A3E; font-weight: 700; }
.prow { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)) 40px; gap: 8px; align-items: end; padding: 10px; background: var(--bg); border-radius: 10px; margin-bottom: 8px; }
.prow .field label { font-size: .8rem; } .prow .field input { min-height: 44px; padding: 8px; }
.prow .rm { width: 40px; height: 44px; border: 0; border-radius: 8px; background: transparent; color: var(--muted); font-size: 1.3rem; cursor: pointer; }
.prow .rm:hover { color: #B3261E; }
.btn-add, .btn-save { justify-self: start; background: none; border: 1.5px dashed var(--muted); color: var(--ink); border-radius: 10px; min-height: 44px; padding: 8px 16px; font: 800 .95rem inherit; font-family: inherit; cursor: pointer; }
.btn-save { border-style: solid; justify-self: center; border-color: var(--line); }
.offers { display: grid; gap: 12px; }
.offer { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 10px 16px; align-items: center; padding: 16px; border: 1.5px solid var(--line); border-radius: 12px; background: var(--surface); }
.offer h3 { margin: 0; font-size: 1.1rem; } .offer .meta2 { color: var(--muted); font-size: .92rem; display: flex; flex-wrap: wrap; gap: 4px 14px; }
.offer .pr { font-size: 1.5rem; font-weight: 900; color: var(--ink); font-variant-numeric: tabular-nums; text-align: end; display: grid; gap: 2px; justify-items: end; }
.offer .pr-before { font-size: .95rem; font-weight: 700; color: #c62828; text-decoration: line-through; }
.offer .btn { grid-column: 1 / -1; margin: 0; }
.testbar { background: #FFF4D6; border: 1px solid #E8C766; color: #6B4E00; padding: 10px 14px; border-radius: 10px; font-weight: 700; font-size: .92rem; }
.note-assumed { background: var(--bg); border: 1px solid var(--line); padding: 10px 14px; border-radius: 10px; font-size: .92rem; margin: 0; }
.manual { background: var(--bg); border-radius: 12px; padding: 18px; display: grid; gap: 10px; } .manual p { margin: 0; color: var(--muted); }
.pair { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }
.party { border: 1px solid var(--line); border-radius: 12px; padding: 14px 14px 16px; display: grid; gap: 10px; margin: 0; min-width: 0; }
.party legend { font-weight: 900; padding: 0 8px; color: var(--ink); font-size: 1.1rem; }
.party .row2 { gap: 10px; }
.party .ro input { background: var(--line); color: var(--muted); }
.item { display: grid; gap: 10px; padding: 12px; background: var(--bg); border-radius: 10px; margin-bottom: 10px; position: relative; }
.item .g { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 8px; } .item .g.w { grid-template-columns: 2fr 1fr 1fr 1fr; }
.item .rm { position: absolute; inset-block-start: 6px; inset-inline-start: 6px; width: 34px; height: 34px; border: 0; background: transparent; font-size: 1.2rem; cursor: pointer; color: var(--muted); }
.item .field label { font-size: .8rem; } .item .field input, .item .field select { min-height: 44px; padding: 8px; }
.nav2 { display: flex; flex-wrap: wrap; align-items: center; gap: 12px; } .nav2 .btn { width: auto; flex: 1 1 220px; margin: 0; }
.note2 { color: var(--muted); font-size: .92rem; margin: 0; }
.resume { display: flex; flex-wrap: wrap; align-items: center; gap: 10px 14px; background: var(--sea-soft); border-radius: 12px; padding: 12px 16px; margin-bottom: 16px; font-weight: 700; }
.resume .btn { width: auto; margin: 0; }
.bigid { font-size: 1.3rem; } .bigid b { font-size: 1.6rem; color: var(--ink); letter-spacing: .04em; }
.later { margin-top: 14px; background: var(--sea-soft); border-radius: 12px; padding: 16px; display: grid; gap: 8px; } .later p { margin: 0; }
.linkrow { display: flex; gap: 8px; } .linkrow input { flex: 1; min-width: 0; min-height: 44px; padding: 8px 12px; border: 1.5px solid var(--line); border-radius: 8px; font: 600 .9rem monospace; direction: ltr; background: var(--surface); }
.linkrow .btn { width: auto; margin: 0; }
.chg-nums { display: flex; gap: 20px; flex-wrap: wrap; font-weight: 700; } .chg-nums b { font-size: 1.4rem; color: var(--ink); } .chg-nums s { color: var(--muted); }
.chg-why { background: var(--bg); padding: 12px 14px; border-radius: 10px; margin: 0; font-weight: 600; }
.ostep .btn, .ostep .nav2 .btn { margin-top: 0; }
.quote-wait { display: flex; align-items: center; gap: 10px; margin-top: 10px; color: var(--muted); font-weight: 600; font-size: .95rem; }
.quote-wait .spin { width: 18px; height: 18px; border: 2.5px solid var(--line); border-top-color: var(--accent); border-radius: 50%; flex: none; animation: quote-spin .8s linear infinite; }
@keyframes quote-spin { to { transform: rotate(360deg); } }
@media (max-width: 900px) {
  .ord-grid { grid-template-columns: minmax(0, 1fr); } .ord-sum { position: static; order: -1; }
  .pair { grid-template-columns: minmax(0, 1fr); }
}
@media (max-width: 560px) {
  .ord .ostep { padding: 18px 14px; } .prow { grid-template-columns: repeat(6, minmax(0, 1fr)); } .prow .field:nth-child(-n+2) { grid-column: span 3; } .prow .field:nth-child(n+3):nth-child(-n+5) { grid-column: span 2; } .prow .rm { grid-column: 1 / -1; width: 100%; height: 36px; font-size: 1rem; } .prow .rm::after { content: " הסרה"; font-size: .9rem; }
  .item .g, .item .g.w { grid-template-columns: repeat(2, minmax(0, 1fr)); } .prog li { font-size: .8rem; padding-inline: 8px; }
  .prog li:not(.on) { font-size: 0; padding: 4px; gap: 0; } .prog li:not(.on)::before { font-size: .8rem; }
}
"""

ORDER_JS = r"""
(function () {
  var CT = window.CT, $ = function (id) { return document.getElementById(id); };
  var COUNTRIES = %(countries)s.split("|").map(function (s) { var i = s.indexOf(" "); return { c: s.slice(0, i), n: s.slice(i + 1) }; });
  var byCode = {}, byName = {}; COUNTRIES.forEach(function (o) { byCode[o.c] = o; byName[o.n] = o; });
  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var money = function (n) { return n == null ? "-" : (n < 0 ? "−" : "") + "₪" + Math.abs(Number(n)).toLocaleString("he-IL", { minimumFractionDigits: 2, maximumFractionDigits: 2 }); };
  var emoji = function (c) { return String.fromCodePoint.apply(null, c.toUpperCase().split("").map(function (ch) { return 127397 + ch.charCodeAt(0); })); };
  var P0 = function () { return { qty: 1, kg: "", l: "", w: "", h: "" }; };
  var I0 = function () { return { desc: "", value: "", currency: "USD", qty: 1, hs: "", originName: "", madeOf: "" }; };
  var S = { step: 1, customerType: "", from: "il", to: "", type: "parcel", parcels: [P0()], cont: { size: "מכולה 20 פיט", qty: 1 },
    sender: {}, recipient: {}, items: [I0()], insurance: { requested: false, amount: "" }, pickup: { date: "", time: "" }, terms: { incoterm: "", vat: "", reason: "", shortDesc: "" },
    signature: "none", declarations: { dangerous: false, terms: false, dims: false }, orderId: null, token: null, selectedOffer: null, quote: null, offers: [], manual: false,
    testMode: false, sigFee: null, addresses: [], ovTok: null };
  var STEP_ORDER = [1, 2, 3, 4, 5];

  /* ---------- helpers ---------- */
  var num = function (v) { return parseFloat(v) || 0; };
  function say(id, m) { var e = $(id); e.textContent = m || ""; e.hidden = !m; }
  function getPath(o, p) { return p.split(".").reduce(function (a, k) { return a == null ? "" : a[k]; }, o); }
  function setPath(o, p, v) { var k = p.split("."), last = k.pop(); k.forEach(function (x) { o = o[x] = o[x] || {}; }); o[last] = v; }
  function flagEl(c) {
    var im = document.createElement("img"); im.className = "flg"; im.alt = ""; im.width = 28; im.height = 20; im.loading = "lazy"; im.src = "https://flagcdn.com/w40/" + c + ".png";
    im.onerror = function () { var s = document.createElement("span"); s.className = "flg em"; s.textContent = emoji(c); if (im.parentNode) im.parentNode.replaceChild(s, im); }; return im;
  }
  function show(n) {
    S.step = n;
    for (var i = 1; i <= 6; i++) $("s" + i).hidden = i !== n;
    $("later").hidden = true;
    document.querySelectorAll("#prog li").forEach(function (li) { var s = +li.getAttribute("data-s"); li.classList.toggle("on", s === n); li.classList.toggle("done", s < n && n <= 5); });
    $("prog").hidden = n === 6;
    $("promo").hidden = !(S.orderId && S.quote && S.quote.total != null && n >= 4 && n <= 5);
    var h = $("s" + n).querySelector("h2"); if (h) { h.focus({ preventScroll: true }); }
    var top = document.querySelector(".ord"); if (top) top.scrollIntoView({ block: "start" });
    render();
  }

  /* ---------- country pickers ---------- */
  var pickers = {};
  document.querySelectorAll(".cpick").forEach(function (box) {
    var key = box.getAttribute("data-key"), btn = document.createElement("button"), panel = document.createElement("div"), open = false;
    btn.type = "button"; btn.className = "cbtn"; btn.setAttribute("aria-haspopup", "listbox"); btn.setAttribute("aria-expanded", "false");
    panel.className = "cpanel"; panel.hidden = true;
    var inp = document.createElement("input"); inp.type = "search"; inp.placeholder = "חיפוש מדינה"; inp.setAttribute("aria-label", "חיפוש מדינה"); inp.autocomplete = "off";
    var ul = document.createElement("ul"); ul.setAttribute("role", "listbox"); panel.appendChild(inp); panel.appendChild(ul); box.appendChild(btn); box.appendChild(panel);
    function paint() {
      btn.innerHTML = ""; var c = S[key], nm = document.createElement("span"); nm.className = "cname";
      if (c) { btn.appendChild(flagEl(c)); nm.textContent = byCode[c].n; } else { nm.className += " ph"; nm.textContent = "בחרו מדינה"; }
      btn.appendChild(nm); var ch = document.createElement("i"); ch.className = "chev"; btn.appendChild(ch);
    }
    function list() {
      var q = inp.value.trim(); ul.innerHTML = ""; var n = 0;
      COUNTRIES.forEach(function (o) {
        if (q && o.n.indexOf(q) < 0) return; n++;
        var li = document.createElement("li"); li.setAttribute("role", "option"); if (S[key] === o.c) li.className = "sel";
        var b = document.createElement("button"); b.type = "button"; b.appendChild(flagEl(o.c)); var t = document.createElement("span"); t.textContent = o.n; b.appendChild(t);
        b.addEventListener("click", function () { S[key] = o.c; close(); paint(); resetOffers(); render(); }); li.appendChild(b); ul.appendChild(li);
      });
      if (!n) { var d = document.createElement("li"); d.className = "none"; d.textContent = "לא נמצאה מדינה בשם הזה."; ul.appendChild(d); }
    }
    function close() { open = false; panel.hidden = true; btn.setAttribute("aria-expanded", "false"); }
    function openIt() { Object.keys(pickers).forEach(function (k) { if (k !== key) pickers[k].close(); }); open = true; inp.value = ""; list(); panel.hidden = false; btn.setAttribute("aria-expanded", "true"); inp.focus(); }
    btn.addEventListener("click", function () { open ? close() : openIt(); }); inp.addEventListener("input", list);
    inp.addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); var f = ul.querySelector("button"); if (f) f.click(); } });
    panel.addEventListener("keydown", function (e) { if (e.key === "Escape") { close(); btn.focus(); } });
    pickers[key] = { close: close, paint: paint }; paint();
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".cpick")) Object.keys(pickers).forEach(function (k) { pickers[k].close(); }); });
  $("o-swap").addEventListener("click", function () { var t = S.from; S.from = S.to; S.to = t; pickers.from.paint(); pickers.to.paint(); resetOffers(); render(); });
  function resetOffers() { S.offers = []; S.selectedOffer = null; S.quote = null; S.manual = false; S.ovTok = null; }

  /* ---------- step 1: who, route, cargo ---------- */
  function chipGroup(id, attr, get, set) {
    document.querySelectorAll("#" + id + " .chip").forEach(function (b) {
      b.addEventListener("click", function () { set(b.getAttribute(attr)); chipPaint(id, attr, get()); });
    });
  }
  function chipPaint(id, attr, val) { document.querySelectorAll("#" + id + " .chip").forEach(function (b) { var on = b.getAttribute(attr) === val; b.classList.toggle("on", on); b.setAttribute("aria-pressed", on); }); }
  chipGroup("o-ct", "data-v", function () { return S.customerType; }, function (v) { S.customerType = v; resetOffers(); render(); });
  chipGroup("o-type", "data-t", function () { return S.type; }, function (v) { S.type = v; resetOffers(); render(); });
  chipGroup("o-feet", "data-v", function () { return S.cont.size; }, function (v) { S.cont.size = v; });
  $("o-cq").addEventListener("input", function () { S.cont.qty = Math.max(1, Math.round(num(this.value)) || 1); });
  $("o-addp").addEventListener("click", function () { if (S.parcels.length < 20) { S.parcels.push(P0()); renderParcels(); } });
  function renderParcels() {
    var box = $("o-parcels"), word = S.type === "pallet" ? "משטח" : "חבילה"; box.innerHTML = "";
    if (S.type === "doc" || S.type === "cont") return;
    S.parcels.forEach(function (p, i) {
      var r = document.createElement("div"); r.className = "prow";
      r.innerHTML = [["qty", "כמות", "1", "1"], ["kg", "משקל (ק״ג)", "0.1", "0"], ["l", "אורך (ס״מ)", "1", "0"], ["w", "רוחב (ס״מ)", "1", "0"], ["h", "גובה (ס״מ)", "1", "0"]].map(function (f) {
        return '<div class="field"><label>' + (S.parcels.length > 1 ? word + " " + (i + 1) + ": " : "") + f[1] + '</label><input type="number" min="0" step="' + f[2] + '" inputmode="decimal" data-k="' + f[0] + '" value="' + esc(p[f[0]]) + '" placeholder="' + f[3] + '"></div>';
      }).join("") + (S.parcels.length > 1 ? '<button type="button" class="rm" aria-label="הסרה">×</button>' : "<span></span>");
      r.querySelectorAll("input").forEach(function (inp) { inp.addEventListener("input", function () { p[inp.getAttribute("data-k")] = inp.value; resetOffers(); calc(); }); });
      var rm = r.querySelector(".rm"); if (rm) rm.addEventListener("click", function () { S.parcels.splice(i, 1); resetOffers(); renderParcels(); calc(); });
      box.appendChild(r);
    });
    $("o-addp").textContent = "+ הוספת " + word;
  }
  function calc() {
    var real = 0, vol = 0; S.parcels.forEach(function (p) { var q = Math.max(1, num(p.qty)); real += num(p.kg) * q; vol += num(p.l) * num(p.w) * num(p.h) * q / 5000; });
    var b = Math.max(real, vol);
    $("o-calc").innerHTML = (S.type === "parcel" || S.type === "pallet") && b ? "משקל פיזי: <b>" + Math.round(real * 10) / 10 + "</b> ק״ג · משקל נפחי: <b>" + Math.round(vol * 10) / 10 + "</b> ק״ג · משקל לחיוב: <b>" + Math.round(b * 10) / 10 + "</b> ק״ג" : "";
  }

  /* ---------- payloads ---------- */
  function payload(extra) {
    var it = S.items.map(function (i) { var c = byName[(i.originName || "").trim()]; return { desc: i.desc, value: num(i.value), currency: i.currency, qty: num(i.qty) || 1, hs: i.hs, origin: c ? c.c : "", madeOf: i.madeOf }; });
    var b = {
      customerType: S.customerType, from: S.from, to: S.to, type: S.type, mode: "intl",
      parcels: (S.type === "doc" ? [{ qty: 1, kg: 0.5, l: 2, w: 2, h: 2 }] : S.parcels.map(function (p) { return { qty: num(p.qty) || 1, kg: num(p.kg), l: num(p.l), w: num(p.w), h: num(p.h) }; })),
      cont: S.cont, selectedOffer: S.selectedOffer, signature: S.signature,
      sender: Object.assign({}, S.sender, { country: S.from }), recipient: Object.assign({}, S.recipient, { country: S.to }),
      zips: { from: S.sender.zip || "", to: S.recipient.zip || "" },
      items: it, insurance: { requested: S.insurance.requested, amount: num(S.insurance.amount) }, pickup: S.pickup, terms: S.terms, declarations: S.declarations, step: S.step
    };
    if (S.orderId) b.orderId = S.orderId;
    return Object.assign(b, extra || {});
  }
  var hdr = function () { return S.token ? { "x-order-token": S.token } : {}; };

  /* ---------- step 1 -> 2 : get prices ---------- */
  $("go1").addEventListener("click", async function () {
    var m = "";
    if (!S.customerType) m = "בחרו אם השולח פרטי או עסקי.";
    else if (!S.from || !S.to) m = "בחרו מדינת מוצא ומדינת יעד.";
    else if (S.from === S.to) m = "מדינת המוצא והיעד זהות. בחרו יעד אחר.";
    else if ((S.type === "parcel" || S.type === "pallet") && !S.parcels.some(function (p) { return num(p.kg) > 0; })) m = "הוסיפו משקל, גם הערכה מספיקה.";
    if (m) return say("e1", m);
    say("e1", ""); var b = this; b.disabled = true; b.hidden = true;
    var wait = $("go1-wait"), waitT = $("go1-wait-t"), msgs = ["מתחברים למערכת השילוח...", "בודקים מחירים מול הספק...", "משווים בין שירותים...", "מכינים את ההצעה הטובה ביותר..."], mi = 0;
    waitT.textContent = msgs[0]; wait.hidden = false;
    var mt = setInterval(function () { mi = (mi + 1) % msgs.length; waitT.textContent = msgs[mi]; }, 900);
    var minWait = new Promise(function (res) { setTimeout(res, 1400); });
    var j = (await Promise.all([CT.api("POST", "/quote", payload()), minWait]))[0];
    clearInterval(mt); wait.hidden = true; b.hidden = false; b.disabled = false; b.textContent = "חישוב מחיר";
    if (!j.ok) return say("e1", j.error && j.error.length > 3 && j.error !== "server" && j.error !== "network" ? j.error : "לא הצלחנו לחשב מחיר כרגע. נסו שוב בעוד רגע.");
    S.offers = j.offers || []; S.manual = !!j.manual; S.testMode = !!j.testMode; S.assumed = j.assumed || {}; S.selectedOffer = null; S.quote = null;
    show(2);
  });
  function renderOffers() {
    var box = $("offers"); box.innerHTML = ""; $("testbar").hidden = !(S.testMode && S.offers.length);
    var as = S.assumed || {}, parts = [];
    if (as.from) parts.push("במוצא: " + as.from); if (as.to) parts.push("ביעד: " + as.to);
    $("assumed").textContent = parts.length ? "המחיר מחושב לפי העיר המרכזית של כל מדינה (" + parts.join(", ") + "). בהמשך נבקש כתובת מדויקת, והמחיר יתעדכן אם יהיה שינוי, למשל באזור מרוחק." : "";
    $("assumed").hidden = !parts.length;
    $("manual").hidden = !S.manual;
    S.offers.forEach(function (o) {
      var d = document.createElement("div"); d.className = "offer";
      d.innerHTML = '<div><h3>' + esc(o.carrier) + ' · ' + esc(o.service) + '</h3><div class="meta2"><span>זמן משוער: ' + esc(o.days) + ' ימי עסקים</span>' + (o.includes || []).map(function (x) { return "<span>" + esc(x) + "</span>"; }).join("") + '</div></div><div class="pr">' + (o.originalTotal != null ? '<s class="pr-before">' + money(o.originalTotal) + "</s>" : "") + '<bdi>' + money(o.total) + '</bdi></div>' +
        '<button type="button" class="btn btn-go">בחירה והמשך</button>';
      d.querySelector("button").addEventListener("click", function () { S.selectedOffer = o.id; S.quote = { total: o.total, originalTotal: o.originalTotal, lines: o.lines, carrier: o.carrier, service: o.service, days: o.days }; show(3); });
      box.appendChild(d);
    });
  }
  $("go-manual").addEventListener("click", function () { S.selectedOffer = null; S.quote = null; show(3); });
  $("b2").addEventListener("click", function () { show(1); });

  /* ---------- step 3: addresses ---------- */
  var ADDR = [["country", "מדינה", "ro"], ["city", "עיר"], ["state", "מדינה או מחוז (אם יש)"], ["street", "רחוב"], ["house", "מספר בית"], ["zip", "מיקוד"], ["details", "פרטים נוספים למסירה"], ["name", "שם איש קשר"], ["company", "חברה (אם יש)"], ["email", "אימייל"], ["phone", "טלפון"]];
  function party(kind) {
    var fs = $("p-" + kind), who = kind;
    var f = function (k, l, cls, type) { return '<div class="field' + (cls ? " " + cls : "") + '"><label for="' + kind + '-' + k + '">' + l + '</label><input id="' + kind + '-' + k + '" data-b="' + kind + "." + k + '" type="' + (type || "text") + '"' + (cls === "ro" ? " readonly tabindex=-1" : "") + ' autocomplete="off"' + (k === "phone" ? ' inputmode="tel"' : "") + (k === "email" ? ' inputmode="email"' : "") + '></div>'; };
    fs.innerHTML = '<legend>' + (kind === "sender" ? "שולח" : "נמען") + '</legend><div class="bookrow" id="bk-' + kind + '" hidden></div>' +
      f("country", "מדינה", "ro") + '<div class="row2">' + f("city", "עיר") + f("state", "מדינה או מחוז") + '</div><div class="row2">' + f("street", "רחוב") + f("house", "מספר בית") + '</div>' +
      f("zip", "מיקוד") + f("details", "פרטים נוספים למסירה") + '<div class="row2">' + f("name", "שם איש קשר") + f("company", "חברה (אם יש)") + '</div><div class="row2">' + f("email", "אימייל", "", "email") + f("phone", "טלפון (עם קידומת מדינה)", "", "tel") + '</div>' +
      (kind === "recipient" ? '<label class="chk-row"><input type="checkbox" id="rec-res"> כתובת מגורים</label>' : "") +
      '<div class="savebox" id="sv-' + kind + '" hidden><label class="chk-row"><input type="checkbox" id="svc-' + kind + '"> שמירת הכתובת בספר הכתובות שלי</label><div class="field" id="svn-' + kind + '" hidden><label for="svi-' + kind + '">כינוי לכתובת</label><input id="svi-' + kind + '" type="text" maxlength="40"></div></div>';
  }
  party("sender"); party("recipient");
  $("rec-res").addEventListener("change", function () { S.recipient.residential = this.checked; });
  ["sender", "recipient"].forEach(function (k) { $("svc-" + k).addEventListener("change", function () { $("svn-" + k).hidden = !this.checked; }); });
  document.addEventListener("input", function (e) { var b = e.target.getAttribute && e.target.getAttribute("data-b"); if (b) setPath(S, b, e.target.value); });
  document.addEventListener("change", function (e) {
    var b = e.target.getAttribute && e.target.getAttribute("data-b");
    if (b && /\.zip$/.test(b)) requote();
  });
  function fillForm() {
    S.sender.country = S.from; S.recipient.country = S.to;
    document.querySelectorAll("[data-b]").forEach(function (i) { var v = getPath(S, i.getAttribute("data-b")); if (i.id.indexOf("-country") > 0) v = byCode[v] ? byCode[v].n : ""; i.value = v == null ? "" : v; });
    $("rec-res").checked = !!S.recipient.residential;
    var sg = $("t-sg"), fee = S.sigFee && S.customerType ? S.sigFee[S.customerType] : null;
    sg.innerHTML = '<option value="none">לא נדרשת חתימה</option><option value="standard">חתימה בקבלה' + (fee != null ? " (תוספת " + money(fee) + ")" : "") + '</option><option value="adult">חתימת מבוגר בקבלה' + (fee != null ? " (תוספת " + money(fee) + ")" : "") + '</option>';
    sg.value = S.signature;
    $("t-inc").value = S.terms.incoterm || ""; $("t-vat").value = S.terms.vat || ""; $("t-rs").value = S.terms.reason || ""; $("t-sd").value = S.terms.shortDesc || "";
    $("d-1").checked = S.declarations.dangerous; $("d-2").checked = S.declarations.terms; $("d-3").checked = S.declarations.dims;
    $("o-pd").value = S.pickup.date || ""; $("o-pt").value = S.pickup.time || ""; $("o-ins").checked = S.insurance.requested; $("o-insbox").hidden = !S.insurance.requested; $("o-insv").value = S.insurance.amount || "";
    var d = new Date(); $("o-pd").min = d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
  }
  function validAddr(a, t) {
    if (!a.city || !a.street) return "מלאו עיר ורחוב של ה" + t + ".";
    if (!a.name) return "מלאו שם איש קשר של ה" + t + ".";
    if ((a.phone || "").replace(/\D/g, "").length < 7) return "מלאו טלפון של ה" + t + ".";
    return "";
  }
  async function saveOrder(extra) {
    var j = await CT.api("POST", "/order/save", payload(extra), hdr());
    if (j.ok && j.token) { S.token = j.token; }
    if (j.ok) { S.orderId = j.orderId; try { localStorage.setItem("ct_last", JSON.stringify({ id: S.orderId, token: S.token })); } catch (e) {} if (j.quote && j.quote.total != null && S.quote) { S.quote.total = j.quote.total; S.quote.originalTotal = j.quote.originalTotal; } }
    return j;
  }
  $("go3").addEventListener("click", async function () {
    var m = validAddr(S.sender, "שולח") || validAddr(S.recipient, "נמען"); if (m) return say("e3", m);
    say("e3", ""); var b = this; b.disabled = true;
    var j = await saveOrder({ step: 4 }); b.disabled = false;
    if (!j.ok) return say("e3", j.error && j.error.length > 3 && j.error !== "server" ? j.error : "לא הצלחנו לשמור. נסו שוב.");
    if (CT.user) { ["sender", "recipient"].forEach(function (k) { if ($("svc-" + k).checked) CT.api("POST", "/addresses", { nickname: $("svi-" + k).value, address: Object.assign({}, S[k], { country: k === "sender" ? S.from : S.to }) }); }); }
    show(4);
  });
  $("b3").addEventListener("click", function () { show(S.manual || !S.offers.length ? 1 : 2); });

  /* ---------- price re-check (zip / signature) with explanation pop-up ---------- */
  async function requote() {
    if (!S.selectedOffer || !S.quote || !S.customerType) return;
    var j = await CT.api("POST", "/quote", payload({ selected: S.selectedOffer, previousTotal: S.quote.total, previousKeys: (S.quote.lines || []).map(function (l) { return l.key; }) }));
    if (!j.ok) return;
    var o = (j.offers || []).filter(function (x) { return x.id === S.selectedOffer; })[0]; if (!o) return;
    S.offers = j.offers; S.quote = { total: o.total, originalTotal: o.originalTotal, lines: o.lines, carrier: o.carrier, service: o.service, days: o.days };
    if (j.change) S.ovTok = null;
    render(); if (j.change) showChange(j.change);
  }
  var REASONS = { remote: "אחת הכתובות נמצאת באזור מרוחק, ולכן חברת השילוח גובה תוספת עבור אזור מרוחק.", signature: "בחרתם דרישת חתימה בקבלה, ולכן נוספה תוספת עבור שירות החתימה." };
  var chgFocus = null;
  function showChange(c) {
    $("chg-t").textContent = c.delta > 0 ? "לאחר בדיקת הכתובת המדויקת, המחיר עלה." : "לאחר בדיקת הכתובת המדויקת, המחיר ירד.";
    $("chg-from").textContent = money(c.from); $("chg-to").textContent = money(c.to);
    $("chg-why").textContent = (c.reasons || []).map(function (r) { return REASONS[r]; }).filter(Boolean).join(" ") || "המחיר מתעדכן לפי הכתובת המדויקת שהזנתם.";
    $("chg-back").hidden = !(c.reasons || []).includes("remote");
    var d = $("chg"); if (!d.open) d.showModal();
  }
  $("chg-ok").addEventListener("click", function () { $("chg").close(); });
  $("chg-back").addEventListener("click", function () { $("chg").close(); if (S.step !== 3) show(3); setTimeout(function () { var z = $("recipient-zip"); if (z) z.focus(); }, 60); });

  /* ---------- step 4: goods ---------- */
  function renderItems() {
    var box = $("items"); box.innerHTML = "";
    var dl = $("cl-countries"); if (!dl) { dl = document.createElement("datalist"); dl.id = "cl-countries"; dl.innerHTML = COUNTRIES.map(function (o) { return '<option value="' + esc(o.n) + '">'; }).join(""); document.body.appendChild(dl); }
    S.items.forEach(function (it, i) {
      var d = document.createElement("div"); d.className = "item";
      d.innerHTML = (S.items.length > 1 ? '<button type="button" class="rm" aria-label="הסרת פריט">×</button>' : "") +
        '<div class="g w"><div class="field"><label>תיאור הסחורה</label><input data-k="desc" type="text" maxlength="200" value="' + esc(it.desc) + '"></div>' +
        '<div class="field"><label>שווי ליחידה</label><input data-k="value" type="number" min="0" step="0.01" inputmode="decimal" value="' + esc(it.value) + '"></div>' +
        '<div class="field"><label>מטבע</label><select data-k="currency"><option>USD</option><option>EUR</option><option>ILS</option><option>GBP</option></select></div>' +
        '<div class="field"><label>כמות</label><input data-k="qty" type="number" min="1" inputmode="numeric" value="' + esc(it.qty) + '"></div></div>' +
        '<div class="g"><div class="field"><label>קוד מכס (HS), אם ידוע</label><input data-k="hs" type="text" inputmode="numeric" maxlength="20" value="' + esc(it.hs) + '"></div>' +
        '<div class="field"><label>ארץ ייצור</label><input data-k="originName" list="cl-countries" type="text" autocomplete="off" value="' + esc(it.originName) + '"></div>' +
        '<div class="field"><label>עשוי מ</label><input data-k="madeOf" type="text" maxlength="80" value="' + esc(it.madeOf) + '"></div></div>';
      d.querySelector('[data-k="currency"]').value = it.currency;
      d.querySelectorAll("[data-k]").forEach(function (inp) { inp.addEventListener("input", function () { it[inp.getAttribute("data-k")] = inp.value; totals(); }); });
      var rm = d.querySelector(".rm"); if (rm) rm.addEventListener("click", function () { S.items.splice(i, 1); renderItems(); totals(); });
      box.appendChild(d);
    });
    totals();
  }
  function totals() {
    var t = {}; S.items.forEach(function (i) { t[i.currency] = (t[i.currency] || 0) + num(i.value) * (num(i.qty) || 1); });
    var parts = Object.keys(t).filter(function (c) { return t[c] > 0; }).map(function (c) { return t[c].toLocaleString("he-IL", { maximumFractionDigits: 2 }) + " " + c; });
    $("o-tv").innerHTML = parts.length ? "שווי כולל משוער: <b>" + parts.join(" · ") + "</b>" : "";
  }
  $("o-addi").addEventListener("click", function () { if (S.items.length < 100) { S.items.push(I0()); renderItems(); } });
  $("o-ins").addEventListener("change", function () { S.insurance.requested = this.checked; $("o-insbox").hidden = !this.checked; });
  $("o-insv").addEventListener("input", function () { S.insurance.amount = this.value; });
  $("o-pd").addEventListener("change", function () { S.pickup.date = this.value; });
  $("o-pt").addEventListener("change", function () { S.pickup.time = this.value; });
  $("go4").addEventListener("click", async function () {
    if (S.type !== "doc" && !S.items.some(function (i) { return i.desc.trim(); })) return say("e4", "כתבו תיאור של הסחורה.");
    if (!S.pickup.date) return say("e4", "בחרו תאריך איסוף.");
    say("e4", ""); var b = this; b.disabled = true; var j = await saveOrder({ step: 5 }); b.disabled = false;
    if (!j.ok) return say("e4", j.error && j.error.length > 3 && j.error !== "server" ? j.error : "לא הצלחנו לשמור. נסו שוב.");
    show(5);
  });
  $("b4").addEventListener("click", function () { show(3); });

  /* ---------- step 5: terms, declarations, send ---------- */
  $("t-inc").addEventListener("change", function () { S.terms.incoterm = this.value; });
  $("t-vat").addEventListener("input", function () { S.terms.vat = this.value; });
  $("t-rs").addEventListener("change", function () { S.terms.reason = this.value; });
  $("t-sd").addEventListener("input", function () { S.terms.shortDesc = this.value; });
  $("t-sg").addEventListener("change", function () { S.signature = this.value; requote(); });
  $("d-1").addEventListener("change", function () { S.declarations.dangerous = this.checked; });
  $("d-2").addEventListener("change", function () { S.declarations.terms = this.checked; });
  $("d-3").addEventListener("change", function () { S.declarations.dims = this.checked; });
  $("b5").addEventListener("click", function () { show(4); });
  $("go5").addEventListener("click", async function () {
    if (!(S.declarations.dangerous && S.declarations.terms && S.declarations.dims)) return say("e5", "כדי לשלוח את ההזמנה יש לאשר את שלוש ההצהרות.");
    if (!S.terms.reason) return say("e5", "בחרו סיבת משלוח.");
    say("e5", ""); var b = this; b.disabled = true; b.textContent = "שולח...";
    var j = await saveOrder({ step: 5, submit: true }); b.disabled = false; b.textContent = "שליחת ההזמנה";
    if (!j.ok) return say("e5", j.errors ? j.errors.join(" ") : (j.error && j.error.length > 3 && j.error !== "server" ? j.error : "לא הצלחנו לשלוח. נסו שוב."));
    $("oid").textContent = S.orderId;
    $("done-t").textContent = S.quote && S.quote.total != null ? "קיבלנו את ההזמנה. נציג מטעמנו ייצור איתכם קשר בהקדם." : "קיבלנו את ההזמנה. נחזור אליכם עם מחיר ואישור סופי בהקדם.";
    $("done-wa").setAttribute("data-wa", "שלום CargoTech, מספר ההזמנה שלי: " + S.orderId);
    var base = "https://wa.me/"; try { base = document.querySelector("[data-wa]").href.split("?")[0]; } catch (e) {}
    $("done-wa").href = base + "?text=" + encodeURIComponent("שלום CargoTech, מספר ההזמנה שלי: " + S.orderId);
    try { localStorage.removeItem("ct_last"); } catch (e) {}
    show(6);
  });
  $("save-later").addEventListener("click", async function () {
    var m = validAddr(S.sender, "שולח") ? "לשמירה, מלאו קודם שם, טלפון וכתובת של השולח." : ""; if (m) return say("e5", m);
    var j = await saveOrder({ step: S.step }); if (!j.ok) return say("e5", "לא הצלחנו לשמור. נסו שוב.");
    say("e5", ""); $("later-url").value = location.origin + location.pathname + "#r=" + S.orderId + "." + S.token; $("later").hidden = false;
  });
  $("later-copy").addEventListener("click", function () { var u = $("later-url"); u.select(); try { navigator.clipboard.writeText(u.value); } catch (e) { document.execCommand("copy"); } this.textContent = "הועתק"; });

  /* ---------- summary + staff price code ---------- */
  function render() {
    renderParcels(); calc(); chipPaint("o-ct", "data-v", S.customerType); chipPaint("o-type", "data-t", S.type); chipPaint("o-feet", "data-v", S.cont.size);
    $("o-cont").hidden = S.type !== "cont"; $("o-addp").hidden = S.type === "doc" || S.type === "cont"; pickers.from.paint(); pickers.to.paint();
    if (S.step === 2) renderOffers();
    if (S.step >= 3 && S.step <= 5) fillForm();
    if (S.step === 4) renderItems();
    $("sum-route").innerHTML = '<bdi>' + (S.from && byCode[S.from] ? esc(byCode[S.from].n) : "?") + '</bdi> ← <bdi>' + (S.to && byCode[S.to] ? esc(byCode[S.to].n) : "?") + '</bdi>';
    var cg = S.type === "doc" ? "מסמך" : S.type === "cont" ? S.cont.size + " × " + S.cont.qty : (S.type === "pallet" ? "משטחים" : "חבילות") + ": " + S.parcels.reduce(function (a, p) { return a + (num(p.qty) || 1); }, 0);
    $("sum-cargo").textContent = cg;
    var q = S.quote;
    $("sum-svc").innerHTML = q && q.carrier ? esc(q.carrier) + " · " + esc(q.service) + "<small>" + esc(q.days) + " ימי עסקים</small>" : (S.step >= 3 ? "מחיר ייקבע על ידינו" : "");
    $("sum-lines").innerHTML = q && q.lines ? q.lines.map(function (l) { return "<div><dt>" + esc(l.label) + "</dt><dd><bdi>" + money(l.price) + "</bdi></dd></div>"; }).join("") : "";
    var tot = q && q.total != null ? money(q.total) : "-";
    var before = q && q.originalTotal != null ? '<s class="pr-before">' + money(q.originalTotal) + "</s> " : "";
    $("sum-total").innerHTML = before + tot; $("sum-top").innerHTML = q && q.total != null ? before + tot : "";
    $("promo").hidden = !(S.orderId && q && q.total != null && S.step >= 4 && S.step <= 5);
    $("pm-ov").hidden = !S.ovTok;
    var showSum = S.step >= 2 && S.step <= 5; document.querySelector(".ord-sum").hidden = !showSum; document.querySelector(".ord-grid").classList.toggle("nosum", !showSum);
  }
  function pm(msg, kind) { var e = $("pm-msg"); e.textContent = msg || ""; e.className = "pmsg" + (kind ? " " + kind : ""); }
  $("pm-go").addEventListener("click", async function () {
    var inp = $("pm-code"), code = inp.value; inp.value = "";           /* the code is read once and wiped from the field at once */
    if (!code.trim()) return pm("הקלידו קוד.", "bad");
    var b = this; b.disabled = true; var j = await CT.api("POST", "/promo", { orderId: S.orderId, code: code }, hdr()); code = ""; b.disabled = false;
    if (!j.ok) return pm(j._status === 429 ? "נסיונות רבים מדי. נסו שוב בעוד כמה דקות." : "הקוד לא תקין.", "bad");
    S.ovTok = j.overrideToken; $("pm-price").value = j.currentTotal; $("pm-why").value = ""; pm("הקוד אומת. אפשר לעדכן מחיר.", "good"); render();
  });
  $("pm-apply").addEventListener("click", async function () {
    var price = $("pm-price").value, why = $("pm-why").value.trim();
    if (price === "" || isNaN(+price)) return pm("הקלידו מחיר.", "bad");
    if (why.length < 2) return pm("כתבו סיבה קצרה.", "bad");
    var j = await CT.api("POST", "/order/override", { orderId: S.orderId, overrideToken: S.ovTok, price: +price, reason: why }, hdr());
    if (!j.ok) { if (j._status === 403) S.ovTok = null; render(); return pm(j.error && j.error.length > 3 && j.error !== "server" ? j.error : "העדכון נכשל.", "bad"); }
    S.ovTok = null; S.quote = Object.assign({}, S.quote, { total: j.quote.total, lines: j.quote.lines }); pm("המחיר עודכן.", "good"); render();
  });

  /* ---------- account ---------- */
  function acct() {
    var a = $("acct"); a.innerHTML = "";
    if (CT.user) { var s = document.createElement("span"); s.textContent = "מחובר: " + (CT.user.email || ""); a.appendChild(s);
      var l = document.createElement("a"); l.href = "account.html"; l.textContent = "ההזמנות שלי"; l.style.cssText = "font-weight:800;color:var(--ink)"; a.appendChild(l);
      var o = document.createElement("button"); o.type = "button"; o.textContent = "התנתקות"; o.addEventListener("click", function () { CT.signOut(); }); a.appendChild(o); }
    else { var b = document.createElement("button"); b.type = "button"; b.textContent = "התחברות או הרשמה"; b.addEventListener("click", function () { CT.openAuth("in"); }); a.appendChild(b); var t = document.createElement("span"); t.textContent = "לא חובה: אפשר להזמין גם בלי להירשם."; a.appendChild(t); }
  }
  function bookRows() {
    ["sender", "recipient"].forEach(function (k) {
      var box = $("bk-" + k); box.hidden = !S.addresses.length; $("sv-" + k).hidden = !CT.user;
      if (!S.addresses.length) return;
      box.innerHTML = '<div class="field"><label for="bks-' + k + '">ספר הכתובות שלי</label><select id="bks-' + k + '"><option value="">בחרו כתובת שמורה</option>' + S.addresses.map(function (a) { return '<option value="' + esc(a.id) + '">' + esc(a.nickname) + "</option>"; }).join("") + "</select></div>";
      $("bks-" + k).addEventListener("change", function () {
        var a = S.addresses.filter(function (x) { return x.id === this.value; }.bind(this))[0]; if (!a) return;
        ["city", "state", "street", "house", "zip", "details", "name", "company", "email", "phone"].forEach(function (f) { S[k][f] = a[f] || ""; }); fillForm(); requote();
      });
    });
  }
  CT.onAuth(async function (u) {
    acct();
    if (u) {
      var m = await CT.api("GET", "/me"); if (m.ok) { S.addresses = m.addresses || []; if (!S.customerType && m.profile && m.profile.useFor) { S.customerType = m.profile.useFor; render(); } }
    } else S.addresses = [];
    bookRows();
  });
  CT.afterSignUp = function () { };

  /* ---------- resume + seed from the home page ---------- */
  function hydrate(o) {
    ["customerType", "type", "from", "to", "signature", "selectedOffer"].forEach(function (k) { if (o[k] != null) S[k] = o[k]; });
    S.parcels = (o.parcels && o.parcels.length ? o.parcels : [P0()]).map(function (p) { return { qty: p.qty, kg: p.kg || "", l: p.l || "", w: p.w || "", h: p.h || "" }; });
    S.cont = o.cont || S.cont; S.sender = o.sender || {}; S.recipient = o.recipient || {}; S.terms = Object.assign(S.terms, o.terms || {}); S.insurance = { requested: !!(o.insurance && o.insurance.requested), amount: (o.insurance && o.insurance.amount) || "" };
    S.pickup = { date: (o.pickup && o.pickup.date) || "", time: (o.pickup && o.pickup.time) || "" }; S.declarations = Object.assign(S.declarations, o.declarations || {});
    S.items = (o.items && o.items.length ? o.items : [I0()]).map(function (i) { return { desc: i.desc, value: i.value || "", currency: i.currency, qty: i.qty, hs: i.hs, originName: byCode[i.origin] ? byCode[i.origin].n : "", madeOf: i.madeOf }; });
    S.orderId = o.id; S.quote = o.quote && o.quote.total != null ? { total: o.quote.total, originalTotal: o.quote.originalTotal, lines: o.quote.lines, carrier: o.quote.carrier, service: o.quote.service, days: o.quote.days } : null;
    S.manual = !!(o.quote && o.quote.manual && o.quote.total == null);
  }
  async function resume(id, token) {
    var r = await CT.api("GET", "/order?id=" + encodeURIComponent(id), null, { "x-order-token": token });
    if (!r.ok) return false;
    S.token = token; hydrate(r.order);
    var info = await CT.api("GET", "/config"); if (info.ok) { S.sigFee = info.signatureFee; S.testMode = !!info.testMode; }
    if (r.order.status !== "draft") { $("oid").textContent = r.order.id; $("done-t").textContent = "ההזמנה הזו כבר נשלחה אלינו."; show(6); return true; }
    var step = Math.min(5, Math.max(3, r.order.step || 3)); if (S.selectedOffer) { /* refresh prices */ var j = await CT.api("POST", "/quote", payload({ selected: S.selectedOffer })); if (j.ok) S.offers = j.offers; }
    show(step); return true;
  }
  (async function boot() {
    CT.init(); acct();
    var cfg = await CT.api("GET", "/config"); if (cfg.ok) { S.sigFee = cfg.signatureFee; S.testMode = !!cfg.testMode; }
    var h = location.hash.match(/^#r=([A-Z0-9-]+)\.([A-Za-z0-9_-]+)$/);
    if (h) { history.replaceState(null, "", location.pathname); if (await resume(h[1], h[2])) return; }
    var seed = null; try { seed = JSON.parse(sessionStorage.getItem("ct_seed") || "null"); sessionStorage.removeItem("ct_seed"); } catch (e) {}
    if (seed) { ["from", "to", "type"].forEach(function (k) { if (seed[k]) S[k] = seed[k]; }); if (seed.parcels && seed.parcels.length) S.parcels = seed.parcels; if (seed.cont) S.cont = seed.cont; }
    else {
      var last = null; try { last = JSON.parse(localStorage.getItem("ct_last") || "null"); } catch (e) {}
      if (last && last.id) { $("resume-t").textContent = "יש לכם הזמנה שלא הושלמה (" + last.id + ")."; $("resume").hidden = false;
        $("resume-go").addEventListener("click", async function () { if (!(await resume(last.id, last.token))) { $("resume").hidden = true; } else $("resume").hidden = true; });
        $("resume-no").addEventListener("click", function () { try { localStorage.removeItem("ct_last"); } catch (e) {} $("resume").hidden = true; }); }
    }
    document.querySelectorAll(".chip[data-t]").forEach(function () { }); render();
  })();
})();
"""
