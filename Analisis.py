# %% [markdown]
# # Proyecto_Programacion_2
# Integrantes: Samuel Marroquin Figueroa, Sofia Alba Larrota

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("Datos/fifa21_muestra_2000.csv")

# %% [markdown]
# ## 1. Carga e inspección inicial de los datos  (Integrante A)
# %%
from IPython.display import display
print(df.shape)
df.info()
display(df.describe())
display(df.describe(include="object"))
# %% [markdown]
# **Conclusión:** 
# 
# - El conjunto de datos tiene 2000 filas y 77 columnas.
# - Predominan las variables numéricas, 55 de tipo int64, frente a 22 de texto (str).
# - Casi no hay datos faltantes en la inspección inicial: la única columna con nulos es
# Loan Date End, con solo 110 valores no nulos de 2000, algo esperable porque
# solo aplica a jugadores cedidos a préstamo.
# - La edad va de 16 a 53 años, con media cercana a 25.

# %% [markdown]
# ## 2. Manejo de datos faltantes  (Integrante B)
# %%
# Revisar los datos faltantes por columna

print(df.isnull().sum()[df.isnull().sum() > 0])

# Calcular el porcentaje de datos faltantes

porcentaje = (df["Loan Date End"].isnull().sum() / len(df)) * 100

print("Porcentaje de datos faltantes:", porcentaje, "%")

# Mapa de calor antes de eliminar la variable

plt.figure(figsize=(12, 5))
sns.heatmap(df.isnull(), cbar=False, yticklabels=False, cmap="Reds")
plt.title("Mapa de calor antes de eliminar datos faltantes")
plt.xlabel("Variables")
plt.ylabel("Registros")
plt.show()

# Eliminar la columna Loan Date End

df = df.drop(columns=["Loan Date End"])

# Comprobar los resultados

print("Dimensiones después de la limpieza:", df.shape)
print("Total de datos faltantes:", df.isnull().sum().sum())

# Mapa de calor después de la limpieza

plt.figure(figsize=(12, 5))
sns.heatmap(df.isnull(), cbar=False, yticklabels=False, cmap="Reds")
plt.title("Mapa de calor después de la limpieza")
plt.xlabel("Variables")
plt.ylabel("Registros")
plt.show()

# %% [markdown]
# **Conclusión:**
#
# - La variable "Loan Date End" presentaba 1.890 valores faltantes,
# equivalentes al 94,5 % de sus registros. Debido a la alta
# proporción de información ausente, se decidió eliminar esta
# columna y conservar los 2.000 registros de jugadores.

# %% [markdown]
# ## 3. Identificación de outliers  (Integrante A)
# %%
# Grupo 1: edad y valoraciones generales
plt.figure(figsize=(8, 5))
sns.boxplot(data=df[["Age", "↓OVA", "POT", "BOV"]])
plt.title("Boxplot de edad y valoraciones generales")
plt.show()

# Grupo 2: atributos técnicos principales
plt.figure(figsize=(12, 5))
sns.boxplot(data=df[["Crossing", "Finishing", "Heading Accuracy", "GK Positioning", "GK Reflexes"]])
plt.title("Boxplot de atributos técnicos")
plt.xticks(rotation=45)
plt.show()

# Grupo 3: atributos de rendimiento
plt.figure(figsize=(10, 5))
sns.boxplot(data=df[["PAC", "SHO", "PAS", "DRI", "DEF", "PHY"]])
plt.title("Boxplot de atributos de rendimiento")
plt.show()

# Grupo 4: puntaje total
plt.figure(figsize=(6, 5))
sns.boxplot(data=df[["Total Stats"]])
plt.title("Boxplot de Total Stats")
plt.show()


