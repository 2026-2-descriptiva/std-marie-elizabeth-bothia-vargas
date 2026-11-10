
import os
import json
import pandas as pd


def main():
    """
    Antes de limpiar o analizar un conjunto de datos, un analista debe
    documentar qué problemas tiene. En este laboratorio usted no va a limpiar
    `data/ventas.csv.gz`: va a construir un reporte de calidad que deje evidencia
    de sus problemas, tal como están en el archivo.

    Lea `data/ventas.csv.gz` sin modificar sus valores. Para trabajar con los
    encabezados, normalícelos: páselos a minúsculas, elimine los espacios al
    inicio y al final (y cualquier marca BOM) y reemplace los espacios
    internos por `_`. Las columnas requeridas son `supplier_id`, `supplier`,
    `country`, `city`, `purchase_date`, `amount`, `discount`, `weight`,
    `units`, `unit_price` y `contact_email`.

    Escriba el reporte en `submission/data_quality_report.json` con estas
    claves:

    - `row_count`: cantidad de filas de datos.
    - `column_count`: cantidad de columnas.
    - `missing_required_columns`: lista ordenada de columnas requeridas que no
      están en el archivo.
    - `unexpected_columns`: lista ordenada de columnas del archivo que no son
      requeridas.
    - `duplicate_row_count`: cantidad de filas idénticas a una fila anterior.
    - `duplicate_supplier_id_row_count`: cantidad de filas cuyo `supplier_id`
      aparece más de una vez (cuente todas esas filas, no solo las
      repetidas).
    - `missing_value_count_by_column`: diccionario con la cantidad de valores
      faltantes de cada columna. Considere faltantes las celdas vacías y las
      que contienen `N/A`.
    - `invalid_email_count`: cantidad de valores de `contact_email` que no
      tienen la forma `usuario@dominio.extension`.
    - `invalid_unit_count`: cantidad de valores numéricos de `units` que no son
      enteros positivos. Los valores faltantes no se cuentan aquí.
    - `country_values`: lista ordenada de los valores distintos de `country`,
      escritos exactamente como aparecen en el archivo.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "row_count": 103,
          "column_count": 11,
          "missing_required_columns": [],
          ...
          "country_values": [" Colombia ", "CO", ...]
        }
    """
# Obtener rutas de forma robusta basadas en la ubicación de este archivo (src/)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "ventas.csv.gz")
    output_filepath = os.path.join(base_dir, "submission", "data_quality_report.json")

    # 1. Leer el archivo CSV comprimido sin modificar sus valores
    df = pd.read_csv(file_path, compression='gzip', low_memory=False)

    # 2. Normalizar los encabezados: minúsculas, limpiar espacios/BOM y reemplazar espacios internos por '_'
    df.columns = (
        df.columns.str.lower()
        .str.strip()
        .str.replace('\ufeff', '', regex=True)
        .str.replace(r'\s+', '_', regex=True)
    )

    # Columnas requeridas
    required_columns = [
        'supplier_id', 'supplier', 'country', 'city', 
        'purchase_date', 'amount', 'discount', 'weight', 
        'units', 'unit_price', 'contact_email'
    ]

    actual_columns = list(df.columns)

    # 3. Métricas básicas
    row_count = len(df)
    column_count = len(actual_columns)

    # 4. Columnas requeridas faltantes e inesperadas
    missing_required_columns = sorted([col for col in required_columns if col not in actual_columns])
    unexpected_columns = sorted([col for col in actual_columns if col not in required_columns])

    # 5. Filas duplicadas idénticas
    duplicate_row_count = int(df.duplicated().sum())

    # 6. Filas cuyo supplier_id aparece más de una vez
    if 'supplier_id' in actual_columns:
        duplicate_supplier_id_row_count = int(df['supplier_id'].duplicated(keep=False).sum())
    else:
        duplicate_supplier_id_row_count = 0

    # 7. Valores faltantes por columna (vacíos, NaN o 'N/A')
    missing_value_count_by_column = {}
    for col in actual_columns:
        s = df[col]
        is_missing = s.isna() | (s.astype(str).str.strip().str.upper() == 'N/A')
        missing_value_count_by_column[col] = int(is_missing.sum())

    # 8. Correos inválidos (no cumplen usuario@dominio.extension)
    if 'contact_email' in actual_columns:
        email_pattern = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
        valid_mask = df['contact_email'].astype(str).str.match(email_pattern, na=False)
        invalid_email_count = int((~valid_mask).sum())
    else:
        invalid_email_count = 0

    # 9. Unidades inválidas (no son enteros positivos)
    if 'units' in actual_columns:
        units_num = pd.to_numeric(df['units'], errors='coerce')
        not_null = units_num.notna()
        is_not_integer = not_null & (units_num % 1 != 0)
        is_not_positive = not_null & (units_num <= 0)
        invalid_unit_count = int((is_not_integer | is_not_positive).sum())
    else:
        invalid_unit_count = 0

    # 10. Valores distintos de country
    if 'country' in actual_columns:
        unique_countries = df['country'].dropna().unique().tolist()
        country_values = sorted([str(c) for c in unique_countries])
    else:
        country_values = []

    # Construir el diccionario del reporte
    report = {
        "row_count": row_count,
        "column_count": column_count,
        "missing_required_columns": missing_required_columns,
        "unexpected_columns": unexpected_columns,
        "duplicate_row_count": duplicate_row_count,
        "duplicate_supplier_id_row_count": duplicate_supplier_id_row_count,
        "missing_value_count_by_column": missing_value_count_by_column,
        "invalid_email_count": invalid_email_count,
        "invalid_unit_count": invalid_unit_count,
        "country_values": country_values
    }

    # Escribir el reporte en formato JSON en la carpeta submission
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
    with open(output_filepath, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=4)

    return report

if __name__ == "__main__":
    main()
    
