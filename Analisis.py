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
# La variable "Loan Date End" presentaba 1.890 valores faltantes,
# equivalentes al 94,5 % de sus registros. Debido a la alta
# proporción de información ausente, se decidió eliminar esta
# columna y conservar los 2.000 registros de jugadores.

# %% [markdown]
# ## 3. Identificación de outliers  (Integrante A)

# %% [markdown]
# ## 4. Valores inconsistentes y duplicados  (Integrante B)

# %% [markdown]
# ## 5. Creación de variables  (Integrante A)

# %% [markdown]
# ## 6. Filtrado y condiciones en pandas  (Integrante B)

# %% [markdown]
# ## 7. Agrupación con groupby  (Integrante A)

# %% [markdown]
# ## 8. Visualizaciones  (Integrante B)

# %% [markdown]
# ## 9. Conclusiones finales  (Integrante A)