from langchain.schema import AIMessage, SystemMessage, HumanMessage

def formato_conversacion(conversacion):
    formato_conversacion = []

    if conversacion[0]['rol'] == 'sistema':
        formato_conversacion.append(SystemMessage(content= conversacion[0]['contenido']))

    print(conversacion)
    
    for mensaje in conversacion[1:]:
        if mensaje['rol'] == 'humano':
            formato_conversacion.append(HumanMessage(content= mensaje['contenido']))
        elif mensaje['rol'] == 'asistente':
            formato_conversacion.append(AIMessage(content= mensaje['contenido']))

    return formato_conversacion