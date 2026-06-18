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
ACCENT_HAB = "#8b5cf6"    # Morado neón para habilidades


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
            self.root.destroy()
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
        
        split_frame = tk.Frame(ventana_rank, bg="#121214")
        split_frame.pack(fill="both", expand=True, padx=10)
        
        f_def = tk.LabelFrame(split_frame, text=" Mejores Defensores 🛡️ ", fg="#00ffcc", bg="#1a1a1e")
        f_def.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        for idx, (user, data) in enumerate(usuarios.obtener_top_5("defensor")):
            tk.Label(f_def, text=f"{idx+1}. {user} - {data['victorias_defensor']} Victorias", fg="#ffffff", bg="#1a1a1e").pack(anchor="w", padx=5, pady=2)
            
        f_atk = tk.LabelFrame(split_frame, text=" Mejores Atacantes ⚔️ ", fg="#ff3e3e", bg="#1a1a1e")
        f_atk.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        for idx, (user, data) in enumerate(usuarios.obtener_top_5("atacante")):
            tk.Label(f_atk, text=f"{idx+1}. {user} - {data['victorias_atacante']} Victorias", fg="#ffffff", bg="#1a1a1e").pack(anchor="w", padx=5, pady=2)


class Ventana_facciones:
    def __init__(self, root, jugador1, jugador2, callback_inicio):
        self.root = root
        self.root.title("Selección de facciones")
        self.root.geometry("500x450")
        self.root.configure(bg="#121214")

        self.jugador1 = jugador1
        self.jugador2 = jugador2
        self.callback_inicio = callback_inicio 

        self.faccion_defensor = tk.StringVar(value="hola Gabo")
        self.faccion_atacante = tk.StringVar(value="hola Gabo")

        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self.root, text="⚔️ ELIJAN SUS FACCIONES ⚔️", font=("Impact", 18), fg="#ffd700", bg="#121214").pack(pady=15)

        frame_opciones = tk.Frame(self.root, bg="#121214")
        frame_opciones.pack(fill="both", expand=True, padx=20)
        facciones_disponibles = [
            ("Nórdica", "Nordica"),
            ("Mágica", "Magica"),
            ("Futurista", "Futuristica")
        ]
    
        frame_defensor = tk.LabelFrame(frame_opciones, text=f" 🛡️ DEFENSOR ({self.jugador1}) ", fg="#00ffcc", bg="#1a1a1e", font=("Segoe UI", 10, "bold"), padx=10, pady=10)
        frame_defensor.pack(side="left", fill="both", expand=True, padx=10)

        for texto, valor in facciones_disponibles:
            tk.Radiobutton(frame_defensor, text=texto, variable=self.faccion_defensor, value=valor,
                           bg="#1a1a1e", fg="#ffffff", selectcolor="#2d2d34", activebackground="#1a1a1e",
                           activeforeground="#ffffff", font=("Segoe UI", 9)).pack(anchor="w", pady=8)
        
        frame_atacante = tk.LabelFrame(frame_opciones, text=f" ⚔️ ATACANTE ({self.jugador2}) ", fg="#ff3e3e", bg="#1a1a1e", font=("Segoe UI", 10, "bold"), padx=10, pady=10)
        frame_atacante.pack(side="right", fill="both", expand=True, padx=10)

        for texto, valor in facciones_disponibles:
            tk.Radiobutton(frame_atacante, text=texto, variable=self.faccion_atacante, value=valor,
                           bg="#1a1a1e", fg="#ffffff", selectcolor="#2d2d34", activebackground="#1a1a1e", activeforeground="#ffffff",
                           font=("Segoe UI", 9)).pack(anchor="w", pady=8)
            
        tk.Button(self.root, text="CONFIRMAR Y ENTRAR AL CAMPO DE BATALLA ➔", bg="#00ffd0", fg="#000000",
                  font=("Segoe UI", 11, "bold"), relief="flat", padx=15, pady=8, command=self.validar_seleccion).pack(pady=25)

    def validar_seleccion(self):
        frame_atacante = self.faccion_atacante.get()
        frame_defensor = self.faccion_defensor.get()

        if not frame_atacante or not frame_defensor:
            messagebox.showerror("Campos Incompletos", "Ambos jugadores deben elegir una facción antes de continuar.")
            return
        
        if frame_defensor == frame_atacante:
            messagebox.showerror("Conflicto de Facción", "¡Grave error comandante! El atacante y el defensor no pueden utilizar la misma facción.")
            return
            
        self.root.destroy()
        self.callback_inicio(frame_defensor, frame_atacante)


