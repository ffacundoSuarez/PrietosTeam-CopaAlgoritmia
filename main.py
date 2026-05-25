"""
Copa de Algoritmia y Programación - UADE 2026
Desafío 3: "La Cancha Inteligente"

Simulación de una cancha de fútbol representada como matriz 40x60.
Permite registrar jugadores desde archivo, moverlos interactivamente,
calcular distancias Manhattan, detectar pases posibles y caminos libres al arco rival.
Incluye árbitro con movimiento aleatorio cercano a la pelota.
"""

import random

# ─────────────────────────────────────────────
# Constantes globales
# ─────────────────────────────────────────────
FILAS = 40
COLUMNAS = 60
EQUIPOS_VALIDOS = ("A", "B")
ROLES_VALIDOS = ("arquero", "defensor", "mediocampista", "delantero")
CELDA_VACIA = "."
OBSTACULO = "X"
RADIO_ARBITRO = 5


# ═══════════════════════════════════════════════════════════════
# TAREA 1: Crear la cancha
# ═══════════════════════════════════════════════════════════════

def crear_cancha():
    """
    Genera la matriz que representa la cancha de fútbol.

    Returns:
        list[list[str]]: Matriz de 40 filas × 60 columnas inicializada con ".".
    """
    cancha = []
    for _ in range(FILAS):
        fila = []
        for _ in range(COLUMNAS):
            fila.append(CELDA_VACIA)
        cancha.append(fila)
    return cancha


# ═══════════════════════════════════════════════════════════════
# TAREA 2: Posicionar jugadores
# ═══════════════════════════════════════════════════════════════

def crear_jugador(nombre, equipo, fila, columna, rol, tiene_pelota):
    """
    Construye el diccionario que representa a un jugador.

    Args:
        nombre       (str):  Nombre del jugador.
        equipo       (str):  'A' (Argentina) o 'B' (Brasil).
        fila         (int):  Fila en la cancha (0-39).
        columna      (int):  Columna en la cancha (0-59).
        rol          (str):  Rol del jugador.
        tiene_pelota (bool): True si este jugador posee la pelota.

    Returns:
        dict: Diccionario con los datos del jugador.
    """
    return {
        "nombre": nombre,
        "equipo": equipo,
        "fila": fila,
        "columna": columna,
        "rol": rol,
        "tiene_pelota": tiene_pelota
    }


def posicionar_jugador(cancha, jugadores, nombre, equipo, fila, columna, rol, tiene_pelota):
    """
    Valida y agrega un jugador a la cancha y a la lista de jugadores.

    Validaciones:
        - Posición dentro de los límites.
        - Celda no ocupada (jugador u obstáculo).
        - Rol y equipo válidos.
        - Solo un jugador con la pelota a la vez.

    Args:
        cancha       (list[list[str]]): Matriz de la cancha.
        jugadores    (list[dict]):      Lista de jugadores registrados.
        nombre       (str):             Nombre del jugador.
        equipo       (str):             Equipo ('A' o 'B').
        fila         (int):             Fila destino.
        columna      (int):             Columna destino.
        rol          (str):             Rol del jugador.
        tiene_pelota (bool):            Indica si porta la pelota.

    Returns:
        bool: True si el jugador fue agregado exitosamente, False en caso contrario.
    """
    if not _posicion_valida(fila, columna):
        print(f"[ERROR] Posición ({fila}, {columna}) fuera de los límites de la cancha.")
        return False

    if cancha[fila][columna] != CELDA_VACIA:
        print(f"[ERROR] La celda ({fila}, {columna}) ya está ocupada (contiene '{cancha[fila][columna]}').")
        return False

    if equipo not in EQUIPOS_VALIDOS:
        print(f"[ERROR] Equipo '{equipo}' inválido. Use 'A' (Argentina) o 'B' (Brasil).")
        return False

    if rol not in ROLES_VALIDOS:
        print(f"[ERROR] Rol '{rol}' inválido. Roles permitidos: {ROLES_VALIDOS}.")
        return False

    if tiene_pelota and _hay_jugador_con_pelota(jugadores):
        print("[ERROR] Ya existe un jugador con la pelota. Solo un jugador puede tenerla a la vez.")
        return False

    nuevo = crear_jugador(nombre, equipo, fila, columna, rol, tiene_pelota)
    jugadores.append(nuevo)
    cancha[fila][columna] = equipo
    print(f"[OK] Jugador '{nombre}' ({equipo} - {rol}) agregado en ({fila}, {columna}).")
    return True


