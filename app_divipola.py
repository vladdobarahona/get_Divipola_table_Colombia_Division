import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# Fondo personalizado y fuente
st.markdown("""
    <style>
    .stApp {
        background-image: "logo_superior_finagro.png";
        background-size: cover;
        background-repeat: repeat;
        background-attachment: fixed;
        font-family: 'Handel Gothic', Frutiger light - Roman;
    }
    </style>
    """, unsafe_allow_html=True)

# Logo a la izquierda y título a la derecha
col1, col2 = st.columns([1, 5])
with col1:
    st.image('https://www.finagro.com.co/sites/default/files/logo-front-finagro.png', width=200)
with col2:
    st.title("Generador de Archivo DIVIPOLA desde el DANE")

# Botón para ejecutar la descarga y procesamiento de datos
if st.button("Descargar y procesar datos"):
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

    # Realiza la unión de los dataframes en base al código de departamento
    divipola = df_municipios.merge(df_departamentos, on='CODIGO_DEPARTAMENTO')

    # Selecciona columnas relevantes
    divipola = divipola[['CODIGO_DEPARTAMENTO', 'NOMBRE_DEPARTAMENTO', 'CODIGO_MUNICIPIO', 'NOMBRE_MUNICIPIO', 'CODIGO_DPTO_MPIO', 'CODIGO_TIPO_MUNICIPIO']]

    # Muestra el DataFrame en la app
    st.dataframe(divipola)

    # Genera el archivo Excel en memoria
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        divipola.to_excel(writer, index=False, sheet_name='DIVIPOLA')
    output.seek(0)

    # Botón para descargar el archivo Excel
    st.download_button(
        label="📥 Descargar archivo Excel",
        data=output,
        file_name="divipola_actualizado.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
