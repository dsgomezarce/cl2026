"""Uso: python3 pub_update.py compact.txt "07/10 12:30"
compact.txt: una línea por fila de Resultados con algún dato:
  R1|NOMBRE, Nombre|4,3,5,...(18, vacío si no jugó el hoyo)|gross_de_la_sheet|estado|index_ronda|hcp_base
Verifica que la suma de hoyos coincida con el Gross de la Sheet y construye leaderboard-publico.html."""
import json, sys, subprocess
PI=[4,3,4,4,5,4,4,3,5,4,3,4,5,4,4,3,5,4]; PC=[4,3,4,5,4,4,5,4,3,4,3,5,4,5,4,4,3,4]
rows=[["Resultados"],[""],["Ronda","Jugador (Nombre Completo)","Salida","Hora"]+[str(i) for i in range(1,19)]+["Ida","Vuelta","Gross","Estado","Index ronda","Index usado","Hcp base"],
      ["Par","Iberostar","",""]+[str(x) for x in PI],["Par","Corales","",""]+[str(x) for x in PC]]
bad=[]; n=0; done={}
for line in open(sys.argv[1], encoding='utf-8'):
    line=line.strip()
    if not line or line.startswith('#'): continue
    rd,name,holes,gross,st,ir,hb=(line.split('|')+['']*7)[:7]
    hs=[h.strip() for h in holes.split(',')]; hs=(hs+['']*18)[:18]
    if all(h.isdigit() for h in hs) and gross.strip() and sum(map(int,hs))!=int(gross): bad.append((rd,name,sum(map(int,hs)),gross))
    rows.append([rd,name,'','']+hs+['','',gross,st,ir,'',hb]); n+=1
    done.setdefault(rd,0); done[rd]+= 1 if (all(h.isdigit() for h in hs) or st.strip()) else 0
if bad: print('ERROR gross no coincide:', bad); sys.exit(1)
json.dump(rows,open('pub_results_live.json','w'),ensure_ascii=False)
import os
RF='/home/claude/cl2026/release.txt'
try: rel=int(open(RF).read().strip())+1
except Exception: rel=int(subprocess.run(['git','-C','/home/claude/cl2026','rev-list','--count','HEAD'],capture_output=True,text=True).stdout.strip() or 0)+1
open(RF,'w').write(str(rel)+'\n')
sys.argv[2]=f"{sys.argv[2]} - R{rel}"
subprocess.run(['python3','build_public.py','pub_participants.json','pub_results_live.json',sys.argv[2],'leaderboard-publico.html'],check=True)
subprocess.run(['python3','build_tv.py','pub_participants.json','pub_results_live.json',sys.argv[2],'leaderboard-tv.html'],check=True)
print('filas',n,'tarjetas completas por ronda',done)
