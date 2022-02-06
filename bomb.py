import time

class Bomb:
    frame = 0
    detail = [[0 for _ in range(20)] for _ in range(20)]
    def __init__(self, r, x, y, map, bomber, st = time.time()):
        self.range = r
        self.posX = x
        self.posY = y
        self.time = 3000
        self.bomber = bomber
        self.sectors = []
        self.st = 0
        self.get_range(map)
        """
        0 十字中心
        1 左右中间
        2 上下中间
        4 上端点
        3 下端点
        5 左端点
        6 右端点
        """
        
        # self.detail = [[0 for _ in range(20)] for _ in range(20)]

    def update(self, dt):
        self.time = self.time - dt
        tm = int(time.time() * 1000);
        delta = tm - self.st
        # print("debug", delta, ( delta / 100 ) % 4)
        self.frame = ( delta // 200 ) % 4
        # if self.time < 1000:
        #     self.frame = 2
        # elif self.time < 2000:
        #     self.frame = 1

    def get_range(self, map):
        # 2 是可以炸的砖块， 3 是炸弹， 1 是墙
        self.detail[self.posX][self.posY] = 0
        self.sectors.append([self.posX, self.posY])

        for x in range(1, self.range):
            if self.posX + x >= 15 or map[self.posX + x][self.posY] == 1 or map[self.posX + x][self.posY] > 4:
                if x != 1:
                    self.detail[self.posX  + x - 1][self.posY] = 6
                break
            elif map[self.posX+x][self.posY] == 0 or map[self.posX-x][self.posY] == 3:
                self.detail[self.posX + x][self.posY] = 1
                self.sectors.append([self.posX+x, self.posY])
            elif map[self.posX+x][self.posY] == 2:
                self.detail[self.posX + x][self.posY] = 1
                self.sectors.append([self.posX+x, self.posY])
                break
        # self.detail[self.posX + self.range -  1][self.posY] = 6
        # self.sectors.append([self.posX + self.range - 1, self.posY])

        for x in range(1, self.range):
            if self.posX - x < 0 or map[self.posX - x][self.posY] == 1 or map[self.posX - x][self.posY] > 4:
                if x != 1:
                    self.detail[self.posX - x + 1][self.posY] = 5
                break
            elif map[self.posX-x][self.posY] == 0 or map[self.posX-x][self.posY] == 3:
                self.detail[self.posX - x][self.posY] = 1
                self.sectors.append([self.posX-x, self.posY])
            elif map[self.posX-x][self.posY] == 2:
                self.detail[self.posX - x][self.posY] = 1
                self.sectors.append([self.posX-x, self.posY])
                break
        
        # self.detail[self.posX - self.range + 1][self.posY] = 5
        # self.sectors.append([self.posX - self.range + 1, self.posY])

        for x in range(1, self.range):
            if self.posY + x >= 13 or map[self.posX][self.posY + x] == 1 or map[self.posX][self.posY + x] > 4:
                if x != 1:
                    self.detail[self.posX][self.posY + x - 1] = 3
                break
            elif map[self.posX][self.posY+x] == 0 or map[self.posX][self.posY+x] == 3:
                self.detail[self.posX][self.posY + x] = 2
                self.sectors.append([self.posX, self.posY+x])
            elif map[self.posX][self.posY+x] == 2:
                self.detail[self.posX][self.posY + x] = 2
                self.sectors.append([self.posX, self.posY+x])
                break
        # self.detail[self.posX][self.posY + self.range - 1] = 3
        # self.sectors.append([self.posX, self.posY + self.range - 1])

        for x in range(1, self.range):
            if self.posY -x < 0 or  map[self.posX][self.posY - x] == 1 or map[self.posX][self.posY - x] > 4:
                if x != 1:
                    self.detail[self.posX][self.posY - x + 1] = 4
                break
            elif map[self.posX][self.posY-x] == 0 or map[self.posX][self.posY-x] == 3:
                self.detail[self.posX][self.posY - x ] = 2
                self.sectors.append([self.posX, self.posY-x])
            elif map[self.posX][self.posY - x] == 2:
                self.detail[self.posX][self.posY - x] = 2
                self.sectors.append([self.posX, self.posY - x])
                break
        # self.detail[self.posX][self.posY - self.range + 1] = 4
        # self.sectors.append([self.posX, self.posY - self.range + 1])