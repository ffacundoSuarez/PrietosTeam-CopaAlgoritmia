


def main():
    print("desafio 2")

    with open("desafio2/penales.txt", "r") as archivo:
        penales = archivo.readline()
        for i in penales:
            print(i)
            if i not in ["L", "C", "R"]:
                print("Esa letra no corresponde a nada.")
    



main()