# %% [markdown]
# **Conclusión:**
#
# - **Edad:** la mayoría de los jugadores tiene entre 22 y 29 años. Hay dos outliers superiores, uno cercano a 42 y otro a 53 años, que corresponden a jugadores veteranos poco frecuentes en la muestra.
# - **Valoraciones generales (OVA, POT y BOV):** presentan outliers en ambos extremos. Por arriba aparecen los jugadores de élite, con valoraciones de más de 85, y por abajo unos pocos con valores cercanos a 47-50. Son valores extremos pero legítimos, no errores.
# - **Atributos de portería (GK Positioning y GK Reflexes):** muestran una gran cantidad de outliers superiores, con valores entre 45 y 90, mientras que la caja está por debajo de 20. Al verificarlo, de los 225 jugadores con GK Positioning mayor a 40, 224 tienen la posición GK. Es decir, no son datos erróneos, sino porteros, una minoría con valores muy altos en estas variables frente a los jugadores de campo.
# - **Heading Accuracy:** tiene outliers inferiores, por debajo de 15 aproximadamente, de jugadores con muy poca capacidad de remate de cabeza.
# - **Crossing, Finishing, SHO y DEF:** no presentan outliers, con cajas amplias y distribuciones bastante dispersas.
# - **PAC, PAS, DRI y PHY:** tienen outliers inferiores (valores cercanos a 25-40) y algunos pocos superiores (por encima de 90 en PAC y PHY).
# - **Total Stats:** presenta muchos outliers inferiores, cerca de 800-960, y dos superiores alrededor de 2300, que corresponden a los jugadores más completos.
# - En general, los outliers reflejan la naturaleza del juego (porteros, estrellas, veteranos) y no errores de captura, por lo que se conservan para el análisis.

# %% [markdown]
# ## 4. Valores inconsistentes y duplicados  (Integrante B)

# %%
# 1. Limpiar espacios y saltos de línea en las columnas de texto
columnas_texto = df.select_dtypes(include=["object", "str"]).columns

for columna in columnas_texto:
    df[columna] = df[columna].str.split().str.join(" ")


# 2. Convertir Hits a números, teniendo en cuenta los valores en miles
def convertir_hits(valor):
    if valor.endswith("K"):
        return float(valor.replace("K", "")) * 1000
    else:
        return float(valor)

df["Hits"] = df["Hits"].apply(convertir_hits)


# 3. Convertir Height de pies y pulgadas a centímetros
def convertir_altura(altura):
    partes = altura.replace('"', '').split("'")
    pies = int(partes[0])
    pulgadas = int(partes[1])
    return round(pies * 30.48 + pulgadas * 2.54)

df["Height"] = df["Height"].apply(convertir_altura)


# 4. Convertir Weight de libras a kilogramos
def convertir_peso(peso):
    libras = int(peso.replace("lbs", ""))
    return round(libras * 0.453592)

df["Weight"] = df["Weight"].apply(convertir_peso)


# 5. Convertir Value, Wage y Release Clause a números
def convertir_euros(valor):
    valor = valor.replace("€", "")

    if valor.endswith("M"):
        return float(valor.replace("M", "")) * 1000000
    elif valor.endswith("K"):
        return float(valor.replace("K", "")) * 1000
    else:
        return float(valor)

df["Value"] = df["Value"].apply(convertir_euros)
df["Wage"] = df["Wage"].apply(convertir_euros)
df["Release Clause"] = df["Release Clause"].apply(convertir_euros)


# 6. Convertir las calificaciones con estrellas a números
for columna in ["W/F", "SM", "IR"]:
    df[columna] = df[columna].str.replace("★", "", regex=False).str.strip().astype(int)


# 7. Convertir Joined a formato de fecha
df["Joined"] = pd.to_datetime(df["Joined"])


# 8. Revisar y eliminar duplicados, si existen
duplicados = df.duplicated().sum()

print("Cantidad de registros duplicados:", duplicados)

if duplicados > 0:
    df = df.drop_duplicates()


# 9. Mostrar los resultados finales
print("\nTipos de datos después de las correcciones:")
print(df.dtypes)

print("\nDimensiones finales:")
print(df.shape)


# %% [markdown]
# **Conclusiones:**
#
# - Se identificaron y corrigieron inconsistencias relacionadas con espacios y saltos de línea en las columnas de texto.
# - La columna `Hits` se convirtió a formato numérico, teniendo en cuenta los valores expresados en miles mediante la abreviatura K.
# - Las columnas `Height` y `Weight` se transformaron a centímetros y kilogramos, respectivamente.
# - Las columnas `Value`, `Wage` y `Release Clause` se convirtieron a valores numéricos en euros, facilitando su utilización en operaciones y análisis.
# - Las calificaciones `W/F`, `SM` e `IR` se transformaron a valores numéricos.
# - La columna `Joined` se convirtió a formato de fecha.
# - Se conservaron como texto las variables categóricas, como nacionalidad, posiciones y nombres, porque representan características de los jugadores y no cantidades.
# - Finalmente, se comprobó que no existen registros duplicados.

