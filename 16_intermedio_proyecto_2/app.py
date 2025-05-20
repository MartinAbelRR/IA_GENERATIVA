import streamlit as st
from dotenv import load_dotenv
from utils import consulta_agente


st.title('Vamos hacer analisis de datos en tu CSV')
st.header('Porfavor sube tu archivo CSV aqui:')

# Capturar el archivo CSV.
data = st.file_uploader("Sube tu archivo CSV", type= ["csv"])

consulta = st.text_input("Escribe tu consulta")
button = st.button("Generar respuesta")

if button:
    # Obtener respuesta.
    respuesta = consulta_agente(data, consulta)
    st.write(respuesta)