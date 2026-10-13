#!/bin/bash
# Uploads the DRAFT back office to a temporary preview link on the back-office address. The live back office is not touched.
set -e
cd "$(dirname "$0")"
bash make-admin-config.sh
npx --yes firebase-tools hosting:channel:deploy draft --config firebase.admin.json --project weclean-62fce --expires 7d
