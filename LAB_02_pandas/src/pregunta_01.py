import pandas as pd

def pregunta_01():
    """
    ¿Cuántos registros tiene la tabla `data/tbl0.tsv`? Retorne la cantidad
    como un número entero.

    Ejemplo del formato de la respuesta:

        40
    """
 #Leer la data
    df= pd.read_csv("data/tbl0.tsv", sep="\t")
    #verifico la longitud
    return len(df)
#  visualizar resultado en la terminal
if __name__ == "__main__":
    print(pregunta_01())
    
