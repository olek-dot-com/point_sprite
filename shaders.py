# shaders.py
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from config import ATLAS_ROWS, ATLAS_COLS

VERT_SHADER = """
#version 330 core
layout(location=0) in vec3 a_pos;
layout(location=1) in int  a_variant;
layout(location=2) in int  a_state;

uniform mat4 u_projection;
uniform mat4 u_view;

flat out int v_variant;
flat out int v_state;

void main() {
    gl_Position = u_projection * u_view * vec4(a_pos, 1.0);
    gl_PointSize = 16.0;
    v_variant = a_variant;
    v_state   = a_state;
}
"""

FRAG_SHADER = f"""
#version 330 core
uniform sampler2D u_atlas;
uniform int       u_flightFrame;

flat in  int      v_variant;
flat in  int      v_state;
out      vec4     FragColor;

void main() {{
    float cellW = 1.0 / float({ATLAS_COLS});
    float cellH = 1.0 / float({ATLAS_ROWS});

    int row = (v_state >= 2) ? v_state : u_flightFrame;
    int col = v_variant;

    vec2 uvOff = vec2(cellW * float(col),
                      cellH * float(row));
    vec2 uv = uvOff + gl_PointCoord * vec2(cellW, cellH);

    vec4 c = texture(u_atlas, uv);
    if (c.a < 0.1) discard;
    FragColor = c;
}}
"""

def create_shader():
    return compileProgram(
         compileShader(VERT_SHADER, GL_VERTEX_SHADER),
         compileShader(FRAG_SHADER, GL_FRAGMENT_SHADER)
    )
