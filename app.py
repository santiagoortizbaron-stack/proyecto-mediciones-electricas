import streamlit as st
import math
import pandas as pd
from datetime import datetime
from io import BytesIO


# ==========================
# CONFIGURACIÓN
# ==========================

st.set_page_config(
    page_title="Mediciones Eléctricas",
    page_icon="⚡",
    layout="wide"
)


# ==========================
# TÍTULO
# ==========================

st.title("⚡ Sistema de Mediciones Eléctricas")
st.subheader("Aplicación de números complejos en circuitos AC")


# ==========================
# MEMORIA DE DATOS
# ==========================

if "datos" not in st.session_state:
    st.session_state.datos = []



# ==========================
# TIPOS DE MEDICIÓN
# ==========================

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


# ==========================
# ENTRADAS
# ==========================

col1, col2 = st.columns(2)


with col1:

    tipo = st.selectbox(
        "Seleccione la medición",
        tipos
    )


    valor = st.number_input(
        "Ingrese el valor medido",
        value=0.0
    )


with col2:

    angulo_texto = st.text_input(
        "Ángulo (opcional)",
        placeholder="Ejemplo: 30"
    )


# ==========================
# CALCULO COMPLEJO
# ==========================

if st.button("➕ Agregar medición"):


    if angulo_texto == "":
        angulo = 0

    else:
        angulo = float(angulo_texto)



    rad = math.radians(angulo)


    real = valor * math.cos(rad)

    imaginaria = valor * math.sin(rad)



    if imaginaria >= 0:

        complejo = (
            f"{real:.2f} + j{imaginaria:.2f}"
        )

    else:

        complejo = (
            f"{real:.2f} - j{abs(imaginaria):.2f}"
        )



    registro = {

        "Fecha":
        datetime.now().strftime("%d/%m/%Y"),


        "Hora":
        datetime.now().strftime("%H:%M:%S"),


        "Tipo":
        tipo,


        "Valor":
        valor,


        "Ángulo (°)":
        angulo,


        "Parte Real":
        round(real,2),


        "Parte Imaginaria":
        round(imaginaria,2),


        "Número Complejo":
        complejo

    }


    st.session_state.datos.append(registro)



    st.success(
        "Medición agregada correctamente"
    )



# ==========================
# MOSTRAR TABLA
# ==========================

st.divider()

st.subheader("📋 Registro de mediciones")


if len(st.session_state.datos) > 0:


    df = pd.DataFrame(
        st.session_state.datos
    )


    st.dataframe(
        df,
        use_container_width=True
    )


else:

    st.info(
        "No existen mediciones registradas"
    )



# ==========================
# BOTONES
# ==========================

col3, col4 = st.columns(2)



with col3:

    if st.button("🗑️ Limpiar tabla"):

        st.session_state.datos = []

        st.success(
            "Tabla limpiada"
        )

        st.rerun()



with col4:


    if len(st.session_state.datos) > 0:


        df = pd.DataFrame(
            st.session_state.datos
        )


        archivo = BytesIO()


        with pd.ExcelWriter(
            archivo,
            engine="openpyxl"
        ) as writer:

            df.to_excel(
                writer,
                index=False,
                sheet_name="Mediciones"
            )



        st.download_button(

            label="📥 Descargar Excel",

            data=archivo.getvalue(),

            file_name="Mediciones_Electricas.xlsx",

            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        )