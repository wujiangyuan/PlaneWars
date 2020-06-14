# 飞机大战
import random

import pygame
from pygame.locals import *
import time


class Plane(object):  # 飞机父类
    def __init__(self, x, y, sc):
        self.x = x
        self.y = y
        self.screen = sc
        self.image = None
        self.bullet_list = []
        # self.image_boom_list = []
        self.boom = False  # 判断是否爆炸
        self.index = 0
        self.num = 1

    # 判断是否被击中
    def shoot_by(self, plane, blt):
        x1 = self.x + self.image.get_rect().width - 10
        y1 = self.y + self.image.get_rect().height - 20
        if x1 > blt.x > self.x and y1 > blt.y > self.y:
            plane.bullet_list.remove(blt)
            return True
        else:
            return False


# 英雄飞机
class HeroPlane(Plane):
    def __init__(self, x, y, sc):
        super(HeroPlane, self).__init__(x, y, sc)
        self.long_press = 0
        self.attack_speed = 10  # 攻速
        self.blood = 100
        self.change_time = 1
        self.image = pygame.image.load("images/me1.png")
        self.image_boom_list = []
        self.image_boom_list.append(pygame.image.load("images/me_destroy_1.png"))
        self.image_boom_list.append(pygame.image.load("images/me_destroy_2.png"))
        self.image_boom_list.append(pygame.image.load("images/me_destroy_3.png"))
        self.image_boom_list.append(pygame.image.load("images/me_destroy_4.png"))

    def __del__(self):
        pass

    def change(self):
        self.change_time += 1
        if self.change_time % 10 == 0:
            if self.change_time % 4 == 0:
                self.image = pygame.image.load("images/me1.png")
            else:
                self.image = pygame.image.load("images/me2.png")

    def display(self):
        if not self.boom:
            self.change()
            self.screen.blit(self.image, (self.x, self.y))
            # 删除越界子弹
            for blt in self.bullet_list:
                if blt.judge():
                    self.bullet_list.remove(blt)
            for blt in self.bullet_list:
                blt.display()
                blt.move()
        else:
            if self.index < len(self.image_boom_list):
                if self.num % 5 == 0:
                    self.screen.blit(self.image_boom_list[self.index],
                                     (self.x, self.y))
                    self.index += 1
                self.num += 1
            print(self.num)

    def injured(self):
        self.blood -= 5
        if self.blood <= 0:
            self.boom = True
        pass

    def move_left(self):
        if self.x >= 5:
            self.x -= 3

    def move_right(self):
        if self.x <= 475 - self.image.get_rect().width:
            self.x += 3

    def move_up(self):
        if self.y > 10:
            self.y -= 3
        pass

    def move_down(self):
        if self.y < 700 - self.image.get_rect().height:
            self.y += 3
        pass

    def shoot(self):
        blt = Bullet(self.x, self.y, self.screen)
        self.bullet_list.append(blt)

    # def shoot_by(self, bullet):
    #     pass


# 玩家子弹类
class Bullet(object):
    def __init__(self, x, y, sc):
        self.x = x + 40
        self.y = y - 20
        self.screen = sc
        self.image = pygame.image.load("images/bullet2.png")

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.y -= 5

    def judge(self):
        if self.y < 0:
            return True
        else:
            return False


# 敌机子弹类
class EnemyBullet(object):
    def __init__(self, x, y, sc):
        self.x = x + 30
        self.y = y + 30
        self.screen = sc
        self.image = pygame.image.load("images/bullet1.png")

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.y += 4

    def judge(self):
        if self.y > 700:
            return True
        else:
            return False


