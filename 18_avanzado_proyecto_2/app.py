import streamlit as st
from utils import get_data_sitio_web, dividir_data, crear_incrustador, subir_data, recuperar_data, get_docs_similares
from constants import PINECONE_INDICE_NOMBRE, WEBSITE_URL

# Creamos la variable de estado para la sesión.
if 'HuggingFace_API_Key' not in st.session_state:
    st.session_state['HuggingFace_API_Key'] = ''
if 'Pinecone_API_Key' not in st.session_state:
    st.session_state['Pinecone_API_Key'] = ''

# Titulo de la aplicación.
st.title('Asistente de IA para Sitio Web')

# Barra lateral para la configuración de la API.
st.sidebar.title('Configuración de la API')
st.session_state['HuggingFace_API_Key'] = st.sidebar.text_input(
    '¿Cuál es tu HuggingFace API Key?', 
    type='password'
    )
st.session_state['Pinecone_API_Key'] = st.sidebar.text_input(
    '¿Cuál es tu Pinecone API Key?', 
    type='password'
    )

cargar_button = st.sidebar.button('Cargar data para Pinecone', key= 'cargar_button')

# Si el botón de cargar es presionado, se ejecuta la función...
if cargar_button:
    # Continuamos solo si API Key de HuggingFace y Pinecone son válidos.
    if st.session_state['HuggingFace_API_Key'] != '' and st.session_state['Pinecone_API_Key'] != '':
        # data buscada desde el sitio web.
        docs_sitio_web = get_data_sitio_web(WEBSITE_URL)
        st.write('Extracción de datos realizada... ')

        # Divir la data en partes más pequeñas.
        docs_divididos = dividir_data(docs_sitio_web)
        st.write('División de datos realizada... ')

        # Crear una instancia de incrustación de Pinecone.
        incrustador = crear_incrustador()
        st.write('Creación de incrustación de Pinecone realizada... ')

        # Subir la data a Pinecone.
        subir_data(st.session_state['Pinecone_API_Key'], PINECONE_INDICE_NOMBRE, incrustador, docs_divididos)
        st.write('Subida de datos a Pinecone realizada... ')

        st.sidebar.success('¡Datos cargados exitosamente!')


    else:
        st.sidebar.error('Por favor, ingresa las API Keys de HuggingFace y Pinecone.')

# Fin de la barra lateral.

# Capturar la pregunta del usuario.
pregunta = st.text_input('¿Cómo puedo ayudarte mi amigo?')
contar_documentos = st.slider('Número de links a buscar', 0, 5, 2)

enviar = st.button('Buscar', key= 'enviar')

if enviar:
    # Procesar solo si la API Key de HuggingFace y Pinecone son válidas.
    if st.session_state['HuggingFace_API_Key'] != '' and st.session_state['Pinecone_API_Key'] != '':
        # Creamos la instancia de incrustador.
        incrustador = crear_incrustador()
        st.write('Creación de incrustación de Pinecone realizada... ')

        # Recuperar la data de Pinecone.
        index = recuperar_data(st.session_state['Pinecone_API_Key'], PINECONE_INDICE_NOMBRE)

        # Realizar la búsqueda en Pinecone.
        docs_similares = get_docs_similares(index, pregunta, k= contar_documentos)
        st.write(docs_similares)

        # Mostrar los resultados.
        st.success('¡Resultados encontrados!')
        for doc in docs_similares:
            st.write(f'**Resultado: {docs_similares.index(doc) + 1}**')
            st.write(f'**Texto:** {doc.page_content}')
            st.write(f'**Link:** {doc.metadata["source"]}')

    else:
        st.error('Por favor, ingresa las API Keys de HuggingFace y Pinecone.')