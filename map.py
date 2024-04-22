from OpenGL.GL import *
import OBJLoad
import numpy as np


def xyz():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glBegin(GL_LINES)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [1, 0, 0, 1])
    glMaterialfv(GL_FRONT, GL_AMBIENT, [1, 0, 0, 1])
    glVertex3d(0, 0, 0)
    glVertex3d(1000, 0, 0)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0, 1, 0, 1])
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0, 1, 0, 1])
    glVertex3d(0, 0, 0)
    glVertex3d(0, 1000, 0)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0, 0, 1, 1])
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0, 0, 1, 1])
    glVertex3d(0, 0, 0)
    glVertex3d(0, 0, 1000)
    glEnd()

class Title3:
    def __init__(self, obj_source):
        self.title = OBJLoad.ObjLoad2(obj_source)
        self.title_list = -1

    def draw(self):
        if not glIsList(self.title_list):
            self.title_list = glGenLists(1)
            glNewList(self.title_list, GL_COMPILE)
            pre_mtl = self.title.face[0][0]
            glMaterialfv(GL_FRONT, GL_AMBIENT, self.title.mtl_dic[pre_mtl]['Ka'])
            glMaterialfv(GL_FRONT, GL_DIFFUSE, self.title.mtl_dic[pre_mtl]['Kd'])
            glBegin(GL_TRIANGLES)
            for single_f in self.title.face:
                glNormal3fv(self.title.points_vn[single_f[1][1] - 1])
                glVertex3f(*self.title.points_v[single_f[1][0] - 1])

                glNormal3fv(self.title.points_vn[single_f[2][1] - 1])
                glVertex3f(*self.title.points_v[single_f[2][0] - 1])

                glNormal3fv(self.title.points_vn[single_f[3][1] - 1])
                glVertex3f(*self.title.points_v[single_f[3][0] - 1])
            glEnd()
            glEndList()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslated(0, 100, 0)
        glRotated(90, 1, 0, 0)
        glRotated(30, 0, 0, 1)
        glRotated(-40, 1, 0, 0)
        glScaled(2, 2, 2)
        glCallLists(self.title_list)

    def __del__(self):
        glDeleteLists(self.title_list, 1)

class Title2:
    def __init__(self, obj_source):
        self.title = OBJLoad.ObjLoad2(obj_source)
        self.title_list = -1

    def draw(self, x, z, size):
        if not glIsList(self.title_list):
            self.title_list = glGenLists(1)
            glNewList(self.title_list, GL_COMPILE)
            pre_mtl = self.title.face[0][0]
            glMaterialfv(GL_FRONT, GL_AMBIENT, self.title.mtl_dic[pre_mtl]['Ka'])
            glMaterialfv(GL_FRONT, GL_DIFFUSE, self.title.mtl_dic[pre_mtl]['Kd'])
            glBegin(GL_TRIANGLES)
            for single_f in self.title.face:
                glNormal3fv(self.title.points_vn[single_f[1][1] - 1])
                glVertex3f(*self.title.points_v[single_f[1][0] - 1])

                glNormal3fv(self.title.points_vn[single_f[2][1] - 1])
                glVertex3f(*self.title.points_v[single_f[2][0] - 1])

                glNormal3fv(self.title.points_vn[single_f[3][1] - 1])
                glVertex3f(*self.title.points_v[single_f[3][0] - 1])
            glEnd()
            glEndList()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glRotated(90, 1, 0, 0)
        glTranslated(x, 0, z)
        glRotated(10, 1, 0, 1)
        glScaled(size, size, size)
        glCallLists(self.title_list)

    def __del__(self):
        glDeleteLists(self.title_list, 1)


class Title1:
    def __init__(self, obj_source):
        self.title = OBJLoad.ObjLoad1(obj_source)
        self.title_list = -1

    def draw(self, x, z, size):
        if not glIsList(self.title_list):
            self.title_list = glGenLists(1)
            glNewList(self.title_list, GL_COMPILE)
            pre_mtl = self.title.face[0][0]
            glMaterialfv(GL_FRONT, GL_AMBIENT, self.title.mtl_dic[pre_mtl]['Ka'])
            glMaterialfv(GL_FRONT, GL_DIFFUSE, self.title.mtl_dic[pre_mtl]['Kd'])
            glBegin(GL_TRIANGLES)
            for single_f in self.title.face:
                glNormal3fv(self.title.points_vn[single_f[1][1] - 1])
                glVertex3f(*self.title.points_v[single_f[1][0] - 1])

                glNormal3fv(self.title.points_vn[single_f[2][1] - 1])
                glVertex3f(*self.title.points_v[single_f[2][0] - 1])

                glNormal3fv(self.title.points_vn[single_f[3][1] - 1])
                glVertex3f(*self.title.points_v[single_f[3][0] - 1])
            glEnd()
            glEndList()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glRotated(90, 1, 0, 0)
        glTranslated(x, 0, z)
        glRotated(10, 1, 0, 1)
        glScaled(size, size, size)
        glCallLists(self.title_list)

    def __del__(self):
        glDeleteLists(self.title_list, 1)


