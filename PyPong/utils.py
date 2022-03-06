from pathlib import Path

from pygame.mixer import Sound
# from pygame.math import Vector2
from pygame import Color


def load_sound(name):
    filename = Path(__file__).parent / Path("sounds" + name + ".wav")
    return Sound(filename)

def print_text(surface, text, 
               font, pos_x_divisor, pos_y, 
               color=Color("white")):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(
        centerx=surface.get_width() / pos_x_divisor, y=pos_y
    )
    surface.blit(text_surface, rect)