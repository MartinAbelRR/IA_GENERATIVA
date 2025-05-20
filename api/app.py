from fastapi import FastAPI
from routers.chatModelRouter import chatModelRouter
from routers.embeddingModelRouter import embeddingModelRouter

app = FastAPI()

@app.get("/")
async def get_root():
    return {"Hello": "World"}

app.include_router(chatModelRouter)
app.include_router(embeddingModelRouter)