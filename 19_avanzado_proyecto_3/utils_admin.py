from pypdf import PdfReader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone as PineconeClient

# Funciones para cargar y procesar la data.
def leer_data_pdf(pdf_file):
    pdf_cargar = PdfReader(pdf_file) # Leer el archivo PDF.
    texto = ""
    for page in pdf_cargar.pages:
        texto += page.extract_text()
    return texto # Retornar el texto extraído del PDF.

# Función para dividir la data en partes más pequeñas.
def dividir_data(texto):
    divididor_texto = RecursiveCharacterTextSplitter(
        chunk_size= 1000, # Tamaño del chunk.
        chunk_overlap= 50, # Superposición entre los chunks.
        length_function= len # Función para calcular la longitud del texto.
    )

    texto_dividido = divididor_texto.split_text(text= texto) # Dividir el texto en partes más pequeñas.
    docs_divididos = divididor_texto.create_documents(texts= texto_dividido) # Crear documentos a partir del texto dividido.
    
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
        pinecone_api_key= pinecone_api_key,
        namespace= 'avanzado_proyecto_3'
    )
    
    return vector_store.add_documents(docs)