import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch()
        html=open('tv_test.html').read()
        for tag in ('r3','r3-abierto','r1'):
            pg=await b.new_page(viewport={'width':1920,'height':1080}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.goto('about:blank#'+tag)
            await pg.set_content('<!doctype html><html><head><meta charset=utf-8></head><body>'+html+'</body></html>')
            await pg.wait_for_timeout(800)
            n=await pg.evaluate("slides.length"); print(tag,'slides',n,[s for s in await pg.evaluate("slides.map(s=>s.title+(s.page?' '+s.page:''))")], errs)
            for i in ([0,8] if "abierto" in tag else [0]):
                await pg.evaluate(f"show({i})"); await pg.wait_for_timeout(700)
                await pg.screenshot(path=f'tv_{tag}_{i}.png')
            # overflow check per slide
            print(await pg.evaluate("[...document.querySelectorAll('.slide')].map((s,i)=>{const r=s.getBoundingClientRect();const c=s.lastElementChild.getBoundingClientRect();return c.bottom>1016?i+':'+Math.round(c.bottom):null}).filter(Boolean)"))
        await b.close()
asyncio.run(main())
