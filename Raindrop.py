import random
from OpenGL.GL import *


class Raindrop:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.uniform(-10, 10)
        self.y = random.uniform(5, 15)
        self.z = random.uniform(-10, 10)
        self.speed = random.uniform(0.05, 0.15)

    def update(self):
        self.y -= self.speed
        if self.y < -2:
            self.reset()

    def draw(self):
        glBegin(GL_POINTS)
        glVertex3f(self.x, self.y, self.z)
        glEnd()