# 敌机类
class EnemyPlane(Plane):
    enemy_number = 0  # 敌机数量

    def __init__(self, x, y, sc):
        EnemyPlane.enemy_number += 1

        super(EnemyPlane, self).__init__(x, y, sc)
        self.direction = {"right": True, "left": False, "up": False, "down": False}  # 判断移动方向
        self.image = pygame.image.load("images/enemy1.png")
        self.image_boom_list = []
        self.image_boom_list.append(pygame.image.load("images/enemy1_down1.png"))
        self.image_boom_list.append(pygame.image.load("images/enemy1_down2.png"))
        self.image_boom_list.append(pygame.image.load("images/enemy1_down3.png"))
        self.image_boom_list.append(pygame.image.load("images/enemy1_down4.png"))

    def __del__(self):
        pass

    def display(self):
        if not self.boom:
            # super().display()
            self.screen.blit(self.image, (self.x, self.y))
            # 删除越界子弹
            for blt in self.bullet_list:
                if blt.judge():
                    self.bullet_list.remove(blt)
            for blt in self.bullet_list:
                blt.display()
                blt.move()
            self.move()
            self.shoot()
        else:
            if self.index < len(self.image_boom_list):
                if self.num % 5 == 0:
                    self.screen.blit(self.image_boom_list[self.index],
                                     (self.x, self.y))
                    self.index += 1
                self.num += 1

    def shoot(self):
        num = random.randint(1, 100)
        if num == 50:
            blt = EnemyBullet(self.x, self.y, self.screen)
            self.bullet_list.append(blt)
            pass

    def move(self):
        dire = random.randint(0, 400)
        if dire == 50:
            self.direction["up"] = True
            self.direction["down"] = False
        elif dire == 150:
            self.direction["up"] = False
            self.direction["down"] = True
        elif dire == 250:
            self.direction["left"] = True
            self.direction["right"] = False
        elif dire == 350:
            self.direction["right"] = True
            self.direction["left"] = False

        if self.direction["up"]:  # 向上走
            self.y += 2
        if self.direction["down"]:  # 向下走
            self.y -= 2
        if self.direction["right"]:  # 向右走
            self.x += 2
        if self.direction["left"]:  # 向左走
            self.x -= 2
        # 到达边界转向
        if self.x > 420:
            self.direction["left"] = True
            self.direction["right"] = False
        if self.x < 0:
            self.direction["left"] = False
            self.direction["right"] = True
        if self.y > 500:
            self.direction["down"] = True
            self.direction["up"] = False
        if self.y < 0:
            self.direction["up"] = True
            self.direction["down"] = False

    # def shoot_by(self, bullet):
    #     pass


class Background(object):
    def __init__(self, sc):
        self.window = sc
        self.y1 = 0
        self.y2 = -768
        self.image = pygame.image.load("images/background.png")

    # 更新背景，背景在动
    def update(self):
        self.y1 += 4
        self.y2 += 4
        if self.y1 >= 700:
            self.y1 = -700
        if self.y2 >= 700:
            self.y2 = -700

    def display(self):
        self.window.blit(self.image, (0, self.y1))
        self.window.blit(self.image, (0, self.y2))


class MySprite(pygame.sprite.Sprite):  # 精灵类 碰撞检测
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()

    def get_x(self): return self.rect.x

    def set_x(self, value): self.rect.x = value

    # X属性
    X = property(get_x, set_x)

    def get_y(self): return self.rect.y

    def set_y(self, value): self.rect.y = value

    # Y属性
    Y = property(get_y, set_y)

    # position属性
    def get_pos(self): return self.rect.topleft

    def set_pos(self, pos): self.rect.topleft = pos

    position = property(get_pos, set_pos)


def collide(hero_plane, enemy_plane):
    player = MySprite(hero_plane.image)
    player.position = (hero_plane.x, hero_plane.y)
    # 遍历玩家子弹列表 判断敌机是否被击中
    for bullet in hero_plane.bullet_list:
        for enemy in enemy_plane:
            if enemy.shoot_by(hero_plane, bullet):
                enemy.boom = True
                break
    # 遍历敌机子弹列表 判断玩家是否被击中
    for enemy in enemy_plane:
        for bullet in enemy.bullet_list:
            b = MySprite(bullet.image)
            b.position = (bullet.x, bullet.y)
            # if hero_plane.shoot_by(enemy, bullet):
            if pygame.sprite.collide_rect(player, b):
                enemy.bullet_list.remove(bullet)
                hero_plane.injured()
    # 遍历敌机列表 判断玩家是否与敌机碰撞
    for enemy in enemy_plane:
        if not enemy.boom:
            e = MySprite(enemy.image)
            e.position = (enemy.x, enemy.y)
            if pygame.sprite.collide_circle(player, e):
                enemy.boom = True
                hero_plane.injured()


