import streamlit as st
from utils import generar_guion

# Estilos de la aplicación.
st.markdown("""
<style>
            div.stButton > button:first-child {
                background-color: #0099ff;
                color: white;
            }
            div.stButton > button:hover {
                background-color: #007ff00;
                color: white;
            }
</style>
""", unsafe_allow_html= True) # unsafe_allow_html permite usar HTML y CSS en Streamlit.

# Crear una variable de estado para la sesión.
if 'API_Key' not in st.session_state:
    st.session_state['API_Key'] = ''

# Título de la aplicación.
st.title('❤️ Herramienta de escritura de guiones de Youtube')

# Barra lateral para captural la API Key.
st.sidebar.title('😎🗝️')
st.session_state['API_Key'] = st.sidebar.text_input('Introduce tu API Key de OpenAI', type= 'password')
st.sidebar.image('./youtube.jpg', width= 300, use_container_width= True) # use_container_width permite usar el ancho del contenedor.

# Capturar entradas del usuario.
indicacion = st.text_input('Por favor introduce el tema del video', 'Escribe aquí el tema del video')
tiempo_video = st.text_input('¿Cuánto tiempo quieres que dure el video? (en minutos)', 'Escribe aquí el tiempo del video')
creatividad = st.slider('¿Qué tan creativo quieres que sea el guión? ', 0.0, 1.0, 0.2, step= 0.1) # Slider para la creatividad.

# Botón para generar el guión.
enviar = st.button('Generar guión para mí')

# Si el botón es presionado, se ejecuta la función.
if enviar:
    if st.session_state['API_Key']:
        respuesta_titulo, respuesta_busqueda, respuesta_guion = generar_guion(indicacion, tiempo_video, creatividad, st.session_state['API_Key']) # Llamar a la función para generar el guión.

        # Inicio de la generación del guión.
        st.success('Espero te guste el guión que he generado para ti. ¡Disfrútalo!') # Mensaje de éxito.

        # Mostrar el tiempo.
        st.subheader('Titulo:')
        st.write(respuesta_titulo.content)

        # Mostrar el guión.
        st.subheader('Tu guión de tu video de Youtube:')
        st.write(respuesta_guion.content)

        # Mostrar el motor de busqueda.
        st.subheader('Salida - DuckDuckGo Search:')
        with st.expander('Mostrar salida'):
            st.info(respuesta_busqueda)
    else:
        # Mensaje de error si no se ha introducido la API Key.
        st.error('Por favor introduce tu API Key de OpenAI en la barra lateral')