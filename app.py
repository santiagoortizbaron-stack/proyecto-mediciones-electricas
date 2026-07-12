import streamlit as st
import math
import pandas as pd
from datetime import datetime
from io import BytesIO


# Configuración de página
st.set_page_config(
    page_title="Mediciones Eléctricas",
    page_icon="⚡",
    layout="wide"
)


# Título
st.title("⚡ Sistema de Mediciones Eléctricas")
st.subheader("Aplicación de números complejos en circuitos AC")


# Guardar datos mientras la página está abierta
if "datos" not in st.session_state:
    st.session_state.datos = []


# Tipos de medición
tipos = [
    "Voltaje fase-neutro (V)",
    "Voltaje fase-fase (V)",
    "Corriente fase A (A)",
    "Corriente fase B (A)",
    "Corriente fase C (A)",
    "Impedancia (Ω)",
    "Resistencia (Ω)",
    "Reactancia inductiva (Ω)",
    "Reactancia capacitiva (Ω)",
    "Potencia activa (W)",
    "Potencia reactiva (VAR)",
    "Potencia aparente (VA)",
    "Frecuencia (Hz)",
    "Energía (kWh)",
    "Factor de potencia"
]


# Entrada de datos

col1, col2 = st.columns(2)


with col1:

    tipo = st.selectbox(
        "Seleccione la medición",
        tipos
    )

    valor = st.number_input(
        "Valor medido",
        min_value=0.0,
        format="%.2f"
    )


with col2:

    angulo = st.text_input(
        "Ángulo (opcional)",
        placeholder="Ejemplo: 30"
    )


# Agregar medición

if st.button("➕ Agregar medición"):

    if angulo.strip() == "":
        ang = 0
    else:
        ang = float(angulo)


    rad = math.radians(ang)


    real = valor * math.cos(rad)

    imaginaria = valor * math.sin(rad)


    complejo = (
        f"{real:.2f} + j{imaginaria:.2f}"
        if imaginaria >= 0
        else
        f"{real:.2f} - j{abs(imaginaria):.2f}"
    )


    nueva_medicion = {

        "Fecha":
        datetime.now().strftime("%d/%m/%Y"),

        "Hora":
        datetime.now().strftime("%H:%M:%S"),

        "Tipo":
        tipo,

        "Valor":
        valor,

        "Angulo (°)":
        ang,

        "Parte Real":
        round(real,2),

        "Parte Imaginaria":
        round(imaginaria,2),

        "Numero Complejo":
        complejo
    }


    st.session_state.datos.append(nueva_medicion)

    st.success("Medición agregada")


# Tabla

st.divider()

st.subheader("📋 Mediciones registradas")


if len(st.session_state.datos) > 0:

    df = pd.DataFrame(st.session_state.datos)

    st.dataframe(
        df,
        use_container_width=True
    )


else:

    st.info("No hay mediciones")


# Limpiar

if st.button("🗑️ Limpiar tabla"):

    st.session_state.datos = []

    st.rerun()



# Descargar Excel

st.divider()

if len(st.session_state.datos) > 0:

    df = pd.DataFrame(st.session_state.datos)

    archivo = BytesIO()

    df.to_excel(
        archivo,
        index=False
    )

    archivo.seek(0)


    st.download_button(

        label="📥 Descargar Excel",

        data=archivo,

        file_name="Mediciones_Electricas.xlsx",

        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )
