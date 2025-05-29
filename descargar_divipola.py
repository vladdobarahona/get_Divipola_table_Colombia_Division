import requests
import pandas as pd

# URLs de los servicios web
url_municipios = "https://geoportal.dane.gov.co/laboratorio/serviciosjson/gdivipola/servicios/municipios.php"
url_departamentos = "https://geoportal.dane.gov.co/laboratorio/serviciosjson/gdivipola/servicios/departamentos.php"

# Realiza la solicitud HTTP para descargar los datos
response_municipios = requests.get(url_municipios)
response_departamentos = requests.get(url_departamentos)

# Convierte las respuestas JSON a diccionarios
data_municipios = response_municipios.json()
data_departamentos = response_departamentos.json()

# Extrae los datos
municipios = data_municipios["resultado"]
departamentos = data_departamentos["resultado"]

# Crea dataframes
df_municipios = pd.DataFrame(municipios)
df_departamentos = pd.DataFrame(departamentos)

# Une los dataframes
divipola = df_municipios.merge(df_departamentos, on='CODIGO_DEPARTAMENTO')

# Selecciona columnas relevantes
divipola = divipola[['CODIGO_DEPARTAMENTO', 'NOMBRE_DEPARTAMENTO', 'CODIGO_MUNICIPIO', 'NOMBRE_MUNICIPIO', 'CODIGO_DPTO_MPIO', 'CODIGO_TIPO_MUNICIPIO']]

# Exporta a Excel
divipola.to_excel("divipola_actualizado.xlsx", index=False)

print("✅ Archivo 'divipola_actualizado.xlsx' generado correctamente.")
