equipos = {}
cantidadPartidos = 6
cantidadEquipos = 4

def registrarEquipo():
    print()

def main():
    print("Ingrese Los resultados del partido de la siguiente forma (EquipoLocal EquipoVisitante GolesLocal GolesVisitante)")
    print("Ejemplo: ARG BRA 1 0")
    for i in range(1,cantidadPartidos + 1):
        linea = input("Partido " + str(i) + ": ")    
        division = linea.split(" ")
        equipoLocal = division[0]
        equipoVisitante = division[1]
        golesLocal = int(division[2])
        golesVisitante = int(division[3])

        for team in [equipoLocal, equipoVisitante]:
            if team not in equipos:
                equipos[team] = {
                    "puntos": 0,
                    "golesAFavor": 0,
                    "golesEnContra": 0
                }
        
        equipos[equipoLocal]["golesAFavor"] += golesLocal
        equipos[equipoVisitante]["golesEnContra"] += golesVisitante

        equipos[equipoVisitante]["golesAFavor"] += golesVisitante
        equipos[equipoVisitante]["golesEnContra"] += golesLocal

        

main()  