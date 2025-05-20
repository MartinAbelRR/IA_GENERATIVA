import base64
from io import StringIO
from langchain.chat_models import init_chat_model
from langchain.schema import HumanMessage, SystemMessage
import streamlit as st
import time

st.title('Vamos a revisar el código de tu código Python')
st.header('Porfavor sube tu archivo .py aquí:')

def get_optimizacion_codigo(texto_script):
    llm = init_chat_model('gpt-4o-mini', model_provider= 'openai', configurable_fields= {'temperature': 0.5})

    # Crear una instancia de SystemMessage con el mensaje del sistema, que tiene información acerca del rol del asistente.
    system_message = SystemMessage(
        content= "Eres un asistente que ayuda a los desarrolladores a optimizar su código Python. "
                 "Tu tarea es revisar el código y sugerir mejoras o correcciones."
    )

    # Crear una instancia de HumanMessage con el mensaje del usuario, que contiene el código a revisar.
    human_message = HumanMessage(
        content= texto_script
    )

    # Llamar al modelo de lenguaje con el mensaje del sistema y el mensaje del usuario.
    response = llm.invoke([system_message, human_message])

    # Obtener el contenido de la respuesta del modelo.
    return response.content

# Crear un enlace de descarga para el archivo.
def descargar_archivo(contenido):
    # Generar un timestamp para el nombre del archivo.
    timestr = time.strftime("%Y%m%d-%H%M%S")

    # Codificador Base64 para el contenido del archivo, base64 porque es un formato de codificación que representa datos binarios en texto ASCII.
    b64 = base64.b64encode(contenido.encode()).decode()

    # Crear un nuevo archivo con el contenido codificado.
    nuevo_nombre_archivo = f"codigo_optimizacion_{timestr}.txt"

    st.markdown("Descargar el archivo optimizado:")
    
    # Creamo un enlace de descarga para el archivo optimizado.
    href = f'<a href="data:file/txt;base64,{b64}" download= "{nuevo_nombre_archivo}">Descargar archivo optimizado</a>'

    # Mostramos el hmltml en la aplicación Streamlit.
    st.markdown(href, unsafe_allow_html= True)

# Capturar el .py
data = st.file_uploader("Sube tu archivo .py", type= ["py", 'ipynb'])

if data is not None:
    # Crear un StringIO y inicializalo con el contenido de data decodificado.
    string_io = StringIO(data.getvalue().decode("utf-8")) # StringIO es un objeto que actua como un archivo en memoria, entonces lo que hacemos es que le pasamos el contenido del archivo subido y lo guardamos en string_io.
    st.write(string_io) # Mostramos el contenido del archivo subido.

    # Leer el contenido de string_io y lo guardamos en la variable leer_data.
    leer_data = string_io.read() # Leemos el contenido del archivo y lo guardamos en leer_data.

    # st.write(leer_data) # Mostramos el contenido del archivo subido.

    # Llamar a la función get_optimizacion_codigo con el contenido del archivo y guardar la respuesta.
    respuesta = get_optimizacion_codigo(leer_data) # Llamamos a la función get_optimizacion_codigo con el contenido del archivo y guardamos la respuesta.

    st.markdown('---') # Agregamos una línea de separación.
    st.subheader('Respuesta del modelo:') # Agregamos un subtitulo.
    st.write(respuesta) # Mostramos la respuesta del modelo.

    # Llamar a la función descargar_archivo con la respuesta del modelo.
    descargar_archivo(respuesta) # Llamamos a la función descargar_archivo con la respuesta del modelo.
    st.markdown('---') # Agregamos una línea de separación.