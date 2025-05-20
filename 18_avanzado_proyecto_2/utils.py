import asyncio
from langchain_community.document_loaders import SitemapLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone as PineconeClient

# Función para buscar data desde un sitio web.
def get_data_sitio_web(sitemap_url):
    bucle = asyncio.new_event_loop() # Crear un nuevo bucle de eventos: Sirve para ejecutar código asíncrono.
    asyncio.set_event_loop(bucle) # Establecer el nuevo bucle de eventos como el bucle actual.
    cargador = SitemapLoader(sitemap_url) # Crear un cargador de Sitemap.

    docs = cargador.load() # Cargar los datos desde el Sitemap.

    return docs # Retornar los documentos cargados.

# Función para dividir la data en partes más pequeñas.
def dividir_data(docs):
    divididor_texto = RecursiveCharacterTextSplitter(
        chunk_size= 1000, # Tamaño del chunk.
        chunk_overlap= 200, # Superposición entre los chunks.
        length_function= len # Función para calcular la longitud del texto.
    )

    docs_divididos = divididor_texto.split_documents(docs) # Dividir los documentos en partes más pequeñas.
    return docs_divididos # Retornar los documentos divididos.

# Función para crar una instancia de incrustador.
def crear_incrustador():
    incrustador = HuggingFaceEmbeddings(model_name= 'all-MiniLM-L6-v2')
    return incrustador # Retornar el incrustador creado.

# Función para subir la data a Pinecone.
def subir_data(pinecone_api_key, pinecone_nombre_indice, incrustador, docs):
    pc = PineconeClient(api_key= pinecone_api_key)
    indice = pc.Index(pinecone_nombre_indice) # Crear un índice de Pinecone: Un indice es una colección de vectores.
    vector_store = PineconeVectorStore( 
        index= indice,
        embedding= incrustador,
        pinecone_api_key= pinecone_api_key
    )
    
    return vector_store.add_documents(docs)

# Función para recuperar la data de Pinecone.
def recuperar_data(pinecone_api_key, pinecone_nombre_indice):
    pc = PineconeClient(api_key= pinecone_api_key)
    indice = pc.Index(pinecone_nombre_indice) # Crear un índice de Pinecone: Un indice es una colección de vectores.

    vector_store = PineconeVectorStore(
        index= indice,
        embedding= crear_incrustador(),
        pinecone_api_key= pinecone_api_key
    )


    return vector_store.as_retriever()

# Función para realizar la búsqueda en Pinecone.
def get_docs_similares(indice, consulta, k= 5):
    docs_similares = indice.invoke(consulta, k= k) # Obtener los documentos más relevantes.
    return docs_similares # Retornar los documentos más relevantes.