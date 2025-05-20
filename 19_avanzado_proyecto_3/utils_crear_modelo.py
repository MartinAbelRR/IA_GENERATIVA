import asyncio
from googletrans import Translator
from langchain_huggingface import HuggingFaceEmbeddings
import pandas as pd
from sklearn.model_selection import train_test_split

traductor = Translator()

def leer_data(data):
    df = pd.read_csv(data, delimiter= ',', header= None)
    return df

# Crear la instancia de incrustador.
def get_incrustrador():
    incrustador = HuggingFaceEmbeddings(model_name= 'sentence-transformers/all-MiniLM-L6-v2')
    return incrustador

# Generar incrustaciones para cada una de las oraciones.
def crear_incrustaciones(df, incrustador):
    # Generar incrustaciones para cada una de las oraciones.
    df[2] = df[0].apply(lambda x: incrustador.embed_query(asyncio.run(traductor.translate(x, src= 'en', dest= 'es')).text))
    df[3] = df[1].apply(lambda x: asyncio.run(traductor.translate(x, src= 'en', dest= 'es')).text)
    return df

# Divididor los datos en conjuntos de entrenamiento y prueba.
def dividir_data_entrenamiento_y_prueba(df):
    df.to_csv('data_limpia.csv', index= False)
    # Dividir los datos en dos conjuntos: entrenamiento y prueba.
    X_entrenamiento, X_prueba, y_entrenamiento, y_prueba = train_test_split(
        list(df[2]), list(df[3]), test_size= 0.25, random_state= 0
    )
    return X_entrenamiento, X_prueba, y_entrenamiento, y_prueba

# Obtener el score del modelo.
def get_puntuacion(modelo, X_prueba, y_prueba):
    puntuacion = modelo.score(X_prueba, y_prueba)
    return puntuacion


