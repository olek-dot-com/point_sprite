import pygame
from OpenGL.GL import *

def load_atlas(path: str) -> int:
    tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex)
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.flip(img, False, True)
    w, h = img.get_size()
    data = pygame.image.tostring(img, "RGBA", True)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S,   GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,   GL_CLAMP_TO_EDGE)
    return tex