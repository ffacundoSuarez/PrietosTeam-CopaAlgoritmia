equipos = {}
equiposOrdenados = []
cantidadPartidos = 6
cantidadEquiposMax = 4

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
            if team not in equipos and len(equipos) < cantidadEquiposMax:
                equipos[team] = {
                    "puntos": 0,
                    "golesAFavor": 0,
                    "golesEnContra": 0,
                    "diferenciaGol": 0,
                    "partidosJugados": 0,
                }
        
        # CALCULO PUNTAJES
        if golesLocal > golesVisitante:
            equipos[equipoLocal]["puntos"] += 3
        elif golesVisitante > golesLocal:
            equipos[equipoVisitante]["puntos"] += 3
        else:
            equipos[equipoLocal]["puntos"] += 1
            equipos[equipoVisitante]["puntos"] += 1

        # STATS EQUIPO LOCAL        
        equipos[equipoLocal]["golesAFavor"] += golesLocal
        equipos[equipoLocal]["golesEnContra"] += golesVisitante
        equipos[equipoLocal]["partidosJugados"] += 1

        # STATS EQUIPO VISITANTE
        equipos[equipoVisitante]["golesAFavor"] += golesVisitante
        equipos[equipoVisitante]["golesEnContra"] += golesLocal
        equipos[equipoVisitante]["partidosJugados"] += 1

        # CALCULO DIFERENCIA DE GOL
        equipos[equipoLocal]["diferenciaGol"] = equipos[equipoLocal]["golesAFavor"] - equipos[equipoLocal]["golesEnContra"]    
        equipos[equipoVisitante]["diferenciaGol"] = equipos[equipoVisitante]["golesAFavor"] - equipos[equipoVisitante]["golesEnContra"]


        {
            'ARG': {'puntos': 9, 'golesAFavor': 10, 'golesEnContra': 4, 'diferenciaGol': 6, 'partidosJugados': 3}, 
            'BRA': {'puntos': 0, 'golesAFavor': 0, 'golesEnContra': 8, 'diferenciaGol': -8, 'partidosJugados': 3}, 
            'HOL': {'puntos': 6, 'golesAFavor': 9, 'golesEnContra': 6, 'diferenciaGol': 3, 'partidosJugados': 3}, 
            'GER': {'puntos': 3, 'golesAFavor': 5, 'golesEnContra': 6, 'diferenciaGol': -1, 'partidosJugados': 3}
        }

        
    print(equipos)  
    

        

main()  
