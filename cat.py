from OpenGL.GL import *
import random as rnd

Exist_cat = []
angle = 3.8159265 / 180
r = [24, 22, 20, 18, 16, 15, 14, 13, 12]
a = [[1, 16], [1, 16], [2, 12], [2, 12], [2, 8], [2, 8], [3, 7], [3, 7]]


def piece(size):
    h = 20
    glBegin(GL_POLYGON)
    glVertex3f(-12 * size, h, 0)
    glVertex3f(0, h, 10 * size)
    glVertex3f(12 * size, h, 0)
    glVertex3f(8 * size, h, -10 * size)
    glVertex3f(-8 * size, h, -10 * size)
    glEnd()


class Confused:
    def __init__(self, x, z):
        self.x = x
        self.z = z

    def draw(self, size):
        glMaterialfv(GL_FRONT, GL_AMBIENT, [1, 1, 1, 0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [1, 1, 1, 0])
        glNormal3fv([0, 1, 0])
        glMatrixMode(GL_MODELVIEW)
        de = 0.7
        for i in range(size):
            trans = (a[i][0] * 20 + int(100 * rnd.random()) % (size * 4)) / 4
            for k in range(6):
                glLoadIdentity()
                glTranslated(self.x + trans, a[i][1] / 4 * 10, self.z + de * trans)
                glRotated(90, 1, 0, 0)
                glRotated(35, 0, 0, 1)
                glRotated(-50, 1, 0, 0)
                glRotated(i, 0, 1, 0)
                piece(r[i] / 10 - 0.4)

                glLoadIdentity()
                glTranslated(self.x - trans, a[i][1] / 4 * 10, self.z - de * trans)
                glRotated(90, 1, 0, 0)
                glRotated(35, 0, 0, 1)
                glRotated(-50, 1, 0, 0)
                glRotated(i, 0, 1, 0)
                piece(r[i] / 10 - 0.4)


def update_cat():
    for cat in Exist_cat:
        cat[0].draw(cat[1] // 4)
        cat[1] += 1
        if cat[1] == 32:
            Exist_cat.remove(cat)