def main_game():
    level = 3
    EnemyPlane.enemy_number = 0
    # 创建一个玩家飞机
    hero_plane = HeroPlane(190, 560, screen)
    # 创建一个敌机
    enemy_plane = list()
    # 长按提示
    long_press = {"right": False, "left": False, "up": False, "down": False, "shoot": False}
    while True:
        screen.blit(background.image, (0, 0))
        # background.update()
        # background.display()
        if hero_plane.num == 21:
            hero_plane.__del__()  # 玩家死亡 退出游戏
            return True
        else:
            if EnemyPlane.enemy_number < level:
                x = random.randint(0, 450)
                y = random.randint(0, 500)
                if EnemyPlane.enemy_number < 3:
                    level += 1
                    enemy_plane.append(EnemyPlane(x, y, screen))
                elif random.randint(0, 200) == 99:
                    enemy_plane.append(EnemyPlane(x, y, screen))
            collide(hero_plane, enemy_plane)
            hero_plane.display()
            for e in enemy_plane:
                if e.boom:
                    if e.num > 20:
                        EnemyPlane.enemy_number -= 1
                        enemy_plane.remove(e)
                        e.__del__()
            for e in enemy_plane:
                e.display()

            for event in pygame.event.get():
                # 退出
                if event.type == QUIT:
                    print("exit")
                    exit()
                elif event.type == KEYDOWN:
                    if event.key == K_a or event.key == K_LEFT:
                        long_press["left"] = True
                        # hero_plane.move_left()
                        # print("left")
                    elif event.key == K_d or event.key == K_RIGHT:
                        long_press["right"] = True
                        # hero_plane.move_right()
                        # print("right")
                    elif event.key == K_w or event.key == K_UP:
                        long_press["up"] = True
                    elif event.key == K_s or event.key == K_DOWN:
                        long_press["down"] = True
                    elif event.key == K_SPACE:
                        long_press["shoot"] = True
                        hero_plane.shoot()
                        # print("space")
                elif event.type == KEYUP:
                    if event.key == K_a or event.key == K_LEFT:
                        long_press["left"] = False
                    elif event.key == K_d or event.key == K_RIGHT:
                        long_press["right"] = False
                    elif event.key == K_w or event.key == K_UP:
                        long_press["up"] = False
                    elif event.key == K_s or event.key == K_DOWN:
                        long_press["down"] = False
                    elif event.key == K_SPACE:
                        long_press["shoot"] = False
            if long_press["right"]:
                hero_plane.move_right()
            if long_press["left"]:
                hero_plane.move_left()
            if long_press["up"]:
                hero_plane.move_up()
            if long_press["down"]:
                hero_plane.move_down()
            if long_press["shoot"]:
                hero_plane.long_press += 1
                if hero_plane.long_press == hero_plane.attack_speed:
                    hero_plane.shoot()
                    hero_plane.long_press = 0
            time.sleep(0.01)
            pygame.display.update()


# 开始窗口
def start_window():
    me_change = 1
    icon = pygame.image.load("images/me1.png")
    start = pygame.image.load("images/start.png")
    # screen.blit(icon, [200, 100])
    # screen.blit(start, [60, 400])
    while True:
        screen.blit(background.image, (0, 0))
        screen.blit(icon, [200, 200])
        screen.blit(start, [100, 400])
        me_change += 1
        if me_change % 10 == 0:
            if me_change % 4 == 0:
                icon = pygame.image.load("images/me2.png")
            else:
                icon = pygame.image.load("images/me1.png")
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_y:
                    while main_game():
                        re_btn = pygame.image.load("images/restart.png")
                        screen.blit(re_btn, [60, 600])
                        pygame.display.update()
                        enter = False
                        while not enter:
                            for event in pygame.event.get():
                                if event.type == KEYDOWN:
                                    if event.key == K_r:
                                        enter = True
                                    elif event.key == K_ESCAPE:
                                        exit()
                    return
            elif event.type == QUIT:
                return
        time.sleep(0.01)


if __name__ == '__main__':
    screen = pygame.display.set_mode((480, 700), 0, 32)
    background = Background(screen)
    start_window()
