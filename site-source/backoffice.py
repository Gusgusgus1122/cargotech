# -*- coding: utf-8 -*-
"""Back office (admin.html) for the owner and employees, and the customer account page (account.html)."""

ADMIN_HTML = """
<div class="ba" id="ba">
<div id="bo-gate" class="ba-gate">
  <div class="ba-gcard">
    <div class="ba-logo">CARGO<span>TECH</span></div>
    <h1>בק-אופיס</h1>
    <p id="bo-msg">טוען...</p>
    <div class="bo-actions" id="bo-acts"></div>
  </div>
</div>

<div id="bo-app" class="ba-app" hidden>
  <aside class="ba-side">
    <div class="ba-logo">CARGO<span>TECH</span><small>בק-אופיס</small></div>
    <nav class="ba-nav tabs" role="tablist" id="bo-tabs" aria-label="ניווט">
      <button type="button" role="tab" class="on" data-t="orders" data-title="הזמנות" aria-selected="true">%(i_orders)s<span>הזמנות</span></button>
      <button type="button" role="tab" data-t="staff" data-title="עובדים" data-admin aria-selected="false">%(i_staff)s<span>עובדים</span></button>
      <button type="button" role="tab" data-t="settings" data-title="הגדרות תמחור" data-admin aria-selected="false">%(i_settings)s<span>הגדרות</span></button>
    </nav>
    <div class="ba-user">
      <div class="ba-who"><span class="ba-av" id="bo-av" aria-hidden="true"></span><span id="bo-who"></span></div>
      <button type="button" class="ba-sbtn" id="bo-code">%(i_key)s<span>הקוד האישי שלי</span></button>
      <button type="button" class="ba-sbtn" id="bo-out">%(i_out)s<span>התנתקות</span></button>
    </div>
  </aside>

  <main class="ba-main">
    <header class="ba-head"><h1 id="ba-title">הזמנות</h1><span class="ba-date" id="ba-date"></span></header>

    <div id="t-orders">
      <div class="ba-kpis" id="ba-kpis">
        <div class="ba-kpi k-new"><span class="kl" id="l1">חדשות</span><b class="kv" id="k1">0</b><small class="kn" id="n1">ממתינות לטיפול</small></div>
        <div class="ba-kpi k-prog"><span class="kl" id="l2">בטיפול</span><b class="kv" id="k2">0</b><small class="kn" id="n2">הוזמנו, נאספו או בדרך</small></div>
        <div class="ba-kpi k-done"><span class="kl" id="l3">נמסרו</span><b class="kv" id="k3">0</b><small class="kn" id="n3">הושלמו</small></div>
        <div class="ba-kpi k-x"><span class="kl" id="l4">טיוטות</span><b class="kv" id="k4">0</b><small class="kn" id="n4">לקוחות שלא סיימו, אפשר לחזור אליהם</small></div>
      </div>

      <section class="ba-card">
        <div class="ba-tools">
          <div class="ba-search">%(i_search)s<input id="f-q" type="search" autocomplete="off" placeholder="חיפוש לפי מספר הזמנה, שם, טלפון או עיר" aria-label="חיפוש"></div>
          <button type="button" class="ba-ico" id="f-go" aria-label="רענון" title="רענון">%(i_refresh)s</button>
        </div>
        <input type="hidden" id="f-st" value="">
        <div class="ba-chips" id="f-chips" role="group" aria-label="סינון לפי סטטוס"></div>
        <p class="ba-meta" id="o-meta" aria-live="polite"></p>
        <div class="ba-scroll"><table class="ba-t"><thead id="o-head"></thead><tbody id="o-body"></tbody></table></div>
        <div class="ba-empty" id="o-empty" hidden><b>אין הזמנות להצגה</b><span>כשלקוח ישמור הזמנה היא תופיע כאן.</span></div>
      </section>
    </div>

    <div id="t-staff" hidden>
      <section class="ba-card">
        <div class="ba-scroll"><table class="ba-t ba-t-static"><thead><tr><th>שם</th><th>אימייל</th><th>תפקיד</th><th>סטטוס</th><th>קוד אישי</th><th>פעולות</th></tr></thead><tbody id="s-body"></tbody></table></div>
      </section>
      <section class="ba-card ba-pad">
        <h2 class="ba-h2">הוספת עובד</h2>
        <form class="ba-form" id="s-form" autocomplete="off" novalidate>
          <div class="row2"><div class="field"><label for="s-name">שם</label><input id="s-name" type="text"></div><div class="field"><label for="s-mail">אימייל</label><input id="s-mail" type="email" autocomplete="off"></div></div>
          <div class="row2"><div class="field"><label for="s-pw">סיסמה זמנית (8 תווים לפחות)</label><input id="s-pw" type="password" autocomplete="new-password"></div>
            <div class="field"><label for="s-role">תפקיד</label><select id="s-role"><option value="staff">עובד</option><option value="admin">מנהל</option></select></div></div>
          <p class="err" id="s-err" role="alert" hidden></p>
          <div><button type="submit" class="btn btn-go btn-sm">הוספת עובד</button></div>
          <p class="ba-note">מסרו לעובד את הסיסמה הזמנית. הוא יכול להחליף אותה דרך שכחתי סיסמה בהתחברות. כל עובד יוצר לעצמו קוד אישי בכפתור הקוד האישי שלי, והקוד לא נחשף למנהל.</p>
        </form>
      </section>
    </div>

    <div id="t-settings" hidden>
      <form id="g-form" class="ba-set" novalidate>
        <section class="ba-card ba-pad">
          <h2 class="ba-h2">תמחור</h2>
          <p class="ba-note ba-lead">הדוגמה: מחיר של 50 מחברת השילוח. עם תוספת 110 אחוז המחיר ללקוח הוא 105, ועם 210 אחוז הוא 155.</p>
          <div class="row2"><div class="field"><label for="g-b">תוספת רווח ללקוח עסקי (%)</label><input id="g-b" type="number" min="0" step="1"></div>
            <div class="field"><label for="g-p">תוספת רווח ללקוח פרטי (%)</label><input id="g-p" type="number" min="0" step="1"></div></div>
          <div class="row2"><div class="field"><label for="g-f">עלות חתימה בקבלה (דולר)</label><input id="g-f" type="number" min="0" step="0.01"></div>
            <div class="field"><label for="g-r">שער דולר לשקל</label><input id="g-r" type="number" min="0.1" step="0.01"></div></div>
          <label class="ba-sw"><input type="checkbox" id="g-ms"><i></i><span>תוספת הרווח חלה גם על תוספות של חברת השילוח, למשל אזור מרוחק</span></label>
          <label class="ba-sw"><input type="checkbox" id="g-mg"><i></i><span>תוספת הרווח חלה גם על עלות החתימה</span></label>
        </section>
        <section class="ba-card ba-pad">
          <h2 class="ba-h2">אבטחה ומצב מערכת</h2>
          <label class="ba-sw"><input type="checkbox" id="g-rl"><i></i><span>קוד עובד עובד רק כשהעובד מחובר (מומלץ)</span></label>
          <label class="ba-sw"><input type="checkbox" id="g-tm"><i></i><span>מצב בדיקה: מחירי דוגמה במקום מחירי אמת. לכבות כשמחברים חברת שילוח</span></label>
        </section>
        <p class="err" id="g-err" role="alert" hidden></p>
        <div class="ba-savebar"><button type="submit" class="btn btn-go">שמירת ההגדרות</button></div>
      </form>
    </div>
  </main>
</div>

<dialog id="ordd" class="dlg dlg-drawer" aria-labelledby="od-h"><div class="dlg-in" id="od-in"></div></dialog>
<dialog id="codd" class="dlg" aria-labelledby="cd-h"><div class="dlg-in">
  <button type="button" class="dlg-x" id="cd-x" aria-label="סגירה">×</button>
  <h2 id="cd-h">הקוד האישי שלי</h2>
  <p id="cd-t"></p>
  <div class="codebox" id="cd-code" hidden><b class="latin" id="cd-val"></b><button type="button" class="btn btn-sm btn-go" id="cd-copy">העתקה</button></div>
  <button type="button" class="btn btn-go" id="cd-make">יצירת קוד חדש</button>
</div></dialog>
</div>
"""
ICON = {'orders': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 7.5 12 3l9 4.5v9L12 21l-9-4.5v-9Z"/><path d="M3 7.5 12 12l9-4.5M12 12v9"/></svg>', 'staff': '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.6-3.6 3.2-5.5 6.5-5.5s5.9 1.9 6.5 5.5"/><circle cx="17.5" cy="9" r="2.5"/><path d="M17 14.6c2.4.1 4 1.6 4.5 4.4"/></svg>', 'settings': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h10M18 7h2M4 17h2M10 17h10"/><circle cx="16" cy="7" r="2.2"/><circle cx="8" cy="17" r="2.2"/></svg>', 'key': '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="8" cy="15" r="4"/><path d="m11 12 9-9M16 7l3 3M14 9l2 2"/></svg>', 'out': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 4h5v16h-5M10 8l-4 4 4 4M6 12h10"/></svg>', 'search': '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="m20 20-4-4"/></svg>', 'refresh': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 12a8 8 0 1 1-2.4-5.7M20 4v5h-5"/></svg>'}
for _k, _v in ICON.items():
    ADMIN_HTML = ADMIN_HTML.replace("%(i_" + _k + ")s", _v)

ADMIN_CSS = r""".ba { --bg: #EEF2F7; --surface: #FFFFFF; --fg: #14283A; --line: #DCE3EB; --muted: #5E7183; --ink: #0F3A5C; --sea-soft: #E4EEF8;
  --ba-nav: #0A2239; --ba-nav-2: #12304D; --ba-acc: #4FC3EC; --ba-r: 14px;
  color-scheme: light; background: var(--bg); color: var(--fg); min-height: 100vh; font-size: 16px; }
.ba *, .ba *::before, .ba *::after { box-sizing: border-box; }
.ba svg { width: 20px; height: 20px; fill: none; stroke: currentColor; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; flex: none; }
.ba button { font-family: inherit; }

/* gate */
.ba-gate { min-height: 100vh; display: grid; place-items: center; padding: 24px 16px; background: radial-gradient(1100px 520px at 85% -10%, #15507F 0%, transparent 60%), linear-gradient(165deg, #0E3558, #08192B 70%); }
.ba-gcard { width: min(440px, 100%); background: #fff; border-radius: 20px; padding: 32px 28px; display: grid; gap: 14px; text-align: center; box-shadow: 0 30px 80px rgba(3, 12, 22, .45); }
.ba-gcard h1 { margin: 0; font-size: 1.6rem; color: #0F3A5C; }
.ba-gcard p { margin: 0; color: #5E7183; line-height: 1.6; }
.ba-logo { font: 900 1.3rem/1 var(--font-display, inherit); letter-spacing: .06em; direction: ltr; color: #0F3A5C; display: flex; align-items: baseline; gap: 0; justify-content: center; }
.ba-logo span { color: #29A8D6; } .ba-logo small { font: 700 .72rem/1 inherit; letter-spacing: 0; margin-inline-start: 10px; opacity: .75; direction: rtl; }
.bo-actions { display: grid; gap: 10px; justify-items: stretch; } .bo-actions .btn { width: 100%; margin: 0; }

/* app frame */
.ba-app { display: grid; grid-template-columns: 252px minmax(0, 1fr); min-height: 100vh; }
.ba-side { background: linear-gradient(180deg, var(--ba-nav) 0%, #071A2C 100%); color: #D5E2EE; padding: 22px 14px; display: flex; flex-direction: column; gap: 22px; position: sticky; top: 0; height: 100vh; }
.ba-side .ba-logo { color: #fff; justify-content: flex-start; padding: 4px 10px; } .ba-side .ba-logo span { color: var(--ba-acc); }
.ba-nav { display: grid; gap: 4px; border: 0; margin: 0; padding: 0; overflow: visible; }
.ba-nav button { display: flex; align-items: center; gap: 12px; min-height: 46px; padding: 0 14px; border: 0; border-radius: 12px; background: none; color: #B7C9DA; font-weight: 700; font-size: 1rem; cursor: pointer; text-align: start; width: 100%; white-space: normal; }
.ba-nav button:hover { background: rgba(255, 255, 255, .06); color: #fff; }
.ba-nav button.on { background: rgba(79, 195, 236, .16); color: #fff; box-shadow: inset 3px 0 0 var(--ba-acc); border-bottom: 0; }
.ba-nav button[hidden] { display: none; }
.ba-user { margin-top: auto; display: grid; gap: 6px; padding-top: 16px; border-top: 1px solid rgba(255, 255, 255, .1); }
.ba-who { display: flex; align-items: center; gap: 10px; padding: 6px 10px 10px; font-weight: 800; color: #fff; font-size: .95rem; line-height: 1.3; }
.ba-av { width: 36px; height: 36px; border-radius: 50%; background: var(--ba-acc); color: #07324B; display: grid; place-items: center; font-weight: 900; flex: none; }
.ba-sbtn { display: flex; align-items: center; gap: 10px; min-height: 40px; padding: 0 12px; border: 0; background: none; color: #B7C9DA; border-radius: 10px; cursor: pointer; font-weight: 700; font-size: .93rem; text-align: start; }
.ba-sbtn:hover { background: rgba(255, 255, 255, .07); color: #fff; }
.ba-main { padding: 26px clamp(16px, 3vw, 36px) 48px; display: grid; grid-template-columns: minmax(0, 1fr); gap: 18px; align-content: start; min-width: 0; }
.ba-head { display: flex; align-items: baseline; justify-content: space-between; gap: 12px; flex-wrap: wrap; }
.ba-head h1 { margin: 0; font-size: 1.7rem; color: #0F3A5C; } .ba-date { color: var(--muted); font-size: .95rem; }

/* kpi */
.ba-kpis { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; margin-bottom: 18px; }
.ba-kpi { background: var(--surface); border: 1px solid var(--line); border-radius: var(--ba-r); padding: 16px 18px; display: grid; gap: 4px; position: relative; overflow: hidden; }
.ba-kpi::before { content: ""; position: absolute; inset-block: 0; inset-inline-start: 0; width: 4px; background: var(--kc, #9AB); }
.ba-kpi.k-new { --kc: #2F8FE0; } .ba-kpi.k-prog { --kc: #E6A117; } .ba-kpi.k-done { --kc: #2FA66A; } .ba-kpi.k-x { --kc: #8C6BD6; }
.ba-kpi .kl { font-weight: 800; color: var(--muted); font-size: .88rem; } .ba-kpi .kv { font-size: 2rem; line-height: 1.1; color: #0F3A5C; font-weight: 900; } .ba-kpi .kn { color: var(--muted); font-size: .8rem; line-height: 1.4; }

/* cards */
.ba-card { background: var(--surface); border: 1px solid var(--line); border-radius: var(--ba-r); overflow: hidden; margin-bottom: 18px; }
.ba-pad { padding: 20px 22px; display: grid; gap: 14px; }
.ba-h2 { margin: 0; font-size: 1.15rem; color: #0F3A5C; }
.ba-note { margin: 0; color: var(--muted); font-size: .9rem; line-height: 1.6; } .ba-lead { background: var(--sea-soft); border-radius: 10px; padding: 10px 12px; color: #0F3A5C; }
.ba-tools { display: flex; gap: 10px; padding: 14px 16px 6px; }
.ba-search { flex: 1; display: flex; align-items: center; gap: 10px; background: var(--bg); border: 1.5px solid transparent; border-radius: 12px; padding: 0 14px; min-height: 46px; color: var(--muted); }
.ba-search:focus-within { border-color: var(--ba-acc); background: #fff; }
.ba-search input { flex: 1; border: 0; background: none; font: inherit; color: var(--fg); min-height: 44px; outline: none; min-width: 0; }
.ba-ico { width: 46px; height: 46px; border-radius: 12px; border: 1.5px solid var(--line); background: #fff; color: #0F3A5C; display: grid; place-items: center; cursor: pointer; }
.ba-ico:hover { border-color: var(--ba-acc); }
.ba-chips { display: flex; gap: 8px; padding: 10px 16px; overflow-x: auto; scrollbar-width: thin; }
.ba-chips button { flex: none; min-height: 36px; padding: 0 14px; border-radius: 999px; border: 1.5px solid var(--line); background: #fff; color: #36506A; font-weight: 800; font-size: .88rem; cursor: pointer; }
.ba-chips button:hover { border-color: #9DB4C9; } .ba-chips button.on { background: #0F3A5C; border-color: #0F3A5C; color: #fff; }
.ba-meta { margin: 0; padding: 4px 18px 10px; color: var(--muted); font-size: .88rem; }
.ba-scroll { overflow-x: auto; }
.ba-t { width: 100%; border-collapse: collapse; min-width: 820px; }
.ba-t th { text-align: start; font-size: .78rem; font-weight: 800; color: var(--muted); letter-spacing: .02em; padding: 10px 16px; background: #F6F9FC; border-block: 1px solid var(--line); white-space: nowrap; }
.ba-t td { padding: 13px 16px; border-bottom: 1px solid #EBF0F5; font-size: .93rem; vertical-align: middle; }
.ba-t tbody tr { cursor: pointer; transition: background .12s; } .ba-t tbody tr:hover { background: #F3F8FD; } .ba-t tbody tr:focus-visible { outline: 2px solid var(--ba-acc); outline-offset: -2px; }
.ba-t-static tbody tr { cursor: default; } .ba-t-static tbody tr:hover { background: none; }
.ba-t small { color: var(--muted); }
.ba-oid { font-weight: 900; color: #0F3A5C; letter-spacing: .02em; }
.ba-route { display: inline-flex; align-items: center; gap: 6px; font-weight: 800; direction: ltr; }
.ba-route i { font-style: normal; color: #8AA0B4; }
.ba-price { font-weight: 800; white-space: nowrap; } .ba-pos { color: #1B8A55; } .ba-neg { color: #C0392B; }
.ba-empty { padding: 40px 20px; display: grid; gap: 4px; text-align: center; color: var(--muted); } .ba-empty b { color: #0F3A5C; font-size: 1.05rem; }
.cpn { font-weight: 800; }
.ba-tag { display: inline-flex; align-items: center; gap: 6px; padding: 3px 10px; border-radius: 8px; background: #FFF3D6; color: #7A5200; font-weight: 800; font-size: .82rem; }

/* status */
.st { display: inline-flex; align-items: center; gap: 6px; padding: 4px 12px; border-radius: 999px; font-weight: 800; font-size: .82rem; white-space: nowrap; background: #EDF1F5; color: #4C6073; border: 0; }
.st::before { content: ""; width: 7px; height: 7px; border-radius: 50%; background: currentColor; }
.st-new { background: #E1F0FF; color: #1769B8; } .st-draft { background: #EEF0F3; color: #6A7886; } .st-quote_sent { background: #EEE8FB; color: #6B48C2; }
.st-booked { background: #FFF1D6; color: #9A6200; } .st-picked_up { background: #FFE7D2; color: #A24A07; } .st-in_transit { background: #D9F3F5; color: #11727C; }
.st-delivered { background: #DDF4E7; color: #1B7A4B; } .st-cancelled { background: #FCE4E1; color: #B02F22; }

/* staff / forms */
.ba-form { display: grid; gap: 14px; max-width: 760px; } .ba-set { display: grid; gap: 18px; max-width: 820px; }
.ba .field { display: grid; gap: 6px; } .ba .field label { font-weight: 800; font-size: .88rem; color: #36506A; }
.ba input[type=text], .ba input[type=email], .ba input[type=password], .ba input[type=number], .ba input[type=date], .ba input[type=search], .ba select {
  width: 100%; min-height: 46px; border: 1.5px solid var(--line); border-radius: 10px; padding: 0 12px; background: #fff; color: var(--fg); font: inherit; }
.ba input:focus, .ba select:focus { outline: none; border-color: var(--ba-acc); box-shadow: 0 0 0 3px rgba(79, 195, 236, .22); }
.ba .row2 { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
.ba-sw { display: flex; align-items: flex-start; gap: 12px; cursor: pointer; line-height: 1.55; font-weight: 600; padding: 10px 0; border-top: 1px solid #EBF0F5; }
.ba-sw input { position: absolute; opacity: 0; width: 1px; height: 1px; }
.ba-sw i { flex: none; width: 44px; height: 26px; border-radius: 999px; background: #C3CFDB; position: relative; transition: background .15s; margin-top: 1px; }
.ba-sw i::after { content: ""; position: absolute; top: 3px; inset-inline-start: 3px; width: 20px; height: 20px; border-radius: 50%; background: #fff; box-shadow: 0 1px 3px rgba(0, 0, 0, .25); transition: inset-inline-start .15s; }
.ba-sw input:checked + i { background: #1FA971; } .ba-sw input:checked + i::after { inset-inline-start: 21px; }
.ba-sw input:focus-visible + i { outline: 3px solid rgba(79, 195, 236, .5); outline-offset: 2px; }
.ba-savebar { position: sticky; bottom: 0; background: linear-gradient(180deg, transparent, var(--bg) 40%); padding: 14px 0 6px; } .ba-savebar .btn { width: auto; min-width: 200px; margin: 0; }
.ba .err { color: #B02F22; font-weight: 700; margin: 0; }
.ba .btn-sm { min-height: 40px; padding: 0 16px; font-size: .92rem; width: auto; margin: 0; }
.ba-t .btn-sm { min-height: 34px; padding: 0 12px; font-size: .84rem; }
.ba .btn-line-dark { background: #fff; border: 1.5px solid #C5D2DE; color: #0F3A5C; }
.od-act { display: flex; flex-wrap: wrap; gap: 8px; align-items: end; } .od-act .field { flex: 1 1 140px; } .od-act .btn { margin: 0; }
td.od-act { display: table-cell; white-space: nowrap; } td.od-act .btn { margin-inline-end: 6px; }

/* order drawer */
.dlg-drawer { margin: 0; margin-inline-start: auto; inset-block: 0; inset-inline-start: auto; inset-inline-end: 0; width: min(680px, 100vw); max-width: 100vw; height: 100dvh; max-height: 100dvh; border-radius: 0; background: #F4F7FB;
  box-shadow: -24px 0 70px rgba(5, 18, 32, .35); }
.dlg-drawer[open] { animation: ba-in .22s ease-out; } @keyframes ba-in { from { transform: translateX(-40px); opacity: .4; } to { transform: none; opacity: 1; } }
@media (prefers-reduced-motion: reduce) { .dlg-drawer[open] { animation: none; } }
.dlg-drawer .dlg-in { padding: 0 0 30px; max-height: 100dvh; gap: 0; align-content: start; }
.od-top { position: sticky; top: 0; z-index: 2; background: linear-gradient(160deg, #0F3A5C, #0A2239); color: #fff; padding: 18px; padding-inline: 64px 22px; display: grid; gap: 10px; }
.od-top .dlg-x { background: rgba(255, 255, 255, .14); color: #fff; inset-block-start: 14px; }
.od-id { display: flex; flex-wrap: wrap; align-items: center; gap: 10px; } .od-id h2 { margin: 0; font-size: 1.35rem; letter-spacing: .04em; color: #fff; }
.od-sum { display: flex; flex-wrap: wrap; gap: 8px 22px; align-items: baseline; }
.od-sum .big { font-size: 1.7rem; font-weight: 900; } .od-sum span { color: #BBD0E2; font-size: .92rem; } .od-sum .rt { font-weight: 900; direction: ltr; color: #fff; font-size: 1.05rem; }
.od-body { padding: 16px 18px 0; display: grid; gap: 12px; }
.od-sec { background: #fff; border: 1px solid var(--line); border-radius: 14px; padding: 16px; display: grid; gap: 10px; }
.od-sec h3 { margin: 0; font-size: .95rem; color: #0F3A5C; padding-bottom: 8px; border-bottom: 1px solid #EBF0F5; }
.od-g { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px 18px; } .od-g div { font-size: .94rem; min-width: 0; overflow-wrap: anywhere; } .od-g span { color: var(--muted); display: block; font-size: .78rem; font-weight: 700; margin-bottom: 1px; }
.od-note { background: #F3F7FB; border-radius: 10px; padding: 10px 12px; font-size: .92rem; } .od-note small { color: var(--muted); }
.od-line { display: flex; justify-content: space-between; gap: 10px; font-size: .94rem; } .od-line small { color: var(--muted); }
.od-total { display: flex; justify-content: space-between; gap: 10px; border-top: 2px solid #0F3A5C; padding-top: 10px; font-weight: 900; font-size: 1.05rem; flex-wrap: wrap; }
.codebox { display: flex; gap: 10px; align-items: center; justify-content: space-between; background: #F4F7FB; border: 1.5px dashed #0F3A5C; border-radius: 12px; padding: 14px; } .codebox b { font-size: 1.4rem; letter-spacing: .08em; }
.codebox .btn { width: auto; margin: 0; }

@media (max-width: 960px) {
  .ba-app { grid-template-columns: minmax(0, 1fr); }
  .ba-side { position: static; height: auto; flex-direction: row; flex-wrap: wrap; align-items: center; padding: 10px 12px; gap: 8px; }
  .ba-side .ba-logo { flex: 1 1 auto; } .ba-nav { order: 3; flex: 1 0 100%; display: flex; overflow-x: auto; gap: 6px; }
  .ba-nav button { width: auto; flex: none; min-height: 42px; box-shadow: none !important; } .ba-nav button.on { background: rgba(79, 195, 236, .22); }
  .ba-user { margin: 0; padding: 0; border: 0; display: flex; align-items: center; gap: 4px; } .ba-who { padding: 0 6px 0 0; } .ba-who #bo-who { display: none; }
  .ba-sbtn span { display: none; } .ba-sbtn { width: 42px; padding: 0; justify-content: center; }
  .ba-kpis { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .ba-main { padding-top: 18px; }
}
@media (max-width: 560px) {
  .ba .row2, .od-g { grid-template-columns: minmax(0, 1fr); }
  .ba-kpi .kv { font-size: 1.6rem; } .ba-kpi .kn { display: none; }
  .od-top { padding-inline: 58px 16px; } .od-body { padding-inline: 12px; }
  .ba-head h1 { font-size: 1.4rem; }
}
"""

ACCOUNT_CSS = r"""
.bo-card { background: var(--surface); border: 1px solid var(--line); border-radius: 14px; padding: 20px; display: grid; gap: 12px; }
.bo-actions { display: flex; flex-wrap: wrap; gap: 10px; } .bo-actions .btn { width: auto; margin: 0; }
.bo-bar { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 10px; margin-bottom: 14px; font-weight: 800; }
.bo-bar-b { display: flex; gap: 8px; } .bo-bar .btn { width: auto; margin: 0; }
.tabs { display: flex; gap: 4px; border-bottom: 1px solid var(--line); margin-bottom: 16px; overflow-x: auto; }
.tabs button { min-height: 46px; padding: 0 18px; background: none; border: 0; border-bottom: 3px solid transparent; font: 800 1rem inherit; font-family: inherit; color: var(--muted); cursor: pointer; white-space: nowrap; }
.tabs button.on { color: var(--ink); border-bottom-color: var(--cyan); }
.bo-filters { display: grid; grid-template-columns: 200px minmax(0, 1fr) auto; gap: 12px; align-items: end; margin-bottom: 10px; } .bo-filters .btn { margin: 0; width: auto; }
table.bo-t { min-width: 760px; } .bo-t tbody tr { cursor: pointer; } .bo-t tbody tr:hover { background: var(--sea-soft); }
.bo-t td, .bo-t th { font-size: .93rem; padding: 10px 12px; }
.st { display: inline-block; padding: 3px 10px; border-radius: 999px; background: var(--bg); font-weight: 800; font-size: .82rem; border: 1px solid var(--line); white-space: nowrap; }
.st-new { background: #E7F4FF; border-color: #9CCBF0; } .st-draft { color: var(--muted); } .st-delivered { background: #E3F6EA; border-color: #8DCFA3; } .st-cancelled { background: #FBE9E7; border-color: #E5A39B; }
.cpn { font-weight: 800; color: var(--ink); }
.dlg-wide { width: min(860px, calc(100vw - 16px)); }
.od-h { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 8px; padding-inline-start: 46px; }
.od-sec { border: 1px solid var(--line); border-radius: 12px; padding: 14px; display: grid; gap: 8px; } .od-sec h3 { margin: 0; font-size: 1.05rem; }
.od-g { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px 16px; } .od-g div { font-size: .95rem; } .od-g span { color: var(--muted); display: block; font-size: .82rem; }
.od-act { display: flex; flex-wrap: wrap; gap: 8px; align-items: end; } .od-act .field { flex: 1 1 140px; } .od-act .btn { width: auto; margin: 0; }
.od-note { background: var(--bg); border-radius: 8px; padding: 8px 10px; font-size: .92rem; } .od-note small { color: var(--muted); }
.codebox { display: flex; gap: 10px; align-items: center; justify-content: space-between; background: var(--bg); border: 1.5px dashed var(--ink); border-radius: 12px; padding: 14px; } .codebox b { font-size: 1.5rem; letter-spacing: .08em; }
.codebox .btn { width: auto; margin: 0; }
.bo-form { max-width: 720px; }
@media (max-width: 700px) { .bo-filters { grid-template-columns: minmax(0, 1fr); } .od-g { grid-template-columns: minmax(0, 1fr); } }
"""

ADMIN_JS = r"""
(function () {
  var CT = window.CT, $ = function (id) { return document.getElementById(id); };
  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var money = function (n) { return n == null ? "-" : (n < 0 ? "−" : "") + "₪" + Math.abs(Number(n)).toLocaleString("he-IL", { minimumFractionDigits: 2, maximumFractionDigits: 2 }); };
  var when = function (t) { try { return new Date(t).toLocaleString("he-IL", { dateStyle: "short", timeStyle: "short" }); } catch (e) { return ""; } };
  var ST = { draft: "טיוטה", new: "חדשה", quote_sent: "הצעה נשלחה", booked: "הוזמן", picked_up: "נאסף", in_transit: "בדרך", delivered: "נמסר", cancelled: "בוטל" };
  var TY = { parcel: "חבילה", doc: "מסמך", pallet: "משטח", cont: "מכולה" };
  var me = null, orders = [];
  function say(id, m) { var e = $(id); e.textContent = m || ""; e.hidden = !m; }
  function gate(msg, acts) {
    $("bo-app").hidden = true; $("bo-gate").hidden = false; $("bo-msg").textContent = msg; var a = $("bo-acts"); a.innerHTML = "";
    (acts || []).forEach(function (x) { var b = document.createElement("button"); b.type = "button"; b.className = "btn " + (x.line ? "btn-line-dark" : "btn-go"); b.textContent = x.t; b.addEventListener("click", x.f); a.appendChild(b); });
  }
  async function refreshMe() {
    if (!CT.ready) return;
    if (!CT.user) return gate("כדי להיכנס לבק-אופיס יש להתחבר.", [{ t: "התחברות", f: function () { CT.openAuth("in"); } }]);
    var m = await CT.api("GET", "/admin/me");
    if (!m.ok) return gate("לא הצלחנו לבדוק את ההרשאה. נסו לרענן.", [{ t: "רענון", f: refreshMe }]);
    if (!m.staff) {
      var acts = [{ t: "התנתקות", line: true, f: function () { CT.signOut(); } }];
      if (m.canBootstrap) { acts.unshift({ t: "הגדרת הבק-אופיס והפיכתי למנהל ראשי", f: async function () { var r = await CT.api("POST", "/admin/bootstrap"); if (r.ok) refreshMe(); else gate("ההגדרה נכשלה.", acts); } }); return gate("זה החשבון של בעל העסק. אפשר להפעיל את הבק-אופיס.", acts); }
      if (!m.emailVerified) acts.unshift({ t: "שליחת קישור לאימות המייל", f: async function () { try { await CT.verifyMail(); $("bo-msg").textContent = "שלחנו קישור לאימות למייל שלך. אחרי האימות רענן את הדף."; } catch (e) { $("bo-msg").textContent = CT.errText(e); } } });
      return gate("לחשבון הזה (" + (CT.user.email || "") + ") אין הרשאת צוות. אם זה המייל של בעל העסק, יש לאמת אותו, ואם אתם עובדים, בקשו מהמנהל להוסיף אתכם.", acts);
    }
    me = m; $("bo-gate").hidden = true; $("bo-app").hidden = false;
    $("bo-who").innerHTML = esc(m.name || "") + "<br><small>" + (m.role === "admin" ? "מנהל" : "עובד") + "</small>"; $("bo-av").textContent = String(m.name || m.email || "?").trim().charAt(0).toUpperCase();
    try { $("ba-date").textContent = new Date().toLocaleDateString("he-IL", { weekday: "long", day: "numeric", month: "long" }); } catch (e) {}
    document.querySelectorAll("[data-admin]").forEach(function (b) { b.hidden = m.role !== "admin"; });
    buildChips();
    loadOrders();
  }
  CT.onAuth(function () { refreshMe(); }); CT.init();
  function buildChips() {
    var box = $("f-chips"); if (box.children.length) return;
    [["", "הכל"]].concat(Object.keys(ST).map(function (k) { return [k, ST[k]]; })).forEach(function (p) {
      var b = document.createElement("button"); b.type = "button"; b.textContent = p[1]; b.setAttribute("data-v", p[0]); b.setAttribute("aria-pressed", p[0] === "" ? "true" : "false"); if (p[0] === "") b.className = "on";
      b.addEventListener("click", function () { $("f-st").value = p[0]; box.querySelectorAll("button").forEach(function (x) { var on = x === b; x.classList.toggle("on", on); x.setAttribute("aria-pressed", on); }); loadOrders(); });
      box.appendChild(b);
    });
  }

  /* tabs */
  document.querySelectorAll("#bo-tabs button").forEach(function (b) {
    b.addEventListener("click", function () {
      var t = b.getAttribute("data-t");
      document.querySelectorAll("#bo-tabs button").forEach(function (x) { var on = x === b; x.classList.toggle("on", on); x.setAttribute("aria-selected", on); });
      ["orders", "staff", "settings"].forEach(function (k) { $("t-" + k).hidden = k !== t; });
      $("ba-title").textContent = b.getAttribute("data-title") || ""; if (t === "staff") loadStaff(); if (t === "settings") loadSettings();
    });
  });
  $("bo-out").addEventListener("click", function () { CT.signOut(); });

  /* summary tiles (from the full, unfiltered list) */
  function stats(list, admin) {
    var n = function (st) { return list.filter(function (o) { return st.indexOf(o.status) > -1; }).length; };
    $("k1").textContent = n(["new"]); $("k2").textContent = n(["quote_sent", "booked", "picked_up", "in_transit"]); $("k3").textContent = n(["delivered"]);
    $("n2").textContent = "הצעה נשלחה, הוזמנו, נאספו או בדרך";
    if (admin) {
      var live = list.filter(function (o) { return o.status !== "draft" && o.status !== "cancelled" && o.quote && o.quote.profit != null; });
      $("l4").textContent = "רווח צפוי"; $("k4").textContent = money(live.reduce(function (a, o) { return a + o.quote.profit; }, 0)); $("n4").textContent = "מהזמנות פעילות, לא כולל טיוטות וביטולים";
    } else { $("l4").textContent = "טיוטות"; $("k4").textContent = n(["draft"]); $("n4").textContent = "לקוחות שלא סיימו, אפשר לחזור אליהם"; }
  }

  /* orders */
  async function loadOrders() {
    $("o-meta").textContent = "טוען...";
    var r = await CT.api("GET", "/admin/orders?status=" + encodeURIComponent($("f-st").value) + "&q=" + encodeURIComponent($("f-q").value.trim()));
    if (!r.ok) { $("o-meta").textContent = "לא הצלחנו לטעון הזמנות."; return; }
    orders = r.orders; var admin = r.role === "admin";
    $("o-head").innerHTML = "<tr><th>הזמנה</th><th>עודכן</th><th>לקוח</th><th>מסלול</th><th>סוג</th><th>סטטוס</th><th>מחיר</th>" + (admin ? "<th>עלות</th><th>רווח</th>" : "") + "<th>קופון</th></tr>";
    $("o-body").innerHTML = ""; $("o-meta").textContent = orders.length + " הזמנות"; $("o-empty").hidden = orders.length > 0; if (!$("f-st").value && !$("f-q").value.trim()) stats(orders, admin);
    orders.forEach(function (o) {
      var tr = document.createElement("tr"), q = o.quote || {}, c = o.coupon;
      tr.tabIndex = 0;
      tr.innerHTML = '<td class="latin"><b class="ba-oid">' + esc(o.id) + "</b></td><td>" + esc(when(o.updatedAt)) + "</td><td>" + esc((o.contact && o.contact.name) || "") + '<br><small class="latin">' + esc((o.contact && o.contact.phone) || "") + "</small></td>" +
        '<td><span class="ba-route">' + esc((o.from || "").toUpperCase()) + " <i>→</i> " + esc((o.to || "").toUpperCase()) + "</span></td><td>" + esc(TY[o.type] || "") + "</td>" +
        '<td><span class="st st-' + esc(o.status) + '">' + esc(ST[o.status] || o.status) + "</span></td><td class=\"ba-price\">" + (q.total != null ? money(q.total) : "ידני") + "</td>" +
        (admin ? "<td>" + (q.cost != null ? money(q.cost) : "-") + '</td><td class="ba-price ' + (q.profit > 0 ? "ba-pos" : q.profit < 0 ? "ba-neg" : "") + '">' + (q.profit != null ? money(q.profit) : "-") + "</td>" : "") +
        '<td class="cpn">' + (c ? '<span class="ba-tag">' + (c.hidden ? "קוד עובד" : esc(c.staffName || "עובד")) + "</span>" : "") + "</td>";
      tr.addEventListener("click", function () { openOrder(o); }); tr.addEventListener("keydown", function (e) { if (e.key === "Enter") openOrder(o); });
      $("o-body").appendChild(tr);
    });
  }
  $("f-go").addEventListener("click", loadOrders);
  $("f-q").addEventListener("keydown", function (e) { if (e.key === "Enter") loadOrders(); });

  function adr(a) { a = a || {}; return esc([a.name, a.company, (a.street || "") + " " + (a.house || ""), a.city, a.zip, a.country && a.country.toUpperCase()].filter(function (x) { return x && String(x).trim(); }).join(", ")) + "<br><small class='latin'>" + esc(a.phone || "") + " " + esc(a.email || "") + "</small>"; }
  function openOrder(o) {
    var admin = me.role === "admin", q = o.quote || {}, d = $("ordd"), box = $("od-in");
    var wa = (o.contact && o.contact.phone) ? "https://wa.me/" + String(o.contact.phone).replace(/\D/g, "").replace(/^0/, "972") + "?text=" + encodeURIComponent("שלום, לגבי הזמנה " + o.id + " ב-CargoTech") : "";
    box.innerHTML = '<div class="od-top"><button type="button" class="dlg-x" id="od-x" aria-label="סגירה">×</button>' +
      '<div class="od-id"><h2 id="od-h" class="latin">' + esc(o.id) + '</h2><span class="st st-' + esc(o.status) + '">' + esc(ST[o.status] || o.status) + "</span></div>" +
      '<div class="od-sum"><span class="rt">' + esc((o.from || "").toUpperCase()) + " → " + esc((o.to || "").toUpperCase()) + '</span><span>' + esc(TY[o.type] || "") + '</span><b class="big">' + (q.total != null ? money(q.total) : "מחיר ידני") + "</b>" + (o.coupon && !o.coupon.hidden ? '<span>קוד עובד: ' + esc(o.coupon.staffName) + "</span>" : "") + "</div></div>" +
      '<div class="od-body">' +
      '<div class="od-sec"><h3>לקוח</h3><div class="od-g"><div><span>שם</span>' + esc((o.contact && o.contact.name) || "") + '</div><div><span>סוג</span>' + (o.customerType === "business" ? "עסקי" : "פרטי") + (o.uid ? " · רשום" : " · אורח") + '</div><div><span>טלפון</span><bdi>' + esc((o.contact && o.contact.phone) || "") + '</bdi></div><div><span>אימייל</span><bdi>' + esc((o.contact && o.contact.email) || "") + "</bdi></div></div>" +
      (wa ? '<a class="btn btn-line-dark btn-sm" style="width:auto;margin:0" href="' + wa + '" target="_blank" rel="noopener">וואטסאפ ללקוח</a>' : "") + "</div>" +
      '<div class="od-sec"><h3>משלוח</h3><div class="od-g"><div><span>מסלול</span>' + esc((o.from || "").toUpperCase()) + " ← " + esc((o.to || "").toUpperCase()) + "</div><div><span>סוג</span>" + esc(TY[o.type] || "") + "</div>" +
      "<div><span>חבילות</span>" + (o.type === "cont" ? esc((o.cont && o.cont.size) + " × " + (o.cont && o.cont.qty)) : (o.parcels || []).map(function (p) { return esc(p.qty + " × " + p.kg + " ק״ג (" + p.l + "×" + p.w + "×" + p.h + ")"); }).join("<br>")) + "</div>" +
      "<div><span>חתימה</span>" + esc({ none: "ללא", standard: "חתימה בקבלה", adult: "חתימת מבוגר" }[o.signature] || "") + "</div></div></div>" +
      '<div class="od-sec"><h3>כתובות</h3><div class="od-g"><div><span>שולח</span>' + adr(o.sender) + "</div><div><span>נמען" + (o.recipient && o.recipient.residential ? " (מגורים)" : "") + "</span>" + adr(o.recipient) + "</div></div></div>" +
      '<div class="od-sec"><h3>סחורה ותנאים</h3>' + (o.items || []).map(function (i) { return "<div>" + esc(i.desc) + " · " + esc(i.qty) + " × " + esc(i.value) + " " + esc(i.currency) + (i.hs ? " · HS " + esc(i.hs) : "") + (i.origin ? " · " + esc(i.origin.toUpperCase()) : "") + "</div>"; }).join("") +
      '<div class="od-g"><div><span>ביטוח</span>' + (o.insurance && o.insurance.requested ? "התבקש, שווי " + esc(o.insurance.amount) : "לא") + "</div><div><span>תנאי מכס ומיסים</span>" + esc((o.terms && o.terms.incoterm) || "") + "</div><div><span>סיבת המשלוח</span>" + esc((o.terms && o.terms.reason) || "") + "</div><div><span>תיאור</span>" + esc((o.terms && o.terms.shortDesc) || "") + "</div></div></div>" +
      '<div class="od-sec"><h3>מחיר</h3>' + (q.carrier ? "<div>" + esc(q.carrier + " · " + q.service + " · " + q.days) + "</div>" : "") +
      (q.lines || []).map(function (l) { return "<div class='od-line'><span>" + esc(l.label) + "</span><span>" + money(l.price) + (admin && l.cost != null ? " <small>(עלות " + money(l.cost) + ")</small>" : "") + "</span></div>"; }).join("") +
      '<div class="od-total"><span>סה״כ ללקוח: ' + (q.total != null ? money(q.total) : "טרם נקבע") + "</span>" + (admin && q.cost != null ? "<span>עלות " + money(q.cost) + " · רווח " + money(q.profit) + (q.markupPct != null ? " · תוספת " + q.markupPct + "%" : "") + "</span>" : "") + "</div>" +
      (o.coupon && !o.coupon.hidden ? '<div class="od-note"><b>קוד עובד:</b> ' + esc(o.coupon.staffName) + " · מחיר מקורי " + money(o.coupon.originalPrice) + " ← מחיר חדש " + money(o.coupon.newPrice) + "<br><small>סיבה: " + esc(o.coupon.reason) + " · " + esc(when(o.coupon.at)) + (o.coupon.superseded ? " · המחיר חושב מחדש בעקבות שינוי בהזמנה, והמחיר הידני כבר לא בתוקף" : "") + "</small></div>" : "") +
      '<div class="od-act"><div class="field"><label for="m-p">מחיר ללקוח (ידני)</label><input id="m-p" type="number" min="0" step="0.01" value="' + (q.total != null ? q.total : "") + '"></div>' +
      (admin ? '<div class="field"><label for="m-c">עלות אצלנו</label><input id="m-c" type="number" min="0" step="0.01" value="' + (q.cost != null ? q.cost : "") + '"></div>' : "") +
      '<div class="field"><label for="m-s">חברה ושירות</label><input id="m-s" type="text" value="' + esc(q.carrier ? q.carrier + (q.service ? " · " + q.service : "") : "") + '"></div><div class="field"><label for="m-d">ימים</label><input id="m-d" type="text" value="' + esc(q.days || "") + '"></div><button type="button" class="btn btn-go btn-sm" id="m-save">שמירת מחיר</button></div></div>' +
      '<div class="od-sec"><h3>איסוף ומעקב</h3><div class="od-act"><div class="field"><label for="k-d">תאריך איסוף</label><input id="k-d" type="date" value="' + esc((o.pickup && o.pickup.date) || "") + '"></div><div class="field"><label for="k-t">שעות</label><input id="k-t" type="text" value="' + esc((o.pickup && o.pickup.time) || "") + '"></div></div>' +
      '<div class="od-act"><div class="field"><label for="k-c">אישור איסוף</label><input id="k-c" type="text" value="' + esc((o.pickup && o.pickup.confirmation) || "") + '"></div><div class="field"><label for="k-n">מספר קריאה לנהג</label><input id="k-n" type="text" value="' + esc((o.pickup && o.pickup.callNumber) || "") + '"></div><div class="field"><label for="k-k">מספר מעקב</label><input id="k-k" type="text" value="' + esc((o.pickup && o.pickup.trackingNumber) || "") + '"></div><button type="button" class="btn btn-go btn-sm" id="k-save">שמירה</button></div></div>' +
      '<div class="od-sec"><h3>סטטוס והערות</h3><div class="od-act"><div class="field"><label for="u-st">סטטוס</label><select id="u-st">' + Object.keys(ST).map(function (k) { return '<option value="' + k + '"' + (k === o.status ? " selected" : "") + ">" + ST[k] + "</option>"; }).join("") + '</select></div><button type="button" class="btn btn-go btn-sm" id="u-save">עדכון סטטוס</button></div>' +
      (o.notes || []).map(function (n) { return '<div class="od-note">' + esc(n.text) + "<br><small>" + esc(n.by) + " · " + esc(when(n.at)) + "</small></div>"; }).join("") +
      '<div class="od-act"><div class="field"><label for="n-t">הערה פנימית</label><input id="n-t" type="text" maxlength="500"></div><button type="button" class="btn btn-line-dark btn-sm" id="n-add">הוספה</button></div></div>' +
      '<p class="err" id="od-err" role="alert" hidden></p></div>';
    d.showModal();
    $("od-x").addEventListener("click", function () { d.close(); });
    var send = async function (body) { var r = await CT.api("POST", "/admin/order/update", Object.assign({ id: o.id }, body)); if (!r.ok) return say("od-err", r.error && r.error.length > 3 && r.error !== "server" ? r.error : "השמירה נכשלה."); say("od-err", ""); await loadOrders(); var n = orders.filter(function (x) { return x.id === o.id; })[0]; if (n) openOrder(n); };
    $("m-save").addEventListener("click", function () { var b = { manualPrice: $("m-p").value, carrier: ($("m-s").value.split(" · ")[0] || ""), service: ($("m-s").value.split(" · ")[1] || ""), days: $("m-d").value }; if (admin) b.manualCost = $("m-c").value; if (b.manualPrice === "") return say("od-err", "הקלידו מחיר."); send(b); });
    $("k-save").addEventListener("click", function () { send({ pickup: { date: $("k-d").value, time: $("k-t").value, confirmation: $("k-c").value, callNumber: $("k-n").value, trackingNumber: $("k-k").value } }); });
    $("u-save").addEventListener("click", function () { send({ status: $("u-st").value }); });
    $("n-add").addEventListener("click", function () { if ($("n-t").value.trim()) send({ note: $("n-t").value }); });
  }

  /* staff */
  async function loadStaff() {
    var r = await CT.api("GET", "/admin/staff"); if (!r.ok) return;
    var b = $("s-body"); b.innerHTML = "";
    r.staff.forEach(function (s) {
      var tr = document.createElement("tr");
      tr.innerHTML = "<td>" + esc(s.name) + '</td><td class="latin">' + esc(s.email) + "</td><td>" + (s.role === "admin" ? "מנהל" : "עובד") + "</td><td>" + '<span class="st ' + (s.active ? "st-delivered" : "st-cancelled") + '">' + (s.active ? "פעיל" : "מושבת") + "</span></td><td>" + (s.hasCode ? "קיים" : "אין") + '</td><td class="od-act"></td>';
      var td = tr.lastChild, add = function (t, f) { var x = document.createElement("button"); x.type = "button"; x.className = "btn btn-line-dark btn-sm"; x.style.cssText = "width:auto;margin:0"; x.textContent = t; x.addEventListener("click", async function (e) { e.stopPropagation(); await f(); loadStaff(); }); td.appendChild(x); };
      if (s.uid !== me.uid) add(s.active ? "השבתה" : "הפעלה", function () { return CT.api("POST", "/admin/staff/update", { uid: s.uid, active: !s.active }); });
      if (s.hasCode) add("ביטול קוד", function () { return CT.api("POST", "/admin/code/revoke", { uid: s.uid }); });
      if (s.uid !== me.uid) add(s.role === "admin" ? "הפיכה לעובד" : "הפיכה למנהל", function () { return CT.api("POST", "/admin/staff/update", { uid: s.uid, role: s.role === "admin" ? "staff" : "admin" }); });
      b.appendChild(tr);
    });
  }
  $("s-form").addEventListener("submit", async function (e) {
    e.preventDefault(); say("s-err", "");
    var r = await CT.api("POST", "/admin/staff/create", { name: $("s-name").value, email: $("s-mail").value, password: $("s-pw").value, role: $("s-role").value });
    $("s-pw").value = ""; if (!r.ok) return say("s-err", r.error && r.error.length > 3 && r.error !== "server" ? r.error : "ההוספה נכשלה.");
    $("s-name").value = ""; $("s-mail").value = ""; loadStaff();
  });

  /* settings */
  async function loadSettings() {
    var r = await CT.api("GET", "/admin/settings"); if (!r.ok) return; var s = r.settings;
    $("g-b").value = s.markupBusinessPct; $("g-p").value = s.markupPrivatePct; $("g-f").value = s.signatureFeeUsd; $("g-r").value = s.usdIls;
    $("g-ms").checked = !!s.markupOnSurcharges; $("g-mg").checked = !!s.markupOnSignature; $("g-rl").checked = !!s.requireStaffLogin; $("g-tm").checked = !!s.testMode;
  }
  $("g-form").addEventListener("submit", async function (e) {
    e.preventDefault(); say("g-err", "");
    var r = await CT.api("POST", "/admin/settings", { markupBusinessPct: +$("g-b").value, markupPrivatePct: +$("g-p").value, signatureFeeUsd: +$("g-f").value, usdIls: +$("g-r").value,
      markupOnSurcharges: $("g-ms").checked, markupOnSignature: $("g-mg").checked, requireStaffLogin: $("g-rl").checked, testMode: $("g-tm").checked });
    say("g-err", r.ok ? "נשמר." : (r.error && r.error.length > 3 && r.error !== "server" ? r.error : "השמירה נכשלה."));
  });

  /* personal code: shown once, never stored */
  $("bo-code").addEventListener("click", function () {
    $("cd-code").hidden = true; $("cd-val").textContent = "";
    $("cd-t").textContent = "הקוד האישי מאפשר לך לשנות מחיר ידנית בשורת הקופון של הזמנה, רק כשאתה מחובר לבק-אופיס. הקוד מוצג פעם אחת ולא נשמר במערכת, ולכן העתק אותו למקום בטוח. יצירת קוד חדשה מבטלת את הקודם.";
    $("cd-make").textContent = me.hasCode ? "יצירת קוד חדש במקום הקודם" : "יצירת קוד אישי"; $("codd").showModal();
  });
  $("cd-x").addEventListener("click", function () { $("cd-val").textContent = ""; $("codd").close(); });
  $("cd-make").addEventListener("click", async function () {
    var r = await CT.api("POST", "/admin/code/generate"); if (!r.ok) { $("cd-t").textContent = "היצירה נכשלה. נסו שוב."; return; }
    $("cd-val").textContent = r.code; $("cd-code").hidden = false; me.hasCode = true; $("cd-make").textContent = "יצירת קוד חדש במקום הקודם";
  });
  $("cd-copy").addEventListener("click", function () { try { navigator.clipboard.writeText($("cd-val").textContent); this.textContent = "הועתק"; } catch (e) {} });
  $("codd").addEventListener("close", function () { $("cd-val").textContent = ""; });
})();
"""

ACCOUNT_HTML = """
<section class="phero"><div class="wrap">%(crumbs)s<h1>האזור שלי</h1><p class="lead">ההזמנות שלכם והכתובות השמורות, במקום אחד.</p></div></section>
<section class="sec"><div class="wrap">
  <div id="ac-gate" class="bo-card"><p>כדי לראות את ההזמנות שלכם יש להתחבר.</p><div class="bo-actions"><button type="button" class="btn btn-go" id="ac-in">התחברות או הרשמה</button></div></div>
  <div id="ac-app" hidden>
    <div class="bo-bar"><span id="ac-who"></span><span class="bo-bar-b"><a class="btn btn-go btn-sm" href="order.html">הזמנה חדשה</a><button type="button" class="btn btn-line-dark btn-sm" id="ac-out">התנתקות</button></span></div>
    <h2>ההזמנות שלי</h2>
    <div class="tscroll"><table class="cmp bo-t"><thead><tr><th>הזמנה</th><th>תאריך</th><th>מסלול</th><th>סטטוס</th><th>מחיר</th><th></th></tr></thead><tbody id="ac-orders"></tbody></table></div>
    <p class="meta" id="ac-empty" hidden>עדיין אין הזמנות.</p>
    <h2 style="margin-top:32px">כתובות שמורות</h2>
    <div id="ac-addr" class="od-sec"></div>
  </div>
</div></section>
"""

ACCOUNT_JS = r"""
(function () {
  var CT = window.CT, $ = function (id) { return document.getElementById(id); };
  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var money = function (n) { return n == null ? "-" : (n < 0 ? "−" : "") + "₪" + Math.abs(Number(n)).toLocaleString("he-IL", { minimumFractionDigits: 2, maximumFractionDigits: 2 }); };
  var ST = { draft: "טיוטה", new: "התקבלה", quote_sent: "הצעה נשלחה", booked: "הוזמן", picked_up: "נאסף", in_transit: "בדרך", delivered: "נמסר", cancelled: "בוטל" };
  $("ac-in").addEventListener("click", function () { CT.openAuth("in"); });
  $("ac-out").addEventListener("click", function () { CT.signOut(); });
  async function load() {
    var r = await CT.api("GET", "/me"); if (!r.ok) return;
    $("ac-who").textContent = ((r.profile && (r.profile.firstName || "")) + " " + ((r.profile && r.profile.lastName) || "")).trim() || r.email;
    var b = $("ac-orders"); b.innerHTML = ""; $("ac-empty").hidden = r.orders.length > 0;
    r.orders.forEach(function (o) {
      var tr = document.createElement("tr"), q = o.quote || {};
      tr.innerHTML = '<td class="latin"><b>' + esc(o.id) + "</b></td><td>" + esc(new Date(o.createdAt).toLocaleDateString("he-IL")) + "</td><td>" + esc((o.from || "").toUpperCase()) + " ← " + esc((o.to || "").toUpperCase()) + "</td><td>" + esc(ST[o.status] || o.status) + "</td><td>" + (q.total != null ? money(q.total) : "-") + "</td><td></td>";
      if (o.status === "draft") { var a = document.createElement("a"); a.className = "more"; a.textContent = "המשך הזמנה"; a.href = "#"; a.addEventListener("click", function (e) { e.preventDefault(); alert_free(); }); tr.lastChild.appendChild(a); }
      b.appendChild(tr);
    });
    var ad = $("ac-addr"); ad.innerHTML = r.addresses.length ? "" : "<span>עדיין לא נשמרו כתובות. אפשר לשמור כתובת בזמן הזמנה.</span>";
    r.addresses.forEach(function (a) {
      var d = document.createElement("div"); d.className = "od-act";
      d.innerHTML = "<div style='flex:1 1 220px'><b>" + esc(a.nickname) + "</b><br><small>" + esc([a.street, a.house, a.city, a.zip, (a.country || "").toUpperCase()].join(" ")) + "</small></div>";
      var x = document.createElement("button"); x.type = "button"; x.className = "btn btn-line-dark btn-sm"; x.style.cssText = "width:auto;margin:0"; x.textContent = "מחיקה";
      x.addEventListener("click", async function () { await CT.api("POST", "/addresses/delete", { id: a.id }); load(); }); d.appendChild(x); ad.appendChild(d);
    });
  }
  function alert_free() { location.href = "order.html"; }
  CT.onAuth(function (u) { $("ac-gate").hidden = !!u; $("ac-app").hidden = !u; if (u) load(); }); CT.init();
})();
"""
