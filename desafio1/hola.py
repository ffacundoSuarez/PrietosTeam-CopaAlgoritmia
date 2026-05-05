equipos = {
    "pais1": {
        "nombre": "",
        "golesLocal": 0,
        "golesVisitante": 0,
        "golesEnContra": 0,
        "puntos": 0,
    },
    "pais2": {
        "nombre": "",
        "golesLocal": 0,
        "golesVisitante": 0,
        "golesEnContra": 0,
        "puntos": 0,
    },
    "pais3": {
        "nombre": "",
        "golesLocal": 0,
        "golesVisitante": 0,
        "golesEnContra": 0,
        "puntos": 0,
    },
    "pais4": {
        "nombre": "",
        "golesLocal": 0,
        "golesVisitante": 0,
        "golesEnContra": 0,
        "puntos": 0,
    },
}

cantidadPartidos = 6
cantidadEquipos = 4

def ocuparEquipo():
    print()

def main():
    print("Ingrese Los resultados del partido de la siguiente forma (EquipoLocal EquipoVisitante GolesLocal GolesVisitante)")
    print("Ejemplo: ARG BRA 1 0")
    for i in range(1,cantidadPartidos + 1):
        linea = input("Partido " + str(i) + ": ")    
        for x in range(1,5):
            ocuparEquipo()
        


main()