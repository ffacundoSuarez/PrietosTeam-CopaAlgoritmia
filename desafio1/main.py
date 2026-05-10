equipos = {}
equiposOrdenados = []
partidosRegistrados = []
cantidadEquiposMax = 4

def main():
    
    with open("desafio1/partidos.txt", "r") as archivo:
        cantLineas = archivo.readline()
        cantidadPartidos = int(cantLineas.strip())

        for i in range(cantidadPartidos):
            linea = archivo.readline()
            division = linea.split()
            equipoLocal = division[0].upper()
            equipoVisitante = division[1].upper()
            golesLocal = int(division[2])
            golesVisitante = int(division[3])

            if equipoLocal < equipoVisitante:
                id_partido = equipoLocal + "-" + equipoVisitante
            else:
                id_partido = equipoVisitante + "-" + equipoLocal

            if id_partido in partidosRegistrados:
                print(f"Aviso: El partido {equipoLocal} vs {equipoVisitante} ya está repetido en el archivo. Lo vamos a ignorar.")
                continue 
            else:
                partidosRegistrados.append(id_partido)

            if 0 <= golesLocal <= 20 and 0 <= golesVisitante <= 20:      
                for team in [equipoLocal, equipoVisitante]:
                    if team not in equipos and len(equipos) < cantidadEquiposMax:
                        equipos[team] = {
                            "puntos": 0,
                            "golesAFavor": 0,
                            "golesEnContra": 0,
                            "diferenciaGol": 0,
                            "partidosJugados": 0,
                        }
                
                if equipoLocal not in equipos or equipoVisitante not in equipos:
                    print(f"Error: El partido {equipoLocal}-{equipoVisitante} involucra un 5to equipo. Lo vamos a ignorar.")
                    continue

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
  
            else:
                print(f"Partido descartado: Goles fuera de rango (0-20)")

    for nombre in equipos:
        puntos = equipos[nombre]["puntos"]
        difGol = equipos[nombre]["diferenciaGol"]
        golesFavor = equipos[nombre]["golesAFavor"]
        equiposOrdenados.append([nombre, puntos, difGol, golesFavor])

    equiposOrdenados.sort(key=lambda x: (-x[1], -x[2], -x[3], x[0]))
    
    print("Clasificados:")
    print(equiposOrdenados[0][0]) 
    print(equiposOrdenados[1][0]) 
    print("Tercero:")
    print(equiposOrdenados[2][0]) 


main()  
