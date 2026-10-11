# Campeonato Latinoamericano de Golf: manual del sistema de scoring, web, TV e impresos

**Edición documentada:** XVIII, Punta Cana 2026. R1 y R2 en Iberostar Bávaro (7 y 8/10), R3 en Corales (9/10).
**Para:** el Comité de la edición 2027 (XIX), o quien tenga que levantar el sistema de cero.
**Escrito:** 11/10/2026, con el torneo cerrado y los resultados finales.

Este documento tiene todo lo necesario para recrear el sistema completo sin otra explicación: aprendizajes, reglamento aplicado, documentos y links, estructura de la planilla con sus fórmulas, código del sitio y la TV, operación día por día, impresos, premios y la lista de datos a cambiar para 2027. El código fuente está en el repo del sitio, carpeta `src/`: [github.com/dsgomezarce/cl2026/tree/main/src](https://github.com/dsgomezarce/cl2026/tree/main/src). En este manual esa carpeta se llama `kit/`.

---

## 0. Cómo usar este manual

1. Leé primero la sección 1 (aprendizajes). Son las reglas que evitan repetir los errores de 2026.
2. Para preparar 2027, seguí la sección 10 (checklist) en orden.
3. Las secciones 3 a 9 son referencia: qué es cada cosa y cómo se arma.
4. Todo lo que está en `kit/` es la versión final usada en 2026. Las rutas dentro de los scripts apuntan a la máquina donde se ejecutaron; ajustalas (sección 5.3).

---

## 1. Aprendizajes de 2026 (leer primero)

Cada punto es una regla para 2027, con el caso que la originó.

### 1.1 Datos y planilla

1. **La clave de todo es el Nombre Completo** ("APELLIDO, Nombres", columna A de Participants). Si en Resultados un nombre no coincide exacto con Participants, la tarjeta desaparece del leaderboard **sin aviso**. En 2027 agregar una columna de control en Resultados que marque "No existe en Participants".
2. **Localizar columnas por nombre de encabezado, nunca por posición.** En 2026 el script de respaldo `r3sync.py` leía el Estado por índice y apuntó a la columna equivocada (Estado está en AC, Index ronda en AD). La web en vivo no tuvo el problema porque lee por encabezado. Cualquier script nuevo: buscar el índice con el nombre del encabezado.
3. **La columna "Scratch" de Participants (N) NO es la categoría Scratch.** Marca al Scratch de cada equipo de Naciones (uno por equipo: 8 en 2026). La categoría Scratch son todos los jugadores de la A, ordenados por gross. En 2026 se usó N por error para excluir de Últimos 18 y salió mal el ganador de la A (Vera en vez de Da Silva). En 2027 conviene renombrar N a "Scratch del equipo Nación".
4. **El snapshot de participantes del sitio se regenera antes de cada ronda.** El sitio guardaba una copia vieja de Participants y mostró Hcp de Corales desactualizados para 17 jugadores en R3. Los jugadores jugaron con el hcp correcto; el error fue solo de visualización, pero cambió el orden de la Cat. B. Antes de habilitar cada ronda: volver a bajar Participants y comparar Hcp Iberostar (S) y Hcp Corales (U) contra lo publicado.
5. **Generar las filas de cada ronda en Resultados en orden de salida desde el principio.** En R3 estaban en orden alfabético y hubo que reordenarlas durante la ronda (sortRange con clave temporal). Los scorers cargan más rápido si siguen el orden del starter.
6. **No usar arrays auxiliares entre hojas para los horarios.** Al filtrar u ordenar quedaban huecos viejos. Usar fórmulas directas por celda o `VSTACK` + `ARRAYFORMULA` en la fila de encabezado.
7. **Borrar los datos de prueba el día anterior** a la primera salida. En 2026 quedaron datos de demo en Resultados hasta la mañana de R1.
8. **Fechas de nacimiento con año de 4 cifras.** En 2026 dos fechas venían con año de 2 cifras y se interpretaron bien de casualidad.
9. **La Sheet usa locale es_ES:** fórmulas con `;`, coma decimal, la API devuelve "-0,3" como texto. Cualquier script que lea valores tiene que convertir la coma.
10. **El Hcp de cada ronda sale de Resultados** (Hcp base AF y Hcp juego Z), no de Participants. Participants solo da el Hcp de referencia por campo.
11. **El score máximo por hoyo no se valida.** Soares (Cat. E) anotó 9 en un par 3 en R1 (máximo 8). Agregar validación en Resultados: par 3 → 8, par 4 → 9, par 5 → 10, excepto Scratch y A.

### 1.2 Reglamento aplicado en el código

12. **Equipos de 3 no tienen descarte.** Si un integrante hace WD, el equipo queda fuera de esa clasificación. En 2026 el sitio dio a Sterling como campeón de Interclubes con 3 jugadores y uno en WD; el campeón correcto era Guarapiranga. Lo mismo aplica a Naciones ("si un equipo presenta dos jugadores menos… NO participarán").
13. **Últimos 18 no es acumulable con NINGÚN otro premio:** podio de categoría, podio Scratch, mejor Senior, Naciones (top 3) e Interclubes (campeón). Primero se excluyó solo a los podios y cambiaron dos ganadores.
14. **Últimos 18 tiene fila Damas propia.** Antes se mezclaba a las damas en A–E por index; Diego pidió una fila Damas separada. La categoría Scratch no tiene Últimos 18, pero sus jugadores compiten en la A.
15. **Desempate de Últimos 18 y de 2.º/3.º:** últimos 18 de la última ronda, luego últimos 9, 6, 3, 2 y 1, en neto con hcp proporcional; por último sorteo. En 2026, Matos y Soonwook empataron en 72 neto y se desempató así.
16. **WD, DQ y NR van al fondo**, ordenados primero por cantidad de rondas jugadas y después por acumulado (Fuenzalida con 2 rondas arriba de Balaguer con 1). Un jugador sin R1/R2 que juega R3 (Fiore) queda último con su R3 visible.
17. **Damas no tiene premio Senior** (decisión final de Diego, después de probar y revertir un "Senior mixto").
18. **El cierre se declara:** al terminar, todo lo "provisorio" pasa a "final", la sección pasa a "🏆 Campeones" y el medallero dice "resultado final". El 1.º de cada categoría se define por muerte súbita en cancha, así que el sitio no marca campeón hasta que el Comité confirma.

### 1.3 Web, TV y publicación

19. **La publicación pública va en GitHub Pages desde el día 0.** Los artifacts de claude.ai muestran la barra de claude.ai, iOS no permite pantalla completa y los conectores solo funcionan para el dueño. Se migró el 7/10 al mediodía.
20. **Claude no puede crear el repo:** crearlo a mano, activar Pages (Settings → Pages → main / root) y configurar el dominio antes del torneo.
21. **Datos en vivo por una hoja espejo pública** con `IMPORTRANGE`, leída por la web cada 90 s (gviz JSONP). El commit cada 10 min queda como respaldo.
22. **No usar emojis de bandera en la web:** en algunos celulares no se ven. Usar SVG propios (en `app3.js`, objeto `SVGF`). Agregar los países nuevos.
23. **Probar a 390 px de ancho**, en la vista más ancha (R3/Total). Nombres en una línea: escritorio "APELLIDO COMPLETO, Nombres", intermedio "APELLIDO, Nombre", móvil "APELLIDO, N.".
24. **La TV se recarga solo si cambia `release.txt`**, con escala fija 1920×1080. Así no parpadea ni se resetea.
25. **Nunca correr `pub_update.py` desde una copia o un test:** escribe `release.txt` del repo con ruta absoluta y sube el contador. Si pasa: `git checkout release.txt`.
26. **El sandbox de Claude no llega al dominio público** (proxy). Verificar el sitio en vivo desde un navegador real y decir qué se verificó y qué no.
27. **Habilitar cada ronda es decisión del Comité** (`max_round.txt`).

### 1.4 Forma de trabajo

28. **"No hagas nada sin mi autorización clara"** (Diego, 8/10). Los ciclos automáticos solo hacen el respaldo autorizado. Habilitar rondas, reordenar filas, cambiar código del sitio, tocar horarios o Participants: con permiso explícito.
29. **Confirmar el alcance antes de cambiar estructuras de la Sheet.** "Hoyo no va" se entendió como "no cargar hoyo a hoyo" y era "sacar la columna Hoyo actual".
30. **Verificar contra el reglamento antes de afirmar un resultado.** Contar desde los datos, no de memoria (en 2026 se informó "5 WD" y eran 4).
31. **No reescribir el historial del repo** sin autorización.
32. **Comunicación a jugadores:** en el Cuadro de Honor no se dice qué premio recibe cada uno; banderas en lugar de códigos; lo más importante arriba.

---

## 2. Reglamento tal como se aplicó en 2026

Fuente: "Condiciones de la Competencia – CL 2026" (link en sección 3).

### 2.1 Participación y hándicap
- Index WHS hasta 25,9. Con 26,0 a 30,0 se juega con 25,9. Más de 30: no participa.
- Hándicap de juego: 100% del Course Handicap del tee correspondiente, con index máximo 25,9.
- Fórmula: `ROUND(MIN(Index;25,9) × Slope / 113 + Rating − Par)`.
- 54 hoyos, juego por golpes.

### 2.2 Categorías

| Categoría | Index | Tee Iberostar (cab.) | Tee Corales (cab.) |
|---|---|---|---|
| Scratch (gross) | los mismos jugadores de la A | Negro | Fazio |
| A | hasta 4,9 | Negro | Fazio |
| B | 5,0 a 10,9 | Azul | Corales |
| C | 11,0 a 14,9 | Azul | Advantage |
| D | 15,0 a 18,4 | Blanco | Advantage |
| E | 18,5 a 25,9 | Blanco | Advantage |
| Damas Neto | todas (si son 5 o más) | Rojo | Damas Forward |

- Mínimo 6 jugadores por categoría; si no, se une a la inmediata anterior.
- Damas: con al menos 5 se arma "Damas Neto"; con menos, juegan en A–E según index desde el tee de damas.
- Senior: 55 años cumplidos al inicio. Premio al mejor Senior de cada categoría con hándicap (A–E), acumulable con el podio. Damas no tiene Senior.

### 2.3 Ajuste diario de hándicap (acumulativo, solo hacia abajo)

| Neto bajo par | −4 | −5 | −6 | −7 | −8 | −9 | −10 | −11 o más |
|---|---|---|---|---|---|---|---|---|
| Baja | 1 | 2 | 3 | 4 | 5 | 6 | 8 | 10 |

- No cambia de categoría. En R3 (otro campo) la reducción se aplica sobre el hcp de juego de ese campo.
- Si el Comité carga un "Index ronda" (Resultados AD), ese index manda y las reducciones se cuentan desde ahí.
- Casos 2026: Mohseni Sebastián jugó R3 con 6 (7 − 1 por 68 neto en R1); Kim Mario Ricardo con 10 (12 − 2 por 67 neto en R1).

### 2.4 Score máximo por hoyo
8 en par 3, 9 en par 4, 10 en par 5. No aplica a Scratch ni A. **El sistema 2026 no lo validaba.**

### 2.5 Desempates
- **1.º puesto:** muerte súbita en cancha, sin hándicap. Si no se puede jugar, automático.
- **2.º y 3.º:** últimos 18, luego 9, 6, 3, 2 y 1 (en neto, hcp proporcional); por último sorteo.
- **Últimos 18 y Seniors:** neto de los últimos 9, 6, 3, 2 y último hoyo; después sorteo.
- Implementación (`tieVec` en app3.js): solo si las rondas de la vista están completas; con 2+ rondas usa los 18 hoyos de la última ronda. "Últimos 9" toma los hoyos 10–18 de la tarjeta aunque el jugador haya salido por el 10. **El Comité 2027 debería definir esto por escrito.**

### 2.6 Copa de Naciones
- Equipos de 4: 1 Scratch + 3 con hándicap. Máximo 3 jugadores en A/B/C, 2 en D, 1 en E; las damas ocupan el cupo de su index. Hasta 2 equipos por país.
- Score por ronda: gross del Scratch + los 2 mejores netos de los otros 3. **El Scratch nunca se descarta.** Par del equipo: 216 por ronda.
- Scratch descalificado: cuenta el gross del jugador de menor hándicap del equipo.
- Equipo con menos de 3 jugadores sin estado en una ronda: fuera.
- Desempate del 1.º: muerte súbita alternando golpes. 2.º y 3.º: descartes de R3, R2, R1, sorteo. **No implementado en el código.**

### 2.7 Interclubes
- Equipos de 4 (puede ser mixto, de distintos países). Cuentan los 3 mejores netos por ronda; gana el menor total.
- Con 3 jugadores no hay descarte: un WD lo deja fuera.

### 2.8 Premios (como se entregaron)

| Premio | Medalla |
|---|---|
| Categorías A–E y Damas (1.º, 2.º, 3.º) | oro, plata, bronce |
| Scratch (1.º, 2.º, 3.º) | oro, plata, bronce |
| Mejor Senior por categoría (A–E) | plata |
| Naciones (1.º, 2.º, 3.º) | oro, plata, bronce a cada integrante |
| Interclubes (campeón) | oro a cada integrante |
| Últimos 18 (A–E + Damas) | plato + vaso térmico |

**Últimos 18, regla final:** mejor neto de la última ronda por categoría A–E y Damas, excluyendo a cualquiera con otro premio. No suma al medallero.

### 2.8 bis Medallero por países
- Oro, plata y bronce de cada categoría, Scratch, Naciones; plata del mejor Senior; oro de Interclubes.
- Naciones e Interclubes suman una medalla al país mayoritario del equipo (`majority`). **El reglamento dice que en Interclubes mixtos cuenta una medalla por cada país:** revisar para 2027.
- Orden: oros, platas, bronces. Desempate: mejor puesto en Naciones, mejores puestos individuales, alfabético.

### 2.9 Otros
- Entrega de tarjeta: antes que cualquier jugador del grupo siguiente.
- Comité 2026: Jano Wuille-Bille, Diego Gomez Arce, Pablo Centurión, Rodrigo Fueyo. Reglas locales: Jano y Diego. Planilla: Tía Marta.

---

## 3. Documentos y links

| Recurso | Link | Para qué |
|---|---|---|
| **Planilla de Golfistas 2026** (principal) | https://docs.google.com/spreadsheets/d/1jxcTguMRh_5O1KulgI2xV7_UiC5Blj27go1vF2US-lo/edit | Inscriptos, categorías, tees, horarios y resultados. Es de otra cuenta, compartida con Diego |
| **Hoja espejo pública** | https://docs.google.com/spreadsheets/d/1S-kTzLUTm1Fm9raCADOaR_cKSsS2j_elgKt7VH1NmTo/edit | `IMPORTRANGE` de Resultados, compartida "cualquiera con el link". La lee la web |
| **Inscripción 2027** (nueva) | https://docs.google.com/spreadsheets/d/1T0Bx4MLdUgwn3ETg3G7i_l8D2szI6R9eZW3W6nCWNVg/edit | Carga de participantes de la próxima edición (sección 11) |
| Condiciones de la Competencia 2026 | https://docs.google.com/document/d/1cUE4bQPSCBQ5o_cNnmo0zqDvdULqVWvq_ftm-mzroT0/edit | Reglamento |
| Condiciones 2026 (.docx) | https://drive.google.com/file/d/1t63X_mLsgLO544n4iKIZr2cYIuqZ-yig/view | Copia Word |
| Reglas Locales Iberostar | https://docs.google.com/document/d/1zJ8yECOV3gRM34ffPJGMi9kDSbm7Wpkxh_5_pBLdqu8/edit | R1 y R2. Ritmo de juego 4 h 41 |
| Reglas Locales Corales | https://docs.google.com/document/d/1LUa-flHOVYFuvPLhvq1gGLXc1s0r4stD_iZOXZVbQF8/edit | R3. Ritmo 4 h 42 |
| Reglas Locales Iberostar (.docx viejo) | https://drive.google.com/file/d/1msTtPehL6aY1keH2akyWtzWfygXZVpp9/view | **Desactualizado** (conserva la línea de "zonas cubiertas con arena"). No usar |
| Reglamento 2025 (referencia) | https://latinoamericano.golf/wp-content/uploads/2025/10/Condiciones-de-la-Competencia-CL-2025-Final-1.pdf | Edición anterior |
| **Leaderboard público** | https://leaderboard.latinoamericano.golf/ | Web para jugadores |
| **Leaderboard TV** | https://leaderboard.latinoamericano.golf/tv/ | Pantalla del clubhouse |
| Repo del sitio | https://github.com/dsgomezarce/cl2026 | GitHub Pages, rama main |
| **Comité de Campeonato** (artifact) | https://claude.ai/artifact/224Bnat9UhH2cT5egGmuA2 | Hub del Comité. Acá está publicado este manual |
| Leaderboard Comité (artifact) | https://claude.ai/artifact/WM5xURfQv6HKgn7ELT8WqT | Lee la Sheet en vivo con conector. Solo funciona para su dueño |
| Leaderboard y TV en artifact | https://claude.ai/artifact/LdNre8tYgXGqpgMCuGnfNT · https://claude.ai/artifact/WSiKM25Z4M4yMAYATUiwnx | Versiones previas, reemplazadas por GitHub Pages |

Los Docs y la planilla de Inscripción 2027 están en "Mi unidad" de la cuenta de Diego.

---

## 4. Planilla de Golfistas: estructura y fórmulas

Locale **es_ES** (fórmulas con `;`, coma decimal).

### 4.1 Pestañas

| Pestaña | sheetId | Contenido |
|---|---|---|
| Participants | 288890070 | Un jugador por fila (2 a 201). Fuente de categoría, tee, hcp y salidas |
| Resultados | 1876230846 | Tarjetas hoyo a hoyo. Fila 3 encabezado, 4 y 5 pares, 6 a 164 datos |
| Categorías | 500000001 | Rangos de index y tees por categoría |
| Campo de Golf | 1340114197 | Slope, rating y par por tee; códigos de equipo |
| Horario R1/R2/R3 simplificado | 498397437 / 634748170 / 634748171 | Armado manual de grupos |
| Horarios día 1/2/3 | 1238421915 / 16 / 17 | Horarios automáticos para imprimir |

### 4.2 Participants (fila 1 encabezado)

| Col. | Campo | Tipo | Fórmula / regla |
|---|---|---|---|
| A | Nombre Completo | carga | "APELLIDO, Nombres". **Clave** |
| B | Acreditado | casilla | |
| C | Name | fórmula | `=IFERROR(REGEXEXTRACT(TRIM(REGEXEXTRACT($A2;",\s*(.+)$"));"^\S+");"")` |
| D | Last Name | fórmula | `=IF($A2="";"";REGEXEXTRACT(TRIM(REGEXEXTRACT($A2;"^[^,]+"));"(?i)^(?:(?:da|de|del|do|dos|das|di|la|van|von)\s+)?\S+"))` |
| E | Index | carga | |
| F | Index verificado | casilla | |
| G | Date of Birth | carga | dd/mm/aaaa |
| H | Edad | fórmula | `=IF($G2="";"";DATEDIF(IF(ISNUMBER($G2);$G2;DATEVALUE($G2));DATE(2026;10;7);"Y"))` **(cambiar la fecha en 2027)** |
| I | Senior | fórmula | `=IF(AND($H2<>"";$H2>=55);"✔";"")` |
| J | Gender | carga | M / F |
| K | Country | carga | nombre en español |
| L | Flag | fórmula | `SWITCH` de nombre de país a emoji (solo para la planilla) |
| M | Equipo Nación | carga | debe existir en Campo de Golf H:I |
| N | Scratch | casilla | **Scratch del equipo Nación**, uno por equipo |
| O | Equipo Interclub | carga | |
| P | Suma Index | (libre) | |
| Q | Categoría | fórmula | `=IF(OR($E2="";$E2>30);"";IF($J2="F";"Damas";IFERROR(INDEX(FILTER('Categorías'!$A$4:$A$52;'Categorías'!$C$4:$C$52<=MIN($E2;25,9);'Categorías'!$D$4:$D$52>=MIN($E2;25,9);'Categorías'!$J$4:$J$52="Sí");1);"")))` |
| R | Tee Iberostar | fórmula | `INDEX` de Categorías por categoría y columna "Tee Iberostar Damas/Caballeros" según J |
| S | Hcp Iberostar | fórmula | `=IF(OR($R2="";$E2="");"";ROUND(MIN($E2;25,9)*VLOOKUP($R2;'Campo de Golf'!$B$4:$F$31;3;FALSE)/113+VLOOKUP($R2;'Campo de Golf'!$B$4:$F$31;4;FALSE)-VLOOKUP($R2;'Campo de Golf'!$B$4:$F$31;5;FALSE)))` |
| T | Tee Corales | fórmula | igual que R con "Tee Corales …" |
| U | Hcp Corales | fórmula | igual que S con T |
| V, W, X | R1 Hoyo, Hora, Pos | carga | salida R1 |
| Y | Control R1 | fórmula (encabezado) | `=VSTACK("Control R1";ARRAYFORMULA(IF(A2:A201="";"";IF((V2:V201="")+(W2:W201="")+(X2:X201="");"Falta salida";IF(COUNTIFS(V2:V201;V2:V201;W2:W201;W2:W201;X2:X201;X2:X201)>1;"Posición repetida";IF(COUNTIFS(V2:V201;V2:V201;W2:W201;W2:W201)>4;"Grupo de más de 4";"OK"))))))` |
| Z, AA, AB / AC | R2 Hoyo, Hora, Pos / Control R2 | | igual |
| AD, AE, AF / AG | R3 Hoyo, Hora, Pos / Control R3 | | igual |
| AH, AI, AL | Clave R1/R2/R3 (aux) | fórmula | `Hoyo|Hora|Pos` para los horarios |
| AJ | Cat. horario (aux) | fórmula | "SC" si N, "W" si Damas, si no la categoría |
| AK | País horario (aux) | fórmula | "(ARG)" vía Campo de Golf H:I |

### 4.3 Resultados

- Fila 1: título. Fila 2: instrucciones. Fila 3: encabezado. Fila 4: par Iberostar. Fila 5: par Corales.
- Datos: R1 filas 6–58, R2 59–111, R3 112–164 (53 por ronda, **en orden de salida**).

| Col. | Campo | Fórmula / regla |
|---|---|---|
| A | Ronda | R1/R2/R3 |
| B | Jugador (Nombre Completo) | igual a Participants A |
| C, D | Salida, Hora | |
| E:V | Hoyos 1–18 | validación 1–15; rojo en negrita bajo par |
| W | Ida | `=IF(COUNT(E6:M6)=9;SUM(E6:M6);"")` |
| X | Vuelta | `=IF(COUNT(N6:V6)=9;SUM(N6:V6);"")` |
| Y | Gross | `=IF(COUNT(E6:V6)=18;SUM(E6:V6);"")` |
| Z | Hcp juego | R1: `=IF(OR($A6="";$AF6="");"";$AF6)`. R2 y R3: Hcp base menos reducciones acumuladas (fórmula abajo) |
| AA | Neto | `=IF(AND(ISNUMBER($Y6);ISNUMBER($Z6));$Y6-$Z6;"")` |
| AB | Verificado | casilla |
| AC | **Estado** | `=IF($AB6;"-";"")`, se pisa a mano con DQ / NR / WD |
| AD | Index ronda | carga manual del Comité |
| AE | Index usado | último Index ronda cargado para ese jugador, o Participants E |
| AF | Hcp base | WHS con el tee de R (R1/R2) o T (R3) y el Index usado |

Hcp juego de R3 (fila 112), para copiar:
```
=IF(OR($A112="";$AF112="");"";IF($AD112<>"";$AF112;LET(netoUno;IFERROR(INDEX(FILTER($AA$6:$AA$58;$A$6:$A$58="R1";$B$6:$B$58=$B112);1);"");netoDos;IFERROR(INDEX(FILTER($AA$59:$AA$111;$A$59:$A$111="R2";$B$59:$B$111=$B112);1);"");manDos;IFERROR(INDEX(FILTER($AD$59:$AD$111;$A$59:$A$111="R2";$B$59:$B$111=$B112);1);"");dUno;IF(ISNUMBER(netoUno);netoUno-72;0);dDos;IF(ISNUMBER(netoDos);netoDos-72;0);redUno;IF(dUno<=-11;10;IFERROR(CHOOSE(-dUno-3;1;2;3;4;5;6;8);0));redDos;IF(dDos<=-11;10;IFERROR(CHOOSE(-dDos-3;1;2;3;4;5;6;8);0));$AF112-IF(manDos<>"";0;redUno)-redDos)))
```

Index usado (AE6):
```
=IF(OR($A6="";$B6="");"";LET(ronda;VALUE(MID($A6;2;1));base;IFERROR(INDEX(Participants!$E$2:$E$300;MATCH($B6;Participants!$A$2:$A$300;0));"");mUno;IFERROR(INDEX(FILTER($AD$6:$AD$300;$A$6:$A$300="R1";$B$6:$B$300=$B6);1);"");mDos;IF(ronda>=2;IFERROR(INDEX(FILTER($AD$6:$AD$300;$A$6:$A$300="R2";$B$6:$B$300=$B6);1);"");"");mTres;IF(ronda>=3;IFERROR(INDEX(FILTER($AD$6:$AD$300;$A$6:$A$300="R3";$B$6:$B$300=$B6);1);"");"");IF(mTres<>"";mTres;IF(mDos<>"";mDos;IF(mUno<>"";mUno;base)))))
```

Hcp base (AF6):
```
=IF(OR($AE6="";$B6="");"";IFERROR(LET(rw;MATCH($B6;Participants!$A$2:$A$300;0);tee;INDEX(IF($A6="R3";Participants!$T$2:$T$300;Participants!$R$2:$R$300);rw);ROUND(MIN($AE6;25,9)*VLOOKUP(tee;'Campo de Golf'!$B$4:$F$31;3;FALSE)/113+VLOOKUP(tee;'Campo de Golf'!$B$4:$F$31;4;FALSE)-VLOOKUP(tee;'Campo de Golf'!$B$4:$F$31;5;FALSE)));""))
```

**Pares 2026**
- Iberostar: 4 3 4 4 5 4 4 3 5 | 4 3 4 5 4 4 3 5 4 (36/36). Tomados de 18birdies, **no confirmados contra la tarjeta oficial.**
- Corales: 4 3 4 5 4 4 5 4 3 | 4 3 5 4 5 4 4 3 4 (36/36). Confirmados.

### 4.4 Categorías (fila 3 encabezado, filas 4–10)
Categoría | Jugadores (`=COUNTIF(Participants!$Q$2:$Q;$A4)`) | Index desde | Index hasta | Tee Iberostar Caballeros | Tee Corales Caballeros | Tee Iberostar Damas | Tee Corales Damas | Modalidad | Asignación automática (Sí/No) | Nota.
Filas: A, B, C, D, E (Sí), Damas (No, asignación por género), Scratch (No, mismos que la A, gross).

### 4.5 Campo de Golf
- B3:F11: Sitio de salida | Gender | Slope | Rating | Par.

| Campo | Tee | Gender | Slope | Rating |
|---|---|---|---|---|
| Iberostar | ⬛ Negro | Male | 122 | 71,8 |
| Iberostar | 🟦 Azul | Male | 116 | 69,3 |
| Iberostar | ⬜ Blanco | Male | 116 | 69,3 |
| Iberostar | 🟥 Rojo | Female | 111 | 66,5 |
| Corales | Fazio | Male | 131 | 74,6 |
| Corales | Corales | Male | 119 | 70,4 |
| Corales | Advantage | Male | 111 | 67,5 |
| Corales | Damas Forward | Female | 110 | 67,7 |

**Azul y Blanco de Iberostar tienen los mismos valores: verificar contra la tarjeta oficial.**
- H3:I15: Equipo Nación → código (Argentina ARG, Argentina B ARG B, Brasil BRA, Brasil B BRA B, Estados Unidos USA, México MEX, Paraguay PAR, Paraguay B PAR B, Venezuela VEN, República Dominicana DOM, Chile CHI).

### 4.6 Horarios
- **Simplificados (R1/R2/R3):** estáticos, los arma a mano el Comité. Hoyo | Hora | Jugador 1–4 con formato "KENT, Alexander (PAR) · SC". Colores para grupos que no se separan.
- **Días 1/2/3:** automáticos desde Participants V:AF, con fórmulas por celda (INDEX/SORT/UNIQUE/FILTER).
- 2026: R1 y R2 por tees 1 y 10, de 8:10 a 9:10, 14 grupos. R3 todos por el 1, de 8:30 a 10:40, ordenados por acumulado de R2 (del peor al mejor; primero 4 del tablero Scratch, luego A…). Buses del lobby a las 07:00, 07:40 y 08:00.

### 4.7 Hoja espejo pública
- Hoja nueva, pestaña "Resultados" (gid 0), compartida como "cualquiera con el link puede ver".
- A1: `=ARRAYFORMULA(TO_TEXT(IMPORTRANGE("<ID de la planilla principal>";"Resultados!A1:AF300")))`. Hay que autorizar el IMPORTRANGE una vez abriendo la hoja.
- La web la lee por `https://docs.google.com/spreadsheets/d/<ID>/gviz/tq?gid=0&headers=0&tqx=out:json;responseHandler:<cb>`.

---

## 5. Leaderboard web y TV

### 5.1 Arquitectura

```
Scorers ──carga──▶ Planilla principal (Resultados)
                          │ IMPORTRANGE
                          ▼
                  Hoja espejo pública ──gviz JSONP cada 90 s──▶ Web / TV (GitHub Pages)
                          
Respaldo cada ~10 min (tarea programada de Claude):
  lee Resultados → compact.txt → pub_update.py → build_site.py → commit + push
  (data.json y HTML con datos embebidos: si gviz falla, el sitio muestra lo último publicado)
```

- Sitio estático en GitHub Pages: `index.html` (web), `tv.html` y `tv/index.html` (TV), `data.json` y `tv/data.json`, `release.txt`, `og.png`, `CNAME`, `.nojekyll`, `robots.txt` (Disallow all + meta noindex).
- Dominio propio `leaderboard.latinoamericano.golf` (archivo CNAME en el repo). El DNS del subdominio lo configuró Diego el 7/10; el detalle del registro no quedó documentado: confirmarlo con quien administre latinoamericano.golf.

### 5.2 Código fuente (en `kit/web/`)

| Archivo | Qué es |
|---|---|
| `app3.js` | Toda la lógica: lectura de participantes y resultados por encabezado (`ingestParticipants`, `ingestResults`), cálculo por ronda, reducción (`reduction`), ranking (`standing`, `rank`, `tieVec`), equipos (`teamRound`, `teamKey`, `teamRanked`), medallero (`majority`, `countryTiebreak`), campeones (`FINAL`), banderas SVG (`SVGF`), datos en vivo (`startLive`, `LIVE_ID`) |
| `head3.html` | CSS y tokens de diseño |
| `body3.html` | Cabecera con `__LOGO__`, selector de ronda, navegación por categoría, pie |
| `tv/tv.js`, `tv/tv.css`, `tv/tv.html` | Versión TV |
| `build_public.py` | Arma `leaderboard-publico.html` con datos embebidos y `startLive` |
| `build_tv.py` | Arma `leaderboard-tv.html` y `tv_data.json` |
| `build_site.py` | Envuelve con doctype, metas Open Graph y PWA, y copia al repo |
| `build_comite.py` | Versión del Comité con conector MCP (opcional) |
| `pub_update.py` | Valida sumas, genera `pub_results_live.json`, sube `release.txt` y corre los dos builds |
| `r3sync.py` | Actualiza las filas R3 de `compact.txt` desde Resultados (**corregir: buscar Estado por encabezado**) |
| `rank.py`, `tvtest.py`, `audit.py` | Pruebas y auditoría visual |
| `og.html` | Fuente de la imagen para compartir (1200×630) |

Datos (`kit/datos/`): `pub_participants.json` (snapshot de Participants, columnas KEEP), `compact.txt` (una línea por tarjeta: `R1|NOMBRE, Nombre|18 hoyos separados por coma|gross|estado|index_ronda|hcp_base`), `roster.json` (fallback), `max_round.txt` (última ronda habilitada), `logo.datauri.txt` (renombrar a `logo.datauri` en la carpeta padre de `web/`), `logo.png`, `icon.png`, `og.png`.

### 5.3 Cómo se construye y publica

```bash
# estructura esperada
proyecto/
  logo.datauri            # data URI del logo (kit/datos/logo.datauri.txt)
  lb/                     # contenido de kit/web + kit/datos
    app3.js head3.html body3.html tv/ ... pub_participants.json compact.txt roster.json max_round.txt og.png
# repo del sitio clonado en /home/claude/cl2026 (o cambiar SITE y RF en build_site.py y pub_update.py)

cd proyecto/lb
python3 pub_update.py compact.txt "07/10 12:30"   # valida, sube release, arma web y TV
python3 build_site.py /ruta/al/repo               # copia al repo
cd /ruta/al/repo && git add -A && git commit -m "Resultados 12:30" && git push
```

- `pub_participants.json` se obtiene leyendo `Participants!A1:U201` (valores) y guardando el JSON tal cual (`build_public.py` se queda solo con las columnas KEEP; nunca publica fecha de nacimiento).
- Mensajes de commit: "Resultados HH:MM" para datos; descripción en español para cambios de código.
- Antes de cada ciclo: `git pull --rebase`. Si hay conflicto: `rebase --abort`, `fetch`, `reset --soft FETCH_HEAD`, commit, push. Si el push falla 3 ciclos seguidos, avisar.

### 5.4 Web: comportamiento acordado
- Cabecera fija que se achica; pastilla de ronda; selector de categoría.
- Orden de secciones: Naciones, Scratch, A–E, Damas, Interclubes, Resultados/Campeones, Medallero.
- Vista por defecto: la última ronda con scores. El Total es el acumulado de las rondas jugadas; el orden es por score vs. par acumulado (un −5 con solo R1 va arriba de un −4 con R1+R2).
- Colores: rojo bajo par, verde en par, ambos en negrita (scores de 72 o menos en negrita).
- Naciones: Scratch siempre en negrita, descarte tachado en rojo sobre gris; equipos colapsados (abiertos en la TV).
- "S" para Senior; estrella dorada al mejor Senior en R3/Total. Copa solo al campeón final.
- Tarjeta hoyo a hoyo al tocar un jugador: círculo birdie, cuadrado bogey.
- Tocar el logo recarga con `?t=` para saltar la caché.
- Sponsor 2026: Seguridad Seguros junto a Paraguay en Naciones.

### 5.5 TV
- 1920×1080 escalado. Hash: `#r1`, `#r2`, `#r3`, `#total`; sin hash, la última ronda con datos. `#min` muestra equipos cerrados.
- Rotación: 8 s por pantalla, 12 s Naciones, Interclubes y Medallero; 14 filas por pantalla.
- Pantalla completa con toque o F/Enter; cursor oculto; `wakeLock`.
- Consulta `../release.txt` cada 3 min y se recarga solo si el número subió, manteniendo la diapositiva.

### 5.6 Diseño
- Azul marino `#0e356b`, azul `#174d99`, cian `#00cfff`.
- Bajo par `#c8102e`, en par `#0f7a52`, descarte `#a3afbf`, fondos `#e6eef8` / `#f4f7fb`, texto apagado `#5a6b82`.
- Dorado `#c9a227`; amarillo podio `#f5c518`; plata `#cfd6df`; bronce `#cd7f45`.
- Fuentes: Kumbh Sans (títulos), Varela Round (subtítulos), Montserrat (texto). Impresos con reportlab: Poppins.
- Logo XVIII Edición (Golf Digest / TaylorMade) en `kit/datos/logo.png`. **Para 2027 hay que pedir el logo nuevo.**

---

## 6. Operación

### 6.1 Antes del torneo (T−30 a T−1)
1. Cerrar inscripción en la planilla de **Inscripción 2027** y pasar los datos a una copia nueva de la Planilla de Golfistas (sección 10).
2. Verificar index en la federación (columna Index verificado) y equipos (Equipos: 4 jugadores, 1 Scratch por equipo Nación).
3. Cargar campos, tees, slope, rating y pares **contra la tarjeta oficial**.
4. Armar horarios R1/R2 con el Comité; revisar Control R1/R2 = OK.
5. Generar filas de Resultados por ronda en orden de salida.
6. Crear la hoja espejo pública y autorizar el IMPORTRANGE.
7. Repo + Pages + dominio. Publicar con datos vacíos; probar web a 390 px y TV en la pantalla real.
8. Imprimir: horarios, planilla del starter por tee, stickers para tarjetas, reglas locales.
9. Borrar datos de prueba el día anterior.

### 6.2 Cada ronda
1. Regenerar `pub_participants.json` y comparar Hcp con la Sheet.
2. Habilitar la ronda (`max_round.txt`) con autorización del Comité.
3. Durante la ronda: los scorers cargan E:V, tildan Verificado y, si corresponde, Estado (WD/DQ/NR). La web se actualiza sola cada 90 s; el respaldo cada 10 min.
4. Al terminar: revisar tarjetas sin Verificado, scores por encima del máximo por hoyo, nombres que no coinciden.
5. Para la ronda siguiente: horarios (R3 por acumulado), stickers, reducciones de hcp aplicadas, Index ronda si el Comité asigna uno.

### 6.3 Cierre
1. Confirmar desempates del 1.º (muerte súbita) y cualquier decisión del Comité.
2. Declarar el torneo cerrado: el sitio pasa de "provisorio" a "final".
3. Correr `awards.js` (sección 8) para obtener podios, Seniors, equipos y Últimos 18, y **verificar a mano contra el reglamento**.
4. Generar la guía de entrega de premios y el Cuadro de Honor.

### 6.4 Tareas programadas de 2026
Se usaron tareas de Claude con `send_later` encadenado ("Leaderboard R1/R2/R3 · ciclo 10 min"), atadas a la computadora de Diego. Ya no queda ninguna activa. Para 2027, si se repite, el prompt de cada ciclo hace: leer Resultados por rango → actualizar `compact.txt` → `pub_update.py` → `build_site.py` → commit "Resultados HH:MM" → push, sin avisar salvo error.

---

## 7. Impresos y gráficas

Todo se genera con HTML + Playwright (Chromium) o reportlab. Comando base: `NODE_PATH=$(npm root -g) node script.js`.

| Material | Fuente en `kit/` | Detalle |
|---|---|---|
| Horarios por ronda | `impresos/horarios/` (`tt2.py`, `build2.py`, `horarios.html`, `gen3c.py`, `rows3.py`) | Prefijo CL, un PDF por ronda, tees en singular, país entre paréntesis en negrita, sin "tentativo" |
| Planilla del starter | `impresos/horarios/starter.py` | Una por tee de salida, columna "Check" |
| Stickers para tarjetas | `impresos/stickers/make_r1.py`, `make_r2.py`, `make_r3.py` | Avery 8162/5162 (Letter, 2×7, 4"×1⅓"; TOP 59,95 pt, LEFT 11,2 pt, PITCH_X 301,5 pt): hoyo, hora, tee, hcp de juego, categoría y país, en orden de salida |
| Guía de entrega de premios | `impresos/premios/premios.html` + `pdf.js` | A4, letra grande, premios numerados con casilla y conteo de medallas |
| Cuadro de Honor (WhatsApp) | `impresos/premios/premiados.html` + `pdf2.js` | Página 120×250 mm, lo más importante arriba, nombres completos con bandera, sin decir qué premio recibe cada uno. PNG con `pdftoppm -png -scale-to-x 1080 -scale-to-y -1` |
| Gráfica campeón Naciones | `impresos/premios/br.html` (1080×1350) y `story.html` (1080×1920) + `shot.js` | Logo, rondas y los 4 jugadores |

- Banderas en impresos: paquete npm `flag-icons@7.2.3` (SVG embebidos como data URI).
- Orden de la ceremonia 2026: Últimos 18 → Interclubes → Seniors → Damas → E → D → C → B → A → Scratch → Naciones, llamando 3.º, 2.º y 1.º.
- Materiales 2026: 15 oros, 16 platas, 11 bronces, 6 platos y 6 vasos térmicos (5 + Damas; la guía impresa decía 5, faltó un juego).

---

## 8. Cálculo de premios (`kit/impresos/premios/awards.js`)

Abre el `index.html` publicado con Playwright y usa las mismas funciones del sitio.

```bash
NODE_PATH=$(npm root -g) node awards.js /ruta/al/repo/index.html > awards.json
```

Devuelve: podio Scratch, podios por categoría, Senior por categoría, top 3 de Naciones e Interclubes, y Últimos 18 con ganador y top 8 por categoría (A–E y Damas), marcando `otroPremio`. La versión del kit ya tiene la regla final (no usa la columna Scratch; excluye cualquier premio; fila Damas). Resultado de control con los datos 2026: A Da Silva 71, B Matos 72, C Fiore Bogarín 78, D Barros 78, E Piazza 77, Damas Mija Kim 85.

**Siempre revisar a mano** los equipos con WD, los empates y los jugadores con WD en rondas anteriores.

---

## 9. Resultados finales 2026 (histórico)

| Clasificación | 1.º | 2.º | 3.º |
|---|---|---|---|
| Naciones | Brasil +20 / 668 (Machado, Soonwook, Massao Kanesaki, Suin) | Argentina +24 (Merlini, García, Fiocca, Curat Vallenilla) | Paraguay +28 (Kent, Storm Plate, Ávila Corvalán, Guerreros) |
| Scratch | Merlini E (216) | Machado +4 | Mohseni Sebastián +11 |
| A | Mohseni Sebastián −2 | Molina Maioli +7 | Merlini +9 |
| B | Valderrama +6 | Paniagua +10 | Dutkiewicz +11 |
| C | Massao Kanesaki +3 | Schemel +11 | Alves +19 |
| D | Kim Mario Ricardo +5 | Hipólito +9 | Aguado +12 |
| E | Severo +4 | Guerreros +5 | Dah-Yuan +12 |
| Damas | García +14 | Kyoung-Aie +17 | Maioli Bartoletti +35 |
| Interclubes | Guarapiranga +25 / 673 (Alves, Schemel, Kim Mario Ricardo, Kim Thiago) | Centenario III +28 | Federacao +34 |

- Seniors: A Amengual, B Paniagua, C Alves, D Kim Mario Ricardo, E Kim Thiago.
- Últimos 18: A Da Silva 71, B Matos 72, C Fiore Bogarín 78, D Barros 78, E Piazza 77, Damas Mija Kim 85.
- 53 jugadores, 4 WD.

---

## 10. Checklist para 2027: qué cambiar y dónde

### 10.1 Datos de la edición
| Dato | Dónde se cambia |
|---|---|
| Edición (XIX), año, sede, fechas | Inscripción 2027 → "Edición 2027"; `build_site.py` (títulos, descripción OG, `apple-mobile-web-app-title`); `body3.html` (cabecera y pie: "Punta Cana · 7 al 9 de octubre de 2026", campos, "2026"); `tv/tv.html` y `tv/tv.js` (cabecera y pie); `og.html`; impresos (títulos) |
| Fecha de inicio para la edad | Participants H: `DATE(2026;10;7)` → nueva fecha |
| Campos y tees | Campo de Golf B:F (slope, rating, par por tee); Categorías E:H (tee por categoría); encabezados "Tee Iberostar/Corales" en Participants R:U y en las fórmulas de AF de Resultados (usan R para R1/R2 y T para R3) |
| Pares hoyo a hoyo | Resultados filas 4 y 5 (la web los toma de ahí); `pub_update.py` (listas `PI` y `PC`); `app3.js` línea 43 (`PARS`, valores por defecto) |
| Qué ronda va en qué campo | fórmula AF de Resultados (`IF($A6="R3";T;R)`); `app3.js` línea 45 (`COURSE`) y línea 56 (detecta "CORALES" en la fila Par) |
| Logo | `logo.datauri`, `logo.png`, `icon.png`, artifact del Comité |
| Dominio y repo | `CNAME`, `BASE` en `build_site.py`, rutas `SITE` y `RF` |
| Hoja espejo pública | `LIVE_ID` en `app3.js` |
| Países nuevos | `app3.js`: `FLAGS` y `SVGF` (líneas 17–18), `CODE` (línea 30), `CNAME` (línea 246); `SWITCH` de Participants L; códigos en Campo de Golf H:I |
| Sponsor | `app3.js` / `head3.html` (logo junto al equipo) |
| Reglamento | Condiciones 2027: revisar desempate "últimos 9" con salida por el 10, medallero de Interclubes mixtos, score máximo por hoyo |

### 10.2 Pasos en orden
1. **Inscripción:** cargar jugadores en la planilla Inscripción 2027. Completar "Edición 2027" cuando se confirme el campo y la fecha.
2. **Copiar la Planilla de Golfistas 2026** (Archivo → Hacer una copia), renombrar a 2027 y vaciar: Participants A:B, E:G, J:K, M:O, V:X, Z:AB, AD:AF; Resultados E:V, AB:AD de las filas de datos; horarios simplificados.
3. **Pasar inscriptos** de Inscripción 2027 a Participants según el "Diccionario de campos" (Nombre Completo → A, Index → E, Fecha de nacimiento → G, Género → J, País → K, Equipo Nación → M, Scratch del equipo → N, Equipo Interclub → O).
4. **Cambiar campos, tees, pares** (10.1). Cambiar la fecha de la edad.
5. **Ajustar la cantidad de filas de Resultados** a la cantidad de jugadores (53 por ronda en 2026: las fórmulas de R3 referencian `$A$6:$A$58` y `$A$59:$A$111`; si cambia la cantidad, actualizar esos rangos).
6. **Hoja espejo nueva** (o reapuntar el IMPORTRANGE) y `LIVE_ID`.
7. **Repo nuevo** (por ejemplo `cl2027`), Pages, dominio. Versionar también el código fuente (`src/`) para no depender de una carpeta temporal.
8. **Arreglos pendientes en el código:** `r3sync.py` por encabezado; validación de score máximo; columna de control de nombres; desempate de Naciones 2.º/3.º; medallero de Interclubes mixtos.
9. **Prueba completa** con datos de demo: web a 390 px, TV en la pantalla, impresos. Borrar el demo el día anterior.

---

## 11. Planilla de Inscripción 2027

[Abrir la planilla Inscripción 2027](https://docs.google.com/spreadsheets/d/1T0Bx4MLdUgwn3ETg3G7i_l8D2szI6R9eZW3W6nCWNVg/edit)

| Pestaña | Contenido |
|---|---|
| Inscripciones | Un jugador por fila desde la fila 5. Encabezado amarillo = cargar; azul = automático |
| Edición 2027 | Sede, campos y fechas (**a definir**), index máximo, edad Senior, mínimos por categoría, tamaño de equipos |
| Categorías | Rangos de index 2026 para estimar la categoría |
| Equipos | Equipos Nación e Interclub, con control de cantidad de jugadores y de Scratch |
| Diccionario de campos | Qué va en cada columna y a qué columna de Participants pasa |

Columnas de Inscripciones: Nº · Apellidos · Nombres · **Nombre Completo** (automático, "APELLIDOS, Nombres") · Género (M/F) · Fecha de nacimiento · **Edad al inicio** · **Senior** · País · Club · Email · Teléfono / WhatsApp · Index WHS · Fecha del Index · Index verificado · **Categoría estimada** · Equipo Nación · Scratch del equipo · Equipo Interclub · Estado (Pendiente/Confirmada/Baja) · Pago recibido · Fecha de inscripción · Observaciones.

- La edad y el Senior se calculan cuando se carga la fecha de inicio en "Edición 2027".
- La categoría estimada usa el index con tope 25,9; con index mayor a 30 dice "No admitido"; las damas van a "Damas".
- Los campos son una propuesta: se pueden agregar o quitar columnas sin romper nada siempre que no se muevan las de fórmula (A, D, G, H, P).

---

## 12. Pendientes abiertos de 2026

1. **Soares, R1, hoyo 16 (par 3):** anotó 9, por encima del máximo de 8. Su R1 debería ser 113. No cambia posiciones. Sin corregir en la Sheet.
2. **Últimos 18 A:** si en la ceremonia se entregó a Vera, el premio correspondía a Fernando Augusto Da Silva (71 neto).
3. **Guía de entrega de premios:** la versión impresa decía Vera y no incluía la fila Damas (Mija Kim).
4. **"Gil Hipólito":** la planilla dice HIPOLITO sin tilde; confirmar.
5. **Pares de Iberostar y slope/rating de Azul y Blanco:** sin verificar.
6. **Medallero de Interclubes mixtos** y **desempate 2.º/3.º de Naciones:** sin implementar según reglamento.

---

## 13. Contenido de `kit/`

```
kit/
  CL_Manual_del_Sistema.md          este documento
  web/                              app3.js, head3.html, body3.html, tv/, build_*.py, pub_update.py, r3sync.py, rank.py, tvtest.py, audit.py, og.html
  datos/                            pub_participants.json, compact.txt, roster.json, max_round.txt, logo.datauri.txt, logo.png, icon.png, og.png
  impresos/horarios/                tt2.py, build2.py, horarios.html, starter.py, gen3c.py, rows3.py, make_r3.py
  impresos/stickers/                make_r1.py, make_r2.py, make_r3.py
  impresos/premios/                 awards.js, premios.html, premiados.html, br.html, story.html, pdf.js, pdf2.js, shot.js, shot2.js
  comite/comite-campeonato.html     fuente del artifact del Comité
```

Los scripts de horarios y stickers leen JSON exportados de la Sheet (`get_values` de Participants o de los horarios simplificados) y tienen rutas de la máquina de 2026: revisar las primeras líneas de cada uno antes de usarlos.
