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