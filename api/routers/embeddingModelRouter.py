from utils.indice import get_faiss_index
from fastapi import APIRouter, UploadFile
from typing import List

embeddingModelRouter = APIRouter(
    prefix= "/embedding-model",
    tags= ["embeddingModel"],
    responses= {404: {"description": "Not found"}}
)


@embeddingModelRouter.post('/')
async def post_file(files: List[UploadFile]):
    global indice
    # Verificar que el archivo sea de tipo texto, excel, csv, pdf o audio.
    for file in files:
        if file.content_type not in ["text/plain", "application/vnd.ms-excel", "text/csv", "application/pdf", "audio/mpeg"]:
            return {"error": f"El archivo {file.filename} no es de tipo texto, pdf, excel, csv o audio."}
        
    # Guardar los archivos en el servidor.
    for file in files:
        # Si el archivo es de tipo texto.
        if file.content_type == "text/plain":
            with open(f"uploads/texts/{file.filename}", "wb") as buffer:
                buffer.write(await file.read())
        # Si el archivo es de tipo excel.
        elif file.content_type == "application/vnd.ms-excel":
            with open(f"uploads/escels/{file.filename}", "wb") as buffer:
                buffer.write(await file.read())
        # Si el archivo es de tipo csv.
        elif file.content_type == "text/csv":
            # Crear un índice FAISS.
            with open(f"uploads/csvs/{file.filename}", "wb") as buffer:
                buffer.write(await file.read())
            indice = get_faiss_index(file.filename, file.content_type)
                
        # Si el archivo es de tipo pdf.
        elif file.content_type == "application/pdf":
            with open(f"uploads/pdfs/{file.filename}", "wb") as buffer:
                buffer.write(await file.read())
        # Si el archivo es de tipo audio.
        elif file.content_type == "audio/mpeg":
            with open(f"uploads/audios/{file.filename}", "wb") as buffer:
                buffer.write(await file.read())
    
    return {"message": "Archivos guardados correctamente."}

@embeddingModelRouter.get('/')
async def get_pala_similar(palabra: str):
    docs = indice.similarity_search(palabra)
    # Retornar las 2 palabras más similares.
    return {"palabras_similares": [docs[0].page_content, docs[1].page_content]}