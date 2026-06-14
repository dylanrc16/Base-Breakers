import tkinter as tk
from Atacante import * # Tu archivo de lógica

class JuegoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clash of Clans - Tactical Map")
        self.root.geometry("850x600")
        self.root.configure(bg="#2c3e50")

        self.manager = AtacanteManager()
        self.ultima_unidad = None 
        self.tropa_seleccionada = Soldado 
        
        self.columnas_mapa = 10
        self.filas_mapa = 10
        self.tamano_casilla = 50 

        # --- CARGAR Y REDIMENSIONAR IMÁGENES ---
        try:
            # Cargamos la imagen original gigante
            img_soldado_grande = tk.PhotoImage(file="Barbaro.png")
            img_tanque_grande = tk.PhotoImage(file="Tank.png")
            img_avion_grande = tk.PhotoImage(file="Rapida.png")
            
            # El .subsample(X, X) divide el tamaño. 
            # Si tu imagen mide 500px, subsample(10) la deja en 50px (perfecta para la casilla).
            # Ajustá el número (10, 15, 8) según qué tan grande sea tu archivo original.
            self.imagenes_tropas = {
                "Soldado": img_soldado_grande.subsample(19, 19),
                "Tanque": img_tanque_grande.subsample(16, 16),
                "Avion": img_avion_grande.subsample(16, 16)
            }
        except Exception as e:
            print("⚠️ ¡Alerta! No se encontraron los archivos PNG o falló el redimensionado.")
            self.imagenes_tropas = None

        self.crear_componentes()
        self.dibujar_cuadricula()

    def crear_componentes(self):
        # --- PANEL LATERAL DE CONTROL ---
        panel_control = tk.Frame(self.root, bg="#34495e", width=300, padx=15, pady=15)
        panel_control.pack(side=tk.RIGHT, fill=tk.Y)

        self.lbl_dinero = tk.Label(panel_control, text=f"🪙 ORO: {self.manager.dinero}", font=("Impact", 20), fg="#f1c40f", bg="#34495e")
        self.lbl_dinero.pack(pady=10)

        lbl_instrucciones = tk.Label(panel_control, text="1. Seleccioná una tropa abajo\n2. Tocá el mapa verde para desplegar", font=("Arial", 10, "italic"), fg="#ecf0f1", bg="#34495e", justify=tk.LEFT)
        lbl_instrucciones.pack(pady=10)

        frame_selector = tk.LabelFrame(panel_control, text=" CUARTEL ", font=("Arial", 11, "bold"), fg="white", bg="#34495e", padx=5, pady=10)
        frame_selector.pack(fill=tk.X, pady=15)

        self.btn_sel_soldado = tk.Button(frame_selector, text=f"⚔️ Soldado ({Soldado().costo})", font=("Arial", 10, "bold"), bg="#27ae60", fg="white", command=lambda: self.cambiar_seleccion_tropa(Soldado, self.btn_sel_soldado))
        self.btn_sel_soldado.pack(fill=tk.X, pady=4)

        self.btn_sel_tanque = tk.Button(frame_selector, text=f"🛡️ Tanque ({Tanque().costo})", font=("Arial", 10, "bold"), bg="#7f8c8d", fg="white", command=lambda: self.cambiar_seleccion_tropa(Tanque, self.btn_sel_tanque))
        self.btn_sel_tanque.pack(fill=tk.X, pady=4)

        self.btn_sel_rapida = tk.Button(frame_selector, text=f"🚀 Avión ({UnidadRapida().costo})", font=("Arial", 10, "bold"), bg="#7f8c8d", fg="white", command=lambda: self.cambiar_seleccion_tropa(UnidadRapida, self.btn_sel_rapida))
        self.btn_sel_rapida.pack(fill=tk.X, pady=4)

        frame_hechizos = tk.LabelFrame(panel_control, text=" HECHIZOS Y HABILIDADES ", font=("Arial", 11, "bold"), fg="white", bg="#34495e", padx=5, pady=10)
        frame_hechizos.pack(fill=tk.X, pady=15)

        self.btn_skill = tk.Button(frame_hechizos, text="⚡ ¡ACTIVAR SUPERPODER! ⚡", font=("Impact", 12), state=tk.DISABLED, bg="#9b59b6", fg="white", command=self.ejecutar_habilidad_tropa)
        self.btn_skill.pack(fill=tk.X, pady=5)

        self.lbl_consola = tk.Label(panel_control, text="⚔️ Prepárate para el ataque...", fg="#bdc3c7", bg="#2c3e50", font=("Courier", 10), height=6, width=28, wraplength=200, justify=tk.LEFT)
        self.lbl_consola.pack(pady=15, side=tk.BOTTOM)

        # --- CANVAS DEL MAPA ---
        self.canvas = tk.Canvas(self.root, bg="#2ecc71", width=self.columnas_mapa * self.tamano_casilla, height=self.filas_mapa * self.tamano_casilla, highlightthickness=2, highlightbackground="#27ae60")
        self.canvas.pack(side=tk.LEFT, padx=20, pady=20)
        self.canvas.bind("<Button-1>", self.hacer_clic_mapa)

    def dibujar_cuadricula(self):
        for i in range(self.columnas_mapa + 1):
            coord = i * self.tamano_casilla
            self.canvas.create_line(coord, 0, coord, self.filas_mapa * self.tamano_casilla, fill="#27ae60", width=1)
            self.canvas.create_line(0, coord, self.columnas_mapa * self.tamano_casilla, coord, fill="#27ae60", width=1)

    def cambiar_seleccion_tropa(self, tipo_clase, boton_presionado):
        self.tropa_seleccionada = tipo_clase
        self.btn_sel_soldado.config(bg="#7f8c8d")
        self.btn_sel_tanque.config(bg="#7f8c8d")
        self.btn_sel_rapida.config(bg="#7f8c8d")
        boton_presionado.config(bg="#27ae60")

    def hacer_clic_mapa(self, event):
        casilla_x = event.x // self.tamano_casilla
        casilla_y = event.y // self.tamano_casilla

        nueva_tropa = self.manager.desplegar_unidad(self.tropa_seleccionada, x=casilla_x, y=casilla_y, faccion="Atacante")
        
        if nueva_tropa:
            self.ultima_unidad = nueva_tropa
            self.lbl_dinero.config(text=f"🪙 ORO: {self.manager.dinero}")
            self.lbl_consola.config(text=f"[DESPLIEGUE]\n{nueva_tropa.nombre} entró a la batalla en ({casilla_x}, {casilla_y}).", fg="#2ecc71")
            self.btn_skill.config(state=tk.NORMAL)
            
            # Dibujamos la tropa usando la función de renders
            self.renderizar_tropa_en_mapa(nueva_tropa)
        else:
            self.lbl_consola.config(text=f"[ALERTA]\nOro insuficiente.", fg="#e74c3c")

    def renderizar_tropa_en_mapa(self, tropa):
        """Dibuja el sprite PNG de la tropa en el mapa. Si no existen, usa círculos."""
        x_pixel = tropa.x * self.tamano_casilla + (self.tamano_casilla // 2)
        y_pixel = tropa.y * self.tamano_casilla + (self.tamano_casilla // 2)
        
        # Si las imágenes cargaron bien, las estampamos en el Canvas
        if self.imagenes_tropas and tropa.nombre in self.imagenes_tropas:
            # .create_image necesita la posición central X, Y y el objeto PhotoImage
            self.canvas.create_image(x_pixel, y_pixel, image=self.imagenes_tropas[tropa.nombre])
        else:
            # Plan de respaldo (Círculos) por si borrás sin querer las imágenes
            color_tropa = "#e74c3c"
            if tropa.nombre == "Tanque": color_tropa = "#34495e"
            elif tropa.nombre == "Avion": color_tropa = "#3498db"

            radio = 15
            self.canvas.create_oval(x_pixel - radio, y_pixel - radio, x_pixel + radio, y_pixel + radio, fill=color_tropa, outline="white", width=2)
            self.canvas.create_text(x_pixel, y_pixel, text=tropa.nombre[0], fill="white", font=("Arial", 10, "bold"))

    def ejecutar_habilidad_tropa(self):
        if self.ultima_unidad:
            self.ultima_unidad.habilidad(self.root)
            self.lbl_consola.config(text=f"[HECHIZO ACTIVO]\n¡{self.ultima_unidad.nombre} usó {self.ultima_unidad.habilidad}!", fg="#9b59b6")

if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = JuegoApp(ventana_principal)
    ventana_principal.mainloop()