"""
Manejo de preguntas del juego
"""
import json
import os
from random import shuffle, sample
from typing import List, Dict, Optional
from juego.config import DATA_DIR


class QuestionManager:
    """Gestiona las preguntas del juego"""
    
    def __init__(self, questions_file: str = "questions.json"):
        """
        Inicializa el gestor de preguntas.
        
        Args:
            questions_file: Nombre del archivo JSON con las preguntas
        """
        self.questions_file = os.path.join(DATA_DIR, questions_file)
        self.questions: List[Dict] = []
        self.current_question: Optional[Dict] = None
        self.load_questions()
    
    def load_questions(self) -> None:
        """Carga las preguntas desde el archivo JSON"""
        try:
            with open(self.questions_file, 'r', encoding='utf-8') as f:
                self.questions = json.load(f)
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {self.questions_file}")
            self.questions = []
        except json.JSONDecodeError:
            print(f"Error: El archivo {self.questions_file} no es un JSON válido")
            self.questions = []
    
    def shuffle_questions(self) -> None:
        """Mezcla las preguntas aleatoriamente"""
        shuffle(self.questions)
    
    def get_next_question(self) -> Optional[Dict]:
        """
        Obtiene la siguiente pregunta.
        
        Returns:
            Diccionario con la pregunta o None si no hay más
        """
        if self.questions:
            self.current_question = self.questions.pop(0).copy()
            return self.current_question
        return None
    
    def get_current_question(self) -> Optional[Dict]:
        """Obtiene la pregunta actual"""
        return self.current_question
    
    def has_more_questions(self) -> bool:
        """Verifica si hay más preguntas disponibles"""
        return len(self.questions) > 0
    
    def get_remaining_count(self) -> int:
        """Obtiene el número de preguntas restantes"""
        return len(self.questions)


class Lifeline:
    """Gestiona los comodines del juego"""
    
    def __init__(self):
        self.fifty_fifty_used = False
        self.skip_question_used = False
    
    def use_fifty_fifty(self, options: List[str], correct_answer: int) -> List[str]:
        """
        Usa el comodín 50/50 eliminando dos respuestas incorrectas.
        
        Args:
            options: Lista de opciones
            correct_answer: Índice de la respuesta correcta
            
        Returns:
            Lista de opciones con dos eliminadas
        """
        if self.fifty_fifty_used:
            return options
        
        self.fifty_fifty_used = True
        incorrect_options = [i for i in range(len(options)) if i != correct_answer]
        
        if len(incorrect_options) >= 2:
            options_to_remove = sample(incorrect_options, 2)
            new_options = [
                option if i not in options_to_remove else ""
                for i, option in enumerate(options)
            ]
            return new_options
        
        return options
    
    def use_skip_question(self) -> bool:
        """
        Usa el comodín para saltar pregunta.
        
        Returns:
            True si se puede usar, False si ya se usó
        """
        if self.skip_question_used:
            return False
        
        self.skip_question_used = True
        return True
    
    def reset(self) -> None:
        """Reinicia todos los comodines"""
        self.fifty_fifty_used = False
        self.skip_question_used = False
