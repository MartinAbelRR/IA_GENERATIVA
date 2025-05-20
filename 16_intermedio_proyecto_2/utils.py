from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
import pandas as pd

def consulta_agente(data, consulta):
    # Cargar el archivo CSV en un DataFrame de pandas.
    df = pd.read_csv(data, sep= ';')

    # Crear el agente de LangChain
    llm = ChatOpenAI(model= 'gpt-3.5-turbo')

    # Crear el agente de pandas DataFrame.
    agent = create_pandas_dataframe_agent(llm, df, verbose= True, allow_dangerous_code= True)

    # Ejecutar la consulta.
    response = agent.invoke(consulta)
    
    return response