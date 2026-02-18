import pygame
import sys
import os
from random import shuffle, sample
from time import sleep

# Inicialización de Pygame
pygame.init()

# Función para dibujar la ventana del juego
def draw_window(screen, width, height, title_image, question, options, user_input, score, player_name):
    # Limpiar la pantalla con un color de fondo
    screen.fill((1, 0, 56))
    
    # Dibujar el título en la parte superior de la ventana
    title_rect = title_image.get_rect(midtop=(width // 2, 50))
    screen.blit(title_image, title_rect)

    # Definir fuentes para la pregunta, puntaje y nombre del jugador
    question_font = pygame.font.SysFont("Arial", 35)
    score_font = pygame.font.SysFont("Arial", 30)
    name_font = pygame.font.SysFont("Arial", 20)

    # Dividir y dibujar la pregunta en la ventana
    question_lines = wrap_text(question, question_font, width - 100)
    question_y = (height - len(question_lines) * question_font.get_linesize()) // 3 + 100
    for line in question_lines:
        question_text = question_font.render(line, True, (255, 255, 255))
        screen.blit(question_text, ((width - question_text.get_width()) // 2, question_y))
        question_y += question_font.get_linesize()

    # Mostrar el puntaje en la esquina inferior derecha
    score_text = score_font.render(f"Dinero: ${score}", True, (255, 255, 255))
    screen.blit(score_text, (width - 400, height - 50))

    # Dibujar las opciones de respuesta en la pantalla
    option_font = pygame.font.SysFont("Arial", 30)
    letters = ["A", "B", "C", "D"]
    # Filtrar opciones vacías para calcular el ancho máximo
    non_empty_options = [opt for opt in options if opt]
    if non_empty_options:
        max_option_width = max(option_font.size(option)[0] for option in non_empty_options)
    else:
        max_option_width = 200
    
    for i, (letter, option) in enumerate(zip(letters[:2], options[:2])):
        if option:  # Solo dibujar si la opción no está vacía
            text = option_font.render(f"{letter}. {option}", True, (255, 255, 255))
            text_rect = text.get_rect(midleft=(width // 4 - max_option_width // 2, height // 2 + i * 90 + 85))
            screen.blit(text, text_rect)

    for i, (letter, option) in enumerate(zip(letters[2:], options[2:])):
        if option:  # Solo dibujar si la opción no está vacía
            text = option_font.render(f"{letter}. {option}", True, (255, 255, 255))
            text_rect = text.get_rect(midleft=(width * 3 // 4 - max_option_width // 2, height // 2 + i * 90 + 85))
            screen.blit(text, text_rect)

    # Mostrar la respuesta ingresada por el usuario
    user_input_font = pygame.font.SysFont("Arial", 25)
    text = user_input_font.render(f"Tu Respuesta: {user_input}", True, (255, 255, 255))
    screen.blit(text, (20, height - 50))

    # Mostrar el nombre del jugador en la parte inferior central de la ventana
    name_text = name_font.render(f"Jugador: {player_name}", True, (255, 255, 255))
    name_rect = name_text.get_rect(midbottom=(width // 2, height - 10))
    screen.blit(name_text, name_rect)

    # Actualizar la pantalla
    pygame.display.update()

# Función para verificar si la respuesta del usuario es correcta
def check_answer(correct_answer, user_input):
    letters = ["A", "B", "C", "D"]
    return user_input.upper() == letters[correct_answer]

# Función para usar el comodín del 50/50
def fifty_fifty(options, correct_answer):
    if not fifty_fifty.used:  # Solo se puede usar una vez
        fifty_fifty.used = True
        incorrect_options = [i for i in range(len(options)) if i != correct_answer]
        if len(incorrect_options) >= 2:
            options_to_remove = sample(incorrect_options, 2)
            options = [option if i not in options_to_remove else "" for i, option in enumerate(options)]
    return options

fifty_fifty.used = False

# Función para dividir el texto en varias líneas para ajustarlo en la ventana
def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] < max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)
    return lines

# Función principal del juego
def main():
    # Solicitar el nombre del jugador ANTES de inicializar la ventana
    player_name = input("Ingresa tu nombre: ")

    # Imprimir las reglas del juego
    print("Las reglas son simples: responde preguntas correctamente y avanza. Tienes la opción de 50/50 y cambiar de pregunta. Puedes retirarte en las estaciones 5 y 7.")
    
    width = 1800
    height = 900
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Quiz Game")
    
    # Cargar y ajustar la imagen del título
    script_dir = os.path.dirname(os.path.abspath(__file__))
    title_image_path = os.path.join(script_dir, "title.png")
    title_image = pygame.image.load(title_image_path)
    title_image = pygame.transform.scale(title_image, (300, 300))

    # Lista de preguntas
    questions = [
        {
            "question": "Cual es la capital de Francia?",
            "options": ["Paris", "Berlin", "Londres", "Madrid"],
            "answer": 0
        },
        {
            "question": "¿Cuál es el nombre del parque nacional ubicado en la región amazónica de Colombia que protege una gran diversidad de flora y fauna?",
            "options": ["Parque Nacional Natural Tayrona", "Parque Nacional Natural Los Nevados", "Parque Nacional Natural El Cocuy", "Parque Nacional Natural Amacayacu"],
            "answer": 3
        },
        {
            "question": "¿Qué ciudad colombiana es conocida como la \"Capital del Oro Blanco\" debido a su importante producción de sal?",
            "options": ["Zipaquirá", "Nemocón", "Cúcuta", "La Guajira"],
            "answer": 0
        },
        {
            "question": "¿Cuándo se fundó la ciudad de Bogotá?",
            "options": ["El 29 de julio de 1525", "El 8 de octubre de 1558", "El 6 de agosto de 1538", "El 12 de abril de 1546"],
            "answer": 2
        },
        {
            "question": "¿Cuál es la altura aproximada del Cerro del Quinini, una montaña en Colombia conocida por su misteriosa niebla perpetua?",
            "options": ["2.000 metros", "3.500 metros", "4.800 metros", "6.200 metros"],
            "answer" : 1
        },
        {
            "question": "¿Qué río atraviesa la ciudad de Cali y es famoso por sus rápidos y practicantes de deportes acuáticos?",
            "options": ["Río Bogotá", "Río Cauca", "Río Magdalena", "Río Caquetá"],
            "answer": 1
        },
        {
            "question": "¿Cuál es el nombre de la famosa danza colombiana que representa la lucha entre el bien y el mal, y suele interpretarse en festivales religiosos?",
            "options": ["Danza del Garabato", "Danza del Diablo", "Danza de la Culebra", "Danza de los Congos"],
            "answer": 1
        },
        {
            "question": "¿Cuál es el nombre del fenómeno natural en Colombia que consiste en la formación de miles de luciérnagas sincronizadas que iluminan los bosques?",
            "options": ["Mariposas amarillas", "Flores de luna", "Ríos de estrellas", "Mar de luciérnagas"],
            "answer": 3
        },
        {
            "question": "¿Qué región de Colombia es famosa por sus tejidos de fique, utilizados en la confección de productos artesanales?",
            "options": ["La Costa Caribe", "La Región Andina", "La Orinoquía", "La Amazonía"],
            "answer": 1   
        },
        {
            "question": "¿Qué tipo de música colombiana es originaria de la región del Pacífico y se caracteriza por sus ritmos africanos y letras que narran historias de esclavitud y resistencia?",
            "options": ["Vallenato", "Currulao", "Bambuco", "Joropo"],
            "answer": 1
        },
        {
            "question": "¿Qué fruta tropical originaria de Colombia se caracteriza por su pulpa suave y jugosa, y es conocida como \"la fruta de la pasión\"?",
            "options": ["Guanábana", "Lulo", "Maracuyá", "Papaya"],
            "answer": 2
        },
        {
            "question": "¿Qué ciudad colombiana es conocida por su tradicional Carnaval de Blancos y Negros, declarado Patrimonio Cultural Inmaterial de la Humanidad por la UNESCO?",
            "options": ["Pasto", "Barranquilla", "Cali", "Manizales"],
            "answer": 0
        },
        {
            "question": "¿Qué pintor colombiano es conocido por su estilo impresionista y sus obras que retratan la vida cotidiana de la costa caribeña?",
            "options": ["Alejandro Obregón", "Débora Arango", "Enrique Grau", "Enrique Olaya Herrera"],
            "answer": 2
        },
        {
            "question": "¿Cuál es el nombre del parque nacional ubicado en la región amazónica de Colombia que protege una gran diversidad de flora y fauna?",
            "options": ["Parque Nacional Natural Tayrona", "Parque Nacional Natural Los Nevados", "Parque Nacional Natural El Cocuy", "Parque Nacional Natural Amacayacu"],
            "answer": 3
        },
        {
            "question": "¿Qué ciudad colombiana es conocida como la \"Capital del Oro Blanco\" debido a su importante producción de sal?",
            "options": ["Zipaquirá", "Nemocón", "Cúcuta", "La Guajira"],
            "answer": 0
        },
        {
            "question": "¿En qué año llegó Cristóbal Colón a América?", 
            "options": ["1485", "1473", "1492", "1468"], 
            "answer": 2
        },
        {
            "question": "¿Cuál es la etnia indígena más numerosa de Colombia?", 
            "options": ["Wayuu", "Emberá", "Sikuani", "Yaggua"], 
            "answer": 0
        },
        {
            "question": "¿Cuándo se fundó la ciudad de Bogotá?", 
            "options": ["El 29 de julio de 1525", "El 8 de octubre de 1558", "El 6 de agosto de 1538", "El 12 de abril de 1546"], 
            "answer": 2
        },
        {
            "question": "¿Cuándo ganó la selección colombiana la Copa América de Fútbol?", 
            "options": ["2010", "2005", "2001", "Ninguna de las anteriores"], 
            "answer": 2
        },
        {
            "question": "¿Hasta qué año Panamá formó parte de Colombia?", 
            "options": ["1923", "1903", "1953", "1913"], 
            "answer": 1
        },
        {
            "question": "¿Cuál fue el primer ciclista colombiano en participar en el Giro de Italia?", 
            "options": ["Lucho Herrera", "Oliverio Rincón", "Martín Emilio Rodríguez", "Nairo Quintana"], 
            "answer": 2
        },
        {
            "question": "¿Cómo se llamó el pueblo fundado por los esclavos cimarrones rebeldes liderados por Benkós Biohó a comienzos del siglo XVI?", 
            "options": ["El pueblo de Montería", "San Basilio de Palenque", "La ciudad de Sincelejo", "El pueblo de Puerto Liberador"], 
            "answer": 1
        },
        {
            "question": "¿Qué día se celebra el día de la independencia de Colombia?", 
            "options": ["20 de julio", "19 de abril", "18 de septiembre", "20 de junio"], 
            "answer": 0
        },
    ]
    # Mezclar las preguntas
    shuffle(questions)
    question = questions.pop(0)

    user_input = ""
    correct_answers = 0
    score = 0
    
    # Reloj para controlar la velocidad del bucle
    clock = pygame.time.Clock()

    # Bucle principal del juego
    while correct_answers < 10:
        draw_window(screen, width, height, title_image, question["question"], question["options"], user_input, score, player_name)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    user_input = "A"
                elif event.key == pygame.K_b:
                    user_input = "B"
                elif event.key == pygame.K_c:
                    user_input = "C"
                elif event.key == pygame.K_d:
                    user_input = "D"
                elif event.key == pygame.K_z and not fifty_fifty.used:  # Tecla Z para la ayuda del 50/50
                    question["options"] = fifty_fifty(question["options"], question["answer"])
                elif event.key == pygame.K_x and len(questions) > 0:  # Tecla X para cambiar de pregunta
                    question = questions.pop(0)
                    user_input = ""
                elif event.key == pygame.K_RETURN:
                    if check_answer(question["answer"], user_input):
                        print("Correcto!")
                        correct_answers += 1
                        score += 1000
                        if correct_answers == 5 or correct_answers == 7:
                            decision = input("¿Quieres terminar el juego y llevar tu puntaje actual? (s/n): ")
                            if decision.lower() == 's':
                                print(f"¡Felicidades! ¡Has ganado {score} pesos!")
                                pygame.quit()
                                sys.exit()
                            else:
                                continue
                    else:
                        print(f"Incorrecto! Perdiste ${score}")
                        print(f"Total de preguntas respondidas correctamente: {correct_answers}")
                        sleep(1)
                        pygame.quit()
                        sys.exit()
                    if len(questions) == 0 or correct_answers >= 10:
                        print(f"Total de preguntas respondidas correctamente: {correct_answers}")
                        print(f"¡Felicidades! ¡Has ganado {score} pesos!")
                        pygame.quit()
                        sys.exit()
                    else:
                        question = questions.pop(0)
                        user_input = ""
        
        # Controlar la velocidad del bucle (60 FPS)
        clock.tick(60)

if __name__ == "__main__":
    main()
