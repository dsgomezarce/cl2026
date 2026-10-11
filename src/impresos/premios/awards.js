const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1600,height:900}});await p.goto('file://'+(process.argv[2]||'/home/claude/cl2026/index.html'));await p.waitForTimeout(2000);
const out=await p.evaluate(()=>{
 const nm=q=>(q.last||q.ln)+', '+(q.first||q.fn);
 const toP=d=>d===0?'E':(d>0?'+'+d:''+d);
 const res={};
 const pod=(rows,k)=>rank(rows,q=>standing(q,k),q=>q.last,q=>tieVec(q,k)).filter(it=>!it.k.grp).map(it=>({pos:it.pos,who:nm(it.x),par:toP(it.k.v),c:it.x.c,sr:!!it.x.sr,id:it.x.id,tot:[1,2,3].reduce((s,r)=>s+(C[it.x.id][r][k==='g'?'g':'n']||0),0)}));
 res.scratch=pod(R.filter(q=>q.cat==='A'),'g').slice(0,3);
 res.cats={};const medal=new Set();
 for(const c of CATS){const r=pod(R.filter(q=>q.cat===c),'n');res.cats[c]={top:r.slice(0,3),senior:c!=='Damas'?(r.find(x=>x.sr)||null):null};r.slice(0,3).forEach(x=>medal.add(x.id));}
 const tr=k=>teamRanked(k==='nac'?'team':'club',k).slice(0,3).map(it=>({pos:it.pos,name:it.x.name,par:toP(it.k.v),mem:it.x.mem.map(m=>nm(m)+(m.sc?' (Scratch)':'')+' · '+m.cat)}));
 res.nac=tr('nac');res.club=tr('club');
 /* Últimos 18 (regla final 2026): mejor neto de la ÚLTIMA ronda por categoría A–E + Damas.
    La categoría Scratch no tiene Últimos 18, pero los jugadores Scratch compiten en la A.
    NO usar q.sc (es el Scratch del equipo de Naciones). No acumulable: se excluye a quien tenga
    CUALQUIER otro premio (podio de categoría, podio Scratch, mejor Senior, Naciones top 3, Interclubes campeón). */
 const prized=new Set(medal);
 pod(R.filter(q=>q.cat==='A'),'g').slice(0,3).forEach(x=>prized.add(x.id));
 for(const c of CATS){const s=res.cats[c].senior;if(s)prized.add(s.id);}
 teamRanked('team','nac').slice(0,3).forEach(it=>it.x.mem.forEach(m=>prized.add(m.id)));
 teamRanked('club','club').slice(0,1).forEach(it=>it.x.mem.forEach(m=>prized.add(m.id)));
 const LAST=3;
 res.l18={};
 for(const g of ['A','B','C','D','E','Damas']){const L=[];for(const q of R){if(q.cat!==g)continue;const o=C[q.id][LAST];if(o.st||o.thru!==18)continue;const seg=n=>{let s=0;for(let i=18-n;i<18;i++)s+=o.holes[i];return s-o.h*n/18};L.push({who:nm(q),cat:q.cat,g:o.g,h:o.h,net:o.n,v:[seg(9),seg(6),seg(3),seg(2),seg(1)],otroPremio:prized.has(q.id),sr:!!q.sr})}
  L.sort((a,b)=>a.net-b.net||a.v[0]-b.v[0]||a.v[1]-b.v[1]||a.v[2]-b.v[2]||a.v[3]-b.v[3]||a.v[4]-b.v[4]);
  res.l18[g]={ganador:L.find(x=>!x.otroPremio)||null,top:L.slice(0,8)};}
 return res});
console.log(JSON.stringify(out,null,1));await b.close()})()
