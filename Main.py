# main.py
import tkinter as tk
from tkinter import messagebox
import math
import random
import os
import usuarios


# Importamos las clases hijas y los managers desde tus otros archivos
from defensor import *
from ataque import *

# Configuración de Paleta de Colores Cyberpunk
BG_MAIN = "#121214"       
BG_PANEL = "#1a1a1e"      
ACCENT_DEF = "#00ffcc"    # Turquesa neón
ACCENT_ATK = "#ff3e3e"    # Rojo neón
TXT_COLOR = "#ffffff"     
COLOR_BASE = "#ffd700"    



class VentanaLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Identificación de Comandantes")
        self.root.geometry("450x550")
        self.root.configure(bg="#121214")
        
        self.jugador1 = None
        self.jugador2 = None

        self.rondas_ganadas_defensor = 0
        self.rondas_ganadas_atacante = 0
        
        self.crear_widgets()

    def crear_widgets(self):
        # Título Cyberpunk
        tk.Label(self.root, text="BASE ASSAULT SYSTEM", font=("Impact", 20), fg="#00ffcc", bg="#121214").pack(pady=20)
        
        # --- SECCIÓN JUGADOR 1 (DEFENSOR) ---
        frame_j1 = tk.LabelFrame(self.root, text=" JUGADOR 1 (DEFENSOR) ", fg="#00ffcc", bg="#1a1a1e", font=("Segoe UI", 10, "bold"), padx=10, pady=10)
        frame_j1.pack(fill="x", padx=20, pady=10)
        
        tk.Label(frame_j1, text="Usuario:", fg="#ffffff", bg="#1a1a1e").grid(row=0, column=0, sticky="w", pady=2)
        self.ent_u1 = tk.Entry(frame_j1, bg="#2d2d34", fg="#ffffff", insertbackground="white", relief="flat")
        self.ent_u1.grid(row=0, column=1, padx=10, pady=2)
        
        tk.Label(frame_j1, text="Password:", fg="#ffffff", bg="#1a1a1e").grid(row=1, column=0, sticky="w", pady=2)
        self.ent_p1 = tk.Entry(frame_j1, show="*", bg="#2d2d34", fg="#ffffff", insertbackground="white", relief="flat")
        self.ent_p1.grid(row=1, column=1, padx=10, pady=2)

        # --- SECCIÓN JUGADOR 2 (ATACANTE) ---
        frame_j2 = tk.LabelFrame(self.root, text=" JUGADOR 2 (ATACANTE) ", fg="#ff3e3e", bg="#1a1a1e", font=("Segoe UI", 10, "bold"), padx=10, pady=10)
        frame_j2.pack(fill="x", padx=20, pady=10)
        
        tk.Label(frame_j2, text="Usuario:", fg="#ffffff", bg="#1a1a1e").grid(row=0, column=0, sticky="w", pady=2)
        self.ent_u2 = tk.Entry(frame_j2, bg="#2d2d34", fg="#ffffff", insertbackground="white", relief="flat")
        self.ent_u2.grid(row=0, column=1, padx=10, pady=2)
        
        tk.Label(frame_j2, text="Password:", fg="#ffffff", bg="#1a1a1e").grid(row=1, column=0, sticky="w", pady=2)
        self.ent_p2 = tk.Entry(frame_j2, show="*", bg="#2d2d34", fg="#ffffff", insertbackground="white", relief="flat")
        self.ent_p2.grid(row=1, column=1, padx=10, pady=2)

        # --- BOTONES DE CONTROL ---
        btn_login = tk.Button(self.root, text="INICIAR PARTIDA ⚔️", bg="#28a745", fg="#ffffff", font=("Segoe UI", 11, "bold"), relief="flat", width=25, command=self.procesar_login)
        btn_login.pack(pady=15)
        
        btn_registrar = tk.Button(self.root, text="REGISTRAR NUEVOS USUARIOS 📝", bg="#17a2b8", fg="#ffffff", font=("Segoe UI", 9, "bold"), relief="flat", width=30, command=self.abrir_registro)
        btn_registrar.pack(pady=5)
        
        btn_top = tk.Button(self.root, text="VER RANKING TOP 5 🏆", bg="#ffd700", fg="#000000", font=("Segoe UI", 9, "bold"), relief="flat", width=30, command=self.mostrar_rankings)
        btn_top.pack(pady=5)

    def abrir_registro(self):
        ventana_reg = tk.Toplevel(self.root)
        ventana_reg.title("Registro de Usuario")
        ventana_reg.geometry("320x250")
        ventana_reg.configure(bg="#121214")
        
        tk.Label(ventana_reg, text="NUEVO REGISTRO", font=("Impact", 14), fg="#00ffcc", bg="#121214").pack(pady=15)
        
        frame = tk.Frame(ventana_reg, bg="#1a1a1e", padx=10, pady=10)
        frame.pack(padx=10, pady=5)
        
        tk.Label(frame, text="Usuario:", fg="#ffffff", bg="#1a1a1e").grid(row=0, column=0, pady=5, sticky="w")
        ent_u = tk.Entry(frame, bg="#2d2d34", fg="#ffffff", insertbackground="white")
        ent_u.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Password:", fg="#ffffff", bg="#1a1a1e").grid(row=1, column=0, pady=5, sticky="w")
        ent_p = tk.Entry(frame, show="*", bg="#2d2d34", fg="#ffffff", insertbackground="white")
        ent_p.grid(row=1, column=1, padx=5, pady=5)
        
        def ejecutar_alta():
            exito, msg = usuarios.registrar_jugador(ent_u.get().strip(), ent_p.get().strip())
            if exito:
                messagebox.showinfo("Éxito", msg)
                ventana_reg.destroy()
            else:
                messagebox.showerror("Error", msg)

        tk.Button(ventana_reg, text="Guardar Cuenta", bg="#00ffd0", fg="#000000", font=("Segoe UI", 10, "bold"), command=ejecutar_alta).pack(pady=15)

    def procesar_login(self):
        u1, p1 = self.ent_u1.get().strip(), self.ent_p1.get().strip()
        u2, p2 = self.ent_u2.get().strip(), self.ent_p2.get().strip()
        
        if u1 == u2:
            messagebox.showerror("Error", "¡El Jugador 1 y el Jugador 2 no pueden ser el mismo usuario!")
            return
            
        v1, m1 = usuarios.verificar_login(u1, p1)
        v2, m2 = usuarios.verificar_login(u2, p2)
        
        if v1 and v2:
            self.jugador1 = u1
            self.jugador2 = u2
            messagebox.showinfo("Combate Listo", f"Bienvenidos\nDefensor: {u1}\nAtacante: {u2}")
            self.root.destroy()  # Cierra la ventana de login para dar paso al juego principal
        else:
            msg_error = ""
            if not v1: msg_error += f"Jugador 1: {m1}\n"
            if not v2: msg_error += f"Jugador 2: {m2}"
            messagebox.showerror("Error de Autenticación", msg_error)

    def mostrar_rankings(self):
        ventana_rank = tk.Toplevel(self.root)
        ventana_rank.title("Clasificación de Honor - TOP 5")
        ventana_rank.geometry("500x350")
        ventana_rank.configure(bg="#121214")
        
        tk.Label(ventana_rank, text="🏆 TOP 5 JUGADORES SUPREMOS 🏆", font=("Impact", 16), fg="#ffd700", bg="#121214").pack(pady=10)
        
        # Panel divido en dos columnas
        split_frame = tk.Frame(ventana_rank, bg="#121214")
        split_frame.pack(fill="both", expand=True, padx=10)
        
        # Columna Defensores
        f_def = tk.LabelFrame(split_frame, text=" Mejores Defensores 🛡️ ", fg="#00ffcc", bg="#1a1a1e")
        f_def.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        for idx, (user, data) in enumerate(usuarios.obtener_top_5("defensor")):
            tk.Label(f_def, text=f"{idx+1}. {user} - {data['victorias_defensor']} Victorias", fg="#ffffff", bg="#1a1a1e").pack(anchor="w", padx=5, pady=2)
            
        # Columna Atacantes
        f_atk = tk.LabelFrame(split_frame, text=" Mejores Atacantes ⚔️ ", fg="#ff3e3e", bg="#1a1a1e")
        f_atk.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        for idx, (user, data) in enumerate(usuarios.obtener_top_5("atacante")):
            tk.Label(f_atk, text=f"{idx+1}. {user} - {data['victorias_atacante']} Victorias", fg="#ffffff", bg="#1a1a1e").pack(anchor="w", padx=5, pady=2)



class JuegoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Base Assault: Cyber Evolution - 2026")
        self.root.geometry("1150x720")
        self.root.configure(bg=BG_MAIN)
        
        self.defensor_mgr = DefensorManager()
        self.atacante_mgr = AtacanteManager()
        
        # Configuración del mapa
        self.filas = 10
        self.columnas = 10
        self.celda_size = 55
        self.base_central_pos = (5, 5) 
        self.vida_base = 500           
        
        # Fases: CONSTRUCCION -> ATAQUE -> COMBATE
        self.fase_actual = "CONSTRUCCION"  
        self.clase_seleccionada = None     

        # Sistema de Facciones (Rúbrica: Mínimo 3 facciones distintas)
        self.facciones_disponibles = ["Nordica", "Magica", "Futuristica"]
        
        # Asignamos facciones diferentes obligatoriamente para cumplir la restricción
        self.faccion_defensor = "Nordica"
        self.faccion_atacante = "Futuristica"
        
        # Diccionario para evitar el Garbage Collector de Tkinter con las imágenes
        self.assets_imagenes = {}
        self.cargar_assets_imagenes()

        # Lista para manejar efectos visuales temporales (como rayos o flechas)
        self.efectos_visuales = [] 

        self.crear_interfaz()
        self.actualizar_paneles_tienda()

    def cargar_assets_imagenes(self):
        """Carga los archivos de manera exacta con fallback a minúsculas."""
        tipos_torres = ["Torre", "Mortero", "Ballesta"]
        
        # Inicializamos los contenedores
        for fac in self.facciones_disponibles:
            self.assets_imagenes[fac] = {}
            
        for fac in self.facciones_disponibles:
            for tipo in tipos_torres:
                nombre_archivo = f"{tipo} {fac}.png"
                ruta_completa = os.path.join("assets", nombre_archivo)
                
                try:
                    # Intento 1: Tal cual está formateado (Ej: "Torre Nordica.png")
                    if os.path.exists(ruta_completa):
                        self.assets_imagenes[fac][tipo] = tk.PhotoImage(file=ruta_completa)
                    else:
                        # Intento 2: Fallback todo en minúsculas (Ej: "torre nordica.png")
                        ruta_minuscula = os.path.join("assets", nombre_archivo.lower())
                        if os.path.exists(ruta_minuscula):
                            self.assets_imagenes[fac][tipo] = tk.PhotoImage(file=ruta_minuscula)
                        else:
                            print(f"⚠️ Archivo no encontrado: {ruta_completa} (ni su versión en minúsculas). Se usará figura geométrica.")
                except Exception as e:
                    print(f"❌ Error cargando {ruta_completa}: {e}")

    def actualizar_labels_oro(self):
        if self.fase_actual == "CONSTRUCCION":
            self.lbl_info_ronda.config(text=f"Fase Actual: FASE DEFENSIVA ({self.faccion_defensor.upper()}) 🛡️  |  Oro Defensor: ${self.defensor_mgr.dinero}", fg=ACCENT_DEF)
        elif self.fase_actual == "ATAQUE":
            self.lbl_info_ronda.config(text=f"Fase Actual: FASE ATACANTE ({self.faccion_atacante.upper()}) ⚔️  |  Oro Atacante: ${self.atacante_mgr.dinero}", fg=ACCENT_ATK)
        else:
            self.lbl_info_ronda.config(text=f"🔥 SIMULACIÓN EN TIEMPO REAL 🔥  |  Vida de la Base: {self.vida_base} HP", fg="#ffaa00")

    def crear_interfaz(self):
        # --- PANEL SUPERIOR ---
        self.panel_superior = tk.Frame(self.root, bg=BG_PANEL, height=90, highlightbackground="#2d2d34", highlightthickness=1)
        self.panel_superior.pack(fill="x", side="top", padx=15, pady=10)
        
        lbl_titulo = tk.Label(self.panel_superior, text="⚡ CLASH OF PYTHON: SUPREME EDITION 2026 ⚡", font=("Impact", 18), fg="#ffffff", bg=BG_PANEL)
        lbl_titulo.pack(pady=5)
        
        self.lbl_info_ronda = tk.Label(self.panel_superior, text="", font=("Segoe UI", 12, "bold"), bg=BG_PANEL)
        self.lbl_info_ronda.pack(pady=2)
        self.actualizar_labels_oro()

        # --- PANEL LATERAL ---
        self.panel_tienda = tk.Frame(self.root, bg=BG_PANEL, width=280, highlightbackground="#2d2d34", highlightthickness=1)
        self.panel_tienda.pack(fill="y", side="left", padx=15, pady=5)
        
        self.lbl_seccion = tk.Label(self.panel_tienda, text="MENU DE COMPRA", font=("Impact", 14), fg=TXT_COLOR, bg=BG_PANEL)
        self.lbl_seccion.pack(pady=15)

        self.contenedor_botones = tk.Frame(self.panel_tienda, bg=BG_PANEL)
        self.contenedor_botones.pack(fill="both", expand=True, padx=10)
        
        self.btn_fase = tk.Button(self.panel_tienda, text="FINALIZAR CONSTRUCCIÓN ➡️", bg="#28a745", fg="#ffffff", font=("Segoe UI", 11, "bold"), relief="flat", pady=10, command=self.avanzar_fase)
        self.btn_fase.pack(fill="x", side="bottom", padx=20, pady=20)

        # --- CANVAS DEL MAPA ---
        self.canvas_mapa = tk.Canvas(self.root, bg="#16161a", width=self.columnas * self.celda_size, height=self.filas * self.celda_size, highlightthickness=1, highlightbackground="#32323a")
        self.canvas_mapa.pack(expand=True, anchor="center", pady=10)
        
        self.canvas_mapa.bind("<Button-1>", self.click_en_mapa)
        self.dibujar_escenario()

    def dibujar_escenario(self):
        self.canvas_mapa.delete("all")
        
        # Cuadrícula de fondo
        for i in range(self.filas + 1):
            self.canvas_mapa.create_line(0, i * self.celda_size, self.columnas * self.celda_size, i * self.celda_size, fill="#24242b")
            self.canvas_mapa.create_line(i * self.celda_size, 0, i * self.celda_size, self.filas * self.celda_size, fill="#24242b")
        
        # Base Central
        bx, by = self.base_central_pos
        pad = 6
        cx = bx * self.celda_size + (self.celda_size // 2)
        cy = by * self.celda_size + (self.celda_size // 2)
        
        color_actual_base = COLOR_BASE if self.vida_base > 0 else "#555555"
        self.canvas_mapa.create_rectangle(bx*self.celda_size+pad, by*self.celda_size+pad, (bx+1)*self.celda_size-pad, (by+1)*self.celda_size-pad, fill=color_actual_base, outline="#b8860b", width=2)
        self.canvas_mapa.create_text(cx, cy, text=f"👑\nBASE\n{self.vida_base}HP", fill="#000000", font=("Segoe UI", 8, "bold"), justify="center")

        # 🏢 DIBUJAR DEFENSAS CON IMÁGENES REALES RECIÉN CARGADAS
        for torre in self.defensor_mgr.defensas_colocadas:
            tx = torre.x * self.celda_size + (self.celda_size // 2)
            ty = torre.y * self.celda_size + (self.celda_size // 2)
            
            fac = self.faccion_defensor
            tipo_t = getattr(torre, 'tipo_imagen', 'Torre')
            
            # Si el diccionario tiene el asset cargado en memoria, lo pinta
            if fac in self.assets_imagenes and tipo_t in self.assets_imagenes[fac]:
                self.canvas_mapa.create_image(tx, ty, image=self.assets_imagenes[fac][tipo_t])
            else:
                # Sistema de respaldo (Fallback) geométrico por si borran una imagen sin querer
                self.canvas_mapa.create_oval(tx-20, ty-20, tx+20, ty+20, fill=BG_PANEL, outline=ACCENT_DEF, width=2)
                emoji = "🏹" if isinstance(torre, TorreBasica) else "💥" if isinstance(torre, TorrePesada) else "🔮"
                self.canvas_mapa.create_text(tx, ty, text=emoji, fill="#ffffff", font=("Arial", 14))

        # 🪖 DIBUJAR ATACANTES CON COORDENADAS CONTINUAS
        for unidad in self.atacante_mgr.unidades_vivas:
            ux, uy = unidad.px, unidad.py
            
            # NOTA: Para las tropas hacés el mismo mapeo. 
            # De momento dejamos círculos neón hasta que agregues tus sprites de tropas a assets/
            self.canvas_mapa.create_oval(ux-15, uy-15, ux+15, uy+15, fill="#2a1415", outline=ACCENT_ATK, width=2)
            emoji = "🪖" if isinstance(unidad, Soldado) else "🛡️" if isinstance(unidad, Tanque) else "⚡"
            self.canvas_mapa.create_text(ux, uy-2, text=emoji, fill="#ffffff", font=("Arial", 10))
            
            # Barra de Vida dinámica debajo de cada unidad
            pct_vida = unidad.vida_actual / unidad.vida_maxima
            color_barra = "#28a745" if pct_vida > 0.5 else "#ffc107" if pct_vida > 0.2 else "#dc3545"
            self.canvas_mapa.create_rectangle(ux-18, uy+18, ux+18, uy+22, fill="#333333", outline="")
            self.canvas_mapa.create_rectangle(ux-18, uy+18, ux-18 + (36 * pct_vida), uy+22, fill=color_barra, outline="")

        # DIBUJAR EFECTOS VISUALES
        for efecto in self.efectos_visuales:
            tipo = efecto["tipo"]
            if tipo == "rayo":
                x1, y1, x2, y2 = efecto["coords"]
                self.canvas_mapa.create_line(x1, y1, (x1+x2)/2 + random.randint(-10,10), (y1+y2)/2 + random.randint(-10,10), x2, y2, fill="#00ffff", width=3, capstyle="round")
                self.canvas_mapa.create_line(x1, y1, x2, y2, fill="#ffffff", width=1)
            elif tipo == "proyectil":
                x1, y1, x2, y2 = efecto["coords"]
                self.canvas_mapa.create_line(x1, y1, x2, y2, fill=ACCENT_DEF, width=2, arrow="last")
            elif tipo == "explosion":
                x, y = efecto["coords"]
                self.canvas_mapa.create_oval(x-25, y-25, x+25, y+25, outline="#ff5500", width=2)





    def actualizar_paneles_tienda(self):
        for widget in self.contenedor_botones.winfo_children():
            widget.destroy()

        # !!! LÍNEA CLAVE: Asegurar que el botón se reactive al cambiar de fase
        self.btn_fase.config(state="normal") 

        if self.fase_actual == "CONSTRUCCION":
            self.lbl_seccion.config(text="🛡️ DEFENSAS DISPONIBLES", fg=ACCENT_DEF)
            self.btn_fase.config(text="FINALIZAR CONSTRUCCIÓN ➡️", bg="#00ffd0", fg="#000000")
            opciones = [("Torre Básica ($100)", TorreBasica), ("Torre Pesada ($250)", TorrePesada), ("Torre Mágica ($200)", TorreMagica)]
            for texto, clase in opciones:
                btn = tk.Button(self.contenedor_botones, text=texto, bg="#22222b", fg=ACCENT_DEF, font=("Segoe UI", 10, "bold"), relief="flat", pady=8, command=lambda c=clase: self.seleccionar_objeto(c))
                btn.pack(fill="x", pady=6)
        elif self.fase_actual == "ATAQUE":
            self.lbl_seccion.config(text="⚔️ RECRUTAR ATACANTES", fg=ACCENT_ATK)
            self.btn_fase.config(text="INICIAR COMBATE 🔥", bg="#dc3545", fg="#ffffff")
            opciones = [("Desplegar Soldado ($80)", Soldado), ("Desplegar Tanque ($200)", Tanque), ("Unidad Rápida ($100)", UnidadRapida)]
            for texto, clase in opciones:
                btn = tk.Button(self.contenedor_botones, text=texto, bg="#22222b", fg=ACCENT_ATK, font=("Segoe UI", 10, "bold"), relief="flat", pady=8, command=lambda c=clase: self.seleccionar_objeto(c))
                btn.pack(fill="x", pady=6)
        elif self.fase_actual == "COMBATE":
            self.lbl_seccion.config(text="⚔️ EN BATALLA...", fg="#ffaa00")
            self.btn_fase.config(text="SIMULANDO... ⏳", bg="#44444a", fg="#aaaaaa", state="disabled")




    def seleccionar_objeto(self, clase):
        self.clase_seleccionada = clase

    def click_en_mapa(self, event):
        if self.fase_actual == "COMBATE": return
        if not self.clase_seleccionada: return

        col = event.x // self.celda_size
        fil = event.y // self.celda_size
        if col >= self.columnas or fil >= self.filas or (col, fil) == self.base_central_pos: return

        if self.fase_actual == "CONSTRUCCION":
            self.defensor_mgr.comprar_estructura(self.clase_seleccionada, col, fil, self.faccion_defensor)
        elif self.fase_actual == "ATAQUE":
            nueva_un = self.atacante_mgr.desplegar_unidad(self.clase_seleccionada, col, fil, self.faccion_atacante)
            if nueva_un:
                nueva_un.px = col * self.celda_size + (self.celda_size // 2)
                nueva_un.py = fil * self.celda_size + (self.celda_size // 2)
        
        self.clase_seleccionada = None 
        self.dibujar_escenario()
        self.actualizar_labels_oro()

    def avanzar_fase(self):
        if self.fase_actual == "CONSTRUCCION":
            self.fase_actual = "ATAQUE"
            self.clase_seleccionada = None
            self.actualizar_paneles_tienda()
            self.actualizar_labels_oro()
        elif self.fase_actual == "ATAQUE":
            if not self.atacante_mgr.unidades_vivas: return
            self.fase_actual = "COMBATE"
            self.actualizar_paneles_tienda()
            self.actualizar_labels_oro()
            self.cooldown_ataque_torres = 0 
            self.ejecutar_game_loop()

    def ejecutar_game_loop(self):
        if self.fase_actual != "COMBATE": return

        bx, by = self.base_central_pos
        base_px = bx * self.celda_size + (self.celda_size // 2)
        base_py = by * self.celda_size + (self.celda_size // 2)

        self.efectos_visuales = []

        # 1. MOVIMIENTO CONTINUO
        for unidad in self.atacante_mgr.unidades_vivas:
            dx = base_px - unidad.px
            dy = base_py - unidad.py
            distancia = math.hypot(dx, dy)

            if distancia <= 35:
                self.vida_base -= (unidad.danio * 0.03)
                if self.vida_base < 0: self.vida_base = 0
            else:
                velocidad_frames = (getattr(unidad, 'velocidad', 1) * 1.8)
                unidad.px += (dx / distancia) * velocidad_frames
                unidad.py += (dy / distancia) * velocidad_frames
                unidad.x = int(unidad.px // self.celda_size)
                unidad.y = int(unidad.py // self.celda_size)

        # 2. ATAQUES CON EFECTOS ESPECIALES
        self.cooldown_ataque_torres += 1
        if self.cooldown_ataque_torres >= 15:
            self.cooldown_ataque_torres = 0  

            for torre in self.defensor_mgr.defensas_colocadas:
                tx = torre.x * self.celda_size + (self.celda_size // 2)
                ty = torre.y * self.celda_size + (self.celda_size // 2)
                
                rango_en_pixeles = torre.alcance * self.celda_size
                objetivo = None
                dist_min = rango_en_pixeles

                for unidad in self.atacante_mgr.unidades_vivas:
                    d = math.hypot(unidad.px - tx, unidad.py - ty)
                    if d <= dist_min:
                        objetivo = unidad
                        dist_min = d

                if objetivo:
                    objetivo.vida_actual -= torre.danio
                    
                    if isinstance(torre, TorreMagica):
                        self.efectos_visuales.append({"tipo": "rayo", "coords": (tx, ty, objetivo.px, objetivo.py)})
                    elif isinstance(torre, TorrePesada):
                        self.efectos_visuales.append({"tipo": "explosion", "coords": (objetivo.px, objetivo.py)})
                    else:
                        self.efectos_visuales.append({"tipo": "proyectil", "coords": (tx, ty, objetivo.px, objetivo.py)})

        # 3. FILTRADO DE BAJAS
        self.atacante_mgr.unidades_vivas = [u for u in self.atacante_mgr.unidades_vivas if u.vida_actual > 0]

        # 4. RENDER
        self.dibujar_escenario()
        self.actualizar_labels_oro()

        # 5. EVALUAR RONDAS
        if self.vida_base <= 0:
            self.rondas_ganadas_atacante += 1
            
            # Verificar si el Atacante ganó la PARTIDA completa (3 rondas)
            if self.rondas_ganadas_atacante >= 3:
                messagebox.showinfo("¡VICTORIA ABSOLUTA!", f"🔥 ¡{self.nombre_atacante} ha destruido la base 3 veces y ganó la partida completa!")
                
                # OJO: AQUÍ VA TU BLOQUE DE CÓDIGO PARA EL ATACANTE
                usuarios.registrar_victoria(self.nombre_atacante, "atacante")
                
                # Cerramos el juego o reiniciamos contadores globales
                self.root.destroy() 
                return
            else:
                messagebox.showinfo("Fin de Ronda", f"💥 El atacante ganó esta ronda.\nMarcador: Defensor {self.rondas_ganadas_defensor} - {self.rondas_ganadas_atacante} Atacante")
                self.reiniciar_partida()

        elif not self.atacante_mgr.unidades_vivas:
            self.rondas_ganadas_defensor += 1
            
            # Verificar si el Defensor ganó la PARTIDA completa (3 rondas)
            if self.rondas_ganadas_defensor >= 3:
                messagebox.showinfo("¡VICTORIA ABSOLUTA!", f"🛡️ ¡{self.nombre_defensor} defendió con éxito 3 rondas y ganó la partida completa!")
                
                # OJO: AQUÍ VA TU BLOQUE DE CÓDIGO PARA EL DEFENSOR
                usuarios.registrar_victoria(self.nombre_defensor, "defensor")
                
                # Cerramos el juego o reiniciamos contadores globales
                self.root.destroy()
                return
            else:
                messagebox.showinfo("Fin de Ronda", f"🛡️ El defensor repelió el ataque en esta ronda.\nMarcador: Defensor {self.rondas_ganadas_defensor} - {self.rondas_ganadas_atacante} Atacante")
                self.reiniciar_partida()
                
        else:
            # Si la ronda no ha terminado, el bucle sigue corriendo
            self.root.after(33, self.ejecutar_game_loop)

    def reiniciar_partida(self):
        self.vida_base = 500
        self.defensor_mgr.defensas_colocadas = []
        self.atacante_mgr.unidades_vivas = []
        self.efectos_visuales = []
        self.defensor_mgr.dinero += 400 
        self.atacante_mgr.dinero += 400
        self.fase_actual = "CONSTRUCCION"
        self.actualizar_paneles_tienda()
        self.dibujar_escenario()
        self.actualizar_labels_oro()

if __name__ == "__main__":
    # 1. Ejecutar Fase de Login primero
    root_login = tk.Tk()
    app_login = VentanaLogin(root_login)
    root_login.mainloop()
    
    # 2. Si se validaron ambos jugadores con éxito, se despliega la app del juego real
    if app_login.jugador1 and app_login.jugador2:
        root_juego = tk.Tk()
        # Puedes guardar los nombres de los jugadores dentro de la clase JuegoApp para usarlos al final
        app_juego = JuegoApp(root_juego)
        app_juego.nombre_defensor = app_login.jugador1
        app_juego.nombre_atacante = app_login.jugador2
        root_juego.mainloop()