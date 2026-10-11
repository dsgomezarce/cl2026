"""Build the public leaderboard: python3 build_public.py participants.json results.json "07/10 00:10" out.html
participants.json: get_values rows of Participants!A1:U201 (header first). results.json: rows of Resultados!A1:AC300 (or [] for none)."""
import json, sys, re
KEEP = ["Nombre Completo","Name","Last Name","Senior","Country","Flag","Equipo Nación","Scratch","Equipo Interclub","Categoría","Hcp Iberostar","Hcp Corales"]
P = json.load(open(sys.argv[1])); Rz = json.load(open(sys.argv[2])); at = sys.argv[3]; out = sys.argv[4]
hdr = P[0]; idx = [hdr.index(k) for k in KEEP]
pub_p = [KEEP] + [[(r[i] if i < len(r) else '') for i in idx] for r in P[1:] if r and r[0].strip()]
import os
MAX = int(open("max_round.txt").read().strip()) if os.path.exists("max_round.txt") else 3
data = {"p": pub_p, "r": Rz, "at": at, "max": MAX}
app = open('app3.js').read().replace('__ROSTER__', open('roster.json').read())
app = app[:app.index('/* --- conexión a Google Sheets --- */')]
app += "\n/* --- datos publicados --- */\nconst PUB = " + json.dumps(data, ensure_ascii=False, separators=(',',':')) + ";\n" \
       "ingestParticipants(PUB.p); ingestResults(PUB.r); applyMax(PUB.max || 3);\n" \
       "document.getElementById('upd').textContent = 'Actualizado ' + PUB.at;\n" \
       "{ const REL = (/R\\d+$/.exec(PUB.at) || [''])[0]; startLive(rows => { ingestResults(rows); render(); document.getElementById('upd').textContent = 'Actualizado ' + hhmm() + (REL ? ' - ' + REL : ''); }); }\n"
head = open('head3.html').read().replace('Leaderboard Comité CL 2026','Leaderboard CL 2026').replace('</style>', 'footer .upd{margin-top:2px;font-size:.7rem;color:var(--muted)}\n</style>', 1)
body = open('body3.html').read().replace('__LOGO__', open('../logo.datauri').read().strip())
body = body.replace('<div class="fs">2026</div>', '<div class="fs">2026</div>\n    <div class="upd" id="upd"></div>')
open(out, 'w').write(head + body + '<script>\n' + app + '\n</script>\n')
print('ok', len(pub_p)-1, 'jugadores,', len(Rz), 'filas de resultados')