def cargar_jugadores_desde_archivo(cancha, jugadores, ruta):
    """
    Lee un archivo .txt y carga los jugadores en la cancha.

    Formato esperado por línea:
        nombre,equipo,fila,columna,rol,tiene_pelota

    Args:
        cancha    (list[list[str]]): Matriz de la cancha.
        jugadores (list[dict]):      Lista de jugadores.
        ruta      (str):             Ruta al archivo .txt.

    Returns:
        None
    """
    with open(ruta, "r", encoding="utf-8") as archivo:
        for numero_linea, linea in enumerate(archivo, start=1):
            linea = linea.strip()
            if linea == "" or linea.startswith("#"):
                continue
            partes = linea.split(",")
            if len(partes) != 6:
                print(f"[ERROR] Línea {numero_linea} con formato inválido: '{linea}'.")
                continue
            nombre       = partes[0].strip()
            equipo       = partes[1].strip()
            fila         = int(partes[2].strip())
            columna      = int(partes[3].strip())
            rol          = partes[4].strip()
            tiene_pelota = partes[5].strip().lower() == "true"
            posicionar_jugador(cancha, jugadores, nombre, equipo, fila, columna, rol, tiene_pelota)


# ═══════════════════════════════════════════════════════════════
# TAREA 3: Mover jugadores
# ═══════════════════════════════════════════════════════════════

DIRECCIONES = {
    "arriba":    (-1,  0),
    "abajo":     ( 1,  0),
    "izquierda": ( 0, -1),
    "derecha":   ( 0,  1)
}


def mover_jugador(cancha, jugadores, nombre, direccion):
    """
    Desplaza al jugador una celda en la dirección indicada.

    El movimiento es inválido si:
        - La dirección no existe.
        - La nueva posición sale de la cancha.
        - La nueva celda está ocupada (jugador u obstáculo).

    Args:
        cancha     (list[list[str]]): Matriz de la cancha.
        jugadores  (list[dict]):      Lista de jugadores.
        nombre     (str):             Nombre del jugador a mover.
        direccion  (str):             'arriba', 'abajo', 'izquierda' o 'derecha'.

    Returns:
        bool: True si el movimiento fue exitoso, False si fue inválido.
    """
    jugador = _buscar_jugador(jugadores, nombre)
    if jugador is None:
        print(f"[ERROR] No se encontró al jugador '{nombre}'.")
        return False

    if direccion not in DIRECCIONES:
        print(f"[ERROR] Dirección '{direccion}' inválida. Use: {list(DIRECCIONES.keys())}.")
        return False

    delta_fila, delta_col = DIRECCIONES[direccion]
    nueva_fila = jugador["fila"] + delta_fila
    nueva_col  = jugador["columna"] + delta_col

    if not _posicion_valida(nueva_fila, nueva_col):
        print(f"[MOVIMIENTO INVÁLIDO] '{nombre}' no puede moverse a ({nueva_fila}, {nueva_col}): fuera de la cancha.")
        return False

    celda_destino = cancha[nueva_fila][nueva_col]
    if celda_destino != CELDA_VACIA:
        if celda_destino == OBSTACULO:
            razon = "obstáculo"
        else:
            razon = f"jugador del equipo '{celda_destino}'"
        print(f"[MOVIMIENTO INVÁLIDO] '{nombre}' no puede moverse a ({nueva_fila}, {nueva_col}): celda ocupada por {razon}.")
        return False

    cancha[jugador["fila"]][jugador["columna"]] = CELDA_VACIA
    jugador["fila"]    = nueva_fila
    jugador["columna"] = nueva_col
    cancha[nueva_fila][nueva_col] = jugador["equipo"]

    print(f"[MOVIMIENTO OK] '{nombre}' se movió {direccion} → ({nueva_fila}, {nueva_col}).")
    return True


