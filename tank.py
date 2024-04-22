from OpenGL.GL import *
import shell
import numpy as np
import OBJLoad
import winsound

angle = 3.1415926 / 180


class Tank:
    def __init__(self, x, z, face_angle, objsource):
        self.view = 50
        self.tank = OBJLoad.ObjLoad1(objsource)
        self.turning_speed = 3
        self.width = 15
        self.length = 25
        self.born_x = x
        self.born_z = z
        self.x = x
        self.z = z
        self.face_angle = face_angle
        self.front_direct = [np.cos(face_angle * angle), np.sin(face_angle * angle)]
        self.left_direct = [-np.sin(face_angle * angle), np.cos(face_angle * angle)]
        self.speed = [0, 0]
        self.force = [0, 0]
        self.an = 0
        self.max_speed = 3
        self.shell_speed = 4
        self.fire_cold = 0.5
        self.fire_counter = 0
        self.reborn_cold = 2
        self.reborn_counter = 0
        self.exist = True
        self.shadow_list = -1
        self.tank_list = -1

    def draw(self):
        if not glIsList(self.shadow_list):
            self.shadow_list = glGenLists(1)
            glNewList(self.shadow_list, GL_COMPILE)
            glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.45, 0.45, 0.45, 0])
            glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.45, 0.45, 0.45, 0])
            glNormal3fv([0, -1, 0])
            glBegin(GL_QUADS)
            h = -18
            glVertex3f(self.length, h, self.width)
            glVertex3f(self.length, h, self.width - 8)
            glVertex3f(-self.length, h, self.width - 8)
            glVertex3f(-self.length, h, self.width)

            glVertex3f(self.length, h, -self.width)
            glVertex3f(self.length, h, -self.width + 8)
            glVertex3f(-self.length, h, -self.width + 8)
            glVertex3f(-self.length, h, -self.width)

            glVertex3f(self.length - 10, h, self.width - 8)
            glVertex3f(self.length - 10, h, -self.width + 8)
            glVertex3f(-self.length + 4, h, -self.width + 8)
            glVertex3f(-self.length + 4, h, self.width - 8)
            glEnd()
            glEndList()
        # 假装阴影设置
        if not glIsList(self.tank_list):
            self.tank_list = glGenLists(1)
            glNewList(self.tank_list, GL_COMPILE)
            pre_mtl = self.tank.face[0][0]
            glMaterialfv(GL_FRONT, GL_AMBIENT, self.tank.mtl_dic[pre_mtl]['Ka'])
            glMaterialfv(GL_FRONT, GL_DIFFUSE, self.tank.mtl_dic[pre_mtl]['Kd'])
            glBegin(GL_TRIANGLES)
            for single_f in self.tank.face:
                glNormal3fv(self.tank.points_vn[single_f[1][2] - 1])
                glVertex3f(*self.tank.points_v[single_f[1][0] - 1])

                glNormal3fv(self.tank.points_vn[single_f[2][2] - 1])
                glVertex3f(*self.tank.points_v[single_f[2][0] - 1])

                glNormal3fv(self.tank.points_vn[single_f[3][2] - 1])
                glVertex3f(*self.tank.points_v[single_f[3][0] - 1])
            glEnd()
            glEndList()
        # 本体设置
        an = self.face_angle * angle
        arr1 = np.array([[np.cos(an), 0, np.sin(an), 0],
                         [0, 1, 0, 0],
                         [-np.sin(an), 0, np.cos(an), 0],
                         [0, 0, 0, 1]])
        arr2 = np.array([[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 1, 0],
                         [self.x, 20, self.z, 1]])
        arr = arr1.dot(arr2)
        # 计算位置
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glMultMatrixd(arr)
        # 平移
        glCallList(self.shadow_list)
        # 影子
        glRotatef(self.an, 0, 0, 1)
        self.an = 0
        # 旋转
        glCallList(self.tank_list)
        # 本体
        self.timer()

    def up(self):
        self.an = -10
        self.force = [self.front_direct[0], self.front_direct[1]]

    def down(self):
        self.an = 10
        self.force = [-self.front_direct[0], -self.front_direct[1]]

    def left(self):
        self.face_angle -= self.turning_speed
        self.front_direct = [np.cos(self.face_angle * angle), np.sin(self.face_angle * angle)]
        self.left_direct = np.array([-np.sin(self.face_angle * angle), np.cos(self.face_angle * angle)])

    def right(self):
        self.face_angle += self.turning_speed
        self.front_direct = [np.cos(self.face_angle * angle), np.sin(self.face_angle * angle)]
        self.left_direct = [-np.sin(self.face_angle * angle), np.cos(self.face_angle * angle)]

    def box(self):
        front_dx = self.length * self.front_direct[0]
        left_dx = self.width * self.left_direct[0]
        front_dz = self.length * self.front_direct[1]
        left_dz = self.width * self.left_direct[1]

        test_points = []

        k_box = 7
        kl = 2 * k_box + 1
        # 碰撞检测点数
        for i in range(kl):
            test_points.append([int(500 + self.x + front_dx + left_dx * (i - k_box) / kl),
                                int(500 + self.z + front_dz + left_dz * (i - k_box) / kl)])
            test_points.append([int(500 + self.x - front_dx + left_dx * (i - k_box) / kl),
                                int(500 + self.z - front_dz + left_dz * (i - k_box) / kl)])
        for i in range(kl):
            test_points.append([int(500 + self.x + left_dx + front_dx * (i - k_box) / kl),
                                int(500 + self.z + left_dz + front_dz * (i - k_box) / kl)])
            test_points.append([int(500 + self.x - left_dx + front_dx * (i - k_box) / kl),
                                int(500 + self.z - left_dz + front_dz * (i - k_box) / kl)])

        return test_points

    def in_or_out(self, x, z):
        delta_p = [x - self.x, z - self.z]
        len_x = abs(delta_p[0] * self.left_direct[0] + delta_p[1] * self.left_direct[1])
        len_z = abs(delta_p[0] * self.front_direct[0] + delta_p[1] * self.front_direct[1])
        if len_x < self.width - 1 and len_z < self.length - 1:
            return True
        else:
            return False

    def hit(self):
        self.exist = False
        self.reborn_counter = self.reborn_cold
        self.x = self.born_x
        self.z = self.born_z
        self.speed = [0, 0]

    def init_force(self):
        self.force = [0, 0]

    def update(self, obstruction):
        if self.fire_counter > 0:
            self.fire_counter -= 0.02
        else:
            self.fire_counter = 0
        # 技能冷却
        if self.reborn_counter > 0:
            self.reborn_counter -= 0.02
        else:
            self.reborn_counter = 0
            self.exist = True
        # 复活冷却

        speed_length = (self.speed[0] ** 2 + self.speed[1] ** 2) ** 0.5
        if speed_length < 0.001:
            self.speed = [0, 0]
            force = [self.force[0], self.force[1]]
        else:
            k_resist = 10
            resist = [self.speed[0] / speed_length / k_resist, self.speed[1] / speed_length / k_resist]
            # 阻力模拟
            force = [self.force[0] - resist[0], self.force[1] - resist[1]]
        accelerate = 0.4
        # 加速度系数
        self.speed = [self.speed[0] + accelerate * force[0], self.speed[1] + accelerate * force[1]]

        speed_length = (self.speed[0] ** 2 + self.speed[1] ** 2) ** 0.5
        if speed_length > self.max_speed:
            self.speed = [self.speed[0] * self.max_speed / speed_length, self.speed[1] * self.max_speed / speed_length]
        # 最大速度限制
        self.x += self.speed[0]
        self.z += self.speed[1]

        speed_overwhelm_set = [0, 0]
        boxes = self.box()
        for edge in boxes:
            if 0 <= edge[0] < 1000 and 0 <= edge[1] < 1000:
                speed_overwhelm_set[0] += obstruction[edge[0]][edge[1]][0]
                speed_overwhelm_set[1] += obstruction[edge[0]][edge[1]][1]

        speed_overwhelm_set[0] /= 4
        speed_overwhelm_set[1] /= 4

        if speed_overwhelm_set != [0, 0]:
            self.speed[0] += speed_overwhelm_set[0]
            self.speed[1] += speed_overwhelm_set[1]

    def fire(self):
        if self.fire_counter == 0:
            winsound.PlaySound('D:/JetBrains/homework/firee.wav', flags=1)
            shell.ExistShell.append(shell.Shell(self.x, self.z, self.shell_speed, self.front_direct))
            self.fire_counter = self.fire_cold

    def timer(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslated(self.x, 100, self.z)
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
        if self.exist:
            if self.fire_counter != 0:
                glBegin(GL_QUADS)
                glMaterialfv(GL_FRONT, GL_DIFFUSE, [1, 0.6, 0.6, 1])
                glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [1, 0.6, 0.6, 1])
                glVertex3d(-w + (2 * w * self.fire_counter / self.fire_cold), height, h)
                glVertex3d(-w, height, h)
                glVertex3d(-w, height, -h)
                glVertex3d(-w + (2 * w * self.fire_counter / self.fire_cold), height, -h)
                glEnd()
            else:
                glBegin(GL_QUADS)
                glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 1, 0.8, 1])
                glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.8, 1, 0.8, 1])
                glVertex3d(w, height, h)
                glVertex3d(-w, height, h)
                glVertex3d(-w, height, -h)
                glVertex3d(w, height, -h)
                glEnd()

        else:
            glBegin(GL_QUADS)
            glMaterialfv(GL_FRONT, GL_DIFFUSE, [1, 0.6, 0.6, 1])
            glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [1, 0.6, 0.6, 1])
            glVertex3d(-w + (2 * w * self.reborn_counter / self.reborn_cold), height, h)
            glVertex3d(-w, height, h)
            glVertex3d(-w, height, -h)
            glVertex3d(-w + (2 * w * self.reborn_counter / self.reborn_cold), height, -h)
            glEnd()
