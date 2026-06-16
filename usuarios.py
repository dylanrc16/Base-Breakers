import json
import os

ARCHIVO_DATOS = "jugadores.json"

def cargar_jugadores():
    """Lee el archivo JSON. Si no existe, devuelve un diccionario vacío."""
    if not os.path.exists(ARCHIVO_DATOS):
        return {}
    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def guardar_jugadores(datos):
    """Guarda el diccionario de jugadores en el archivo JSON."""
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def registrar_jugador(username, password):
    """Registra un nuevo usuario si no existe."""
    jugadores = cargar_jugadores()
    if username in jugadores:
        return False, "El nombre de usuario ya existe."
    
    if not username or not password:
        return False, "Los campos no pueden estar vacíos."
        
    jugadores[username] = {
        "password": password,
        "victorias_defensor": 0,
        "victorias_atacante": 0
    }
    guardar_jugadores(jugadores)
    return True, "¡Registro exitoso!"

def verificar_login(username, password):
    """Valida las credenciales de un jugador."""
    jugadores = cargar_jugadores()
    if username == "" or password == "":
         return False, "Campos incompletos."
    if username in jugadores and jugadores[username]["password"] == password:
        return True, "Login correcto."
    return False, "Usuario o contraseña incorrectos."

def registrar_victoria(username, rol):
    """Suma una victoria en el rol correspondiente ('defensor' o 'atacante')."""
    jugadores = cargar_jugadores()
    if username in jugadores:
        if rol == "defensor":
            jugadores[username]["victorias_defensor"] += 1
        elif rol == "atacante":
            jugadores[username]["victorias_atacante"] += 1
        guardar_jugadores(jugadores)

def obtener_top_5(rol):
    """Devuelve los 5 mejores jugadores en el rol solicitado ('defensor' o 'atacante')."""
    jugadores = cargar_jugadores()
    campo = "victorias_defensor" if rol == "defensor" else "victorias_atacante"
    
    # Ordenamos de mayor a menor según las victorias del rol
    lista_ordenada = sorted(
        jugadores.items(), 
        key=lambda item: item[1][campo], 
        reverse=True
    )
    return lista_ordenada[:5]