# ═══════════════════════════════════════════════════════════════
# ÁRBITRO
# ═══════════════════════════════════════════════════════════════

def crear_arbitro(cancha):
    """
    Coloca al árbitro en el centro de la cancha y retorna su posición.

    Args:
        cancha (list[list[str]]): Matriz de la cancha.

    Returns:
        dict: Diccionario con la posición del árbitro.
    """
    fila    = FILAS // 2
    columna = COLUMNAS // 2
    cancha[fila][columna] = OBSTACULO
    print(f"[OK] Árbitro colocado en ({fila}, {columna}).")
    return {"fila": fila, "columna": columna}


def mover_arbitro(cancha, arbitro, jugadores):
    """
    Mueve al árbitro aleatoriamente una celda dentro de un radio cercano a la pelota.
    El árbitro ocupa la celda como obstáculo 'X'.

    Args:
        cancha    (list[list[str]]): Matriz de la cancha.
        arbitro   (dict):            Posición actual del árbitro.
        jugadores (list[dict]):      Lista de jugadores.

    Returns:
        None
    """
    portador = _obtener_portador(jugadores)
    if portador is None:
        return

    fila_pelota = portador["fila"]
    col_pelota  = portador["columna"]

    # Generar candidatos aleatorios dentro del radio cercano a la pelota
    candidatos = []
    for df in range(-RADIO_ARBITRO, RADIO_ARBITRO + 1):
        for dc in range(-RADIO_ARBITRO, RADIO_ARBITRO + 1):
            nueva_fila = fila_pelota + df
            nueva_col  = col_pelota + dc
            if not _posicion_valida(nueva_fila, nueva_col):
                continue
            if cancha[nueva_fila][nueva_col] != CELDA_VACIA:
                continue
            candidatos.append((nueva_fila, nueva_col))

    if not candidatos:
        return

    nueva_fila, nueva_col = random.choice(candidatos)

    # Liberar celda anterior y ocupar la nueva
    cancha[arbitro["fila"]][arbitro["columna"]] = CELDA_VACIA
    arbitro["fila"]    = nueva_fila
    arbitro["columna"] = nueva_col
    cancha[nueva_fila][nueva_col] = OBSTACULO
    print(f"[ÁRBITRO] Se movió a ({nueva_fila}, {nueva_col}).")


# ═══════════════════════════════════════════════════════════════
# TAREA 4: Calcular distancia a la pelota
# ═══════════════════════════════════════════════════════════════

def calcular_distancias(jugadores):
    """
    Calcula la distancia Manhattan de cada jugador respecto al que posee la pelota.
    Indica quién es el más cercano (o quiénes en caso de empate).

    Args:
        jugadores (list[dict]): Lista de jugadores registrados.

    Returns:
        None
    """
    portador = _obtener_portador(jugadores)
    if portador is None:
        print("[INFO] Ningún jugador tiene la pelota actualmente.")
        return

    print(f"\n=== Distancias Manhattan respecto a '{portador['nombre']}' (pelota en ({portador['fila']}, {portador['columna']})) ===")

    distancias = []
    for jugador in jugadores:
        if jugador is portador:
            continue
        dist = _distancia_manhattan(jugador, portador)
        distancias.append((jugador["nombre"], dist))
        print(f"  {jugador['nombre']:20s} → distancia: {dist}")

    if not distancias:
        print("  (No hay otros jugadores en la cancha.)")
        return

    minima = min(d for _, d in distancias)
    mas_cercanos = []
    for nombre, d in distancias:
        if d == minima:
            mas_cercanos.append(nombre)

    if len(mas_cercanos) == 1:
        print(f"\n[MÁS CERCANO] {mas_cercanos[0]} (distancia {minima}).")
    else:
        print(f"\n[EMPATE - MÁS CERCANOS] {', '.join(mas_cercanos)} (distancia {minima} cada uno).")


# ═══════════════════════════════════════════════════════════════
# TAREA 5: Detectar posibilidad de pase
# ═══════════════════════════════════════════════════════════════

