#!/usr/bin/env bash
# One-command deploy. Run from this folder:  bash deploy.sh
set -e
cd "$(dirname "$0")"
PROJECT="weclean-62fce"
SITE="cargotech-site"
command -v node >/dev/null || { echo "Node.js is not installed. Install it from https://nodejs.org and run again."; exit 1; }
FB="npx --yes firebase-tools"
echo "1/5 login (a browser window opens)"; $FB login
echo "2/5 installing functions dependencies"; (cd functions && npm install --omit=dev --no-audit --no-fund)
echo "3/5 creating the hosting site $SITE (ignored if it already exists)"; $FB hosting:sites:create "$SITE" --project "$PROJECT" || true
echo "4/5 creating the Firestore database if missing (ignored if it already exists)"; $FB firestore:databases:create "(default)" --location=eur3 --project "$PROJECT" || true
echo "5/5 deploying"; $FB deploy --project "$PROJECT" --only hosting,functions,firestore
echo "Done: https://$SITE.web.app"
