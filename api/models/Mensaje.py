from pydantic import BaseModel

class Mensaje(BaseModel):
    contenido: str
    rol: str