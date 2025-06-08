import pygame
from pygame.locals import DOUBLEBUF, OPENGL, K_ESCAPE, K_TAB, K_r
from glm import perspective, radians, rotate, mat4, vec3
from context import init_context
from shaders import create_shader
from textures import load_atlas
from particles import ParticleSystem
from renderer import Renderer
from camera import Camera
from config import FLIGHT_FRAME_T


# Nowe importy dla sceny
from scene_loader import GLTFScene
from scene_shaders import create_scene_shader
from scene_renderer import SceneRenderer

from OpenGL.GL import *
from skybox_renderer import SkyboxRenderer

def main():
    # 1) Init window + GL context
    init_context(800, 600, "Deszcz Point-Sprite")

    # 2) Load rain resources
    rain_shader = create_shader()
    atlas_tex = load_atlas("atlas.png")
    psys = ParticleSystem()
    rain_renderer = Renderer(rain_shader, psys, atlas_tex)
    skybox = SkyboxRenderer("sky/skymap.png", 0.7)

    # 3) Load scene
    scene = GLTFScene()
    try:
        scene.load('scene/scene2.gltf')  # Ścieżka z oryginalnego kodu
        scene.prepare_for_rendering()
        scene_shader = create_scene_shader()
        scene_renderer = SceneRenderer(scene_shader, scene)
        scene_loaded = True
        print(f"Załadowano scenę: {len(scene.vao_list)} obiektów")
    except Exception as e:
        print(f"Błąd ładowania sceny: {e}")
        scene_loaded = False

    # 4) Setup camera control
    camera = Camera()
    camera_enabled = True
    rain_enabled = True

    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    pygame.mouse.get_rel()  # flush motion

    # 5) Projection
    proj = perspective(radians(45.0), 800 / 600, 0.1, 200.0)


    # 6) Main loop
    clock = pygame.time.Clock()
    running = True

    print("Sterowanie:")
    print("ESC - wyjście")
    print("TAB - włącz/wyłącz kontrolę kamery")
    print("R - włącz/wyłącz deszcz")
    print("WSAD - ruch kamery")
    print("Spacja - w górę, Shift - w dół")

    while running:
        dt = clock.tick(60) / 1000.0

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == K_ESCAPE:
                    running = False
                elif e.key == K_TAB:
                    camera_enabled = not camera_enabled
                    pygame.mouse.set_visible(not camera_enabled)
                    pygame.event.set_grab(camera_enabled)
                    pygame.mouse.get_rel()  # flush motion
                    print(f"Kontrola kamery: {'włączona' if camera_enabled else 'wyłączona'}")
                elif e.key == K_r:
                    rain_enabled = not rain_enabled
                    print(f"Deszcz: {'włączony' if rain_enabled else 'wyłączony'}")

        # Camera input
        if camera_enabled:
            dx, dy = pygame.mouse.get_rel()
            camera.process_mouse_delta(dx, dy)

        keys = pygame.key.get_pressed()
        if camera_enabled:
            camera.process_keyboard(keys, dt)

        # Update systems
        if rain_enabled:
            psys.update(dt)

        flightFrame = int((pygame.time.get_ticks() / 1000.0 / FLIGHT_FRAME_T) % 2)

        # Render
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.1, 0.1, 0.1, 1.0)  # Sky blue background
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        view = camera.get_view_matrix()

        skybox.render(proj, view)

        # Render scene
        if scene_loaded:
            # Create rotation matrix for the scene
            model_matrix = rotate(mat4(1.0), radians(90), vec3(1, 0, 0))
            scene_renderer.set_model_matrix(model_matrix)
            scene_renderer.render(proj, view, camera.position)

        # Render rain
        if rain_enabled:
            # Enable blending for rain particles
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            rain_renderer.render(proj, view, flightFrame)

            glDisable(GL_BLEND)

        pygame.display.flip()

    # Cleanup
    skybox.cleanup()
    if scene_loaded:
        scene.cleanup()

    pygame.quit()


if __name__ == '__main__':
    main()