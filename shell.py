from OpenGL.GL import *
import cat

ExistShell = []
shell_map = [[[0, 0] for i in range(1000)] for j in range(1000)]

class Shell:
    def __init__(self, x, z, speed, direction):
        self.direction = direction
        self.speed = speed
        self.x = x + self.direction[0] * 30
        self.z = z + self.direction[1] * 30

    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glBegin(GL_QUADS)
        glColor4f(0.2, 0.2, 0.2, 1)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.2, 0.2, 0.2, 1])
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.2, 0.2, 0.2, 1])
        size = 3
        height = 22
        glVertex3d(size + self.x, height, size + self.z)
        glVertex3d(-size + self.x, height, size + self.z)
        glVertex3d(-size + self.x, height, -size + self.z)
        glVertex3d(size + self.x, height, -size + self.z)
        glEnd()

    def update(self):
        self.x += self.speed * self.direction[0]
        self.z += self.speed * self.direction[1]


def updating_shell(tree, mountain, base, tank1, tank2):
    for a_shell in ExistShell:
        a_shell.update()
        if a_shell.x > 500 or a_shell.x < -500 or a_shell.z > 500 or a_shell.z < -500:
            # 出界
            ExistShell.remove(a_shell)
            continue
        if tank1.in_or_out(a_shell.x, a_shell.z) and tank1.exist:
            # tank1 击中
            cat.Exist_cat.append([cat.Confused(tank1.x, tank1.z), 0])
            tank1.hit()
            ExistShell.remove(a_shell)
            continue
        if tank2.in_or_out(a_shell.x, a_shell.z) and tank2.exist:
            # tank2 击中
            cat.Exist_cat.append([cat.Confused(tank2.x, tank2.z), 0])
            tank2.hit()
            ExistShell.remove(a_shell)
            continue

        ex = True
        for t in tree:
            if t.in_or_out(a_shell.x, a_shell.z):
                t.hit()
                ex = False
                ExistShell.remove(a_shell)
                break
        if not ex:
            continue

        ex = True
        for t in mountain:
            if t.in_or_out(a_shell.x, a_shell.z):
                ex = False
                ExistShell.remove(a_shell)
                break
        if not ex:
            continue

        ex = True
        for t in base:
            if t.in_or_out(a_shell.x, a_shell.z):
                ex = False
                ExistShell.remove(a_shell)
                break
        if not ex:
            continue
        a_shell.draw()
