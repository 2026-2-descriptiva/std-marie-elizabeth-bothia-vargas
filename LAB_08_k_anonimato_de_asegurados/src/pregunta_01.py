
import json
from pathlib import Path
import pandas as pd

def pregunta_01():
    """
    Una aseguradora quiere publicar datos de sus afiliados para que un grupo
    de investigación estudie el costo de los seguros, sin que nadie pueda
    reconocer a una persona. El archivo `data/insurance.csv.gz` tiene una fila
    por afiliado con su edad (`age`), sexo (`sex`), índice de masa corporal
    (`bmi`), número de hijos (`children`), si fuma (`smoker`), región
    (`region`) y el costo de su seguro (`charges`).

    El archivo no tiene nombres ni documentos, pero eso no basta: la edad, el
    sexo, el índice de masa corporal, el número de hijos y la región son
    cuasi-identificadores, porque combinados pueden señalar a una persona.
    `smoker` es el atributo sensible que se quiere proteger.

    En este laboratorio usted va a medir el riesgo de reidentificación y a
    decidir qué publicar. Use estas definiciones:

    - Una clase de equivalencia es un grupo de registros con los mismos
      valores en todos los cuasi-identificadores. Un conjunto de datos cumple
      k-anonimato si toda clase tiene al menos k registros. Use k = 5.
    - `age_group`: `18-29`, `30-39`, `40-49` o `50-64`.
    - `bmi_group`: `bajo peso` (menos de 18.5), `normal` (desde 18.5 y menos
      de 25), `sobrepeso` (desde 25 y menos de 30) u `obesidad` (30 o más).
    - `children_group`: `0`, `1-2` o `3+`.

    Evalúe dos esquemas de generalización:

    - `with_children`: `age_group`, `sex`, `bmi_group`, `children_group` y
      `region`.
    - `without_children`: `age_group`, `sex`, `bmi_group` y `region`; el
      número de hijos no se publica.

    En cada esquema, suprima (no publique) los registros de las clases con
    menos de 5 registros. Luego, entre las clases publicadas, identifique las
    que no tienen diversidad en el atributo sensible, es decir, aquellas en
    las que todos los afiliados fuman o ninguno fuma: en esas clases, saber
    que alguien pertenece a ellas revela si fuma.

    Escriba `submission/privacy_report.json` con estas claves:

    - `original_k`: el menor tamaño de clase usando los cuasi-identificadores
      originales, sin generalizar.
    - `original_unique_records`: cuántos registros son los únicos de su clase
      con los cuasi-identificadores originales.
    - `schemes`: un diccionario con una entrada por esquema (`with_children` y
      `without_children`), cada una con las claves `quasi_identifiers` (la
      lista de columnas del esquema), `equivalence_classes` (clases antes de
      suprimir), `k_before_suppression`, `suppressed_records`,
      `published_records`, `published_classes`,
      `classes_without_smoker_diversity` y
      `records_without_smoker_diversity`.
    - `selected_scheme`: el esquema que suprime menos registros.
    - `mean_charges_original` y `mean_charges_published`: el costo promedio
      de todos los afiliados y el de los registros publicados con el esquema
      seleccionado.
    - `smoker_rate_original` y `smoker_rate_published`: la proporción de
      fumadores en ambos casos.

    Escriba también `submission/insurance_published.csv`, sin el índice de
    Pandas, con los registros publicados del esquema seleccionado, en el
    mismo orden del archivo original, y las columnas del esquema seguidas de
    `smoker` y `charges`.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "original_k": 1,
          "original_unique_records": 1330,
          "schemes": {
            "with_children": {
              "quasi_identifiers": ["age_group", "sex", ...],
              "equivalence_classes": 278,
              ...
            },
            ...
          },
          ...
        }
    """
    base_dir = Path(__file__).resolve().parent.parent
    input_path = base_dir / "data" / "insurance.csv.gz"
    output_dir = base_dir / "submission"
    report_path = output_dir / "privacy_report.json"
    published_path = output_dir / "insurance_published.csv"

    # Cargar los datos originales
    df = pd.read_csv(input_path)

    # Calcular métricas originales (sin generalizar)
    original_qis = ["age", "sex", "bmi", "children", "region"]
    original_sizes = df.groupby(original_qis, observed=False).size()
    original_k = int(original_sizes.min())
    original_unique_records = int((original_sizes == 1).sum())

    # Crear columnas generalizadas
    df["age_group"] = pd.cut(
        df["age"],
        bins=[17, 29, 39, 49, 64],
        labels=["18-29", "30-39", "40-49", "50-64"],
    ).astype(str)

    df["bmi_group"] = pd.cut(
        df["bmi"],
        bins=[0, 18.5, 25.0, 30.0, float("inf")],
        labels=["bajo peso", "normal", "sobrepeso", "obesidad"],
        right=False,  # Intervalos [a, b): incluye izquierda, excluye derecha
    ).astype(str)

    df["children_group"] = pd.cut(
        df["children"],
        bins=[-1, 0, 2, float("inf")],
        labels=["0", "1-2", "3+"],
    ).astype(str)

    # Evaluar los dos esquemas
    schemes_def = {
        "with_children": ["age_group", "sex", "bmi_group", "children_group", "region"],
        "without_children": ["age_group", "sex", "bmi_group", "region"],
    }

    schemes_report = {}
    published_dfs = {}

    for scheme_name, qis in schemes_def.items():
        # Tamaño de clase por fila antes de suprimir
        class_sizes = df.groupby(qis).transform("size")
        group_counts = df.groupby(qis).size()

        equivalence_classes = int(len(group_counts))
        k_before_suppression = int(group_counts.min())

        # Suprimir registros en clases con menos de k=5 registros
        mask_published = class_sizes >= 5
        suppressed_records = int((~mask_published).sum())
        published_df = df[mask_published].copy()
        published_records = int(len(published_df))

        # Calcular clases publicadas y falta de diversidad en `smoker`
        if published_records > 0:
            smoker_nunique = published_df.groupby(qis)["smoker"].nunique()
            published_classes = int(len(smoker_nunique))
            classes_without_diversity = int((smoker_nunique == 1).sum())

            # Contar cuántos registros publicados pertenecen a esas clases sin diversidad
            class_smoker_nunique = published_df.groupby(qis)["smoker"].transform("nunique")
            records_without_diversity = int((class_smoker_nunique == 1).sum())
        else:
            published_classes = 0
            classes_without_diversity = 0
            records_without_diversity = 0

        schemes_report[scheme_name] = {
            "quasi_identifiers": qis,
            "equivalence_classes": equivalence_classes,
            "k_before_suppression": k_before_suppression,
            "suppressed_records": suppressed_records,
            "published_records": published_records,
            "published_classes": published_classes,
            "classes_without_smoker_diversity": classes_without_diversity,
            "records_without_smoker_diversity": records_without_diversity,
        }
        published_dfs[scheme_name] = published_df

    # Seleccionar el esquema que suprime menos registros
    selected_scheme = min(
        schemes_report, key=lambda s: schemes_report[s]["suppressed_records"]
    )
    selected_qis = schemes_def[selected_scheme]
    selected_df = published_dfs[selected_scheme]

    # Calcular promedios de costo y tasas de fumadores
    mean_charges_original = float(df["charges"].mean())
    mean_charges_published = float(selected_df["charges"].mean())
    smoker_rate_original = float((df["smoker"] == "yes").mean())
    smoker_rate_published = float((selected_df["smoker"] == "yes").mean())

    # Armar el reporte final
    report = {
        "original_k": original_k,
        "original_unique_records": original_unique_records,
        "schemes": schemes_report,
        "selected_scheme": selected_scheme,
        "mean_charges_original": mean_charges_original,
        "mean_charges_published": mean_charges_published,
        "smoker_rate_original": smoker_rate_original,
        "smoker_rate_published": smoker_rate_published,
    }

    # Guardar JSON y CSV en `submission/`
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    output_cols = selected_qis + ["smoker", "charges"]
    selected_df[output_cols].to_csv(published_path, index=False)

    return report  
