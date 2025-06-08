# scene_renderer.py
from OpenGL.GL import *
from glm import value_ptr, mat4, vec3


class SceneRenderer:
    def __init__(self, shader, scene):
        self.shader = shader
        self.scene = scene
        self.model_matrix = mat4(1.0)  # Identity matrix

        # Lighting parameters
        self.light_pos = vec3(5.0, 5.0, 10.0)
        self.light_color = vec3(1.0, 1.0, 1.0)
        self.ambient_color = vec3(0.3, 0.3, 0.4)

    def set_model_matrix(self, matrix):
        """Ustawia macierz modelu (transformacje sceny)"""
        self.model_matrix = matrix

    def set_lighting(self, light_pos=None, light_color=None, ambient_color=None):
        """Ustawia parametry oświetlenia"""
        if light_pos:
            self.light_pos = light_pos
        if light_color:
            self.light_color = light_color
        if ambient_color:
            self.ambient_color = ambient_color

    def render(self, proj_matrix, view_matrix, camera_pos):
        """Renderuje scenę"""
        glUseProgram(self.shader)

        # Ustaw uniformy
        self._set_uniforms(proj_matrix, view_matrix, camera_pos)

        # Renderuj wszystkie meshe
        for vao_data in self.scene.vao_list:
            self._render_mesh(vao_data)

        glUseProgram(0)

    def _set_uniforms(self, proj_matrix, view_matrix, camera_pos):
        """Ustawia uniformy shadera"""
        # Macierze
        proj_loc = glGetUniformLocation(self.shader, "u_projection")
        view_loc = glGetUniformLocation(self.shader, "u_view")
        model_loc = glGetUniformLocation(self.shader, "u_model")

        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, value_ptr(proj_matrix))
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, value_ptr(view_matrix))
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, value_ptr(self.model_matrix))

        # Oświetlenie
        light_pos_loc = glGetUniformLocation(self.shader, "u_lightPos")
        light_color_loc = glGetUniformLocation(self.shader, "u_lightColor")
        ambient_color_loc = glGetUniformLocation(self.shader, "u_ambientColor")
        view_pos_loc = glGetUniformLocation(self.shader, "u_viewPos")

        glUniform3fv(light_pos_loc, 1, value_ptr(self.light_pos))
        glUniform3fv(light_color_loc, 1, value_ptr(self.light_color))
        glUniform3fv(ambient_color_loc, 1, value_ptr(self.ambient_color))
        glUniform3fv(view_pos_loc, 1, value_ptr(camera_pos))

    def _render_mesh(self, vao_data):
        """Renderuje pojedynczy mesh"""
        # Ustaw kolor bazowy
        base_color_loc = glGetUniformLocation(self.shader, "u_baseColor")
        glUniform4f(base_color_loc, *vao_data['base_color'])

        # Ustaw teksturę
        has_texture_loc = glGetUniformLocation(self.shader, "u_hasTexture")
        if vao_data['texture'] is not None:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, vao_data['texture'])
            glUniform1i(glGetUniformLocation(self.shader, "u_texture"), 0)
            glUniform1i(has_texture_loc, 1)
        else:
            glUniform1i(has_texture_loc, 0)

        # Renderuj
        glBindVertexArray(vao_data['vao'])

        if vao_data['has_indices']:
            glDrawElements(GL_TRIANGLES, vao_data['count'], GL_UNSIGNED_INT, None)
        else:
            glDrawArrays(GL_TRIANGLES, 0, vao_data['count'])

        glBindVertexArray(0)

        # Odwiąż teksturę
        if vao_data['texture'] is not None:
            glBindTexture(GL_TEXTURE_2D, 0)