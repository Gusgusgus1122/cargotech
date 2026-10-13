#!/bin/bash
# Writes firebase.admin.json for the back-office site, using the site name saved in admin-site.txt.
cd "$(dirname "$0")"
id=$(cat admin-site.txt 2>/dev/null || echo "cargotech-admin")
cat > firebase.admin.json <<EOF
{
  "hosting": {
    "site": "$id",
    "public": "public-admin",
    "ignore": ["firebase.json", "**/.*", "**/node_modules/**"],
    "headers": [
      {
        "source": "**",
        "headers": [
          { "key": "X-Frame-Options", "value": "DENY" },
          { "key": "X-Robots-Tag", "value": "noindex, nofollow" },
          { "key": "Referrer-Policy", "value": "no-referrer" },
          { "key": "X-Content-Type-Options", "value": "nosniff" },
          { "key": "Cache-Control", "value": "no-store" }
        ]
      }
    ],
    "rewrites": [
      { "source": "/api/v1/**", "function": { "functionId": "adminapi", "region": "europe-west1" } }
    ]
  }
}
EOF
