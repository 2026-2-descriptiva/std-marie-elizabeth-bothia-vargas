import pandas as pd


def pregunta_11():
    """
    La cuarta columna (`codes`) contiene letras minúsculas separadas por
    comas. Para cada una de esas letras, sume los valores de la segunda
    columna (`value`) de los registros en los que aparece. Retorne un
    diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"a": 122, "b": 49, "c": 91, ...}
    """

    df = pd.read_csv(
        "data/data.csv.gz",
        header=None,
        sep="\t",
    )

    acumulado = {}

    # Recorremos la segunda columna (valores) y la cuarta (códigos)
    for value, codes in zip(df[1], df[3]):
        # Convertimos el valor a entero
        val = int(value)
        # Separamos las letras minúsculas por coma
        letras = codes.split(",")
        
        for letra in letras:
            acumulado[letra] = acumulado.get(letra, 0) + val

    # Retornamos el diccionario ordenado alfabéticamente por clave
    return dict(sorted(acumulado.items()))


if __name__ == "__main__":
    print(pregunta_11())
