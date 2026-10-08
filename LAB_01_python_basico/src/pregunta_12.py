import pandas as pd


def pregunta_12():
    """
    Para cada letra de la primera columna (`letter`), sume todos los valores
    numéricos de los pares `clave:valor` de la quinta columna (`metrics`).
    Retorne un diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"A": 177, "B": 187, "C": 114, ...}
    """

    df = pd.read_csv(
        "data/data.csv.gz",
        header=None,
        sep="\t",
    )

    acumulado = {}

    # Recorremos la primera columna (letra) y la quinta columna (métricas)
    for letter, metrics in zip(df[0], df[4]):
        # Separamos los pares por coma
        pares = metrics.split(",")
        
        # Sumamos los valores enteros de cada par "clave:valor"
        suma_fila = sum(int(par.split(":")[1]) for par in pares)
        
        # Acumulamos el total para la letra correspondiente
        acumulado[letter] = acumulado.get(letter, 0) + suma_fila

    # Retornamos el diccionario ordenado alfabéticamente por clave
    return dict(sorted(acumulado.items()))


if __name__ == "__main__":
    print(pregunta_12())