#!/usr/bin/env python3
"""
Script de prueba para verificar que el juego funciona correctamente
"""
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Prueba que todas las importaciones funcionen"""
    print("Probando importaciones...")
    try:
        from juego.config import WINDOW_WIDTH, WINDOW_HEIGHT
        print(f"✓ Config cargado (Ventana: {WINDOW_WIDTH}x{WINDOW_HEIGHT})")
        
        from juego.questions import QuestionManager, Lifeline
        print("✓ QuestionManager y Lifeline importados")
        
        from juego.ui import GameUI
        print("✓ GameUI importado")
        
        from juego.game import Game
        print("✓ Game importado")
        
        return True
    except Exception as e:
        print(f"✗ Error en importaciones: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_questions():
    """Prueba la carga de preguntas"""
    print("\nProbando carga de preguntas...")
    try:
        from juego.questions import QuestionManager
        qm = QuestionManager()
        print(f"✓ Preguntas cargadas: {len(qm.questions)} preguntas")
        
        if qm.questions:
            qm.shuffle_questions()
            question = qm.get_next_question()
            if question:
                print(f"✓ Primera pregunta obtenida: {question['question'][:50]}...")
            else:
                print("✗ No se pudo obtener pregunta")
                return False
        else:
            print("⚠ Advertencia: No hay preguntas cargadas")
        
        return True
    except Exception as e:
        print(f"✗ Error cargando preguntas: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_pygame_init():
    """Prueba la inicialización de pygame"""
    print("\nProbando inicialización de pygame...")
    try:
        import pygame
        pygame.init()
        print("✓ Pygame inicializado")
        
        # Intentar crear una superficie pequeña
        screen = pygame.display.set_mode((100, 100))
        print("✓ Superficie creada")
        
        pygame.quit()
        print("✓ Pygame cerrado correctamente")
        return True
    except Exception as e:
        print(f"✗ Error inicializando pygame: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("PRUEBAS DEL JUEGO - ¿QUIÉN QUIERE SER MILLONARIO?")
    print("=" * 50)
    
    all_tests_passed = True
    
    all_tests_passed &= test_imports()
    all_tests_passed &= test_questions()
    all_tests_passed &= test_pygame_init()
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("✓ TODAS LAS PRUEBAS PASARON")
        print("\nPuedes ejecutar el juego con: python3 main.py")
    else:
        print("✗ ALGUNAS PRUEBAS FALLARON")
        print("Revisa los errores arriba antes de ejecutar el juego")
    print("=" * 50)