def detectar_pases(cancha, jugadores):
    """
    Lista todos los pases posibles para el jugador que posee la pelota
    y retorna la lista de receptores disponibles.

    Un pase es posible si:
        - El receptor es del mismo equipo.
        - Están en la misma fila o columna (línea recta, sin diagonales).
        - No hay jugadores rivales, obstáculos 'X' ni el árbitro entre ellos.

    Args:
        cancha    (list[list[str]]): Matriz de la cancha.
        jugadores (list[dict]):      Lista de jugadores.

    Returns:
        list[dict]: Lista de jugadores a los que se puede pasar.
    """
    portador = _obtener_portador(jugadores)
    if portador is None:
        print("[INFO] Ningún jugador tiene la pelota actualmente.")
        return []

    print(f"\n=== Pases posibles para '{portador['nombre']}' ({portador['equipo']}) ===")

    pases_posibles = []
    for receptor in jugadores:
        if receptor is portador:
            continue
        if receptor["equipo"] != portador["equipo"]:
            continue
        if receptor["fila"] != portador["fila"] and receptor["columna"] != portador["columna"]:
            continue

        bloqueado, motivo = _camino_bloqueado(cancha, portador, receptor)
        if not bloqueado:
            pases_posibles.append(receptor)
        else:
            print(f"  [PASE BLOQUEADO] → {receptor['nombre']}: {motivo}.")

    if not pases_posibles:
        print("  No hay pases posibles disponibles.")
    else:
        for i, receptor in enumerate(pases_posibles, start=1):
            print(f"  {i}. {receptor['nombre']} en ({receptor['fila']}, {receptor['columna']}).")

    return pases_posibles


def elegir_pase(jugadores, pases_posibles):
    """
    Permite al usuario elegir a quién pasarle la pelota.
    Transfiere la posesión de la pelota al receptor elegido.

    Args:
        jugadores      (list[dict]): Lista de jugadores.
        pases_posibles (list[dict]): Lista de receptores disponibles.

    Returns:
        None
    """
    if not pases_posibles:
        return

    eleccion = input("\n¿A quién querés pasarle? (número o 'no' para no pasar): ").strip().lower()

    if eleccion == "no":
        print("[PASE] Se decidió no pasar.")
        return

    if not eleccion.isdigit():
        print("[ERROR] Ingresá un número válido.")
        return

    indice = int(eleccion) - 1
    if indice < 0 or indice >= len(pases_posibles):
        print("[ERROR] Número fuera de rango.")
        return

    portador = _obtener_portador(jugadores)
    receptor = pases_posibles[indice]

    portador["tiene_pelota"] = False
    receptor["tiene_pelota"] = True

    print(f"[PASE OK] '{portador['nombre']}' le pasó la pelota a '{receptor['nombre']}'.")


# ═══════════════════════════════════════════════════════════════
# TAREA 6: Detectar camino libre al arco
# ═══════════════════════════════════════════════════════════════

def detectar_camino_libre_al_arco(cancha, jugadores):
    """
    Analiza qué delanteros tienen camino libre hacia el arco rival.

    Condiciones para "camino libre":
        - El jugador es delantero.
        - Está en la mitad ofensiva de su equipo
          (Argentina: columnas 30-59, Brasil: columnas 0-29).
        - No existe ningún rival, obstáculo 'X' ni árbitro en la misma fila
          entre el jugador y el arco rival.

    Args:
        cancha    (list[list[str]]): Matriz de la cancha.
        jugadores (list[dict]):      Lista de jugadores.

    Returns:
        None
    """
    print("\n=== Análisis de camino libre al arco ===")

    delanteros = []
    for jugador in jugadores:
        if jugador["rol"] == "delantero":
            delanteros.append(jugador)

    if not delanteros:
        print("  No hay delanteros registrados.")
        return

    for delantero in delanteros:
        equipo  = delantero["equipo"]
        fila    = delantero["fila"]
        columna = delantero["columna"]

        en_mitad_ofensiva = (
            (equipo == "A" and 30 <= columna <= 59) or
            (equipo == "B" and 0  <= columna <= 29)
        )

        if not en_mitad_ofensiva:
            print(f"  [SIN CAMINO LIBRE] '{delantero['nombre']}': no está en la mitad ofensiva (columna {columna}).")
            continue

        if equipo == "A":
            cols_entre   = range(columna + 1, 60)
            equipo_rival = "B"
        else:
            cols_entre   = range(columna - 1, -1, -1)
            equipo_rival = "A"

        libre = True
        for col in cols_entre:
            celda = cancha[fila][col]
            if celda == OBSTACULO or celda == equipo_rival:
                libre = False
                break

        if libre:
            print(f"  [CAMINO LIBRE] '{delantero['nombre']}' tiene camino libre al arco rival desde ({fila}, {columna}).")
        else:
            print(f"  [SIN CAMINO LIBRE] '{delantero['nombre']}': hay un rival u obstáculo en la trayectoria.")


