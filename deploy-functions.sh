#!/bin/bash
# Updates ONLY the server functions (data proxy, leads, orders, back office API). Does not touch the live site pages.
set -e
cd "$(dirname "$0")"
if [ ! -f functions/.env ]; then
  echo "הגדרה חד פעמית: כתובת המייל של המנהל (שמתחברים איתה לבק-אופיס ונהיים מנהל ראשי)."
  read -p "מייל המנהל (Google): " owner
  echo "OWNER_EMAIL=$owner" > functions/.env
fi
(cd functions && npm install --omit=dev)
npx --yes firebase-tools deploy --project weclean-62fce --only functions
