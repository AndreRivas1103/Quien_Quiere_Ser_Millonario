# ¿Quién Quiere Ser Millonario?

Juego en Python con Pygame basado en el famoso programa de televisión "¿Quién Quiere Ser Millonario?".

## Características

- **10 niveles** con premios escalonados hasta $1,000,000
- **Sistema de estaciones seguras** en las preguntas 5 y 7
- **Comodines disponibles**:
  - 50/50: Elimina dos respuestas incorrectas
  - Saltar pregunta: Cambia la pregunta actual
- **Interfaz gráfica mejorada** con diseño moderno
- **Sistema de preguntas** en formato JSON fácil de modificar
- **Código limpio y estructurado** con separación de responsabilidades

## 📁 Estructura del Proyecto

```
Quien_Quiere_Ser_Millonario/
├── juego/
│   ├── __init__.py          # Paquete del juego
│   ├── config.py            # Configuración y constantes
│   ├── game.py              # Lógica principal del juego
│   ├── ui.py                # Interfaz gráfica
│   ├── questions.py          # Gestión de preguntas y comodines
│   ├── utils.py             # Utilidades y funciones auxiliares
│   └── title.png            # Imagen del título
├── data/
│   └── questions.json       # Base de datos de preguntas
├── main.py                  # Script principal para ejecutar
├── requirements.txt         # Dependencias del proyecto
└── README.md                # Este archivo
```

## 🚀 Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/AndreRivas1103/Quien_Quiere_Ser_Millonario.git
cd Quien_Quiere_Ser_Millonario
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

O instala pygame directamente:
```bash
pip install pygame
```

## Cómo Jugar

1. Ejecuta el juego:
```bash
python3 main.py
```

O directamente:
```bash
python3 juego/game.py
```

**Nota:** En sistemas Linux modernos, usa `python3` en lugar de `python`.

2. Ingresa tu nombre cuando se solicite

3. Usa los controles del teclado:
   - **A, B, C, D**: Seleccionar una opción de respuesta
   - **Enter**: Confirmar tu respuesta
   - **Z**: Usar comodín 50/50 (solo una vez)
   - **X**: Saltar pregunta (solo una vez)
   - **Espacio**: Continuar en pantallas de transición
   - **ESC**: Salir o retirarse en estaciones seguras

## 🏆 Sistema de Premios

- Pregunta 1: $1,000
- Pregunta 2: $2,000
- Pregunta 3: $5,000
- Pregunta 4: $10,000
- **Pregunta 5: $20,000** ⭐ Estación Segura
- Pregunta 6: $50,000
- **Pregunta 7: $100,000** ⭐ Estación Segura
- Pregunta 8: $250,000
- Pregunta 9: $500,000
- Pregunta 10: **$1,000,000** 🏆 Gran Premio

## 📝 Agregar Preguntas

Las preguntas se almacenan en `data/questions.json`. Puedes agregar nuevas preguntas siguiendo este formato:

```json
{
    "question": "Tu pregunta aquí?",
    "options": ["Opción A", "Opción B", "Opción C", "Opción D"],
    "answer": 0,
    "difficulty": 1
}
```

Donde `answer` es el índice de la respuesta correcta (0-3) y `difficulty` es el nivel de dificultad (1-4).

## 🛠️ Mejoras Implementadas

- ✅ Código refactorizado con clases y funciones limpias
- ✅ Separación de responsabilidades (UI, lógica, datos)
- ✅ Diseño visual mejorado con colores y tipografía moderna
- ✅ Sistema de niveles con premios escalonados
- ✅ Pantallas de inicio y fin de juego
- ✅ Manejo mejorado de comodines
- ✅ Base de datos de preguntas en JSON
- ✅ Mejor feedback visual para el usuario

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso educativo.

## 👨‍💻 Autor

Desarrollado con Python y Pygame
