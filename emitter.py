import numpy as np
from particle import Particle

GRAVITY = np.array([0, -15, 0], dtype=np.float32)

class ParticleEmitter:
    def __init__(self, num_particles):
        self.particles = [Particle() for _ in range(num_particles)]

    def update(self, dt):
        for p in self.particles:
            p.position += p.speed * dt
            p.speed += GRAVITY * dt * 0.12
            p.ttl -= dt
            if p.position[1] < 0 or p.ttl <= 0:
                p.reset()

    def get_positions(self):
        return np.array([p.position for p in self.particles], dtype=np.float32)
