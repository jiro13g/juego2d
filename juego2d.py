import math
import random
import sys

import pygame

pygame.init()

# ---------------------------------------------------------------- Ajustes
ANCHO, ALTO = 900, 520
FPS = 60

VEL_JUGADOR = 5
GRAVEDAD = 0.65
FUERZA_SALTO = -13
VEL_CAIDA_MAX = 14
REBOTE = -9
FRAMES_COYOTE = 6
FRAMES_BUFFER = 6
FRAMES_INVULNERABLE = 90
VIDAS_MAX = 3
INICIO = (55, 400)
SUELO_Y = 465

# Colores
BLANCO = (255, 255, 255)
NEGRO = (25, 25, 30)
AMARILLO = (255, 210, 30)
AMARILLO_CLARO = (255, 245, 130)
ROJO = (220, 55, 55)
ROJO_CLARO = (255, 130, 130)
AZUL = (40, 80, 220)
NARANJA = (235, 130, 30)
MORADO = (140, 70, 200)
MARRON = (130, 80, 40)
MARRON_OSCURO = (90, 55, 30)
VERDE = (55, 160, 70)
VERDE_OSCURO = (35, 110, 50)
PIEL = (255, 205, 160)
ABISMO = (20, 28, 60)
GRIS = (90, 90, 100)
PANEL = (30, 60, 120)

# ---------------------------------------------------------------- Niveles
# suelos: (x, ancho)          -> los huecos entre ellos son precipicios
# plataformas: (x, y, ancho)
# monedas: (x, y)
# enemigos: (x_min, x_max, y_base, velocidad)
NIVELES = [
    {
        "nombre": "Pradera",
        "tiempo": 40,
        "suelos": [(0, 330), (430, 470)],
        "plataformas": [(140, 385, 150), (350, 320, 150), (570, 380, 150), (690, 270, 130)],
        "monedas": [(190, 350), (240, 350), (400, 285), (455, 285),
                    (620, 345), (735, 235), (810, 430), (500, 430)],
        "enemigos": [(120, 290, 465, 2.0), (480, 780, 465, 3.0)],
    },
    {
        "nombre": "Dos abismos",
        "tiempo": 55,
        "suelos": [(0, 240), (340, 220), (660, 240)],
        "plataformas": [(250, 390, 90), (450, 350, 110), (580, 390, 100),
                        (720, 330, 110), (570, 260, 100)],
        "monedas": [(100, 430), (180, 430), (285, 355), (400, 430), (495, 315),
                    (620, 355), (740, 430), (840, 430), (770, 295), (610, 225)],
        "enemigos": [(360, 525, 465, 2.5), (680, 865, 465, 2.5), (450, 525, 350, 1.5)],
    },
    {
        "nombre": "La torre",
        "tiempo": 65,
        "suelos": [(0, 390), (510, 390)],
        "plataformas": [(30, 395, 100), (180, 335, 100), (30, 275, 100), (180, 215, 100),
                        (395, 395, 120), (400, 300, 110), (400, 200, 110),
                        (640, 395, 100), (790, 335, 100), (640, 275, 100), (790, 215, 100)],
        "monedas": [(60, 360), (210, 300), (60, 240), (210, 180), (445, 360), (445, 265), (445, 165),
                    (670, 360), (820, 300), (670, 240), (820, 180), (150, 430), (580, 430)],
        "enemigos": [(130, 355, 465, 2.5), (540, 865, 465, 3.0), (395, 480, 395, 1.5)],
    },
    {
        "nombre": "Las islas",
        "tiempo": 70,
        "suelos": [(0, 200), (700, 200)],
        "plataformas": [(230, 410, 90), (360, 360, 90), (490, 410, 90), (620, 360, 80),
                        (300, 270, 100), (450, 220, 100), (600, 270, 100)],
        "monedas": [(265, 375), (395, 325), (525, 375), (650, 325), (335, 235),
                    (485, 185), (635, 235), (80, 430), (150, 430), (780, 430), (840, 430)],
        "enemigos": [(0, 165, 465, 3.0), (705, 865, 465, 3.5),
                     (490, 545, 410, 1.5), (450, 515, 220, 1.5)],
    },
    {
        "nombre": "El castillo",
        "tiempo": 90,
        "suelos": [(0, 150), (250, 150), (500, 150), (750, 150)],
        "plataformas": [(155, 395, 90), (405, 395, 90), (655, 395, 90),
                        (60, 300, 100), (260, 290, 110), (460, 300, 100), (660, 290, 110),
                        (800, 200, 100), (350, 200, 120), (120, 200, 100)],
        "monedas": [(190, 360), (440, 360), (690, 360), (90, 265), (295, 255),
                    (495, 265), (695, 255), (835, 165), (390, 165), (150, 165),
                    (60, 430), (300, 430), (550, 430), (800, 430)],
        "enemigos": [(250, 365, 465, 3.0), (500, 615, 465, 3.0), (750, 865, 465, 3.5),
                     (350, 435, 200, 2.0), (660, 735, 290, 1.5)],
    },
]

