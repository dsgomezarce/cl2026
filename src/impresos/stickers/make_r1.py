import sys, re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, white, black

GF = '/usr/share/fonts/truetype/google-fonts/'
pdfmetrics.registerFont(TTFont('P', GF + 'Poppins-Regular.ttf'))
pdfmetrics.registerFont(TTFont('PM', GF + 'Poppins-Medium.ttf'))
pdfmetrics.registerFont(TTFont('PB', GF + 'Poppins-Bold.ttf'))

NAVY = HexColor('#0e356b'); BLUE = HexColor('#174d99'); CYAN = HexColor('#00cfff')
GREY = HexColor('#5b6b80'); LINE = HexColor('#c9d3e0')
TEE = {'Negro': HexColor('#111111'), 'Azul': HexColor('#1f5fd1'), 'Blanco': white, 'Rojo': HexColor('#d32f2f')}

# Avery 8162 / 5162: Letter, 2 x 7, 4" x 1-1/3"
W, H = 4 * inch, (4 / 3) * inch
TOP = 59.95  # pt, según plantilla oficial Avery 8162
LEFT = 11.2  # pt, según plantilla oficial Avery 8162
PITCH_X = 301.5  # pt

P = [  # last, first, cat, tee, hcp, country
("AGUADO","Luis","D","Blancos","11","Argentina"),("ALVES","Norivaldo","C","Azules","9","Brasil"),
("AMARILLA","Matías","D","Blancos","10","Paraguay"),("AMENGUAL","Ernesto","A","Negros","5","Venezuela"),
("ARRAIZ","Andrés","C","Azules","11","Venezuela"),("ÁVILA","Diego","C","Azules","9","Paraguay"),
("AZIZI","Mir","E","Blancos","13","Estados Unidos"),("BALAGUER","Diego","A","Negros","4","Argentina"),
("BARROS","Ezequiel","D","Blancos","10","Argentina"),("CARREÑO","Guillermo","E","Blancos","20","Venezuela"),
("CURAT","Manuel","E","Blancos","15","Argentina"),("DA SILVA","Fernando","A","Negros","3","Brasil"),
("DAH-YUAN","Kuo","E","Blancos","13","Brasil"),("DOMBALD","Matías","A","Negros","3","Argentina"),
("DUTKIEWICZ","Idzi","C","Azules","9","México"),("FIOCCA","Bautista","D","Blancos","9","Argentina"),
("FIORE","Sergio","C","Azules","12","Paraguay"),("FUENZALIDA","Daniel","A","Negros","1","Argentina"),
("GARCÍA","María","Damas","Rojos","4","Argentina"),("HIPOLITO","Gil","D","Blancos","12","Brasil"),
("GONZÁLEZ","José","D","Blancos","11","Paraguay"),("GUERREROS","Esteban","E","Blancos","13","Paraguay"),
("HOUSTON","Alejandro","A","Negros","-1","Paraguay"),("KENT","Alexander","A","Negros","-1","Paraguay"),
("KIM","Mario","D","Blancos","11","Brasil"),("KIM","Mija","Damas","Rojos","9","Brasil"),
("KIM","Thiago","E","Blancos","13","Brasil"),("KYOUNG-AIE","Kim","Damas","Rojos","8","Brasil"),
("LIRD","Martín","E","Blancos","14","Paraguay"),("MACHADO","Herik","A","Negros","-4","Brasil"),
("MAIOLI","Lara","Damas","Rojos","6","Paraguay"),("MASSAO","Celio","C","Azules","11","Brasil"),
("MATOS","Luis","B","Azules","3","República Dominicana"),("MERLINI","Gonzalo","A","Negros","-4","Argentina"),
("MOHSENI","Abbas","D","Blancos","10","Estados Unidos"),("MOHSENI","Sebastián","A","Negros","5","Estados Unidos"),
("MOLINA","Mauricio","A","Negros","4","Paraguay"),("MONSIVÁIS","Daniel","B","Azules","4","México"),
("PANIAGUA","Enrique","B","Azules","8","Argentina"),("PASCUA","Felipe","B","Azules","6","Estados Unidos"),
("PEDRERO","Alonso","A","Negros","1","México"),("PIAZZA","Amadeo","E","Blancos","15","Argentina"),
("SÁNCHEZ","Eduardo","B","Azules","4","Argentina"),("SCHEMEL","Alexander","C","Azules","12","Brasil"),
("SEVERO","Fausto","E","Blancos","13","Brasil"),("SIMÓN","Carlos","B","Azules","6","Venezuela"),
("SLOANE","Benjamín","B","Azules","5","Estados Unidos"),("SOARES","Horacio","E","Blancos","20","Argentina"),
("SOONWOOK","Byen","B","Azules","7","Brasil"),("STORM","Christian","A","Negros","1","Paraguay"),
("SUIN","Lee","Damas","Rojos","12","Brasil"),("VALDERRAMA","Héctor","B","Azules","7","Estados Unidos"),
("VERA","Jeancarlo","A","Negros","-2","Estados Unidos"),
]

def fit(c, text, font, size, maxw, minsize=7):
    while size > minsize and c.stringWidth(text, font, size) > maxw:
        size -= 0.25
    return size

def hcp_txt(h):
    n = int(h)
    return f"+{-n}" if n < 0 else str(n)   # WHS: plus handicap

