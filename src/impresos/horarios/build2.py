import base64, asyncio, html
from playwright.async_api import async_playwright

FULL = {
'Alves':'ALVES, Norivaldo','Schemel':'SCHEMEL, Alexander','Fiore':'FIORE BOGARÍN, Sergio Luis','Kent':'KENT, Alexander',
'Amengual':'AMENGUAL, Ernesto','Merlini':'MERLINI, Gonzalo José','Machado':'MACHADO, Herik','Pedrero':'PEDRERO, Alonso',
'Da Silva':'DA SILVA, Fernando Augusto','S. Mohseni':'MOHSENI, Sebastián','Storm':'STORM PLATE, Christian',
'Balaguer':'BALAGUER, Diego','Dombald':'DOMBALD, Matías','Houston':'HOUSTON CUBILLA, Alejandro','Molina':'MOLINA MAIOLI, Mauricio',
'Fuenzalida':'FUENZALIDA, Daniel','Vera':'VERA, Jeancarlo','Matos':'MATOS, Luis','Soonwook':'SOONWOOK, Byen',
'Monsiváis':'MONSIVÁIS, Daniel','Simón':'SIMÓN, Carlos','Pascua':'PASCUA, Felipe','García':'GARCÍA, María Eugenia',
'Paniagua':'PANIAGUA, Enrique','Sánchez':'SÁNCHEZ, Eduardo','Sloane':'SLOANE, Benjamín','Valderrama':'VALDERRAMA, Héctor',
'Fiocca':'FIOCCA, Bautista','A. Mohseni':'MOHSENI, Abbas','Suin':'SUIN, Lee','Kim Mija':'KIM, Mija','Kyoung':'KYOUNG-AIE, Kim',
'Maioli':'MAIOLI BARTOLETTI, Lara Lee','Ávila':'ÁVILA CORVALÁN, Diego','Massao':'MASSAO KANESAKI, Celio','Dutkiewicz':'DUTKIEWICZ, Idzi',
'Arraiz':'ARRAIZ, Andrés','Carreño':'CARREÑO, Guillermo','Guerreros':'GUERREROS G., Esteban','Curat':'CURAT VALLENILLA, Manuel',
'Azizi':'AZIZI, Mir','Aguado':'AGUADO, Luis','Barros':'BARROS, Ezequiel','Amarilla':'AMARILLA, Matías','González':'GONZÁLEZ, José Domingo',
'Hipolito':'HIPOLITO, Gil','Kim M.':'KIM, Mario Ricardo','Severo':'SEVERO, Fausto','Lird':'LIRD, Martín','Dah':'DAH-YUAN, Kuo',
'Kim T.':'KIM, Thiago','Piazza':'PIAZZA, Amadeo Félix','Soares':'SOARES, Horacio'}
CAT = {'Alves':'C','Schemel':'C','Fiore':'C','Kent':'SC','Amengual':'SC','Merlini':'SC','Machado':'SC','Pedrero':'SC','Da Silva':'A',
'S. Mohseni':'SC','Storm':'A','Balaguer':'A','Dombald':'A','Houston':'A','Molina':'A','Fuenzalida':'A','Vera':'A','Matos':'B','Soonwook':'B',
'Monsiváis':'B','Simón':'B','Pascua':'B','García':'W','Paniagua':'B','Sánchez':'B','Sloane':'B','Valderrama':'B','Fiocca':'D',
'A. Mohseni':'D','Suin':'W','Kim Mija':'W','Kyoung':'W','Maioli':'W','Ávila':'C','Massao':'C','Dutkiewicz':'C','Arraiz':'C',
'Carreño':'E','Guerreros':'E','Curat':'E','Azizi':'E','Aguado':'D','Barros':'D','Amarilla':'D','González':'D','Hipolito':'D',
'Kim M.':'D','Severo':'E','Lird':'E','Dah':'E','Kim T.':'E','Piazza':'E','Soares':'E'}
FLAG = {'Kent':'PAR','Amengual':'VEN','Merlini':'ARG','Machado':'BRA','Pedrero':'MEX','Da Silva':'BRA','S. Mohseni':'USA','Storm':'PAR',
'Monsiváis':'MEX','Simón':'VEN','Pascua':'USA','García':'ARG','Ávila':'PAR','Massao':'BRA','Dutkiewicz':'MEX','Arraiz':'VEN',
'Fiocca':'ARG','A. Mohseni':'USA','Suin':'BRA','Carreño':'VEN','Guerreros':'PAR','Curat':'ARG','Azizi':'USA'}

