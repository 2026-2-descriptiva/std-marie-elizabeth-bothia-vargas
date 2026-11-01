
from pathlib import Path

import pandas as pd
import re

def pregunta_01():
    """
    El archivo `data/clusters_report.txt` es un reporte de clústeres de
    palabras clave pensado para ser leído por una persona, no por un programa:
    los encabezados ocupan varias líneas, las columnas están alineadas con
    espacios y la lista de palabras clave de un clúster continúa en las líneas
    siguientes.

    Su tarea es convertir ese reporte en un DataFrame de Pandas con una fila
    por clúster y las columnas:

    - `cluster`: número del clúster, como entero.
    - `cantidad_de_palabras_clave`: como entero.
    - `porcentaje_de_palabras_clave`: como número decimal; por ejemplo, el
      texto `15,9 %` debe quedar como `15.9`.
    - `principales_palabras_clave`: todas las palabras clave del clúster en un
      solo texto, separadas por una coma y un único espacio.

    Retorne el DataFrame.

    Ejemplo del formato de la respuesta (se omite la última columna):

           cluster  cantidad_de_palabras_clave  porcentaje_de_palabras_clave
        0        1                         105                          15.9
        1        2                         102                          15.4
        ...
    """

import pandas as pd
import re

def pregunta_01():
    # Abrimos el archivo de texto donde está el reporte
    filepath = "data/clusters_report.txt"
    # filepath = "LAB_03_ingestion_de_texto_plano/data/clusters_report.txt"
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    clusters_data = []
    current_cluster = None
    current_cantidad = None
    current_porcentaje = None
    current_keywords = []

    for line in lines:
        stripped_line = line.strip()
        
        # Omitir líneas vacías, encabezados o líneas divisorias
        if not stripped_line or "---" in stripped_line or "cluster" in stripped_line.lower() or "palabras" in stripped_line.lower():
            continue

        # Separar la línea intentando detectar el número de clúster al inicio
        partes = stripped_line.split(maxsplit=3)
        
        if len(partes) >= 3 and partes[0].isdigit():
            # Si ya teníamos un clúster anterior, lo procesamos y guardamos
            if current_cluster is not None:
                texto_completo = re.sub(r"\s+", " ", " ".join(current_keywords)).strip()
                # Limpiar puntos finales, comas sobrantes y espacios múltiples
                texto_completo = texto_completo.rstrip(".")
                keywords_list = [kw.strip() for kw in texto_completo.split(",") if kw.strip()]
                principales_palabras = ", ".join(keywords_list)
                
                clusters_data.append({
                    "cluster": int(current_cluster),
                    "cantidad_de_palabras_clave": int(current_cantidad),
                    "porcentaje_de_palabras_clave": float(current_porcentaje.replace(",", ".")),
                    "principales_palabras_clave": principales_palabras
                })

            # Capturar nuevo clúster
            current_cluster = partes[0]
            current_cantidad = partes[1]
            current_porcentaje = partes[2].lstrip("%").strip()
            current_keywords = [partes[3].lstrip("%").strip()] if len(partes) > 3 else []
        else:
            # Línea de continuación de palabras clave
            if current_cluster is not None:
                current_keywords.append(stripped_line)

    # Guardar el último clúster
    if current_cluster is not None:
        texto_completo = re.sub(r"\s+", " ", " ".join(current_keywords)).strip()
        texto_completo = texto_completo.rstrip(".")
        keywords_list = [kw.strip() for kw in texto_completo.split(",") if kw.strip()]
        principales_palabras = ", ".join(keywords_list)
        
        clusters_data.append({
            "cluster": int(current_cluster),
            "cantidad_de_palabras_clave": int(current_cantidad),
            "porcentaje_de_palabras_clave": float(current_porcentaje.replace(",", ".")),
            "principales_palabras_clave": principales_palabras
        })

    df = pd.DataFrame(clusters_data)
    return df

if __name__ == "__main__":
    print(pregunta_01())