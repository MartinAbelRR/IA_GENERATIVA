import streamlit as st
from utils import *

# Definir la app.
def main():
    st.title('Resumen de llamadas de clientes importantes')

    # Subir multiples archivos.
    subir_archivos = st.file_uploader('Sube los archivos de audio', type= ['MP3', 'mp3', 'wav'], accept_multiple_files= True)

    if subir_archivos:
        st.write('Archivos subidos:')

        # Mostrar los archivos subidos y botones en un formulario tabulado.
        for archivo in subir_archivos:
            nombre_archivo = f'data/audio/{archivo.name}'

            col1, col2, col3 = st.columns([0.1, 1, 2])

            with col1:
                st.write('-')
            with col2:
                st.write(nombre_archivo)
            with col3:
                enviar_button = st.button(f'Resumir y enviar a {nombre_archivo}', key= nombre_archivo)

                if enviar_button:
                    texto_leido = resumir_audio(nombre_archivo)
                    st.write(texto_leido)
                    st.success(f'Email enviado a {nombre_archivo} con éxito!')

# Ejecutar la app.
if __name__ == '__main__':
    main()