#!/bin/bash
# One-time: creates the SEPARATE address for the back office (a second Firebase Hosting site in the same project).
# Safe to run again. Does not touch the public site.
set -e
cd "$(dirname "$0")"
PROJECT=weclean-62fce
current=$(cat admin-site.txt 2>/dev/null || echo "cargotech-admin")
read -p "שם הכתובת של הבק-אופיס [$current] (יהיה: שם.web.app): " id
id=${id:-$current}
if npx --yes firebase-tools hosting:sites:create "$id" --project $PROJECT; then
  echo "האתר $id נוצר."
else
  echo "אם ההודעה למעלה אומרת שהאתר כבר קיים אצלך, הכול בסדר. אם הוא תפוס אצל מישהו אחר, הריצו שוב ובחרו שם אחר."
fi
echo "$id" > admin-site.txt
bash "$(dirname "$0")/make-admin-config.sh"
echo ""
echo "הכתובת של הבק-אופיס: https://$id.web.app"
echo "חשוב: בקונסולת Firebase, בחלק Authentication > Settings > Authorized domains, לוודא שהכתובת $id.web.app מופיעה (אם לא, להוסיף)."
