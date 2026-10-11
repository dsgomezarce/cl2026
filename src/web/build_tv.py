"""python3 build_tv.py participants.json results.json "07/10 12:30" out.html"""
import json, sys
P = json.load(open(sys.argv[1])); Rz = json.load(open(sys.argv[2])); at = sys.argv[3]; out = sys.argv[4]
core = open('app3.js').read().replace('__ROSTER__', open('roster.json').read())
core = core[:core.index('function fitCards(')]
_full = open('app3.js').read()
core += '\n' + _full[_full.index('/* --- datos en vivo'):_full.index('/* --- conexión a Google Sheets --- */')]
import os
MAX = int(open("max_round.txt").read().strip()) if os.path.exists("max_round.txt") else 3
data = json.dumps({"p": P, "r": Rz, "at": at, "max": MAX}, ensure_ascii=False, separators=(',',':'))
js = core + "\n" + open('tv/tv.js').read() + f"\nconst PUB = {data};\ningestParticipants(PUB.p); ingestResults(PUB.r); MAXR = PUB.max || 3; startTV(PUB.at);\n"
html = open('tv/tv.css').read() + open('tv/tv.html').read().replace('__LOGO__', open('../logo.datauri').read().strip()) + '<script>\n' + js + '\n</script>\n'
open(out, 'w').write(html); open('tv_data.json','w').write(data); print('ok tv', len(html)//1024, 'KB + tv_data.json')
