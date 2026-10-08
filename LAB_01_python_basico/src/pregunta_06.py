import pandas as pd


def pregunta_06():
    """
    La quinta columna (`metrics`) contiene pares `clave:valor` separados por
    comas. Para cada clave, encuentre el valor mínimo y el valor máximo que
    aparecen en todo el archivo. Retorne una lista de tuplas
    `(clave, mínimo, máximo)` ordenada alfabéticamente por la clave.

    Observe que el orden es mínimo y luego máximo, al contrario de la
    pregunta 5.

    Ejemplo del formato de la respuesta:

        [("aaa", 1, 9), ("bbb", 1, 9), ...]
    """

    #leo el archivo comprimodo
    df = pd.read_csv(
        "data/data.csv.gz", header=None, sep="\t"
    )

    data = []

    #  Descone cada celda de la columna 4 en pares (clave, valor)
    for fila in df[4]:
        elementos = fila.split(",")
        for item in elementos:
            clave, valor = item.split(":")
            data.append((clave, int(valor)))

    # Creo un DataFrame con todos los pares clave-valor
    df_metrics = pd.DataFrame(data, columns=["clave", "valor"])

    # Agrupo por clave y obtener min y max
    resultado = (
        df_metrics.groupby("clave")["valor"].agg(["min", "max"]).sort_index()
    )

    # Convierto a lista de tuplas [(clave, min, max), ...]
    return list(resultado.itertuples(name=None))
    returned() 
if __name__ == "__main__":
    print(pregunta_06())