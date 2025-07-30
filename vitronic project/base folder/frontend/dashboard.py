import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Dashboard de Usuarios", layout="wide")
st.title("📊 Registered users dashboard")

# Llamar a la API de FastAPI
API_URL = "http://localhost:8000/data/"
response = requests.get(API_URL)

if response.status_code == 200:
    json_data = response.json()

    # Verifica que contiene las claves necesarias
    if "columns" in json_data and "data" in json_data:
        df = pd.DataFrame(json_data["data"], columns=json_data["columns"])

        # Conversión de campos si existen
        if "fecha" in df.columns:
            df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")

        # Mostrar datos
        st.subheader("📄 Data")
        st.dataframe(df)

    else:
        st.error("❌ Formato inesperado en la respuesta de la API.")

else:
    st.error(f"❌ Error al llamar a la API: {response.status_code}")
