"""Copia leaderboard-publico.html, leaderboard-tv.html y tv_data.json al repo de GitHub Pages, con su esqueleto HTML."""
import sys, shutil
SITE = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/cl2026'
HEAD = ('<!doctype html><html lang="es"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<meta name="robots" content="noindex,nofollow">'
        '<meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes">'
        '<meta name="apple-mobile-web-app-title" content="CL 2026"><meta name="theme-color" content="#0e356b">'
        '<style>*,*::before,*::after{box-sizing:border-box}:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>'
        '</head><body>')
BASE = 'https://leaderboard.latinoamericano.golf/'
def og(path, title):
    d = 'Resultados del XVIII Campeonato Latinoamericano de Golf: Copa de Naciones, categorías, Seniors e Interclubes. Punta Cana, 7 al 9 de octubre de 2026.'
    return (f'<title>{title}</title><meta name="description" content="{d}">'
            f'<meta property="og:type" content="website"><meta property="og:site_name" content="Campeonato Latinoamericano de Golf 2026">'
            f'<meta property="og:title" content="{title}"><meta property="og:description" content="{d}">'
            f'<meta property="og:url" content="{BASE}{path}"><meta property="og:image" content="{BASE}og.png">'
            f'<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Leaderboard del XVIII Campeonato Latinoamericano de Golf">'
            f'<meta property="og:locale" content="es_LA"><meta name="twitter:card" content="summary_large_image">'
            f'<meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{d}"><meta name="twitter:image" content="{BASE}og.png">')
for src, dst, path, title in (('leaderboard-publico.html', 'index.html', '', 'Leaderboard · XVIII Campeonato Latinoamericano de Golf'),
                              ('leaderboard-tv.html', 'tv.html', 'tv/', 'Leaderboard TV · XVIII Campeonato Latinoamericano de Golf')):
    head = HEAD if dst != 'tv.html' else HEAD.replace('width=device-width,initial-scale=1,viewport-fit=cover', 'width=device-width,initial-scale=1,minimum-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover')
    open(f'{SITE}/{dst}', 'w').write(head.replace('</head>', og(path, title) + '</head>') + open(src).read() + '</body></html>')
shutil.copy('og.png', f'{SITE}/og.png')
shutil.copy('tv_data.json', f'{SITE}/data.json')
import os; os.makedirs(f'{SITE}/tv', exist_ok=True)
shutil.copy(f'{SITE}/tv.html', f'{SITE}/tv/index.html'); shutil.copy('tv_data.json', f'{SITE}/tv/data.json')
open(f'{SITE}/.nojekyll', 'w').write('')
open(f'{SITE}/robots.txt', 'w').write('User-agent: *\nDisallow: /\n')
print('site ok')