# %% [markdown]
# ## 5. Creación de variables  (Integrante A)
# %%
# Variable 1: índice de masa corporal (peso en kg / altura en metros al cuadrado)
df["IMC"] = (df["Weight"] / (df["Height"] / 100) ** 2).round(2)

# Variable 2: margen de crecimiento (potencial menos valoración actual)
df["Margen_crecimiento"] = df["POT"] - df["↓OVA"]

# Variable 3: categoría de edad
df["Categoria_edad"] = pd.cut(
    df["Age"],
    bins=[0, 21, 29, 100],
    labels=["Joven", "Adulto", "Veterano"]
)

# Revisar las variables nuevas
display(df[["IMC", "Margen_crecimiento", "Categoria_edad"]].describe(include="all"))

# %% [markdown]
# **Conclusión:**
#
# - Se crearon tres variables nuevas a partir de las existentes.
# - **IMC:** relaciona el peso (kg) con la altura (m) de cada jugador. Su media es de 22.86, con valores entre 18.39 y 29.76, lo que indica una complexión física normal en la mayoría de los jugadores.
# - **Margen_crecimiento:** es la diferencia entre el potencial (POT) y la valoración actual (OVA). Su media es de 5.25 puntos y llega hasta 25, lo que identifica a los jugadores con mayor margen de mejora. Coincide con la columna Growth del conjunto original.
# - **Categoria_edad:** agrupa la edad en tres rangos, Joven (hasta 21 años), Adulto (22 a 29) y Veterano (30 o más). La categoría más frecuente es Adulto, con 1093 de los 2000 jugadores.
# %% [markdown]
# ## 6. Filtrado y condiciones en pandas  (Integrante B)

# %%
# RESULTADO 1: Jugadores con mayor valor de mercado

jugadores_valiosos = df[["Name", "Age", "Nationality", "Value", "Wage"]]

jugadores_valiosos = jugadores_valiosos.sort_values(by="Value", ascending=False)

jugadores_valiosos.head(10)


# %% [markdown]
# **Conclusión 1:** Al analizar los diez jugadores con mayor valor de mercado,
# se encontró que K. Mbappé ocupa el primer lugar con €105,5 millones
# seguido de K. De Bruyne con €87 millones. Alemania es la nacionalidad
# con mayor representación en este grupo, con tres jugadores.
# Esto permite observar las diferencias en el valor de mercado
# de los futbolistas de la muestra.


# %%
# RESULTADO 2: Jugadores jóvenes con alto valor de mercado

jugadores_jovenes = df[(df["Age"] < 24) & (df["Value"] > 20000000)]

jugadores_jovenes = jugadores_jovenes[["Name", "Age", "Nationality", "Value", "↓OVA"]]

jugadores_jovenes = jugadores_jovenes.sort_values(by="Value", ascending=False)

jugadores_jovenes.head(10)


# %% [markdown]
# **Conclusión 2:** Se identificaron cinco jugadores menores de 24 años
# con un valor de mercado superior a 20 millones de euros. K. Mbappé
# destaca nuevamente con un valor de €105,5 millones y una valoración general de 90.
# Esto muestra que dentro de la muestra existen jugadores jóvenes
# con un alto valor de mercado y un buen rendimiento general.


# %%
# RESULTADO 3: Nacionalidades con mayor cantidad de jugadores

nacionalidades = df["Nationality"].value_counts().head(10)

nacionalidades


# %% [markdown]
# **Conclusión 3:** Inglaterra es la nacionalidad con mayor representación
# en la muestra, con 163 jugadores, seguida de Alemania con 141
# y Francia con 111. Esto permite identificar cuáles son los países
# que tienen mayor presencia de futbolistas en la base de datos.


# %%
# RESULTADO 4: Jugadores con mayor potencial de crecimiento

