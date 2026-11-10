
import os
import glob
import pandas as pd

def pregunta_01():
    """
    Las frases de este laboratorio no están en una tabla, sino en miles de    archivos de texto organizados en carpetas. Dentro de `data/` hay dos
    carpetas, `train/` y `test/`, y cada una contiene las carpetas
    `negative/`, `neutral/` y `positive/`. Cada archivo `.txt` contiene una
    frase, y la carpeta donde se encuentra indica su sentimiento.

    Su tarea es construir un dataset para cada división y guardarlo en:

    - `submission/train_dataset.csv`
    - `submission/test_dataset.csv`

    Cada archivo debe tener dos columnas: `phrase`, con el texto de la frase,
    y `target`, con el nombre de la carpeta de sentimiento (`negative`,
    `neutral` o `positive`). Recorra las carpetas y los archivos en orden
    alfabético, de modo que el resultado sea siempre el mismo. No guarde el
    índice de Pandas en el CSV.

    Ejemplo del formato de cada archivo:

        phrase,target
        "The real estate company posted a net loss ...",negative
        ...
        "Cardona slowed her vehicle , turned around ...",neutral
        ...
    """   
    def create_dataset(input_dir, output_filepath):
        data = []
        
        # Obtener los sentimientos (carpetas) en orden alfabético
        sentiments = sorted(os.listdir(input_dir))
        
        for sentiment in sentiments:
            sentiment_path = os.path.join(input_dir, sentiment)
            
            # Verificar que sea una carpeta
            if os.path.isdir(sentiment_path):
                # Obtener y ordenar alfabéticamente los archivos .txt
                txt_files = sorted(glob.glob(os.path.join(sentiment_path, "*.txt")))
                
                for file_path in txt_files:
                    with open(file_path, "r", encoding="utf-8") as f:
                        phrase = f.read().strip()
                        data.append({"phrase": phrase, "target": sentiment})
        
        # Crear el DataFrame y exportarlo a CSV sin el índice
        df = pd.DataFrame(data)
        
        # Asegurar que el directorio de salida exista
        os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
        
        df.to_csv(output_filepath, index=False, encoding="utf-8")

    # Obtener la ruta base del directorio actual (src/) y subir un nivel para llegar al laboratorio
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    train_path = os.path.join(base_dir, "data", "train")
    test_path = os.path.join(base_dir, "data", "test")
    train_out = os.path.join(base_dir, "submission", "train_dataset.csv")
    test_out = os.path.join(base_dir, "submission", "test_dataset.csv")

    # Procesar train y test usando rutas robustas
    create_dataset(train_path, train_out)
    create_dataset(test_path, test_out)
    print("Archivos creados exitosamente en la carpeta submission/")
    
if __name__ == "__main__":
    pregunta_01()