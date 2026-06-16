
# ataque.py

class Unidad:
    """Clase Padre para todas las unidades atacantes."""
    def __init__(self, nombre, costo, vida, danio, velocidad, habilidad, turnos_habilidad, x, y, faccion_visual):
        self.nombre = nombre
        self.costo = costo
        self.vida_maxima = vida
        self.vida_actual = vida
        self.danio = danio
        self.velocidad = velocidad  # Cantidad de movimiento por turno [cite: 102]
        self.habilidad = habilidad
        self.turnos_habilidad = turnos_habilidad
        self.contador_turnos = 0
        self.x = x
        self.y = y
        self.faccion_visual = faccion_visual

    def recibir_danio(self, cantidad):
        self.vida_actual -= cantidad
        if self.vida_actual < 0:
            self.vida_actual = 0
        return self.vida_actual == 0  # True si muere

    def mover_hacia(self, target_x, target_y):
        """Lógica base de movimiento hacia el objetivo."""
        # Se mueve tantas casillas como su velocidad lo permita
        pasos = int(self.velocidad)
        for _ in range(pasos):
            if self.x < target_x: self.x += 1
            elif self.x > target_x: self.x -= 1
            
            if self.y < target_y: self.y += 1
            elif self.y > target_y: self.y -= 1


# --- CLASES HIJAS (Tipos de Unidades) ---

class Soldado(Unidad):
    def __init__(self, x, y, faccion_visual):
        # Bajo costo y estadísticas normales básico [cite: 106]
        super().__init__(
            nombre="Soldado", costo=80, vida=150, danio=20, velocidad=1,
            habilidad="Escudo Temporal", turnos_habilidad=3,
            x=x, y=y, faccion_visual=faccion_visual
        )

    def usar_habilidad(self):
        """Lógica de Escudo[cite: 109, 113]."""
        print(f"¡{self.nombre} activa {self.habilidad}!")


class Tanque(Unidad):
    def __init__(self, x, y, faccion_visual):
        # Mucha vida, pero movimiento lento [cite: 106]
        super().__init__(
            nombre="Tanque", costo=200, vida=450, danio=40, velocidad=0.5,
            habilidad="Daño Extra contra Torres", turnos_habilidad=2,
            x=x, y=y, faccion_visual=faccion_visual
        )

    def usar_habilidad(self):
        """Lógica de Daño Extra[cite: 112, 113]."""
        print(f"¡{self.nombre} activa {self.habilidad}!")


class UnidadRapida(Unidad):
    def __init__(self, x, y, faccion_visual):
        # Poco daño, pero se mueve más rápido [cite: 106]
        super().__init__(
            nombre="Unidad Rápida", costo=100, vida=100, danio=15, velocidad=2,
            habilidad="Aumento de Velocidad", turnos_habilidad=3,
            x=x, y=y, faccion_visual=faccion_visual
        )

    def usar_habilidad(self):
        """Lógica de Furia / Velocidad[cite: 111, 113]."""
        print(f"¡{self.nombre} activa {self.habilidad}!")


# --- MANAGER DEL ATACANTE ---

class AtacanteManager:
    def __init__(self):
        self.dinero = 600  # Dinero inicial de ronda [cite: 120, 135]
        self.unidades_vivas = []

    def desplegar_unidad(self, clase_unidad, x, y, faccion):
        """Recibe la CLASE de la unidad dinámicamente (ej: Tanque)"""
        unidad_temporal = clase_unidad(x, y, faccion)
        
        if self.dinero >= unidad_temporal.costo:
            self.dinero -= unidad_temporal.costo
            self.unidades_vivas.append(unidad_temporal)
            return unidad_temporal
        return None
