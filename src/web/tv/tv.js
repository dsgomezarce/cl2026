/* --- TV: parámetros por #ancla: r1 | r2 | r3 | total; Naciones/Interclubes abiertos por defecto, "min" los muestra cerrados (ej. #min, #r2-min) --- */
const TV = (() => {
  const h = (location.hash || '').replace('#','').toLowerCase();
  const m = /(r[123]|total)/.exec(h);
  return { round: m ? (m[1] === 'total' ? 'r3' : m[1]) : null, isTotal: !!(m && m[1] === 'total'), abierto: !/min/.test(h) };
})();
const SLIDE_MS = 8000, OPEN_MS = 12000, ROWS = 14;
function latestRound(){ for (const r of [3,2,1]) if (R.some(p => (RES[p.id]||{})[r] && (RES[p.id][r].holes||[]).some(isNum))) return 'r'+r; return 'r1'; }
/* Escala del escenario 1920x1080 al tamaño real de la pantalla. Se recalcula siempre (algunos navegadores de TV
   informan un tamaño provisorio al cargar y no avisan cuando cambia), y se anula cualquier zoom o scroll heredado. */
let _sc = '';
function scaleStage(){ const vv = window.visualViewport, de = document.documentElement;
  const w = de.clientWidth || innerWidth, h = de.clientHeight || innerHeight, st = document.getElementById('stage');
  if (!st || !w || !h) return; const s = Math.min(w/1920, h/1080), key = w + 'x' + h;
  if (key !== _sc){ _sc = key; st.style.transform = `translate(${(w-1920*s)/2}px,${(h-1080*s)/2}px) scale(${s})`; }
  if (scrollX || scrollY) scrollTo(0, 0); }
try { history.scrollRestoration = 'manual'; } catch(e){}
addEventListener('resize', scaleStage); addEventListener('orientationchange', scaleStage); addEventListener('load', scaleStage);
addEventListener('pageshow', () => { _sc = ''; scaleStage(); });
if (window.visualViewport) visualViewport.addEventListener('resize', scaleStage);
document.fonts && document.fonts.ready.then(() => { _sc = ''; scaleStage(); });
setInterval(scaleStage, 2000);
const shortName = p => `${esc(p.ln)}, ${esc((p.fn||'').charAt(0))}.`;
const fullName = p => `<b>${esc(p.last || p.ln)}</b>, ${esc(p.first || p.fn)}`;
function chunk(a, n){ const k = Math.max(1, Math.ceil(a.length / n)), size = Math.ceil(a.length / k), out = []; for (let i = 0; i < a.length; i += size) out.push(a.slice(i, i+size)); return out.length ? out : [[]]; }
function headRow(label){ const rs = RS(), multi = rs.length > 1;
  return `<tr><th>Pos</th><th class="l">${label}</th><th>Par</th>${rs.map(r=>`<th>R${r}</th>`).join('')}${multi?'<th>Total</th>':''}</tr>`; }
