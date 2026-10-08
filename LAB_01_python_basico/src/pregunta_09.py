import pandas as pd


def pregunta_09():
    """
    Cuente cuántas veces aparece cada clave en la quinta columna (`metrics`)
    de todo el archivo. Retorne un diccionario `{clave: cantidad}` con las
    claves en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"aaa": 13, "bbb": 16, "ccc": 23, ...}
    """

    df=pd.read_csv("data/data.csv.gz", header=None, sep="\t")
        
    conteo = {}

    # La quinta columna corresponde al índice 4
    for fila in df[4]:
        # Separar la cadena por comas para obtener cada par "clave:valor"
        elementos = fila.split(",")
        for elemento in elementos:
            # Separar la clave del valor usando los dos puntos ":"
            clave, _ = elemento.split(":")
            # Contar las apariciones de cada clave
            conteo[clave] = conteo.get(clave, 0) + 1

    # Retornar el diccionario ordenado alfabéticamente por clave
    return dict(sorted(conteo.items()))


if __name__ == "__main__":
    print(pregunta_09())