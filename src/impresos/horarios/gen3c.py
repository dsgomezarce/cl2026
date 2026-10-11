import json, base64, asyncio, html, sys, subprocess
sys.path.insert(0,'.')
from rows3 import R, NOTE, WD
from playwright.async_api import async_playwright
TT='../tt/'
FULLN=["PIAZZA, Amadeo Félix","MASSAO KANESAKI, Celio","ÁVILA CORVALÁN, Diego","FIORE BOGARÍN, Sergio Luis","DA SILVA, Fernando Augusto","MERLINI, Gonzalo José","HOUSTON CUBILLA, Alejandro","STORM PLATE, Christian","GONZÁLEZ, José Domingo","KIM, Mario Ricardo","MOLINA MAIOLI, Mauricio","MAIOLI BARTOLETTI, Lara Lee","GARCÍA, María Eugenia","CURAT VALLENILLA, Manuel"]
def full(f,l):
    for n in FULLN:
        a,b=n.split(', ')
        if a.split(' ')[0]==l.split(' ')[0] and b.split(' ')[0]==f and (a==l or a.startswith(l+' ')): return n
    return f'{l}, {f}'
CODE={'Argentina':'ARG','Brasil':'BRA','Paraguay':'PAR','Venezuela':'VEN','México':'MEX','Estados Unidos':'USA','República Dominicana':'DOM'}
def cat(r): return 'SC' if r[3] else ('W' if r[4]=='Damas' else r[4])
def grp(h):
    out=[]
    for t in sorted({r[8] for r in R if r[7]==h}):
        out.append((t,sorted([r for r in R if r[7]==h and r[8]==t],key=lambda r:r[9])))
    return out
logo=base64.b64encode(open('../logo.png','rb').read()).decode()
F='/usr/share/fonts/truetype/google-fonts/'
f400=base64.b64encode(open(F+'Poppins-Regular.ttf','rb').read()).decode()
f700=base64.b64encode(open(F+'Poppins-Bold.ttf','rb').read()).decode()
FONTS=f"@font-face{{font-family:P;src:url(data:font/ttf;base64,{f400})}}@font-face{{font-family:P;font-weight:700;src:url(data:font/ttf;base64,{f700})}}"
FECHA='Viernes 9 de octubre de 2026'
# ---------- Horarios (mismo diseño que R1) ----------
def table(tee):
    h=[f'<tr class="hole"><td colspan="11">HOYO {tee}</td></tr>','<tr class="th"><td>Bus</td><td>Tee</td><td>Hora</td>'+'<td>Jugador</td><td>Cat.</td>'*4+'</tr>']
    for i,(t,g) in enumerate(grp(tee)):
        cells=''
        for k in range(4):
            if k<len(g):
                r=g[k]; fl=f'({CODE[r[10].replace(" B","")]})' if r[10] else ''
                cells+=f'<td class="n{" pr" if k==2 else ""}">{html.escape(full(r[0],r[1]))} <b>{fl}</b></td><td class="c">{cat(r)}</td>'
            else: cells+=f'<td class="n{" pr" if k==2 else ""}"></td><td class="c"></td>'
        BUS=[(5,'07:00'),(5,'07:40'),(4,'08:00')]
        acc=0; bus=''
        for n,bt in BUS:
            if i==acc: bus=f'<td class="bus" rowspan="{n}"><b>{bt}</b><span>Lobby<br>Iberostar Selection</span></td>'
            acc+=n
        h.append(f'<tr class="{"z" if i%2 else ""}{" bt" if bus else ""}">{bus}<td class="c">{tee}</td><td class="t">{t}</td>{cells}</tr>')
    return '\n'.join(h)