# ═══════════════════════════════════════════════════════════════
# MENÚ INTERACTIVO
# ═══════════════════════════════════════════════════════════════

def menu_interactivo(cancha, jugadores, arbitro):
    """
    Permite al usuario mover jugadores turno a turno.
    Después de cada movimiento exitoso el árbitro se mueve,
    y se muestran los pases posibles y el camino libre al arco.

    Args:
        cancha    (list[list[str]]): Matriz de la cancha.
        jugadores (list[dict]):      Lista de jugadores.
        arbitro   (dict):            Posición del árbitro.

    Returns:
        None
    """
    print("\n" + "=" * 60)
    print("  INICIO DEL JUEGO")
    print("=" * 60)
    print("  Escribí 'salir' en cualquier momento para terminar.")
    print("=" * 60)

    while True:
        print("\n¿Qué jugador querés mover?")
        nombre = input("  Nombre: ").strip()

        if nombre.lower() == "salir":
            print("\n[FIN] Simulación terminada.")
            break

        jugador = _buscar_jugador(jugadores, nombre)
        if jugador is None:
            print(f"[ERROR] No se encontró al jugador '{nombre}'.")
            continue

        print(f"  Jugador encontrado: {jugador['nombre']} ({jugador['equipo']} - {jugador['rol']}) en ({jugador['fila']}, {jugador['columna']}).")
        print(f"  Direcciones válidas: {list(DIRECCIONES.keys())}")
        direccion = input("  Dirección: ").strip().lower()

        if direccion == "salir":
            print("\n[FIN] Simulación terminada.")
            break

        movimiento_ok = mover_jugador(cancha, jugadores, nombre, direccion)

        if movimiento_ok:
            mover_arbitro(cancha, arbitro, jugadores)
            calcular_distancias(jugadores)
            pases_posibles = detectar_pases(cancha, jugadores)
            elegir_pase(jugadores, pases_posibles)
            detectar_camino_libre_al_arco(cancha, jugadores)


# ═══════════════════════════════════════════════════════════════
# FUNCIONES AUXILIARES (privadas)
# ═══════════════════════════════════════════════════════════════

def _posicion_valida(fila, columna):
    """
    Verifica que la posición esté dentro de los límites de la cancha.

    Args:
        fila    (int): Fila a verificar.
        columna (int): Columna a verificar.

    Returns:
        bool: True si la posición es válida.
    """
    return 0 <= fila < FILAS and 0 <= columna < COLUMNAS


def _buscar_jugador(jugadores, nombre):
    """
    Busca un jugador por nombre.

    Args:
        jugadores (list[dict]): Lista de jugadores.
        nombre    (str):        Nombre a buscar.

    Returns:
        dict | None: El jugador encontrado o None.
    """
    for jugador in jugadores:
        if jugador["nombre"] == nombre:
            return jugador
    return None


def _hay_jugador_con_pelota(jugadores):
    """
    Indica si algún jugador ya posee la pelota.

    Args:
        jugadores (list[dict]): Lista de jugadores.

    Returns:
        bool: True si hay un portador.
    """
    for jugador in jugadores:
        if jugador["tiene_pelota"]:
            return True
    return False


def _obtener_portador(jugadores):
    """
    Retorna el jugador que actualmente posee la pelota.

    Args:
        jugadores (list[dict]): Lista de jugadores.

    Returns:
        dict | None: El portador o None si ninguno tiene la pelota.
    """
    for jugador in jugadores:
        if jugador["tiene_pelota"]:
            return jugador
    return None


