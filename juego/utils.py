"""
Utilidades del juego
"""
import pygame


def wrap_text(text: str, font: pygame.font.Font, max_width: int) -> list:
    """
    Divide el texto en varias líneas para ajustarlo en la ventana.
    
    Args:
        text: Texto a dividir
        font: Fuente de pygame
        max_width: Ancho máximo permitido
        
    Returns:
        Lista de líneas de texto
    """
    words = text.split(" ")
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] < max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line.strip())
            current_line = word + " "
    
    if current_line:
        lines.append(current_line.strip())
    
    return lines if lines else [""]


def draw_text_centered(surface: pygame.Surface, text: str, font: pygame.font.Font, 
                       color: tuple, y: int, width: int) -> None:
    """
    Dibuja texto centrado horizontalmente.
    
    Args:
        surface: Superficie donde dibujar
        text: Texto a dibujar
        font: Fuente de pygame
        color: Color del texto
        y: Posición Y
        width: Ancho de la superficie
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(width // 2, y))
    surface.blit(text_surface, text_rect)


def draw_button(surface: pygame.Surface, text: str, font: pygame.font.Font,
                x: int, y: int, width: int, height: int,
                bg_color: tuple, text_color: tuple,
                hover: bool = False) -> pygame.Rect:
    """
    Dibuja un botón en la superficie.
    
    Args:
        surface: Superficie donde dibujar
        text: Texto del botón
        font: Fuente de pygame
        x, y: Posición
        width, height: Dimensiones
        bg_color: Color de fondo
        text_color: Color del texto
        hover: Si el botón está siendo hover
        
    Returns:
        Rectángulo del botón
    """
    if hover:
        bg_color = tuple(min(255, c + 30) for c in bg_color)
    
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, bg_color, button_rect)
    pygame.draw.rect(surface, text_color, button_rect, 2)
    
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=button_rect.center)
    surface.blit(text_surface, text_rect)
    
    return button_rect
