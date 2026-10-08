import pandas as pd

def pregunta_02():
    """
    Cuente cuántos registros hay para cada letra de la primera columna
    (`letter`). Retorne una lista de tuplas `(letra, cantidad)` ordenada
    alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 8), ("B", 7), ("C", 5), ...]
    """

       # Leo el archivo comprimido directamente con pandas
    df = pd.read_csv("data/data.csv.gz", 
                     header=None, sep="\t")
    # Tomo la primera columna (columna 0), conteo de frecuencias y ordeno por letra
    conteo = df[0].value_counts().sort_index()

    # Convierto el resultado a la lista de tuplas requerida [('A', 8), ('B', 7), ...]
    return list(conteo.items())
             
# Esta línea ejecuta la función e imprime el resultado en la terminal:
if __name__ == "__main__":
    print(pregunta_02())