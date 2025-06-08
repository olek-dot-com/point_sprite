# renderer.py
import ctypes
from OpenGL.GL import *
from glm import value_ptr

class Renderer:
    def __init__(self, shader, particles, atlas_tex):
        self.shader    = shader
        self.particles = particles
        self.atlas     = atlas_tex
        self._setup_vao()

    def _setup_vao(self):
        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        # pozycje
        self.posVBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.posVBO)
        glBufferData(GL_ARRAY_BUFFER, self.particles.positions.nbytes,
                     self.particles.positions, GL_DYNAMIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,0,ctypes.c_void_p(0))

        # wariant
        self.varVBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.varVBO)
        glBufferData(GL_ARRAY_BUFFER, self.particles.variants.nbytes,
                     self.particles.variants, GL_STATIC_DRAW)
        glEnableVertexAttribArray(1)
        glVertexAttribIPointer(1,1,GL_INT,0,ctypes.c_void_p(0))

        # stan
        self.stateVBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.stateVBO)
        glBufferData(GL_ARRAY_BUFFER, self.particles.states.nbytes,
                     self.particles.states, GL_DYNAMIC_DRAW)
        glEnableVertexAttribArray(2)
        glVertexAttribIPointer(2,1,GL_INT,0,ctypes.c_void_p(0))

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def render(self, proj, view, flightFrame):
        glUseProgram(self.shader)
        loc_p = glGetUniformLocation(self.shader, "u_projection")
        loc_v = glGetUniformLocation(self.shader, "u_view")
        loc_f = glGetUniformLocation(self.shader, "u_flightFrame")

        glUniformMatrix4fv(loc_p, 1, GL_FALSE, value_ptr(proj))
        glUniformMatrix4fv(loc_v, 1, GL_FALSE, value_ptr(view))
        glUniform1i(loc_f, flightFrame)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.atlas)
        glUniform1i(glGetUniformLocation(self.shader, "u_atlas"), 0)

        # update buffers
        glBindBuffer(GL_ARRAY_BUFFER, self.posVBO)
        glBufferSubData(GL_ARRAY_BUFFER, 0,
                        self.particles.positions.nbytes,
                        self.particles.positions)
        glBindBuffer(GL_ARRAY_BUFFER, self.stateVBO)
        glBufferSubData(GL_ARRAY_BUFFER, 0,
                        self.particles.states.nbytes,
                        self.particles.states)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        glBindVertexArray(self.VAO)
        glDrawArrays(GL_POINTS, 0, self.particles.positions.shape[0])
        glBindVertexArray(0)
        glUseProgram(0)