
import pandas as pd

def pregunta_01():
    """
    Calcule la suma de los valores de la segunda columna (`value`) del
    archivo `data/data.csv.gz` y retorne el resultado como un número entero.

    Ejemplo del formato de la respuesta:

        214
    """

     # Leo el archivo comprimido directamente con pandas
    df = pd.read_csv("data/data.csv.gz", 
                     header=None, sep="\t")
         
    
    # La segunda columna tiene índice 1
    suma = df[1].sum()
    
    return int(suma)

# Esta línea ejecuta la función e imprime el resultado en la terminal:
if __name__ == "__main__":
    print(pregunta_01())


