import streamlit as st
from backend.routers.agenteMarketingRouter import get_respuesta_agente_marketing

st.set_page_config(
    page_title= "Herramienta de Marketing",
    page_icon= ":bar_chart:",
    layout= "centered",
    initial_sidebar_state= "collapsed"
)

st.header("Hola, ¿en qué puedo ayudarte hoy?")

# Agregar un campo de área de texto.
formato_input = st.text_area("Introduce texto", height= 275)

# Agregar un campo de selección.
opcion_tipoTarea = st.selectbox("Selecciona el tipo de tarea", ["Escribe una copia de ventas", "Crea un tweet", "Escribe una descripción de producto"], key= 1)

# Agregar un campo de edad.
opcion_edad = st.selectbox(
    "A que grupo de edad va dirigido",
    ["Niños", "Adolescentes", "Adultos", "Adultos mayores"],
    key= 2
)

# Agregar la cantidad de palabras.
opcion_numPalabras = st.slider("Selecciona la cantidad de palabras", 0, 200, 25)

submit = st.button("Generar")

if submit:
    st.write(get_respuesta_agente_marketing(formato_input, opcion_edad, opcion_tipoTarea))