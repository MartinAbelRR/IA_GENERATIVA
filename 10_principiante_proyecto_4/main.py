from langchain_openai import OpenAI
from configs.prompts import few_shot_prompt_template

# Si trabajas con modelos de chat como gpt-4, usa ChatOpenAI. Para tareas de completado de texto tradicional, usa OpenAI.
llm = OpenAI(temperature= .9, model= 'gpt-3.5-turbo-instruct') 

consulta = "¿Qué es una casa?"

print(few_shot_prompt_template.format(plantilla_usuario_consulta= consulta, plantilla_opcion_edad= "niño", plantilla_opcion_tipoTarea= "escribe una copia de ventas"))
print(llm.invoke(few_shot_prompt_template.format(plantilla_usuario_consulta= consulta, plantilla_opcion_edad= "niño", plantilla_opcion_tipoTarea= "escribe una copia de ventas")))