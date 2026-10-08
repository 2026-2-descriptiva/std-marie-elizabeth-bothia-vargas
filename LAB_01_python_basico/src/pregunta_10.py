import pandas as pd


def pregunta_10():
    """
    Para cada registro del archivo, en el mismo orden en que aparecen,
    retorne una tupla con la letra de la primera columna (`letter`), la
    cantidad de elementos de la cuarta columna (`codes`) y la cantidad de
    pares de la quinta columna (`metrics`). El resultado es una lista con una
    tupla por registro.

    Ejemplo del formato de la respuesta:

        [("E", 3, 5), ("A", 3, 4), ("B", 4, 4), ...]
    """

    df = pd.read_csv(
        "data/data.csv.gz",
        header=None,
        sep="\t",
    )

    resultado = []

    for _, fila in df.iterrows():
        letter = fila[0]
        # Cantidad de elementos en la cuarta columna (índice 3)
        num_codes = len(fila[3].split(","))
        # Cantidad de elementos/pares en la quinta columna (índice 4)
        num_metrics = len(fila[4].split(","))

        resultado.append((letter, num_codes, num_metrics))

    return resultado

if __name__ == "__main__":
 print(pregunta_10())   
