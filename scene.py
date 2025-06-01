from OpenGL.GL import *
import numpy as np

def draw_ground():
    # Trawa (ziemia)
    glColor3f(0.18, 0.4, 0.18)
    glBegin(GL_QUADS)
    glVertex3f(-10, 0, -10)
    glVertex3f(10, 0, -10)
    glVertex3f(10, 0, 10)
    glVertex3f(-10, 0, 10)
    glEnd()

    # Domek jako sześcian
    glColor3f(0.5, 0.3, 0.2)
    draw_cube(-3, 0.5, 2, 2, 1, 2)

    # Dach domku (piramida)
    glColor3f(0.8, 0.2, 0.2)
    draw_pyramid(-3, 1.1, 2, 2, 1)

    # Drzewko: pień
    glColor3f(0.4, 0.2, 0.1)
    draw_cube(5, 0.4, -2, 0.4, 0.8, 0.4)

    # Korona drzewa (kula z trójkątów)
    glColor3f(0.2, 0.4, 0.2)
    draw_sphere(5, 1.2, -2, 0.8)


def draw_cube(cx, cy, cz, sx, sy, sz):
    # Narysuj sześcian w środku (cx,cy,cz) o rozmiarach sx,sy,sz
    x = sx / 2;
    y = sy / 2;
    z = sz / 2
    # 6 ścian, każda z 4 wierzchołków
    glBegin(GL_QUADS)
    # Dolna
    glVertex3f(cx - x, cy - y, cz - z)
    glVertex3f(cx + x, cy - y, cz - z)
    glVertex3f(cx + x, cy - y, cz + z)
    glVertex3f(cx - x, cy - y, cz + z)
    # Górna
    glVertex3f(cx - x, cy + y, cz - z)
    glVertex3f(cx + x, cy + y, cz - z)
    glVertex3f(cx + x, cy + y, cz + z)
    glVertex3f(cx - x, cy + y, cz + z)
    # Przód
    glVertex3f(cx - x, cy - y, cz + z)
    glVertex3f(cx + x, cy - y, cz + z)
    glVertex3f(cx + x, cy + y, cz + z)
    glVertex3f(cx - x, cy + y, cz + z)
    # Tył
    glVertex3f(cx - x, cy - y, cz - z)
    glVertex3f(cx + x, cy - y, cz - z)
    glVertex3f(cx + x, cy + y, cz - z)
    glVertex3f(cx - x, cy + y, cz - z)
    # Lewa
    glVertex3f(cx - x, cy - y, cz - z)
    glVertex3f(cx - x, cy - y, cz + z)
    glVertex3f(cx - x, cy + y, cz + z)
    glVertex3f(cx - x, cy + y, cz - z)
    # Prawa
    glVertex3f(cx + x, cy - y, cz - z)
    glVertex3f(cx + x, cy - y, cz + z)
    glVertex3f(cx + x, cy + y, cz + z)
    glVertex3f(cx + x, cy + y, cz - z)
    glEnd()


def draw_pyramid(cx, cy, cz, sx, h):
    # Piramida z podstawą kwadratową
    x = sx / 2
    # Podstawa (opcjonalnie)
    glBegin(GL_QUADS)
    glVertex3f(cx - x, cy, cz - x)
    glVertex3f(cx + x, cy, cz - x)
    glVertex3f(cx + x, cy, cz + x)
    glVertex3f(cx - x, cy, cz + x)
    glEnd()
    # 4 ściany boczne (trójkąty)
    glBegin(GL_TRIANGLES)
    for dx, dz in [(-x, -x), (x, -x), (x, x), (-x, x)]:
        glVertex3f(cx, cy + h, cz)
        glVertex3f(cx + dx, cy, cz + dz)
        glVertex3f(cx + dx if dz == x else cx - x if dx == x else cx + x, cy,
                   cz + dz if dx == x else cz - x if dz == x else cz + x)
    glEnd()


def draw_sphere(cx, cy, cz, r, stacks=8, slices=8):
    # Bardzo uproszczona kula z "siatki"
    for i in range(stacks):
        lat0 = np.pi * (-0.5 + float(i) / stacks)
        z0 = np.sin(lat0)
        zr0 = np.cos(lat0)
        lat1 = np.pi * (-0.5 + float(i + 1) / stacks)
        z1 = np.sin(lat1)
        zr1 = np.cos(lat1)
        glBegin(GL_QUAD_STRIP)
        for j in range(slices + 1):
            lng = 2 * np.pi * float(j) / slices
            x = np.cos(lng)
            y = np.sin(lng)
            glVertex3f(cx + r * x * zr0, cy + r * y * zr0, cz + r * z0)
            glVertex3f(cx + r * x * zr1, cy + r * y * zr1, cz + r * z1)
        glEnd()
