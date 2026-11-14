
import pandas as pd
import os
import re
from pathlib import Path
from pandas import DataFrame

def pregunta_01():
    """
    El archivo `data/solicitudes_de_credito.csv.gz` contiene las solicitudes de
    un programa de crédito, pero llegó sucio: tiene una columna de índice que
    no pertenece a los datos, registros duplicados, registros incompletos y
    valores que representan lo mismo escritos de formas distintas en los
    campos de texto, las fechas, el estrato y el monto.

    Su tarea es limpiarlo y guardar el resultado en
    `submission/solicitudes_de_credito.csv`, usando punto y coma (`;`) como
    separador y sin el índice de Pandas.

    El archivo limpio debe cumplir lo siguiente:

    - Contiene solamente las nueve columnas `sexo`, `tipo_de_emprendimiento`,
      `idea_negocio`, `barrio`, `estrato`, `comuna_ciudadano`,
      `fecha_de_beneficio`, `monto_del_credito` y `línea_credito`, en ese
      orden.
    - Los campos de texto están en minúsculas y sus palabras separadas por
      espacios.
    - `estrato` y `monto_del_credito` son números enteros, sin símbolos ni
      separadores de miles.
    - Todas las fechas de `fecha_de_beneficio` usan un mismo formato, por
      ejemplo `AAAA-MM-DD`.
    - No hay registros incompletos. La única excepción es
      `comuna_ciudadano`: sus valores faltantes son parte de los datos
      originales y deben conservarse.
    - No hay registros duplicados.

    Ejemplo del formato del archivo:

        sexo;tipo_de_emprendimiento;idea_negocio;barrio;estrato;...
        femenino;comercio;almacen de ropa en;los cerros el vergel;2;...
        ...
    """
    # Definir la ruta base del laboratorio (funciona desde cualquier directorio)
    base_dir = Path(__file__).resolve().parent.parent
    input_path = base_dir / "data" / "solicitudes_de_credito.csv.gz"
    output_dir = base_dir / "submission"
    output_path = output_dir / "solicitudes_de_credito.csv"

    #  Cargar el archivo
    df = pd.read_csv(input_path, sep=";", index_col=0)

    # Seleccionar explícitamente las 9 columnas en el orden requerido
    columnas = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "estrato",
        "comuna_ciudadano",
        "fecha_de_beneficio",
        "monto_del_credito",
        "línea_credito",
    ]
    df = df[columnas].copy()

    # Eliminar registros incompletos (excepto en `comuna_ciudadano`)
    columnas_obligatorias = [col for col in columnas if col != "comuna_ciudadano"]
    df = df.dropna(subset=columnas_obligatorias)

    #  Estandarizar textos: minúsculas, sin guiones y palabras unidas por un espacio
    text_columns = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "línea_credito",
    ]
    for col in text_columns:
        df[col] = (
            df[col]
            .str.lower()
            .str.replace("-", " ", regex=False)
            .str.replace("_", " ", regex=False)
            .str.split()
            .str.join(" ")
        )

    #  Limpiar y convertir `estrato` y `monto_del_credito` a enteros 
    df["estrato"] = df["estrato"].astype(int)
    df["monto_del_credito"] = (
        df["monto_del_credito"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
        .astype(float)
        .astype(int)
    )

   #  Unificar fechas a AAAA-MM-DD contemplando múltiples formatos
    fechas = pd.Series(pd.NaT, index=df.index)
    for fmt in ("%d/%m/%Y", "%Y/%m/%d", "%Y-%m-%d", "%d-%m-%Y"):
        fechas = fechas.fillna(
            pd.to_datetime(df["fecha_de_beneficio"], format=fmt, errors="coerce")
        )
    df["fecha_de_beneficio"] = fechas.dt.strftime("%Y-%m-%d")

    #  Eliminar duplicados y asegurar el orden final de columnas
    df = df.drop_duplicates()
    df = df[columnas]

    # Guardar el resultado
    output_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, sep=";", index=False)

if __name__ == "__main__":
    pregunta_01()