function playerSlides(rows, k, title, cap, sen){
  const ranked = rank(rows, p => standing(p,k), p => p.last, p => tieVec(p,k)), rs = RS(), multi = rs.length > 1;
  const best = sen && view === 'r3' ? (ranked.find(it => it.x.sr && !it.k.grp) || {}).x : null;
  const lines = ranked.map(it => { const p = it.x, vals = rs.map(r => roundVal(C[p.id][r], k)), done = vals.filter(isNum);
    const tot = done.length ? done.reduce((a,v)=>a+v,0) : null;   // total acumulado de las rondas jugadas
    const extra = (sen && p.sr ? '<span class="sr srw">Senior</span>' + (p === best ? STAR : '') : '') + (it.lead && FIN ? CUP : '');
    return `<tr class="${it.lead?'lead':''}"><td class="pos">${it.pos}</td><td class="l nm">${flag(p.c,p.f)}${fullName(p)}${extra}</td>${it.k.grp?'<td class="par dim">—</td>':`<td class="par ${parCls(it.k.v)}">${toPar(it.k.v)}</td>`}${vals.map(v=>isNum(v)?`<td class="r ${parCls(v-72)}">${v}</td>`:`<td class="r dim">${v||'—'}</td>`).join('')}${multi?(isNum(tot)?`<td class="tot">${tot}</td>`:'<td class="tot dim">—</td>'):''}</tr>`; });
  const pages = chunk(lines, ROWS);
  return pages.map((pg, i) => ({ title, cap, page: pages.length > 1 ? `${i+1} / ${pages.length}` : '', ms: SLIDE_MS,
    html: `<table><thead>${headRow('Jugador')}</thead><tbody>${pg.join('')}</tbody></table>`, leg: sen && rows.some(p => p.sr) }));
}
function teamData(groups, mode){
  const rs = RS();
  const teams = Object.entries(groups).map(([name, mem]) => { const x = {}; ROUNDS.forEach(r => x[r] = teamRound(mem, r, mode)); return {name, mem, rs:x}; });
  const key = t => teamKey(t, rs, mode);
  return rank(teams, key, t => t.name);
}
const teamFlag = (t, mode) => mode === 'nac' ? natFlag(t.mem) : (new Set(t.mem.map(m=>m.c)).size === 1 ? flag(t.mem[0].c, t.mem[0].f) : '');
function teamSlides(groups, mode, title, cap){
  const ranked = teamData(groups, mode), rs = RS(), multi = rs.length > 1;
  if (!TV.abierto){
    const lines = ranked.map(it => { const t = it.x, all = rs.every(r => t.rs[r]), tot = rs.some(r => t.rs[r]) ? rs.reduce((s,r) => s + (t.rs[r] ? t.rs[r].total : 0), 0) : null;
      return `<tr class="${it.lead?'lead':''}"><td class="pos">${it.pos}</td><td class="l team">${teamFlag(t, mode)}<b>${esc(t.name)}</b>${mode === 'nac' ? spImg(t.name,'spt') : ''}${it.lead&&FIN?CUP:''}</td>${it.k.grp?'<td class="par dim">—</td>':`<td class="par ${parCls(it.k.v)}">${toPar(it.k.v)}</td>`}${rs.map(r => t.rs[r] ? `<td class="r">${t.rs[r].total}</td>` : '<td class="r dim">—</td>').join('')}${multi?(isNum(tot)?`<td class="tot">${tot}</td>`:'<td class="tot dim">—</td>'):''}</tr>`; });
    return chunk(lines, ROWS).map((pg, i, a) => ({ title, cap, page: a.length > 1 ? `${i+1} / ${a.length}` : '', ms: OPEN_MS,
      html: `<table><thead>${headRow('Equipo')}</thead><tbody>${pg.join('')}</tbody></table>` }));
  }
  const cols = ranked.length <= 8 ? 4 : 3;
  const cards = ranked.map(it => { const t = it.x;
    const order = memberOrder(t.mem, mode);
    const rows = order.map(p => { const role = mode === 'nac' && p.sc ? 'SC' : (p.cat === 'Damas' ? 'W' : p.cat);
      const cells = rs.map(r => { const x = t.rs[r], o = C[p.id][r];
        const k = (x && x.used.has(p.id+':g')) || (mode === 'nac' && p.sc && !(x && x.used.has(p.id+':n'))) ? 'g' : 'n';
        const v = roundVal(o, k), used = x && x.used.has(p.id+':'+k);
        return isNum(v) ? `<td class="s ${mode === 'nac' && p.sc ? 'cnt' : !x ? '' : used ? 'cnt' : 'nc'} ${parCls(v - 72)}">${v}</td>` : `<td class="s dim">${v || '—'}</td>`; }).join('');
      return `<tr><td class="l">${mode === 'nac' ? natFlag(t.mem) : flag(p.c,p.f)}<b>${esc(p.ln)}</b>, ${esc((p.fn||'').charAt(0))}.<span class="tag">${role}</span></td>${cells}</tr>`; }).join('');
    const all = rs.every(r => t.rs[r]), tot = rs.some(r => t.rs[r]) ? rs.reduce((s,r) => s + (t.rs[r] ? t.rs[r].total : 0), 0) : '';
    return `<div class="card ${it.lead?'lead':''}"><div class="ch"><span class="cp">${it.lead&&FIN?CUP.replace('class="cup"','class="cup cupc"'):''}${it.pos}</span><span class="cn">${teamFlag(t, mode)}${esc(t.name)}${mode === 'nac' ? spImg(t.name,'spt') : ''}</span><span class="cpar ${it.k.grp?'':parCls(it.k.v)}">${it.k.grp?'—':toPar(it.k.v)}</span><span class="ct">${tot}</span></div><table><tbody>${rows}</tbody></table></div>`; });
  return [{ title, cap, page: '', ms: OPEN_MS, html: `<div class="grid ${cols===3?'cmp':''}" style="grid-template-columns:repeat(${cols},1fr)">${cards.join('')}</div>` }];
}

