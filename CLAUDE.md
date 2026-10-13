# CargoTech project (read this first)

Owner: Nofar (he/him). ALWAYS reply to him in Hebrew only: clean Hebrew, masculine forms, plain non-programmer explanations,
no quotation marks around English translations, do everything he asks in full (ask if unclear),
and end every reply with a checklist: one line per requested item, yes/no.
He runs scripts himself in the terminal. Design changes stay in draft/preview until he approves. Never deploy to live without his explicit yes.

Labeling rule: every time a fix is made to the public site, write the word web in the report; every time a fix is made to the back office, write the word בק (a fix to both gets both words).

## Structure
- site-source/  Python generator. `./site-source/build.sh` rebuilds public-draft (site, Hebrew RTL) and public-admin (back office, English LTR).
  - build.py (public site + page assembly), bo2.py (back-office UI: HTML/CSS/JS), authkit.py (login dialog), orderflow.py (order page),
    backoffice.py (customer account page), wizard.py, datatool.py, skin.css, content/ (article texts).
- functions/  Firebase Cloud Functions (Node). lib/api.js (customer + admin routes), lib/backoffice.js (back-office routes),
  lib/pricing.js, lib/providers.js (carrier test provider + real FedEx provider), lib/fedexRates.js (FedEx's own rate cards - carrier cost, pre-markup;
  >68kg a parcel becomes freight and uses the Freight tables instead), lib/store.js (Firestore / memory), test/run.js (`node test/run.js` must print ALL TESTS PASSED).
- public-draft/, public-admin/  built output. public/ = what is live.
- Scripts: deploy-functions.sh, preview.sh, preview-admin.sh, go-live.sh, go-live-admin.sh, setup-admin-site.sh.
- ARCHITECTURE.md  two servers (api for customers, adminapi for back office), one Firestore. Servers never call each other.

## Rules that must never break
- A staff price code is never stored or logged (only a keyed fingerprint). Prices are recomputed on the server.
- Cost and profit are visible to admins only. Money entries (deposit, add money, charge, refund) are admin-only.
- Firestore is closed to browsers (Admin SDK only).
- Business price = carrier price +110%, private +210% (editable in back-office Settings).

## Still open
Contact details (phone/WhatsApp/email) are placeholders; usdIls rate placeholder 3.6;
real FedEx pickup scheduling (Ship pricing is live as of 2026-10-11 - real FedEx price lists wired in as carrier cost,
testMode must be off in Settings for customers to see it instead of the sample test prices);
real e-mail sending (now queued in Outbox); card payments (manual ledger now); domain/sitemap/GA4; skipped back-office modules
(Orders2, SEO, Referrals, Ship Templates, phones, OutBounds, E-Shop, Chat).