tree = []
mountain = []
base = []
force = [[[0, 0] for i in range(1000)] for i in range(1000)]


def check_winner():
    global base
    a = 0
    b = 0
    for i in base:
        if i.owner == 1: a += 1
        if i.owner == 2: b += 1
    if a == 0 or b == 0:
        return True
    else: return False


class Obj:
    def __init__(self, obj_source, x, y, z, up, r):
        self.tree = OBJLoad.ObjLoad1(obj_source)
        self.obj_list = -1
        self.x = x
        self.y = y
        self.z = z
        self.up = up
        self.r = r

    def force_position(self, force):
        angle = 3.14159265 / 180
        for r in range(self.r - 10, self.r):
            p = None
            for a in range(360):
                temp_p = [int(r * np.cos(a * angle) + 0.5), int(r * np.sin(a * angle) + 0.5)]
                if p != temp_p:
                    p = temp_p
                    force[500 + self.x + p[0]][500 + self.z + p[1]][0] = p[0]
                    force[500 + self.x + p[0]][500 + self.z + p[1]][1] = p[1]

    def draw(self):
        if not glIsList(self.obj_list):
            self.obj_list = glGenLists(1)
            glNewList(self.obj_list, GL_COMPILE)
            glMatrixMode(GL_MODELVIEW)
            pre_mtl = None
            glBegin(GL_TRIANGLES)
            for single_f in self.tree.face:
                if single_f[0] != pre_mtl:
                    pre_mtl = single_f[0]
                    glMaterialfv(GL_FRONT, GL_AMBIENT, self.tree.mtl_dic[pre_mtl]['Ka'])
                    glMaterialfv(GL_FRONT, GL_DIFFUSE, self.tree.mtl_dic[pre_mtl]['Kd'])
                    glMaterialfv(GL_FRONT, GL_SPECULAR, self.tree.mtl_dic[pre_mtl]['Ks'])
                    glMaterialfv(GL_FRONT, GL_SHININESS, self.tree.mtl_dic[pre_mtl]['Ns'])

                glNormal3fv(self.tree.points_vn[single_f[1][2] - 1])
                glVertex3f(*self.tree.points_v[single_f[1][0] - 1])

                glNormal3fv(self.tree.points_vn[single_f[2][2] - 1])
                glVertex3f(*self.tree.points_v[single_f[2][0] - 1])

                glNormal3fv(self.tree.points_vn[single_f[3][2] - 1])
                glVertex3f(*self.tree.points_v[single_f[3][0] - 1])
            glEnd()
            glEndList()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslated(self.x, self.y, self.z)
        glScaled(self.up, self.up, self.up)
        glCallLists(self.obj_list)

    def in_or_out(self, x, z):
        delta_p = [x - self.x, z - self.z]
        delta = delta_p[0] ** 2 + delta_p[1] ** 2
        if delta <= self.r ** 2:
            return True
        else:
            return False


