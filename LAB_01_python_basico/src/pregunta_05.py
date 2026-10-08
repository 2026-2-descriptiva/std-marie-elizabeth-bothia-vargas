import pandas as pd


def pregunta_05():
    """
    Para cada letra de la primera columna (`letter`), encuentre el valor
    máximo y el valor mínimo de la segunda columna (`value`). Retorne una lista
    de tuplas `(letra, máximo, mínimo)` ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 9, 2), ("B", 9, 1), ...]

    """
    #Leo el dataset comprimido desde pandas
    df= pd.read_csv("data/data.csv.gz", 
                         header=None, sep="\t")
    # Agrupo por la columna 0 y obtener 'max' y 'min' de la columna 1
    agrupado = df.groupby(0)[1].agg(["max", "min"]).sort_index()

    # Convierto el DataFrame a lista de tuplas [(letra, max, min), ...]
    return list(agrupado.itertuples(name=None))
    
# Esta línea ejecuta la función e imprime el resultado en la terminal:
if __name__ == "__main__":
    print(pregunta_05())



