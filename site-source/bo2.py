# ShippingToGo-style back office: English, left-to-right, plain dense Material-like look.
BX_HTML = """
<div class="bx" dir="ltr" lang="en" id="bx">
<div id="bx-gate" class="bx-gate"><div class="bx-gcard"><div class="bx-logo">CARGO<span>TECH</span></div><h1>Back office</h1><p id="bx-msg">Loading...</p><div id="bx-acts" class="bx-acts"></div></div></div>

<div id="bx-app" class="bx-app" hidden>
  <aside class="bx-side" id="bx-side">
    <div class="bx-logo">CARGO<span>TECH</span></div>
    <form class="bx-qs" id="qs-form" autocomplete="off">
      <select id="qs-by" aria-label="Search by"><option value="userId">UserId</option><option value="email">Email</option><option value="pickupId">PickupId</option><option value="shippingAuthorization">ShippingAuthorization</option></select>
      <div class="bx-qs-r"><input id="qs-q" type="text" aria-label="Search value" placeholder="Search"><button type="submit">Go</button></div>
      <small id="qs-msg" hidden></small>
    </form>
    <nav class="bx-nav" id="bx-nav">
      <a href="#orders" data-v="orders">Orders<b class="bdg" id="b-orders" hidden></b></a>
      <a href="#users" data-v="users">Users</a>
      <a href="#tasks" data-v="tasks">Agent Tasks<b class="bdg" id="b-tasks" hidden></b></a>
      <a href="#payments" data-v="payments">Payments</a>
      <a href="#agents" data-v="agents">Agents</a>
      <a href="#receipts" data-v="receipts">Receipts</a>
      <a href="#messages" data-v="messages">Messages<b class="bdg" id="b-messages" hidden></b></a>
      <a href="#ledger" data-v="ledger">Accounting Transactions</a>
      <a href="#quotes" data-v="quotes">Price Quotation</a>
      <a href="#outbox" data-v="outbox">Outbox (e-mails)</a>
      <a href="#finance" data-v="finance" data-admin>Finance</a>
      <details class="bx-nav-group" id="bx-nav-settings" data-admin>
        <summary>Settings</summary>
        <div class="bx-nav-sub">
          <a href="#staff" data-v="staff">Staff</a>
          <a href="#coupons" data-v="coupons">Coupons</a>
          <a href="#pricelists" data-v="pricelists">Price List</a>
          <a href="#banners" data-v="banners">Banners</a>
          <a href="#settings" data-v="settings">General</a>
        </div>
      </details>
    </nav>
    <div class="bx-user"><div class="bx-who" id="bx-who"></div><button type="button" id="bx-code">My personal code</button><button type="button" id="bx-out-all" title="Signs out of this and every other device; sign back in anywhere right after">Sign out everywhere</button><button type="button" id="bx-out">Sign out</button></div>
  </aside>
  <main class="bx-main"><h1 id="bx-title"></h1><div id="bx-view"></div></main>
</div>

<dialog id="shipd" class="bx-dlg bx-big" aria-label="Shipment details"><div class="bx-dlg-in" id="ship-in"></div></dialog>
<dialog id="taskd" class="bx-dlg bx-big" aria-label="Task details"><div class="bx-dlg-in" id="task-in"></div></dialog>
<dialog id="pld" class="bx-dlg bx-big" aria-label="Price list"><div class="bx-dlg-in" id="pl-in"></div></dialog>
<dialog id="printd" class="bx-dlg" aria-label="Print"><div class="bx-dlg-in"><div class="bx-bar"><button type="button" class="pri" id="pr-go">Print / Save as PDF</button><button type="button" id="pr-x">Close</button></div><div id="pr-doc" class="pr-doc"></div></div></dialog>
<dialog id="codd" class="bx-dlg" aria-label="My personal code"><div class="bx-dlg-in">
  <h2>My personal code</h2><p id="cd-t"></p>
  <div class="codebox" id="cd-code" hidden><b id="cd-val"></b><button type="button" id="cd-copy">Copy</button></div>
  <div class="bx-bar"><button type="button" class="pri" id="cd-make">Create code</button><button type="button" id="cd-x">Close</button></div>
</div></dialog>
</div>
"""

BX_CSS = r"""
.bx{--bg:#f3f6f9;--card:#fff;--line:#dde2e6;--fg:#172532;--mut:#5a6f7e;--pri:#185b92;--prih:#104772;--accent:#2aa0c7;--ok:#267a3e;--warn:#c9701a;--bad:#c62828;
  direction:ltr;text-align:left;font:14px/1.5 -apple-system,ui-sans-serif,"SF Pro Display","Segoe UI",Roboto,Arial,sans-serif;color:var(--fg);background:var(--bg);min-height:100vh}
.bx *{box-sizing:border-box}.bx h1,.bx h2,.bx h3{font-family:inherit;margin:0;color:var(--fg)}.bx h1,.bx h2{font-weight:700;letter-spacing:-.01em}
.bx a{color:var(--pri);text-decoration:none}.bx a:hover{text-decoration:underline}
.bx button{font:inherit;cursor:pointer;border:1px solid var(--line);background:#fff;color:var(--fg);border-radius:6px;padding:6px 12px;min-height:34px;transition:background .15s ease,transform .1s ease,border-color .15s ease}
.bx button:hover{background:#f0f3f7}.bx button:active{transform:translateY(1px)}.bx button:focus-visible{outline:2px solid var(--accent);outline-offset:1px}
.bx button.pri{background:var(--pri);border-color:var(--pri);color:#fff}.bx button.pri:hover{background:var(--prih)}
.bx button.dng{color:var(--bad);border-color:#e7b4b4}.bx button:disabled{opacity:.5;cursor:default;transform:none}
.bx input,.bx select,.bx textarea{font:inherit;color:var(--fg);background:#fff;border:1px solid #c9ced4;border-radius:4px;padding:6px 8px;min-height:34px;width:100%;max-width:100%}
.bx textarea{min-height:70px;resize:vertical}.bx input:focus,.bx select:focus,.bx textarea:focus{outline:2px solid var(--accent);border-color:var(--pri)}
.bx label{display:block;font-size:12px;color:var(--mut);margin:0 0 3px}
.bx-gate{min-height:100vh;display:grid;place-items:center;padding:20px}.bx-gcard{background:#fff;border:1px solid var(--line);border-radius:6px;padding:32px;max-width:430px;width:100%;text-align:center}
.bx-gcard h1{font-size:20px;margin:10px 0}.bx-gcard p{color:var(--mut);margin:0 0 18px}.bx-acts{display:grid;gap:10px}.bx-gcard button{width:100%}
.bx-logo{font-weight:800;letter-spacing:.06em;font-size:18px;color:#0b2540}.bx-logo span{color:var(--pri)}
.bx-app{display:grid;grid-template-columns:230px minmax(0,1fr);min-height:100vh}
.bx-side{background:#fff;border-right:1px solid var(--line);padding:16px 12px;display:flex;flex-direction:column;gap:14px;position:sticky;top:0;height:100vh;overflow:auto}
.bx-qs{display:grid;gap:6px;background:#f7f8fa;border:1px solid var(--line);border-radius:6px;padding:8px}.bx-qs-r{display:flex;gap:6px}.bx-qs-r button{padding:6px 10px}.bx-qs small{color:var(--bad)}
.bx-nav{display:flex;flex-direction:column;gap:1px}.bx-nav a{display:flex;justify-content:space-between;align-items:center;padding:8px 10px;border-radius:4px;color:var(--fg)}
.bx-nav a:hover{background:#f0f3f7;text-decoration:none}.bx-nav a.on{background:#e3f0fc;color:var(--prih);font-weight:600}
.bx-nav-group{border-radius:4px}.bx-nav-group summary{cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center;padding:8px 10px;border-radius:4px;color:var(--fg)}
.bx-nav-group summary::-webkit-details-marker{display:none}.bx-nav-group summary::after{content:"›";transform:rotate(90deg);transition:transform .15s;color:var(--mut)}
.bx-nav-group[open] summary::after{transform:rotate(270deg)}.bx-nav-group summary:hover{background:#f0f3f7}
.bx-nav-group.has-on>summary{color:var(--prih);font-weight:600}
.bx-nav-sub{display:flex;flex-direction:column;gap:1px;padding-inline-start:14px;margin-top:1px}
.bx-nav-sub a{display:flex;padding:7px 10px;border-radius:4px;color:var(--fg);font-size:.95em}
.bx-nav-sub a:hover{background:#f0f3f7;text-decoration:none}.bx-nav-sub a.on{background:#e3f0fc;color:var(--prih);font-weight:600}
.bdg{background:var(--bad);color:#fff;border-radius:9px;font-size:11px;padding:1px 7px;font-weight:600}
.bx-user{margin-top:auto;display:grid;gap:6px;border-top:1px solid var(--line);padding-top:12px}.bx-who{font-size:13px}.bx-who small{color:var(--mut)}
.bx-main{padding:20px 24px 60px;min-width:0}.bx-main>h1{font-size:20px;margin-bottom:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;margin-bottom:14px;box-shadow:0 1px 2px rgba(16,71,114,.04)}
.card h2{font-size:15px;margin-bottom:10px}.card h3{font-size:13px;margin:0 0 8px;color:var(--mut);text-transform:uppercase;letter-spacing:.04em}
.flt{display:flex;flex-wrap:wrap;gap:10px;align-items:flex-end}.flt>div{min-width:130px;flex:0 1 180px}.flt .grow{flex:1 1 240px}.flt .btns{display:flex;gap:8px;flex:0 0 auto;min-width:0}
.tw{overflow:auto;border:1px solid var(--line);border-radius:6px;background:#fff}
table.t{border-collapse:collapse;width:100%;font-size:13px}table.t th{position:sticky;top:0;background:#f7f8fa;text-align:left;font-weight:600;color:#44505c;padding:8px 10px;border-bottom:1px solid var(--line);white-space:nowrap}
table.t td{padding:7px 10px;border-bottom:1px solid #eef0f2;vertical-align:top}table.t tbody tr.ck{cursor:pointer}table.t tbody tr.ck:hover{background:#f3f8fd}
table.t tbody tr.guest-row{background:#e3f2fd}table.t tbody tr.guest-row:hover{background:#cfe8fc}
table.t td.r,table.t th.r{text-align:right;font-variant-numeric:tabular-nums}small,.mut{color:var(--mut)}td small{display:block}
.meta{display:flex;justify-content:space-between;gap:10px;align-items:center;margin:10px 0;color:var(--mut);flex-wrap:wrap}.pg{display:flex;gap:6px;align-items:center}
.bx .bchip{line-height:1.4;min-height:0;height:auto;margin:0;vertical-align:middle;display:inline-block;padding:1px 8px;border-radius:10px;font-size:12px;white-space:nowrap;background:#eceff1;color:#455a64}
.bx .c-new,.bx .c-open,.bx .c-unpaid,.bx .c-draft{background:#fff3e0;color:#e65100}.bx .c-quote_sent,.bx .c-booked,.bx .c-partial,.bx .c-read{background:#e3f2fd;color:#0d47a1}
.bx .c-picked_up,.bx .c-in_transit{background:#ede7f6;color:#4527a0}.bx .c-delivered,.bx .c-paid,.bx .c-closed,.bx .c-done{background:#e8f5e9;color:#1b5e20}.bx .c-cancelled{background:#ffebee;color:#b71c1c}
.pos{color:var(--ok)}.neg{color:var(--bad)}.empty{padding:26px;text-align:center;color:var(--mut)}
.two{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.three{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.kv{display:grid;grid-template-columns:130px minmax(0,1fr);gap:4px 10px;font-size:13px}.kv dt{color:var(--mut)}.kv dd{margin:0;overflow-wrap:anywhere}
.tabs{display:flex;gap:2px;border-bottom:1px solid var(--line);margin-bottom:12px;flex-wrap:wrap}.tabs button{border:0;border-bottom:2px solid transparent;border-radius:0;background:none;padding:8px 12px}.tabs button.on{border-bottom-color:var(--pri);color:var(--prih);font-weight:600}
.msg{margin:8px 0;padding:8px 10px;border-radius:4px;background:#e8f5e9;color:#1b5e20}.msg.e{background:#ffebee;color:#b71c1c}
.frm{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;align-items:end}.frm .w2{grid-column:span 2}.frm .wf{grid-column:1/-1}
.bx-dlg{border:0;padding:0;border-radius:8px;max-width:min(560px,96vw);width:100%;color:var(--fg);box-shadow:0 12px 40px rgba(0,0,0,.3)}.bx-dlg::backdrop{background:rgba(15,25,35,.5)}
.bx-big{max-width:min(1100px,98vw);height:min(94vh,980px)}.bx-dlg-in{padding:18px;background:#f3f4f6;height:100%;overflow:auto;direction:ltr;text-align:left;font:14px/1.45 -apple-system,"Segoe UI",Roboto,Arial,sans-serif}
.bx-dlg *{box-sizing:border-box}.bx-dlg button{font:inherit;cursor:pointer;border:1px solid var(--line);background:#fff;border-radius:6px;padding:6px 12px;min-height:34px;color:var(--fg);transition:background .15s ease,transform .1s ease}
.bx-dlg button:hover{background:#f0f3f7}.bx-dlg button:active{transform:translateY(1px)}
.bx-dlg button.pri{background:var(--pri);border-color:var(--pri);color:#fff}.bx-dlg input,.bx-dlg select,.bx-dlg textarea{font:inherit;border:1px solid #c9ced4;border-radius:4px;padding:6px 8px;min-height:34px;width:100%}
.bx-dlg label{display:block;font-size:12px;color:var(--mut);margin:0 0 3px}.bx-dlg h2{font-size:16px;margin:0 0 10px;font-weight:700}.bx-dlg h3{font-size:13px;margin:0 0 8px;color:var(--mut);text-transform:uppercase;letter-spacing:.04em}
.bx-bar{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0}.sh-head{display:flex;justify-content:space-between;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:10px}.sh-head h2{margin:0;font-size:18px;font-weight:700;letter-spacing:-.01em}
.acts{display:flex;flex-wrap:wrap;gap:6px}.acts button{padding:5px 10px;min-height:30px;font-size:13px}.acts button.on{background:#e3f0fc;border-color:var(--accent);color:var(--prih)}
.panel{border:1px solid var(--accent);background:#f5faff;border-radius:8px;padding:12px;margin:10px 0}.panel h3{color:var(--prih)}
.li{display:flex;justify-content:space-between;gap:10px;padding:3px 0;border-bottom:1px dashed #e5e8eb}.li.tot{font-weight:700;border-bottom:0;border-top:1px solid #cfd4d9;margin-top:4px;padding-top:6px}
.ent{border-bottom:1px solid #eef0f2;padding:6px 0;font-size:13px}.ent small{display:inline;margin-left:6px}
.codebox{display:flex;gap:10px;align-items:center;background:#f7f8fa;border:1px dashed #9aa5b1;border-radius:6px;padding:10px;margin:10px 0}.codebox b{font:700 18px/1 ui-monospace,Menlo,monospace;letter-spacing:.06em;flex:1}
.pr-doc{background:#fff;border:1px solid var(--line,#dfe2e6);padding:26px;margin-top:10px}.pr-doc h2{font-size:20px}.pr-doc table{width:100%;border-collapse:collapse;margin:14px 0}.pr-doc td,.pr-doc th{padding:6px;border-bottom:1px solid #e5e8eb;text-align:left}.pr-doc td.r,.pr-doc th.r{text-align:right}
.sw{display:flex;gap:8px;align-items:flex-start;margin:8px 0}.sw input{width:auto;min-height:0;margin-top:3px}.sw span{color:var(--fg)}
@media(max-width:900px){.bx-app{grid-template-columns:1fr}.bx-side{position:static;height:auto;border-right:0;border-bottom:1px solid var(--line)}.bx-nav{flex-direction:row;flex-wrap:wrap}.bx-user{margin-top:0}
 .bx-main{padding:14px 12px 50px}.two,.three{grid-template-columns:1fr}.bx-big{height:100vh;max-width:100vw;border-radius:0}.kv{grid-template-columns:110px minmax(0,1fr)}.frm .w2{grid-column:auto}}
@media print{body *{visibility:hidden}#printd,#printd *{visibility:visible}#printd{position:absolute;left:0;top:0;width:100%;max-width:none;box-shadow:none}#printd .bx-bar{display:none}#printd .bx-dlg-in{background:#fff;padding:0}.pr-doc{border:0}}
"""

