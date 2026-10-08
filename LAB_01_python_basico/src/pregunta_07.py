import pandas as pd


def pregunta_07():
    """
    Para cada valor distinto de la segunda columna (`value`), construya la
    lista de letras de la primera columna (`letter`) que aparecen con ese
    valor. Conserve las letras repetidas y el orden en que aparecen en el
    archivo. Retorne una lista de tuplas `(valor, letras)` ordenada por el
    valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["E", "B", "E"]), (2, ["A", "E"]), ...]
    """
    #Leo el comprimido
    df = pd.read_csv(
            "data/data.csv.gz", header=None, sep="\t"
        )
    
   # Asigno nombres a las dos primeras columnas para manipularlas fácilmente
    df = df.rename(columns={0: "letter", 1: "value"})

    # Agrupo por la columna 'value' conservando el orden de 'letter'
    resultado = (
        df.groupby("value")["letter"]
        .apply(list)
        .reset_index()
    )

    # Convierto a lista de tuplas (valor, lista_de_letras)
    return list(zip(resultado["value"], resultado["letter"]))

if __name__ == "__main__":
 print(pregunta_07())

