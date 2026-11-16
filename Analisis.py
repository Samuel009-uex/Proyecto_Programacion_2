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

# %% [markdown]
# ## 7. Agrupación con groupby  (Integrante A)

# %% [markdown]
# ## 8. Visualizaciones  (Integrante B)

# %% [markdown]
# ## 9. Conclusiones finales  (Integrante A)