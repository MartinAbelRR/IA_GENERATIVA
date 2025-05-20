from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain.schema import SystemMessage
from models.Mensaje import Mensaje
from typing import List

# Configuración de nuestro asistente virtual.
data_sistema = {
    "contenido": SystemMessage(content= "Eres un asistente virtual.").content,
    "rol": "sistema"
}

# Inicialización nuestro asistente virtual.
asistente_virtual = AzureChatOpenAI(
    azure_endpoint= "https://openai-mr.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-08-01-preview",
    api_version= '2024-08-01-preview',
    temperature= 0.7,
    max_tokens= 100,
)

# Incialización de nuestro Incrustador.
incrustaciones = AzureOpenAIEmbeddings(
    api_key= "4fvn3Tm9Lqbnb0sDmS7tcrCLbNdzAvD7oowZpecVJAVkBSu7z3XeJQQJ99BAACYeBjFXJ3w3AAABACOGvMmt",
    azure_endpoint= "https://openai-mr.openai.azure.com/openai/deployments/text-embedding-3-small/embeddings?api-version=2023-05-15",
    api_version= "2023-05-15"
) # Crear un objeto de la clase AzureOpenAIEmbeddings.

# Inicialización de la conversación.
conversacion: List[Mensaje] = []

conversacion.append(data_sistema)