css=FONTS+'''@page{size:letter landscape;margin:0.35in}body{font-family:P,sans-serif;color:#111;margin:0}
header{display:flex;align-items:center;gap:18px;border-bottom:2px solid #0e356b;padding-bottom:6px;margin-bottom:6px}header img{height:46px}
.ttl{flex:1;display:flex;flex-direction:column}.ttl b{font-size:15px;color:#0e356b}.ttl span{font-size:10px;color:#555}
.rt{display:flex;flex-direction:column;align-items:flex-end;gap:2px;font-size:10px}.rt img{height:52px}
table{width:100%;border-collapse:collapse;font-size:10.6px}td{padding:5px 5px;white-space:nowrap}
tr.hole td{text-align:center;font-weight:700;color:#fff;background:#0e356b;font-size:11.5px;letter-spacing:.08em;padding:3px}
tr.th td{font-weight:700;border-bottom:1px solid #0e356b;color:#0e356b}tr.z td{background:#eef2f8}
td.c{text-align:center;font-weight:700;width:26px}td.t{font-weight:700;width:38px}td.n.pr{border-left:1px solid #b9c6d8}tr.sp td{height:8px}
.leg{margin-top:8px;font-size:8.5px;color:#555}
td.bus{background:#0e356b!important;color:#fff;text-align:center;width:92px;border-bottom:2px solid #fff;line-height:1.25}
td.bus b{display:block;font-size:17px}td.bus span{font-size:8.5px;color:#cfe3ff}tr.bt td{border-top:2px solid #0e356b}
.avi{margin-top:10px;border:2px solid #c62828;border-radius:6px;padding:6px 12px;display:flex;gap:14px;align-items:center;font-size:10.5px}.avi b{color:#c62828;font-size:11.5px;white-space:nowrap;letter-spacing:.04em}
.tees{margin-top:10px;display:flex;gap:10px;align-items:stretch}.tees h4{margin:0 8px 0 0;font-size:11px;color:#0e356b;align-self:center;letter-spacing:.06em}
.tee{border:1.5px solid #0e356b;border-radius:6px;padding:5px 12px;display:flex;flex-direction:column;align-items:center;min-width:110px}
.tee b{font-size:15px;color:#0e356b}.tee span{font-size:9.5px;color:#555}'''
HOR=f'''<!doctype html><meta charset="utf-8"><style>{css}</style><header><img src="data:image/png;base64,{logo}">
<div class="ttl"><b>Horarios de Salida · Ronda Final</b><span>Groupings and Starting Times · Final Round · Todos salen por el Hoyo 1</span></div>
<div class="rt"><b style="font-size:13px;color:#0e356b">Corales Golf Club</b><span>{FECHA}</span></div></header>
<table>{table('1')}</table>
<div class="avi"><b>IMPORTANTE · TRASLADOS</b><span>Los buses parten del Lobby del Iberostar Selection en el horario indicado, sin espera. Los jugadores que no se suban al transporte de la organización deberán llegar a Corales Golf Club por su cuenta y son responsables de presentarse en el tee a su hora de salida.</span></div>
<div class="tees"><h4>TEES DE SALIDA</h4><div class="tee"><b>Fazio</b><span>Scratch · Categoría A</span></div><div class="tee"><b>Corales</b><span>Categoría B</span></div><div class="tee"><b>Advantage</b><span>Categorías C, D y E</span></div><div class="tee"><b>Forward</b><span>Damas</span></div></div>
<div class="leg">Traslado a Corales Golf Club desde el Lobby del Iberostar Selection · Entre paréntesis: equipo de Naciones · SC Scratch · W Damas</div>'''
# ---------- Starter ----------
TEEC={'Negro':'#111','Azul':'#1f5fd1','Blanco':'#fff','Rojo':'#d32f2f'}
def hcp(n): return f'+{-n}' if n<0 else str(n)
def starter(h):
    blocks=''
    for i,(t,g) in enumerate(grp(h),1):
        trs=''
        for r in g:
            f,l,ctry,sc,ca,tee,hc,_,_,pos,_=r
            c='SCRATCH' if sc else ('DAMAS' if ca=='Damas' else ca)
            nt=NOTE.get((l,f),'')
            trs+=f'<tr{" class=nr" if nt else ""}><td class="p">{pos}</td><td class="n"><b>{html.escape(l)}</b>, {html.escape(f)}{' <span class=wd>WD R2</span>' if (l,f) in WD else ''}</td><td>{ctry}</td><td class="c">{c}</td><td>{tee}</td><td class="h">{hcp(hc)}{"*" if nt else ""}</td><td class="ck"><span></span></td></tr>'
            if nt: trs+=f'<tr class="nt"><td></td><td colspan="6">{nt}</td></tr>'
        carros='1–2 y 3–4' if len(g)==4 else '1–2 y 3'
        blocks+=f'<section class="g"><div class="gh"><span class="t">{t}</span><span class="gn">Grupo {i} · {len(g)} jugadores · carros {carros}</span></div><table><colgroup><col style="width:6%"><col style="width:34%"><col style="width:19%"><col style="width:11%"><col style="width:13%"><col style="width:8%"><col style="width:10%"></colgroup><thead><tr><th>Pos</th><th>Jugador</th><th>País</th><th>Cat.</th><th>Tee</th><th>Hcp</th><th>Presente</th></tr></thead><tbody>{trs}</tbody></table></section>'
    return f'''<!doctype html><meta charset="utf-8"><style>{FONTS}
@page{{size:letter;margin:.3in}} body{{font-family:P;margin:0;color:#111;font-size:11px}}
header{{display:flex;align-items:center;gap:14px;border-bottom:2px solid #0e356b;padding-bottom:6px;margin-bottom:8px}}
header img{{height:38px}} .tt{{flex:1}} .tt b{{display:block;font-size:17px;color:#0e356b}} .tt span{{font-size:10px;color:#555}}
.big{{font-size:24px;font-weight:700;color:#fff;background:#0e356b;border-radius:6px;padding:2px 14px}}
.g{{break-inside:avoid;margin-bottom:5px}} .gh{{display:flex;align-items:baseline;gap:10px;border-bottom:1px solid #0e356b;margin-bottom:2px}}
.t{{font-size:16px;font-weight:700;color:#0e356b}} .gn{{font-size:9.5px;color:#555}}
table{{width:100%;border-collapse:collapse;table-layout:fixed}} th{{text-align:left;font-size:8.5px;color:#5b6b80;font-weight:400;padding:0 4px}} th:nth-child(1),th:nth-child(4),th:nth-child(6),th:nth-child(7){{text-align:center}}
td{{padding:1px 4px;line-height:1.3;border-bottom:1px solid #e3e8f0}} td.n{{font-size:12px}} td.p,td.c,td.h{{text-align:center;font-weight:700}} td.h{{font-size:13px}}
tr:nth-child(2) td{{border-bottom:1.5px solid #9fb0c8}}
.nr td{{border-bottom:0}} tr.nt td{{color:#c62828;font-weight:700;font-size:9.5px;padding-top:0}}
span.wd{{font-size:8px;color:#888;font-weight:700;margin-left:4px}} .sw{{display:inline-block;width:9px;height:9px;border:1px solid #777;margin-right:5px;vertical-align:-1px}}
td.ck{{text-align:center}} td.ck span{{display:inline-block;width:11px;height:11px;border:1.3px solid #555;border-radius:2px}}
</style><header><img src="data:image/png;base64,{logo}"><div class="tt"><b>Starter · Ronda Final · Salida Hoyo {h}</b><span>Corales Golf Club · {FECHA}</span></div><span class="big">HOYO {h}</span></header>{blocks}'''
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page()
        await pg.set_content(HOR,wait_until='load')
        await pg.pdf(path='CL_Horarios_R3_traslados.pdf',format='Letter',landscape=True,print_background=True,margin={k:'0.35in' for k in ('top','bottom','left','right')})
        for h in ():
            await pg.set_content(starter(h),wait_until='load')
            await pg.pdf(path=f'CL_Starter_R3_Hoyo{h}.pdf',format='Letter',print_background=True,margin={k:'0.3in' for k in ('top','bottom','left','right')})
        await b.close()
asyncio.run(main())
