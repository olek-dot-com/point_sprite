import numpy as np
from config import *

class ParticleSystem:
    def __init__(self):
        self.positions      = np.zeros((NUM_PARTICLES, 3), dtype=np.float32)
        self.velocities     = np.zeros((NUM_PARTICLES, 3), dtype=np.float32)
        self.variants       = np.random.randint(0, ATLAS_COLS,
                                            size=NUM_PARTICLES,
                                            dtype=np.int32)
        self.states         = np.zeros(NUM_PARTICLES, dtype=np.int32)
        self.timers         = np.zeros(NUM_PARTICLES, dtype=np.float32)
        # Timer for toggling flight state between 0 and 1
        self.flight_timers  = np.zeros(NUM_PARTICLES, dtype=np.float32)
        self.init_particles()

    def init_particles(self):
        # Randomize spawn positions
        self.positions[:,0] = np.random.uniform(X_MIN, X_MAX, NUM_PARTICLES)
        self.positions[:,1] = np.random.uniform(Y_MIN, Y_MAX, NUM_PARTICLES)
        self.positions[:,2] = np.random.uniform(Z_SPAWN,
                                              Z_SPAWN + Z_HEIGHT,
                                              NUM_PARTICLES)
        # Initial downward velocity
        self.velocities[:]    = (0.0, 0.0, -RAIN_SPEED)
        # Start all particles in flight frame 0
        self.states[:]        = 0
        self.timers[:]        = 0.0
        self.flight_timers[:] = 0.0

    def update(self, dt):
        # 1) Toggle flight state (0 <-> 1) for particles in flight (state < 2)
        flight_mask = (self.states < 2)
        self.flight_timers[flight_mask] += dt
        toggle = flight_mask & (self.flight_timers >= FLIGHT_FRAME_T)
        if np.any(toggle):
            # Reduce timer and flip state
            self.flight_timers[toggle] -= FLIGHT_FRAME_T
            self.states[toggle] = 1 - self.states[toggle]

        # 2) Move particles still in flight (state 0 or 1)
        flight = (self.states < 2)
        prev_z = self.positions[:,2].copy()
        self.positions[flight, 2] += self.velocities[flight, 2] * dt

        # 3) Detect hit on ground and enter splat phase (state 2)
        hit = flight & (prev_z >= Z_GROUND) & (self.positions[:,2] < Z_GROUND)
        if np.any(hit):
            self.states[hit]         = 2
            self.timers[hit]         = SPLAT_TIME
            self.positions[hit, 2]   = Z_GROUND
            self.flight_timers[hit]  = 0.0

        # 4) Decrement timers for splat phases and handle transition 2->3
        splat_mask = (self.states >= 2)
        if np.any(splat_mask):
            self.timers[splat_mask] -= dt
            # Transition from phase2 (state 2) to splash (state 3)
            to_splash = splat_mask & (self.states == 2) & (self.timers <= HALF_SPLAT)
            if np.any(to_splash):
                self.states[to_splash] = 3

        # 5) After splat animation ends (timer <= 0), reset particle
        done = (self.states >= 2) & (self.timers <= 0.0)
        if np.any(done):
            cnt = np.count_nonzero(done)
            self.positions[done,0]     = np.random.uniform(X_MIN, X_MAX, cnt)
            self.positions[done,1]     = np.random.uniform(Y_MIN, Y_MAX, cnt)
            self.positions[done,2]     = np.random.uniform(Z_SPAWN, Z_SPAWN + Z_HEIGHT, cnt)
            self.velocities[done,2]    = -RAIN_SPEED
            self.states[done]          = 0
            self.timers[done]          = 0.0
            self.flight_timers[done]   = 0.0