def _distancia_manhattan(jugador_a, jugador_b):
    """
    Calcula la distancia Manhattan entre dos jugadores.

    Args:
        jugador_a (dict): Primer jugador.
        jugador_b (dict): Segundo jugador.

    Returns:
        int: Distancia Manhattan.
    """
    diferencia_filas    = abs(jugador_a["fila"]    - jugador_b["fila"])
    diferencia_columnas = abs(jugador_a["columna"] - jugador_b["columna"])
    return diferencia_filas + diferencia_columnas


def _camino_bloqueado(cancha, origen, destino):
    """
    Verifica si hay obstáculos 'X' o jugadores rivales entre dos jugadores
    alineados horizontalmente o verticalmente.
    Los jugadores del propio equipo NO bloquean el pase.
    El árbitro (marcado como 'X') sí bloquea el pase.

    Args:
        cancha  (list[list[str]]): Matriz de la cancha.
        origen  (dict):            Jugador con la pelota.
        destino (dict):            Receptor del pase.

    Returns:
        tuple[bool, str]: (True, motivo) si está bloqueado; (False, "") si libre.
    """
    equipo_rival = "B" if origen["equipo"] == "A" else "A"

    fila_o, col_o = origen["fila"], origen["columna"]
    fila_d, col_d = destino["fila"], destino["columna"]

    celdas = []
    if fila_o == fila_d:
        paso = 1 if col_d > col_o else -1
        for col in range(col_o + paso, col_d, paso):
            celdas.append(cancha[fila_o][col])
    else:
        paso = 1 if fila_d > fila_o else -1
        for fila in range(fila_o + paso, fila_d, paso):
            celdas.append(cancha[fila][col_o])

    for celda in celdas:
        if celda == OBSTACULO:
            return True, "hay un obstáculo o el árbitro en la trayectoria"
        if celda == equipo_rival:
            return True, "hay un jugador rival en la trayectoria"

    return False, ""


def agregar_obstaculo(cancha, fila, columna):
    """
    Coloca un obstáculo 'X' en la cancha en la posición indicada.

    Args:
        cancha  (list[list[str]]): Matriz de la cancha.
        fila    (int):             Fila del obstáculo.
        columna (int):             Columna del obstáculo.

    Returns:
        bool: True si el obstáculo fue colocado, False si la posición es inválida.
    """
    if not _posicion_valida(fila, columna):
        print(f"[ERROR] Posición ({fila}, {columna}) fuera de los límites.")
        return False
    if cancha[fila][columna] != CELDA_VACIA:
        print(f"[ERROR] La celda ({fila}, {columna}) ya está ocupada.")
        return False
    cancha[fila][columna] = OBSTACULO
    print(f"[OK] Obstáculo colocado en ({fila}, {columna}).")
    return True


# ═══════════════════════════════════════════════════════════════
# PROGRAMA PRINCIPAL
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":

    print("=" * 60)
    print("  COPA DE ALGORITMIA Y PROGRAMACIÓN - UADE 2026")
    print("  Desafío 3: La Cancha Inteligente")
    print("=" * 60)

    cancha    = crear_cancha()
    jugadores = []

    # ── Cargar jugadores desde archivo ──────────────────────────
    print("\n--- Cargando jugadores desde archivo ---")
    cargar_jugadores_desde_archivo(cancha, jugadores, "jugadores.txt")

    # ── Colocar árbitro ─────────────────────────────────────────
    print("\n--- Colocando árbitro ---")
    arbitro = crear_arbitro(cancha)

    # ── Colocar obstáculos ──────────────────────────────────────
    print("\n--- Colocando obstáculos ---")
    agregar_obstaculo(cancha, 5, 30)
    agregar_obstaculo(cancha, 15, 45)

    # ── Estado inicial ──────────────────────────────────────────
    print("\n--- Estado inicial ---")
    calcular_distancias(jugadores)
    detectar_pases(cancha, jugadores)
    detectar_camino_libre_al_arco(cancha, jugadores)

    # ── Menú interactivo ────────────────────────────────────────
    menu_interactivo(cancha, jugadores, arbitro)

    print("\n" + "=" * 60)
    print("  Fin de la simulación.")
    print("=" * 60)