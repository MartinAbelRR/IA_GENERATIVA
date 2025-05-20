from langchain_openai import ChatOpenAI
import os
import whisper

def resumir_audio(archivo_audio):
    """
    Esta función toma un archivo de audio y devuelve su transcripción.
    """
    
    # Cargar el modelo Whisper.
    modelo = whisper.load_model("base")

    # Transcribir el audio.
    resultado = modelo.transcribe(archivo_audio)

    # Configurar el modelo de lenguaje.
    llm = ChatOpenAI(
        model_name= "gpt-3.5-turbo",
        temperature= 0.1,
        max_tokens= 200
    )

    response = llm.invoke('Resume el siguiente texto: ' + resultado['text'])

    return response.content