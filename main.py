import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
from PIL import Image
from Raindrop import Raindrop


def init_pygame_opengl():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
    glTranslatef(0.0, 0.0, -20)

    # OpenGL: konfiguracja renderingu
    glEnable(GL_DEPTH_TEST)  # Głębia
    glEnable(GL_BLEND)  # Przezroczystość
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glEnable(GL_TEXTURE_2D)  # Włączenie tekstur
    glEnable(GL_POINT_SPRITE)  # Włączenie point sprite
    glTexEnvi(GL_POINT_SPRITE, GL_COORD_REPLACE, GL_TRUE)  # Tekstura ma działać per punkt

    glEnable(GL_PROGRAM_POINT_SIZE)  # Pozwól ustawić rozmiar punktu z kodu
    glPointSize(32)  # Rozmiar punktu (sprite'a)

    glClearColor(0.1, 0.1, 0.1, 1.0)  # Ciemne tło (lepszy kontrast)

    # Dodatkowe ustawienia dla lepszej obsługi przezroczystości
    glEnable(GL_ALPHA_TEST)
    glAlphaFunc(GL_GREATER, 0.1)  # Piksele z alfą mniejszą niż 0.1 będą przezroczyste

def main_loop():
    init_pygame_opengl()

    # Wczytanie tekstury dla kropli
    texture_id = load_texture_pygame("raindrop.png")

    # Inicjalizacja kropli deszczu
    raindrops = [Raindrop() for _ in range(1200)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Czyszczenie ekranu i bufora głębokości
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Aktywacja tekstury
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glColor4f(1.0, 1.0, 1.0, 1.0)  # Biały kolor = pełna jasność tekstury

        # Aktualizacja i rysowanie każdej kropli
        for drop in raindrops:
            drop.update()
            drop.draw()

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()


def load_texture_pygame(path):
    texture_surface = pygame.image.load(path)
    texture_surface = texture_surface.convert_alpha()  # Upewnij się, że mamy kanał alfa
    texture_data = pygame.image.tostring(texture_surface, "RGBA")  # True = flip w pionie

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGBA,
        texture_surface.get_width(),
        texture_surface.get_height(),
        0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data
    )

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

    return tex_id

if __name__ == "__main__":
    main_loop()
