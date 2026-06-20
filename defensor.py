# defensor.py
import time

#clase padre para las unidades de defensa
class Defensa:
    """Clase Padre para todas las estructuras defensivas."""
    #funcion para iniciar el resto de clases
    #e: parametros de unidades de defensa
    def __init__(self, nombre, costo, vida, daño, alcance, habilidad, x, y, faccion_visual):
        self.nombre = nombre
        self.costo = costo
        self.vida_maxima = vida
        self.vida_actual = vida
        self.daño = daño
        self.alcance = alcance
        self.habilidad = habilidad
       
        self.tiempo_habilidad = time.time()
        self.habilidad_disponible = False
        self.habilidad_activa = False
        self.x = x
        self.y = y
        self.faccion_visual = faccion_visual

    #funcion para manejar cuanto se le debe restar a la vida actual
    #e: self, cantidad de daño
    #s: True si la unidad fue destruida
    def recibir_daño(self, cantidad):
        self.vida_actual -= cantidad
        if self.vida_actual < 0:
            self.vida_actual = 0
        return self.vida_actual == 0  # Retorna True si fue destruida

    def recargar_habilidad(self):
        self.contador_turnos += 1


# --- CLASES HIJAS (Tipos de Torres) ---

#clase para la torre básica
class TorreBasica(Defensa):
    #funcion que recibe el x,y y la facción a la que pertenece el defensor
    def __init__(self, x, y, faccion_visual):

        self.tipo_imagen = "Torre" #arquero, mago, francotirador

        # Daño normal y costo bajo
        #llamo a los metodos de la clase padre:
        super().__init__(
            nombre="Torre Básica", costo=100, vida=300, daño=25, alcance=2,
            habilidad="Curación", #*
            
            x=x, y=y, faccion_visual=faccion_visual
        )
    #funcion para utilizar la habilidad de la Torre
    def usar_habilidad(self):
        
        if not self.habilidad_activa:
            self.habilidad_activa = True  
            self.vida_actual = self.vida_maxima  # Se sana al 100% al instante


#clase para la torre pesada (mortero)
class TorrePesada(Defensa):
    #recibe x,y y la facción perteneciente
    def __init__(self, x, y, faccion_visual):

        self.tipo_imagen = "Mortero"
        # Mucha vida y daño alto, costo elevado
        #llamo a los metodos de la clase padre:
        super().__init__(
            nombre="Torre Pesada", costo=250, vida=600, daño=40, alcance=3,
            habilidad=" Aumento de Daño",
            x=x, y=y, faccion_visual=faccion_visual
        )
    #funcion para activar la habilidad
    def usar_habilidad(self):
        
        if not self.habilidad_activa:
            self.habilidad_activa = True  
            self.daño *= 2.0  # Pasa de 25 a 50 de daño
        


#clase para la torre mágica (ballesta)
class TorreMagica(Defensa):
    #recibe x,y y la faccion perteneciente
    def __init__(self, x, y, faccion_visual):

        self.tipo_imagen = "Ballesta"
        # Daño bajo, pero habilidad especial fuerte
        #recibe los metodos de la clase padre
        super().__init__(
            nombre="Torre Mágica", costo=200, vida=250, daño=15, alcance=4,
            habilidad="Amplificacion", 
            x=x, y=y, faccion_visual=faccion_visual
        )
    
    #funcion para activar la habilidad de la unidad
    def usar_habilidad(self):

        if not self.habilidad_activa:
            self.habilidad_activa = True  
            self.alcance += 2  # Sube el alcance de 4 a 6 casillas, cubre casi todo el Canvas
            
#clase para los muros
class Muros(Defensa):
    #recibe x,y, y la facción
    def __init__(self, x, y, faccion_visual):
        self.tipo_imagen = "Muro" #facilita la busqueda de la imagen

        #utilizo los metodos de la clase padre para facilitar todo
        super().__init__(
            nombre= "Muro Defensivo", costo= 50, vida= 200, daño= 0, alcance= 0,
            habilidad= "Ninguna", x=x, y=y, faccion_visual= faccion_visual
        )
    
    #si no se tenia esta funcion el codigo de descontrolaba, por eso se pone vacía
    def usar_habilidad(self):
        pass



# --- MANAGER DEL DEFENSOR ---

class DefensorManager:
    def __init__(self):
        self.dinero = 600  # Dinero inicial de ronda
        self.defensas_colocadas = [] #lista de las defensas colocadas

    #funcion para "comprar" las estructuras
    #e: self, clase de la torre, x,y, facción perteneciente
    def comprar_estructura(self, clase_torre, x, y, faccion):
        """
        Recibe la CLASE de la torre dinámicamente (ej: TorreBasica)
        """
        # Instancia temporal para ver cuánto cuesta
        torre_temporal = clase_torre(x, y, faccion)
        
        if self.dinero >= torre_temporal.costo:
            self.dinero -= torre_temporal.costo #le resto al dinero el costo de la torre
            self.defensas_colocadas.append(torre_temporal) #agrego la torre a la lista
            return torre_temporal
        return None
    
    #funcion para comprar muros

    def comprar_muro(self, x, y, faccion):
        """
        compra un muro, sigue la misma lógica
        que las torres
        """
        muro_nuevo = Muros(x, y, faccion)

        #misma logica que con las torres
        
        if self.dinero >= muro_nuevo.costo:
            self.dinero -= muro_nuevo.costo
            self.defensas_colocadas.append(muro_nuevo)
            return muro_nuevo
        return None
    
