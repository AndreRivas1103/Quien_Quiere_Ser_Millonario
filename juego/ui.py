"""
Interfaz gráfica del juego
"""
import pygame
from typing import Optional, Tuple
from juego.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BACKGROUND, COLOR_TEXT,
    COLOR_PRIMARY, COLOR_SECONDARY, COLOR_SUCCESS, COLOR_ERROR,
    COLOR_OPTION_BG, COLOR_OPTION_HOVER, COLOR_OPTION_SELECTED,
    FONT_TITLE_SIZE, FONT_QUESTION_SIZE, FONT_OPTION_SIZE,
    FONT_SCORE_SIZE, FONT_INFO_SIZE, PRIZES, SAFE_HAVENS
)
from juego.utils import wrap_text, draw_text_centered, draw_button


class GameUI:
    """Gestiona la interfaz gráfica del juego"""
    
    def __init__(self, screen: pygame.Surface):
        """
        Inicializa la UI del juego.
        
        Args:
            screen: Superficie de pygame donde dibujar
        """
        self.screen = screen
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        
        # Cargar fuentes
        self.font_title = pygame.font.SysFont("Arial", FONT_TITLE_SIZE, bold=True)
        self.font_question = pygame.font.SysFont("Arial", FONT_QUESTION_SIZE)
        self.font_option = pygame.font.SysFont("Arial", FONT_OPTION_SIZE)
        self.font_score = pygame.font.SysFont("Arial", FONT_SCORE_SIZE, bold=True)
        self.font_info = pygame.font.SysFont("Arial", FONT_INFO_SIZE)
        
        # Cargar imagen del título
        self.title_image = self._load_title_image()
        
        # Rectángulos de las opciones para detectar clics
        self.option_rects = []
    
    def _load_title_image(self) -> Optional[pygame.Surface]:
        """Carga la imagen del título"""
        try:
            import os
            script_dir = os.path.dirname(os.path.abspath(__file__))
            title_path = os.path.join(script_dir, "title.png")
            if os.path.exists(title_path):
                image = pygame.image.load(title_path)
                return pygame.transform.scale(image, (300, 300))
            else:
                print(f"Advertencia: No se encontró la imagen {title_path}")
                return None
        except Exception as e:
            print(f"Error al cargar la imagen del título: {e}")
            return None
    
    def draw_game_screen(self, question: str, options: list, selected_option: str,
                        current_level: int, score: int, player_name: str,
                        lifeline_fifty_used: bool, lifeline_skip_used: bool) -> None:
        """
        Dibuja la pantalla principal del juego.
        
        Args:
            question: Texto de la pregunta
            options: Lista de opciones de respuesta
            selected_option: Opción seleccionada por el usuario
            current_level: Nivel actual (1-10)
            score: Puntaje actual
            player_name: Nombre del jugador
            lifeline_fifty_used: Si el comodín 50/50 fue usado
            lifeline_skip_used: Si el comodín de saltar fue usado
        """
        # Limpiar pantalla
        self.screen.fill(COLOR_BACKGROUND)
        
        # Dibujar título
        if self.title_image:
            title_rect = self.title_image.get_rect(midtop=(self.width // 2, 20))
            self.screen.blit(self.title_image, title_rect)
        
        # Dibujar información del nivel y premio
        self._draw_level_info(current_level, score)
        
        # Dibujar pregunta
        self._draw_question(question)
        
        # Dibujar opciones
        self._draw_options(options, selected_option)
        
        # Dibujar información del jugador y comodines
        self._draw_player_info(player_name, lifeline_fifty_used, lifeline_skip_used)
        
        # Actualizar pantalla
        pygame.display.update()
    
    def _draw_level_info(self, level: int, score: int) -> None:
        """Dibuja la información del nivel y premio"""
        # Nivel actual
        level_text = f"Pregunta {level}/10"
        level_surface = self.font_score.render(level_text, True, COLOR_PRIMARY)
        self.screen.blit(level_surface, (50, 50))
        
        # Premio actual
        if level <= len(PRIZES):
            prize = PRIZES[level - 1]
            prize_text = f"Premio: ${prize:,}"
            prize_surface = self.font_score.render(prize_text, True, COLOR_SECONDARY)
            self.screen.blit(prize_surface, (50, 90))
            
            # Indicador de estación segura
            if level in SAFE_HAVENS:
                safe_text = "ESTACIÓN SEGURA"
                safe_surface = self.font_info.render(safe_text, True, COLOR_SUCCESS)
                self.screen.blit(safe_surface, (50, 130))
        
        # Puntaje acumulado
        score_text = f"Dinero acumulado: ${score:,}"
        score_surface = self.font_score.render(score_text, True, COLOR_TEXT)
        score_rect = score_surface.get_rect(topright=(self.width - 50, 50))
        self.screen.blit(score_surface, score_rect)
    
    def _draw_question(self, question: str) -> None:
        """Dibuja la pregunta"""
        question_lines = wrap_text(question, self.font_question, self.width - 100)
        start_y = 200
        
        for i, line in enumerate(question_lines):
            draw_text_centered(
                self.screen, line, self.font_question,
                COLOR_TEXT, start_y + i * self.font_question.get_linesize(),
                self.width
            )
    
    def _draw_options(self, options: list, selected_option: str) -> None:
        """Dibuja las opciones de respuesta"""
        letters = ["A", "B", "C", "D"]
        self.option_rects = []
        
        # Calcular posiciones
        option_width = 400
        option_height = 80
        spacing = 20
        start_x = (self.width - (2 * option_width + spacing)) // 2
        start_y = 400
        
        for i, (letter, option) in enumerate(zip(letters, options)):
            if not option:  # Opción eliminada por 50/50
                continue
            
            # Calcular posición
            row = i // 2
            col = i % 2
            x = start_x + col * (option_width + spacing)
            y = start_y + row * (option_height + spacing)
            
            # Color según selección
            if letter == selected_option:
                bg_color = COLOR_OPTION_SELECTED
                border_color = COLOR_PRIMARY
            else:
                bg_color = COLOR_OPTION_BG
                border_color = COLOR_TEXT
            
            # Dibujar botón de opción
            option_rect = pygame.Rect(x, y, option_width, option_height)
            pygame.draw.rect(self.screen, bg_color, option_rect)
            pygame.draw.rect(self.screen, border_color, option_rect, 3)
            
            # Dibujar texto
            option_text = f"{letter}. {option}"
            text_surface = self.font_option.render(option_text, True, COLOR_TEXT)
            text_rect = text_surface.get_rect(center=option_rect.center)
            self.screen.blit(text_surface, text_rect)
            
            self.option_rects.append((option_rect, letter))
    
    def _draw_player_info(self, player_name: str, lifeline_fifty_used: bool,
                         lifeline_skip_used: bool) -> None:
        """Dibuja información del jugador y comodines"""
        # Nombre del jugador
        name_text = f"Jugador: {player_name}"
        name_surface = self.font_info.render(name_text, True, COLOR_TEXT)
        name_rect = name_surface.get_rect(midbottom=(self.width // 2, self.height - 10))
        self.screen.blit(name_surface, name_rect)
        
        # Comodines
        y_pos = self.height - 50
        x_start = 50
        
        # Comodín 50/50
        fifty_text = "50/50"
        fifty_color = COLOR_ERROR if lifeline_fifty_used else COLOR_SUCCESS
        fifty_surface = self.font_info.render(fifty_text, True, fifty_color)
        self.screen.blit(fifty_surface, (x_start, y_pos))
        
        # Comodín saltar pregunta
        skip_text = "Saltar"
        skip_color = COLOR_ERROR if lifeline_skip_used else COLOR_SUCCESS
        skip_surface = self.font_info.render(skip_text, True, skip_color)
        self.screen.blit(skip_surface, (x_start + 100, y_pos))
        
        # Instrucciones
        instructions = "Presiona A/B/C/D para seleccionar | Enter para confirmar | Z: 50/50 | X: Saltar"
        inst_surface = self.font_info.render(instructions, True, COLOR_TEXT)
        inst_rect = inst_surface.get_rect(bottomright=(self.width - 50, self.height - 10))
        self.screen.blit(inst_surface, inst_rect)
    
    def draw_start_screen(self, player_name: str) -> bool:
        """
        Dibuja la pantalla de inicio.
        
        Args:
            player_name: Nombre del jugador
            
        Returns:
            True si el usuario quiere comenzar
        """
        self.screen.fill(COLOR_BACKGROUND)
        
        # Título
        if self.title_image:
            title_rect = self.title_image.get_rect(center=(self.width // 2, 200))
            self.screen.blit(self.title_image, title_rect)
        
        # Bienvenida
        welcome_text = f"¡Bienvenido, {player_name}!"
        draw_text_centered(self.screen, welcome_text, self.font_title,
                          COLOR_PRIMARY, 350, self.width)
        
        # Reglas
        rules = [
            "Responde 10 preguntas correctamente para ganar $1,000,000",
            "Puedes usar los comodines 50/50 (Z) y Saltar pregunta (X)",
            "En las preguntas 5 y 7 puedes retirarte con tu premio",
            "¡Buena suerte!"
        ]
        
        y_start = 450
        for i, rule in enumerate(rules):
            draw_text_centered(self.screen, rule, self.font_info,
                             COLOR_TEXT, y_start + i * 40, self.width)
        
        # Botón de comenzar
        start_button = draw_button(
            self.screen, "Presiona ESPACIO para comenzar",
            self.font_option, self.width // 2 - 250, 650, 500, 60,
            COLOR_OPTION_BG, COLOR_PRIMARY
        )
        
        pygame.display.update()
        return start_button
    
    def draw_end_screen(self, won: bool, score: int, correct_answers: int,
                       player_name: str) -> None:
        """
        Dibuja la pantalla de fin de juego.
        
        Args:
            won: Si el jugador ganó
            score: Puntaje final
            correct_answers: Número de respuestas correctas
            player_name: Nombre del jugador
        """
        self.screen.fill(COLOR_BACKGROUND)
        
        if won:
            title_text = "¡FELICIDADES!"
            color = COLOR_SUCCESS
            message = f"¡Has ganado ${score:,}!"
        else:
            title_text = "FIN DEL JUEGO"
            color = COLOR_ERROR
            message = f"Has respondido {correct_answers} preguntas correctamente"
        
        draw_text_centered(self.screen, title_text, self.font_title,
                          color, 200, self.width)
        
        draw_text_centered(self.screen, message, self.font_question,
                          COLOR_TEXT, 300, self.width)
        
        draw_text_centered(self.screen, f"Puntaje final: ${score:,}",
                          self.font_score, COLOR_PRIMARY, 400, self.width)
        
        draw_text_centered(self.screen, "Presiona ESC para salir",
                          self.font_info, COLOR_TEXT, 600, self.width)
        
        pygame.display.update()
    
    def draw_safe_haven_screen(self, current_level: int, score: int) -> bool:
        """
        Dibuja la pantalla de estación segura.
        
        Args:
            current_level: Nivel actual
            score: Puntaje actual
            
        Returns:
            True si el jugador quiere continuar, False si se retira
        """
        self.screen.fill(COLOR_BACKGROUND)
        
        draw_text_centered(self.screen, "ESTACIÓN SEGURA",
                          self.font_title, COLOR_SUCCESS, 200, self.width)
        
        draw_text_centered(self.screen, f"Puedes retirarte con ${score:,}",
                          self.font_question, COLOR_TEXT, 300, self.width)
        
        draw_text_centered(self.screen, "¿Quieres continuar?",
                          self.font_info, COLOR_TEXT, 400, self.width)
        
        draw_text_centered(self.screen, "Presiona ESPACIO para continuar | ESC para retirarte",
                          self.font_info, COLOR_TEXT, 500, self.width)
        
        pygame.display.update()
        return True