def label(c, x, y, p, rnd, guides):
    last, first, cat, tee, hcp, country = p[:6]
    pad = 0.09 * inch
    if guides:
        c.setStrokeColor(LINE); c.setLineWidth(0.5); c.setDash(2, 2)
        c.roundRect(x, y, W, H, 0.08 * inch); c.setDash()
    # right HCP block
    bw = 0.95 * inch
    bx = x + W - pad - bw; by = y + pad; bh = H - 2 * pad
    c.setFillColor(NAVY); c.roundRect(bx, by, bw, bh, 0.07 * inch, stroke=0, fill=1)
    c.setFillColor(CYAN); c.setFont('PM', 6.5)
    c.drawCentredString(bx + bw / 2, by + bh - 0.17 * inch, 'HCP DE JUEGO')
    c.setFillColor(white); s = fit(c, hcp_txt(hcp), 'PB', 30, bw - 8)
    c.setFont('PB', s); c.drawCentredString(bx + bw / 2, by + bh / 2 - 0.13 * inch, hcp_txt(hcp))
    c.setFont('PM', 7.5)
    c.drawCentredString(bx + bw / 2, by + 0.08 * inch, 'SCRATCH' if cat == 'SC' else ('DAMAS' if cat == 'Damas' else f'CATEGORÍA {cat}'))
    # left area
    lx = x + pad; lw = bx - lx - 0.08 * inch; top = y + H - pad
    lh = 0.36 * inch; lwid = lh * 781 / 255
    c.drawImage(LOGO, lx, top - lh, lwid, lh, mask='auto')
    c.setFillColor(GREY); c.setFont('PM', 6.3)
    rx = lx + lwid + 0.06 * inch
    c.drawString(rx, top - 0.13 * inch, rnd[0])
    c.drawString(rx, top - 0.25 * inch, rnd[1])
    # name
    name = f"{last}, {first}"
    c.setFillColor(NAVY); s = fit(c, name, 'PB', 13.5, lw)
    c.setFont('PB', s); c.drawString(lx, top - lh - 0.2 * inch, name)
    # tee + country
    yy = top - lh - 0.39 * inch
    sq = 0.085 * inch
    c.setFillColor(TEE.get(tee, white)); c.setStrokeColor(GREY); c.setLineWidth(0.6)
    c.rect(lx, yy - 0.005 * inch, sq, sq, stroke=1, fill=1)
    c.setFillColor(black); c.setFont('PM', 8)
    t = f"Tee {tee}"
    c.drawString(lx + sq + 0.05 * inch, yy, t)
    tw = c.stringWidth(t, 'PM', 8)
    c.setFillColor(GREY); c.drawString(lx + sq + 0.05 * inch + tw + 4, yy, '·')
    c.setFillColor(black); ctry = country.upper()
    cs = fit(c, ctry, 'PM', 8, lw - (sq + 0.05 * inch + tw + 12), 6)
    c.setFont('PM', cs); c.drawString(lx + sq + 0.05 * inch + tw + 12, yy, ctry)
    # tee time
    yy2 = y + pad + 0.02 * inch
    c.setFont('P', 7.5); c.setFillColor(GREY); c.drawString(lx, yy2, 'SALIDA')
    sx = lx + c.stringWidth('SALIDA', 'P', 7.5) + 6
    c.setFillColor(black); c.setFont('PB', 9.5)
    if len(p) > 6 and p[6]:
        c.drawString(sx, yy2, p[6])
    else:
        c.drawString(sx, yy2, 'Hoyo'); hx = sx + c.stringWidth('Hoyo', 'PB', 9.5) + 3
        c.setStrokeColor(GREY); c.setLineWidth(0.6); c.line(hx, yy2 - 1, hx + 18, yy2 - 1)
        hx += 26; c.drawString(hx, yy2, 'Hora'); hx += c.stringWidth('Hora', 'PB', 9.5) + 3
        c.line(hx, yy2 - 1, hx + 34, yy2 - 1)

def build(out, rnd, guides=True):
    c = canvas.Canvas(out, pagesize=letter)
    c.setTitle('Stickers tarjetas – ' + ' '.join(rnd))
    for i, p in enumerate(P):
        k = i % 14
        if i and k == 0: c.showPage()
        col, row = k % 2, k // 2
        x = LEFT + col * PITCH_X
        y = letter[1] - TOP - (row + 1) * H
        label(c, x, y, p, rnd, guides)
    c.save()

LOGO = sys.argv[1]
if len(sys.argv) > 3 and sys.argv[3] == 'gris':
    NAVY = HexColor('#2b2b2b'); CYAN = HexColor('#d0d0d0'); GREY = HexColor('#555555'); LINE = HexColor('#bbbbbb')
    TEE.update({'Negras': HexColor('#000000'), 'Azules': HexColor('#6e6e6e'), 'Blancas': white,
                'Rojos': HexColor('#b5b5b5'), 'Rojas': HexColor('#b5b5b5')})
    from PIL import Image
    Image.open(LOGO).convert('LA').save('logo_gris.png'); LOGO = 'logo_gris.png'

import json
CN={'Mexico':'México'}
R=json.load(open('rows.json'))
R.sort(key=lambda r:(int(r[7]),r[8],int(r[9])))
P=[]
for f,l,ctry,sc,cat,tee,h,hoyo,hora,pos in R:
    P.append((l,f,'SC' if sc=='TRUE' else cat,tee.split(' ',1)[1],h,CN.get(ctry,ctry),f'Hoyo {hoyo} · {hora}'))
assert len(P)==53
build(sys.argv[2], ('RONDA 1 · MIÉ 7 OCT', 'IBEROSTAR BÁVARO'), guides=False)
