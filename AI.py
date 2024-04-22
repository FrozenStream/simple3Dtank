import tank
import numpy as np
from OpenGL.GL import *

angle = 3.1415926 / 180


def arctan(dz, dx):
    if dx != 0:
        tangle = np.arctan(dz / dx) / angle
        if dx < 0:
            if dz > 0:
                tangle += 180
            else:
                tangle -= 180
    else:
        if dz > 0:
            tangle = 90
        else:
            tangle = -90
    if tangle < 0: tangle += 360
    if tangle > 360: tangle -= 360
    return tangle


class AItank(tank.Tank):
    def __init__(self, x, z, shells, obs, bases):
        super().__init__(x, z, 0, './models/atank.obj')
        self.shells = shells
        self.bases = bases
        self.obs = obs
        self.bases = bases

    def turning(self, target_direc):
        delta = self.face_angle - target_direc
        while delta < 0: delta += 360
        while delta > 360: delta -= 360
        if 1.6 <= delta <= 90:
            self.left()
            return 0
        elif 90 <= delta <= 178.4:
            self.right()
            return 0
        elif 181.6 <= delta <= 270:
            self.left()
            return 0
        elif 270 <= delta <= 348.4:
            self.right()
            return 0
        elif 0 <= delta <= 1.6 or 348.4 <= delta <= 360:
            return 1
        elif 168.4 <= delta <= 181.6:
            return -1

    def danger(self):
        ans = [0, 0]
        for i in self.shells:
            a = arctan(i.direction[1], i.direction[0])
            b = arctan(self.z - i.z, self.x - i.x)
            if abs(a - b) >= 90: continue
            dx = i.x - self.x
            dz = i.z - self.z
            dist = (dx * dx + dz * dz) ** 0.5
            k = 1 / dist * np.sin((a - b) * angle)
            if dist * np.cos((a - b) * angle) < 300:
                if 0 < a - b < 30:
                    ans[1] += -i.direction[0] * k
                    ans[0] += i.direction[1] * k
                elif -30 < a - b < 0:
                    ans[1] += i.direction[0] * k
                    ans[0] += -i.direction[1] * k
        if ans != [0, 0]:
            return arctan(ans[1], ans[0])
        else:
            return 0

    def moving(self):
        if not self.exist: return
        closest = None
        mind = 10000000
        for i in self.bases:
            if i.owner == 2: continue
            dx = i.x - self.x
            dz = i.z - self.z
            dist = (dx * dx + dz * dz) ** 0.5
            if mind > dist:
                mind = dist
                closest = i

        to_face = arctan(closest.z - self.z, closest.x - self.x)
        f = True
        while f:
            f = False
            tempx = self.x + 100 * np.cos(to_face * angle)
            tempz = self.z + 100 * np.sin(to_face * angle)
            tempangle = to_face
            for i in self.obs:
                if i.in_or_out(tempx, tempz):
                    f = True
                    tempangle = arctan(i.z - self.z, i.x - self.x)
                    break

            print('\r' + str(tempangle), end='')
            if tempangle - to_face > 2:
                to_face -= 5
            elif tempangle - to_face < -2:
                to_face += 5
        # 判断是否指向障碍

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslated(self.x + 100 * np.cos(to_face * angle), 10, self.z + 100 * np.sin(to_face * angle))
        glRotated(90, 1, 0, 0)
        glRotated(30, 0, 0, 1)
        glRotated(-40, 1, 0, 0)
        glBegin(GL_TRIANGLES)
        glVertex3f(-10, 0, -10)
        glVertex3f(10, 0, -10)
        glVertex3f(0, 0, 10)
        glEnd()

        danger = self.danger()
        if danger:
            a = self.turning(danger)
            if a == 1:
                self.up()
            elif a == -1:
                self.down()
        else:

            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            glTranslated(self.x + 100 * np.cos(to_face * angle), 10, self.z + 100 * np.sin(to_face * angle))
            glRotated(90, 1, 0, 0)
            glRotated(30, 0, 0, 1)
            glRotated(-40, 1, 0, 0)
            glBegin(GL_TRIANGLES)
            glVertex3f(-10, 0, -10)
            glVertex3f(10, 0, -10)
            glVertex3f(0, 0, 10)
            glEnd()

            a = self.turning(to_face)
            if a == 1:
                self.up()
            elif a == -1:
                self.down()
