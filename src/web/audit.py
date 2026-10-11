import asyncio, json, sys
from playwright.async_api import async_playwright
JS = r"""
() => {
 const out=[];
 const sel='h1,h2,h3,p,.eyebrow,.sub,.note,footer div,.hd span,.rh,.sum,.sum span,.banner,td.nm,td.l,.seg button,header *,.bar *,th';
 for (const e of document.querySelectorAll(sel)){
   const cs=getComputedStyle(e); if (cs.display==='none'||!e.getClientRects().length) continue;
   const walker=document.createTreeWalker(e,NodeFilter.SHOW_TEXT); let n; const W=[];
   while(n=walker.nextNode()){ const re=/\S+/g; let m; while(m=re.exec(n.textContent)){ const rr=document.createRange(); rr.setStart(n,m.index); rr.setEnd(n,m.index+m[0].length); const b=rr.getBoundingClientRect(); if(b.width>0) W.push([m[0],Math.round(b.top), b.left, b.right]); } }
   if(!W.length) continue;
   const tops=[...new Set(W.map(w=>w[1]))].sort((a,b)=>a-b);
   const lines=[]; for(const t of tops){ if(!lines.length||t-lines[lines.length-1]>4) lines.push(t); }
   if (lines.length>1){
     const last=lines[lines.length-1]; const lw=W.filter(w=>w[1]>=last-4).map(w=>w[0]);
     out.push({el:e.tagName+'.'+e.className, lines:lines.length, last:lw.join(' '), text:e.innerText.replace(/\s+/g,' ').slice(0,80)});
   }
 }
 return out;
}
"""
async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch()
        for w in (1280,900,760,600,390,360):
            ctx=await b.new_context(viewport={'width':w,'height':900},is_mobile=w<600,has_touch=w<600)
            pg=await ctx.new_page()
            await pg.set_content('<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"></head><body>'+open('lb2.html').read()+'</body></html>')
            hdr=["Nombre Completo","Acreditado","Name","Last Name","Index","Index verificado","Date of Birth","Edad","Senior","Gender","Country","Flag","Equipo Nación","Scratch","Equipo Interclub","Suma Index","Categoría","Tee Iberostar","Hcp Iberostar","Tee Corales","Hcp Corales"]
            P=[hdr]+json.load(open('au.json')); D=json.load(open('demo_full.json'))
            await pg.evaluate(f"ingestParticipants({json.dumps(P)}); ingestResults({json.dumps(D)}); srcMsg=''; setView('r3')")
            await pg.click('#naciones .tg'); await pg.click('#cat-B .pb'); await pg.click('#interclubes .tg')
            await pg.wait_for_timeout(400)
            res=await pg.evaluate(JS)
            print('==',w, 'pageW', await pg.evaluate("document.documentElement.scrollWidth"))
            for x in res: print('  ',x)
            await pg.screenshot(path=f'full_{w}.png', full_page=True)
            await ctx.close()
        await b.close()
asyncio.run(main())
