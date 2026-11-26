let gUnsub = null;
onAuthStateChanged(auth, user => {
  stopListeners(); S.me = user; S.g = null; OFF = null; closeModal(); if (gUnsub) { gUnsub(); gUnsub = null; }
  if (user) gUnsub = onSnapshot(doc(db,'gusers',user.uid), d => {
    S.g = d.exists() ? d.data() : { name: user.displayName || '', email: user.email, offices: [] };
    const want = S.g.cur && (S.g.offices || []).some(o => o.id === S.g.cur) ? S.g.cur : null;
    if (want !== OFF){ stopListeners(); OFF = want; if (OFF) startListeners(); }
    render();
  }, e => toast(errMsg(e)));
  doRender();
});

/* ---------- المكاتب: كل مكتب داتا لوحده، والدخول بكود ---------- */
const CODE_CH = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
const newCode = () => Array.from(crypto.getRandomValues(new Uint8Array(6)), b => CODE_CH[b % CODE_CH.length]).join('');
function vOffices(){
  const list = S.g?.offices || [];
  return `<header class="top"><div class="in"><span class="brand"><img src="icon.png" alt="">فطار المكتب</span><span class="sp"></span><a href="#" data-act="logout" class="who">خروج</a></div></header>
  <main class="wrap" style="max-width:520px">
    <h2>أهلًا ${esc(S.g?.name || '')} 👋</h2>
    ${list.length ? `<div class="card"><b>مكاتبك</b>${list.map(o => `<div class="between" style="padding:8px 0;border-bottom:1px solid var(--line)"><span>🏢 ${esc(o.name)}</span><button class="btn sm pri" data-act="offGo" data-id="${o.id}">ادخل</button></div>`).join('')}</div>` : ''}
    <div class="card" style="margin-top:12px"><b>ادخل مكتب بالكود</b><p class="mut" style="margin:4px 0 8px;font-size:13px">خد الكود من أدمن المكتب.</p>
      <form id="joinForm" class="row"><input name="code" required maxlength="8" placeholder="مثلًا: K7QM2P" style="flex:1;text-transform:uppercase;letter-spacing:2px"><button class="btn pri" type="submit">ادخل</button></form></div>
    <div class="card" style="margin-top:12px"><b>اعمل مكتب جديد</b><p class="mut" style="margin:4px 0 8px;font-size:13px">هتبقى الأدمن، وتاخد كود تبعته لزمايلك.</p>
      <form id="newOffForm" class="row"><input name="name" required maxlength="40" placeholder="اسم المكتب أو الشركة" style="flex:1"><button class="btn pri" type="submit">اعمل</button></form></div>
  </main>`;
}
async function setCur(oid, add){
  const offices = (S.g?.offices || []).filter(o => o.id !== add?.id); if (add) offices.push(add);
  await setDoc(doc(db,'gusers',me()), { name: S.g?.name || S.me.displayName || '', email: S.me.email, offices, cur: oid }, { merge:true });
}
document.addEventListener('submit', async e => {
  if (e.target.id !== 'joinForm' && e.target.id !== 'newOffForm') return;
  e.preventDefault(); const f = new FormData(e.target), btn = e.target.querySelector('button'); btn.disabled = true;
  const prof = { name: S.g?.name || S.me.displayName || S.me.email.split('@')[0], email: S.me.email, payInfo:'', createdAt: serverTimestamp() };
  try {
    if (e.target.id === 'joinForm'){
      const code = f.get('code').trim().toUpperCase().replace(/[^A-Z0-9]/g, '');
      const c = await getDoc(doc(db,'codes',code)); if (!c.exists()) throw new Error('الكود ده مش موجود — اتأكد منه');
      const oid = c.data().oid;
      await setDoc(doc(db,'offices',oid,'users',me()), { ...prof, code }, { merge:true });
      const o = await getDoc(doc(db,'offices',oid));
      await setCur(oid, { id: oid, name: o.data()?.name || 'مكتب' }); toast('أهلًا بيك في ' + (o.data()?.name || 'المكتب') + ' 🎉');
    } else {
      const name = f.get('name').trim(), code = newCode(), oref = doc(collection(db,'offices')), b = writeBatch(db);
      b.set(oref, { name, code, createdBy: me(), createdAt: serverTimestamp() });
      b.set(doc(db,'codes',code), { oid: oref.id });
      b.set(doc(db,'offices',oref.id,'users',me()), { ...prof, code });
      b.set(doc(db,'offices',oref.id,'config','app'), { admins: [me()] });
      await b.commit(); await setCur(oref.id, { id: oref.id, name }); toast('المكتب اتعمل 🎉 الكود: ' + code);
    }
  } catch (err) { toast(errMsg(err)); btn.disabled = false; }
});