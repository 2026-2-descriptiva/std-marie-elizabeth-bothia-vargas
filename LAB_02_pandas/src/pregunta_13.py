import pandas as pd


def pregunta_13():
    """
    Combine las tablas `data/tbl0.tsv` y `data/tbl2.tsv` usando la columna
    `c0`, que ambas comparten. Luego, sume los valores de la columna `c5b`
    para cada categoría de la columna `c1`. Retorne una Serie de Pandas cuyo
    índice son las categorías, en orden alfabético, y cuyos valores son las
    sumas.

    Ejemplo del formato de la respuesta:

        c1
        A    146
        B    134
        C     81
        ...
    """
#cargar datos
    df0=pd.read_csv("data/tbl0.tsv", sep="\t")
    df2=pd.read_csv("data/tbl2.tsv", sep="\t")
    
    df_merged = pd.merge(df0, df2, on="c0")
    
    #  Agrupar por la columna 'c1', seleccionar 'c5b', sumar y ordenar el índice alfabéticamente
    df = df_merged.groupby("c1")["c5b"].sum().sort_index()
    
   
    return df

if __name__ == "__main__":
    print(pregunta_13())
