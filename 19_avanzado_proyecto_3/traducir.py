import asyncio
from googletrans import Translator
async def traducir():   
    traductor = Translator()

    resultado = await traductor.translate('Hola mundo', src='es', dest='en')

    print(resultado.text)

    return resultado.text

asyncio.run(traducir())