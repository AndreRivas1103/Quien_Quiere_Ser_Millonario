"""
Configuración del juego
"""
import os

# Rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(os.path.dirname(BASE_DIR), "assets")
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")

# Configuración de la ventana
WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 900
FPS = 60

# Colores
COLOR_BACKGROUND = (1, 0, 56)
COLOR_TEXT = (255, 255, 255)
COLOR_PRIMARY = (255, 215, 0)  # Dorado
COLOR_SECONDARY = (255, 140, 0)  # Naranja
COLOR_SUCCESS = (0, 255, 0)  # Verde
COLOR_ERROR = (255, 0, 0)  # Rojo
COLOR_OPTION_BG = (30, 30, 100)
COLOR_OPTION_HOVER = (50, 50, 150)
COLOR_OPTION_SELECTED = (100, 150, 255)

# Fuentes
FONT_TITLE_SIZE = 48
FONT_QUESTION_SIZE = 35
FONT_OPTION_SIZE = 30
FONT_SCORE_SIZE = 30
FONT_INFO_SIZE = 20

# Configuración del juego
MAX_QUESTIONS = 10
QUESTION_VALUE = 1000
SAFE_HAVENS = [5, 7]  # Estaciones seguras donde se puede retirar

# Premios por nivel (en pesos colombianos)
PRIZES = [
    1000,      # Pregunta 1
    2000,      # Pregunta 2
    5000,      # Pregunta 3
    10000,     # Pregunta 4
    20000,     # Pregunta 5 (Estación segura)
    50000,     # Pregunta 6
    100000,    # Pregunta 7 (Estación segura)
    250000,    # Pregunta 8
    500000,    # Pregunta 9
    1000000,   # Pregunta 10 (Gran premio)
]

# Teclas
KEY_OPTION_A = "a"
KEY_OPTION_B = "b"
KEY_OPTION_C = "c"
KEY_OPTION_D = "d"
KEY_CONFIRM = "return"
KEY_FIFTY_FIFTY = "z"
KEY_SKIP_QUESTION = "x"
