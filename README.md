# Proyecto_Programacion_2: análisis exploratorio de jugadores de FIFA 21

Análisis exploratorio de una muestra de 2000 jugadores de FIFA 21 con Python y pandas: carga e inspección, datos faltantes, outliers, valores inconsistentes y duplicados, creación de variables, filtrado, agrupación, visualizaciones y conclusiones.

## Integrantes
- Samuel Marroquin Figueroa (Integrante A)
- Sofia Alba Larrota (Integrante B)

## Fuente de los datos
Dataset [FIFA 21 Messy, Raw Dataset For Cleaning/Exploring](https://www.kaggle.com/datasets/yagunnersya/fifa-21-messy-raw-dataset-for-cleaning-exploring) en Kaggle. Contiene datos de los jugadores del videojuego FIFA 21 extraídos de (https://sofifa.com): identificación y perfil, club y contrato, valoraciones, valor de mercado y salario, y atributos técnicos, físicos y de portería. El dataset completo tiene 18 979 jugadores y 77 columnas; este proyecto trabaja con una muestra de 2000 jugadores con la misma estructura (`fifa21_muestra_2000.csv`).

## Estructura de los datos
- **Registros:** 2000. Cada fila representa **un jugador** de FIFA 21, identificado por `ID`.
- **Variables:** 77 en el archivo original y **79** en la base final (se elimina `Loan Date End` y se crean `IMC`, `Margen_crecimiento` y `Categoria_edad`). La base final no tiene valores faltantes ni registros duplicados.
- **Tipos de variables (base final):** 13 categóricas, 6 numéricas continuas, 59 numéricas discretas y 1 de tipo fecha (`Joined`).
  - *Categóricas:* identificadores y etiquetas (`ID`, nombres, URLs), `Nationality`, `Positions`, `BP`, `foot`, `A/W`, `D/W`, `Team & Contract` y `Categoria_edad`.
  - *Continuas:* `Height`, `Weight`, `Value`, `Wage`, `Release Clause` e `IMC`.
  - *Discretas:* `Age`, las valoraciones (`↓OVA`, `POT`, `BOV`), los atributos con sus totales, `Hits` y las estrellas (`W/F`, `SM`, `IR`), todos números enteros.

### Cambios entre la base original y la final

| Cambio | Columnas | Detalle |
|---|---|---|
| Eliminada | `Loan Date End` | Tenía 1890 faltantes (94,5 %): solo aplica a los 110 jugadores cedidos |
| Texto limpiado | todas las de texto | Se quitan espacios y saltos de línea sobrantes |
| Convertida a número | `Hits` | De texto (`1.1K`) a decimal (`1100.0`) |
| Convertida a centímetros | `Height` | De pies y pulgadas (`5'8"`) a entero en cm |
| Convertida a kilogramos | `Weight` | De libras (`146lbs`) a entero en kg |
| Convertidas a euros | `Value`, `Wage`, `Release Clause` | De texto (`€1.5M`, `€250K`) a decimal en euros |
| Convertidas a entero | `W/F`, `SM`, `IR` | De `3 ★` / `3★` a `3` |
| Convertida a fecha | `Joined` | De texto a `datetime` |
| Creadas | `IMC`, `Margen_crecimiento`, `Categoria_edad` | Ver el diccionario |

### Particularidades de los datos
- **Ceros que significan «sin valor»:** hay 27 jugadores con `Value` = 0, 26 con `Wage` = 0 (los 26 agentes libres) y 137 con `Release Clause` = 0. Un cero aquí quiere decir que la fuente no asigna valor, no que el jugador valga 0 €.
- **`Team & Contract` mezcla varios datos en un texto:** 26 agentes libres (el texto empieza con un país y termina en `Free`), 110 cedidos (terminan en `On Loan`) y el resto con los años del contrato (`Club AAAA ~ AAAA`).
- **`BP` y `Positions`:** en 342 jugadores la mejor posición no aparece en la lista `Positions`; se conserva como viene en la fuente.
- **Homónimos:** 18 valores de `Name` y 1 de `LongName` (*Nicolás Fernández*) se repiten, pero son jugadores distintos; se identifican por `ID`.
- **Totales de atributos:** `Mentality` no incluye `Composure`, y `Total Stats` es la suma de los siete totales.
- **Nombre de columna con símbolo:** la valoración general se llama `↓OVA`, tal como viene en la fuente.

## Diccionario de datos
Tipos y valores de la base **final** (después de ejecutar `analisis.py`), agrupados por tema.

**Identificación y perfil**

| Variable | Tipo | Descripción | Valores / unidades |
|---|---|---|---|
| `ID` | Categórica | Identificador único del jugador en Sofifa | 2000 valores distintos |
| `Name` | Categórica | Nombre corto del jugador (el que aparece en el juego) | 1982 valores distintos |
| `LongName` | Categórica | Nombre completo del jugador | 1999 valores distintos |
| `Age` | Numérica discreta | Edad en años | 16 a 53 años |
| `Nationality` | Categórica | País de la selección del jugador | 124 valores distintos |
| `Height` | Numérica continua | Estatura en **centímetros** (en el original venía en pies y pulgadas, ej. `5'8"`) | 160 a 203 cm |
| `Weight` | Numérica continua | Peso en **kilogramos** (en el original venía en libras, ej. `146lbs`) | 55 a 103 kg |
| `foot` | Categórica | Pie dominante (`Right` / `Left`) | `Right` (1536), `Left` (464) |
| `Positions` | Categórica | Posiciones en las que puede jugar, separadas por espacio (ej. `CM CDM`) | 256 valores distintos |
| `BP` | Categórica | Mejor posición del jugador (*Best Position*); puede no aparecer en `Positions` | `CB` (383), `ST` (282), `CAM` (258), `GK` (224), `CDM` (153), `RM` (147), `RB` (115), `LB` (112), `CM` (103), `LM` (93), `RW` (44), `RWB` (36), `LWB` (26), `LW` (16), `CF` (8) |
| `photoUrl` | Categórica | URL de la foto del jugador | 2000 valores distintos |
| `playerUrl` | Categórica | URL de la ficha del jugador en Sofifa | 2000 valores distintos |

**Club y contrato**

| Variable | Tipo | Descripción | Valores / unidades |
|---|---|---|---|
| `Team & Contract` | Categórica | Club y vigencia del contrato en un solo texto. Tres formatos: `Club AAAA ~ AAAA` (contrato), `Club Mes D, AAAA On Loan` (cedido, con la fecha de fin del préstamo) y `País Free` (agente libre; en estos casos el primer valor es un país, no un club) | 1728 valores distintos |
| `Joined` | Fecha | Fecha en que el jugador se unió a su club | 2005-07-01 a 2020-10-08 |

**Valoración y mercado**

| Variable | Tipo | Descripción | Valores / unidades |
|---|---|---|---|
| `↓OVA` | Numérica discreta | Valoración general (*overall*) del jugador. El símbolo ↓ viene de la fuente y se conserva en el nombre | 47 a 91 puntos |
| `POT` | Numérica discreta | Potencial: valoración máxima que se estima que alcanzará | 48 a 95 puntos |
| `BOV` | Numérica discreta | Mejor valoración general del jugador (*Best Overall Rating*) | 48 a 91 puntos |
| `Growth` | Numérica discreta | Margen de crecimiento: `POT` − `↓OVA` | 0 a 25 puntos |
| `Value` | Numérica continua | Valor de mercado estimado, en **euros** (en el original venía como `€250K`, `€1.5M`). 0 = sin valor asignado | 0 a 105 500 000 € |
| `Wage` | Numérica continua | Salario en **euros** (en el original venía como `€1K`). 0 = sin salario asignado | 0 a 370 000 € |
| `Release Clause` | Numérica continua | Cláusula de rescisión en **euros**. 0 = sin cláusula asignada | 0 a 203 100 000 € |
| `Hits` | Numérica discreta | Popularidad de la ficha del jugador en Sofifa (número de visitas; en el original venía como texto, ej. `1.1K`) | 1 a 1 900 visitas |

**Resumen de atributos**

| Variable | Tipo | Descripción | Valores / unidades |
|---|---|---|---|
| `PAC` | Numérica discreta | Ritmo (*pace*) | 25 a 96 puntos |
| `SHO` | Numérica discreta | Tiro (*shooting*) | 20 a 86 puntos |
| `PAS` | Numérica discreta | Pase (*passing*) | 25 a 93 puntos |
| `DRI` | Numérica discreta | Regate (*dribbling*) | 28 a 91 puntos |
| `DEF` | Numérica discreta | Defensa (*defending*) | 15 a 90 puntos |
| `PHY` | Numérica discreta | Físico (*physical*) | 31 a 91 puntos |
| `Base Stats` | Numérica discreta | Suma de `PAC` + `SHO` + `PAS` + `DRI` + `DEF` + `PHY` | 239 a 485 puntos |
| `Total Stats` | Numérica discreta | Suma de los siete totales: `Attacking`, `Skill`, `Movement`, `Power`, `Mentality`, `Defending`, `Goalkeeping` | 786 a 2 304 puntos |

**Atributos de ataque**

| Variable | Tipo | Descripción | Valores / unidades |
|---|---|---|---|
| `Attacking` | Numérica discreta | Total de ataque: suma de `Crossing`, `Finishing`, `Heading Accuracy`, `Short Passing`, `Volleys` | 42 a 409 puntos |
| `Crossing` | Numérica discreta | Centros | 7 a 94 puntos |
| `Finishing` | Numérica discreta | Definición | 3 a 91 puntos |
| `Heading Accuracy` | Numérica discreta | Precisión de cabeza | 5 a 89 puntos |
| `Short Passing` | Numérica discreta | Pase corto | 12 a 94 puntos |
| `Volleys` | Numérica discreta | Voleas | 4 a 90 puntos |

**Atributos de habilidad**

| Variable | Tipo | Descripción | Valores / unidades |
|---|---|---|---|
| `Skill` | Numérica discreta | Total de habilidad: suma de `Dribbling`, `Curve`, `FK Accuracy`, `Long Passing`, `Ball Control` | 55 a 441 puntos |
| `Dribbling` | Numérica discreta | Regate (atributo individual) | 5 a 92 puntos |
| `Curve` | Numérica discreta | Efecto | 7 a 89 puntos |
| `FK Accuracy` | Numérica discreta | Precisión en tiros libres | 7 a 89 puntos |
| `Long Passing` | Numérica discreta | Pase largo | 11 a 93 puntos |
| `Ball Control` | Numérica discreta | Control de balón | 9 a 92 puntos |

**Atributos de movimiento**

| Variable | Tipo | Descripción | Valores / unidades |
|---|---|---|---|
| `Movement` | Numérica discreta | Total de movimiento: suma de `Acceleration`, `Sprint Speed`, `Agility`, `Reactions`, `Balance` | 135 a 458 puntos |
| `Acceleration` | Numérica discreta | Aceleración | 15 a 96 puntos |
| `Sprint Speed` | Numérica discreta | Velocidad punta | 15 a 96 puntos |
| `Agility` | Numérica discreta | Agilidad | 15 a 93 puntos |
| `Reactions` | Numérica discreta | Reacciones | 32 a 92 puntos |
| `Balance` | Numérica discreta | Equilibrio | 20 a 95 puntos |

**Atributos de potencia**

| Variable | Tipo | Descripción | Valores / unidades |
|---|---|---|---|
| `Power` | Numérica discreta | Total de potencia: suma de `Shot Power`, `Jumping`, `Stamina`, `Strength`, `Long Shots` | 152 a 422 puntos |
| `Shot Power` | Numérica discreta | Potencia de tiro | 20 a 91 puntos |
| `Jumping` | Numérica discreta | Salto | 29 a 93 puntos |
| `Stamina` | Numérica discreta | Resistencia | 16 a 95 puntos |
| `Strength` | Numérica discreta | Fuerza | 24 a 94 puntos |
| `Long Shots` | Numérica discreta | Tiros de larga distancia | 4 a 92 puntos |

**Atributos de mentalidad**

| Variable | Tipo | Descripción | Valores / unidades |
|---|---|---|---|
| `Mentality` | Numérica discreta | Total de mentalidad: suma de `Aggression`, `Interceptions`, `Positioning`, `Vision`, `Penalties` (**no incluye** `Composure`) | 63 a 421 puntos |
| `Aggression` | Numérica discreta | Agresividad | 12 a 93 puntos |
| `Interceptions` | Numérica discreta | Intercepciones | 5 a 91 puntos |
| `Positioning` | Numérica discreta | Colocación | 3 a 91 puntos |
| `Vision` | Numérica discreta | Visión de juego | 11 a 94 puntos |
| `Penalties` | Numérica discreta | Penales | 8 a 92 puntos |
| `Composure` | Numérica discreta | Compostura | 14 a 92 puntos |

**Atributos de defensa**

| Variable | Tipo | Descripción | Valores / unidades |
|---|---|---|---|
| `Defending` | Numérica discreta | Total de defensa: suma de `Marking`, `Standing Tackle`, `Sliding Tackle` | 24 a 272 puntos |
| `Marking` | Numérica discreta | Marca | 3 a 94 puntos |
| `Standing Tackle` | Numérica discreta | Entrada de pie | 6 a 90 puntos |
| `Sliding Tackle` | Numérica discreta | Entrada deslizante | 7 a 88 puntos |

**Atributos de portería**

| Variable | Tipo | Descripción | Valores / unidades |
|---|---|---|---|
| `Goalkeeping` | Numérica discreta | Total de portería: suma de `GK Diving`, `GK Handling`, `GK Kicking`, `GK Positioning`, `GK Reflexes` | 15 a 416 puntos |
| `GK Diving` | Numérica discreta | Estirada (portero) | 3 a 86 puntos |
| `GK Handling` | Numérica discreta | Manejo de balón (portero) | 2 a 84 puntos |
| `GK Kicking` | Numérica discreta | Saque (portero) | 2 a 87 puntos |
| `GK Positioning` | Numérica discreta | Colocación (portero) | 2 a 91 puntos |
| `GK Reflexes` | Numérica discreta | Reflejos (portero) | 3 a 88 puntos |

**Valoraciones por estrellas y ritmo de trabajo**

| Variable | Tipo | Descripción | Valores / unidades |
|---|---|---|---|
| `W/F` | Numérica discreta | Habilidad con el pie malo (*Weak Foot*), de 1 a 5 estrellas (en el original venía como `3 ★`) | 1 a 5 estrellas |
| `SM` | Numérica discreta | Movimientos de habilidad (*Skill Moves*), de 1 a 5 estrellas (en el original venía como `3★`) | 1 a 5 estrellas |
| `IR` | Numérica discreta | Reputación internacional (*International Reputation*), de 1 a 5 estrellas (en la muestra, de 1 a 4) | 1 a 4 estrellas |
| `A/W` | Categórica | Ritmo de trabajo en ataque (*Attacking Work Rate*): `Low`, `Medium` o `High` | `Medium` (1356), `High` (540), `Low` (104) |
| `D/W` | Categórica | Ritmo de trabajo en defensa (*Defensive Work Rate*): `Low`, `Medium` o `High` | `Medium` (1474), `High` (331), `Low` (195) |

**Variables creadas**

| Variable | Tipo | Descripción | Valores / unidades |
|---|---|---|---|
| `IMC` | Numérica continua | **Variable creada.** Índice de masa corporal: `Weight / (Height / 100)²`, redondeado a 2 decimales | 18.39 a 29.76 kg/m² |
| `Margen_crecimiento` | Numérica discreta | **Variable creada.** `POT` − `↓OVA`. Coincide con `Growth` | 0 a 25 puntos |
| `Categoria_edad` | Categórica | **Variable creada.** Rango de edad: `Joven` (hasta 21), `Adulto` (22 a 29) y `Veterano` (30 o más) | `Adulto` (1093), `Joven` (493), `Veterano` (414) |

## Organización del repositorio
- `analisis.py`: solución final del proyecto (ítems 1 a 9).
- `cuadernos/`: cuadernos de exploración de cada integrante.
- `Datos/`: base de datos (`fifa21_muestra_2000.csv`), muestra de 2000 jugadores del dataset de Kaggle.
- `README.md`: documentación de los datos (ítem 10).

## Conclusiones
1. (Integrante A) **Calidad de los datos:** la muestra de 2000 jugadores de FIFA 21 llegó casi completa. La única variable con muchos faltantes, Loan Date End (94,5 %), se eliminó, y no se encontraron registros duplicados. El principal trabajo de limpieza fue convertir a números las columnas que venían como texto, como Height, Weight, Value y Wage.
2. (Integrante B) **Formato inconsistente, no duplicados:** la base no tenía registros repetidos, pero varias columnas venían como texto con unidades, símbolos o abreviaturas (pies y pulgadas, libras, `€1.5M`, `1.1K`, `3 ★`) y la fecha de ingreso como texto. Al convertirlas a números y fechas se pudieron filtrar, agrupar y graficar. Además, 27 jugadores tienen `Value` = 0, 26 tienen `Wage` = 0 (los agentes libres) y 137 tienen `Release Clause` = 0: son ceros de «sin valor asignado», algo a tener en cuenta al interpretar promedios de estas variables.
3. (Integrante A) **La edad marca el nivel y el potencial:** la valoración media sube de 60,27 en los jóvenes a 68,98 en los veteranos, mientras que el margen de crecimiento cae de 12,84 a casi cero (0,01). Los jugadores con mayor potencial de mejora son adolescentes, como W. Faghir, de 16 años, con 25 puntos de crecimiento posible.
4. (Integrante B) **El valor y la velocidad se concentran en pocos jugadores, y la edad y el pie no bastan para explicar la valoración:** K. Mbappé (21 años) lidera el valor de mercado (105,5 millones de euros) y la velocidad (PAC de 96), y solo 5 jugadores menores de 24 años superan los 20 millones. Los mayores márgenes de crecimiento los tienen adolescentes de 18 años o menos, como W. Faghir (de 58 a 83). El gráfico de edad contra valoración muestra jugadores de nivel alto en distintas edades, y la valoración según el pie dominante es muy parecida (mediana de 66 en zurdos y 65 en diestros).
5. (Integrante A) **Composición y habilidades de la muestra:** la mayoría de los jugadores tiene entre 20 y 30 años, y Inglaterra (163), Alemania (141), Francia (111) y España (108) son los países más representados. Entre las habilidades, pase y regate son las que más se relacionan (correlación de 0,83), y tiro y defensa muestran una relación negativa (-0,43).

## Averiguar Ilook