class Tree(Obj):
    def __init__(self, obj_source, x, y, z, up, r):
        super().__init__(obj_source, x, y, z, up, r)
        self.health = 100

    def draw(self):
        if not glIsList(self.obj_list):
            self.obj_list = glGenLists(1)
            glNewList(self.obj_list, GL_COMPILE)
            glMatrixMode(GL_MODELVIEW)
            glTranslated(0, 1, 0)
            glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.45, 0.45, 0.45, 0])
            glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.45, 0.45, 0.45, 0])
            glNormal3fv([0, -1, 0])
            glBegin(GL_POLYGON)
            glVertex3f(28, 0, 0)
            glVertex3f(24.249, 0, -14)
            glVertex3f(14, 0, -24.249)
            glVertex3f(0, 0, -28)
            glVertex3f(-14, 0, -24.249)
            glVertex3f(-24.249, 0, -14)
            glVertex3f(-28, 0, 0)
            glVertex3f(-24.249, 0, 14)
            glVertex3f(-14, 0, 24.249)
            glVertex3f(0, 0, 28)
            glVertex3f(14, 0, 24.249)
            glVertex3f(24.249, 0, 14)
            glEnd()
            # 假装阴影

            glMatrixMode(GL_MODELVIEW)
            glTranslated(0, -2, 0)
            pre_mtl = None
            glBegin(GL_TRIANGLES)
            for single_f in self.tree.face:
                if single_f[0] != pre_mtl:
                    pre_mtl = single_f[0]
                    glMaterialfv(GL_FRONT, GL_AMBIENT, self.tree.mtl_dic[pre_mtl]['Ka'])
                    glMaterialfv(GL_FRONT, GL_DIFFUSE, self.tree.mtl_dic[pre_mtl]['Kd'])
                    glMaterialfv(GL_FRONT, GL_SPECULAR, self.tree.mtl_dic[pre_mtl]['Ks'])
                    glMaterialfv(GL_FRONT, GL_SHININESS, self.tree.mtl_dic[pre_mtl]['Ns'])

                glNormal3fv(self.tree.points_vn[single_f[1][2] - 1])
                glVertex3f(*self.tree.points_v[single_f[1][0] - 1])

                glNormal3fv(self.tree.points_vn[single_f[2][2] - 1])
                glVertex3f(*self.tree.points_v[single_f[2][0] - 1])

                glNormal3fv(self.tree.points_vn[single_f[3][2] - 1])
                glVertex3f(*self.tree.points_v[single_f[3][0] - 1])
            glEnd()
            glEndList()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslated(self.x, self.y, self.z)
        glScaled(self.up, self.up, self.up)
        glCallLists(self.obj_list)
        self.he_table()

    def hit(self):
        self.health -= 20
        if self.health <= 0:
            self.destroyed()

    def destroyed(self):
        global force
        global tree
        angle = 3.14159265 / 180
        for r in range(self.r - 10, self.r):
            p = None
            for a in range(360):
                temp_p = [int(r * np.cos(a * angle) + 0.5), int(r * np.sin(a * angle) + 0.5)]
                if p != temp_p:
                    p = temp_p
                    force[500 + self.x + p[0]][500 + self.z + p[1]][0] = 0
                    force[500 + self.x + p[0]][500 + self.z + p[1]][1] = 0
        tree.remove(self)

    def he_table(self):
        if self.health != 100:
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            glTranslated(self.x, 160, self.z)
            glRotated(90, 1, 0, 0)
            glRotated(30, 0, 0, 1)
            glRotated(-40, 1, 0, 0)
            # 旋转
            size_h = 8
            size_w = 50
            height = 0
            glLineWidth(3)
            glNormal3fv([0, 1, 0])
            glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.6, 0.6, 0.6, 1])
            glBegin(GL_LINE_LOOP)
            glVertex3d(size_w, height, size_h)
            glVertex3d(-size_w, height, size_h)
            glVertex3d(-size_w, height, -size_h)
            glVertex3d(size_w, height, -size_h)
            glEnd()
            w = size_w - 1
            h = size_h - 1
            glBegin(GL_QUADS)
            glMaterialfv(GL_FRONT, GL_DIFFUSE, [1, 0.6, 0.6, 1])
            glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [1, 0.6, 0.6, 1])
            glVertex3d(-w + (2 * w * self.health / 100), height, h)
            glVertex3d(-w, height, h)
            glVertex3d(-w, height, -h)
            glVertex3d(-w + (2 * w * self.health / 100), height, -h)
            glEnd()


