import glfw
import map
import time
import tank
import shell
import cat
import AI
from OpenGL.GL import *

glfw.init()
glfw.window_hint(glfw.SAMPLES, 4)
# 抗锯齿
window = glfw.create_window(1200, 800, "Tanks War", None, None)
glfw.make_context_current(window)
# glfw初始化

glEnable(GL_DEPTH_TEST)
# 开启深度测试

ambient_light_intensity = [0.5, 0.5, 0.5, 1]
glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambient_light_intensity)

diffuse_light_intensity = [0.8, 0.8, 0.8, 1]
glLightfv(GL_LIGHT1, GL_DIFFUSE, diffuse_light_intensity)
glLightfv(GL_LIGHT1, GL_POSITION, [100, 100, 0, 0])
glEnable(GL_LIGHT1)
# LIGHT1
glEnable(GL_LIGHTING)
# 光照设置

game_mode = 0
Game_Over = False
width = 1200
height = 800
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(-600, 600, -400, 400, -1000, 1000)

title = map.Title2('./models/title.obj')
single_player = map.Title2('./models/single_player.obj')
double_player = map.Title2('./models/double_player.obj')
fx1 = map.Title1('./models/fx1.obj')
fx2 = map.Title1('./models/fx2.obj')
game_over = map.Title3('./models/GAMEOVER.obj')


def hello():
    title.draw(0, -100, 4)
    single_player.draw(0, 50, 3)
    double_player.draw(0, 150, 3)
    fx1.draw(-400, 120, 3)
    fx2.draw(300, 100, 3)


def hello_view_reset(wide, high):
    glViewport(0, 0, wide, high)


def view_init():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-600, 600, -400, 400, -1000, 1000)
    glRotated(50, 1, 0, 0)
    glRotated(30, 0, 1, 0)
    glViewport(0, 0, width, height)
    # 视角初始化


def view_reset(wide, high):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-wide / 2, wide / 2, -high / 2, high / 2, -1000, 1000)
    glRotated(50, 1, 0, 0)
    glRotated(30, 0, 1, 0)
    glViewport(0, 0, wide, high)


def mouse_button_callback(window, button, action, mods):
    global game_mode
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        x, y = glfw.get_cursor_pos(window)
        if 450 <= x <= 750 and 400 <= y <= 450 and game_mode == 0:
            game_mode = 1
            view_init()
        elif 450 <= x <= 750 and 500 <= y <= 550 and game_mode == 0:
            game_mode = 2
            view_init()


glfw.set_mouse_button_callback(window, mouse_button_callback)
# 设置鼠标回调事件

tank_player1 = tank.Tank(-300, -300, 0, './models/tank1.obj')
tank_player2 = tank.Tank(300, 300, 0, './models/tank2.obj')


# 键盘事件
def process_input1(window):
    if tank_player1.exist:
        if glfw.PRESS == glfw.get_key(window, glfw.KEY_W):
            tank_player1.up()
        elif glfw.PRESS == glfw.get_key(window, glfw.KEY_S):
            tank_player1.down()
        if glfw.PRESS == glfw.get_key(window, glfw.KEY_A):
            tank_player1.left()
        elif glfw.PRESS == glfw.get_key(window, glfw.KEY_D):
            tank_player1.right()
        if glfw.PRESS == glfw.get_key(window, glfw.KEY_H):
            tank_player1.fire()


def process_input2(window):
    if tank_player2.exist:
        if glfw.PRESS == glfw.get_key(window, glfw.KEY_UP):
            tank_player2.up()
        elif glfw.PRESS == glfw.get_key(window, glfw.KEY_DOWN):
            tank_player2.down()
        if glfw.PRESS == glfw.get_key(window, glfw.KEY_LEFT):
            tank_player2.left()
        elif glfw.PRESS == glfw.get_key(window, glfw.KEY_RIGHT):
            tank_player2.right()
        if glfw.PRESS == glfw.get_key(window, glfw.KEY_ENTER):
            tank_player2.fire()


the_map = map.Map(1)
# 地图
tree = map.tree
mountain = map.mountain
base = map.base
force_pos = map.force
# 获取障碍物
tank_enemys1 = AI.AItank(300, 300, shell.ExistShell, tree + mountain, base)

t = 0
the_t = 0
while not glfw.window_should_close(window):
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)
    glClearColor(0.88, 0.88, 0.88, 1)
    # 窗口色彩初始化
    if game_mode == 0:
        the_width, the_height = glfw.get_framebuffer_size(window)
        if the_width != width or the_height != height:
            hello_view_reset(the_width, the_height)
        # 窗口大小改变
        hello()

    else:
        the_width, the_height = glfw.get_framebuffer_size(window)
        if the_width != width or the_height != height:
            view_reset(the_width, the_height)
        # 窗口大小改变
        map.xyz()
        the_map.draw()
        # 地图
        if game_mode == 1:
            tank_player1.init_force()
            tank_enemys1.init_force()
            process_input1(window)
            tank_enemys1.moving()
            # player 移动控制
            tank_player1.draw()
            tank_enemys1.draw()
            tank_player1.update(force_pos)
            tank_enemys1.update(force_pos)
            if not Game_Over:
                shell.updating_shell(tree, mountain, base, tank_player1, tank_enemys1)
                the_map.base_update(tank_player1, tank_enemys1)
                cat.update_cat()
            if map.check_winner():
                tank_player1.exist = False
                tank_enemys1.exist = False
                Game_Over = True
            if Game_Over:
                game_over.draw()

        if game_mode == 2:
            tank_player1.init_force()
            tank_player2.init_force()
            process_input1(window)
            process_input2(window)
            # player1,2 移动控制
            tank_player1.draw()
            tank_player2.draw()
            tank_player1.update(force_pos)
            tank_player2.update(force_pos)
            if not Game_Over:
                shell.updating_shell(tree, mountain, base, tank_player1, tank_player2)
                the_map.base_update(tank_player1, tank_player2)
                cat.update_cat()
            if map.check_winner():
                tank_player1.exist = False
                tank_player2.exist = False
                Game_Over = True
            if Game_Over:
                game_over.draw()
            # 双人模式
        # 绘制结束

    glfw.poll_events()
    glfw.swap_buffers(window)

    mt = time.time()
    if mt - t <= 0.02:
        time.sleep(0.02 - (mt - t))
    mt = time.time()
    # print('\r' + str(1 / (mt - t)), end='')
    t = mt
    # 帧数显示
