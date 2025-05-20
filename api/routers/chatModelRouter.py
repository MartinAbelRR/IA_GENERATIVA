from utils.conversacion import formato_conversacion
from configuracion import conversacion, asistente_virtual

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from models.Mensaje import Mensaje
from typing import List

chatModelRouter = APIRouter(
    prefix= "/chat-model",
    tags= ["chatModel"],
    responses= {404: {"description": "Not found"}}
)

@chatModelRouter.get("/")
async def get_conversacion() -> List[Mensaje]:
    return JSONResponse(content= conversacion, status_code= 200)

@chatModelRouter.post("/")
async def post_conversacion(mensaje: Mensaje) -> List[Mensaje]:
    if mensaje.rol != 'humano':
        return JSONResponse(content= {"error": "El mensaje debe ser de tipo humano"}, status_code= 400)
    
    conversacion.append(mensaje.model_dump())    

    respuesta_asistente = asistente_virtual.invoke(formato_conversacion(conversacion))

    if respuesta_asistente != None:
        data_asistente = {
            "contenido": respuesta_asistente.content,
            "rol": "asistente"
        }
        conversacion.append(data_asistente)

    return JSONResponse(content= conversacion, status_code= 200)
    