class Base:
    def __init__(self, x, z, up, r, owner):
        self.base1 = OBJLoad.ObjLoad1('./models/base1.obj')
        self.base2 = OBJLoad.ObjLoad1('./models/base2.obj')
        self.base3 = OBJLoad.ObjLoad1('./models/empty_base.obj')
        self.base1_list = -1
        self.base2_list = -1
        self.base0_list = -1
        self.x = x
        self.z = z
        self.up = up
        self.r = r
        self.owner = owner

    def force_position(self, force):
        angle = 3.14159265 / 180
        for r in range(self.r - 10, self.r):
            p = None
            for a in range(360):
                temp_p = [int(r * np.cos(a * angle) + 0.5), int(r * np.sin(a * angle) + 0.5)]
                if p != temp_p:
                    p = temp_p
                    force[500 + self.x + p[0]][500 + self.z + p[1]][0] = p[0]
                    force[500 + self.x + p[0]][500 + self.z + p[1]][1] = p[1]

    def near(self, x, z):
        tx = self.x - x
        tz = self.z - z
        if tx * tx + tz * tz <= 4 * self.r * self.r:
            return True
        else:
            return False

    def in_or_out(self, x, z):
        delta_p = [x - self.x, z - self.z]
        delta = delta_p[0] ** 2 + delta_p[1] ** 2
        if delta <= self.r ** 2:
            return True
        else:
            return False

    def draw(self):
        if not glIsList(self.base1_list):
            self.base1_list = glGenLists(1)
            glNewList(self.base1_list, GL_COMPILE)
            glMatrixMode(GL_MODELVIEW)
            pre_mtl = None
            glBegin(GL_TRIANGLES)
            for single_f in self.base1.face:
                if single_f[0] != pre_mtl:
                    pre_mtl = single_f[0]
                    glMaterialfv(GL_FRONT, GL_AMBIENT, self.base1.mtl_dic[pre_mtl]['Ka'])
                    glMaterialfv(GL_FRONT, GL_DIFFUSE, self.base1.mtl_dic[pre_mtl]['Kd'])
                    glMaterialfv(GL_FRONT, GL_SPECULAR, self.base1.mtl_dic[pre_mtl]['Ks'])
                    glMaterialfv(GL_FRONT, GL_SHININESS, self.base1.mtl_dic[pre_mtl]['Ns'])

                glNormal3fv(self.base1.points_vn[single_f[1][2] - 1])
                glVertex3f(*self.base1.points_v[single_f[1][0] - 1])

                glNormal3fv(self.base1.points_vn[single_f[2][2] - 1])
                glVertex3f(*self.base1.points_v[single_f[2][0] - 1])

                glNormal3fv(self.base1.points_vn[single_f[3][2] - 1])
                glVertex3f(*self.base1.points_v[single_f[3][0] - 1])
            glEnd()
            glEndList()
        if not glIsList(self.base2_list):
            self.base2_list = glGenLists(1)
            glNewList(self.base2_list, GL_COMPILE)
            glMatrixMode(GL_MODELVIEW)
            pre_mtl = None
            glBegin(GL_TRIANGLES)
            for single_f in self.base2.face:
                if single_f[0] != pre_mtl:
                    pre_mtl = single_f[0]
                    glMaterialfv(GL_FRONT, GL_AMBIENT, self.base2.mtl_dic[pre_mtl]['Ka'])
                    glMaterialfv(GL_FRONT, GL_DIFFUSE, self.base2.mtl_dic[pre_mtl]['Kd'])
                    glMaterialfv(GL_FRONT, GL_SPECULAR, self.base2.mtl_dic[pre_mtl]['Ks'])
                    glMaterialfv(GL_FRONT, GL_SHININESS, self.base2.mtl_dic[pre_mtl]['Ns'])

                glNormal3fv(self.base2.points_vn[single_f[1][2] - 1])
                glVertex3f(*self.base2.points_v[single_f[1][0] - 1])

                glNormal3fv(self.base2.points_vn[single_f[2][2] - 1])
                glVertex3f(*self.base2.points_v[single_f[2][0] - 1])

                glNormal3fv(self.base2.points_vn[single_f[3][2] - 1])
                glVertex3f(*self.base2.points_v[single_f[3][0] - 1])
            glEnd()
            glEndList()
        if not glIsList(self.base0_list):
            self.base0_list = glGenLists(1)
            glNewList(self.base0_list, GL_COMPILE)
            glMatrixMode(GL_MODELVIEW)
            pre_mtl = None
            glBegin(GL_TRIANGLES)
            for single_f in self.base3.face:
                if single_f[0] != pre_mtl:
                    pre_mtl = single_f[0]
                    glMaterialfv(GL_FRONT, GL_AMBIENT, self.base3.mtl_dic[pre_mtl]['Ka'])
                    glMaterialfv(GL_FRONT, GL_DIFFUSE, self.base3.mtl_dic[pre_mtl]['Kd'])
                    glMaterialfv(GL_FRONT, GL_SPECULAR, self.base3.mtl_dic[pre_mtl]['Ks'])
                    glMaterialfv(GL_FRONT, GL_SHININESS, self.base3.mtl_dic[pre_mtl]['Ns'])

                glNormal3fv(self.base3.points_vn[single_f[1][2] - 1])
                glVertex3f(*self.base3.points_v[single_f[1][0] - 1])

                glNormal3fv(self.base3.points_vn[single_f[2][2] - 1])
                glVertex3f(*self.base3.points_v[single_f[2][0] - 1])

                glNormal3fv(self.base3.points_vn[single_f[3][2] - 1])
                glVertex3f(*self.base3.points_v[single_f[3][0] - 1])
            glEnd()
            glEndList()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslated(self.x, 0, self.z)
        glScaled(self.up, self.up, self.up)
        if self.owner == 1:
            glCallLists(self.base1_list)
        elif self.owner == 2:
            glCallLists(self.base2_list)
        elif self.owner == 0:
            glCallLists(self.base0_list)


