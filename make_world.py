# يحوّل نسخة «فطار المكتب» العادية (ob/docs) لنسخة المكاتب (world/docs)
import re, shutil, os, sys
SRC='/home/claude/ob/docs'; DST='/home/claude/world/docs'
ver = sys.argv[1]
shutil.rmtree(DST, ignore_errors=True); shutil.copytree(SRC, DST)
p=DST+'/index.html'; s=open(p).read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:70],s.count(old)); s=s.replace(old,new)
s=s.replace("doc(db,","doc(ODB(),").replace("collection(db,","collection(ODB(),")
s=s.replace("{ uid:me(), orderId:","{ uid:me(), officeId:OFF, orderId:")
rep("collectionGroup(db,'items')","query(collectionGroup(db,'items'), where('officeId','==',OFF))")
rep("await setDoc(doc(ODB(),'users',cred.user.uid), { name, email:cred.user.email, payInfo:'', createdAt:serverTimestamp() });",
    "await setDoc(doc(db,'gusers',cred.user.uid), { name, email:cred.user.email, offices:[], cur:null, createdAt:serverTimestamp() });")
rep("const S = { me:null,", """let OFF = null; // المكتب الحالي
const ODB = () => doc(db,'offices',OFF);
const S = { g:null, office:null, me:null,""")
rep("  if (!['users','orders','items','transfers','rests','config','carry','catalog'].every(k=>S.loaded[k])){",
"""  if (!S.g){ app.innerHTML = '<div class="loading">جاري التحميل…</div>'; return; }
  if (!OFF){ app.innerHTML = vOffices(); return; }
  if (!['users','orders','items','transfers','rests','config','carry','catalog'].every(k=>S.loaded[k])){""")
rep("  L('complaints', collection(ODB(),'complaints'),",
"""  L('office', ODB(), d => { S.office = d.exists() ? { id:d.id, ...d.data() } : null; });
  L('complaints', collection(ODB(),'complaints'),""")
rep("if (e?.code === 'permission-denied' && (amPending() || !S.loaded.meDoc)) { S.loaded[name] = true; render(); return; } toast(errMsg(e)); }));","if (e?.code === 'permission-denied' && (amPending() || !S.loaded.meDoc)) { S.loaded[name] = true; render(); return; } toast(errMsg(e)); S.loaded[name] = true; render(); }));")
rep("""onAuthStateChanged(auth, user => {
  stopListeners(); S.me = user; closeModal();
  if (user) startListeners();
  doRender();
});""", open('/home/claude/world/offices_block.js').read())
rep("  claimAdmin: () =>","""  offGo: oid => setCur(oid),
  offSwitch: () => setDoc(doc(db,'gusers',me()), { cur: null }, { merge:true }),
  offCode: () => copy(`ادخل «فطار المكتب» على ${location.origin} واكتب الكود ده: ${S.office?.code || ''}`),
  offLeave: async () => { if (!confirm('تخرج من المكتب ده؟ حسابك فيه هيفضل، بس مش هيظهر عندك')) return;
    await setDoc(doc(db,'gusers',me()), { offices: (S.g?.offices || []).filter(o => o.id !== OFF), cur: null }, { merge:true }); },
  claimAdmin: () =>""")
rep("""  return `<h2>حسابي</h2><div class="card">
    <form id="profForm">""","""  return `<h2>حسابي</h2>
  <div class="card"><div class="between"><b>🏢 ${esc(S.office?.name || 'المكتب')}</b><button class="btn sm" data-act="offSwitch">مكتب تاني</button></div>
    <div class="mut" style="font-size:13px;margin-top:6px">كود المكتب: <b style="letter-spacing:2px;color:var(--ink)">${esc(S.office?.code || '…')}</b> — ابعته لزمايلك يدخلوا بيه</div>
    <div class="row" style="margin-top:8px"><button class="btn sm pri" data-act="offCode">انسخ الكود ورسالة الدعوة</button><button class="btn sm" data-act="offLeave">اخرج من المكتب</button></div></div>
  <div class="card">
    <form id="profForm">""")
rep("""${S.ramadan ? 'فطار المكتب 🌙' : 'فطار المكتب'}</a>""", """${esc(S.office?.name || 'فطار المكتب')}${S.ramadan ? ' 🌙' : ''}</a>""")
rep("serverTimestamp, writeBatch, getDocs, increment, deleteField }","serverTimestamp, writeBatch, getDocs, getDoc, increment, deleteField }")
s=re.sub(r'const firebaseConfig = \{.*?\};','''const firebaseConfig = {
  apiKey: "AIzaSyDbj9I3wq6Dr4WfhqA3J1dFL-tinLAncCc",
  authDomain: "fetar-offices.firebaseapp.com",
  projectId: "fetar-offices",
  storageBucket: "fetar-offices.firebasestorage.app",
  messagingSenderId: "7684902639",
  appId: "1:7684902639:web:fd95e03555ab21a287951a"
};''',s,count=1,flags=re.S)
rep("/^ob-v/.test(k)","/^fo-v/.test(k)")
# الإشعارات شغالة على رابط نسخة المكاتب
rep("const PUSH_HOST = /^office-breakfast\\.pages\\.dev$|github\\.io$/.test(location.hostname);",
    "const PUSH_HOST = /^offices\\.office-breakfast\\.pages\\.dev$/.test(location.hostname);")
open(p,'w').write(s)
w=DST+'/sw.js'; t=open(w).read(); t=re.sub(r"const VER = '[^']*'", f"const VER = '{ver}'", t); open(w,'w').write(t)
print('ok')
