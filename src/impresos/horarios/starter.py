import json, base64, asyncio, html
from playwright.async_api import async_playwright
R=json.load(open('../stickers/rows.json'))
CN={'Mexico':'México'}
TEEC={'Negro':'#111','Azul':'#1f5fd1','Blanco':'#fff','Rojo':'#d32f2f'}
logo=base64.b64encode(open('../logo.png','rb').read()).decode()
ibe=base64.b64encode(open('iberostar.png','rb').read()).decode()
F='/usr/share/fonts/truetype/google-fonts/'
f400=base64.b64encode(open(F+'Poppins-Regular.ttf','rb').read()).decode()
f700=base64.b64encode(open(F+'Poppins-Bold.ttf','rb').read()).decode()
def hcp(h): n=int(h); return f'+{-n}' if n<0 else str(n)
def page(hoyo):
    rows=sorted([r for r in R if r[7]==hoyo],key=lambda r:(r[8],int(r[9])))
    times=sorted({r[8] for r in rows})
    blocks=''
    for i,t in enumerate(times,1):
        g=[r for r in rows if r[8]==t]
        trs=''
        for f,l,ctry,sc,cat,tee,h,_,_,pos in g:
            c='SCRATCH' if sc=='TRUE' else ('DAMAS' if cat=='Damas' else cat)
            tn=tee.split(' ',1)[1]
            trs+=f'<tr><td class="p">{pos}</td><td class="n"><b>{html.escape(l)}</b>, {html.escape(f)}</td><td>{CN.get(ctry,ctry)}</td><td class="c">{c}</td><td><span class="sw" style="background:{TEEC[tn]}"></span>{tn}</td><td class="h">{hcp(h)}</td><td class="ck"><span></span></td></tr>'
        blocks+=f'<section class="g"><div class="gh"><span class="t">{t}</span><span class="gn">Grupo {i} · {len(g)} jugadores · carros {'1–2 y 3–4' if len(g)==4 else '1–2 y 3'}</span></div><table><colgroup><col style="width:6%"><col style="width:34%"><col style="width:19%"><col style="width:11%"><col style="width:13%"><col style="width:8%"><col style="width:10%"></colgroup><thead><tr><th>Pos</th><th>Jugador</th><th>País</th><th>Cat.</th><th>Tee</th><th>Hcp</th><th>Check</th></tr></thead><tbody>{trs}</tbody></table></section>'
    return f'''<!doctype html><meta charset="utf-8"><style>
@font-face{{font-family:P;src:url(data:font/ttf;base64,{f400})}}@font-face{{font-family:P;font-weight:700;src:url(data:font/ttf;base64,{f700})}}
@page{{size:letter;margin:.3in}} body{{font-family:P;margin:0;color:#111;font-size:11px}}
header{{display:flex;align-items:center;gap:14px;border-bottom:2px solid #0e356b;padding-bottom:6px;margin-bottom:8px}}
header img{{height:38px}} .tt{{flex:1}} .tt b{{display:block;font-size:17px;color:#0e356b}} .tt span{{font-size:10px;color:#555}}
.big{{font-size:24px;font-weight:700;color:#fff;background:#0e356b;border-radius:6px;padding:2px 14px}}
.g{{break-inside:avoid;margin-bottom:5px}} .gh{{display:flex;align-items:baseline;gap:10px;border-bottom:1px solid #0e356b;margin-bottom:2px}}
.t{{font-size:16px;font-weight:700;color:#0e356b}} .gn{{font-size:9.5px;color:#555}}
table{{width:100%;border-collapse:collapse;table-layout:fixed}} th{{text-align:left;font-size:8.5px;color:#5b6b80;font-weight:400;padding:0 4px}} th:nth-child(1),th:nth-child(4),th:nth-child(6),th:nth-child(7){{text-align:center}}
td{{padding:1px 4px;line-height:1.3;border-bottom:1px solid #e3e8f0}} td.n{{font-size:12px}} td.p,td.c,td.h{{text-align:center;font-weight:700}}  td.h{{font-size:13px}}
tr:nth-child(2) td{{border-bottom:1.5px solid #9fb0c8}}
.sw{{display:inline-block;width:9px;height:9px;border:1px solid #777;margin-right:5px;vertical-align:-1px}}
td.ck{{text-align:center}} td.ck span{{display:inline-block;width:11px;height:11px;border:1.3px solid #555;border-radius:2px}}
</style><header><img src="data:image/png;base64,{logo}"><div class="tt"><b>Starter · Ronda 1 · Salida Hoyo {hoyo}</b><span>Iberostar Bávaro Golf Club · Miércoles 7 de octubre de 2026</span></div><span class="big">HOYO {hoyo}</span><img src="data:image/png;base64,{ibe}"></header>{blocks}'''
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page()
        for h in ('1','10'):
            await pg.set_content(page(h),wait_until='load')
            await pg.pdf(path=f'../out/CL_Starter_R1_Hoyo{h}.pdf',format='Letter',print_background=True,margin={'top':'0.3in','bottom':'0.3in','left':'0.3in','right':'0.3in'})
        await b.close()
asyncio.run(main())
