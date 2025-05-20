import asyncio
from googletrans import Translator
import joblib # Para guardar y cargar modelos de machine learning.
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline # Para crear un pipeline: Un pipeline es una secuencia de pasos de procesamiento de datos y modelado.
from sklearn.preprocessing import StandardScaler
import streamlit as st
from utils_crear_modelo import *

traductor = Translator()

st.time_input('Vamos a construir un modelo de machine learning.')

# Crear lista los titulos de las pestañas.
pestanias_titulos = ['Preprocesamiento de datos', 'Entrenamiento del modelo', 'Evaluación del modelo', 'Guardar el modelo']
pestanias = st.tabs(pestanias_titulos)

if 'data_limpia' not in st.session_state:
    st.session_state['data_limpia'] = ''
if 'data_entrenamiento' not in st.session_state:
    st.session_state['data_entrenamiento'] = ''
if 'data_prueba' not in st.session_state:
    st.session_state['data_prueba'] = ''
if 'etiqueta_entrenamiento' not in st.session_state:
    st.session_state['etiqueta_entrenamiento'] = ''
if 'etiqueta_prueba' not in st.session_state:
    st.session_state['etiqueta_prueba'] = ''
if 'clasificador_svm' not in st.session_state:
    st.session_state['clasificador_svm'] = ''


# Agregar conenido a cada pestaña.

# Pestaña 1: Preprocesamiento de datos.
with pestanias[0]:
    st.header('Preprocesamiento de datos')
    st.write('Aquí nosotros preprocesamos los datos...')

    # Cargar los datos.
    data = st.file_uploader('Cargar datos', type= ['csv', 'xlsx'])

    button = st.button('Cargar datos', key= 'cargar_datos')

    if button:
        with st.spinner('Cargando datos...'):
            nuestra_data = leer_data(data)
            incrustador = get_incrustrador()

            # Generar incrustaciones para cada una de las oraciones.
            st.session_state['data_limpia'] = crear_incrustaciones(nuestra_data, incrustador)
        st.success('Datos cargados correctamente.')

# Pestaña 2: Entrenamiento del modelo.
with pestanias[1]:
    st.header('Entrenamiento del modelo')
    st.write('Aquí nosotros entrenamos el modelo...')

    button = st.button('Entrenar modelo', key= 'entrenar_modelo')

    if button:
        with st.spinner('Entrenando modelo...'):
            st.session_state['data_entrenamiento'], st.session_state['data_prueba'], st.session_state['etiqueta_entrenamiento'], st.session_state['etiqueta_prueba'] = dividir_data_entrenamiento_y_prueba(st.session_state['data_limpia'])

            # Inicializar un modelo SVM, con class_weight= 'balanced' para manejar el desbalanceo de clases.
            # porque nuestro conjunto de entrenamiento tiene una cantidad aproximada y equitativa de oraciones de sentimiento positivas y negativas.
            st.session_state['clasificador_svm'] = make_pipeline(StandardScaler(), SVC(class_weight= 'balanced')) # Pipeline: Un pipeline es una secuencia de pasos de procesamiento de datos y modelado: Lo que hace es que primero escala los datos y luego entrena el modelo SVM.

            # Ajustar el modelo SVM a los datos de entrenamiento.
            st.session_state['clasificador_svm'].fit(st.session_state['data_entrenamiento'], st.session_state['etiqueta_entrenamiento'])
        st.success('Modelo entrenado correctamente.')

# Pestaña 3: Evaluación del modelo.
with pestanias[2]:
    st.header('Evaluación del modelo')
    st.write('Aquí nosotros evaluamos el modelo...')

    button = st.button('Evaluar modelo', key= 'evaluar_modelo')

    if button:
        with st.spinner('Evaluando modelo...'):
            puntuacion_precision = get_puntuacion(st.session_state['clasificador_svm'], st.session_state['data_prueba'], st.session_state['etiqueta_prueba'])
            st.success(f'Puntuación del modelo: {100 * puntuacion_precision}%') 

            # Texto de muestra.
            texto = 'Conductor grosero con conducción temeraria.'
            st.write(f'NUestro problema: {texto}')

            # Convertir nuestro texto a incrustación.
            incrustador = get_incrustrador()
            texto_incrustado = incrustador.embed_query(asyncio.run(traductor.translate(texto, src= 'es', dest= 'en')).text)

            # Predicción usando el modelo SVM.
            resultado = st.session_state['clasificador_svm'].predict([texto_incrustado])
            st.write(f'Departamento al que pertenece: {resultado[0]}')


        st.success('Modelo evaluado correctamente.')
    
# Pestaña 4: Guardar el modelo.
with pestanias[3]:
    st.header('Guardar el modelo')
    st.write('Aquí nosotros guardamos el modelo...')

    button = st.button('Guardar modelo', key= 'guardar_modelo')

    if button:
        with st.spinner('Guardando modelo...'):
            joblib.dump(st.session_state['clasificador_svm'], '19_avanzado_proyecto_3/model/modelo_svm.pkl')

        st.success('Modelo guardado correctamente.')