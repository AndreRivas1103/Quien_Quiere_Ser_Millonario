"""
Juego principal - ¿Quién Quiere Ser Millonario?
"""
import pygame
import sys
from juego.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, MAX_QUESTIONS,
    PRIZES, SAFE_HAVENS, KEY_OPTION_A, KEY_OPTION_B,
    KEY_OPTION_C, KEY_OPTION_D, KEY_CONFIRM,
    KEY_FIFTY_FIFTY, KEY_SKIP_QUESTION
)
from juego.questions import QuestionManager, Lifeline
from juego.ui import GameUI


class Game:
    """Clase principal del juego"""
    
    def __init__(self):
        """Inicializa el juego"""
        # Obtener nombre ANTES de inicializar pygame para evitar bloqueos
        self.player_name = self.get_player_name()
        
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("¿Quién Quiere Ser Millonario?")
        
        self.clock = pygame.time.Clock()
        self.ui = GameUI(self.screen)
        self.question_manager = QuestionManager()
        self.lifeline = Lifeline()
        
        self.running = True
        self.current_level = 0
        self.score = 0
        self.selected_option = ""
        self.current_question = None
    
    def get_player_name(self) -> str:
        """Solicita el nombre del jugador"""
        return input("Ingresa tu nombre: ").strip() or "Jugador"
    
    def handle_start_screen(self) -> bool:
        """Maneja la pantalla de inicio"""
        waiting = True
        while waiting and self.running:
            try:
                self.ui.draw_start_screen(self.player_name)
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        return False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            waiting = False
                        elif event.key == pygame.K_ESCAPE:
                            self.running = False
                            return False
                
                self.clock.tick(FPS)
            except Exception as e:
                print(f"Error en pantalla de inicio: {e}")
                import traceback
                traceback.print_exc()
                self.running = False
                return False
        
        return self.running
    
    def handle_safe_haven(self) -> bool:
        """
        Maneja la pantalla de estación segura.
        
        Returns:
            True si continúa, False si se retira
        """
        waiting = True
        continue_game = True
        
        while waiting and self.running:
            self.ui.draw_safe_haven_screen(self.current_level, self.score)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                        continue_game = True
                    elif event.key == pygame.K_ESCAPE:
                        waiting = False
                        continue_game = False
            
            self.clock.tick(FPS)
        
        return continue_game
    
    def handle_end_screen(self, won: bool, correct_answers: int) -> None:
        """Maneja la pantalla de fin de juego"""
        waiting = True
        
        while waiting and self.running:
            self.ui.draw_end_screen(won, self.score, correct_answers, self.player_name)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        waiting = False
            
            self.clock.tick(FPS)
    
    def check_answer(self, user_answer: str, correct_answer: int) -> bool:
        """
        Verifica si la respuesta es correcta.
        
        Args:
            user_answer: Respuesta del usuario (A, B, C, D)
            correct_answer: Índice de la respuesta correcta
            
        Returns:
            True si es correcta, False si no
        """
        letters = ["A", "B", "C", "D"]
        return user_answer.upper() == letters[correct_answer]
    
    def process_game_events(self) -> str:
        """
        Procesa los eventos del juego.
        
        Returns:
            Acción realizada: "answer", "fifty_fifty", "skip", "quit", o ""
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            elif event.type == pygame.KEYDOWN:
                # Selección de opciones
                if event.key == pygame.K_a:
                    self.selected_option = "A"
                elif event.key == pygame.K_b:
                    self.selected_option = "B"
                elif event.key == pygame.K_c:
                    self.selected_option = "C"
                elif event.key == pygame.K_d:
                    self.selected_option = "D"
                
                # Confirmar respuesta
                elif event.key == pygame.K_RETURN:
                    if self.selected_option:
                        return "answer"
                
                # Comodín 50/50
                elif event.key == pygame.K_z:
                    if not self.lifeline.fifty_fifty_used and self.current_question:
                        return "fifty_fifty"
                
                # Comodín saltar pregunta
                elif event.key == pygame.K_x:
                    if not self.lifeline.skip_question_used:
                        return "skip"
        
        return ""
    
    def run(self) -> None:
        """Ejecuta el juego principal"""
        # Pantalla de inicio
        if not self.handle_start_screen():
            self.quit()
            return
        
        # Preparar preguntas
        self.question_manager.shuffle_questions()
        
        # Bucle principal del juego
        correct_answers = 0
        
        while self.running and correct_answers < MAX_QUESTIONS:
            # Obtener siguiente pregunta
            self.current_question = self.question_manager.get_next_question()
            
            if not self.current_question:
                break
            
            self.current_level = correct_answers + 1
            self.selected_option = ""
            
            # Bucle de la pregunta actual
            question_active = True
            
            while question_active and self.running:
                try:
                    # Dibujar pantalla
                    self.ui.draw_game_screen(
                        self.current_question["question"],
                        self.current_question["options"],
                        self.selected_option,
                        self.current_level,
                        self.score,
                        self.player_name,
                        self.lifeline.fifty_fifty_used,
                        self.lifeline.skip_question_used
                    )
                    
                    # Procesar eventos
                    action = self.process_game_events()
                except Exception as e:
                    print(f"Error durante el juego: {e}")
                    import traceback
                    traceback.print_exc()
                    self.running = False
                    break
                
                if action == "quit":
                    self.running = False
                    question_active = False
                
                elif action == "answer":
                    # Verificar respuesta
                    is_correct = self.check_answer(
                        self.selected_option,
                        self.current_question["answer"]
                    )
                    
                    if is_correct:
                        correct_answers += 1
                        self.score = PRIZES[correct_answers - 1]
                        
                        # Verificar si es estación segura
                        if correct_answers in SAFE_HAVENS:
                            if not self.handle_safe_haven():
                                # El jugador se retira
                                self.handle_end_screen(True, correct_answers)
                                self.quit()
                                return
                        
                        # Verificar si ganó
                        if correct_answers >= MAX_QUESTIONS:
                            self.handle_end_screen(True, correct_answers)
                            self.quit()
                            return
                        
                        question_active = False
                    else:
                        # Respuesta incorrecta
                        self.handle_end_screen(False, correct_answers)
                        self.quit()
                        return
                
                elif action == "fifty_fifty":
                    # Usar comodín 50/50
                    if not self.lifeline.fifty_fifty_used:
                        self.current_question["options"] = self.lifeline.use_fifty_fifty(
                            self.current_question["options"],
                            self.current_question["answer"]
                        )
                
                elif action == "skip":
                    if self.lifeline.use_skip_question():
                        question_active = False
                        # Obtener nueva pregunta
                        self.current_question = self.question_manager.get_next_question()
                        if not self.current_question:
                            self.running = False
                            break
                
                self.clock.tick(FPS)
        
        # Fin del juego
        if self.running:
            self.handle_end_screen(True, correct_answers)
        
        self.quit()
    
    def quit(self) -> None:
        """Cierra el juego"""
        pygame.quit()
        sys.exit()


def main():
    """Función principal"""
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\n\nJuego interrumpido por el usuario.")
        pygame.quit()
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError en el juego: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)


if __name__ == "__main__":
    main()