BX_JS = r"""
(function () {
  var CT = window.CT, $ = function (id) { return document.getElementById(id); };
  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var money = function (n) { return n == null || n === "" ? "-" : (n < 0 ? "-" : "") + "₪" + Math.abs(Number(n)).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 }); };
  var dt = function (t) { return t ? String(t).slice(0, 10) + " " + String(t).slice(11, 16) : ""; };
  var d10 = function (t) { return t ? String(t).slice(0, 10) : ""; };
  var ST = { draft: "Draft", new: "New", quote_sent: "Quote sent", booked: "Booked", picked_up: "Picked up", in_transit: "In transit", delivered: "Delivered", cancelled: "Cancelled" };
  var PAY = { unpaid: "Unpaid", partial: "Partial", paid: "Paid", cancelled: "Cancelled" };
  var KIND = { charge: "Order charge", additional_charge: "Additional charge", payment: "Payment", deposit: "Deposit (credit card)", add_money: "Add money (system)", refund: "Refund" };
  var METH = { credit_card: "Credit card", bank_transfer: "Bank transfer", cash: "Cash", system: "System", check: "Check", other: "Other" };
  var TY = { parcel: "Parcel", doc: "Document", pallet: "Pallet", cont: "Container" };
  var TASKTY = { pickup: "Pickup", security: "Security", release_origin: "Release Origin", release_destination: "Release Destination", address: "Address", shipping_return: "Shipping Return" };
  var TASKCAT = { operation: "Operation", finance: "Finance" };
  var SHIP = { cargo: "Cargo", sea: "Sea", courier: "Courier", domestic: "Domestic" };
  var LBL = { shipping: "Shipping", remote: "Remote area surcharge", remote_area: "Remote area surcharge", signature: "Signature on delivery", adjust: "Price adjustment", manual: "Shipping" };
  var lbl = function (l) { return LBL[l.key] || l.label; };
  var chip = function (k, map) { return '<span class="bchip c-' + esc(k) + '">' + esc((map && map[k]) || k || "") + "</span>"; };
  var me = null, view = "", state = {}, cur = null, agentsCache = null;
  var say = function (id, m, bad) { var e = $(id); if (!e) return; e.textContent = m || ""; e.hidden = !m; e.className = "msg" + (bad ? " e" : ""); };
  var errOf = function (r) { return r && r.error && r.error.length > 3 && r.error !== "server" && r.error !== "network" ? r.error : "Something went wrong. Try again."; };

  /* ---------- sign-in gate ---------- */
  function gate(msg, acts) {
    $("bx-app").hidden = true; $("bx-gate").hidden = false; $("bx-msg").textContent = msg; var a = $("bx-acts"); a.innerHTML = "";
    (acts || []).forEach(function (x) { var b = document.createElement("button"); b.type = "button"; if (!x.line) b.className = "pri"; b.textContent = x.t; b.addEventListener("click", x.f); a.appendChild(b); });
  }
  async function refreshMe() {
    if (!CT.ready) return;
    if (!CT.user) return gate("Sign in to open the back office.", [{ t: "Sign in", f: function () { CT.openAuth("in"); } }]);
    var m = await CT.api("GET", "/admin/me");
    if (!m.ok) return gate("Could not check your permission. Try again.", [{ t: "Retry", f: refreshMe }]);
    if (!m.staff) {
      var acts = [{ t: "Sign out", line: true, f: function () { CT.signOut(); } }];
      if (m.canBootstrap) { acts.unshift({ t: "Set up the back office (make me main admin)", f: async function () { var r = await CT.api("POST", "/admin/bootstrap"); if (r.ok) refreshMe(); else gate("Setup failed.", acts); } }); return gate("This is the owner account. You can activate the back office.", acts); }
      if (!m.emailVerified) acts.unshift({ t: "Send e-mail verification link", f: async function () { try { await CT.verifyMail(); $("bx-msg").textContent = "Verification link sent. After verifying, refresh this page."; } catch (e) { $("bx-msg").textContent = CT.errText(e); } } });
      return gate("This account (" + (CT.user.email || "") + ") is not staff. Ask an admin to add you.", acts);
    }
    me = m; $("bx-gate").hidden = true; $("bx-app").hidden = false;
    $("bx-who").innerHTML = esc(m.name || "") + "<br><small>" + (m.role === "admin" ? "Admin" : "Staff") + "</small>";
    document.querySelectorAll("[data-admin]").forEach(function (b) { b.hidden = m.role !== "admin"; });
    route(); counts();
  }
  CT.onAuth(function () { refreshMe(); }); CT.init();
  $("bx-out").addEventListener("click", function () { CT.signOut(); });
  $("bx-out-all").addEventListener("click", async function () {
    if (!confirm("Sign out of every device, including this one? You'll need to sign in again right away, anywhere.")) return;
    await CT.api("POST", "/admin/staff/signout", {});
    CT.signOut();
  });

  async function counts() {
    var r = await CT.api("GET", "/admin/counts"); if (!r.ok) return;
    [["orders", r.newOrders], ["tasks", r.openTreatments], ["messages", r.newMessages]].forEach(function (p) { var b = $("b-" + p[0]); b.textContent = p[1]; b.hidden = !p[1]; });
  }

  /* ---------- quick search ---------- */
  $("qs-form").addEventListener("submit", async function (e) {
    e.preventDefault(); var q = $("qs-q").value.trim(); if (!q) return; $("qs-msg").hidden = true;
    var r = await CT.api("GET", "/admin/search?by=" + encodeURIComponent($("qs-by").value) + "&q=" + encodeURIComponent(q));
    if (!r.ok || !r.found) { $("qs-msg").textContent = "Nothing found."; $("qs-msg").hidden = false; return; }
    if (r.kind === "user") location.hash = "#user/" + r.id; else openShip(r.id);
  });

  /* ---------- router ---------- */
  var TITLES = { orders: "Orders", users: "Users", tasks: "Agent Tasks", payments: "Payments", agents: "Agents", receipts: "Receipts", messages: "Messages", ledger: "Accounting Transactions", quotes: "Price Quotation", outbox: "Outbox (e-mails)", staff: "Staff", finance: "Finance", coupons: "Coupons", pricelists: "Price List", banners: "Banners", settings: "Settings" };
  function route() {
    if (!me) return;
    var h = location.hash.replace(/^#\/?/, "") || "orders", p = h.split("/"), v = p[0];
    if (!TITLES[v] && v !== "user") v = "orders";
    view = v; document.querySelectorAll("#bx-nav a").forEach(function (a) { a.classList.toggle("on", a.getAttribute("data-v") === (v === "user" ? "users" : v)); });
    var sg = $("bx-nav-settings"); if (sg) { var inGroup = sg.querySelector("a.on"); sg.classList.toggle("has-on", !!inGroup); if (inGroup) sg.open = true; }
    $("bx-title").textContent = v === "user" ? "User details" : TITLES[v]; state = { page: 0, f: {} };
    var box = $("bx-view"); box.innerHTML = "";
    if (v === "user") return userPage(p[1]);
    if (v === "agents") return agentsPage();
    if (v === "staff") return staffPage();
    if (v === "finance") return financePage();
    if (v === "coupons") return couponsPage();
    if (v === "pricelists") return pricelistsPage();
    if (v === "banners") return bannersPage();
    if (v === "settings") return settingsPage();
    listPage(v);
  }
  window.addEventListener("hashchange", route);

  /* ---------- generic list pages ---------- */
  var LM = { orders: "orders", users: "users", tasks: "treatments", payments: "payments", receipts: "receipts", messages: "messages", ledger: "ledger", quotes: "quotes", outbox: "outbox" };
  var orderCols = function (extra) {
    return [["Pickup ID", function (r) { return "<b>" + esc(r.id) + "</b>"; }], ["Date", function (r) { return esc(d10(r.createdAt)); }],
      ["User", function (r) { return (r.uid ? (r.userNo ? "#" + r.userNo + " " : "") : '<span class="bchip c-partial">Guest</span> ') + esc(r.name) + "<small>" + esc(r.email) + "</small>"; }],
      ["Route", function (r) { return esc(String(r.from || "").toUpperCase()) + " → " + esc(String(r.to || "").toUpperCase()) + "<small>" + esc((r.fromCity || "") + " → " + (r.toCity || "")) + "</small>"; }],
      ["Carrier", function (r) { return esc(r.carrier); }], ["Ship type", function (r) { return r.shipType ? chip(r.shipType, SHIP) : "-"; }], ["Tracking", function (r) { return esc(r.tracking); }], ["Pickup", function (r) { return esc(r.pickupDate); }]].concat(extra || []);
  };
  var CFG = {
    orders: { f: ["q", "from", "to", "status", "type", "shipType"], guestHighlight: true, cols: orderCols([["Status", function (r) { return chip(r.status, ST) + (r.treatment ? ' <span class="bchip c-open">In treatment</span>' : ""); }], ["Payment", function (r) { return chip(r.pay, PAY) + (!r.uid && r.pay !== "paid" ? ' <button type="button" class="pay-confirm" data-pc="' + esc(r.id) + '">Confirm payment</button>' : ""); }], ["Total", function (r) { return money(r.total); }, "r"]]), open: "id" },
    quotes: { f: ["q", "from", "to", "status"], st: ["draft", "new", "quote_sent"], guestHighlight: true, cols: orderCols([["Status", function (r) { return chip(r.status, ST); }], ["Quote", function (r) { return money(r.total); }, "r"]]), open: "id" },
    payments: { f: ["q", "from", "to", "pay", "type"], guestHighlight: true, cols: orderCols([["Payment", function (r) { return chip(r.pay, PAY) + (!r.uid && r.pay !== "paid" ? ' <button type="button" class="pay-confirm" data-pc="' + esc(r.id) + '">Confirm payment</button>' : ""); }], ["Total", function (r) { return money(r.total); }, "r"], ["Paid", function (r) { return money(r.paid); }, "r"], ["Due", function (r) { return '<span class="' + (r.due > 0 ? "neg" : "") + '">' + money(r.due) + "</span>"; }, "r"]]), open: "id", focus: "pay", sum: function (t) { return "Total " + money(t.total) + " · Paid " + money(t.paid) + " · Due " + money(t.due); } },
    users: { f: ["q", "from", "to"], cols: [["UserId", function (r) { return "<b>#" + r.userNo + "</b>"; }], ["Name", function (r) { return esc(r.name) + (r.blocked ? ' <span class="bchip c-cancelled">Blocked</span>' : ""); }], ["Email", function (r) { return esc(r.email); }], ["Phone", function (r) { return esc(r.phone); }], ["Type", function (r) { return esc(r.type); }], ["Joined", function (r) { return esc(d10(r.createdAt)); }], ["Orders", function (r) { return r.orders; }, "r"], ["Balance", function (r) { return '<span class="' + (r.balance > 0 ? "neg" : "") + '">' + money(r.balance) + "</span>"; }, "r"], ["Coupon", function (r) { return r.coupon ? '<span class="bchip c-paid">' + esc(r.coupon.code) + " (" + r.coupon.pct + "%)</span><small>by " + esc(r.coupon.by) + "</small>" : '<span class="mut">-</span>'; }]], openUser: "uid" },
    tasks: { f: ["q", "from", "to", "ttype", "openedBy", "tstatus"], defaults: { status: "open" }, cols: [["Opened", function (r) { return esc(dt(r.createdAt)); }], ["Pickup ID", function (r) { return r.orderId ? "<b>" + esc(r.orderId) + "</b>" : '<span class="mut">-</span>'; }], ["User", function (r) { return (r.userNo ? "#" + r.userNo + " " : "") + esc(r.name); }], ["Type", function (r) { return chip(r.type, TASKTY); }], ["Category", function (r) { return chip(r.category, TASKCAT); }], ["Treatment", function (r) { return esc(r.text) + (r.result ? "<small>Result: " + esc(r.result) + "</small>" : ""); }], ["Handled by", function (r) { return esc(r.handledByName); }], ["Opened by", function (r) { return esc(r.openedByName); }], ["Status", function (r) { return chip(r.status); }]], open: "orderId" },
    receipts: { f: ["q", "from", "to"], cols: [["Receipt no.", function (r) { return "<b>" + r.no + "</b>"; }], ["Date", function (r) { return esc(dt(r.at)); }], ["User", function (r) { return (r.userNo ? "#" + r.userNo + " " : "") + esc(r.userName); }], ["Pickup ID", function (r) { return esc(r.orderId); }], ["Method", function (r) { return esc(METH[r.method] || r.method); }], ["Amount", function (r) { return money(r.amount); }, "r"], ["By", function (r) { return esc(r.by); }], ["", function (r) { return '<button type="button" data-rc="' + esc(r.id) + '">View</button>'; }]], sum: function (t) { return "Total " + money(t.amount); } },
    ledger: { f: ["q", "from", "to", "kind"], cols: [["Date", function (r) { return esc(dt(r.at)); }], ["User", function (r) { return (r.userNo ? "#" + r.userNo + " " : "") + esc(r.userName); }], ["Pickup ID", function (r) { return esc(r.orderId); }], ["Type", function (r) { return esc(KIND[r.kind] || r.kind); }], ["Method", function (r) { return esc(METH[r.method] || r.method); }], ["Note", function (r) { return esc(r.note); }], ["Debit", function (r) { return r.debit ? money(r.debit) : ""; }, "r"], ["Credit", function (r) { return r.credit ? money(r.credit) : ""; }, "r"], ["By", function (r) { return esc(r.by); }]], open: "orderId", sum: function (t) { return "Debit " + money(t.debit) + " · Credit " + money(t.credit) + " · Balance " + money(t.debit - t.credit); } },
    messages: { f: ["q", "from", "to", "mstatus"], cols: [["Received", function (r) { return esc(dt(r.createdAt)); }], ["Name", function (r) { return esc(r.name); }], ["Phone", function (r) { return esc(r.phone); }], ["Service", function (r) { return esc(r.service); }], ["Route", function (r) { return esc(r.route); }], ["Cargo", function (r) { return esc(r.cargo) + "<small>" + esc(r.page) + "</small>"; }], ["Status", function (r) { return chip(r.status); }], ["Note", function (r) { return esc(r.note); }], ["", function (r) { return '<button type="button" data-ms="' + esc(r.id) + '" data-st="read">Read</button> <button type="button" data-ms="' + esc(r.id) + '" data-st="done">Done</button> <button type="button" data-mn="' + esc(r.id) + '">Note</button>' + (r.phone ? ' <a href="https://wa.me/' + String(r.phone).replace(/\D/g, "").replace(/^0/, "972") + '" target="_blank" rel="noopener">WhatsApp</a>' : ""); }]] },
    outbox: { f: ["q", "from", "to"], cols: [["Queued", function (r) { return esc(dt(r.at)); }], ["To", function (r) { return esc(r.to); }], ["Subject", function (r) { return esc(r.subject); }], ["Pickup ID", function (r) { return esc(r.orderId); }], ["Type", function (r) { return esc(r.kind); }], ["By", function (r) { return esc(r.by); }], ["Status", function (r) { return chip(r.status === "queued" ? "open" : "closed").replace(/Open|open/, "Queued"); }]], note: "E-mails are queued here. Real sending starts when a mail service is connected." },
  };
  var FIELD = {
    q: '<div class="grow"><label for="f-q">Search</label><input id="f-q" type="search" placeholder="Search"></div>',
    from: '<div><label for="f-from">From date</label><input id="f-from" type="date"></div>', to: '<div><label for="f-to">To date</label><input id="f-to" type="date"></div>',
    status: '<div><label for="f-status">Status</label><select id="f-status"><option value="">All</option>' + Object.keys(ST).map(function (k) { return '<option value="' + k + '">' + ST[k] + "</option>"; }).join("") + "</select></div>",
    pay: '<div><label for="f-pay">Payment</label><select id="f-pay"><option value="">All</option><option value="unpaid">Unpaid</option><option value="partial">Partial</option><option value="paid">Paid</option></select></div>',
    type: '<div><label for="f-type">Customer</label><select id="f-type"><option value="">All</option><option value="private">Private</option><option value="business">Business</option></select></div>',
    shipType: '<div><label for="f-shipType">Ship type</label><select id="f-shipType"><option value="">All</option>' + Object.keys(SHIP).map(function (k) { return '<option value="' + k + '">' + SHIP[k] + "</option>"; }).join("") + "</select></div>",
    kind: '<div><label for="f-kind">Type</label><select id="f-kind"><option value="">All</option>' + Object.keys(KIND).map(function (k) { return '<option value="' + k + '">' + KIND[k] + "</option>"; }).join("") + "</select></div>",
    tstatus: '<div><label for="f-status">Status</label><select id="f-status"><option value="">All</option><option value="open">Open</option><option value="closed">Closed</option></select></div>',
    mstatus: '<div><label for="f-status">Status</label><select id="f-status"><option value="">All</option><option value="new">New</option><option value="read">Read</option><option value="done">Done</option></select></div>',
    ttype: '<div><label for="f-type">Task type</label><select id="f-type"><option value="">All</option>' + Object.keys(TASKTY).map(function (k) { return '<option value="' + k + '">' + TASKTY[k] + "</option>"; }).join("") + "</select></div>",
    openedBy: '<div><label for="f-openedBy">Opened by</label><select id="f-openedBy"><option value="">All</option></select></div>',
  };
  function filterVals() {
    var f = {}; ["q", "from", "to", "status", "pay", "type", "kind", "shipType", "openedBy"].forEach(function (k) { var e = $("f-" + k); if (e) f[k] = e.value.trim(); }); return f;
  }
  async function listPage(v) {
    var c = CFG[v], box = $("bx-view");
    var staffNames = []; if (v === "tasks") { var sn = await CT.api("GET", "/admin/staff/names"); staffNames = sn.ok ? sn.staff.filter(function (s) { return s.active; }) : []; }
    var statusOpts = c.st ? FIELD.status.replace(/<option value="">All<\/option>.*<\/select>/, '<option value="">All</option>' + c.st.map(function (k) { return '<option value="' + k + '">' + ST[k] + "</option>"; }).join("") + "</select>") : null;
    box.innerHTML =
      '<div class="card"><form class="flt" id="f-form">' + c.f.map(function (k) { return k === "status" && statusOpts ? statusOpts : k === "openedBy" ? FIELD.openedBy.replace("</select>", staffNames.map(function (s) { return '<option value="' + s.uid + '">' + esc(s.name) + "</option>"; }).join("") + "</select>") : FIELD[k]; }).join("") + '<div class="btns"><button type="submit" class="pri">Search</button><button type="button" id="f-reset">Reset</button>' + (v === "tasks" ? '<button type="button" class="pri" id="nt-toggle" title="New task">+</button>' : "") + '</div></form></div>' +
      (v === "tasks" ? '<div class="card" id="nt-wrap" hidden><h2>New task</h2><form id="nt-form" class="frm">' + fld("uid", "User ID (give this or Pickup ID)", "", "number") + fld("pid", "Pickup ID (give this or User ID)", "") + sel("ttype", "Type", Object.keys(TASKTY).map(function (k) { return [k, TASKTY[k]]; }), "") + sel("tcat", "Category", [["operation", "Operation"], ["finance", "Finance"]], "operation") + sel("thandle", "Handled by", staffNames.map(function (s) { return [s.uid, s.name]; }), me.uid) + '<div class="wf"><label for="p-text">What needs handling</label><textarea id="p-text"></textarea></div><div><button type="submit" class="pri" title="Open task">+</button></div></form><div id="nt-msg" hidden></div></div>' : "") +
      (c.note ? '<p class="mut">' + esc(c.note) + "</p>" : "") + '<div class="meta"><span id="l-meta">Loading...</span><span class="pg"><button type="button" id="l-prev">‹ Prev</button><span id="l-pg"></span><button type="button" id="l-next">Next ›</button></span></div><div class="tw"><table class="t"><thead><tr>' +
      c.cols.map(function (x) { return '<th class="' + (x[2] || "") + '">' + esc(x[0]) + "</th>"; }).join("") + '</tr></thead><tbody id="l-body"></tbody></table><div class="empty" id="l-empty" hidden>Nothing to show.</div></div>';
    if (c.defaults) Object.keys(c.defaults).forEach(function (k) { var e = $("f-" + k); if (e) e.value = c.defaults[k]; });
    $("f-form").addEventListener("submit", function (e) { e.preventDefault(); state.page = 0; load(); });
    $("f-reset").addEventListener("click", function () { $("f-form").reset(); if (c.defaults) Object.keys(c.defaults).forEach(function (k) { var e = $("f-" + k); if (e) e.value = c.defaults[k]; }); state.page = 0; load(); });
    $("l-prev").addEventListener("click", function () { if (state.page > 0) { state.page--; load(); } });
    $("l-next").addEventListener("click", function () { if ((state.page + 1) * 100 < state.total) { state.page++; load(); } });
    var ntt = $("nt-toggle"); if (ntt) ntt.addEventListener("click", function () { var w = $("nt-wrap"); w.hidden = !w.hidden; });
    var ntf = $("nt-form");
    if (ntf) ntf.addEventListener("submit", async function (e) {
      e.preventDefault();
      var uidVal = pv("uid").trim(), pidVal = pv("pid").trim();
      if (!uidVal && !pidVal) return say("nt-msg", "Give at least a User ID or a Pickup ID.", true);
      var t = pv("text"); if (!t.trim()) return say("nt-msg", "Describe what needs handling.", true);
      var body = { type: pv("ttype"), category: pv("tcat"), handledByUid: pv("thandle"), text: t };
      if (pidVal) {
        var sr = await CT.api("GET", "/admin/search?by=pickupId&q=" + encodeURIComponent(pidVal));
        if (!sr.ok || !sr.found) return say("nt-msg", "Pickup ID not found.", true);
        body.orderId = sr.id;
      }
      if (uidVal) {
        var ur = await CT.api("GET", "/admin/search?by=userId&q=" + encodeURIComponent(uidVal));
        if (!ur.ok || !ur.found) return say("nt-msg", "User ID not found.", true);
        body.uid = ur.id;
      }
      var x = await CT.api("POST", "/admin/task/create", body);
      if (!x.ok) return say("nt-msg", errOf(x), true);
      ntf.reset(); say("nt-msg", "Task opened."); load(); counts();
    });
    load();
    async function load() {
      var f = filterVals(), qs = "m=" + LM[v] + "&page=" + state.page;
      Object.keys(f).forEach(function (k) { if (f[k]) qs += "&" + k + "=" + encodeURIComponent(f[k]); });
      $("l-meta").textContent = "Loading...";
      var r = await CT.api("GET", "/admin/list?" + qs); if (view !== v) return;
      if (!r.ok) { $("l-meta").textContent = "Could not load."; return; }
      state.total = r.total; state.rows = r.rows;
      $("l-meta").textContent = r.total + " records" + (r.totals && c.sum ? " · " + c.sum(r.totals) : "");
      $("l-pg").textContent = "Page " + (r.page + 1) + " / " + Math.max(1, Math.ceil(r.total / 100));
      $("l-prev").disabled = r.page === 0; $("l-next").disabled = (r.page + 1) * 100 >= r.total;
      var tb = $("l-body"); tb.innerHTML = ""; $("l-empty").hidden = r.rows.length > 0;
      r.rows.forEach(function (row) {
        var tr = document.createElement("tr"); tr.innerHTML = c.cols.map(function (x) { return '<td class="' + (x[2] || "") + '">' + x[1](row) + "</td>"; }).join("");
        if (v === "tasks" || c.open || c.openUser) { tr.className = "ck"; tr.addEventListener("click", function (e) { if (e.target.closest("button,a,select")) return; if (v === "tasks") return openTask(row.id); if (c.openUser) location.hash = "#user/" + row[c.openUser]; else if (row[c.open]) openShip(row[c.open], c.focus); }); }
        if (c.guestHighlight && !row.uid) tr.classList.add("guest-row");
        tb.appendChild(tr);
      });
      tb.querySelectorAll("[data-pc]").forEach(function (b) { b.addEventListener("click", function (e) { e.stopPropagation(); openShip(b.getAttribute("data-pc"), "pay"); }); });
      tb.querySelectorAll("[data-ms]").forEach(function (b) { b.addEventListener("click", async function () { await CT.api("POST", "/admin/message/update", { id: b.getAttribute("data-ms"), status: b.getAttribute("data-st") }); load(); counts(); }); });
      tb.querySelectorAll("[data-mn]").forEach(function (b) { b.addEventListener("click", async function () { var t = prompt("Note"); if (t == null) return; await CT.api("POST", "/admin/message/update", { id: b.getAttribute("data-mn"), note: t }); load(); }); });
      tb.querySelectorAll("[data-rc]").forEach(function (b) { b.addEventListener("click", function () { var rc = state.rows.filter(function (x) { return x.id === b.getAttribute("data-rc"); })[0]; if (rc) printReceipt(rc, rc.userName); }); });
    }
    state.reload = load;
  }
  function reloadView() { if (state.reload) state.reload(); else if (view === "user") route(); counts(); }

  /* ---------- task detail (Agent Tasks) ---------- */
  var curTask = null;
  async function openTask(id) {
    var r = await CT.api("GET", "/admin/task?id=" + encodeURIComponent(id)); if (!r.ok) return;
    curTask = r; var d = $("taskd"); if (!d.open) d.showModal(); renderTask();
  }
  async function renderTask() {
    var R = curTask, t = R.task, box = $("task-in");
    var sn = await CT.api("GET", "/admin/staff/names"); var staffList = sn.ok ? sn.staff.filter(function (s) { return s.active; }) : [];
    box.innerHTML =
      '<div class="sh-head"><h2>' + chip(t.type, TASKTY) + " " + chip(t.category, TASKCAT) + " " + chip(t.status) + '</h2><button type="button" id="tk-x">Close window</button></div>' +
      '<div class="card"><div class="three"><dl class="kv"><dt>Pickup ID</dt><dd>' + (t.orderId ? '<a href="#" id="tk-order">' + esc(t.orderId) + "</a>" : '<span class="mut">-</span>') + "</dd></dl><dl class=\"kv\"><dt>User</dt><dd>" + (t.userNo ? '<a href="#user/' + esc(t.uid) + '" id="tk-user">#' + t.userNo + " " + esc(t.userName) + "</a>" : "-") + "</dd></dl><dl class=\"kv\"><dt>Opened by</dt><dd>" + esc(t.openedByName) + "</dd></dl></div>" +
      '<div class="wf"><label for="tk-desc">Treatment</label><textarea id="tk-desc">' + esc(t.text) + '</textarea></div>' +
      '<div class="frm"><div><label for="tk-awb">AWB</label><input id="tk-awb" type="text" value="' + esc(t.awb || "") + '"></div>' +
      (t.status === "open" ? '<div><label for="tk-handle">Handled by</label><select id="tk-handle">' + staffList.map(function (s) { return '<option value="' + s.uid + '"' + (s.uid === t.handledByUid ? " selected" : "") + ">" + esc(s.name) + "</option>"; }).join("") + "</select></div>" : '<div><label>Handled by</label><div style="padding-top:7px">' + esc(t.handledByName) + "</div></div>") +
      '</div><div class="bx-bar"><button type="button" class="pri" id="tk-save">Save changes</button>' + (t.status === "open" ? '<button type="button" class="dng" id="tk-close">Close task</button>' : "") + "</div><div id=\"tk-msg\" hidden></div></div>" +
      '<div class="card"><h3>Updates</h3>' + (R.log.length ? R.log.map(function (l) { return '<div class="ent">' + esc(l.text) + "<br><small>" + esc(l.by) + " · " + esc(dt(l.at)) + "</small></div>"; }).join("") : '<span class="mut">No updates yet.</span>') +
      (t.status === "open" ? '<div class="wf" style="margin-top:10px"><label for="tk-note">Add an update</label><textarea id="tk-note"></textarea></div><div><button type="button" class="pri" id="tk-add">Add update</button></div>' : "") + "</div>";
    $("tk-x").addEventListener("click", function () { $("taskd").close(); reloadView(); });
    var ord = $("tk-order"); if (ord) ord.addEventListener("click", function (e) { e.preventDefault(); $("taskd").close(); openShip(t.orderId); });
    var sv = $("tk-save"); if (sv) sv.addEventListener("click", async function () {
      var jobs = [CT.api("POST", "/admin/task/update", { treatmentId: t.id, awb: pv("tk-awb"), desc: pv("tk-desc") })];
      var hSel = $("tk-handle"); if (hSel && hSel.value !== t.handledByUid) jobs.push(CT.api("POST", "/admin/task/reassign", { treatmentId: t.id, handledByUid: hSel.value }));
      var results = await Promise.all(jobs);
      var bad = results.find(function (x) { return !x.ok; });
      if (bad) return say("tk-msg", errOf(bad), true);
      await openTask(t.id); say("tk-msg", "Saved."); reloadView();
    });
    var cl = $("tk-close"); if (cl) cl.addEventListener("click", async function () {
      if (!confirm("Close this task?")) return;
      var x = await CT.api("POST", "/admin/task/close", { treatmentId: t.id, text: pv("tk-note") });
      if (!x.ok) return say("tk-msg", errOf(x), true);
      await openTask(t.id); reloadView();
    });
    var add = $("tk-add"); if (add) add.addEventListener("click", async function () {
      var n = pv("tk-note"); if (!n.trim()) return say("tk-msg", "Write something first.", true);
      var x = await CT.api("POST", "/admin/task/update", { treatmentId: t.id, text: n });
      if (!x.ok) return say("tk-msg", errOf(x), true);
      await openTask(t.id);
    });
  }
  $("taskd").addEventListener("close", function () { curTask = null; });

  /* ---------- printable documents ---------- */
  function showDoc(html) { $("pr-doc").innerHTML = html; var d = $("printd"); if (!d.open) d.showModal(); }
  $("pr-go").addEventListener("click", function () { window.print(); }); $("pr-x").addEventListener("click", function () { $("printd").close(); });
  function printReceipt(rc, name) {
    showDoc("<h2>Receipt #" + rc.no + "</h2><p>CargoTech · " + esc(dt(rc.at)) + "</p><table><tr><td>Received from</td><td>" + esc(name || rc.name || "") + "</td></tr><tr><td>Pickup ID</td><td>" + esc(rc.orderId || "-") + "</td></tr><tr><td>Method</td><td>" + esc(METH[rc.method] || rc.method) + "</td></tr><tr><td>Note</td><td>" + esc(rc.note || "") + "</td></tr><tr><th>Amount</th><th class='r'>" + money(rc.amount) + "</th></tr></table><p class='mut'>No VAT is shown in this document.</p>");
  }
  function printInvoice(o, u, pay) {
    var q = o.quote || {};
    showDoc("<h2>Invoice #" + (o.invoice ? o.invoice.no : "") + "</h2><p>CargoTech · " + esc(dt(o.invoice && o.invoice.at)) + "</p><p><b>Bill to:</b> " + esc((o.contact && o.contact.name) || (u && u.name) || "") + "<br>" + esc((o.contact && o.contact.email) || "") + "</p><p><b>Shipment " + esc(o.id) + "</b><br>" + esc((o.sender && o.sender.city) || "") + ", " + esc(String(o.from).toUpperCase()) + " → " + esc((o.recipient && o.recipient.city) || "") + ", " + esc(String(o.to).toUpperCase()) + "<br>" + esc(q.carrier || "") + " " + esc(q.service || "") + "</p><table>" +
      (q.lines || []).map(function (l) { return "<tr><td>" + esc(lbl(l)) + "</td><td class='r'>" + money(l.price) + "</td></tr>"; }).join("") + "<tr><th>Total</th><th class='r'>" + money(q.total) + "</th></tr><tr><td>Paid</td><td class='r'>" + money(pay.paid) + "</td></tr><tr><td>Balance due</td><td class='r'>" + money(pay.due) + "</td></tr></table>");
  }

  /* ---------- the shipment dialog ---------- */
  var panel = null, focusPay = false;
  async function openShip(id, focus) {
    var r = await CT.api("GET", "/admin/order?id=" + encodeURIComponent(id)); if (!r.ok) return;
    cur = r; panel = null; focusPay = focus === "pay"; var d = $("shipd"); if (!d.open) d.showModal(); renderShip(); if (focusPay) { var e = $("sh-pay"); if (e) e.scrollIntoView(); }
  }
  var adr = function (a) { a = a || {}; return esc([a.name, a.company, ((a.street || "") + " " + (a.house || "")).trim(), a.city, a.zip, a.country && a.country.toUpperCase()].filter(Boolean).join(", ")) + "<br><small>" + esc([a.phone, a.email].filter(Boolean).join(" · ")) + "</small>"; };
  var TRACK = { fedex: "https://www.fedex.com/fedextrack/?trknbr=", dhl: "https://www.dhl.com/global-en/home/tracking.html?tracking-id=", ups: "https://www.ups.com/track?tracknum=" };
  var trackUrl = function (o) { var t = o.pickup && o.pickup.trackingNumber, c = String((o.quote && o.quote.carrier) || "").toLowerCase(), k = Object.keys(TRACK).filter(function (x) { return c.indexOf(x) > -1; })[0]; return t && k ? TRACK[k] + encodeURIComponent(t) : ""; };
  function renderShip() {
    var R = cur, o = R.order, q = o.quote || {}, admin = R.role === "admin", p = R.pay, u = R.user, box = $("ship-in");
    var acts = [["tracking", "Tracking"], ["label", "Label"], ["invoice", "Invoice"], ["receipt", "Receipt"], ["resend", "Resend"], ["return", "Return"], ["change_label", "Change Label"], ["pickup_time", "Change Pickup Time"], ["ship_type", "Ship Type"], ["deposit", "Deposit (Credit Card)", 1], ["add_money", "Add Money (System)", 1], ["doc_add", "Add Documents"], ["treatment_add", "In Treatment"], ["comment", "Log / Add Comment"], ["user_details", "Update User Details"], ["pickup_details", "Update Pickup Details"], ["manage_pickup", "Manage Pickup"], ["summary", "Summary Email To User"], ["email_user", "Email To User"], ["email_agent", "Email To Agent"], ["whatsapp", "WhatsApp"], ["additional_charge", "Additional Charge", 1], ["charge_order", "Charge Order", 1], ["refund", "Refund", 1], ["price", "Manual Price"], ["status", "Change Status"], ["actual_weight", "Actual Weight"], ["pricing_override", "Pricing Override", 1], ["cancel", "Cancel Order"]];
    box.innerHTML = '<div class="sh-head"><h2>Shipment ' + esc(o.id) + " " + chip(o.status, ST) + " " + chip(p.status, PAY) + (o.returned ? ' <span class="bchip c-cancelled">Returned</span>' : "") + '</h2><button type="button" id="sh-x">Close</button></div>' +
      '<div class="card"><div class="acts" id="sh-acts">' + acts.filter(function (a) { return !a[2] || admin; }).map(function (a) { return '<button type="button" data-a="' + a[0] + '" class="' + (panel === a[0] ? "on" : "") + '">' + a[1] + "</button>"; }).join("") + '</div><div id="sh-panel"></div><div id="sh-msg" hidden></div></div>' +
      '<div class="two"><div class="card"><h3>Customer</h3><dl class="kv"><dt>User</dt><dd>' + (u ? '<a href="#user/' + esc(u.uid) + '" id="sh-ulink">#' + u.userNo + " " + esc(u.name || u.email) + "</a>" : "Guest") + "</dd><dt>Name</dt><dd>" + esc((o.contact && o.contact.name) || "") + "</dd><dt>Phone</dt><dd>" + esc((o.contact && o.contact.phone) || "") + "</dd><dt>Email</dt><dd>" + esc((o.contact && o.contact.email) || "") + "</dd><dt>Type</dt><dd>" + (o.customerType === "business" ? "Business" : "Private") + "</dd><dt>Created</dt><dd>" + esc(dt(o.createdAt)) + "</dd></dl></div>" +
      '<div class="card"><h3>Shipment</h3><dl class="kv"><dt>Route</dt><dd>' + esc(String(o.from).toUpperCase()) + " → " + esc(String(o.to).toUpperCase()) + "</dd><dt>Type</dt><dd>" + esc(TY[o.type] || "") + "</dd><dt>Ship type</dt><dd>" + esc(SHIP[o.shipType] || "-") + "</dd><dt>Packages</dt><dd>" + (o.type === "cont" ? esc((o.cont && o.cont.size) + " × " + (o.cont && o.cont.qty)) : (o.parcels || []).map(function (x) { return esc(x.qty + " × " + x.kg + " kg (" + x.l + "×" + x.w + "×" + x.h + ")"); }).join("<br>")) + "</dd><dt>Actual weight</dt><dd>" + (o.actualKg != null ? o.actualKg + " kg" : "-") + "</dd><dt>Signature</dt><dd>" + esc(o.signature || "none") + "</dd><dt>Insurance</dt><dd>" + (o.insurance && o.insurance.requested ? "Requested, value " + esc(o.insurance.amount) : "No") + "</dd></dl></div></div>" +
      '<div class="two"><div class="card"><h3>Sender</h3>' + adr(o.sender) + '</div><div class="card"><h3>Recipient' + (o.recipient && o.recipient.residential ? " (residential)" : "") + "</h3>" + adr(o.recipient) + "</div></div>" +
      '<div class="two"><div class="card"><h3>Pickup &amp; tracking</h3><dl class="kv"><dt>Pickup date</dt><dd>' + esc((o.pickup && o.pickup.date) || "") + " " + esc((o.pickup && o.pickup.time) || "") + "</dd><dt>Pickup status</dt><dd>" + esc((o.pickup && o.pickup.pickupStatus) || "-") + "</dd><dt>Confirmation</dt><dd>" + esc((o.pickup && o.pickup.confirmation) || "") + "</dd><dt>Call number</dt><dd>" + esc((o.pickup && o.pickup.callNumber) || "") + "</dd><dt>Shipping authorization</dt><dd>" + esc((o.pickup && o.pickup.trackingNumber) || "") + "</dd><dt>Label</dt><dd>" + (o.label && o.label.url ? '<a href="' + esc(o.label.url) + '" target="_blank" rel="noopener">Open label</a>' : "-") + "</dd></dl></div>" +
      '<div class="card"><h3>Goods &amp; terms</h3>' + (o.items || []).map(function (i) { return "<div>" + esc(i.desc) + " · " + esc(i.qty) + " × " + esc(i.value) + " " + esc(i.currency) + (i.hs ? " · HS " + esc(i.hs) : "") + (i.origin ? " · " + esc(String(i.origin).toUpperCase()) : "") + "</div>"; }).join("") + '<dl class="kv"><dt>Incoterm</dt><dd>' + esc((o.terms && o.terms.incoterm) || "") + "</dd><dt>Reason</dt><dd>" + esc((o.terms && o.terms.reason) || "") + "</dd><dt>Description</dt><dd>" + esc((o.terms && o.terms.shortDesc) || "") + "</dd></dl></div></div>" +
      '<div class="card" id="sh-pay"><h2>Payment</h2><div class="three"><div><h3>Order by user</h3><dl class="kv"><dt>Customer</dt><dd>' + esc((o.contact && o.contact.name) || "") + "</dd><dt>Date</dt><dd>" + esc(d10(o.submittedAt || o.createdAt)) + "</dd><dt>Carrier</dt><dd>" + esc(q.carrier || "") + " " + esc(q.service || "") + "</dd><dt>Quote</dt><dd>" + (q.total != null ? money(q.total) : "Manual") + "</dd></dl></div>" +
      '<div><h3>Details after pickup</h3><dl class="kv"><dt>Actual weight</dt><dd>' + (o.actualKg != null ? o.actualKg + " kg" : "-") + "</dd><dt>Charged</dt><dd>" + money(p.charged) + "</dd><dt>Paid</dt><dd>" + money(p.paid) + "</dd><dt>Due</dt><dd class='" + (p.due > 0 ? "neg" : "") + "'>" + money(p.due) + "</dd></dl></div>" +
      '<div><h3>Complete order</h3><dl class="kv"><dt>Status</dt><dd>' + chip(o.status, ST) + "</dd><dt>Completed</dt><dd>" + esc(dt(o.completedAt)) + "</dd><dt>Invoice</dt><dd>" + (o.invoice ? "#" + o.invoice.no : "-") + "</dd><dt>Receipts</dt><dd>" + R.receipts.map(function (x) { return "#" + x.no; }).join(", ") + (R.receipts.length ? "" : "-") + '</dd></dl></div></div>' +
      '<h3 style="margin-top:12px">Other details</h3>' +
      (admin ? '<div class="li"><span>Commission</span><span>' + (o.commissionPctOverride != null ? o.commissionPctOverride + "%" : "Default (" + (q.markupPct != null ? q.markupPct : "-") + "%)") + "</span></div><div class=\"li\"><span>Discount</span><span>" + (o.discountPct ? o.discountPct + "% (shipment override)" : q.customerDiscountPct ? q.customerDiscountPct + "% (customer discount)" : "-") + "</span></div>" + (q.originalTotal != null ? '<div class="li"><span>Price before discount</span><span><s>' + money(q.originalTotal) + "</s></span></div>" : "") : "") +
      '<div class="li"><span>Coupon</span><span>' + (o.coupon ? (o.coupon.hidden ? "Staff code used" : "Staff: " + esc(o.coupon.staffName) + " · " + money(o.coupon.originalPrice) + " → " + money(o.coupon.newPrice) + " · " + esc(o.coupon.reason || "")) : "-") + "</span></div>" +
      (q.lines || []).map(function (l) { return '<div class="li"><span>' + esc(lbl(l)) + "</span><span>" + money(l.price) + (admin && l.cost != null ? " <small>cost " + money(l.cost) + "</small>" : "") + "</span></div>"; }).join("") +
      '<div class="li tot"><span>Total to customer</span><span>' + (q.total != null ? money(q.total) : "-") + "</span></div>" + (admin && q.cost != null ? '<div class="li"><span>Our cost / profit</span><span>' + money(q.cost) + " / " + money(q.profit) + "</span></div>" : "") +
      '<div class="bx-bar"><button type="button" data-a="live">Live Trace</button><button type="button" data-a="additional_charge"' + (admin ? "" : " hidden") + '>Additional Charge</button><button type="button" data-a="pdf">Download PDF</button></div></div>' +
      '<div class="two"><div class="card"><h3>Treatments</h3>' + (R.treatments.length ? R.treatments.map(function (t) { return '<div class="ent">' + chip(t.status) + " " + (t.type ? chip(t.type, TASKTY) + " " : "") + (t.category ? chip(t.category, TASKCAT) + " " : "") + esc(t.text) + "<br><small>" + esc(t.by) + " · " + esc(dt(t.createdAt)) + (t.result ? " · Result: " + esc(t.result) : "") + "</small>" + (t.status === "open" ? ' <button type="button" data-tc="' + esc(t.id) + '">Close</button>' : "") + "</div>"; }).join("") : '<span class="mut">None.</span>') + "</div>" +
      '<div class="card"><h3>Documents</h3>' + ((o.docs || []).length ? o.docs.map(function (d) { return '<div class="ent">' + (d.url ? '<a href="' + esc(d.url) + '" target="_blank" rel="noopener">' + esc(d.name) + "</a>" : esc(d.name)) + " <small>" + esc(d.by) + " · " + esc(dt(d.at)) + '</small> <button type="button" data-dr="' + esc(d.id) + '">Remove</button></div>'; }).join("") : '<span class="mut">None.</span>') + "</div></div>" +
      '<div class="two"><div class="card"><h3>Log</h3>' + (R.log.length ? R.log.map(function (l) { return '<div class="ent">' + esc(l.text) + "<br><small>" + esc(l.by) + " · " + esc(dt(l.at)) + "</small></div>"; }).join("") : '<span class="mut">No entries.</span>') + (o.notes || []).map(function (n) { return '<div class="ent">' + esc(n.text) + "<br><small>" + esc(n.by) + " · " + esc(dt(n.at)) + " (note)</small></div>"; }).join("") + "</div>" +
      '<div class="card"><h3>Accounting for this order</h3>' + (R.ledger.length ? R.ledger.map(function (l) { return '<div class="li"><span>' + esc(KIND[l.kind] || l.kind) + " <small>" + esc(dt(l.at)) + " · " + esc(l.by) + "</small></span><span>" + (l.debit ? money(l.debit) : "") + (l.credit ? '<span class="pos"> −' + money(l.credit) + "</span>" : "") + "</span></div>"; }).join("") : '<span class="mut">No entries.</span>') + "<h3 style='margin-top:12px'>E-mails</h3>" + (R.outbox.length ? R.outbox.map(function (m) { return '<div class="ent">' + esc(m.subject) + " <small>to " + esc(m.to) + " · " + esc(m.status) + " · " + esc(dt(m.at)) + "</small></div>"; }).join("") : '<span class="mut">None.</span>') + "</div></div>";
    $("sh-x").addEventListener("click", function () { $("shipd").close(); reloadView(); });
    box.querySelectorAll("[data-a]").forEach(function (b) { b.addEventListener("click", function () { act(b.getAttribute("data-a")); }); });
    box.querySelectorAll("[data-tc]").forEach(function (b) { b.addEventListener("click", function () { var t = prompt("Result / note (optional)"); if (t == null) return; run("treatment_close", { treatmentId: b.getAttribute("data-tc"), text: t }); }); });
    box.querySelectorAll("[data-dr]").forEach(function (b) { b.addEventListener("click", function () { run("doc_remove", { docId: b.getAttribute("data-dr") }); }); });
    var ul = $("sh-ulink"); if (ul) ul.addEventListener("click", function () { $("shipd").close(); });
    if (panel) drawPanel();
  }
  function flash(m, bad) { var e = $("sh-msg"); if (e) { e.textContent = m; e.hidden = !m; e.className = "msg" + (bad ? " e" : ""); } }
  async function run(action, body) {
    flash(""); var r = await CT.api("POST", "/admin/order/action", Object.assign({ id: cur.order.id, action: action }, body || {}));
    if (!r.ok) { flash(errOf(r), true); return null; }
    cur = r; renderShip(); flash("Saved."); counts(); return r;
  }
  async function getAgents() { if (!agentsCache) { var r = await CT.api("GET", "/admin/list?m=agents"); agentsCache = r.ok ? r.rows : []; } return agentsCache; }
  var fld = function (id, label, val, type, cls) { return '<div class="' + (cls || "") + '"><label for="p-' + id + '">' + label + '</label><input id="p-' + id + '" type="' + (type || "text") + '" value="' + esc(val == null ? "" : val) + '"></div>'; };
  var area = function (id, label, val) { return '<div class="wf"><label for="p-' + id + '">' + label + '</label><textarea id="p-' + id + '">' + esc(val || "") + "</textarea></div>"; };
  var sel = function (id, label, opts, val) { return '<div><label for="p-' + id + '">' + label + '</label><select id="p-' + id + '">' + opts.map(function (o) { return '<option value="' + o[0] + '"' + (o[0] === val ? " selected" : "") + ">" + esc(o[1]) + "</option>"; }).join("") + "</select></div>"; };
  var pv = function (id) { var e = $("p-" + id); return e ? e.value : ""; };
  async function act(a) {
    var o = cur.order, p = o.pickup || {}, q = o.quote || {};
    if (a === "live") { var u = trackUrl(o); if (u) window.open(u, "_blank", "noopener"); else flash(p.trackingNumber ? "No tracking page is known for this carrier. Tracking number: " + p.trackingNumber : "No tracking number yet.", true); return; }
    if (a === "pdf") return printInvoice(Object.assign({}, o, { invoice: o.invoice || { no: "(draft)", at: new Date().toISOString() } }), cur.user, cur.pay);
    if (a === "invoice") { var r1 = await run("invoice"); if (r1) printInvoice(r1.order, r1.user, r1.pay); return; }
    if (a === "receipt") { var r2 = await run("receipt"); if (r2 && r2.receipt) printReceipt(r2.receipt, (o.contact && o.contact.name) || ""); return; }
    if (a === "charge_order") { if (!confirm("Charge the customer account with the order price?")) return; return run("charge_order"); }
    if (a === "cancel") { if (!confirm("Cancel this order?")) return; return run("cancel"); }
    panel = panel === a ? null : a; renderShip();
  }
  async function drawPanel() {
    var a = panel, o = cur.order, p = o.pickup || {}, q = o.quote || {}, el = $("sh-panel"), H = "", go = "Save", fn = null, cancel = '<button type="button" id="p-x">Cancel</button>';
    var mail = (o.contact && o.contact.email) || "";
    switch (a) {
      case "tracking": H = "<h3>Tracking</h3><dl class='kv'><dt>Number</dt><dd>" + esc(p.trackingNumber || "-") + "</dd><dt>Carrier</dt><dd>" + esc(q.carrier || "-") + "</dd></dl>" + (trackUrl(o) ? '<a href="' + esc(trackUrl(o)) + '" target="_blank" rel="noopener">Open carrier tracking page</a>' : "<p class='mut'>Set the number with Label or Update Pickup Details.</p>"); go = null; break;
      case "label": case "change_label": H = "<h3>" + (a === "label" ? "Label" : "Change label") + "</h3><div class='frm'>" + fld("url", "Label link (PDF)", o.label && o.label.url, "text", "w2") + fld("trackingNumber", "Shipping authorization / tracking", p.trackingNumber) + fld("carrier", "Carrier", (o.label && o.label.carrier) || q.carrier) + fld("note", "Note", o.label && o.label.note, "text", "w2") + "</div>"; fn = function () { return { url: pv("url"), trackingNumber: pv("trackingNumber"), carrier: pv("carrier"), note: pv("note") }; }; break;
      case "pickup_time": H = "<h3>Change pickup time</h3><div class='frm'>" + fld("date", "Date", p.date, "date") + fld("time", "Time window", p.time) + "</div>"; fn = function () { return { date: pv("date"), time: pv("time") }; }; break;
      case "ship_type": H = "<h3>Shipment type</h3><div class='frm'>" + sel("shipType", "Type", [["", "Select..."], ["cargo", "Cargo"], ["sea", "Sea"], ["courier", "Courier"], ["domestic", "Domestic"]], o.shipType || "") + "</div>"; fn = function () { return { shipType: pv("shipType") }; }; break;
      case "pickup_details": H = "<h3>Update pickup details</h3><div class='frm'>" + fld("confirmation", "Pickup confirmation", p.confirmation) + fld("callNumber", "Driver call number", p.callNumber) + fld("trackingNumber", "Shipping authorization / tracking", p.trackingNumber) + "</div>"; fn = function () { return { confirmation: pv("confirmation"), callNumber: pv("callNumber"), trackingNumber: pv("trackingNumber") }; }; break;
      case "manage_pickup": H = "<h3>Manage pickup</h3><div class='frm'>" + sel("pickupStatus", "Pickup status", [["scheduled", "Scheduled"], ["confirmed", "Confirmed"], ["missed", "Missed"], ["done", "Done"], ["cancelled", "Cancelled"]], p.pickupStatus || "scheduled") + fld("confirmation", "Pickup confirmation", p.confirmation) + fld("callNumber", "Driver call number", p.callNumber) + "</div>"; a = "manage_pickup"; fn = function () { return { pickupStatus: pv("pickupStatus"), confirmation: pv("confirmation"), callNumber: pv("callNumber") }; }; break;
      case "user_details": {
        var side = function (k, t, x) { x = x || {}; return "<h3 class='wf'>" + t + "</h3>" + fld(k + "name", "Name", x.name) + fld(k + "company", "Company", x.company) + fld(k + "phone", "Phone", x.phone) + fld(k + "email", "Email", x.email, "email") + fld(k + "street", "Street", x.street) + fld(k + "house", "House", x.house) + fld(k + "city", "City", x.city) + fld(k + "zip", "Zip", x.zip); };
        H = "<h3>Update user details</h3><div class='frm'>" + side("s", "Sender", o.sender) + side("r", "Recipient", o.recipient) + "</div>";
        fn = function () { var m = function (k, x) { return Object.assign({}, x, { name: pv(k + "name"), company: pv(k + "company"), phone: pv(k + "phone"), email: pv(k + "email"), street: pv(k + "street"), house: pv(k + "house"), city: pv(k + "city"), zip: pv(k + "zip") }); }; return { sender: m("s", o.sender), recipient: m("r", o.recipient) }; }; break;
      }
      case "deposit": case "add_money": H = "<h3>" + (a === "deposit" ? "Deposit (credit card, entered manually)" : "Add money (system)") + "</h3><p class='mut'>Creates a payment entry and a receipt. Card charging itself is not connected yet.</p><div class='frm'>" + fld("amount", "Amount (₪)", "", "number") + fld("note", "Note", "", "text", "w2") + "</div>"; fn = function () { return { amount: pv("amount"), note: pv("note") }; }; break;
      case "additional_charge": H = "<h3>Additional charge</h3><div class='frm'>" + fld("amount", "Amount (₪)", "", "number") + fld("note", "Reason", "", "text", "w2") + "</div>"; fn = function () { return { amount: pv("amount"), note: pv("note") }; }; break;
      case "refund": H = "<h3>Refund</h3><div class='frm'>" + fld("amount", "Amount (₪)", "", "number") + sel("method", "Method", Object.keys(METH).map(function (k) { return [k, METH[k]]; }), "other") + fld("note", "Reason", "", "text", "w2") + "</div>"; fn = function () { return { amount: pv("amount"), method: pv("method"), note: pv("note") }; }; break;
      case "doc_add": H = "<h3>Add document</h3><p class='mut'>Add a name and a link to the file (file upload will be added with storage).</p><div class='frm'>" + fld("name", "Document name", "") + fld("url", "Link (https://...)", "", "text", "w2") + "</div>"; fn = function () { return { name: pv("name"), url: pv("url") }; }; break;
      case "treatment_add": { H = "<h3>Open a task (Agent Tasks)</h3><div class='frm'>" + sel("ttype", "Type", Object.keys(TASKTY).map(function (k) { return [k, TASKTY[k]]; }), "") + sel("tcat", "Category", [["operation", "Operation"], ["finance", "Finance"]], "operation") + area("text", "What needs handling", "") + "</div>"; fn = function () { return { type: pv("ttype"), category: pv("tcat"), text: pv("text") }; }; break; }
      case "comment": H = "<h3>Add comment to log</h3><div class='frm'>" + area("text", "Comment", "") + "</div>"; fn = function () { return { text: pv("text") }; }; break;
      case "status": H = "<h3>Change status</h3><div class='frm'>" + sel("status", "Status", Object.keys(ST).map(function (k) { return [k, ST[k]]; }), o.status) + "</div>"; fn = function () { return { status: pv("status") }; }; break;
      case "actual_weight": H = "<h3>Actual weight</h3><p class='mut'>Price is recalculated automatically from the same carrier/service, at the greater of this and the original dimensional weight.</p><div class='frm'>" + fld("kg", "Weight after pickup (kg)", o.actualKg, "number") + "</div>"; fn = function () { return { kg: pv("kg") }; }; break;
      case "pricing_override": H = "<h3>Pricing override (this shipment only)</h3><p class='mut'>Leave commission empty to use the default 110%/210% markup from Settings. Price is recalculated from the same carrier/service.</p><div class='frm'>" + fld("commissionPctOverride", "Commission (%)", o.commissionPctOverride, "number") + fld("discountPct", "Discount (%)", o.discountPct || "", "number") + "</div>"; fn = function () { return { commissionPctOverride: pv("commissionPctOverride"), discountPct: pv("discountPct") }; }; break;
      case "return": H = "<h3>Return shipment</h3><p class='mut'>Marks the shipment as returned and cancelled.</p><div class='frm'>" + area("text", "Reason", "") + "</div>"; fn = function () { return { text: pv("text") }; }; break;
      case "resend": H = "<h3>Resend shipment details to the customer</h3><div class='frm'>" + fld("to", "To", mail, "email", "w2") + "</div>"; fn = function () { return { to: pv("to") }; }; go = "Queue e-mail"; break;
      case "summary": H = "<h3>Summary e-mail to user</h3><div class='frm'>" + fld("to", "To", mail, "email", "w2") + area("text", "Extra text (optional)", "") + "</div>"; fn = function () { return { to: pv("to"), text: pv("text") }; }; go = "Queue e-mail"; break;
      case "email_user": H = "<h3>E-mail to user</h3><div class='frm'>" + fld("to", "To", mail, "email", "w2") + fld("subject", "Subject", "", "text", "wf") + area("text", "Message", "") + "</div>"; fn = function () { return { to: pv("to"), subject: pv("subject"), text: pv("text") }; }; go = "Queue e-mail"; break;
      case "email_agent": { var ag2 = await getAgents(); H = "<h3>E-mail to agent</h3><div class='frm'>" + sel("agentId", "Agent", [["", "- choose -"]].concat(ag2.map(function (x) { return [x.id, x.name + (x.email ? " (" + x.email + ")" : "")]; })), "") + fld("to", "Or e-mail address", "", "email") + fld("subject", "Subject", "", "text", "wf") + area("text", "Message (empty = shipment summary)", "") + "</div>"; fn = function () { return { agentId: pv("agentId"), to: pv("to"), subject: pv("subject"), text: pv("text") }; }; go = "Queue e-mail"; break; }
      case "whatsapp": H = "<h3>WhatsApp</h3><div class='frm'>" + fld("phone", "Phone", (o.contact && o.contact.phone) || "", "text") + area("text", "Message (empty = shipment summary)", "") + "</div>"; go = "Open WhatsApp"; fn = function () { return { phone: pv("phone"), text: pv("text") }; }; break;
      case "price": H = "<h3>Manual price</h3><div class='frm'>" + fld("price", "Price to customer (₪)", q.total, "number") + (cur.role === "admin" ? fld("cost", "Our cost (₪)", q.cost, "number") : "") + fld("carrier", "Carrier", q.carrier) + fld("service", "Service", q.service) + fld("days", "Days", q.days) + "</div>"; break;
      default: return;
    }
    el.innerHTML = '<div class="panel">' + H + '<div class="bx-bar">' + (go ? '<button type="button" class="pri" id="p-go">' + go + "</button>" : "") + cancel + "</div></div>";
    $("p-x").addEventListener("click", function () { panel = null; renderShip(); });
    var g = $("p-go"); if (!g) return;
    g.addEventListener("click", async function () {
      g.disabled = true;
      if (a === "price") { var r = await CT.api("POST", "/admin/order/update", { id: o.id, manualPrice: pv("price"), manualCost: cur.role === "admin" ? pv("cost") : undefined, carrier: pv("carrier"), service: pv("service"), days: pv("days") }); g.disabled = false; if (!r.ok) return flash(errOf(r), true); panel = null; return openShip(o.id); }
      var r2 = await run(a, fn ? fn() : {}); g.disabled = false;
      if (r2 && a === "whatsapp" && r2.url) window.open(r2.url, "_blank", "noopener");
      if (r2 && (a === "deposit" || a === "add_money") && r2.receipt) { panel = null; renderShip(); flash("Saved. Receipt #" + r2.receipt.no + " created."); }
      else if (r2) { panel = null; renderShip(); flash("Saved."); }
    });
  }
  $("shipd").addEventListener("close", function () { cur = null; });

  /* ---------- user page ---------- */
  var UTABS = [["orders", "Orders"], ["payments", "Payments"], ["accounting", "Accounting"], ["receipts", "Receipts"], ["ledger", "AccountingTransactions"], ["quotes", "PriceQuotation"], ["documents", "Documents"], ["update", "UpdateDetails"]];
  async function userPage(uid) {
    var rr = await Promise.all([CT.api("GET", "/admin/user?uid=" + encodeURIComponent(uid || "")), CT.api("GET", "/admin/staff/names")]);
    var r = rr[0], staffNames = rr[1].ok ? rr[1].staff : []; var box = $("bx-view");
    if (!r.ok) { box.innerHTML = '<div class="card">User not found. <a href="#users">Back to users</a></div>'; return; }
    var u = r.user, admin = r.role === "admin", tab = state.tab || "update";
    var tblO = function (rows) { return rows.length ? '<div class="tw"><table class="t"><thead><tr><th>Pickup ID</th><th>Date</th><th>Route</th><th>Status</th><th>Payment</th><th class="r">Total</th><th class="r">Due</th></tr></thead><tbody>' + rows.map(function (x) { return '<tr class="ck" data-o="' + esc(x.id) + '"><td><b>' + esc(x.id) + "</b></td><td>" + esc(d10(x.createdAt)) + "</td><td>" + esc(String(x.from).toUpperCase()) + " → " + esc(String(x.to).toUpperCase()) + "</td><td>" + chip(x.status, ST) + "</td><td>" + chip(x.pay, PAY) + '</td><td class="r">' + money(x.total) + '</td><td class="r">' + money(x.due) + "</td></tr>"; }).join("") + "</tbody></table></div>" : '<div class="empty">Nothing to show.</div>'; };
    var body = {
      orders: function () { return tblO(r.orders); }, payments: function () { return tblO(r.payments); }, quotes: function () { return tblO(r.quotes); },
      accounting: function () { return '<div class="three"><div class="card"><h3>Charged</h3><b>' + money(r.charged) + '</b></div><div class="card"><h3>Paid</h3><b>' + money(r.paid) + '</b></div><div class="card"><h3>Balance (owed)</h3><b class="' + (r.balance > 0 ? "neg" : "") + '">' + money(r.balance) + "</b></div></div>" + (admin ? '<div class="card"><h2>New accounting entry</h2><div class="frm"><div><label for="le-k">Entry</label><select id="le-k"><option value="credit">Payment received (credit)</option><option value="debit">Charge (debit)</option></select></div><div><label for="le-a">Amount (₪)</label><input id="le-a" type="number" min="0" step="0.01"></div><div><label for="le-m">Method</label><select id="le-m">' + Object.keys(METH).map(function (k) { return '<option value="' + k + '">' + METH[k] + "</option>"; }).join("") + '</select></div><div class="w2"><label for="le-n">Note</label><input id="le-n" type="text"></div><div><button type="button" class="pri" id="le-go">Add entry</button></div></div><div id="le-msg" hidden></div></div>' : ""); },
      receipts: function () { return r.receipts.length ? '<div class="tw"><table class="t"><thead><tr><th>No.</th><th>Date</th><th>Pickup ID</th><th>Method</th><th class="r">Amount</th><th></th></tr></thead><tbody>' + r.receipts.map(function (x) { return "<tr><td><b>" + x.no + "</b></td><td>" + esc(dt(x.at)) + "</td><td>" + esc(x.orderId) + "</td><td>" + esc(METH[x.method] || x.method) + '</td><td class="r">' + money(x.amount) + '</td><td><button type="button" data-rc="' + esc(x.id) + '">View</button></td></tr>'; }).join("") + "</tbody></table></div>" : '<div class="empty">No receipts.</div>'; },
      ledger: function () { return r.ledger.length ? '<div class="tw"><table class="t"><thead><tr><th>Date</th><th>Type</th><th>Pickup ID</th><th>Note</th><th class="r">Debit</th><th class="r">Credit</th></tr></thead><tbody>' + r.ledger.map(function (x) { return "<tr><td>" + esc(dt(x.at)) + "</td><td>" + esc(KIND[x.kind] || x.kind) + "</td><td>" + esc(x.orderId) + "</td><td>" + esc(x.note) + '</td><td class="r">' + (x.debit ? money(x.debit) : "") + '</td><td class="r">' + (x.credit ? money(x.credit) : "") + "</td></tr>"; }).join("") + "</tbody></table></div>" : '<div class="empty">No transactions.</div>'; },
      documents: function () { return r.documents.length ? r.documents.map(function (d) { return '<div class="ent">' + (d.url ? '<a href="' + esc(d.url) + '" target="_blank" rel="noopener">' + esc(d.name) + "</a>" : esc(d.name)) + " <small>" + esc(d.orderId) + " · " + esc(dt(d.at)) + "</small></div>"; }).join("") : '<div class="empty">No documents. Add them from a shipment.</div>'; },
      update: function () {
        return '<form id="uu-form" class="frm">' +
          '<div><label>UserId</label><input value="' + u.userNo + '" disabled></div>' +
          sel("agent", "HandleByAgent", [["", "-"]].concat(staffNames.map(function (s) { return [s.uid, s.name + (s.active ? "" : " (inactive)")]; })), u.handleByAgent || "") + fld("affid", "AffiliateId", u.affiliateId) +
          fld("fn", "First name", u.firstName) + fld("ln", "Last name", u.lastName) +
          '<div><label>Email</label><input value="' + esc(u.email) + '" disabled></div>' +
          fld("company", "Company", u.company) + fld("country", "Country", u.country) + fld("city", "City", u.city) +
          fld("address", "Address", u.address) + fld("zip", "Zip", u.zip) + fld("commission", "Commission", u.commission) +
          fld("permission", "Permission", u.permission) + fld("brand", "Brand", u.brand) + fld("discount", "Discount (%)", u.discountPct, "number") +
          fld("ph", "Phone", u.phone) + sel("isact", "IsActive", [["yes", "Yes"], ["no", "No"]], u.isActive || "yes") +
          sel("use", "Account type", [["private", "Private"], ["business", "Business"]], u.useFor || "private") + fld("utype", "UserType", u.userType) +
          fld("social", "SocialMediaShare", u.socialMediaShare) + fld("couriers", "Couriers", u.couriers) + fld("poa", "PowerOfAttorney", u.powerOfAttorney) +
          fld("debt", "DebtAmountLimit", u.debtAmountLimit, "number") + fld("lang", "DefaultLang", u.defaultLang) + fld("accmail", "AccountingEmail", u.accountingEmail) +
          fld("sdr", "SdrAgent", u.sdrAgent) + fld("rettime", "UserReturnTime", u.userReturnTime) +
          (admin ? '<label class="sw wf"><input type="checkbox" id="p-bl"' + (u.blocked ? " checked" : "") + "><span>Blocked (marker for staff)</span></label>" : "") +
          '<div><button type="submit" class="pri">Save</button></div><div><button type="button" id="uu-clear">Clear</button></div></form><div id="uu-msg" hidden></div>';
      },
    };
    var logRows = r.log.map(function (l, i) { return "<tr><td><b>" + u.userNo + "." + (i + 1) + "</b></td><td>" + esc(l.orderId || "-") + "</td><td>" + esc(l.by) + "</td><td>" + esc(l.type || "-") + "</td><td>" + esc(l.text) + "</td><td>" + esc(dt(l.at)) + "</td></tr>"; }).join("");
    box.innerHTML = '<div class="card"><div class="sh-head"><h2>#' + u.userNo + " " + esc([u.firstName, u.lastName].join(" ").trim() || u.email) + (u.blocked ? ' <span class="bchip c-cancelled">Blocked</span>' : "") + '</h2><span><small class="mut">User_id: ' + u.userNo + ' &nbsp; mail: ' + esc(u.email) + '</small> ' + (admin ? '<button type="button" id="u-imp">Log in as this customer</button> ' : "") + (u.email ? '<button type="button" id="u-reset">Send password reset link</button> ' : "") + '<a href="#users">‹ Back to users</a></span></div><div id="uh-msg" hidden></div><div class="three"><dl class="kv"><dt>Email</dt><dd>' + esc(u.email) + "</dd><dt>Phone</dt><dd>" + esc(u.phone) + '</dd></dl><dl class="kv"><dt>Type</dt><dd>' + esc(u.useFor) + "</dd><dt>Joined</dt><dd>" + esc(d10(u.createdAt)) + '</dd></dl><dl class="kv"><dt>Balance</dt><dd class="' + (r.balance > 0 ? "neg" : "") + '">' + money(r.balance) + "</dd><dt>Orders</dt><dd>" + r.orders.length + "</dd><dt>Coupon</dt><dd>" + (r.coupon ? '<span class="bchip c-paid">' + esc(r.coupon.code) + " (" + r.coupon.pct + "%)</span>" : '<span class="mut">None</span>') + "</dd></dl></div>" +
      '<div class="wf" style="margin-top:12px"><label for="p-ud">User description</label><textarea id="p-ud">' + esc(u.description) + '</textarea></div><div><button type="button" class="pri" id="ud-go">Save</button></div><div id="ud-msg" hidden></div>' +
      '</div><div class="card"><h3>Log</h3><div class="tw" style="max-height:220px;overflow-y:auto"><table class="t"><thead><tr><th>LogId</th><th>pickupId</th><th>agent</th><th>action</th><th>log</th><th>iTime</th></tr></thead><tbody>' + (logRows || '<tr><td colspan="6" class="empty">No log entries.</td></tr>') + '</tbody></table></div><p style="margin:8px 0 0"><a href="#" id="u-logadd">Add</a></p></div>' +
      '<div class="card"><div class="tabs" id="u-tabs">' + UTABS.map(function (t) { return '<button type="button" data-t="' + t[0] + '" class="' + (t[0] === tab ? "on" : "") + '">' + t[1] + "</button>"; }).join("") + '</div><div id="u-body">' + body[tab]() + "</div></div>";
    var ub = $("u-body");
    var imp = $("u-imp");
    if (imp) imp.addEventListener("click", async function () {
      if (!confirm("Open the site signed in as " + (u.firstName || u.email) + "? This is logged on their account.")) return;
      imp.disabled = true; say("uh-msg", "");
      var x = await CT.api("POST", "/admin/user/impersonate", { uid: uid });
      imp.disabled = false;
      if (!x.ok) return say("uh-msg", errOf(x), true);
      window.open(SITE_URL + "/?as=" + encodeURIComponent(x.token), "_blank", "noopener");
    });
    var rst = $("u-reset");
    if (rst) rst.addEventListener("click", async function () {
      if (!confirm("Send a password reset link to " + u.email + "?")) return;
      rst.disabled = true; say("uh-msg", "");
      try { await CT.init(); await CT.reset(u.email); await CT.api("POST", "/admin/user/reset_password_log", { uid: uid }); say("uh-msg", "Reset link sent to " + u.email + "."); }
      catch (e) { say("uh-msg", CT.errText(e), true); }
      rst.disabled = false;
    });
    var udGo = $("ud-go"); if (udGo) udGo.addEventListener("click", async function () { var x = await CT.api("POST", "/admin/user/update", { uid: uid, description: $("p-ud").value }); if (!x.ok) return say("ud-msg", errOf(x), true); say("ud-msg", "Saved."); });
    var la = $("u-logadd"); if (la) la.addEventListener("click", async function (e) { e.preventDefault(); var t = prompt("Log entry"); if (!t) return; var x = await CT.api("POST", "/admin/user/log/add", { uid: uid, text: t }); if (!x.ok) return say("uh-msg", errOf(x), true); userPage(uid); });
    box.querySelectorAll("#u-tabs button").forEach(function (b) { b.addEventListener("click", function () { state.tab = b.getAttribute("data-t"); userPage(uid); }); });
    ub.querySelectorAll("[data-o]").forEach(function (tr) { tr.addEventListener("click", function () { openShip(tr.getAttribute("data-o")); }); });
    ub.querySelectorAll("[data-rc]").forEach(function (b) { b.addEventListener("click", function () { var rc = r.receipts.filter(function (x) { return x.id === b.getAttribute("data-rc"); })[0]; if (rc) printReceipt(rc, [u.firstName, u.lastName].join(" ")); }); });
    var lg = $("le-go"); if (lg) lg.addEventListener("click", async function () { var x = await CT.api("POST", "/admin/ledger/add", { uid: uid, kind: $("le-k").value, amount: $("le-a").value, method: $("le-m").value, note: $("le-n").value }); if (!x.ok) return say("le-msg", errOf(x), true); state.tab = "accounting"; userPage(uid); });
    var uf = $("uu-form");
    if (uf) {
      uf.addEventListener("submit", async function (e) {
        e.preventDefault();
        var b = {
          uid: uid, firstName: pv("fn"), lastName: pv("ln"), phone: pv("ph"), useFor: pv("use"), userType: pv("utype"), isActive: pv("isact"),
          company: pv("company"), country: pv("country"), city: pv("city"), address: pv("address"), zip: pv("zip"), commission: pv("commission"),
          permission: pv("permission"), brand: pv("brand"), discountPct: pv("discount") || null, socialMediaShare: pv("social"), couriers: pv("couriers"),
          powerOfAttorney: pv("poa"), debtAmountLimit: pv("debt") || null, defaultLang: pv("lang"), accountingEmail: pv("accmail"), sdrAgent: pv("sdr"),
          userReturnTime: pv("rettime"), handleByAgent: pv("agent"), affiliateId: pv("affid"),
        };
        if ($("p-bl")) b.blocked = $("p-bl").checked;
        var x = await CT.api("POST", "/admin/user/update", b); if (!x.ok) return say("uu-msg", errOf(x), true); await userPage(uid); say("uu-msg", "Saved.");
      });
      var cl = $("uu-clear"); if (cl) cl.addEventListener("click", function () { uf.reset(); });
    }
  }

  /* ---------- agents ---------- */
  async function agentsPage() {
    var box = $("bx-view"), admin = me.role === "admin";
    var r = await CT.api("GET", "/admin/list?m=agents"); agentsCache = r.ok ? r.rows : [];
    box.innerHTML = (admin ? '<div class="card"><h2 id="ag-h">Add agent</h2><form class="frm" id="ag-form"><input type="hidden" id="ag-id">' + fld("name", "Name", "") + sel("kind", "Kind", [["agent", "Agent"], ["carrier", "Carrier"], ["other", "Other"]], "agent") + fld("email", "Email", "", "email") + fld("phone", "Phone", "") + fld("country", "Country (2 letters)", "") + fld("notes", "Notes", "", "text", "w2") + '<div class="btns" style="display:flex;gap:8px"><button type="submit" class="pri">Save</button><button type="button" id="ag-new">New</button></div></form><div id="ag-msg" hidden></div></div>' : "") +
      '<div class="tw"><table class="t"><thead><tr><th>Name</th><th>Kind</th><th>Email</th><th>Phone</th><th>Country</th><th>Notes</th><th></th></tr></thead><tbody>' + (agentsCache.length ? agentsCache.map(function (a) { return "<tr><td><b>" + esc(a.name) + "</b></td><td>" + esc(a.kind) + "</td><td>" + esc(a.email) + "</td><td>" + esc(a.phone) + "</td><td>" + esc(String(a.country || "").toUpperCase()) + "</td><td>" + esc(a.notes) + "</td><td>" + (admin ? '<button type="button" data-e="' + esc(a.id) + '">Edit</button> <button type="button" class="dng" data-d="' + esc(a.id) + '">Delete</button>' : "") + "</td></tr>"; }).join("") : '<tr><td colspan="7" class="empty">No agents yet.</td></tr>') + "</tbody></table></div>";
    if (!admin) return;
    $("ag-new").addEventListener("click", function () { $("ag-form").reset(); $("ag-id").value = ""; $("ag-h").textContent = "Add agent"; });
    box.querySelectorAll("[data-e]").forEach(function (b) { b.addEventListener("click", function () { var a = agentsCache.filter(function (x) { return x.id === b.getAttribute("data-e"); })[0]; $("ag-id").value = a.id; ["name", "email", "phone", "country", "notes"].forEach(function (k) { $("p-" + k).value = a[k] || ""; }); $("p-kind").value = a.kind || "agent"; $("ag-h").textContent = "Edit agent"; window.scrollTo(0, 0); }); });
    box.querySelectorAll("[data-d]").forEach(function (b) { b.addEventListener("click", async function () { if (!confirm("Delete this agent?")) return; await CT.api("POST", "/admin/agent/delete", { id: b.getAttribute("data-d") }); agentsPage(); }); });
    $("ag-form").addEventListener("submit", async function (e) { e.preventDefault(); var x = await CT.api("POST", "/admin/agent/save", { id: $("ag-id").value, name: pv("name"), kind: pv("kind"), email: pv("email"), phone: pv("phone"), country: pv("country"), notes: pv("notes") }); if (!x.ok) return say("ag-msg", errOf(x), true); agentsPage(); });
  }

  /* ---------- staff ---------- */
  async function staffPage() {
    var box = $("bx-view"); var r = await CT.api("GET", "/admin/staff"); if (!r.ok) { box.innerHTML = '<div class="card">Admins only.</div>'; return; }
    box.innerHTML = '<div class="tw"><table class="t"><thead><tr><th>Name</th><th>Email</th><th>Role</th><th>Status</th><th>Personal code</th><th></th></tr></thead><tbody id="s-body"></tbody></table></div><div class="card" style="margin-top:14px"><h2>Add employee</h2><form class="frm" id="s-form" autocomplete="off">' + fld("name", "Name", "") + fld("mail", "Email", "", "email") + fld("pw", "Temporary password (8+ chars)", "", "password") + sel("role", "Role", [["staff", "Staff"], ["admin", "Admin"]], "staff") + '<div><button type="submit" class="pri">Add</button></div></form><div id="s-err" hidden></div><p class="mut">Give the employee the temporary password. Each employee creates a personal price code with My personal code; the code is never visible to the admin.</p></div>';
    var b = $("s-body");
    r.staff.forEach(function (s) {
      var tr = document.createElement("tr");
      tr.innerHTML = "<td>" + esc(s.name) + "</td><td>" + esc(s.email) + "</td><td>" + (s.role === "admin" ? "Admin" : "Staff") + "</td><td>" + chip(s.active ? "done" : "cancelled").replace(/Done|done|cancelled/, s.active ? "Active" : "Disabled") + "</td><td>" + (s.hasCode ? "Yes" : "No") + '</td><td class="acts"></td>';
      var td = tr.lastChild, add = function (t, f) { var x = document.createElement("button"); x.type = "button"; x.textContent = t; x.addEventListener("click", async function () { var res = await f(); if (res && res.ok === false) return say("s-err", errOf(res), true); staffPage(); }); td.appendChild(x); };
      if (s.uid !== me.uid) add(s.active ? "Disable" : "Enable", function () { return CT.api("POST", "/admin/staff/update", { uid: s.uid, active: !s.active }); });
      if (s.hasCode) add("Revoke code", function () { return CT.api("POST", "/admin/code/revoke", { uid: s.uid }); });
      if (s.uid !== me.uid) add(s.role === "admin" ? "Make staff" : "Make admin", function () { return CT.api("POST", "/admin/staff/update", { uid: s.uid, role: s.role === "admin" ? "staff" : "admin" }); });
      if (s.uid !== me.uid) add("Force sign out", function () { if (!confirm("Sign " + s.name + " out of every device? They'll need to sign in again.")) return Promise.resolve({ ok: true }); return CT.api("POST", "/admin/staff/signout", { uid: s.uid }); });
      b.appendChild(tr);
    });
    $("s-form").addEventListener("submit", async function (e) { e.preventDefault(); var x = await CT.api("POST", "/admin/staff/create", { name: pv("name"), email: pv("mail"), password: pv("pw"), role: pv("role") }); if (!x.ok) return say("s-err", errOf(x), true); staffPage(); });
  }

  /* ---------- finance ---------- */
  var FIN_PRESETS = [["7", "Last 7 days"], ["30", "Last 30 days"], ["90", "Last 90 days"], ["365", "Last 12 months"]];
  function finRange(days) {
    var to = new Date(), from = new Date(); from.setDate(from.getDate() - Number(days));
    var f = function (d) { return d.toISOString().slice(0, 10); };
    return { from: f(from), to: f(to) };
  }
  /* one rounded end, square at the baseline: top=true rounds the two top corners (upward bar), top=false rounds the two bottom corners (downward bar) */
  function barPath(x, y, w, h, r, top) {
    if (h <= 0.5) return "";
    r = Math.min(r, w / 2, h);
    if (top) return "M" + x + "," + (y + h) + "V" + (y + r) + "Q" + x + "," + y + " " + (x + r) + "," + y + "H" + (x + w - r) + "Q" + (x + w) + "," + y + " " + (x + w) + "," + (y + r) + "V" + (y + h) + "Z";
    return "M" + x + "," + y + "H" + (x + w) + "V" + (y + h - r) + "Q" + (x + w) + "," + (y + h) + " " + (x + w - r) + "," + (y + h) + "H" + (x + r) + "Q" + x + "," + (y + h) + " " + x + "," + (y + h - r) + "Z";
  }
  /* a small hand-rolled SVG bar chart: one series per chart (title names it, no legend needed), optionally diverging around a zero baseline */
  function barChart(rows, key, opts) {
    opts = opts || {};
    var W = 760, H = 150, padL = 56, padR = 10, padT = 10, padB = 20, innerW = W - padL - padR, innerH = H - padT - padB;
    var vals = rows.map(function (r) { return r[key]; });
    var gap = 2, slot = innerW / Math.max(1, rows.length), barW = Math.max(2, Math.min(24, slot - gap));
    var svg = '<svg viewBox="0 0 ' + W + ' ' + H + '" style="width:100%;height:' + H + 'px" role="img" aria-label="' + esc(opts.label || key) + ' by period">';
    var axisColor = "#c3c2b7", gridColor = "#e1e0d9", textColor = "#898781";
    if (opts.diverging) {
      var maxAbs = Math.max(1, vals.reduce(function (a, v) { return Math.max(a, Math.abs(v)); }, 0));
      var zeroY = padT + innerH / 2;
      svg += '<line x1="' + padL + '" y1="' + zeroY + '" x2="' + (W - padR) + '" y2="' + zeroY + '" stroke="' + axisColor + '" stroke-width="1"/>';
      [1, 0.5].forEach(function (f) {
        var y1 = zeroY - f * (innerH / 2), y2 = zeroY + f * (innerH / 2);
        svg += '<line x1="' + padL + '" y1="' + y1 + '" x2="' + (W - padR) + '" y2="' + y1 + '" stroke="' + gridColor + '" stroke-width="1"/>';
        svg += '<line x1="' + padL + '" y1="' + y2 + '" x2="' + (W - padR) + '" y2="' + y2 + '" stroke="' + gridColor + '" stroke-width="1"/>';
        svg += '<text x="' + (padL - 6) + '" y="' + (y1 + 3) + '" text-anchor="end" font-size="10" fill="' + textColor + '">' + money(f * maxAbs) + "</text>";
      });
      rows.forEach(function (r, i) {
        var v = r[key], x = padL + i * slot + (slot - barW) / 2, h = (Math.abs(v) / maxAbs) * (innerH / 2);
        var d = v >= 0 ? barPath(x, zeroY - h, barW, h, 4, true) : barPath(x, zeroY, barW, h, 4, false);
        if (d) svg += '<path d="' + d + '" fill="' + (v >= 0 ? opts.pos : opts.neg) + '"><title>' + esc(r.date) + ": " + money(v) + "</title></path>";
      });
    } else {
      var maxVal = Math.max(1, vals.reduce(function (a, v) { return Math.max(a, v); }, 0));
      [1, 0.5, 0].forEach(function (f) {
        var y = padT + innerH - f * innerH;
        svg += '<line x1="' + padL + '" y1="' + y + '" x2="' + (W - padR) + '" y2="' + y + '" stroke="' + (f === 0 ? axisColor : gridColor) + '" stroke-width="1"/>';
        svg += '<text x="' + (padL - 6) + '" y="' + (y + 3) + '" text-anchor="end" font-size="10" fill="' + textColor + '">' + money(f * maxVal) + "</text>";
      });
      rows.forEach(function (r, i) {
        var v = r[key], x = padL + i * slot + (slot - barW) / 2, h = (v / maxVal) * innerH, y = padT + innerH - h;
        var d = barPath(x, y, barW, h, 4, true);
        if (d) svg += '<path d="' + d + '" fill="' + opts.color + '"><title>' + esc(r.date) + ": " + money(v) + "</title></path>";
      });
    }
    svg += "</svg>";
    return svg;
  }
  async function financePage() {
    var box = $("bx-view");
    box.innerHTML = '<div class="card"><form class="flt" id="fin-f"><div><label for="fin-range">Range</label><select id="fin-range">' + FIN_PRESETS.map(function (p) { return '<option value="' + p[0] + '">' + p[1] + "</option>"; }).join("") + '</select></div><div><label for="fin-grp">Group by</label><select id="fin-grp"><option value="day">Day</option><option value="month">Month</option></select></div></form></div><div id="fin-body"><div class="empty">Loading...</div></div>';
    async function load() {
      var days = $("fin-range").value, grp = $("fin-grp").value, rng = finRange(days);
      var r = await CT.api("GET", "/admin/finance?from=" + rng.from + "&to=" + rng.to + "&group=" + grp);
      var out = $("fin-body");
      if (!r.ok) { out.innerHTML = '<div class="card">Admins only.</div>'; return; }
      var rows = r.rows, t = r.totals;
      out.innerHTML =
        '<div class="three"><div class="card"><h3>Revenue</h3><b>' + money(t.revenue) + '</b></div><div class="card"><h3>Refunds</h3><b>' + money(t.refunds) + '</b></div><div class="card"><h3>Net profit / loss</h3><b class="' + (t.profit < 0 ? "neg" : "pos") + '">' + money(t.profit) + "</b></div></div>" +
        '<div class="card"><h3>Revenue</h3>' + (rows.length ? barChart(rows, "revenue", { color: "#185b92", label: "Revenue" }) : '<div class="empty">No data in this range.</div>') + "</div>" +
        '<div class="card"><h3>Refunds</h3>' + (rows.length ? barChart(rows, "refunds", { color: "#c9701a", label: "Refunds" }) : '<div class="empty">No data in this range.</div>') + "</div>" +
        '<div class="card"><h3>Net profit / loss</h3>' + (rows.length ? barChart(rows, "profit", { diverging: true, pos: "#185b92", neg: "#c62828", label: "Profit" }) : '<div class="empty">No data in this range.</div>') + "</div>" +
        '<div class="card"><h3>By period</h3><div class="tw"><table class="t"><thead><tr><th>Date</th><th class="r">Revenue</th><th class="r">Refunds</th><th class="r">Profit / loss</th></tr></thead><tbody>' +
        (rows.length ? rows.map(function (x) { return "<tr><td>" + esc(x.date) + '</td><td class="r">' + money(x.revenue) + '</td><td class="r">' + money(x.refunds) + '</td><td class="r ' + (x.profit < 0 ? "neg" : "") + '">' + money(x.profit) + "</td></tr>"; }).join("") : '<tr><td colspan="4" class="empty">No data in this range.</td></tr>') +
        "</tbody></table></div></div>";
    }
    $("fin-f").addEventListener("change", load);
    load();
  }

  /* ---------- coupons ---------- */
  var CPST = { active: "Active", used: "Used", expired: "Expired", cancelled: "Cancelled", scheduled: "Scheduled" };
  async function couponsPage() {
    var box = $("bx-view"), admin = me.role === "admin";
    box.innerHTML =
      (admin ? '<div class="card"><h2>Create coupon</h2><form id="cp-form" class="frm">' + fld("code", "Code (leave empty to auto-generate)", "") + fld("pct", "Discount (%)", "", "number") + sel("usage", "Usage", [["once", "Once (first redeemer only)"], ["multi", "Multiple customers"]], "once") + fld("from", "Valid from", new Date().toISOString().slice(0, 10), "date") + fld("to", "Valid to", "", "date") + '<div class="wf"><label for="p-note">Note (internal)</label><input id="p-note" type="text"></div><div><button type="submit" class="pri">Create</button></div></form><div id="cp-msg" hidden></div></div>' : "") +
      '<div class="card"><form class="flt" id="cp-f"><div class="grow"><label for="f-q">Search</label><input id="f-q" type="text"></div><div><button type="submit" class="pri">Search</button></div></form></div>' +
      '<div class="tw"><table class="t"><thead><tr><th>Code</th><th>User</th><th class="r">Discount</th><th>Usage</th><th>Valid</th><th>Status</th><th>Note</th><th>By</th><th></th></tr></thead><tbody id="cp-body"></tbody></table></div>';
    async function load() {
      var q = $("f-q").value.trim();
      var r = await CT.api("GET", "/admin/list?m=coupons" + (q ? "&q=" + encodeURIComponent(q) : ""));
      var tb = $("cp-body"); tb.innerHTML = "";
      if (!r.ok || !r.rows.length) { tb.innerHTML = '<tr><td colspan="9" class="empty">No coupons yet.</td></tr>'; return; }
      r.rows.forEach(function (c) {
        var tr = document.createElement("tr");
        tr.innerHTML = "<td><b>" + esc(c.code) + "</b></td><td>" + (c.userNo ? "#" + c.userNo + " " + esc(c.userName) : '<span class="mut">Not redeemed yet</span>') + '</td><td class="r">' + c.pct + "%</td><td>" + esc(c.usageType) + "</td><td>" + esc(c.validFrom) + " → " + esc(c.validTo) + "</td><td>" + chip(c.status, CPST) + "</td><td>" + esc(c.note) + "</td><td>" + esc(c.by) + "</td><td>" + (admin ? (c.status !== "cancelled" ? '<button type="button" class="dng" data-cc="' + esc(c.id) + '">Cancel</button>' : '<button type="button" class="pri" data-cr="' + esc(c.id) + '">Reactivate</button>') : "") + "</td>";
        tb.appendChild(tr);
      });
      tb.querySelectorAll("[data-cc]").forEach(function (b) { b.addEventListener("click", async function () { if (!confirm("Cancel this coupon?")) return; var x = await CT.api("POST", "/admin/coupon/cancel", { id: b.getAttribute("data-cc") }); if (!x.ok) return alert(errOf(x)); load(); }); });
      tb.querySelectorAll("[data-cr]").forEach(function (b) { b.addEventListener("click", async function () { if (!confirm("Reactivate this coupon?")) return; var x = await CT.api("POST", "/admin/coupon/reactivate", { id: b.getAttribute("data-cr") }); if (!x.ok) return alert(errOf(x)); load(); }); });
    }
    $("cp-f").addEventListener("submit", function (e) { e.preventDefault(); load(); });
    var cf = $("cp-form");
    if (cf) cf.addEventListener("submit", async function (e) {
      e.preventDefault();
      var x = await CT.api("POST", "/admin/coupon/create", { code: pv("code"), pct: pv("pct"), usageType: pv("usage"), validFrom: pv("from"), validTo: pv("to"), note: pv("note") });
      if (!x.ok) return say("cp-msg", errOf(x), true);
      cf.reset(); say("cp-msg", "Created: " + x.coupon.code); load();
    });
    load();
  }

  /* ---------- price lists (admin only): upload a carrier's rate card as CSV (parsed in the browser, no
     server-side file handling needed). First column = weight break (kg), the rest = zone columns. ---------- */
  function parseCsv(text) {
    var lines = text.replace(/^﻿/, "").split(/\r\n|\r|\n/).filter(function (l) { return l.trim() !== ""; });
    if (!lines.length) return null;
    var headers = lines[0].split(",").map(function (h) { return h.trim(); });
    var rows = lines.slice(1).map(function (l) { return l.split(",").map(function (c) { return c.trim(); }); });
    return { headers: headers, rows: rows };
  }
  async function pricelistsPage() {
    var box = $("bx-view");
    box.innerHTML =
      '<div class="card"><h2>Upload a price list</h2><p class="mut">CSV only. First column: weight (kg). Other columns: one per zone, with the price at that weight break. Catalog groups related files together (e.g. several services from the same carrier). Uploading the same key again replaces it.</p><form id="pl-form" class="frm">' +
      fld("catalog", "Catalog (e.g. fedex_shipping)", "") + fld("key", "Key (e.g. dhl_priority)", "") + fld("label", "Label", "") + fld("csv", "CSV file", "", "file") +
      '<div><button type="submit" class="pri">Upload</button></div></form><div id="pl-msg" hidden></div></div>' +
      '<div class="tw"><table class="t"><thead><tr><th>Catalog</th><th>Label</th><th>Key</th><th class="r">Rows</th><th class="r">Columns</th><th>Source</th><th>Updated</th><th>By</th><th></th></tr></thead><tbody id="pl-body"></tbody></table></div>';
    async function load() {
      var r = await CT.api("GET", "/admin/pricelist/list");
      var tb = $("pl-body"); tb.innerHTML = "";
      if (!r.ok || !r.lists.length) { tb.innerHTML = '<tr><td colspan="9" class="empty">No price lists.</td></tr>'; return; }
      r.lists.forEach(function (l) {
        var tr = document.createElement("tr"); tr.className = "ck";
        tr.innerHTML = "<td>" + esc(l.catalog || "-") + "</td><td><b>" + esc(l.label) + "</b></td><td>" + esc(l.key) + '</td><td class="r">' + l.rowCount + '</td><td class="r">' + l.colCount + "</td><td>" + (l.builtin ? '<span class="bchip">Built-in</span>' : '<span class="bchip c-paid">Uploaded</span>') + "</td><td>" + (l.updatedAt ? esc(dt(l.updatedAt)) : "-") + "</td><td>" + esc(l.by) + "</td><td><button type=\"button\" data-pv=\"" + esc(l.key) + "\">View</button> " + (l.builtin ? "" : '<button type="button" class="dng" data-pd="' + esc(l.key) + '">Delete</button>') + "</td>";
        tr.addEventListener("click", function (e) { if (e.target.closest("button")) return; openPricelist(l.key); });
        tb.appendChild(tr);
      });
      tb.querySelectorAll("[data-pv]").forEach(function (b) { b.addEventListener("click", function (e) { e.stopPropagation(); openPricelist(b.getAttribute("data-pv")); }); });
      tb.querySelectorAll("[data-pd]").forEach(function (b) { b.addEventListener("click", async function (e) { e.stopPropagation(); if (!confirm("Delete this price list?")) return; var x = await CT.api("POST", "/admin/pricelist/delete", { key: b.getAttribute("data-pd") }); if (!x.ok) return alert(errOf(x)); load(); }); });
    }
    $("pl-form").addEventListener("submit", function (e) {
      e.preventDefault();
      var catalog = pv("catalog").trim(), key = pv("key").trim(), label = pv("label").trim(), file = $("p-csv").files[0];
      if (!key || !label) return say("pl-msg", "Key and label are required.", true);
      if (!file) return say("pl-msg", "Choose a CSV file.", true);
      var reader = new FileReader();
      reader.onload = async function () {
        var parsed = parseCsv(String(reader.result || ""));
        if (!parsed || !parsed.rows.length) return say("pl-msg", "The file has no data rows.", true);
        var x = await CT.api("POST", "/admin/pricelist/save", { catalog: catalog, key: key, label: label, headers: parsed.headers, rows: parsed.rows });
        if (!x.ok) return say("pl-msg", errOf(x), true);
        $("pl-form").reset(); say("pl-msg", "Saved: " + x.key); load();
      };
      reader.onerror = function () { say("pl-msg", "Could not read the file.", true); };
      reader.readAsText(file);
    });
    load();
  }
  async function openPricelist(key) {
    var d = $("pld"), box = $("pl-in");
    box.innerHTML = '<div class="sh-head"><h2>Loading…</h2></div>'; if (!d.open) d.showModal();
    var rr = await Promise.all([CT.api("GET", "/admin/pricelist?key=" + encodeURIComponent(key)), CT.api("GET", "/admin/settings")]);
    var r = rr[0], sr = rr[1];
    if (!r.ok) { box.innerHTML = '<div class="sh-head"><h2>Could not load.</h2><button type="button" id="pl-x2">Close</button></div>'; $("pl-x2").addEventListener("click", function () { d.close(); }); return; }
    var p = r.pricelist, s = sr.ok ? sr.settings : null;
    var rowsHtml = p.rows.map(function (row) { return "<tr>" + row.map(function (v) { return "<td class='r'>" + (v == null ? '<span class="mut">-</span>' : v) + "</td>"; }).join("") + "</tr>"; }).join("");
    box.innerHTML =
      '<div class="sh-head"><h2>' + esc(p.label) + (p.catalog ? ' <span class="bchip">' + esc(p.catalog) + "</span>" : "") + '</h2><button type="button" id="pl-x">Close window</button></div>' +
      (p.builtin ? '<p class="mut">Built-in - already wired into real customer quotes.</p>' : '<p class="mut">Uploaded - not yet wired into customer quotes (needs a code change per carrier).</p>') +
      (s ? '<p class="mut">What the customer actually pays: this price × (1 + commission% / 100). Commission right now (Settings): ' + s.markupBusinessPct + '% business, ' + s.markupPrivatePct + '% private - unless a specific shipment has its own Pricing Override.</p>' : "") +
      '<div class="tw"><table class="t"><thead><tr>' + p.headers.map(function (h) { return "<th" + (h === "kg" ? "" : ' class="r"') + ">" + esc(h) + "</th>"; }).join("") + "</tr></thead><tbody>" + rowsHtml + "</tbody></table></div>";
    $("pl-x").addEventListener("click", function () { d.close(); });
  }

  /* ---------- banners: marketing / contact banners shown on the public site (CargoTech banner script reads them). ---------- */
  var BANNER_TEMPLATES = [["center", "Center modal"], ["bottom", "Bottom bar"], ["side", "Side card"], ["full", "Full screen"]];
  var BANNER_ANIMS = [["fade-up", "Fade up"], ["scale", "Scale in"], ["slide-side", "Slide from side"]];
  var BANNER_CTA = [["none", "No button"], ["link", "Link"], ["whatsapp", "WhatsApp"], ["phone", "Phone call"], ["contact", "Open contact form"]];
  var BANNER_PAGE = [["all", "All pages"], ["home", "Homepage only"]];
  var BANNER_FREQ = [["always", "Every visit"], ["session", "Once per visit (session)"], ["once", "Once ever per visitor"]];
  async function bannersPage() {
    var box = $("bx-view"), editing = null;
    box.innerHTML =
      '<div class="card"><h2 id="bn-form-t">New banner</h2><form id="bn-form" class="frm">' +
      fld("title", "Title", "") + area("body", "Body text", "") + fld("imageUrl", "Image URL (optional)", "", "text", "w2") +
      sel("ctaType", "Button", BANNER_CTA, "none") + fld("ctaText", "Button text", "") + fld("ctaValue", "Button link / phone (not needed for \"Open contact form\")", "", "text", "w2") +
      sel("template", "Layout", BANNER_TEMPLATES, "center") + sel("anim", "Entrance animation", BANNER_ANIMS, "fade-up") +
      sel("page", "Show on", BANNER_PAGE, "all") + fld("delaySec", "Delay before showing (seconds)", 2, "number") +
      sel("frequency", "Show again", BANNER_FREQ, "always") + fld("activeFrom", "Active from (optional)", "", "date") + fld("activeTo", "Active to (optional)", "", "date") +
      '<label class="sw"><input type="checkbox" id="p-enabled" checked><span>Enabled</span></label>' +
      '<div><button type="submit" class="pri" id="bn-save">Create banner</button> <button type="button" id="bn-cancel" hidden>Cancel edit</button></div></form><div id="bn-msg" hidden></div></div>' +
      '<div class="tw"><table class="t"><thead><tr><th>Title</th><th>Layout</th><th>Show on</th><th>Active</th><th class="r">Shows</th><th class="r">Clicks</th><th class="r">Dismissed</th><th></th></tr></thead><tbody id="bn-body"></tbody></table></div>';
    function resetForm() {
      editing = null; $("bn-form").reset(); $("p-enabled").checked = true; $("bn-form-t").textContent = "New banner"; $("bn-save").textContent = "Create banner"; $("bn-cancel").hidden = true;
    }
    async function load() {
      var r = await CT.api("GET", "/admin/banner/list");
      var tb = $("bn-body"); tb.innerHTML = "";
      if (!r.ok || !r.banners.length) { tb.innerHTML = '<tr><td colspan="8" class="empty">No banners yet.</td></tr>'; return; }
      r.banners.forEach(function (p) {
        var active = p.enabled ? (p.activeFrom || p.activeTo ? '<span class="bchip c-paid">' + esc(p.activeFrom || "…") + " → " + esc(p.activeTo || "…") + "</span>" : '<span class="bchip c-paid">On</span>') : '<span class="bchip">Off</span>';
        var tr = document.createElement("tr");
        tr.innerHTML = "<td><b>" + esc(p.title) + "</b></td><td>" + esc((BANNER_TEMPLATES.find(function (t) { return t[0] === p.template; }) || [])[1] || p.template) + "</td><td>" + esc((BANNER_PAGE.find(function (t) { return t[0] === p.page; }) || [])[1] || p.page) + "</td><td>" + active + '</td><td class="r">' + p.shows + '</td><td class="r">' + p.clicks + '</td><td class="r">' + p.dismisses + '</td><td><button type="button" data-be="' + esc(p.id) + '">Edit</button> <button type="button" class="dng" data-bdel="' + esc(p.id) + '">Delete</button></td>';
        tb.appendChild(tr);
      });
      tb.querySelectorAll("[data-be]").forEach(function (b) { b.addEventListener("click", function () { var p = r.banners.find(function (x) { return x.id === b.getAttribute("data-be"); }); if (p) startEdit(p); }); });
      tb.querySelectorAll("[data-bdel]").forEach(function (b) { b.addEventListener("click", async function () { if (!confirm("Delete this banner?")) return; var x = await CT.api("POST", "/admin/banner/delete", { id: b.getAttribute("data-bdel") }); if (!x.ok) return alert(errOf(x)); if (editing === b.getAttribute("data-bdel")) resetForm(); load(); }); });
    }
    function startEdit(p) {
      editing = p.id;
      $("p-title").value = p.title; $("p-body").value = p.body || ""; $("p-imageUrl").value = p.imageUrl || "";
      $("p-ctaType").value = p.ctaType || "none"; $("p-ctaText").value = p.ctaText || ""; $("p-ctaValue").value = p.ctaValue || "";
      $("p-template").value = p.template; $("p-anim").value = p.anim; $("p-page").value = p.page; $("p-delaySec").value = p.delaySec || 0;
      $("p-frequency").value = p.frequency || "always"; $("p-activeFrom").value = p.activeFrom || ""; $("p-activeTo").value = p.activeTo || ""; $("p-enabled").checked = p.enabled !== false;
      $("bn-form-t").textContent = "Editing: " + p.title; $("bn-save").textContent = "Save changes"; $("bn-cancel").hidden = false;
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
    $("bn-cancel").addEventListener("click", resetForm);
    $("bn-form").addEventListener("submit", async function (e) {
      e.preventDefault();
      var title = pv("title").trim(); if (!title) return say("bn-msg", "Title is required.", true);
      var body = { id: editing, title: title, body: pv("body"), imageUrl: pv("imageUrl"), ctaType: pv("ctaType"), ctaText: pv("ctaText"), ctaValue: pv("ctaValue"), template: pv("template"), anim: pv("anim"), page: pv("page"), delaySec: pv("delaySec"), frequency: pv("frequency"), activeFrom: pv("activeFrom"), activeTo: pv("activeTo"), enabled: $("p-enabled").checked };
      var x = await CT.api("POST", "/admin/banner/save", body);
      if (!x.ok) return say("bn-msg", errOf(x), true);
      say("bn-msg", "Saved."); resetForm(); load();
    });
    load();
  }

  /* ---------- settings ---------- */
  async function settingsPage() {
    var box = $("bx-view"); var r = await CT.api("GET", "/admin/settings"); if (!r.ok) { box.innerHTML = '<div class="card">Admins only.</div>'; return; } var s = r.settings;
    var sw = function (id, on, t) { return '<label class="sw"><input type="checkbox" id="g-' + id + '"' + (on ? " checked" : "") + "><span>" + t + "</span></label>"; };
    box.innerHTML = '<form id="g-form"><div class="card"><h2>Pricing</h2><p class="mut">Example: carrier price 50. With 110% markup the customer pays 105; with 210% they pay 155.</p><div class="frm">' + fld("b", "Business markup (%)", s.markupBusinessPct, "number") + fld("p", "Private markup (%)", s.markupPrivatePct, "number") + fld("f", "Signature fee (USD)", s.signatureFeeUsd, "number") + fld("r", "USD to ILS rate", s.usdIls, "number") + "</div>" + sw("ms", s.markupOnSurcharges, "Markup also applies to carrier surcharges (e.g. remote area)") + sw("mg", s.markupOnSignature, "Markup also applies to the signature fee") + '</div><div class="card"><h2>Security and system mode</h2>' + sw("rl", s.requireStaffLogin, "A staff code works only while that employee is signed in (recommended)") + sw("tm", s.testMode, "Test mode: sample prices instead of real carrier prices. Turn off when a carrier is connected") + '</div><div id="g-err" hidden></div><button type="submit" class="pri">Save settings</button></form>';
    $("g-form").addEventListener("submit", async function (e) { e.preventDefault(); var x = await CT.api("POST", "/admin/settings", { markupBusinessPct: +pv("b"), markupPrivatePct: +pv("p"), signatureFeeUsd: +pv("f"), usdIls: +pv("r"), markupOnSurcharges: $("g-ms").checked, markupOnSignature: $("g-mg").checked, requireStaffLogin: $("g-rl").checked, testMode: $("g-tm").checked }); say("g-err", x.ok ? "Saved." : errOf(x), !x.ok); });
  }

  /* ---------- personal code: shown once, never stored ---------- */
  $("bx-code").addEventListener("click", function () {
    $("cd-code").hidden = true; $("cd-val").textContent = "";
    $("cd-t").textContent = "Your personal code lets you set a manual price on the coupon line of an order, only while you are signed in. It is shown once and is not stored, so copy it to a safe place. Creating a new code cancels the old one.";
    $("cd-make").textContent = me.hasCode ? "Create a new code (replaces the old one)" : "Create code"; $("codd").showModal();
  });
  $("cd-x").addEventListener("click", function () { $("cd-val").textContent = ""; $("codd").close(); });
  $("cd-make").addEventListener("click", async function () { var r = await CT.api("POST", "/admin/code/generate"); if (!r.ok) { $("cd-t").textContent = "Could not create the code. Try again."; return; } $("cd-val").textContent = r.code; $("cd-code").hidden = false; me.hasCode = true; });
  $("cd-copy").addEventListener("click", function () { try { navigator.clipboard.writeText($("cd-val").textContent); this.textContent = "Copied"; } catch (e) {} });
  $("codd").addEventListener("close", function () { $("cd-val").textContent = ""; });
})();
"""