class JuegoApp:
    def __init__(self, root, faccion_defensor, faccion_atacante):
        self.root = root
        self.root.title("Base Assault")
        self.root.geometry("1150x720")
        self.root.configure(bg=BG_MAIN)
        
        self.nombre_defensor = ""
        self.nombre_atacante = ""
        self.rondas_ganadas_defensor = 0
        self.rondas_ganadas_atacante = 0
        
        self.defensor_mgr = DefensorManager()
        self.atacante_mgr = AtacanteManager()
        
        self.filas = 10
        self.columnas = 10
        self.celda_size = 55
        self.base_central_pos = (5, 5) 
        self.vida_base = 500          
        
        self.fase_actual = "CONSTRUCCION"  
        self.clase_seleccionada = None     

        self.facciones_disponibles = ["Nordica", "Magica", "Futuristica"]
        
        # Guardamos correctamente las facciones inyectadas por las ventanas previas
        self.faccion_defensor = faccion_defensor
        self.faccion_atacante = faccion_atacante
        self.faccion_seleccionada = faccion_defensor  # Arranca controlando el defensor
        self.img_base_central = None

        self.assets_imagenes = {}
        # Cargamos explícitamente la facción que arranca construyendo
        self.cargar_assets_imagenes()

        self.efectos_visuales = [] 

        self.crear_interfaz()
        self.actualizar_paneles_tienda()

    def seleccionar_faccion(self, nombre_fac):
        if nombre_fac in self.facciones_disponibles:
            self.faccion_seleccionada = nombre_fac
            
            self.cargar_assets_imagenes()
        
    def cargar_assets_imagenes(self):
        """Carga los archivos de la facción actual seleccionada incluyendo muros."""
        if not self.faccion_seleccionada:
            return

        tipos_defensas = ["Torre", "Mortero", "Ballesta", "Muro"]
        faccion = self.faccion_seleccionada
        self.assets_imagenes[faccion] = {}

        for tipo in tipos_defensas:
            nombre_archivo = f"{tipo} {faccion}.png"
            ruta_completa = os.path.join("assets", "assets de defensa", nombre_archivo)
                
            try:
                if os.path.exists(ruta_completa):
                    img_original = tk.PhotoImage(file=ruta_completa)
                    
                    # === TRUCO DE REESCALADO PARA EL MURO ===
                    if tipo == "Muro":
                        # Modifica estos números si lo quieres aún más pequeño (ej: 3, 3 o 4, 4)
                        self.assets_imagenes[faccion][tipo] = img_original.subsample(2, 2)
                    else:
                        self.assets_imagenes[faccion][tipo] = img_original
                        
                    print(f"✅ Asset cargado: {ruta_completa}")
                else:
                    # Fallback minúsculas
                    nombre_minuscula = f"{tipo.lower()} {faccion.lower()}.png"
                    ruta_minuscula = os.path.join("assets", "assets de defensa", nombre_minuscula)
                    if os.path.exists(ruta_minuscula):
                        img_original = tk.PhotoImage(file=ruta_minuscula)
                        if tipo == "Muro":
                            self.assets_imagenes[faccion][tipo] = img_original.subsample(2, 2)
                        else:
                            self.assets_imagenes[faccion][tipo] = img_original
                        print(f"✅ Asset cargado (fallback): {ruta_minuscula}")
                    else:
                        print(f"⚠️ Archivo no encontrado: {ruta_completa}")
            except Exception as e:
                print(f"❌ Error cargando {ruta_completa}: {e}")

        # --- Cargar la imagen de la base central ---
        if self.img_base_central is None: 
            ruta_base = os.path.join("assets", "main", "Base.png")
            try:
                if os.path.exists(ruta_base):
                    img_grande = tk.PhotoImage(file=ruta_base)
                    self.img_base_central = img_grande.subsample(10, 10) 
                    print(f"✅ Asset de Base Central cargado y reescalado")
            except Exception as e:
                print(f"❌ Error al cargar la imagen de la base: {e}")

    def actualizar_labels_oro(self):
        if self.fase_actual == "CONSTRUCCION":
            self.lbl_info_ronda.config(text=f"Fase Actual: FASE DEFENSIVA ({self.faccion_defensor.upper()}) 🛡️  |  Oro Defensor: ${self.defensor_mgr.dinero}", fg=ACCENT_DEF)
        elif self.fase_actual == "ATAQUE":
            self.lbl_info_ronda.config(text=f"Fase Actual: FASE ATACANTE ({self.faccion_atacante.upper()}) ⚔️  |  Oro Atacante: ${self.atacante_mgr.dinero}", fg=ACCENT_ATK)
        else:
            self.lbl_info_ronda.config(text=f"🔥 SIMULACIÓN EN TIEMPO REAL 🔥  |  Facciones enfrentadas", fg="#ffaa00")

    def crear_interfaz(self):
        # --- PANEL SUPERIOR ---
        self.panel_superior = tk.Frame(self.root, bg=BG_PANEL, height=90, highlightbackground="#2d2d34", highlightthickness=1)
        self.panel_superior.pack(fill="x", side="top", padx=15, pady=10)
        
        lbl_titulo = tk.Label(self.panel_superior, text="⚡ CLASH OF PYTHON: SUPREME EDITION 2026 ⚡", font=("Impact", 18), fg="#ffffff", bg=BG_PANEL)
        lbl_titulo.pack(pady=5)
        
        self.lbl_info_ronda = tk.Label(self.panel_superior, text="", font=("Segoe UI", 12, "bold"), bg=BG_PANEL)
        self.lbl_info_ronda.pack(pady=2)

        # AGREGADO: Aquí está la etiqueta de vida de la base que faltaba en tu interfaz
        self.lbl_vida_base = tk.Label(self.panel_superior, text=f"Vida de la Base: {self.vida_base} HP", font=("Segoe UI", 11, "bold"), fg=COLOR_BASE, bg=BG_PANEL)
        self.lbl_vida_base.pack(pady=2)

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
        
        for i in range(self.filas + 1):
            self.canvas_mapa.create_line(0, i * self.celda_size, self.columnas * self.celda_size, i * self.celda_size, fill="#24242b")
            self.canvas_mapa.create_line(i * self.celda_size, 0, i * self.celda_size, self.filas * self.celda_size, fill="#24242b")
        
        # --- BASE CENTRAL ---
        bx, by = self.base_central_pos
        cx = bx * self.celda_size + (self.celda_size // 2)
        cy = by * self.celda_size + (self.celda_size // 2)
        
        # Si la imagen existe y la base sigue viva, la dibujamos
        if self.vida_base > 0:
            self.canvas_mapa.create_image(cx, cy, image=self.img_base_central)
            # Le dejamos un pequeño texto abajo o encima con la vida para que el usuario sepa cuánto le queda
            self.canvas_mapa.create_text(cx, cy + 20, text=f"{int(self.vida_base)} HP", fill="#ffffff", font=("Segoe UI", 8, "bold"))

        for torre in self.defensor_mgr.defensas_colocadas:
            tx = torre.x * self.celda_size + (self.celda_size // 2)
            ty = torre.y * self.celda_size + (self.celda_size // 2)
            
            fac = self.faccion_defensor
            tipo_t = getattr(torre, 'tipo_imagen', 'Torre')
            
            #intenta dibujar el sprite desde la carpeta assets
            if fac in self.assets_imagenes and tipo_t in self.assets_imagenes[fac]:
                self.canvas_mapa.create_image(tx, ty, image=self.assets_imagenes[fac][tipo_t])
            else:
                #si no hay imagen, busca crear el objeto 
                if tipo_t == "Muro":
                    #Si es un muro se dibuja un bloque gris
                    x_izq = torre.x * self.celda_size + 4
                    y_sup = torre.y * self.celda_size + 4
                    x_der = (torre.x + 1) * self.celda_size - 4
                    y_inf = (torre.y + 1) * self.celda_size - 4

                    self.canvas_mapa.create_rectangle(x_izq, y_sup, x_der, y_inf, fill= "#5a5a66", outline= "#8a8a98", width= 2)
                    self.canvas_mapa.create_text(tx, ty, text="🧱", fill="#ffffff", font=("Arial", 12)) 

                else:
                    self.canvas_mapa.create_oval(tx-20, ty-20, tx+20, ty+20, fill=BG_PANEL, outline=ACCENT_DEF, width=2)
                    emoji = "🏹" if isinstance(torre, TorreBasica) else "💥" if isinstance(torre, TorrePesada) else "🔮"
                    self.canvas_mapa.create_text(tx, ty, text=emoji, fill="#ffffff", font=("Arial", 14))

        for unidad in self.atacante_mgr.unidades_vivas:
            ux, uy = unidad.px, unidad.py
            self.canvas_mapa.create_oval(ux-15, uy-15, ux+15, uy+15, fill="#2a1415", outline=ACCENT_ATK, width=2)
            emoji = "🪖" if isinstance(unidad, Soldado) else "🛡️" if isinstance(unidad, Tanque) else "⚡"
            self.canvas_mapa.create_text(ux, uy-2, text=emoji, fill="#ffffff", font=("Arial", 10))
            
            pct_vida = unidad.vida_actual / unidad.vida_maxima
            color_barra = "#28a745" if pct_vida > 0.5 else "#ffc107" if pct_vida > 0.2 else "#dc3545"
            self.canvas_mapa.create_rectangle(ux-18, uy+18, ux+18, uy+22, fill="#333333", outline="")
            self.canvas_mapa.create_rectangle(ux-18, uy+18, ux-18 + (36 * pct_vida), uy+22, fill=color_barra, outline="")

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

        self.btn_fase.config(state="normal") 

        if self.fase_actual == "CONSTRUCCION":
            self.lbl_seccion.config(text="🛡️ DEFENSAS DISPONIBLES", fg=ACCENT_DEF)
            self.btn_fase.config(text="FINALIZAR CONSTRUCCIÓN ➡️", bg="#00ffd0", fg="#000000")


            opciones = [("Torre Básica ($100)", TorreBasica),
                        ("Torre Pesada ($250)", TorrePesada),
                        ("Torre Mágica ($200)", TorreMagica),
                        ("Muros ($50)", Muros)]


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
            

            # --- AGREGADO: BOTÓN DE ACTIVACIÓN DE HABILIDADES DURANTE COMBATE ---
            btn_habilidades = tk.Button(
                self.contenedor_botones, text="⚔️ HABILIDADES ATAQUE ⚔️", 
                bg=ACCENT_HAB, fg="#ffffff", font=("Segoe UI", 11, "bold"), 
                relief="flat", pady=12, command=self.activar_habilidades_atacante
            )
            btn_habilidades.pack(fill="x", pady=(20, 5))  # Separación inferior pequeña

            # --- NUEVO BOTÓN: HABILIDADES DEFENSIVAS (MISMO ESTILO) ---
            btn_habilidades_defensa = tk.Button(
                self.contenedor_botones, text="🛡️ HABILIDADES DEFENSIVAS 🛡️", 
                bg="#34495E",  # Un gris oscuro azulado para diferenciarlo del morado
                fg="#ffffff", font=("Segoe UI", 11, "bold"), 
                relief="flat", pady=12, command=self.activar_habilidades_defensor
            )
            btn_habilidades_defensa.pack(fill="x", pady=(5, 20))  # Margen para separarlo de lo que siga abajo
            

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
            # IMPORTANTE: Al pasar a la fase de ataque, cargamos los assets de esa facción en memoria
            self.seleccionar_faccion(self.faccion_atacante)
            self.actualizar_paneles_tienda()
            self.actualizar_labels_oro()
        elif self.fase_actual == "ATAQUE":
            if not self.atacante_mgr.unidades_vivas: return
            self.fase_actual = "COMBATE"
            self.actualizar_paneles_tienda()
            self.actualizar_labels_oro()
            self.cooldown_ataque_torres = 0 
            self.ejecutar_game_loop()



    # --- AGREGADO: NUEVA FUNCIÓN PARA DISPARAR LAS HABILIDADES EN EL LOOP ---
    def activar_habilidades_atacante(self):
        """Recorre las unidades en batalla y ejecuta sus comportamientos especiales."""
        if not self.atacante_mgr.unidades_vivas:
            return

        for unidad in self.atacante_mgr.unidades_vivas: #atacante_mrg variable de AtacanteManager
            unidad.usar_habilidad()


    # --- FUNCIÓN PARA EL BOTÓN DE HABILIDADES DEL DEFENSOR (IGUAL A LA OTRA) ---
    def activar_habilidades_defensor(self):
        """Recorre las torres en batalla y ejecuta sus comportamientos especiales."""
        if not self.defensor_mgr.defensas_colocadas:
            return

        for torre in self.defensor_mgr.defensas_colocadas:
            torre.usar_habilidad()
            
        


    def ejecutar_game_loop(self):
        if self.fase_actual != "COMBATE": return

        bx, by = self.base_central_pos
        base_px = bx * self.celda_size + (self.celda_size // 2)
        base_py = by * self.celda_size + (self.celda_size // 2)

        self.efectos_visuales = []

        # 1. MOVIMIENTO Y ATAQUE CONTINUO (UNIDADES VS DEFENSAS)
        for unidad in self.atacante_mgr.unidades_vivas:
            dx = base_px - unidad.px
            dy = base_py - unidad.py
            distancia = math.hypot(dx, dy)

            # --- PRIORIDAD 1: ATAQUE A LA BASE CENTRAL ---
            if distancia <= 35:
                self.vida_base -= (unidad.daño * 0.03)
                if self.vida_base < 0: self.vida_base = 0
                
            else:
                # Calcular predicción de movimiento para este frame
                velocidad_frames = (getattr(unidad, 'velocidad', 1) * 1.8)
                siguiente_px = unidad.px + (dx / distancia) * velocidad_frames
                siguiente_py = unidad.py + (dy / distancia) * velocidad_frames
                
                celda_futura_x = int(siguiente_px // self.celda_size)
                celda_futura_y = int(siguiente_py // self.celda_size)
                
                # --- PRIORIDAD 2: DETECTAR SI UN MURO BLOQUEA EL PASO EN LA CELDA ---
                muro_bloqueador = None
                for defensa in self.defensor_mgr.defensas_colocadas:
                    if defensa.x == celda_futura_x and defensa.y == celda_futura_y:
                        if "Muro" in defensa.nombre:
                            muro_bloqueador = defensa
                            break
                
                if muro_bloqueador:
                    # Frena y le da con todo al muro
                    muro_bloqueador.vida_actual -= (unidad.daño * 0.03)
                    if random.random() < 0.08:
                        mx = muro_bloqueador.x * self.celda_size + (self.celda_size // 2)
                        my = muro_bloqueador.y * self.celda_size + (self.celda_size // 2)
                        self.efectos_visuales.append({"tipo": "proyectil", "coords": (unidad.px, unidad.py, mx, my)})
                        
                else:
                    # --- PRIORIDAD 3: CONTRAATAQUE A TORRES CERCANAS ---
                    # Si no hay muro estorbando, revisamos si hay una torre al alcance de los puños/armas de la unidad
                    torre_al_alcance = None
                    dist_min_torre = 60 # Rango de ataque cuerpo a cuerpo/corto de la unidad en píxeles
                    
                    for defensa in self.defensor_mgr.defensas_colocadas:
                        if "Muro" not in defensa.nombre: # Solo nos interesa golpear estructuras de ataque
                            tx = defensa.x * self.celda_size + (self.celda_size // 2)
                            ty = defensa.y * self.celda_size + (self.celda_size // 2)
                            dist_a_torre = math.hypot(tx - unidad.px, ty - unidad.py)
                            
                            if dist_a_torre <= dist_min_torre:
                                torre_al_alcance = defensa
                                break # Encontró una torre objetivo cercana
                    
                    if torre_al_alcance:
                        # La unidad se detiene temporalmente a dañar la torre defensiva
                        torre_al_alcance.vida_actual -= (unidad.daño * 0.03)
                        
                        # Efecto visual de chispazos o golpes del atacante hacia la torre
                        if random.random() < 0.1:
                            tx = torre_al_alcance.x * self.celda_size + (self.celda_size // 2)
                            ty = torre_al_alcance.y * self.celda_size + (self.celda_size // 2)
                            self.efectos_visuales.append({
                                "tipo": "rayo" if isinstance(unidad, UnidadRapida) else "proyectil", 
                                "coords": (unidad.px, unidad.py, tx, ty)
                            })
                    else:
                        # CAMINO TOTALMENTE LIBRE: Avanza fluidamente hacia la base central
                        unidad.px = siguiente_px
                        unidad.py = siguiente_py
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
                    objetivo.vida_actual -= torre.daño
                    
                    if isinstance(torre, TorreMagica):
                        self.efectos_visuales.append({"tipo": "rayo", "coords": (tx, ty, objetivo.px, objetivo.py)})
                    elif isinstance(torre, TorrePesada):
                        self.efectos_visuales.append({"tipo": "explosion", "coords": (objetivo.px, objetivo.py)})
                    else:
                        self.efectos_visuales.append({"tipo": "proyectil", "coords": (tx, ty, objetivo.px, objetivo.py)})

        
        # 3. FILTRADO DE BAJAS
        self.atacante_mgr.unidades_vivas = [u for u in self.atacante_mgr.unidades_vivas if u.vida_actual > 0]
        
        # === Remueve los muros (o torres si llegaran a morir) con vida <= 0 ===
        self.defensor_mgr.defensas_colocadas = [d for d in self.defensor_mgr.defensas_colocadas if d.vida_actual > 0]

        # 4. RENDER
        self.dibujar_escenario()
        self.actualizar_labels_oro()
        
        self.lbl_vida_base.config(text=f"Vida de la Base: {max(0, round(self.vida_base, 1))} HP")

        # 5. EVALUAR RONDAS
        if self.vida_base <= 0.1:
            self.vida_base = 0
            self.lbl_vida_base.config(text="Vida de la Base: 0 HP")
            
            self.rondas_ganadas_atacante += 1
            
            if self.rondas_ganadas_atacante >= 3:
                messagebox.showinfo("¡VICTORIA ABSOLUTA!", f"🔥 ¡{self.nombre_atacante} ha destruido la base 3 veces y ganó la partida completa!")
                usuarios.registrar_victoria(self.nombre_atacante, "atacante")
                self.root.destroy() 
                return
            else:
                messagebox.showinfo("Fin de Ronda", f"💥 El atacante ganó esta ronda.\nMarcador: Defensor {self.rondas_ganadas_defensor} - {self.rondas_ganadas_atacante} Atacante")
                self.reiniciar_partida()

        elif not self.atacante_mgr.unidades_vivas:
            self.rondas_ganadas_defensor += 1
            
            if self.rondas_ganadas_defensor >= 3:
                messagebox.showinfo("¡VICTORIA ABSOLUTA!", f"🛡️ ¡{self.nombre_defensor} defendió con éxito 3 rondas y ganó la partida completa!")
                usuarios.registrar_victoria(self.nombre_defensor, "defensor")
                self.root.destroy()
                return
            else:
                messagebox.showinfo("Fin de Ronda", f"🛡️ El defensor repelió el ataque en esta ronda.\nMarcador: Defensor {self.rondas_ganadas_defensor} - {self.rondas_ganadas_atacante} Atacante")
                self.reiniciar_partida()
                
        else:
            self.root.after(33, self.ejecutar_game_loop)

    def reiniciar_partida(self):
        self.vida_base = 500
        self.defensor_mgr.defensas_colocadas = []
        self.atacante_mgr.unidades_vivas = []
        self.efectos_visuales = []

        #bono de dinero dependiendo de rendimiento en la ronda
        oro_base = 500 
        self.defensor_mgr.dinero = oro_base + (150 if self.vida_base > 0 else 0) #bono al defensor si defendió
        self.atacante_mgr.dinero = oro_base + (150 if self.vida_base <= 0 else 0) #bono al atacante si destruyó la base
        
        self.fase_actual = "CONSTRUCCION"

        # Volvemos a setear la facción del defensor para la nueva fase de construcción
        self.seleccionar_faccion(self.faccion_defensor)
        
        self.actualizar_paneles_tienda()
        self.dibujar_escenario()
        self.actualizar_labels_oro()
        self.lbl_vida_base.config(text=f"Vida de la Base: {self.vida_base} HP")


if __name__ == "__main__":
    # 1. Lanzar Inicio de Sesión
    root_login = tk.Tk()
    app_login = VentanaLogin(root_login)
    root_login.mainloop()
    
    # 2. Si se loguearon, pasar a la selección de facciones
    if app_login.jugador1 and app_login.jugador2:
        def levantar_juego_principal(fac_def, fac_atk):
            root_juego = tk.Tk()
            
            # Pasamos las facciones directamente por parámetros para evitar inyecciones vacías
            app_juego = JuegoApp(root_juego, fac_def, fac_atk)
            app_juego.nombre_defensor = app_login.jugador1
            app_juego.nombre_atacante = app_login.jugador2
            
            root_juego.mainloop()

        root_fac = tk.Tk()
        app_fac = Ventana_facciones(root_fac, app_login.jugador1, app_login.jugador2, levantar_juego_principal)
        root_fac.mainloop()