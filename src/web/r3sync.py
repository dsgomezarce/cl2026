"""Uso: python3 r3sync.py r3.json -> actualiza filas R3 de compact.txt. r3.json = values de Resultados!B112:AD164 (estado en AD). Imprime CAMBIOS n / errores."""
import json, sys
rows = json.load(open(sys.argv[1]))
cur = {l.split('|')[1]: l for l in open('compact.txt').read().splitlines() if l.startswith('R3|')}
new = {}
for r in rows:
    r = r + [''] * (29 - len(r)); n = r[0]
    holes = r[3:21]; gross = r[23].strip(); st = r[28].strip() if len(r) > 28 else ''
    st = '' if st in ('-', '') else st
    if not any(h.strip() for h in holes) and not st: continue
    hs = [h.strip() for h in holes]
    if gross and all(hs) and sum(map(int, hs)) != int(gross): print('ERROR suma', n, gross); sys.exit(1)
    if not all(hs): gross = ''
    new[n] = f"R3|{n}|{','.join(hs)}|{gross}|{st}||"
ch = [n for n in new if cur.get(n) != new[n]] + [n for n in cur if n not in new]
if ch:
    L = [l for l in open('compact.txt').read().splitlines() if not l.startswith('R3|')] + list(new.values())
    open('compact.txt', 'w').write('\n'.join(L) + '\n')
print('CAMBIOS', len(ch), ch)
