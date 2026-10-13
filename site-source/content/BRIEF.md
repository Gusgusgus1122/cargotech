# Brief: Hebrew SEO articles for CargoTech (international shipping, import/export, Israel)

Brand voice: plain Hebrew ("המילים קשות, הדרך פשוטה, הכל אפשרי"). Every hard term (Incoterms, HS Code, AWB, FCL...) is explained in one simple sentence the first time it appears. Masculine plural/neutral address ("אתם"). Short sentences. No fluff, no hype, no emojis. Clean, correct Hebrew only (no mixed-up characters). Latin terms may appear inside Hebrew text (e.g. DHL, FDA).

Accuracy rules (important, this is a real business site):
- Write only what is stable general knowledge. Do NOT invent or state exact tariff rates, VAT percentages, fees, de-minimis value thresholds, transit days, prices or regulation dates. When a number would normally go there, say it changes and tell the reader to verify with the authority (רשות המסים / מכס, the destination customs, FDA, the courier) or that CargoTech checks it per shipment.
- Stable facts are fine (for example: FDA Prior Notice is required for food shipped to the US; EU shipments need customs declarations from non-EU countries; volumetric weight exists; lithium batteries are dangerous goods with carrier rules).
- Do not claim CargoTech has offices/licences/partners that are not given. You may say "הצוות שלנו" / "נבדוק מול הצוות המקומי ביעד".
- No legal or tax advice tone: suggest verifying the final rule per shipment.

SEO rules: the main keyword (what people search in Hebrew) appears in title, h1, desc, lead and the first <h2> naturally. Title leads with the keyword. Each <h2> is itself a search-style phrase. Answer the main question in the first 2 sentences of the body. Never keyword-stuff.

Output: a JSON array saved to the file path you are given. Each item is an object with EXACTLY these keys:
- "file": e.g. "ship-to-france.html"  (use the filenames listed for you)
- "cat": "dest" (destination/route pages) or "guide"
- "short": short link label, 2-6 words Hebrew (e.g. "שילוח לצרפת")
- "title": <title> for Google, ends with " | CargoTech", up to ~65 chars
- "desc": meta description, 120-155 chars
- "h1": the page headline (contains the main search keyword)
- "lead": one sentence beginning with "בקצרה:" (<= 200 chars)
- "tldr": 2-3 sentences summarising the answer (plain text, no HTML)
- "service": one of exactly: "יבוא", "יצוא", "שילוח אווירי או ימי", "קורייר", "מזון לארה\"ב (FDA)", "עמילות מכס", "עדיין לא יודע"
- "minutes": e.g. "4 דקות קריאה"
- "body": HTML string. Use only <h2>, <p>, <ul>, <li>, <b>, <ol>. 3-5 <h2> sections, 380-550 words total, genuinely useful and specific to the topic (not generic filler; destination pages must be specific to that country's customs context, typical restrictions, what to prepare, gift vs commercial shipment, returns). End with a short practical checklist (<ul>) or "מה לעשות עכשיו" section. No <h1>. No links inside body.
- "faq": array of exactly 3 objects {"q": "...", "a": "..."}: real questions people type into Google about this topic (natural Hebrew phrasing, starting with מה / איך / האם / כמה / מתי), answer 1-2 plain sentences, same accuracy rules (no numbers you cannot guarantee). Do NOT repeat the h1 as a question.
- "rel": 2-4 related filenames, chosen only from the master file list below.

Master file list (valid "rel" targets): customs.html import.html export.html shipping.html courier.html fda-food.html europe.html usa.html pricing.html glossary.html article-customs-broker.html article-fcl-lcl.html article-volumetric-weight.html article-fda-prior-notice.html
plus new pages: ship-to-france.html ship-to-germany.html ship-to-spain.html ship-to-italy.html ship-to-netherlands.html ship-to-greece.html ship-to-uk.html ship-to-ireland.html ship-to-canada.html ship-to-australia.html ship-to-china.html ship-to-turkey.html ship-from-europe-to-israel.html ship-from-us-to-israel.html send-gift-abroad.html envelope-to-usa.html how-to-ship-package-abroad.html international-shipping-complete-guide.html commercial-invoice.html proforma-invoice.html packing-list.html prohibited-goods.html ship-fragile-items.html postal-codes-country-codes.html import-from-china.html trade-war-tariffs.html incoterms-guide.html hs-code-guide.html import-taxes-israel.html import-step-by-step.html lithium-batteries-shipping.html eori-number.html export-from-israel.html ecommerce-shipping-abroad.html shipping-insurance.html tracking-shipments.html parcel-return.html customs-delays.html air-vs-sea-freight.html courier-companies-compared.html ups-vs-fedex-vs-dhl.html isf-filing-usa.html fda-facility-registration.html fda-food-labeling.html food-shipping-usa-checklist.html ddp-vs-dap.html
 new batch (also valid rel targets): ship-to-sweden.html ship-to-portugal.html ship-from-china-to-israel.html turkey-israel-shipping.html domestic-shipping-israel.html ship-from-thailand-to-israel.html international-relocation-guide.html relocation-container-shipping.html relocation-cost.html relocation-mistakes.html relocation-with-pets.html move-to-usa-shipping.html shipping-for-businesses.html express-shipping-for-law-firms.html hightech-equipment-shipping.html ship-computers-to-employees-abroad.html new-office-international-shipping.html ship-to-amazon-fba.html reduce-shipping-costs.html lost-package-what-to-do.html ship-documents-abroad.html damage-claims-fragile-items.html low-cost-international-shipping.html consolidated-shipping.html hts-vs-hs-codes.html customs-valuation.html dangerous-goods-shipping.html international-returns-service.html drop-shipping-israel.html shipping-to-online-stores.html eur1-certificate.html trade-agreements.html send-to-loved-ones-worldwide.html

Quality bar example of the tone/format (existing article excerpt): "כשסחורה נכנסת לישראל או יוצאת ממנה, צריך להגיש למכס דיווח. הדיווח כולל מה הסחורה, מה ערכה ומאיפה היא מגיעה. עמיל המכס מגיש את הדיווח בשמכם, ומוודא שהמס מחושב נכון."
After writing, validate with: python3 -c "import json;d=json.load(open(PATH));print(len(d))" and confirm every item has all keys and body word counts are within range.
