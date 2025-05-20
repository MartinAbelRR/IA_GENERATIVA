from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from backend.configs.ejemplos import ejemplos_ninos, get_ejemplos
from backend.configs.plantillas import ejemplos_template, prefijo, sufijo

ejemplos_prompt = PromptTemplate(
    input_variables= ["consulta", "respuesta"],
    template= ejemplos_template
)

few_shot_prompt_template = FewShotPromptTemplate(
    examples= ejemplos_ninos,
    example_prompt= ejemplos_prompt,
    prefix= prefijo,
    suffix= sufijo,
    input_variables= ["plantilla_usuario_consulta", "plantilla_opcion_edad", "plantilla_opcion_tipoTarea"],
    example_separator= "\n\n"
)

def get_few_shot_prompt_template_segun_grupo_edad(grupoEdad):
    ejemplos_grupo = get_ejemplos(grupoEdad)
    few_shot_prompt_template.examples = ejemplos_grupo
    return few_shot_prompt_template