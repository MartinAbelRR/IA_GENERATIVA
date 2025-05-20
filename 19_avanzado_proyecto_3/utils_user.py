from langchain_community.callbacks.manager import get_openai_callback # Sirve para obtener el callback de OpenAI: El callback es una función que se ejecuta después de que se completa una tarea.
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_pinecone import PineconeVectorStore
import joblib
import os 
from pinecone import Pinecone as PineconeClient

# Función para crar una instancia de incrustador.
def crear_incrustador():
    incrustador = HuggingFaceEmbeddings(model_name= 'all-MiniLM-L6-v2')
    return incrustador # Retornar el incrustador creado.

# Función para recuperar la data de Pinecone.
def recuperar_data(pinecone_api_key, pinecone_nombre_indice):
    pc = PineconeClient(api_key= pinecone_api_key)
    indice = pc.Index(pinecone_nombre_indice) # Crear un índice de Pinecone: Un indice es una colección de vectores.

    vector_store = PineconeVectorStore(
        index= indice,
        embedding= crear_incrustador(),
        pinecone_api_key= pinecone_api_key,
        namespace= 'avanzado_proyecto_3'
    )

    return vector_store.as_retriever()

# Función para realizar la búsqueda en Pinecone.
def get_docs_similares(indice, consulta, k= 5):
    docs_similares = indice.invoke(consulta, k= k) # Obtener los documentos más relevantes.
    return docs_similares # Retornar los documentos más relevantes.

# Función para obtener la respuesta.
def get_respuesta(docs, consulta):
    indicacion = ChatPromptTemplate.from_template('A partir de los siguientes documentos, responde la pregunta: {context} \n Pregunta: {consulta}')
    cadena = create_stuff_documents_chain(llm= ChatOpenAI(temperature= 0.1, model= 'gpt-4o-mini'), prompt= indicacion)

    with get_openai_callback() as callback:
        respuesta = cadena.invoke({'context': docs, 'consulta': consulta}) # Obtener la respuesta a partir de los documentos y la consulta.
        print(f"Tokens usados: {callback.total_tokens}")
    return respuesta # Retornar la respuesta.


# Predecir el modelo.
def predecir(consulta):
    modelo_ajustado = joblib.load(os.path.relpath('/home/martin/Escritorio/cursos/langchain__gen_ai/19_avanzado_proyecto_3/model/modelo_svm.pkl', os.getcwd()))
    resultado = modelo_ajustado.predict([consulta])
    return resultado[0]