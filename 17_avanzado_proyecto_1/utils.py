from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun

# Función para crear el guión de Youtube.
def generar_guion(indicacion, tiempo_video, creatividad, api_key):
    # Plantilla para generar el titulo.
    indicacion_titulo = PromptTemplate(
        input_variables= ['tema'],
        template= 'Por favor escribe un título atractivo para un video de Youtube sobre {tema}.'
    )

    # Plantilla para generar el guión usando la busqueda de DuckDuckGo.
    indicacion_guion = PromptTemplate(
        input_variables= ['titulo', 'duckduckgo_search', 'duracion'],
        template= 'Crea un guion para un video de Youtube en base a este titulo para mi. TITULO: {titulo} de {duracion} minutos usando la siguiente busqueda de DuckDuckGo: {duckduckgo_search}.'
    )

    # Instanciar el modelo de lenguaje de OpenAI.
    llm = ChatOpenAI(
        openai_api_key= api_key,
        model= 'gpt-3.5-turbo',
        temperature= creatividad
    )
    # Instanciar el motor de busqueda de DuckDuckGo.
    busqueda = DuckDuckGoSearchRun()

    # Crear la cadena para el titlo y el guión.
    titulo_chain = indicacion_titulo | llm
    guion_chain = indicacion_guion | llm

    # Ejecutar la cadena de titulo.
    response_titulo = titulo_chain.invoke({'tema': indicacion})

    # Ejecutamos la cadena que creamos para el guión usando la busqueda de DuckDuckGo.
    response_busqueda = busqueda.invoke(indicacion)
    response_guion = guion_chain.invoke({'titulo': response_titulo, 'duckduckgo_search': response_busqueda, 'duracion': tiempo_video})

    # Retornar el titulo, la busqueda y el guión.
    return response_titulo, response_busqueda, response_guion

    