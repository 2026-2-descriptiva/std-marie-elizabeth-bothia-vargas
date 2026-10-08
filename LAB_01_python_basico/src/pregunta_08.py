import pandas as pd


def pregunta_08():
    """
    Repita la pregunta 7, pero ahora cada lista de letras debe contener cada
    letra una sola vez y estar ordenada alfabéticamente. Retorne una lista de
    tuplas `(valor, letras)` ordenada por el valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["B", "E"]), (2, ["A", "E"]), ...]
    """
    df=pd.read_csv("data/data.csv.gz", header=None, sep="\t")
    
    df = df.rename(columns={0: "letter", 1: "value"})

    # Para eliminar duplicados y ordenar las letras de cada grupo:
    resultado = (
        df.groupby("value")["letter"]
        .apply(lambda x: sorted(list(set(x))))
        .reset_index()
    )

    return list(zip(resultado["value"], resultado["letter"]))

if __name__ == "__main__":
 print(pregunta_08())