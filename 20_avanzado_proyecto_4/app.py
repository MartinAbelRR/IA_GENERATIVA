import asyncio
from googletrans import Translator

import streamlit as st
import uuid
from utils import *

def main():
    st.set_page_config(page_title= 'Asistencia en la Revisión de CVs', page_icon= ':guardsman:', layout= 'wide')
    st.title('HR- Asistencia en la Revisión de CVs')
    st.subheader('Puedo ayudarte a revisar los CVs de los candidatos para el puesto de trabajo que necesites. Solo tienes que subir el archivo y yo me encargaré del resto.')

    # Entrada del usuario.
    descripcion_puesto = st.text_area('Porfavor pega el la descripción del puesto de trabajo que necesitas cubrir:', key= '1')
    cantidad_cvs = st.text_input('¿Cuántos CVs quieres filtrar?', key= '2')
    
    # Subir los CVs (solo archivos PDF).
    pdf = st.file_uploader('Sube los CVs (solo archivos PDF)', type= 'pdf', accept_multiple_files= True)

    # Botón para enviar.
    enviar = st.button('Ayudar a Revisar CVs')

    if enviar:
        with st.spinner('Revisando CVs...'):
            st.write('Nuestro proceso de revisión de CVs ha comenzado. Porfavor espera un momento mientras revisamos los CVs.')
            # Crear un unico ID, para que podamos usar la consulta y obtener solo los documentos cargados por el usuario desde store vector Pinecone.
            st.session_state['id_unico'] = str(uuid.uuid4().hex)
            # st.write(st.session_state['id_unico'])

            # Crear una lista de documento a partir de los archivos PDF subidos por el usuario.
            docs = crear_docs(pdf, st.session_state['id_unico'])
            # st.write(docs)

            # Mostrar la cantidad de CVs que el usuario ha subido.
            st.write(f'Has subido {len(pdf)} CVs para revisar.')

            # Crear una instancia de incrustador.
            incrustador = crear_incrustador()

            # Subir data a PINECONE.
            subir_data_pinecone('pcsk_W3Snq_BApRmVFtDqgvJpFUDP4ehy8jNQmdP8jjNipa2Gwww75pxvr9gx2UsHuAQprZFTc', 'vectorstore', incrustador, docs, '76d8d32d2cda4e66b6c79350f546ffa0')
            st.write('Los CVs han sido subidos a PINECONE.')

            # Buscar documentos relevantes desde PINECONE. 
            indice = recuperar_data('pcsk_W3Snq_BApRmVFtDqgvJpFUDP4ehy8jNQmdP8jjNipa2Gwww75pxvr9gx2UsHuAQprZFTc', 'vectorstore', '76d8d32d2cda4e66b6c79350f546ffa0')
            docs_similares = get_docs_similares(indice, descripcion_puesto, k= int(cantidad_cvs))
            # st.write(f'Los documentos más relevantes son: {docs_similares}')

            # Intrudicr una linea de separación.
            st.write(':heavy_minus_sign:' * 30)

            #Para cada documento similar, mostrar el nombre del archivo y el texto.
            for item in range(len(docs_similares)):
                st.subheader(':guardsman: CVs más relevantes :guardsman: ' + str(item + 1))

                # Mostrar la ruta del archivo.
                st.write('Nombre del archivo: ' + docs_similares[item][0].metadata['source'])

                # Introducir una línea de separación.
                with st.expander('Mostrar CV'):
                    st.info('Puntunación de similitud: ' + str(docs_similares[item][1]))

                    # Obtener un resumen de los item actuales usando una función `get_resumen` que nos creará usando LLM & Langchain.
                    resumen = get_resumen(docs_similares[item][0])
                    
                    # Traducir el resumen de forma asíncrona con asyncio.to_thread.
                    traductor = Translator() # Crear una instancia de Goslate para la traducción.
                    texto_traducido = asyncio.run(traductor.translate(resumen['output_text'], dest= 'es')) # Traducir el texto al español.
                    st.write(texto_traducido.text)


if __name__ == '__main__':
    main()