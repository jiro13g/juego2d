# La aventura de las monedas

Juego de plataformas 2D hecho con **Python** y **pygame**. Recoge todas las
monedas, salta sobre los enemigos y evita caer a los precipicios.

## Características

- **3 formas de jugar:** un jugador, dos jugadores en el mismo teclado, o jugador contra la computadora.
- **2 modos de juego:** *Clásico* (3 vidas, sin límite de tiempo) y *Contrarreloj* (tiempo límite por nivel y bonus por rapidez).
- **5 niveles** con dificultad creciente: Pradera, Dos abismos, La torre, Las islas y El castillo.
- Enemigos que se pueden aplastar saltando encima.
- Salto variable, *coyote time* y *jump buffer* para un control más justo.
- Efectos de partículas, monedas animadas y HUD con vidas y puntuación.

## Requisitos

- Python 3.9 o superior
- pygame 2.5 o superior

## Instalación y ejecución

```bash
# 1. Clona el repositorio
git clone https://github.com/TU_USUARIO/aventura-monedas.git
cd aventura-monedas

# 2. (Opcional) crea un entorno virtual
python -m venv .venv
source .venv/bin/activate      # En Windows: .venv\Scripts\activate

# 3. Instala las dependencias
pip install -r requirements.txt

# 4. Juega
python juego2d.py
```

## Controles

| Acción | Un jugador / vs CPU | Dos jugadores |
|--------|---------------------|---------------|
| Moverse | `A` / `D` o flechas | J1: `A` / `D` · J2: flechas |
| Saltar | `W`, flecha arriba o `ESPACIO` | J1: `W` o `ESPACIO` · J2: flecha arriba |
| Pausa | `P` | `P` |
| Reiniciar partida | `R` | `R` |
| Volver al menú | `ESC` | `ESC` |
| Continuar al siguiente nivel | `ENTER` | `ENTER` |

En los menús usa las flechas arriba/abajo o los números para elegir, y `ENTER` para aceptar.

## Cómo se juega

- Cada moneda vale **10 puntos** y aplastar un enemigo **50**.
- Si un enemigo te toca o caes a un precipicio, pierdes una vida.
- Al completar un nivel recuperas una vida (hasta 3).
- En los modos de dos jugadores y contra la computadora, las monedas son compartidas y gana quien tenga más puntos.
- En *Contrarreloj*, si se acaba el tiempo pierdes la partida; si terminas antes, recibes un bonus.

## Estructura del proyecto

```
.
├── juego2d.py         # Código del juego
├── requirements.txt   # Dependencias
├── README.md
├── LICENSE
└── .gitignore
```

## Licencia

Distribuido bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE).