import json
def load(fn):
    D={'1':[],'10':[]}
    for r in json.load(open(fn)):
        g=[(r[i],r[i+1],r[i+2]) for i in range(2,len(r),3)]
        D[r[0]].append((r[1],g))
    return D
D1=load('d1.json'); D2=load('d2.json')
logo = base64.b64encode(open('../logo.png', 'rb').read()).decode()
font = base64.b64encode(open('/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf', 'rb').read()).decode()
ibe = base64.b64encode(open('iberostar.png','rb').read()).decode()
fontb = base64.b64encode(open('/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf', 'rb').read()).decode()

def table(tee, rows):
    h = [f'<tr class="hole"><td colspan="10">HOYO {tee}</td></tr>',
         '<tr class="th"><td>Tee</td><td>Hora</td>' + '<td>Jugador</td><td>Cat.</td>' * 4 + '</tr>']
    for i, (t, g) in enumerate(rows):
        cells = ''
        for k in range(4):
            if k < len(g):
                n, f, ct = g[k]
                cells += f'<td class="n{" pr" if k == 2 else ""}">{html.escape(n)} <b>{f}</b></td><td class="c">{ct}</td>'
            else:
                cells += f'<td class="n{" pr" if k == 2 else ""}"></td><td class="c"></td>'
        h.append(f'<tr class="{"z" if i % 2 else ""}"><td class="c">{tee}</td><td class="t">{t}</td>{cells}</tr>')
    return '\n'.join(h)

def page(title_es, title_en, date, course, D, first):
    return f'''<section class="pg">
<header><img src="data:image/png;base64,{logo}">
<div class="ttl"><b>{title_es}</b><span>{title_en}</span></div>
<div class="rt"><img src="data:image/png;base64,{ibe}"><span>{date}</span></div></header>
<table>{table(first, D[first])}<tr class="sp"><td colspan="10"></td></tr>{table('10' if first == '1' else '1', D['10' if first == '1' else '1'])}</table>
</section>'''

css = f'''@font-face{{font-family:P;src:url(data:font/ttf;base64,{font})}}
@font-face{{font-family:P;font-weight:700;src:url(data:font/ttf;base64,{fontb})}}
@page{{size:letter landscape;margin:0.35in}}
body{{font-family:P,'Noto Color Emoji',sans-serif;color:#111;margin:0}}
.pg{{page-break-after:always}}
header{{display:flex;align-items:center;gap:18px;border-bottom:2px solid #0e356b;padding-bottom:6px;margin-bottom:6px}}
header img{{height:46px}}
.ttl{{flex:1;display:flex;flex-direction:column}} .ttl b{{font-size:15px;color:#0e356b}} .ttl span{{font-size:10px;color:#555}}
.rt{{text-align:right;display:flex;flex-direction:column;align-items:flex-end;gap:2px;font-size:10px}} .rt img{{height:52px}} .rt b{{font-size:11px;color:#0e356b}}
table{{width:100%;border-collapse:collapse;font-size:10.6px}}
td{{padding:5px 5px;white-space:nowrap}}
tr.hole td{{text-align:center;font-weight:700;color:#fff;background:#0e356b;font-size:11.5px;letter-spacing:.08em;padding:3px}}
tr.th td{{font-weight:700;border-bottom:1px solid #0e356b;color:#0e356b}}
tr.z td{{background:#eef2f8}}
td.c{{text-align:center;font-weight:700;width:26px}} td.t{{font-weight:700;width:38px}}
td.n.pr{{border-left:1px solid #b9c6d8}}
tr.sp td{{height:8px}}
footer{{margin-top:6px;font-size:8px;color:#555}}'''

doc = f'<!doctype html><meta charset="utf-8"><style>{css}</style>' + \
    page('Horarios de Salida · Ronda 1', 'Groupings and Starting Times · Round 1', 'Miércoles 7 de octubre de 2026', 'Iberostar Bávaro Golf Club', D1, '1') + \
    page('Horarios de Salida · Ronda 2', 'Groupings and Starting Times · Round 2', 'Jueves 8 de octubre de 2026', 'Iberostar Bávaro Golf Club', D2, '1')
open('horarios.html', 'w').write(doc)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page()
        await pg.set_content(doc, wait_until='load')
        await pg.pdf(path='Horarios_R1_R2.pdf', format='Letter', landscape=True, print_background=True,
                     margin={'top': '0.35in', 'bottom': '0.35in', 'left': '0.35in', 'right': '0.35in'})
        await b.close()
asyncio.run(main())
print('ok')
