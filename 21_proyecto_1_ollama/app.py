import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

def get_respuesa_llm(entrada_form, correo_de_origen, correo_de_destino, estilo):
    llm = ChatOllama(model= 'deepseek-r1:7b', temperature= 0.4, top_p= 0.85, top_k= 20)

    plantilla = """
    Eres un asistente de IA que ayuda a redactar correos electrónicos.
    Escribe un correo electrónico en español basado en la siguiente información:
    Correo de origen: {correo_de_origen}
    Correo de destino: {correo_de_destino}
    Estilo: {estilo}
    Tema: {entrada_form}

    Texto del correo electrónico:
    """

    indicacion = ChatPromptTemplate.from_template(
        template= plantilla
    )

    indicacion_template = indicacion.invoke({
        'entrada_form': entrada_form,
        'correo_de_origen': correo_de_origen,
        'correo_de_destino': correo_de_destino,
        'estilo': estilo
    })

    # Generar el correo electrónico.
    respuesta = llm.invoke(indicacion_template)

    return respuesta.content.split('</think>')[1]



st.set_page_config(
    page_title= 'Generar emails',
    page_icon= '✉️',
    layout= 'centered',
    initial_sidebar_state= 'collapsed'
)
st.header('Generar emails con IA')

entrada_form = st.text_area('Escriba el tema del email', height= 275)

# Crear columnas para la UI - para recibir el input del usuario.
col1, col2, col3 = st.columns([10, 10, 5])
with col1:
    correo_de_origen = st.text_input('Correo de origen')

with col2:
    correo_de_destino = st.text_input('Correo de destino')

with col3:
    estilo = st.selectbox('Estilo', ['Formal', 'Apropiado', 'No satisfactorio', 'Neutral'], index= 0)

enviar = st.button('Generar email')

# Cuando el usuario hace clic en el botón, se genera el correo electrónico.
if enviar:
    if entrada_form and correo_de_origen and correo_de_destino:
        with st.spinner('Generando el correo electrónico...'):
            respuesta = get_respuesa_llm(entrada_form, correo_de_origen, correo_de_destino, estilo)
            st.write(respuesta)
    else:
        st.warning('Por favor, complete todos los campos.')