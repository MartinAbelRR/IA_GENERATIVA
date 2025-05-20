from langchain_openai import OpenAI
from backend.configs.prompts import get_few_shot_prompt_template_segun_grupo_edad

# Si trabajas con modelos de chat como gpt-4, usa ChatOpenAI. Para tareas de completado de texto tradicional, usa OpenAI.
llm = OpenAI(temperature= .9, model= 'gpt-3.5-turbo-instruct') 

def get_respuesta_agente_marketing(consulta, opcion_edad, opcion_tipoTarea):
    few_shot_prompt_template = get_few_shot_prompt_template_segun_grupo_edad(opcion_edad)

    print(few_shot_prompt_template.format(plantilla_usuario_consulta= consulta, plantilla_opcion_edad= opcion_edad, plantilla_opcion_tipoTarea= opcion_tipoTarea))
    
    return llm.invoke(few_shot_prompt_template.format(plantilla_usuario_consulta= consulta, plantilla_opcion_edad= opcion_edad, plantilla_opcion_tipoTarea= opcion_tipoTarea))
    