# فطار المكتب — نسخة المكاتب

نفس موقع «فطار المكتب» بس لأكتر من مكتب: أي حد يعمل مكتب وياخد كود، والباقي يدخلوا بالكود.

- الموقع: `docs/` (ملف واحد `index.html` + `sw.js` + الأيقونات)
- Firebase: مشروع `fetar-offices` (Firestore + Email/Password)
- القواعد: `firestore.rules` — كل مكتب تحت `offices/{oid}` ومحدش يقرا مكتب مش عضو فيه
- Index مطلوب: `items.officeId` (Collection group – Ascending)
- النشر: Cloudflare Pages (preview: offices.office-breakfast.pages.dev)
