import asyncio
from googletrans import Translator
import streamlit as st
from utils_user import *    

traductor = Translator()

if 'tickets_hr' not in st.session_state:
    st.session_state['tickets_hr'] = []
if 'tickets_it' not in st.session_state:
    st.session_state['tickets_it'] = []
if 'tickets_transporte' not in st.session_state:
    st.session_state['tickets_transporte'] = []

def main():
    st.header('Herramienta de Clasificación de Ticket Automatizada')

    # Capturar el entrada del usuario.
    st.write('Nosotros estamos aquí para ayudarte, por favor escribe tu pregunta:')
    user_entrada = st.text_input('🔍')

    if user_entrada:
         # Crear la instancia de incrustador.
        incrustador = crear_incrustador()

         # Recuperar la data del indice de Pinecone.
        indice = recuperar_data('pcsk_W3Snq_BApRmVFtDqgvJpFUDP4ehy8jNQmdP8jjNipa2Gwww75pxvr9gx2UsHuAQprZFTc', 'vectorstore')
        
         # Esta función nos ayudará en buscar el documento más similar.
        docs_similares = get_docs_similares(indice, user_entrada, k= 2)

        # Esta función nos ayudará en obtener la respuesta.
        respuesta = get_respuesta(docs_similares, user_entrada)
        st.write('Respuesta:')
        st.write(respuesta)

        # Button para enviar el ticket.
        button_ticket = st.button('¿Enviar Ticket?')

        if button_ticket:
            st.write('Ticket Enviado')

            consulta = incrustador.embed_query(asyncio.run(traductor.translate(user_entrada, src= 'es', dest= 'en')).text)

            # Cargando el modelo ML, para que podamos usarlo para predecir la clase a la que pertenece este cumplimiento.
            prediccion_departamento = predecir(consulta)
            if prediccion_departamento == 'HORA':
                st.write('El departamento al que pertenece este ticket es: HR')
            else:
                st.write(f'El departamento al que pertenece este ticket es: {prediccion_departamento}')

            # Añadiendo el ticket a la lista de abajo, para que podamos verlos/usarlos más adelante.
            if prediccion_departamento == 'HORA':
                st.session_state['tickets_hr'].append(user_entrada)
            elif prediccion_departamento == 'IT':
                st.session_state['tickets_it'].append(user_entrada)
            else:
                st.session_state['tickets_transporte'].append(user_entrada)

if __name__ == '__main__':
    main()