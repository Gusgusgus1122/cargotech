#!/bin/bash
# Publishes the back office to its own LIVE address (public-admin). The public site is not touched.
set -e
cd "$(dirname "$0")"
bash make-admin-config.sh
read -p "לפרסם את הבק-אופיס לכתובת שלו? (y/n) " a
[ "$a" = "y" ] || exit 0
npx --yes firebase-tools deploy --project weclean-62fce --config firebase.admin.json --only hosting
