"""
Copa de Algoritmia y Programación - UADE 2026
Desafío 3: "La Cancha Inteligente"
"""

# ─────────────────────────────────────────────
# Constantes globales
# ─────────────────────────────────────────────
FILAS = 100
COLUMNAS = 60
EQUIPOS_VALIDOS = ("A", "B")
ROLES_VALIDOS = ("arquero", "defensor", "mediocampista", "delantero")
CELDA_VACIA = "."
OBSTACULO = "X"


# ═══════════════════════════════════════════════════════════════
# TAREA 1: Crear la cancha
# ═══════════════════════════════════════════════════════════════

def crear_cancha():
    """
    Genera la matriz que representa la cancha de fútbol.

    Returns:
        list[list[str]]: Matriz de 100 filas × 60 columnas inicializada con ".".
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
        fila         (int):  Fila en la cancha (0-99).
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
    # Validar límites
    if not _posicion_valida(fila, columna):
        print(f"[ERROR] Posición ({fila}, {columna}) fuera de los límites de la cancha.")
        return False

    # Validar celda libre
    if cancha[fila][columna] != CELDA_VACIA:
        print(f"[ERROR] La celda ({fila}, {columna}) ya está ocupada (contiene '{cancha[fila][columna]}').")
        return False

    # Validar equipo
    if equipo not in EQUIPOS_VALIDOS:
        print(f"[ERROR] Equipo '{equipo}' inválido. Use 'A' (Argentina) o 'B' (Brasil).")
        return False

    # Validar rol
    if rol not in ROLES_VALIDOS:
        print(f"[ERROR] Rol '{rol}' inválido. Roles permitidos: {ROLES_VALIDOS}.")
        return False

    # Validar posesión única de la pelota
    if tiene_pelota and _hay_jugador_con_pelota(jugadores):
        print("[ERROR] Ya existe un jugador con la pelota. Solo un jugador puede tenerla a la vez.")
        return False

    # Registrar jugador
    nuevo = crear_jugador(nombre, equipo, fila, columna, rol, tiene_pelota)
    jugadores.append(nuevo)
    cancha[fila][columna] = equipo
    print(f"[OK] Jugador '{nombre}' ({equipo} - {rol}) agregado en ({fila}, {columna}).")
    return True


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

    # Validar límites
    if not _posicion_valida(nueva_fila, nueva_col):
        print(f"[MOVIMIENTO INVÁLIDO] '{nombre}' no puede moverse a ({nueva_fila}, {nueva_col}): fuera de la cancha.")
        return False

    # Validar celda destino libre
    celda_destino = cancha[nueva_fila][nueva_col]
    if celda_destino != CELDA_VACIA:
        if celda_destino == OBSTACULO:
            razon = "obstáculo"
        else:
            razon = f"jugador del equipo '{celda_destino}'"
        print(f"[MOVIMIENTO INVÁLIDO] '{nombre}' no puede moverse a ({nueva_fila}, {nueva_col}): celda ocupada por {razon}.")
        return False

    # Actualizar matriz y posición del jugador
    cancha[jugador["fila"]][jugador["columna"]] = CELDA_VACIA
    jugador["fila"]    = nueva_fila
    jugador["columna"] = nueva_col
    cancha[nueva_fila][nueva_col] = jugador["equipo"]

    print(f"[MOVIMIENTO OK] '{nombre}' se movió {direccion} → ({nueva_fila}, {nueva_col}).")
    return True


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
    mas_cercanos = [nombre for nombre, d in distancias if d == minima]

    if len(mas_cercanos) == 1:
        print(f"\n[MÁS CERCANO] {mas_cercanos[0]} (distancia {minima}).")
    else:
        print(f"\n[EMPATE - MÁS CERCANOS] {', '.join(mas_cercanos)} (distancia {minima} cada uno).")


# ═══════════════════════════════════════════════════════════════
# TAREA 5: Detectar posibilidad de pase
# ═══════════════════════════════════════════════════════════════

def detectar_pases(cancha, jugadores):
    """
    Lista todos los pases posibles para el jugador que posee la pelota.

    Un pase es posible si:
        - El receptor es del mismo equipo.
        - Están en la misma fila o columna (línea recta, sin diagonales).
        - No hay jugadores rivales ni obstáculos 'X' entre ellos
          (los compañeros propios NO bloquean el pase).

    Args:
        cancha    (list[list[str]]): Matriz de la cancha.
        jugadores (list[dict]):      Lista de jugadores.

    Returns:
        None
    """
    portador = _obtener_portador(jugadores)
    if portador is None:
        print("[INFO] Ningún jugador tiene la pelota actualmente.")
        return

    print(f"\n=== Pases posibles para '{portador['nombre']}' ({portador['equipo']}) ===")

    hay_pases = False
    for receptor in jugadores:
        if receptor is portador:
            continue
        if receptor["equipo"] != portador["equipo"]:
            continue
        if receptor["fila"] != portador["fila"] and receptor["columna"] != portador["columna"]:
            continue  # No están en línea recta

        bloqueado, motivo = _camino_bloqueado(cancha, portador, receptor)
        if not bloqueado:
            print(f"  [PASE POSIBLE] → {receptor['nombre']} en ({receptor['fila']}, {receptor['columna']}).")
            hay_pases = True
        else:
            print(f"  [PASE BLOQUEADO] → {receptor['nombre']}: {motivo}.")

    if not hay_pases:
        print("  No hay pases posibles disponibles.")


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
        - No existe ningún rival ni obstáculo 'X' en la misma fila
          entre el jugador y el arco rival.
          Los compañeros de equipo no bloquean el camino.

    Args:
        cancha    (list[list[str]]): Matriz de la cancha.
        jugadores (list[dict]):      Lista de jugadores.

    Returns:
        None
    """
    print("\n=== Análisis de camino libre al arco ===")
    delanteros = [j for j in jugadores if j["rol"] == "delantero"]

    if not delanteros:
        print("  No hay delanteros registrados.")
        return

    for delantero in delanteros:
        equipo  = delantero["equipo"]
        fila    = delantero["fila"]
        columna = delantero["columna"]

        # Verificar mitad ofensiva
        en_mitad_ofensiva = (
            (equipo == "A" and 30 <= columna <= 59) or
            (equipo == "B" and 0 <= columna <= 29)
        )

        if not en_mitad_ofensiva:
            print(f"  [SIN CAMINO LIBRE] '{delantero['nombre']}': no está en la mitad ofensiva (columna {columna}).")
            continue

        # Determinar rango de columnas entre el jugador y el arco rival
        if equipo == "A":
            cols_entre = range(columna + 1, 60)
            equipo_rival = "B"
        else:
            cols_entre = range(columna - 1, -1, -1)
            equipo_rival = "A"

        # Verificar si hay rivales u obstáculos en la misma fila
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
    diferencia_filas = abs(jugador_a["fila"] - jugador_b["fila"])
    diferencia_columnas = abs(jugador_a["columna"] - jugador_b["columna"])
    return diferencia_filas + diferencia_columnas


