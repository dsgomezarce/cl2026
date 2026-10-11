import itertools
C={'Merlini':'ARG','Machado':'BRA','Kent':'PAR','Amengual':'VEN','S. Mohseni':'USA','Pedrero':'MEX','Da Silva':'BRA','Storm':'PAR',
'Monsiváis':'MEX','Simón':'VEN','Pascua':'USA','García':'ARG','Dutkiewicz':'MEX','Ávila':'PAR','Arraiz':'VEN','Massao':'BRA',
'Fiocca':'ARG','A. Mohseni':'USA','Suin':'BRA','Curat':'ARG','Carreño':'VEN','Guerreros':'PAR','Azizi':'USA'}
def ok(*units):
    c=[C[x] for u in units for x in u]; return len(c)==len(set(c))
def pairings(xs):
    if not xs: yield []; return
    a=xs[0]
    for i in range(1,len(xs)):
        b=xs[i]
        if C[a]!=C[b]:
            for r in pairings(xs[1:i]+xs[i+1:]): yield [(a,b)]+r
# A: 8 -> 4 pairs; scratch prefer paired scratch-scratch
A=['Merlini','Machado','Kent','Amengual','S. Mohseni','Pedrero','Da Silva','Storm']
sol=[]
for ps in pairings(A):
    for p in itertools.permutations(ps):
        if p[0]>p[1] or p[2]>p[3] or p[0]>p[2]: continue
        if ok(p[0],p[1]) and ok(p[2],p[3]) and ok(p[0],p[2]) and ok(p[1],p[3]):
            sol.append(p)
print('A sols',len(sol)); 
# prefer: day1 group1 all scratch-ish: count non-scratch
ns={'Da Silva','Storm'}
sol.sort(key=lambda p: (sum(x in ns for x in p[0]+p[1])!=0 and sum(x in ns for x in p[2]+p[3])!=0, ))
print(sol[0])
BCs=[]
for b in pairings(['Monsiváis','Simón','Pascua','García']):
  for c in pairings(['Dutkiewicz','Ávila','Arraiz','Massao']):
    for cc in [c, c[::-1]]:
      if ok(b[0],cc[0]) and ok(b[1],cc[1]): BCs.append((b,cc))
print('BC',len(BCs),BCs[:1])
DEs=[]
D=['Fiocca','A. Mohseni','Suin']
for d1 in itertools.combinations(D,2):
  ds=[x for x in D if x not in d1][0]
  for e in pairings(['Curat','Carreño','Guerreros','Azizi']):
    for ee in [e,e[::-1]]:
      if ok(d1,(ds,)) and ok(d1,ee[0]) and ok((ds,),ee[1]): DEs.append((d1,ds,ee))
print('DE',len(DEs),DEs[:3])
