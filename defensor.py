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
        self.habilidad_activa = False
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
    def usar_habilidad(self):
        
        if not self.habilidad_activa:
            self.habilidad_activa = True  
            self.vida_actual = self.vida_maxima  # Se sana al 100% al instante



class TorrePesada(Defensa):
    def __init__(self, x, y, faccion_visual):

        self.tipo_imagen = "Mortero"
        # Mucha vida y daño alto, pero costo elevado
        super().__init__(
            nombre="Torre Pesada", costo=250, vida=600, daño=60, alcance=3,
            habilidad="Daño en Área", turnos_habilidad=4, 
            x=x, y=y, faccion_visual=faccion_visual
        )
    
    def usar_habilidad(self):
        """Lógica de Escudo: Se cura una vez por partida."""
        if not self.habilidad_activa:
            self.habilidad_activa = True  
            self.daño *= 2.0  # Pasa de 25 a 50 de daño
        



class TorreMagica(Defensa):
    def __init__(self, x, y, faccion_visual):

        self.tipo_imagen = "Ballesta"
        # Daño bajo, pero habilidad especial fuerte
        super().__init__(
            nombre="Torre Mágica", costo=200, vida=250, daño=15, alcance=4,
            habilidad="Amplificacion", turnos_habilidad=3, 
            x=x, y=y, faccion_visual=faccion_visual
        )
    
    def usar_habilidad(self):

        if not self.habilidad_activa:
            self.habilidad_activa = True  
            self.alcance += 2  # Sube el alcance de 4 a 6 casillas, cubriendo casi todo el Canvas
            

class Muros(Defensa):
    def __init__(self, x, y, faccion_visual):
        self.tipo_imagen = "Muro" #facilita la busqueda de la imagen

        super().__init__(
            nombre= "Muro Defensivo", costo= 50, vida= 200, daño= 0, alcance= 0,
            habilidad= "Ninguna", turnos_habilidad= 0, x=x, y=y, faccion_visual= faccion_visual
        )
    def usar_habilidad(self):
        pass



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
    
    def comprar_muro(self, x, y, faccion):
        """
        compra un muro, sigue la misma lógica
        que las torres
        """
        muro_nuevo = Muros(x, y, faccion)

        if self.dinero >= muro_nuevo.costo:
            self.dinero -= muro_nuevo.costo
            self.defensas_colocadas.append(muro_nuevo)
            return muro_nuevo
        return None
    
