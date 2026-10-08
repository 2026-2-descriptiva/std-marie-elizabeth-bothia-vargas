import pandas as pd


def pregunta_03():
    """
    Sume los valores de la segunda columna (`value`) para cada letra de la
    primera columna (`letter`). Retorne una lista de tuplas `(letra, suma)`
    ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 53), ("B", 36), ("C", 27), ...]

    """
    #leo el el archivo comprimido directamente con pandas
    df = pd.read_csv("data/data.csv.gz", 
                     header=None, sep="\t")     

    #  Agrupar por la columna 0 (letter) y sumar los valores de la columna 1 (value)
    suma_por_letra = df.groupby(0)[1].sum().sort_index()

    #  Convertir el resultado a una lista de tuplas [('A', 53), ('B', 36), ...]
    return list(suma_por_letra.items())

# Esta línea ejecuta la función e imprime el resultado en la terminal:
if __name__ == "__main__":
    print(pregunta_03())