# scene_shaders.py
from OpenGL.GL import GL_VERTEX_SHADER, GL_FRAGMENT_SHADER
from OpenGL.GL.shaders import compileProgram, compileShader

SCENE_VERT_SHADER = """
#version 330 core
layout(location=0) in vec3 a_position;
layout(location=1) in vec3 a_normal;
layout(location=2) in vec2 a_texCoord;

uniform mat4 u_projection;
uniform mat4 u_view;
uniform mat4 u_model;
uniform vec3 u_lightPos;
uniform vec3 u_viewPos;

out vec3 v_worldPos;
out vec3 v_normal;
out vec2 v_texCoord;
out vec3 v_lightDir;
out vec3 v_viewDir;

void main() {
    vec4 worldPos = u_model * vec4(a_position, 1.0);
    v_worldPos = worldPos.xyz;

    // Transform normal to world space
    v_normal = normalize(mat3(transpose(inverse(u_model))) * a_normal);

    v_texCoord = a_texCoord;

    // Calculate lighting vectors
    v_lightDir = normalize(u_lightPos - v_worldPos);
    v_viewDir = normalize(u_viewPos - v_worldPos);

    gl_Position = u_projection * u_view * worldPos;
}
"""

SCENE_FRAG_SHADER = """
#version 330 core
in vec3 v_worldPos;
in vec3 v_normal;
in vec2 v_texCoord;
in vec3 v_lightDir;
in vec3 v_viewDir;

uniform sampler2D u_texture;
uniform bool u_hasTexture;
uniform vec4 u_baseColor;
uniform vec3 u_lightColor;
uniform vec3 u_ambientColor;

out vec4 FragColor;

void main() {
    vec3 normal = normalize(v_normal);

    // Base color from texture or material
    vec4 baseColor = u_baseColor;
    if (u_hasTexture) {
        vec4 texColor = texture(u_texture, v_texCoord);
        baseColor *= texColor;
    }

    // Ambient lighting
    vec3 ambient = u_ambientColor * baseColor.rgb;

    // Diffuse lighting
    float diff = max(dot(normal, v_lightDir), 0.0);
    vec3 diffuse = diff * u_lightColor * baseColor.rgb;

    // Specular lighting (simple Phong)
    vec3 reflectDir = reflect(-v_lightDir, normal);
    float spec = pow(max(dot(v_viewDir, reflectDir), 0.0), 32.0);
    vec3 specular = spec * u_lightColor * 0.3;

    vec3 result = ambient + diffuse + specular;
    FragColor = vec4(result, baseColor.a);
}
"""


def create_scene_shader():
    """Tworzy shader program do renderowania sceny"""
    return compileProgram(
        compileShader(SCENE_VERT_SHADER, GL_VERTEX_SHADER),
        compileShader(SCENE_FRAG_SHADER, GL_FRAGMENT_SHADER)
    )