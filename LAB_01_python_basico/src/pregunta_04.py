import pandas as pd


def pregunta_04():
    """
    Cuente cuántos registros hay en cada mes, usando la fecha de la tercera
    columna (`date`). Represente el mes como un texto de dos dígitos y retorne
    una lista de tuplas `(mes, cantidad)` ordenada por el mes.

    Ejemplo del formato de la respuesta:

        [("01", 3), ("02", 4), ("03", 2), ...]
    """
    #leo el el archivo comprimido directamente con pandas
    df = pd.read_csv("data/data.csv.gz", 
                     header=None, sep="\t")
    # Extrae los caracteres del mes directamente del texto "YYYY-MM-DD"
    # Tomamos los caracteres entre las posiciones 5 y 7 (el mes)
    meses = df[2].astype(str).str[5:7]
    

    # Cuento y ordeno por el mes
    conteo = meses.value_counts().sort_index()

    # Converto a la lista de tuplas requerida
    return list(conteo.items())
    
# Esta línea ejecuta la función e imprime el resultado en la terminal para verificar:
if __name__ == "__main__":
    print(pregunta_04())
    
     
    
  
