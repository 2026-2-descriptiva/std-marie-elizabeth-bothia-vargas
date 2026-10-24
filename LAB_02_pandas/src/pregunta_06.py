import pandas as pd


def pregunta_06():
    """
    Usando `data/tbl1.tsv`, obtenga los valores distintos de la columna `c4`,
    conviértalos a mayúsculas y retórnelos como una lista ordenada
    alfabéticamente.

    Ejemplo del formato de la respuesta:

        ["A", "B", "C", "D", "E", "F", "G"]
    """

    df= pd.read_csv("data/tbl1.tsv", sep="\t")
    
    mayusculas = df['c4'].dropna().astype(str).str.upper().unique()
    
    #  Convertir el resultado a una lista y ordenarla alfabéticamente
    mayusculas = sorted(list(mayusculas))
    return mayusculas
    
if __name__ == "__main__":
    print(pregunta_06())
    
