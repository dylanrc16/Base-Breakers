# ataque.py
import time

class Unidad:
    """Clase Padre para todas las unidades atacantes."""
    def __init__(self, nombre, costo, vida, daño, velocidad, habilidad, x, y, faccion_visual):
        self.nombre = nombre
        self.costo = costo
        self.vida_maxima = vida
        self.vida_actual = vida
        self.daño = daño
        self.velocidad = velocidad  
        self.habilidad = habilidad

        self.tiempo_habilidad = time.time()
        self.habilidad_disponible = False
        self.habilidad_activa = False
        self.x = x
        self.y = y
        self.faccion_visual = faccion_visual

    def recibir_daño(self, cantidad):
        self.vida_actual -= cantidad
        if self.vida_actual < 0:
            self.vida_actual = 0
        return self.vida_actual == 0  

    def mover_hacia(self, target_x, target_y):
        """Lógica base de movimiento hacia el objetivo."""
        pasos = int(self.velocidad)
        for _ in range(pasos):
            if self.x < target_x: self.x += 1
            elif self.x > target_x: self.x -= 1
            
            if self.y < target_y: self.y += 1
            elif self.y > target_y: self.y -= 1


# --- CLASES HIJAS (Tipos de Unidades) ---

class Soldado(Unidad):
    def __init__(self, x, y, faccion_visual):
        super().__init__(
            nombre="Soldado", costo=80, vida=150, daño=20, velocidad=1,
            habilidad="Escudo Temporal",
            x=x, y=y, faccion_visual=faccion_visual
        )

    def usar_habilidad(self):
        """Lógica de Escudo: Se cura una vez por partida."""
        if not self.habilidad_activa:
            self.habilidad_activa = True  # Bloqueada para el resto de la ronda
            curacion = self.vida_maxima * 0.50
            self.vida_actual = min(self.vida_maxima, self.vida_actual + curacion)
        


class Tanque(Unidad):
    def __init__(self, x, y, faccion_visual):
        super().__init__(
            nombre="Tanque", costo=200, vida=450, daño=40, velocidad=0.5,
            habilidad="Daño Extra contra Torres", 
            x=x, y=y, faccion_visual=faccion_visual
        )

    def usar_habilidad(self):
        """Lógica de Daño Extra: Multiplica su daño una única vez."""
        if not self.habilidad_activa:
            self.habilidad_activa = True  # Bloqueada para el resto de la ronda
            self.daño *= 2.5  
            
        

class UnidadRapida(Unidad):
    def __init__(self, x, y, faccion_visual):
        super().__init__(
            nombre="Unidad Rápida", costo=100, vida=100, daño=15, velocidad=2,
            habilidad="Aumento de Velocidad", 
            x=x, y=y, faccion_visual=faccion_visual
        )

    def usar_habilidad(self):
        """Lógica de Velocidad: Duplica su velocidad una única vez."""
        if not self.habilidad_activa:
            self.habilidad_activa = True  # Bloqueada para el resto de la ronda
            self.velocidad *= 2.0  
            
        
            
# --- MANAGER DEL ATACANTE ---

class AtacanteManager:
    def __init__(self):
        self.dinero = 600  
        self.unidades_vivas = []

    def desplegar_unidad(self, clase_unidad, x, y, faccion):
        unidad_temporal = clase_unidad(x, y, faccion)
        
        if self.dinero >= unidad_temporal.costo:
            self.dinero -= unidad_temporal.costo
            self.unidades_vivas.append(unidad_temporal)
            return unidad_temporal
        return None