class Map:
    def __init__(self, map_number):
        self.plant = None
        if map_number == 1:
            self.grassland()

    def grassland(self):
        global force
        global tree
        global mountain
        trees_position = [[300, 0],
                          [400, 300],
                          [-200, -400],
                          [400, 200],
                          [-200, 300],
                          [-300, -200],
                          [200, -300]]
        mountain_position = [[100, 200],
                             [-100, -200]]
        base_position = [[-400, 100],
                         [400, -100]]
        self.plant = Obj('./models/plant.obj', 0, -10, 0, 1, 0)
        for position in trees_position:
            tree.append(Tree('./models/tree.obj', position[0], 0, position[1], 1, 12))
            tree[-1].force_position(force)

        for position in mountain_position:
            mountain.append(Obj('./models/mountain.obj', position[0], 0, position[1], 2, 100))
            mountain[-1].force_position(force)

        base.append(Base(-400, -400, 0.5, 35, 1))
        base[-1].force_position(force)
        base.append(Base(400, 400, 0.5, 35, 2))
        base[-1].force_position(force)

        for position in base_position:
            base.append(Base(position[0], position[1], 0.5, 35, 2))
            base[-1].force_position(force)

        self.river = glGenLists(1)
        self.ar = glGenLists(1)

        glNewList(self.river, GL_COMPILE)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.4, 0.4, 1.0, 0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.2, 0.2, 0.2, 0])
        glNormal3fv([0, 1, 0])
        glBegin(GL_QUADS)
        glVertex3f(-500, 1, 500)
        glVertex3f(-500, 1, 400)
        glVertex3f(-100, 1, 0)
        glVertex3f(0, 1, 0)

        glVertex3f(500, 1, -500)
        glVertex3f(500, 1, -400)
        glVertex3f(100, 1, 0)
        glVertex3f(0, 1, 0)

        glVertex3f(-150, 1, 50)
        glVertex3f(-50, 1, -50)
        glVertex3f(150, 1, -50)
        glVertex3f(50, 1, 50)
        glEnd()
        glEndList()
        # 河流创建

        glNewList(self.ar, GL_COMPILE)
        glBegin(GL_QUADS)
        glVertex3f(20, 10, 4)
        glVertex3f(20, 10, -4)
        glVertex3f(-20, 10, -4)
        glVertex3f(-20, 10, 4)
        glEnd()
        glBegin(GL_TRIANGLES)
        glVertex3f(20, 10, 10)
        glVertex3f(30, 10, 0)
        glVertex3f(20, 10, -10)
        glEnd()
        glEndList()
        # 箭头创建

        for i in range(1000):
            for j in range(1, 10):
                force[i][1000 - j][1] = -10 + j
                force[i][j][1] = 10 - j
                force[j][i][0] = 10 - j
                force[1000 - j][i][0] = -10 + j
        # 边缘碰撞
        for x in range(1000):
            for z in range(1000):
                if 10 < x <= 450 and 900 - z < x < 1000 - z:
                    force[x][z] = [0.03, -0.03]
                if 990 > x >= 550 and 1000 - z < x < 1100 - z:
                    force[x][z] = [0.03, -0.03]
                if 450 <= x <= 550 and 450 <= z <= 550:
                    force[x][z] = [0.03, 0]
        # 河流推动

    def base_update(self, tank1, tank2):
        global base
        for b in base:
            owner = 0
            if b.near(tank1.x, tank1.z):
                if owner == 0:
                    owner = 1
                elif owner == 2:
                    owner = 3
            if b.near(tank2.x, tank2.z):
                if owner == 0:
                    owner = 2
                elif owner == 1:
                    owner = 3
            if owner == 1:
                b.owner = 1
            elif owner == 2:
                b.owner = 2
            elif owner == 3:
                b.owner = 0

    def draw(self):
        self.plant.draw()
        for t in tree:
            t.draw()
        for t in mountain:
            t.draw()
        for t in base:
            t.draw()

        glCallLists(self.river)
        # 河流
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [1, 1, 1, 1])
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [1, 1, 1, 1])
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glRotated(45, 0, 1, 0)
        glTranslated(-300, 0, -35)
        glCallList(self.ar)
        glLoadIdentity()
        glRotated(45, 0, 1, 0)
        glTranslated(300, 0, 35)
        glCallList(self.ar)
        glLoadIdentity()
        glCallList(self.ar)
        # 河流箭头
