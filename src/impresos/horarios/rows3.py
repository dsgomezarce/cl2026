# first,last,country,scratch,cat,tee,hcpR3,hoyo,hora,pos,team   (Participants + Resultados Z R3)
D="""Herik|MACHADO|Brasil|1|A|Fazio|-1|09:00|1|Brasil
Gonzalo|MERLINI|Argentina|1|A|Fazio|-1|09:00|2|Argentina
Jeancarlo|VERA|Estados Unidos|0|A|Fazio|1|09:10|1|
Alejandro|HOUSTON|Paraguay|1|A|Fazio|2|09:10|3|Paraguay B
Alexander|KENT|Paraguay|1|A|Fazio|2|09:00|3|Paraguay
Christian|STORM|Paraguay|0|A|Fazio|3|09:10|2|Paraguay
Alonso|PEDRERO|México|1|A|Fazio|4|09:10|4|México
Daniel|FUENZALIDA|Argentina|0|A|Fazio|4|09:30|1|
Fernando|DA SILVA|Brasil|1|A|Fazio|6|09:20|3|Brasil B
Matías|DOMBALD|Argentina|1|A|Fazio|6|09:20|2|Argentina B
Sebastián|MOHSENI|Estados Unidos|0|A|Fazio|6|09:00|4|
Diego|BALAGUER|Argentina|0|A|Fazio|7|09:30|3|Argentina B
Mauricio|MOLINA|Paraguay|0|A|Fazio|7|09:20|1|Paraguay B
Ernesto|AMENGUAL|Venezuela|1|A|Fazio|8|09:20|4|Venezuela
Luis|MATOS|República Dominicana|0|B|Corales|4|09:30|2|México
Daniel|MONSIVÁIS|México|0|B|Corales|5|09:50|4|México
Eduardo|SÁNCHEZ|Argentina|0|B|Corales|5|09:40|2|Argentina B
Benjamín|SLOANE|Estados Unidos|0|B|Corales|6|09:50|1|
Carlos|SIMÓN|Venezuela|0|B|Corales|7|09:30|4|Venezuela
Felipe|PASCUA|Estados Unidos|0|B|Corales|7|09:40|3|
Byen|SOONWOOK|Brasil|0|B|Corales|8|09:50|3|Brasil
María|GARCÍA|Argentina|0|Damas|Forward|5|10:40|1|Argentina
Héctor|VALDERRAMA|Estados Unidos|0|B|Corales|8|09:40|1|
Enrique|PANIAGUA|Argentina|0|B|Corales|10|09:40|4|
Idzi|DUTKIEWICZ|México|0|B|Corales|10|09:50|2|México
Diego|ÁVILA|Paraguay|0|C|Advantage|6|10:00|3|Paraguay
Norivaldo|ALVES|Brasil|0|C|Advantage|7|10:00|2|
Lara|MAIOLI|Paraguay|0|Damas|Forward|7|10:30|3|
Celio|MASSAO|Brasil|0|C|Advantage|8|10:00|1|Brasil
Andrés|ARRAIZ|Venezuela|0|C|Advantage|9|10:00|4|Venezuela
Kim|KYOUNG-AIE|Brasil|0|Damas|Forward|9|10:40|2|
Alexander|SCHEMEL|Brasil|0|C|Advantage|9|08:50|3|
Sergio|FIORE|Paraguay|0|C|Advantage|9|08:50|4|
Mija|KIM|Brasil|0|Damas|Forward|10|10:40|4|Brasil B
Bautista|FIOCCA|Argentina|0|D|Advantage|10|10:10|1|Argentina
Ezequiel|BARROS|Argentina|0|D|Advantage|11|08:30|3|
Matías|AMARILLA|Paraguay|0|D|Advantage|11|08:40|2|
Abbas|MOHSENI|Estados Unidos|0|D|Advantage|12|08:50|2|
Luis|AGUADO|Argentina|0|D|Advantage|12|10:10|2|Argentina B
Mario|KIM|Brasil|0|D|Advantage|10|10:10|3|
José|GONZÁLEZ|Paraguay|0|D|Advantage|12|10:10|4|Paraguay B
Lee|SUIN|Brasil|0|Damas|Forward|13|10:40|3|Brasil
Gil|HIPOLITO|Brasil|0|D|Advantage|13|08:40|1|Brasil B
Esteban|GUERREROS|Paraguay|0|E|Advantage|14|10:20|2|Paraguay
Kuo|DAH-YUAN|Brasil|0|E|Advantage|14|10:20|3|Brasil B
Thiago|KIM|Brasil|0|E|Advantage|14|10:30|1|
Fausto|SEVERO|Brasil|0|E|Advantage|14|10:20|1|
Mir|AZIZI|Estados Unidos|0|E|Advantage|14|08:50|1|
Martín|LIRD|Paraguay|0|E|Advantage|15|10:30|2|Paraguay B
Manuel|CURAT|Argentina|0|E|Advantage|16|10:20|4|Argentina
Amadeo|PIAZZA|Argentina|0|E|Advantage|16|08:30|1|
Guillermo|CARREÑO|Venezuela|0|E|Advantage|21|08:40|3|Venezuela
Horacio|SOARES|Argentina|0|E|Advantage|21|08:30|2|"""
R=[]
for l in D.splitlines():
    f,la,c,sc,ca,tee,h,t,pos,team=l.split('|')
    R.append((f,la,c,int(sc),ca,tee,int(h),'1',t,int(pos),team))
assert len(R)==53
NOTE={('MOHSENI','Sebastián'):'* Reducción −1 golpe: neto R1 68 (−4). Hcp Corales 7',('KIM','Mario'):'* Reducción −2 golpes: neto R1 67 (−5). Hcp Corales 12'}
WD={('FIORE','Sergio'),('BALAGUER','Diego'),('MONSIVÁIS','Daniel')}
