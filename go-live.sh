#!/bin/bash
# Publishes the approved draft to the LIVE site: copies public-draft over public, then deploys hosting only.
set -e
cd "$(dirname "$0")"
read -p "לפרסם את הטיוטה לאתר החי? (y/n) " a
[ "$a" = "y" ] || exit 0
rm -rf public && cp -R public-draft public && rm -f public/admin.html
npx --yes firebase-tools deploy --project weclean-62fce --only hosting
