def procesar_penales(secuencia):

    """
    Analiza la frecuencia de tiros y determina la dirección dominante.
    Aplica la prioridad táctica L > R > C en caso de empate.
    
    Parametro que recibe:
        secuencia (str): Cadena de caracteres con direcciones L, R o C. Si no es alguna de esas letras, la ignora.
        
    Retorna:
        tupla: (dirección_frecuente, cantidad) o (None, None) si es inválida.
    """


    if 1 <= len(secuencia) <= 1000:

        contadores = {
            'L': 0, 
            'R': 0, 
            'C': 0
        }

        for tiro in secuencia:
            if tiro.upper() in contadores:
                contadores[tiro.upper()] += 1

        if contadores['L'] == 0 and contadores['R'] == 0 and contadores['C'] == 0:
            return None, None
                            
        max_dir = 'L'
        max_cant = contadores['L']
                
        if contadores['R'] > max_cant:
            max_dir = 'R'
            max_cant = contadores['R']
                    
        if contadores['C'] > max_cant:
            max_dir = 'C'
            max_cant = contadores['C']

        return max_dir, max_cant

    else:
        return None, None


def main():
    """
    Función principal del programa.
    
    Se encarga de la entrada/salida de datos: lee la secuencia de penales 
    desde el archivo de texto provisto (penales.txt), invoca la función de procesamiento 
    y muestra los resultados.

    """

    
    try:
        with open("desafio2/penales.txt", "r") as archivo:

            secuencia = archivo.read().strip()

            resultado_dir, resultado_cant = procesar_penales(secuencia)        
            
            if resultado_dir is not None:
                print(resultado_dir)
                print(resultado_cant)

    except FileNotFoundError:
        pass

if __name__ == "__main__":
    main()
