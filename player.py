import pygame
import math
import time
from bomb import Bomb

class Player:
    posX = 1
    posY = 1
    direction = 0
    frame = 0
    animation = []
    range = 7
    bomb_limit = 6
    allpic = None
    width = 60
    hscale = 1.5
    height = 60 * hscale
    coor_xst = 22
    coor_yst = 62
    death_tm = 0
    speed = 0.08
    uuid = ""
    update = False
    freeze = False
    movement = True
    
    # 隶属哪一个
    tempx = 1 
    tempy = 1
    H = 1
    W = 1


    def __init__(self, H = 1, W = 1):
        self.life = True
        self.H = H
        self.W = W
        self.load()

    def move(self, dx, dy, grid, enemys):
        if self.freeze:
            return

        self.tempx = round(self.posX)
        self.tempy = round(self.posY)

        map = []

        for i in range(len(grid)):
            map.append([])
            for j in range(len(grid[i])):
                map[i].append(grid[i][j])

        for x in enemys:
            if x == self:
                continue
            elif not x.life:
                continue
            else:
                map[int(x.posX/4)][int(x.posY/4)] = 2

        # if self.posX % 4 != 0 and dx == 0:
        #     if self.posX % 4 == 1:
        #         self.posX -= 1
        #     elif self.posX % 4 == 3:
        #         self.posX += 1
        #     return
        # if self.posY % 4 != 0 and dy == 0:
        #     if self.posY % 4 == 1:
        #         self.posY -= 1
        #     elif self.posY % 4 == 3:
        #         self.posY += 1
        #     return

        # right
        if dx == 1:
            if 0.999 > math.modf(self.posX)[0] > 0.5:
                self.posX += self.speed
            elif self.tempx + 1 < 15 and  map[self.tempx + 1][self.tempy] == 0:
                self.posX += self.speed
        # left
        elif dx == -1:
            if 0.001 < math.modf(self.posX)[0] < 0.5:
                # print(0 , math.modf(self.posX)[0] , 0.5)
                self.posX -= self.speed
            # self.tempx = math.ceil(self.posX / 4)
            elif self.tempx - 1 >= 0 and  map[self.tempx - 1][self.tempy] == 0:
                self.posX -= self.speed

        # bottom
        if dy == 1:
            if 0.999 > math.modf(self.posY)[0] > 0.5:
                # print("bottom", self.posY,  math.modf(self.posY)[0])
                self.posY += self.speed
            elif self.tempy + 1 < 13 and  map[self.tempx][self.tempy + 1] == 0:
                self.posY += self.speed
        # top
        elif dy == -1:

            if 0.001 < math.modf(self.posY)[0] < 0.5:
                # print("top", self.posY ,math.modf(self.posY)[0])
                self.posY -= self.speed
            elif self.tempy - 1 >= 0 and  map[self.tempx][self.tempy - 1] == 0:
                self.posY -= self.speed

        self.tempx = round(self.posX)
        self.tempy = round(self.posY)

    def plant_bomb(self, map):
        b = Bomb(self.range, round(self.tempx), round(self.tempy), map, self, time.time() * 1000)
        return b

    def check_death(self, exp):
        for e in exp:
            for s in e.sectors:
                if self.tempx == s[0] and self.tempy == s[1]:
                    self.life = False
                    self.freeze = True
                    self.death_tm = 0

    def dump_status(self, ):
        data = {}
        data["protocol"] = "player_status"
        data["pos"] = [self.posX, self.posY]
        data["movement"] = self.movement
        data["direction"] = self.direction
        data["uuid"] = self.uuid
        data["life"] = self.life
        data["freeze"] = self.freeze

        return data

    def load(self):
        '''
        :param self:
        :param filename:文件路径
        :param row:精灵序列图行数
        :param columns:精灵序列图列数
        :return:
        '''
        allpic = pygame.image.load("images/hero/huoying.png").convert_alpha()  # 载入整张精灵序列图
        # 60 -> title_width
        # self.height -> 1.3tile_width
        size = (allpic.get_width() * ( self.W / self.width), allpic.get_height() * self.hscale * ( self.W / self.width))
        self.allpic = pygame.transform.scale(allpic, size)
        # print(self.allpic)
        self.allpic_rect = self.allpic.get_rect()  # 获取图片的rect值
        # self.frame_width = self.main_rect.width / columns  # 计算单一帧的宽度=图宽/列数
        # self.frame_height = self.main_rect.height / row  # 计算单一帧的高度=图宽/行数
        # self.rect = self.x + self.movex, self.y + self.movey, self.frame_width, self.frame_height  # 更新rect

    def get_pic_coor(self):
        """
        获得当前精灵图的左下角坐标
        """

        mp = [0, 2, 3, 1]
        fm = int(self.frame)
        k = 1.0 * self.W / self.width
        return (self.posX * self.W , self.posY * self.H - 0.5 * self.H) , (self.coor_xst * k + fm * 100 * k, 
            self.coor_yst * k + 100 * self.hscale * mp[self.direction] * k, self.width * k, self.height * k )

    def load_animations(self, scale):
        front = []
        back = []
        left = []
        right = []
        resize_width = scale
        resize_height = scale

        f1 = pygame.image.load('images/hero/pf0.png')
        f2 = pygame.image.load('images/hero/pf1.png')
        f3 = pygame.image.load('images/hero/pf2.png')

        f1 = pygame.transform.scale(f1, (resize_width, resize_height))
        f2 = pygame.transform.scale(f2, (resize_width, resize_height))
        f3 = pygame.transform.scale(f3, (resize_width, resize_height))

        front.append(f1)
        front.append(f2)
        front.append(f3)

        r1 = pygame.image.load('images/hero/pr0.png')
        r2 = pygame.image.load('images/hero/pr1.png')
        r3 = pygame.image.load('images/hero/pr2.png')

        r1 = pygame.transform.scale(r1, (resize_width, resize_height))
        r2 = pygame.transform.scale(r2, (resize_width, resize_height))
        r3 = pygame.transform.scale(r3, (resize_width, resize_height))

        right.append(r1)
        right.append(r2)
        right.append(r3)

        b1 = pygame.image.load('images/hero/pb0.png')
        b2 = pygame.image.load('images/hero/pb1.png')
        b3 = pygame.image.load('images/hero/pb2.png')

        b1 = pygame.transform.scale(b1, (resize_width, resize_height))
        b2 = pygame.transform.scale(b2, (resize_width, resize_height))
        b3 = pygame.transform.scale(b3, (resize_width, resize_height))

        back.append(b1)
        back.append(b2)
        back.append(b3)

        l1 = pygame.image.load('images/hero/pl0.png')
        l2 = pygame.image.load('images/hero/pl1.png')
        l3 = pygame.image.load('images/hero/pl2.png')

        l1 = pygame.transform.scale(l1, (resize_width, resize_height))
        l2 = pygame.transform.scale(l2, (resize_width, resize_height))
        l3 = pygame.transform.scale(l3, (resize_width, resize_height))

        left.append(l1)
        left.append(l2)
        left.append(l3)

        self.animation.append(front)
        self.animation.append(right)
        self.animation.append(back)
        self.animation.append(left)
