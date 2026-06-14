import math

class Unidad:
    def __init__(self, nombre, costo, vida, danio, velocidad, habilidad, turnos_habilidad, x=0, y=0, faccion_visual=None):
        self.nombre = nombre
        self.costo = costo
        self.vida_maxima = vida      # Requerido para el cálculo de porcentaje de la barra de vida
        self.vida_actual = vida
        self.danio = danio
        self.velocidad = velocidad
        self.habilidad_nombre = habilidad
        self.turnos_habilidad = turnos_habilidad
        self.contador_turnos = 0
        self.habilidad_activa = False
        
        # Coordenadas lógicas de la cuadrícula (Matriz)
        self.x = x
        self.y = y
        self.faccion = faccion_visual
        
        # --- FÍSICA DE PÍXELES CONTINUOS ---
        # Convertimos la casilla inicial al centro exacto en píxeles (Cada celda mide 50x50)
        self.celda_size = 50
        self.px = x * self.celda_size + (self.celda_size // 2)
        self.py = y * self.celda_size + (self.celda_size // 2)

    def recibir_danio(self, cantidad):
        """Resta vida a la unidad y retorna True si murió."""
        self.vida_actual -= cantidad
        if self.vida_actual < 0:
            self.vida_actual = 0
        return self.vida_actual == 0

    def escanear_objetivo_mas_cercano(self, lista_defensas, base_pos_celda):
        """
        IA de Clash of Clans: Escanea el mapa gigante usando Pitágoras 
        y encuentra los píxeles de la estructura viva más cercana.
        """
        # Por defecto, el objetivo final siempre es la Base Central
        base_x_pixel = base_pos_celda[0] * self.celda_size + (self.celda_size // 2)
        base_y_pixel = base_pos_celda[1] * self.celda_size + (self.celda_size // 2)
        
        objetivo_x = base_x_pixel
        objetivo_y = base_y_pixel
        
        # Calculamos la distancia inicial a la base usando math.hypot (Pitágoras: sqrt(dx^2 + dy^2))
        distancia_minima = math.hypot(base_x_pixel - self.px, base_y_pixel - self.py)
        
        # Revisamos si hay alguna torre de defensa que esté más cerca que la base
        for torre in lista_defensas:
            tx_pixel = torre.x * self.celda_size + (self.celda_size // 2)
            ty_pixel = torre.y * self.celda_size + (self.celda_size // 2)
            
            distancia_a_torre = math.hypot(tx_pixel - self.px, ty_pixel - self.py)
            
            if distancia_a_torre < distancia_minima:
                distancia_minima = distancia_a_torre
                objetivo_x = tx_pixel
                objetivo_y = ty_pixel
                
        return objetivo_x, objetivo_y

    def avanzar_hacia_pixel(self, obj_x, obj_y):
        """
        Mueve la unidad de manera fluida en píxeles flotantes hacia su objetivo actual.
        La velocidad afecta directamente el paso de movimiento.
        """
        # Calculamos el vector de dirección
        dx = obj_x - self.px
        dy = obj_y - self.py
        distancia = math.hypot(dx, dy)
        
        # Si ya llegó muy cerca del objetivo, no se mueve más
        if distancia < 5:
            return
            
        # Normalizamos el movimiento basándonos en la velocidad de la tropa
        paso_píxeles = self.velocidad * 4  # Factor de escala para que se mueva bien en el mapa gigante
        
        self.px += (dx / distancia) * paso_píxeles
        self.py += (dy / distancia) * paso_píxeles
        
        # Sincronizamos las coordenadas de la matriz por si el juego las ocupa para colisiones
        self.x = int(self.px // self.celda_size)
        self.y = int(self.py // self.celda_size)


# --- CLASES HIJAS (TROPAS DEL CUARTEL) ---

class Soldado(Unidad):
    def __init__(self, x=0, y=0, faccion_visual=None):
        super().__init__(
            nombre="Soldado", costo=100, vida=150, danio=20, velocidad=1.2,
            habilidad="Furia Espartana", turnos_habilidad=3,
            x=x, y=y, faccion_visual=faccion_visual
        )

    def habilidad(self, ventana_tk):
        if not self.habilidad_activa:
            self.habilidad_activa = True
            self.danio += 15  # Buff de daño temporal
            self.velocidad *= 1.5  # Corre más rápido
            print(f"🔥 ¡{self.nombre} activó Furia! Daño aumentado a {self.danio}")
            # Desactivar el hechizo automáticamente después de 8 segundos usando el .after de Tkinter
            ventana_tk.after(8000, self.desactivar_habilidad)

    def desactivar_habilidad(self):
        if self.habilidad_activa:
            self.habilidad_activa = False
            self.danio -= 15
            self.velocidad /= 1.5
            print(f"⏳ La habilidad de {self.nombre} ha terminado.")


class Tanque(Unidad):
    def __init__(self, x=0, y=0, faccion_visual=None):
        super().__init__(
            nombre="Tanque", costo=300, vida=450, danio=10, velocidad=0.6,
            habilidad="Escudo de Hierro", turnos_habilidad=4,
            x=x, y=y, faccion_visual=faccion_visual
        )

    def habilidad(self, ventana_tk):
        if not self.habilidad_activa:
            self.habilidad_activa = True
            print(f"🛡️ ¡{self.nombre} activó Escudo! Mitiga el 50% del daño entrante.")
            # En tu lógica de recibir daño podrías validar si esto está activo para dividir el golpe entre 2

class UnidadRapida(Unidad):
    def __init__(self, x=0, y=0, faccion_visual=None):
        # En el main se busca como "Avion" en el diccionario de imágenes/emojis
        super().__init__(
            nombre="Avion", costo=500, vida=120, danio=35, velocidad=2.5,
            habilidad="Ataque de Precisión", turnos_habilidad=2,
            x=x, y=y, faccion_visual=faccion_visual
        )

    def habilidad(self, ventana_tk):
        print(f"🚀 ¡{self.nombre} ejecuta un bombardeo aéreo instantáneo!")


# --- MÁNAGER DE ATACANTES ---

class AtacanteManager:
    def __init__(self):
        self.dinero = 1200  # Oro inicial para gastar en el mapa gigante
        self.unidades_vivas = []

    def desplegar_unidad(self, clase_unidad, x, y, faccion):
        """Valida el costo e inicializa la tropa en la matriz."""
        # Creamos una instancia fantasma rápida solo para verificar el precio real de la clase
        unidad_test = clase_unidad()
        
        if self.dinero >= unidad_test.costo:
            self.dinero -= unidad_test.costo
            # Creamos la unidad real en la posición del mapa gigante cliqueada
            nueva_unidad = clase_unidad(x=x, y=y, faccion_visual=faccion)
            self.unidades_vivas.append(nueva_unidad)
            return nueva_unidad
        else:
            return None  # No hay plata

    def actualizar_movimientos(self, lista_defensas, base_pos_celda):
        """
        Este método lo vas a llamar desde el bucle principal (Update) del juego.
        Hace que cada soldado escanee el mapa y avance un paso hacia su píxel objetivo.
        """
        for unidad in self.unidades_vivas:
            # 1. La IA calcula cuál es el blanco ideal en píxeles
            obj_x, obj_y = unidad.escanear_objetivo_mas_cercano(lista_defensas, base_pos_celda)
            # 2. La física continua desplaza la tropa hacia allá
            unidad.avanzar_hacia_pixel(obj_x, obj_y)