def _camino_bloqueado(cancha, origen, destino):
    """
    Verifica si hay obstáculos 'X' o jugadores rivales entre dos jugadores
    alineados horizontalmente o verticalmente.
    Los jugadores del propio equipo NO bloquean el pase.

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
            return True, "hay un obstáculo en la trayectoria"
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
# PROGRAMA PRINCIPAL – Casos de prueba
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":

    # ── Inicialización ──────────────────────────────────────────
    print("=" * 60)
    print("  COPA DE ALGORITMIA Y PROGRAMACIÓN - UADE 2026")
    print("  Desafío 3: La Cancha Inteligente")
    print("=" * 60)

    cancha    = crear_cancha()
    jugadores = []

    # ── Agregar obstáculos ──────────────────────────────────────
    print("\n--- Colocando obstáculos ---")
    agregar_obstaculo(cancha, 10, 30)
    agregar_obstaculo(cancha, 20, 45)

    # ── TAREA 2: Posicionar jugadores ───────────────────────────
    print("\n--- Registrando jugadores ---")

    posicionar_jugador(cancha, jugadores, "Messi",       "A", 10, 40, "delantero",     True)
    posicionar_jugador(cancha, jugadores, "Di Maria",    "A", 10, 35, "mediocampista", False)
    posicionar_jugador(cancha, jugadores, "MacAllister", "A", 15, 40, "mediocampista", False)
    posicionar_jugador(cancha, jugadores, "Romero",      "A",  5, 15, "defensor",      False)
    posicionar_jugador(cancha, jugadores, "Martinez",    "A", 50,  2, "arquero",       False)
    posicionar_jugador(cancha, jugadores, "Vinicius",    "B", 10, 50, "delantero",     False)
    posicionar_jugador(cancha, jugadores, "Rodrygo",     "B", 20, 10, "delantero",     False)
    posicionar_jugador(cancha, jugadores, "Paqueta",     "B", 15, 35, "mediocampista", False)

    # Casos de error
    print("\n--- Casos de error esperados ---")
    posicionar_jugador(cancha, jugadores, "Error1", "A", 10, 40, "delantero", False)  # celda ocupada
    posicionar_jugador(cancha, jugadores, "Error2", "A", -1,  0, "defensor",  False)  # fuera de límites
    posicionar_jugador(cancha, jugadores, "Error3", "C", 20, 20, "defensor",  False)  # equipo inválido
    posicionar_jugador(cancha, jugadores, "Error4", "A", 20, 20, "portero",   False)  # rol inválido
    posicionar_jugador(cancha, jugadores, "Error5", "B", 30, 30, "defensor",  True)   # ya hay portador

    # ── TAREA 3: Mover jugadores ────────────────────────────────
    print("\n--- Movimientos ---")
    mover_jugador(cancha, jugadores, "Messi",    "derecha")    # OK
    mover_jugador(cancha, jugadores, "Messi",    "arriba")     # OK
    mover_jugador(cancha, jugadores, "Martinez", "izquierda")  # OK → col 1
    mover_jugador(cancha, jugadores, "Martinez", "izquierda")  # OK → col 0
    mover_jugador(cancha, jugadores, "Martinez", "izquierda")  # Fuera de cancha → inválido

    mover_jugador(cancha, jugadores, "Di Maria", "arriba")     # fila 9, col 35: libre
    mover_jugador(cancha, jugadores, "Romero",   "abajo")      # OK

    # Movimiento hacia obstáculo (obstáculo en (10, 30), Di Maria quedó en fila 9 col 35)
    # MacAllister está en (15, 40), lo movemos hacia el obstáculo en (10, 30)
    mover_jugador(cancha, jugadores, "MacAllister", "izquierda")  # OK → col 39
    mover_jugador(cancha, jugadores, "MacAllister", "izquierda")  # OK → col 38
    mover_jugador(cancha, jugadores, "MacAllister", "izquierda")  # OK → col 37
    mover_jugador(cancha, jugadores, "MacAllister", "izquierda")  # OK → col 36
    mover_jugador(cancha, jugadores, "MacAllister", "izquierda")  # OK → col 35... espera, Di Maria está ahí
    # Usamos a Romero para moverse hacia el obstáculo en (10, 30): Romero bajó a (6, 15)
    # Agregamos un jugador cerca del obstáculo para demostrar el caso
    posicionar_jugador(cancha, jugadores, "Almada", "A", 10, 29, "mediocampista", False)
    mover_jugador(cancha, jugadores, "Almada", "derecha")  # intenta ir a (10, 30): obstáculo → inválido

    # Intento de superposición: Paqueta intenta moverse a (15, 36) donde está MacAllister
    mover_jugador(cancha, jugadores, "Paqueta", "derecha")     # colisión con MacAllister → inválido

    # ── TAREA 4: Distancia Manhattan ────────────────────────────
    calcular_distancias(jugadores)

    # ── TAREA 5: Pases posibles ─────────────────────────────────
    detectar_pases(cancha, jugadores)

    # ── TAREA 6: Camino libre al arco ───────────────────────────
    detectar_camino_libre_al_arco(cancha, jugadores)

    print("\n" + "=" * 60)
    print("  Fin de la simulación.")
    print("=" * 60)