import numpy as np
import random

DROP_AREA = 18
DROP_HEIGHT = 14
MIN_TTL = 0.7
MAX_TTL = 1.5

class Particle:
    def __init__(self):
        self.position = np.zeros(3, dtype=np.float32)
        self.speed = np.zeros(3, dtype=np.float32)
        self.ttl = 0.0
        self.reset()

    def reset(self):
        self.position[0] = random.uniform(-DROP_AREA/2, DROP_AREA/2)
        self.position[1] = random.uniform(DROP_HEIGHT/1.5, DROP_HEIGHT)
        self.position[2] = random.uniform(-DROP_AREA/2, DROP_AREA/2)
        self.speed[0] = random.uniform(-1, 1)
        self.speed[1] = random.uniform(-13, -10)
        self.speed[2] = random.uniform(-1, 1)
        self.ttl = random.uniform(MIN_TTL, MAX_TTL)
