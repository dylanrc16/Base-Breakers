# Base Assault: Cyber Evolution ⚔️🛡️

Juego de estrategia para dos jugadores desarrollado en Python con Tkinter. Un jugador asume el rol de **Defensor**, construyendo torres y muros para proteger su base central, mientras el otro juega como **Atacante**, comprando y desplegando unidades para destruirla. Gana la partida quien primero consiga 3 rondas a su favor.

Proyecto desarrollado para el curso de Introducción a la Programación (Modalidad Live Learning).

---

## Integrantes

- Dylan Rodríguez
- Gabriel Campos

---

## Requisitos previos

- **Python 3.10 o superior**
- Tkinter (incluido por defecto en la mayoría de instalaciones de Python; en Linux puede requerir `sudo apt install python3-tk`)
- No se necesitan librerías externas adicionales (el proyecto no usa pygame en la versión actual ni dependencias de `pip`)

---

## Estructura del proyecto

```
Tiquicia-Wars/
├── main.py              # Archivo principal: login, selección de facciones y loop del juego
├── defensor.py           # Clases de torres, muros y el manager del defensor
├── ataque.py              # Clases de unidades atacantes y el manager del atacante
├── usuarios.py            # Registro, login y ranking de jugadores (persistencia en JSON)
├── jugadores.json          # Se genera automáticamente al registrar el primer usuario
└── assets/
    ├── main/
    │   ├── Base [Facción].png      # Imagen de la base central por facción
    │   └── Fondo_Mapa.png           # Fondo del campo de batalla
    ├── assets de defensa/
    │   ├── Torre [Facción].png
    │   ├── Mortero [Facción].png
    │   ├── Ballesta [Facción].png
    │   └── Muro [Facción].png
    └── assets de ataque/
        ├── Soldado [Facción].png
        ├── Tanque [Facción].png
        └── UnidadRapida [Facción].png
```

> ⚠️ Las imágenes deben respetar exactamente el formato de nombre `Tipo Facción.png` (ej. `Torre Nordica.png`), con la primera letra de cada palabra en mayúscula, ya que el juego las busca por ese nombre exacto al cargar assets.

---

## Cómo ejecutar el juego

1. Clonar o descargar el repositorio completo.
2. Asegurarse de que la carpeta `assets/` esté en la misma ubicación que `main.py`, con las imágenes correspondientes.
3. Abrir una terminal en la carpeta del proyecto.
4. Ejecutar:

   ```bash
   python main.py
   ```

5. Se abrirá la ventana de identificación de comandantes (login).

---

## Cómo jugar

### 1. Inicio de sesión

- Ambos jugadores deben registrarse con usuario y contraseña antes de poder jugar (botón **"REGISTRAR NUEVOS USUARIOS"**).
- Una vez registrados, cada jugador ingresa sus credenciales en su respectivo panel (Jugador 1 = Defensor, Jugador 2 = Atacante) y se presiona **"INICIAR PARTIDA"**.
- No se permite que ambos jugadores usen el mismo usuario.
- El botón **"VER RANKING TOP 5"** muestra los 5 mejores jugadores como defensor y como atacante, basados en victorias acumuladas históricas.

### 2. Selección de facciones

- Cada jugador elige una facción distinta entre **Nórdica**, **Mágica** y **Futurista**.
- El defensor y el atacante no pueden elegir la misma facción.
- La facción solo afecta el aspecto visual de torres, muros, unidades y base central.

### 3. Fase de construcción (Defensor)

- El defensor cuenta con dinero inicial para comprar:
  - **Torre Básica** ($100) — daño moderado, costo bajo.
  - **Torre Pesada** ($250) — mucha vida y daño alto, costo elevado.
  - **Torre Mágica** ($200) — daño bajo pero alcance amplio.
  - **Muro** ($50) — bloquea el paso de unidades atacantes.
- Se selecciona el tipo de estructura desde el panel lateral y se hace clic en la celda del mapa donde se desea colocar.
- No se puede construir sobre la base central.
- Al finalizar, se presiona **"FINALIZAR CONSTRUCCIÓN"**.

### 4. Fase de ataque (Atacante)

- El atacante recibe su propio dinero inicial para comprar:
  - **Soldado** ($80) — estadísticas equilibradas.
  - **Tanque** ($200) — mucha vida, movimiento lento.
  - **Unidad Rápida** ($100) — poco daño, se mueve rápido.
- Se selecciona la unidad y se hace clic en la celda del mapa donde se desea desplegar.
- Al finalizar, se presiona **"INICIAR COMBATE"** (requiere al menos una unidad desplegada).

### 5. Fase de combate

- Las unidades avanzan automáticamente hacia la base central, atacando muros o torres que encuentren en su camino.
- Las torres disparan automáticamente a las unidades dentro de su alcance.
- Durante esta fase aparecen dos botones de habilidades especiales (uso único por ronda):
  - **"HABILIDADES ATAQUE"** — activa la habilidad especial de todas las unidades vivas del atacante.
  - **"HABILIDADES DEFENSIVAS"** — activa la habilidad especial de todas las estructuras del defensor.
- La ronda termina cuando:
  - La vida de la base llega a 0 → gana el **atacante** esa ronda.
  - Todas las unidades atacantes son eliminadas → gana el **defensor** esa ronda.

### 6. Fin de ronda y partida

- Al finalizar cada ronda se reinicia el tablero (torres, muros y unidades se eliminan) y se entrega dinero base más un bono según el resultado de la ronda anterior.
- El primer jugador en ganar **3 rondas** gana la partida completa y su victoria queda registrada en el ranking.

---

## Habilidades especiales

| Estructura / Unidad | Habilidad | Efecto (uso único por ronda) |
|---|---|---|
| Torre Básica | Disparo Doble | Restaura el 100% de su vida actual |
| Torre Pesada | Daño en Área | Duplica su daño |
| Torre Mágica | Amplificación | Aumenta su alcance en 2 casillas |
| Muro | — | No tiene habilidad activa |
| Soldado | Escudo Temporal | Recupera el 50% de su vida máxima |
| Tanque | Daño Extra contra Torres | Multiplica su daño x2.5 |
| Unidad Rápida | Aumento de Velocidad | Duplica su velocidad de movimiento |

---

## Persistencia de datos

Los usuarios y su historial de victorias se guardan en `jugadores.json`, generado y actualizado automáticamente por `usuarios.py`. Este archivo se crea en la primera ejecución si no existe.

Ejemplo de estructura:

```json
{
    "usuario1": {
        "password": "1234",
        "victorias_defensor": 3,
        "victorias_atacante": 1
    }
}
```

> ⚠️ Las contraseñas se almacenan en texto plano. Este proyecto es de carácter académico y no implementa cifrado de credenciales.

---

## Notas técnicas

- El juego se ejecuta en un único bucle (`ejecutar_game_loop`) que se reprograma cada 33 ms con `root.after()`, simulando el combate en tiempo real dentro del hilo principal de Tkinter.
- Si una imagen de un asset no se encuentra, el juego recurre automáticamente a una representación gráfica de respaldo (óvalos y emojis) para que la partida no se interrumpa.

---

## Problemas conocidos / limitaciones

- No hay sonido implementado (pygame no se usa en la versión actual).
- Las contraseñas no están cifradas.
- Las habilidades especiales son de un solo uso por ronda y se deben activar manualmente con los botones correspondientes durante el combate.
