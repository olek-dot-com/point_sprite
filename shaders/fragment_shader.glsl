#version 330
uniform sampler2D spriteTex;
out vec4 fragColor;
void main()
{
    fragColor = texture(spriteTex, gl_PointCoord);
    if (fragColor.a < 0.1) discard; // przezroczystość tła
}