/* --- medallero provisorio (TV): podio de los 3 primeros + tabla de todos los países --- */
function medalRows(){
  const W = medalList(), by = {};
  R.forEach(p => { by[p.c] = by[p.c] || {c:p.c, f:p.f, oro:0, plata:0, bronce:0}; });
  W.forEach(w => { if (by[w.c]) by[w.c][w.m]++; });
  const rows = Object.values(by).map(x => ({...x, tot:x.oro + x.plata + x.bronce}))
    .sort((tb => (a,b) => b.oro - a.oro || b.plata - a.plata || b.bronce - a.bronce || tb(a,b))(countryTiebreak()));
  rows.forEach((x, i) => { x.pos = i + 1; x.tie = false; });
  return rows;
}
function medalSlides(){
  const rows = medalRows(); if (!rows.some(x => x.tot)) return [];
  const big = (m, t) => `<span class="md ${m}"><i></i><b>${t}</b></span>`;
  const cnt = (x, m) => x[m] ? `<span class="mc ${m}">${x[m]}</span>` : '<span class="mc z">0</span>';
  const podOrder = [1, 0, 2].map(i => rows[i]).filter(x => x && x.tot);
  const pod = podOrder.map(x => { const m = x.pos === 1 ? 'oro' : x.pos === 2 ? 'plata' : 'bronce';
    return `<div class="pc p${x.pos}"><div class="pf">${flag(x.c, x.f)}</div><div class="pn">${esc(CNAME[x.c] || x.c)}</div><div class="pm">${cnt(x,'oro')}${cnt(x,'plata')}${cnt(x,'bronce')}</div><div class="pb ${m}">${big(m, (x.tie ? 'T' : '') + x.pos)}</div></div>`; }).join('');
  const trs = rows.map(x => `<tr class="${x.pos === 1 ? 'lead' : ''}${x.pos && x.pos <= 3 ? ' top' : ''}${!x.tot ? ' nil' : ''}"><td class="pos">${x.pos <= 3 && x.tot ? big(['oro','plata','bronce'][x.pos-1], x.pos) : x.pos}</td><td class="l team">${flag(x.c, x.f)}<b>${esc(CNAME[x.c] || x.c)}</b></td><td>${cnt(x,'oro')}</td><td>${cnt(x,'plata')}</td><td>${cnt(x,'bronce')}</td><td class="tot">${x.tot}</td></tr>`).join('');
  const head = `<tr><th>Pos</th><th class="l">País</th><th>${big('oro',1)}</th><th>${big('plata',2)}</th><th>${big('bronce',3)}</th><th>Total</th></tr>`;
  return [{ title:'Medallero', cap: FINAL() ? 'Final · por países' : 'Provisorio · por países', page:'', ms: OPEN_MS,
    html: `<table class="medt"><thead>${head}</thead><tbody>${trs}</tbody></table>` }];
}
let slides = [], cur = 0, timer = null;
function buildSlides(){
  recompute();
  const RANGE = {A:'Index hasta 4,9', B:'Index 5,0 a 10,9', C:'Index 11,0 a 14,9', D:'Index 15,0 a 18,4', E:'Index 18,5 a 25,9', Damas:'Index hasta 25,9'};
  slides = [
    ...teamSlides(group('team'), 'nac', 'Copa de Naciones', ''),
    ...playerSlides(R.filter(p => p.cat === 'A'), 'g', 'Scratch', 'Gross', false),
    ...CATS.flatMap(c => playerSlides(R.filter(p => p.cat === c), 'n', c === 'Damas' ? 'Damas' : 'Categoría ' + c, RANGE[c], c !== 'Damas')),
    ...teamSlides(group('club'), 'club', 'Interclubes', '3 mejores netos'),
    ...medalSlides(),
  ];
  document.getElementById('slides').innerHTML = slides.map((s, i) =>
    `<section class="slide" data-i="${i}"><div class="st"><h2>${s.title}</h2>${s.cap?`<span>${s.cap}</span>`:''}${s.page?`<span class="pg">${s.page}</span>`:''}</div><div>${s.html}</div></section>`).join('');
  const names = []; slides.forEach((s, i) => { if (!names.length || names[names.length-1].t !== s.title) names.push({t:s.title, i}); });
  const short = t => t.replace('Copa de Naciones','Naciones').replace('Categoría ','Cat. ');
  document.getElementById('ft').innerHTML = '<div class="bar" id="bar"></div>' + names.map(n => `<span class="dot" data-t="${esc(n.t)}">${short(n.t)}</span>`).join('') + `<span class="yr">2026</span><span class="up" id="upd"></span>`;
}
function show(i){
  cur = (i + slides.length) % slides.length;
  document.querySelectorAll('.slide').forEach(el => el.classList.toggle('on', +el.dataset.i === cur));
  document.querySelectorAll('.ft .dot').forEach(el => el.classList.toggle('on', el.dataset.t === slides[cur].title));
  const bar = document.getElementById('bar'), ms = slides[cur].ms;
  bar.style.transition = 'none'; bar.style.width = '0'; void bar.offsetWidth;
  bar.style.transition = `width ${ms}ms linear`; bar.style.width = '100%';
  clearTimeout(timer); timer = setTimeout(() => show(cur + 1), ms);
}
function startTV(at){
  view = TV.round || latestRound(); if (+view[1] > MAXR) view = 'r' + MAXR;
  if (TV.isTotal && MAXR < 3) TV.isTotal = false;
  document.getElementById('rd').textContent = TV.isTotal ? 'Total' : 'Ronda ' + view[1];
  buildSlides();
  document.getElementById('upd').textContent = at ? 'Actualizado ' + at : ''; scaleStage(); show(0);
  pollData(at);
  try { const k = +sessionStorage.getItem('cl26-tv-slide'); if (k > 0 && k < slides.length) show(k); } catch(e){}
  /* Recargar solo cuando hay una versión nueva publicada (los datos ya llegan en vivo sin recargar) */
  const myRel = +((/R(\d+)$/.exec(at || '') || [0,0])[1]);
  setInterval(async () => { try { const r = await fetch('../release.txt?t=' + Date.now(), {cache: 'no-store'}); if (!r.ok) return;
      const n = parseInt((await r.text()).trim(), 10); if (!n || !myRel || n <= myRel) return;
      try { sessionStorage.setItem('cl26-tv-slide', String(cur)); } catch(e){}
      location.replace(location.pathname + '?t=' + Date.now() + location.hash); } catch(e){} }, 3 * 60 * 1000);
}
/* --- datos nuevos sin recargar (así no se sale de pantalla completa) --- */
function pollData(at){
  const REL = (/R\d+$/.exec(at || '') || [''])[0];
  const apply = (fn, label) => { fn(); const keep = cur; buildSlides(); document.getElementById('upd').textContent = 'Actualizado ' + label; show(Math.min(keep, slides.length - 1)); };
  let lastAt = at, liveOk = false;
  startLive(rows => { liveOk = true; apply(() => ingestResults(rows), hhmm() + (REL ? ' - ' + REL : '')); });
  /* respaldo: si la hoja en vivo no responde, usar data.json publicado */
  setInterval(async () => { if (liveOk) return;
    try { const r = await fetch('data.json?t=' + Date.now(), {cache: 'no-store'}); if (!r.ok) return;
      const d = await r.json(); if (!d || d.at === lastAt) return; lastAt = d.at; apply(() => { ingestParticipants(d.p); ingestResults(d.r); }, d.at); } catch(e){}
  }, 90 * 1000);
}
/* --- pantalla completa: un toque o la tecla F --- */
function goFull(){ const el = document.documentElement; if (document.fullscreenElement || !el.requestFullscreen) return;
  el.requestFullscreen().catch(() => {}); }
addEventListener('click', goFull);
addEventListener('keydown', e => { if (e.key === 'f' || e.key === 'F' || e.key === 'Enter') goFull(); });
document.addEventListener('fullscreenchange', () => { document.getElementById('fs').hidden = !!document.fullscreenElement; });
let curT; addEventListener('mousemove', () => { document.body.classList.remove('nocur'); clearTimeout(curT); curT = setTimeout(() => document.body.classList.add('nocur'), 3000); });
addEventListener('hashchange', () => location.reload());

/* Mantener la pantalla encendida mientras la TV muestra el leaderboard (si el navegador lo permite) */
let wl = null;
async function keepAwake(){ try { if ('wakeLock' in navigator && document.visibilityState === 'visible' && !wl){ wl = await navigator.wakeLock.request('screen'); wl.addEventListener('release', () => { wl = null; }); } } catch(e){ wl = null; } }
document.addEventListener('visibilitychange', keepAwake);
['click','keydown','touchstart'].forEach(ev => addEventListener(ev, keepAwake, {passive: true}));
keepAwake(); setInterval(keepAwake, 60000);
