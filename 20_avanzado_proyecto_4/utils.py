from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain.schema import Document
from langchain.chains.summarize import load_summarize_chain
from pypdf import PdfReader
from pinecone import Pinecone

# Extraer información de un archivo PDF.
def get_texto_pdf(pdf):
    texto = ""
    pdf_leido = PdfReader(pdf)

    for pagina in pdf_leido.pages:
        texto += pagina.extract_text()

    return texto

# Iterar sobre los archivos PDF en que el usuario ha subido uno por uno.
def crear_docs(lista_pdfs, id_unico):
    docs = []

    for pdf in lista_pdfs:
        texo = get_texto_pdf(pdf)

        # Agregar el texto a nuestra lista - Agregar la data y su meta-data: Meta-data es la información adicional que se almacena junto con el texto, como el nombre del archivo, la fecha de creación, etc.
        docs.append(Document(page_content= texo, metadata= {'source': pdf.name, 'id_unico': id_unico, 'type': pdf.type, 'size': pdf.size}))

    return docs

# Crear una instancia de incrustador.
def crear_incrustador():
    # Crear una instancia de incrustador.
    incrustador = HuggingFaceEmbeddings(model_name= 'all-MiniLM-L6-v2', model_kwargs= {'device': 'cuda'})
    return incrustador

# Función para subir data al vector de PINECONE.
def subir_data_pinecone(pinecone_api_key, pinecone_nombre_indice, incrustador, docs, unique_id):
    pc = Pinecone(api_key= pinecone_api_key)
    indice = pc.Index(pinecone_nombre_indice) # Crear un índice de Pinecone: Un indice es una colección de vectores.
    vector_store = PineconeVectorStore( 
        index= indice,
        embedding= incrustador,
        pinecone_api_key= pinecone_api_key,
        namespace= f'avanzado_proyecto_4-{unique_id}'
    )

    return vector_store.add_documents(docs)

# Función para realizar la búsqueda en Pinecone.
def recuperar_data(pinecone_api_key, pinecone_nombre_indice, unique_id):
    pc = Pinecone(api_key= pinecone_api_key) # Crear una instancia de Pinecone.
    indice = pc.Index(pinecone_nombre_indice) # Crear un índice de Pinecone: Un indice es una colección de vectores.

    vector_store = PineconeVectorStore(
        index= indice,
        embedding= crear_incrustador(),
        pinecone_api_key= pinecone_api_key,
        namespace= f'avanzado_proyecto_4-{unique_id}'
    )

    return vector_store

# Función para obtener los documentos más relevantes.
def get_docs_similares(indice, consulta, k= 5):
    docs_similares = indice.similarity_search_with_score(query= consulta, k= k) # Realizar la búsqueda de similitud.
    return docs_similares # Retornar los documentos más relevantes.

def get_resumen(doc):
    llm = ChatOpenAI(model= 'gpt-4o-mini', temperature= 0.1) # Crear una instancia de LLM.
    chain = load_summarize_chain(llm, chain_type= 'map_reduce') # Crear una cadena de resumen map_reduce: Map-reduce es un patrón de programación que se utiliza para procesar grandes cantidades de datos en paralelo. En este caso, se utiliza para resumir el texto en partes más pequeñas y luego combinar los resultados.
    resumen = chain.invoke([doc]) # Invocar la cadena de resumen.

    return resumen # Retornar el resumen.