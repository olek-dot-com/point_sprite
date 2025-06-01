import pygame
from pygame.locals import *
from OpenGL.GL import *
import numpy as np
from emitter import ParticleEmitter
from camera import OrbitCamera
from scene import draw_ground  # ta wersja co wyżej, bez glut

def load_shader(shader_type, source):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
        raise RuntimeError(glGetShaderInfoLog(shader))
    return shader

def create_program(vertex_path, fragment_path):
    with open(vertex_path, 'r') as f:
        vertex_src = f.read()
    with open(fragment_path, 'r') as f:
        fragment_src = f.read()
    program = glCreateProgram()
    vertex_shader = load_shader(GL_VERTEX_SHADER, vertex_src)
    fragment_shader = load_shader(GL_FRAGMENT_SHADER, fragment_src)
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)
    if glGetProgramiv(program, GL_LINK_STATUS) != GL_TRUE:
        raise RuntimeError(glGetProgramInfoLog(program))
    return program

def load_texture(path):
    from PIL import Image
    img = Image.open(path).convert('RGBA')
    img_data = img.tobytes()
    width, height = img.size
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return tex_id

def main():
    # --- Inicjalizacja ---
    pygame.init()
    width, height = 1000, 700
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("System cząstek - point sprite rain (PyOpenGL)")
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_PROGRAM_POINT_SIZE)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # --- Tworzenie obiektów ---
    emitter = ParticleEmitter(num_particles=1200)
    camera = OrbitCamera()

    program = create_program("shaders/vertex_shader.glsl", "shaders/fragment_shader.glsl")
    sprite_tex = load_texture("textures/raindrop.png")

    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    glBindVertexArray(vao)
    positions = emitter.get_positions()
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, positions.nbytes, positions, GL_DYNAMIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    clock = pygame.time.Clock()
    running = True
    mouse_down = False
    last_pos = None

    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_down = True
                    last_pos = pygame.mouse.get_pos()
                elif event.button == 4:
                    camera.zoom(-1)
                elif event.button == 5:
                    camera.zoom(1)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_down = False
            elif event.type == pygame.MOUSEMOTION and mouse_down:
                x, y = pygame.mouse.get_pos()
                dx = x - last_pos[0]
                dy = y - last_pos[1]
                camera.process_mouse(dx, dy)
                last_pos = (x, y)

        emitter.update(dt)
        positions = emitter.get_positions()

        glClearColor(0.42, 0.58, 0.95, 1.0)  # kolor nieba
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # --- Rysowanie tła ---
        glUseProgram(0)
        draw_ground()

        # --- Rysowanie deszczu (point sprite) ---
        glUseProgram(program)
        loc_view = glGetUniformLocation(program, "view")
        loc_proj = glGetUniformLocation(program, "projection")
        glUniformMatrix4fv(loc_view, 1, GL_FALSE, camera.get_view_matrix().astype(np.float32).T)
        glUniformMatrix4fv(loc_proj, 1, GL_FALSE, camera.get_projection_matrix(width, height).astype(np.float32).T)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, sprite_tex)
        glUniform1i(glGetUniformLocation(program, "spriteTex"), 0)

        glBindVertexArray(vao)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, positions.nbytes, positions, GL_DYNAMIC_DRAW)
        glDrawArrays(GL_POINTS, 0, len(positions))
        glBindVertexArray(0)
        glUseProgram(0)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