jugadores_crecimiento = df[["Name", "Age", "Nationality", "↓OVA", "POT", "Growth"]]

jugadores_crecimiento = jugadores_crecimiento.sort_values(by="Growth", ascending=False)

jugadores_crecimiento.head(10)


# %% [markdown]
# **Conclusión 4:** Se identificaron los diez jugadores con mayor potencial
# de crecimiento en la muestra. W. Faghir, de 16 años, ocupa el primer
# lugar con un crecimiento potencial de 25 puntos, pasando de una
# valoración actual de 58 a un potencial de 83. Además, todos los
# jugadores encontrados tienen 18 años o menos, lo que evidencia
# la presencia de futbolistas jóvenes con importantes posibilidades
# de desarrollo.


# %%
# RESULTADO 5: Jugadores con mayor velocidad

jugadores_rapidos = df[df["PAC"] >= 90]

jugadores_rapidos = jugadores_rapidos[["Name", "Age", "Nationality", "Positions", "PAC", "DRI", "↓OVA"]]

jugadores_rapidos = jugadores_rapidos.sort_values(by="PAC", ascending=False)

print("Cantidad de jugadores con velocidad de 90 o más:",len(jugadores_rapidos))

jugadores_rapidos.head(10)


# %% [markdown]
# **Conclusión 5:** Se encontraron 28 jugadores con una velocidad
# de 90 puntos o más. K. Mbappé ocupa el primer lugar con 96 puntos
# de velocidad, seguido de varios jugadores con puntuaciones de 93.
# Este resultado permite identificar a los futbolistas más rápidos
# de la muestra y comparar su velocidad con su capacidad de regate
# y su valoración general.

# %% [markdown]
# ## 7. Agrupación con groupby  (Integrante A)
# %%
# Resultado 1: valoración media (OVA) por categoría de edad
r1 = df.groupby("Categoria_edad", observed=True)["↓OVA"].mean().round(2)
display(r1)

# %% [markdown]
# **Conclusión 1:** la valoración media sube con la edad: 60.27 en los jóvenes, 66.95 en los adultos y 68.98 en los veteranos. Los jugadores con más experiencia tienen, en promedio, mejor nivel actual.

# %%
# Resultado 2: valor de mercado medio por categoría de edad
r2 = df.groupby("Categoria_edad", observed=True)["Value"].mean().round(0)
display(r2)

# %% [markdown]
# **Conclusión 2:** los adultos son los más valiosos, con un promedio de unos 2,53 millones de euros, frente a 1,92 millones de los veteranos y 1,06 millones de los jóvenes. El mercado paga más por quienes combinan buen nivel y varios años por delante.

# %%
# Resultado 3: los 10 países con más jugadores
r3 = df.groupby("Nationality")["ID"].count().sort_values(ascending=False).head(10)
display(r3)

# %% [markdown]
# **Conclusión 3:** Inglaterra lidera la muestra con 163 jugadores, seguida de Alemania con 141, Francia con 111 y España con 108. Cuatro países europeos concentran los primeros puestos, aunque Brasil (95) y Argentina (81) destacan como los mayores representantes de Sudamérica.

# %%
# Resultado 4: margen de crecimiento medio por categoría de edad
r4 = df.groupby("Categoria_edad", observed=True)["Margen_crecimiento"].mean().round(2)
display(r4)

# %% [markdown]
# **Conclusión 4:** el margen de crecimiento cae con la edad: 12.84 puntos en los jóvenes, 3.81 en los adultos y prácticamente cero (0.01) en los veteranos. Es lo esperable, porque los veteranos ya alcanzaron su potencial.

# %%
# Resultado 5: salario medio según el pie dominante
r5 = df.groupby("foot")["Wage"].mean().round(0)
display(r5)

# %% [markdown]
# **Conclusión 5:** los jugadores zurdos ganan en promedio algo más (8494) que los diestros (8321), pero la diferencia es pequeña, de unos 170, así que el pie dominante no parece influir de forma importante en el salario.

# %% [markdown]
# ## 8. Visualizaciones  (Integrante B)

# %% [markdown]
# ## 9. Conclusiones finales  (Integrante A)