OPCIONES_JUGADORES = [
    ("Un jugador", "Recoge todas las monedas tú solo"),
    ("Dos jugadores", "J1: A / D / W     J2: flechas"),
    ("Jugador vs Computadora", "Compite contra la CPU por las monedas"),
]
OPCIONES_MODO = [
    ("Clásico", "3 vidas y sin límite de tiempo"),
    ("Contrarreloj", "Tiempo límite por nivel y bonus por rapidez"),
]


def crear_fondo():
    """Degradado de cielo, se dibuja una sola vez."""
    fondo = pygame.Surface((ANCHO, ALTO))
    arriba, abajo = (70, 160, 255), (175, 225, 255)
    for y in range(ALTO):
        t = y / ALTO
        color = tuple(int(a + (b - a) * t) for a, b in zip(arriba, abajo))
        pygame.draw.line(fondo, color, (0, y), (ANCHO, y))
    return fondo


# ---------------------------------------------------------------- Jugador
class Jugador:
    def __init__(self, nombre, color, controles=None, bot=False):
        self.nombre = nombre
        self.color = color
        self.controles = controles
        self.bot = bot
        self.rect = pygame.Rect(0, 0, 34, 45)

        self.puntos = 0
        self.vidas = VIDAS_MAX
        self.activo = True

        # Estado de la IA
        self.objetivo = None
        self.meta = None
        self.ia_timer = 0
        self.ia_dist = 9999

        self.inicio = INICIO
        self.reiniciar_posicion(*INICIO)

    def reiniciar_posicion(self, x=None, y=None):
        if x is not None:
            self.inicio = (x, y)
        self.x, self.y = float(self.inicio[0]), float(self.inicio[1])
        self.vx = 0.0
        self.vy = 0.0
        self.en_suelo = False
        self.coyote = 0
        self.buffer = 0
        self.salto_prev = False
        self.mirando = 1
        self.invulnerable = 0
        self.prev_bottom = self.inicio[1] + self.rect.height
        self._sincronizar()

    def _sincronizar(self):
        self.rect.topleft = (round(self.x), round(self.y))

    # ---- Entrada humana
    def leer_teclas(self, teclas):
        c = self.controles
        izq = any(teclas[k] for k in c["izq"])
        der = any(teclas[k] for k in c["der"])
        salto = any(teclas[k] for k in c["salto"])
        return int(der) - int(izq), salto

    # ---- IA sencilla para el modo contra la computadora
    def hay_peligro(self, direccion, superficies):
        """True si delante no hay suelo (precipicio)."""
        r = self.rect
        px = r.centerx + direccion * (r.width // 2 + 22)
        for s in superficies:
            if s.left <= px <= s.right and s.top >= r.bottom - 4:
                return False
        return True

    def decidir_ia(self, monedas, enemigos, superficies):
        r = self.rect
        if not monedas:
            return 0, False

        if self.objetivo is None or self.objetivo not in monedas:
            self.objetivo = min(
                monedas,
                key=lambda m: abs(m.centerx - r.centerx) + 2 * abs(m.centery - r.centery),
            )
            self.ia_dist, self.ia_timer = 9999, 0
            self.meta = None
        obj = self.objetivo

        # La meta se decide en el suelo y se mantiene mientras está en el aire
        if self.en_suelo or self.meta is None:
            meta_x, meta_y = obj.centerx, obj.centery
            # Si la moneda está muy alta, usa una plataforma intermedia
            if meta_y < r.bottom - 125:
                mejor, mejor_valor = None, None
                for s in superficies:
                    subida = r.bottom - s.top
                    hueco = max(0, s.left - r.right, r.left - s.right)
                    if subida < 20 or subida > 110 or hueco > 110:
                        continue
                    valor = abs(s.centerx - obj.centerx) + 2 * abs(s.top - obj.centery)
                    if mejor_valor is None or valor < mejor_valor:
                        mejor, mejor_valor = s, valor
                if mejor is not None:
                    meta_x, meta_y = mejor.centerx, mejor.top - 30
            self.meta = (meta_x, meta_y)
        meta_x, meta_y = self.meta

        dx = meta_x - r.centerx
        dy = meta_y - r.centery
        direccion = 0 if abs(dx) < 8 else (1 if dx > 0 else -1)

        # Si no avanza hacia la moneda, prueba con otra
        self.ia_timer += 1
        if self.ia_timer >= 90:
            distancia = abs(obj.centerx - r.centerx) + abs(obj.centery - r.centery)
            if distancia > self.ia_dist - 20:
                self.objetivo = random.choice(monedas)
                distancia = 9999
            self.ia_dist, self.ia_timer = distancia, 0

        salto = False
        if self.en_suelo:
            if direccion and self.hay_peligro(direccion, superficies):
                salto = True
            for e in enemigos:
                if e.vivo and abs(e.rect.centery - r.centery) < 40:
                    dist = (e.rect.centerx - r.centerx) * (direccion or 1)
                    if 0 < dist < 90:
                        salto = True
            if dy < -25 and abs(dx) < 140:
                salto = True
        elif self.vy < 0:
            salto = True  # mantener pulsado mientras sube
        return direccion, salto

    # ---- Física
    def actualizar(self, direccion, salto_pulsado, superficies):
        objetivo = direccion * VEL_JUGADOR
        self.vx += (objetivo - self.vx) * (0.3 if direccion else 0.2)
        if direccion == 0 and abs(self.vx) < 0.1:
            self.vx = 0
        if direccion:
            self.mirando = direccion

        self.x += self.vx
        self.x = max(0, min(self.x, ANCHO - self.rect.width))

        # Salto con coyote time y buffer
        if salto_pulsado and not self.salto_prev:
            self.buffer = FRAMES_BUFFER
        self.salto_prev = salto_pulsado

        self.coyote = FRAMES_COYOTE if self.en_suelo else max(0, self.coyote - 1)
        self.buffer = max(0, self.buffer - 1)

        if self.buffer > 0 and self.coyote > 0:
            self.vy = FUERZA_SALTO
            self.buffer = 0
            self.coyote = 0

        # Salto variable
        if self.vy < -4 and not salto_pulsado:
            self.vy *= 0.85

        # Gravedad y colisión con plataformas de un solo sentido
        self.prev_bottom = self.rect.bottom
        self.vy = min(self.vy + GRAVEDAD, VEL_CAIDA_MAX)
        self.y += self.vy
        self._sincronizar()

        self.en_suelo = False
        if self.vy >= 0:
            for s in superficies:
                if self.rect.colliderect(s) and self.prev_bottom <= s.top:
                    self.y = s.top - self.rect.height
                    self.vy = 0
                    self.en_suelo = True
                    self._sincronizar()
                    break

        if self.invulnerable > 0:
            self.invulnerable -= 1

    def dibujar(self, sup, frames, fuente_etiqueta=None):
        if self.invulnerable > 0 and (self.invulnerable // 4) % 2 == 0:
            return

        r = self.rect
        caminando = self.en_suelo and abs(self.vx) > 1
        desplazamiento = 3 if caminando and (frames // 6) % 2 else 0

        pygame.draw.rect(sup, MARRON_OSCURO, (r.x + 3 + desplazamiento, r.bottom - 7, 12, 7), border_radius=3)
        pygame.draw.rect(sup, MARRON_OSCURO, (r.right - 15 - desplazamiento, r.bottom - 7, 12, 7), border_radius=3)
        pygame.draw.rect(sup, self.color, (r.x, r.y, r.width, r.height - 5), border_radius=7)
        pygame.draw.circle(sup, PIEL, (r.centerx, r.y + 7), 12)
        pygame.draw.circle(sup, NEGRO, (r.centerx + 4 * self.mirando, r.y + 5), 2)

        if fuente_etiqueta is not None:
            etiqueta = fuente_etiqueta.render(self.nombre, True, self.color)
            sup.blit(etiqueta, etiqueta.get_rect(center=(r.centerx, r.y - 14)))


# ---------------------------------------------------------------- Enemigo
class Enemigo:
    def __init__(self, x_min, x_max, y_base, velocidad):
        self.x_min, self.x_max = x_min, x_max
        self.velocidad = velocidad
        self.rect = pygame.Rect(x_min, y_base - 35, 35, 35)
        self.reaparecer()

    def reaparecer(self):
        self.x = float(self.x_min)
        self.direccion = 1
        self.vivo = True
        self.espera = 0
        self.rect.x = self.x_min

    def derrotar(self):
        self.vivo = False
        self.espera = 300  # reaparece a los 5 segundos

    def actualizar(self):
        if not self.vivo:
            self.espera -= 1
            if self.espera <= 0:
                self.reaparecer()
            return

        self.x += self.velocidad * self.direccion
        if self.x <= self.x_min:
            self.x, self.direccion = self.x_min, 1
        elif self.x >= self.x_max:
            self.x, self.direccion = self.x_max, -1
        self.rect.x = round(self.x)

    def dibujar(self, sup):
        if not self.vivo:
            return
        r = self.rect
        pygame.draw.rect(sup, ROJO, r, border_radius=8)
        for ox in (10, 25):
            pygame.draw.circle(sup, BLANCO, (r.x + ox, r.y + 14), 5)
            pygame.draw.circle(sup, NEGRO, (r.x + ox + 2 * self.direccion, r.y + 14), 2)
        pygame.draw.line(sup, NEGRO, (r.x + 4, r.y + 6), (r.x + 14, r.y + 10), 3)
        pygame.draw.line(sup, NEGRO, (r.x + 31, r.y + 6), (r.x + 21, r.y + 10), 3)


# ---------------------------------------------------------------- Juego
class Juego:
    def __init__(self):
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("La aventura de las monedas")
        self.reloj = pygame.time.Clock()

        self.fuente = pygame.font.SysFont("Arial", 25, bold=True)
        self.fuente_media = pygame.font.SysFont("Arial", 21, bold=True)
        self.fuente_pequena = pygame.font.SysFont("Arial", 17)
        self.fuente_etiqueta = pygame.font.SysFont("Arial", 15, bold=True)
        self.fuente_grande = pygame.font.SysFont("Arial", 48, bold=True)

        self.fondo = crear_fondo()
        self.capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        self.capa.fill((0, 0, 0, 175))

        self.nubes = [[140, 75, 1.0, 0.15], [680, 105, 1.2, 0.10], [420, 45, 0.8, 0.20]]
        self.mejores = {}

        self.modo_jug = 0      # 0 = solo, 1 = dos jugadores, 2 = vs CPU
        self.modo_juego = 0    # 0 = clásico, 1 = contrarreloj
        self.seleccion = 0
        self.estado = "menu_jugadores"

        self.jugadores = []
        self.nivel = 0
        self.particulas = []
        self.frames = 0
        self.bloqueo = 0
        self.bonus = 0
        self.motivo = ""
        self.suelos, self.plataformas, self.superficies = [], [], []
        self.monedas, self.enemigos = [], []
        self.total_monedas = 0

    # ------------------------------------------------------------ Partida
    def crear_jugadores(self):
        j1 = {"izq": (pygame.K_a, pygame.K_LEFT), "der": (pygame.K_d, pygame.K_RIGHT),
              "salto": (pygame.K_w, pygame.K_UP, pygame.K_SPACE)}
        if self.modo_jug == 0:
            return [Jugador("J1", AZUL, j1)]
        if self.modo_jug == 1:
            c1 = {"izq": (pygame.K_a,), "der": (pygame.K_d,),
                  "salto": (pygame.K_w, pygame.K_SPACE)}
            c2 = {"izq": (pygame.K_LEFT,), "der": (pygame.K_RIGHT,),
                  "salto": (pygame.K_UP,)}
            return [Jugador("J1", AZUL, c1), Jugador("J2", NARANJA, c2)]
        return [Jugador("J1", AZUL, j1), Jugador("CPU", MORADO, bot=True)]

    def nueva_partida(self):
        self.jugadores = self.crear_jugadores()
        self.nivel = 0
        self.bonus = 0
        self.motivo = ""
        self.cargar_nivel(0)
        self.estado = "jugando"

    def cargar_nivel(self, indice):
        datos = NIVELES[indice]
        self.nivel = indice
        self.suelos = [pygame.Rect(x, SUELO_Y, w, ALTO - SUELO_Y) for x, w in datos["suelos"]]
        self.plataformas = [pygame.Rect(x, y, w, 20) for x, y, w in datos["plataformas"]]
        self.superficies = self.suelos + self.plataformas
        self.monedas = [pygame.Rect(x, y, 22, 22) for x, y in datos["monedas"]]
        self.total_monedas = len(self.monedas)
        self.enemigos = [Enemigo(*e) for e in datos["enemigos"]]
        self.particulas = []
        self.frames = 0

        for k, j in enumerate(self.jugadores):
            if j.activo:
                j.reiniciar_posicion(INICIO[0] + 45 * k, INICIO[1])
                j.invulnerable = FRAMES_INVULNERABLE
                j.objetivo = None
                j.meta = None

    def siguiente_nivel(self):
        self.cargar_nivel(self.nivel + 1)
        self.estado = "jugando"

    @property
    def limite_frames(self):
        return NIVELES[self.nivel]["tiempo"] * FPS

    def terminar(self, estado, motivo=""):
        self.estado = estado
        self.motivo = motivo
        humanos = [j.puntos for j in self.jugadores if not j.bot]
        clave = (self.modo_jug, self.modo_juego)
        self.mejores[clave] = max(self.mejores.get(clave, 0), max(humanos, default=0))

    def completar_nivel(self):
        self.bonus = 0
        if self.modo_juego == 1:
            self.bonus = max(0, (self.limite_frames - self.frames) // FPS)
        for j in self.jugadores:
            if j.activo:
                j.puntos += self.bonus
                j.vidas = min(VIDAS_MAX, j.vidas + 1)

        if self.nivel == len(NIVELES) - 1:
            self.terminar("ganaste")
        else:
            self.estado = "nivel_completo"
            self.bloqueo = 60

    # ------------------------------------------------------------ Lógica
    def crear_particulas(self, x, y, color, cantidad=10):
        for _ in range(cantidad):
            angulo = random.uniform(0, 2 * math.pi)
            vel = random.uniform(1, 4)
            self.particulas.append(
                [x, y, math.cos(angulo) * vel, math.sin(angulo) * vel - 1,
                 random.randint(20, 35), color]
            )

    def actualizar_particulas(self):
        for p in self.particulas:
            p[0] += p[2]
            p[1] += p[3]
            p[3] += 0.15
            p[4] -= 1
        self.particulas = [p for p in self.particulas if p[4] > 0]

    def mover_nubes(self):
        for nube in self.nubes:
            nube[0] += nube[3]
            if nube[0] > ANCHO + 80:
                nube[0] = -100

    def perder_vida(self, j):
        j.vidas -= 1
        if j.vidas <= 0:
            j.activo = False
            self.crear_particulas(j.rect.centerx, j.rect.centery, j.color, 16)
            return False
        return True

    def actualizar(self):
        self.mover_nubes()
        self.actualizar_particulas()

        if self.estado == "nivel_completo":
            self.bloqueo = max(0, self.bloqueo - 1)
        if self.estado != "jugando":
            return

        self.frames += 1
        teclas = pygame.key.get_pressed()

        for enemigo in self.enemigos:
            enemigo.actualizar()

        for j in self.jugadores:
            if not j.activo:
                continue

            if j.bot:
                direccion, salto = j.decidir_ia(self.monedas, self.enemigos, self.superficies)
            else:
                direccion, salto = j.leer_teclas(teclas)
            j.actualizar(direccion, salto, self.superficies)

            # Monedas
            for moneda in self.monedas[:]:
                if j.rect.colliderect(moneda):
                    self.monedas.remove(moneda)
                    j.puntos += 10
                    self.crear_particulas(moneda.centerx, moneda.centery, AMARILLO)

            # Enemigos: se aplastan saltando encima
            for enemigo in self.enemigos:
                if not enemigo.vivo or not j.rect.colliderect(enemigo.rect):
                    continue
                if j.vy > 0 and j.prev_bottom <= enemigo.rect.top + 10:
                    enemigo.derrotar()
                    j.puntos += 50
                    j.vy = REBOTE
                    self.crear_particulas(enemigo.rect.centerx, enemigo.rect.centery, ROJO, 14)
                elif j.invulnerable == 0:
                    if self.perder_vida(j):
                        j.invulnerable = FRAMES_INVULNERABLE
                        j.vy = -8
                        j.vx = 7 if j.rect.centerx >= enemigo.rect.centerx else -7
                    break

            # Precipicio
            if j.activo and j.rect.top > ALTO:
                if self.perder_vida(j):
                    j.reiniciar_posicion()
                    j.invulnerable = FRAMES_INVULNERABLE

        # Condiciones de fin
        if not any(j.activo for j in self.jugadores):
            self.terminar("perdiste", "FIN DEL JUEGO")
        elif self.modo_juego == 1 and self.frames >= self.limite_frames:
            self.terminar("perdiste", "¡SE ACABÓ EL TIEMPO!")
        elif not self.monedas:
            self.completar_nivel()

    # ------------------------------------------------------------ Dibujo
    def texto(self, txt, fuente, color, pos, centrado=False):
        img = fuente.render(txt, True, color)
        sombra = fuente.render(txt, True, NEGRO)
        rect = img.get_rect(center=pos) if centrado else img.get_rect(topleft=pos)
        self.pantalla.blit(sombra, rect.move(2, 2))
        self.pantalla.blit(img, rect)

    def dibujar_corazon(self, x, y, color, e=1.0):
        s = self.pantalla
        radio, off = int(6 * e), int(5 * e)
        pygame.draw.circle(s, color, (x - off, y), radio)
        pygame.draw.circle(s, color, (x + off, y), radio)
        pygame.draw.polygon(s, color, [(x - int(11 * e), y + int(2 * e)),
                                       (x + int(11 * e), y + int(2 * e)),
                                       (x, y + int(16 * e))])

    def dibujar_nube(self, x, y, escala):
        for dx, dy, radio in ((0, 0, 22), (25, -5, 28), (50, 3, 20)):
            pygame.draw.circle(self.pantalla, BLANCO,
                               (int(x + dx * escala), int(y + dy * escala)), int(radio * escala))

    def dibujar_moneda(self, moneda, indice):
        t = self.frames if self.estado != "menu" else 0
        flotar = math.sin(t * 0.08 + indice) * 3
        ancho = 3 + 9 * abs(math.cos(t * 0.06 + indice))
        cx, cy = moneda.centerx, moneda.centery + flotar
        pygame.draw.ellipse(self.pantalla, AMARILLO, (cx - ancho, cy - 12, ancho * 2, 24))
        pygame.draw.ellipse(self.pantalla, AMARILLO_CLARO,
                            (cx - ancho * 0.55, cy - 7, ancho * 1.1, 14))

    def dibujar_mundo(self):
        s = self.pantalla
        s.blit(self.fondo, (0, 0))
        for nube in self.nubes:
            self.dibujar_nube(*nube[:3])

        # Precipicios (todo lo que no es suelo)
        pygame.draw.rect(s, ABISMO, (0, SUELO_Y, ANCHO, ALTO - SUELO_Y))
        for suelo in self.suelos:
            pygame.draw.rect(s, MARRON, suelo)
            pygame.draw.rect(s, VERDE, (suelo.x, suelo.y, suelo.width, 14))
            pygame.draw.rect(s, VERDE_OSCURO, (suelo.x, suelo.y + 10, suelo.width, 4))

        for p in self.plataformas:
            pygame.draw.rect(s, MARRON, p)
            pygame.draw.rect(s, VERDE, (p.x, p.y, p.width, 6))

        for i, moneda in enumerate(self.monedas):
            self.dibujar_moneda(moneda, i)
        for enemigo in self.enemigos:
            enemigo.dibujar(s)

        etiqueta = self.fuente_etiqueta if len(self.jugadores) > 1 else None
        for j in self.jugadores:
            if j.activo:
                j.dibujar(s, self.frames, etiqueta)

        for x, y, _, _, vida, color in self.particulas:
            pygame.draw.circle(s, color, (int(x), int(y)), max(1, vida // 8))

    def dibujar_hud(self):
        datos = NIVELES[self.nivel]
        recogidas = self.total_monedas - len(self.monedas)

        if self.modo_juego == 1:
            restante = max(0, math.ceil((self.limite_frames - self.frames) / FPS))
            tiempo = f"Tiempo: {restante}s"
            color = ROJO_CLARO if restante <= 10 else BLANCO
        else:
            tiempo = f"Tiempo: {self.frames // FPS}s"
            color = BLANCO

        self.texto(
            f"Nivel {self.nivel + 1}/{len(NIVELES)}: {datos['nombre']}   -   "
            f"Monedas {recogidas}/{self.total_monedas}   -   {tiempo}",
            self.fuente_media, color, (ANCHO // 2, 20), centrado=True
        )

        for i, j in enumerate(self.jugadores):
            x0 = 20 if i == 0 else ANCHO - 210
            color_texto = BLANCO if j.activo else GRIS
            self.texto(f"{j.nombre}: {j.puntos}", self.fuente_media, color_texto, (x0, 40))
            for v in range(VIDAS_MAX):
                col = ROJO if v < j.vidas else GRIS
                self.dibujar_corazon(x0 + 125 + v * 26, 52, col, 0.8)

        if self.modo_jug == 1:
            ayuda = "J1: A/D + W     J2: flechas     P: pausa     ESC: menú"
        else:
            ayuda = "Mover: A/D o flechas   |   Saltar: W, arriba o ESPACIO   |   P: pausa   |   ESC: menú"
        self.texto(ayuda, self.fuente_pequena, BLANCO, (ANCHO // 2, 492), centrado=True)

    def lineas_puntuacion(self):
        lineas = [f"{j.nombre}: {j.puntos} puntos" for j in self.jugadores]
        if len(self.jugadores) > 1:
            a, b = self.jugadores[0], self.jugadores[1]
            if a.puntos == b.puntos:
                lineas.append("¡Empate!")
            else:
                ganador = a if a.puntos > b.puntos else b
                lineas.append(f"¡Gana {ganador.nombre}!")
        return lineas

    def dibujar_overlay(self, titulo, color, lineas):
        self.pantalla.blit(self.capa, (0, 0))
        self.texto(titulo, self.fuente_grande, color, (ANCHO // 2, 160), centrado=True)
        for i, linea in enumerate(lineas):
            self.texto(linea, self.fuente, BLANCO, (ANCHO // 2, 225 + i * 38), centrado=True)

    def dibujar_menu(self):
        s = self.pantalla
        s.blit(self.fondo, (0, 0))
        for nube in self.nubes:
            self.dibujar_nube(*nube[:3])
        pygame.draw.rect(s, MARRON, (0, SUELO_Y, ANCHO, ALTO - SUELO_Y))
        pygame.draw.rect(s, VERDE, (0, SUELO_Y, ANCHO, 14))

        self.texto("La aventura de las monedas", self.fuente_grande, AMARILLO,
                   (ANCHO // 2, 60), centrado=True)

        if self.estado == "menu_jugadores":
            subtitulo, opciones = "¿Cuántos jugadores?", OPCIONES_JUGADORES
        else:
            subtitulo, opciones = "Elige el modo de juego", OPCIONES_MODO
        self.texto(subtitulo, self.fuente, BLANCO, (ANCHO // 2, 125), centrado=True)

        for i, (titulo, descripcion) in enumerate(opciones):
            y = 165 + i * 85
            marco = pygame.Rect(200, y, 500, 70)
            pygame.draw.rect(s, PANEL, marco, border_radius=12)
            if i == self.seleccion:
                pygame.draw.rect(s, AMARILLO, marco, width=4, border_radius=12)
            self.texto(f"{i + 1}. {titulo}", self.fuente, BLANCO, (ANCHO // 2, y + 24), centrado=True)
            self.texto(descripcion, self.fuente_pequena, AMARILLO_CLARO, (ANCHO // 2, y + 52), centrado=True)

        pie = "Flechas arriba/abajo o números para elegir  -  ENTER para aceptar  -  ESC para "
        pie += "salir" if self.estado == "menu_jugadores" else "volver"
        self.texto(pie, self.fuente_pequena, BLANCO, (ANCHO // 2, 492), centrado=True)

    def dibujar(self):
        if self.estado in ("menu_jugadores", "menu_modo"):
            self.dibujar_menu()
            return

        self.dibujar_mundo()
        self.dibujar_hud()

        if self.estado == "pausa":
            self.dibujar_overlay("PAUSA", BLANCO, ["Pulsa P para continuar"])
        elif self.estado == "nivel_completo":
            lineas = self.lineas_puntuacion()
            if self.modo_juego == 1:
                lineas.insert(0, f"Bonus de tiempo: +{self.bonus}")
            lineas.append("Pulsa ENTER para continuar")
            self.dibujar_overlay(f"¡NIVEL {self.nivel + 1} COMPLETADO!", AMARILLO, lineas)
        elif self.estado == "ganaste":
            clave = (self.modo_jug, self.modo_juego)
            lineas = self.lineas_puntuacion()
            lineas.append(f"Mejor puntuación: {self.mejores.get(clave, 0)}")
            lineas.append("R: jugar de nuevo   |   ENTER: menú")
            self.dibujar_overlay("¡GANASTE EL JUEGO!", AMARILLO, lineas)
        elif self.estado == "perdiste":
            clave = (self.modo_jug, self.modo_juego)
            lineas = self.lineas_puntuacion()
            lineas.append(f"Mejor puntuación: {self.mejores.get(clave, 0)}")
            lineas.append("R: jugar de nuevo   |   ENTER: menú")
            self.dibujar_overlay(self.motivo or "FIN DEL JUEGO", ROJO, lineas)

    # ------------------------------------------------------------ Eventos
    def ir_menu(self):
        self.estado = "menu_jugadores"
        self.seleccion = self.modo_jug

    def aceptar_opcion(self):
        if self.estado == "menu_jugadores":
            self.modo_jug = self.seleccion
            self.estado = "menu_modo"
            self.seleccion = self.modo_juego
        else:
            self.modo_juego = self.seleccion
            self.nueva_partida()

    def evento_menu(self, tecla):
        opciones = OPCIONES_JUGADORES if self.estado == "menu_jugadores" else OPCIONES_MODO
        n = len(opciones)

        if tecla == pygame.K_ESCAPE:
            if self.estado == "menu_modo":
                self.ir_menu()
            else:
                self.salir()
        elif tecla in (pygame.K_UP, pygame.K_w):
            self.seleccion = (self.seleccion - 1) % n
        elif tecla in (pygame.K_DOWN, pygame.K_s):
            self.seleccion = (self.seleccion + 1) % n
        elif pygame.K_1 <= tecla <= pygame.K_9:
            indice = tecla - pygame.K_1
            if indice < n:
                self.seleccion = indice
                self.aceptar_opcion()
        elif tecla in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            self.aceptar_opcion()

    def eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.salir()
            if evento.type != pygame.KEYDOWN:
                continue

            if self.estado in ("menu_jugadores", "menu_modo"):
                self.evento_menu(evento.key)
                continue

            tecla = evento.key
            if tecla == pygame.K_ESCAPE:
                self.ir_menu()
            elif tecla == pygame.K_r:
                self.nueva_partida()
            elif tecla == pygame.K_p:
                if self.estado == "jugando":
                    self.estado = "pausa"
                elif self.estado == "pausa":
                    self.estado = "jugando"
            elif tecla in (pygame.K_RETURN, pygame.K_KP_ENTER):
                if self.estado == "nivel_completo" and self.bloqueo == 0:
                    self.siguiente_nivel()
                elif self.estado in ("ganaste", "perdiste"):
                    self.ir_menu()

    @staticmethod
    def salir():
        pygame.quit()
        sys.exit()

    def paso(self):
        self.reloj.tick(FPS)
        self.eventos()
        self.actualizar()
        self.dibujar()
        pygame.display.flip()

    def ejecutar(self):
        while True:
            self.paso()


if __name__ == "__main__":
    Juego().ejecutar()
