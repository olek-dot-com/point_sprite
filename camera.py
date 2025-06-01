import numpy as np

def look_at(eye, target, up):
    f = target - eye
    f = f / np.linalg.norm(f)
    u = up / np.linalg.norm(up)
    s = np.cross(f, u)
    s = s / np.linalg.norm(s)
    u = np.cross(s, f)

    m = np.identity(4, dtype=np.float32)
    m[0, :3] = s
    m[1, :3] = u
    m[2, :3] = -f
    m[0, 3] = -np.dot(s, eye)
    m[1, 3] = -np.dot(u, eye)
    m[2, 3] = np.dot(f, eye)
    return m

def perspective(fovy, aspect, znear, zfar):
    f = 1.0 / np.tan(np.radians(fovy) / 2)
    m = np.zeros((4, 4), dtype=np.float32)
    m[0, 0] = f / aspect
    m[1, 1] = f
    m[2, 2] = (zfar + znear) / (znear - zfar)
    m[2, 3] = (2 * zfar * znear) / (znear - zfar)
    m[3, 2] = -1.0
    return m

class OrbitCamera:
    def __init__(self, distance=22, angle_az=50, angle_el=45):
        self.angle = [angle_az, angle_el]
        self.distance = distance

    def get_view_matrix(self):
        x = self.distance * np.sin(np.radians(self.angle[0])) * np.cos(np.radians(self.angle[1]))
        y = self.distance * np.sin(np.radians(self.angle[1]))
        z = self.distance * np.cos(np.radians(self.angle[0])) * np.cos(np.radians(self.angle[1]))
        eye = np.array([x, y, z], dtype=np.float32)
        target = np.array([0, 4, 0], dtype=np.float32)
        up = np.array([0, 1, 0], dtype=np.float32)
        return look_at(eye, target, up)

    def get_projection_matrix(self, width, height):
        return perspective(60, width / height, 0.1, 100.0)

    def process_mouse(self, dx, dy):
        self.angle[0] += dx * 0.5
        self.angle[1] -= dy * 0.5
        self.angle[1] = np.clip(self.angle[1], -89, 89)

    def zoom(self, dz):
        self.distance += dz
        if self.distance < 5: self.distance = 5
        if self.distance > 60: self.distance = 60
