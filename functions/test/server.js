"use strict";
/* Local preview/test server: serves a built site folder and runs the same API code with an in-memory database.
   Usage: node test/server.js <siteDir> <port>      (never used in production) */
const http = require("http"), fs = require("fs"), path = require("path"), url = require("url");
const { createApi } = require("../lib/api");
const { memoryStore } = require("../lib/store");
const root = path.resolve(process.argv[2] || "."), port = +process.argv[3] || 8099;
const adminRoot = process.argv[4] ? path.resolve(process.argv[4]) : null, adminPort = +process.argv[5] || 0;   /* optional second server = the separate back-office site */
const users = {
  owner: { uid: "u-owner", email: "owner@example.com", emailVerified: true },
  emp: { uid: "u-emp", email: "emp@example.com", emailVerified: true },
  cust: { uid: "u-cust", email: "c@example.com", emailVerified: true },
};
const store = memoryStore();
const mk = (scope) => createApi({
  store, scope, ownerEmail: () => "owner@example.com",
  verifyIdToken: async (t) => { const u = users[String(t).replace("test:", "")]; if (!u) throw new Error("bad"); return u; },
  createAuthUser: async ({ email }) => (users[String(email).split("@")[0]] || { uid: "u-new" + Math.random().toString(36).slice(2, 7) }).uid,
});
const types = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".css": "text/css", ".json": "application/json", ".txt": "text/plain" };
const apiPublic = mk(adminRoot ? "public" : "all"), apiAdmin = adminRoot ? mk("admin") : null;
const serve = (root, port, api) => http.createServer((req, res) => {
  const u = url.parse(req.url, true);
  if (u.pathname.startsWith("/api/v1/")) {
    let body = ""; req.on("data", (c) => { body += c; });
    req.on("end", async () => {
      let parsed = {}; try { parsed = body ? JSON.parse(body) : {}; } catch (e) {}
      const r = { method: req.method, path: u.pathname, headers: req.headers, query: u.query, body: parsed, ip: "127.0.0.1" };
      const out = { set(k, v) { res.setHeader(k, v); }, status(s) { res.statusCode = s; return this; }, json(p) { res.setHeader("Content-Type", "application/json"); res.end(JSON.stringify(p)); } };
      await api(r, out);
    });
    return;
  }
  let p = path.join(root, u.pathname === "/" ? "index.html" : u.pathname);
  if (!p.startsWith(root) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.statusCode = 404; return res.end("not found"); }
  res.setHeader("Content-Type", types[path.extname(p)] || "application/octet-stream"); fs.createReadStream(p).pipe(res);
}).listen(port, () => console.log("listening " + port));
serve(root, port, apiPublic);
if (adminRoot) serve(adminRoot, adminPort, apiAdmin);
