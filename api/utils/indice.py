from configuracion import incrustaciones
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS

def get_faiss_index(file, tipo):
    if tipo == "text/csv":
        cargador = CSVLoader(
            file_path= f"uploads/csvs/{file}", csv_args= {
            'delimiter': ',', # Delimitador de los datos.
            'quotechar': '"', # Caracter de comillas.
            'fieldnames': ['Palabras'], # Nombres de los campos.
        })

    return FAISS.from_documents(
        cargador.load(),
        incrustaciones
    )

