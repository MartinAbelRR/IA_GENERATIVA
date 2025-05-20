# Librerías

# Nos ayuda a generar incrustaciones.
# Una incrustación es un vector (lista) de números de coma flotante. La distancia entre dos vectores mide su relación. Las distancias pequeñas sugieren una alta relación y las distancias grandes sugieren una baja relación.
from langchain_openai import AzureOpenAIEmbeddings

# FAISS es una biblioteca de código abierto desarrollada por Facebook AI Research para la búsqueda eficiente de similitudes y la agrupación de conjuntos de datos a gran escala. 
# Proporciona estructuras y algoritmos de indexación optimizados para tareas como sistemas de recomendación y búsqueda de vecinos más cercanos.
from langchain_community.vectorstores import FAISS

# Le permite utilizar Streamlit, un marco para crear aplicaciones web interactivas. Proporciona funciones para crear interfaces de usuario, mostrar datos y manejar entradas de usuarios.
import streamlit as st

# El siguiente fragmento nos ayuda a importar datos de archivos CSV para nuestras tareas.
from langchain_community.document_loaders import CSVLoader

# Inicializar el objeto de incrustación.
incrustaciones = AzureOpenAIEmbeddings(
    api_key= "DD9qeB494VetXsszNahzx70q1cuVztjearZBV0q9PrZNZeTg9VFGJQQJ99ALACYeBjFXJ3w3AAABACOGM3Gs",
    azure_endpoint= "https://open-ai-ma.openai.azure.com/openai/deployments/text-embedding-3-small/embeddings?api-version=2023-05-15",
    api_version= "2023-05-15"
) # Crear un objeto de la clase AzureOpenAIEmbeddings.

cargador = CSVLoader(file_path= './data/data.csv', csv_args= {
    'delimiter': ',', # Delimitador de los datos.
    'quotechar': '"', # Caracter de comillas.
    'fieldnames': ['Palabras'], # Nombres de los campos.
})

data = cargador.load()
# print(data)

# Crear un índice FAISS: Un índice es una estructura de datos que se utiliza para buscar rápidamente elementos en una base de datos.
db = FAISS.from_documents(
    data,
    incrustaciones
)

# Al usar st.set_page_config(), puede personalizar la apariencia de la página web de su aplicación Streamlit.
st.set_page_config(
    page_title="Ayuda para la Educación de los Niños",
    page_icon= "🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.header("Ayuda para la Educación de los Niños")

# Función para recibir la entrada del usuario.
def get_user_input():
    user_input = st.text_input("Ingrese una palabra", key= input)
    return user_input

user_input = get_user_input()
submit = st.button("Buscar palabras similares")

if submit:
    # Si el botón de envío se presiona, se buscarán palabras similares.
    docs = db.similarity_search(user_input)

    st.subheader("Palabras similares")
    st.text(docs[0].page_content)
    st.text(docs[1].page_content)