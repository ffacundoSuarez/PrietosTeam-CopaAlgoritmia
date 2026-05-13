
def main():
    try:
        with open("desafio2/penales.txt", "r") as archivo:
            secuencia = archivo.read().strip()
            print(secuencia) 

            if 1 <= len(secuencia) <= 1000:
                contadores = {'L': 0, 'R': 0, 'C': 0}

                for tiro in secuencia:
                    if tiro.upper() in contadores:
                        contadores[tiro.upper()] += 1
                    else:
                        print("Hubo una letra que no era L-R-C")
                
                max_dir = 'L'
                max_cant = contadores['L']
                
                if contadores['R'] > max_cant:
                    max_dir = 'R'
                    max_cant = contadores['R']
                    
                if contadores['C'] > max_cant:
                    max_dir = 'C'
                    max_cant = contadores['C']
                    
                print(max_dir)
                print(max_cant)
            else:
                print("Error: los goles tienen que ser entre 1 y 1000")

    except FileNotFoundError:
        print("No se encontro el archivo 'desafio2/penales.txt'")

if __name__ == "__main__":
    main()
