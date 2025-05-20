import streamlit as st
from utils_admin import *

def main():
    st.set_page_config(page_title= 'Cargar PDF a Pinecone', page_icon= ':books:', layout= 'wide')
    st.title('Por favor cargue su archivo PDF... :books:')

    # Subir el archivo PDF.
    pdf = st.file_uploader('Sube tu archivo PDF', type= 'pdf', label_visibility= 'collapsed')

    # Extraer el texto desde el PDF.
    if pdf is not None:
        with st.spinner('Espera para esto...'): # Mostrar un spinner mientras se procesa el archivo: Un spinner es un indicador de carga que muestra que el programa está trabajando en algo.
            texto = leer_data_pdf(pdf) # Leer el archivo PDF.
            st.write('El archivo PDF ha sido cargado con éxito. Ahora, vamos a extraer el texto del PDF y cargarlo en Pinecone...') # Mensaje de éxito.

            # Crear pedazos de texto.
            docs_dividos = dividir_data(texto)
            # st.write()
            st.write('Hecho el división de texto...')

            # Crear incrustador de texto.
            incrustador = crear_incrustador()
            st.write('Hecho el creador de incrustador de texto...')

            # Construir la tienda de vectores (Subir el la data del PDF a Pinecone).
            subir_data('pcsk_W3Snq_BApRmVFtDqgvJpFUDP4ehy8jNQmdP8jjNipa2Gwww75pxvr9gx2UsHuAQprZFTc', 'vectorstore', incrustador, docs_dividos)

        
        st.success('El texto ha sido extraído y cargado en Pinecone con éxito.') # Mensaje de éxito.

if __name__ == '__main__':
    main()

