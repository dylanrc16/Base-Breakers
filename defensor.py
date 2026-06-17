# defensor.py

class Defensa:
    """Clase Padre para todas las estructuras defensivas."""
    def __init__(self, nombre, costo, vida, daño, alcance, habilidad, turnos_habilidad, x, y, faccion_visual):
        self.nombre = nombre
        self.costo = costo
        self.vida_maxima = vida
        self.vida_actual = vida
        self.daño = daño
        self.alcance = alcance
        self.habilidad = habilidad
        self.turnos_habilidad = turnos_habilidad
        self.contador_turnos = 0
        self.x = x
        self.y = y
        self.faccion_visual = faccion_visual

    def recibir_daño(self, cantidad):
        self.vida_actual -= cantidad
        if self.vida_actual < 0:
            self.vida_actual = 0
        return self.vida_actual == 0  # Retorna True si fue destruida

    def recargar_habilidad(self):
        self.contador_turnos += 1


# --- CLASES HIJAS (Tipos de Torres) ---

class TorreBasica(Defensa):
    def __init__(self, x, y, faccion_visual):

        self.tipo_imagen = "Torre" #arquero, mago, francotirador

        # Daño normal y costo bajo
        super().__init__(
            nombre="Torre Básica", costo=100, vida=300, daño=25, alcance=2,
            habilidad="Disparo Doble", turnos_habilidad=2, 
            
            x=x, y=y, faccion_visual=faccion_visual
        )



class TorrePesada(Defensa):
    def __init__(self, x, y, faccion_visual):

        self.tipo_imagen = "Mortero"
        # Mucha vida y daño alto, pero costo elevado
        super().__init__(
            nombre="Torre Pesada", costo=250, vida=600, daño=60, alcance=3,
            habilidad="Daño en Área", turnos_habilidad=4, 
            x=x, y=y, faccion_visual=faccion_visual
        )



class TorreMagica(Defensa):
    def __init__(self, x, y, faccion_visual):

        self.tipo_imagen = "Ballesta"
        # Daño bajo, pero habilidad especial fuerte
        super().__init__(
            nombre="Torre Mágica", costo=200, vida=250, daño=15, alcance=4,
            habilidad="Congelar", turnos_habilidad=3, 
            x=x, y=y, faccion_visual=faccion_visual
        )

   

# --- MANAGER DEL DEFENSOR ---

class DefensorManager:
    def __init__(self):
        self.dinero = 600  # Dinero inicial de ronda
        self.defensas_colocadas = []

    def comprar_estructura(self, clase_torre, x, y, faccion):
        """
        Recibe la CLASE de la torre dinámicamente (ej: TorreBasica).
        Instancia la torre temporalmente para verificar el costo.
        """
        # Instancia temporal para ver cuánto cuesta
        torre_temporal = clase_torre(x, y, faccion)
        
        if self.dinero >= torre_temporal.costo:
            self.dinero -= torre_temporal.costo
            self.defensas_colocadas.append(torre_temporal)
            return torre_temporal
        return None