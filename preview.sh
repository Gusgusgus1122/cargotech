#!/bin/bash
# Uploads the DRAFT design (public-draft) to a temporary preview link. The live site is not touched.
set -e
cd "$(dirname "$0")"
npx --yes firebase-tools hosting:channel:deploy draft --config firebase.preview.json --project weclean-62fce --expires 7d
