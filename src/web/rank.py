import asyncio, json, sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch(); pg=await b.new_page(viewport={'width':1100,'height':900})
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.set_content('<!doctype html><html><head><meta charset=utf-8></head><body>'+open('lb2.html').read()+'</body></html>')
        hdr=["Nombre Completo","Acreditado","Name","Last Name","Index","Index verificado","Date of Birth","Edad","Senior","Gender","Country","Flag","Equipo Nación","Scratch","Equipo Interclub","Suma Index","Categoría","Tee Iberostar","Hcp Iberostar","Tee Corales","Hcp Corales"]
        P=[hdr]+json.load(open('au.json')); D=json.load(open('demo_full.json'))
        await pg.evaluate(f"ingestParticipants({json.dumps(P)}); ingestResults({json.dumps(D)}); setView('r3')")
        for v in ('r1','r2','r3'):
            await pg.evaluate(f"setView('{v}')")
            rows=await pg.eval_on_selector_all('#naciones tr.team', 'rs=>rs.map(r=>r.innerText.replace(/\\s+/g," "))')
            print(v, rows[:4])
        await pg.evaluate("setView('r3')")
        if len(sys.argv)>1:
            await pg.screenshot(path='s_tot.png')
            await pg.click('.tg'); await pg.evaluate("setView('r2')")
            await pg.screenshot(path='s_r2.png',full_page=True)
            await pg.set_viewport_size({'width':400,'height':900}); await pg.evaluate("setView('r3')")
            await pg.screenshot(path='s_m.png')
        print('errors',errs)
        await b.close()
asyncio.run(main())
