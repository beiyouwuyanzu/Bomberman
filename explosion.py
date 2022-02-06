class Explosion:

    bomber = None

    def __init__(self, x, y, r):
        self.sourceX = x
        self.sourceY = y
        self.range = r
        self.time = 300
        self.frame = 0
        self.sectors = []
        self.detail = [[0 for _ in range(20)] for _ in range(20)]
    def explode(self, map, bombs, b):
        # print("start explode")
        self.bomber = b.bomber
        for x, y in b.sectors:
            self.sectors.append([x, y])
            self.detail[x][y] = b.detail[x][y]
        # self.sectors.extend(b.sectors)
        bombs.remove(b)
        self.bomb_chain(bombs, map)
        # print("end explode")

    def bomb_chain(self, bombs, map):

        for s in self.sectors:
            for x in bombs:
                if x.posX == s[0] and x.posY == s[1]:

                    map[x.posX][x.posY] = 0
                    if x.bomber:
                        x.bomber.bomb_limit += 1
                    self.explode(map, bombs, x)

    def clear_sectors(self, map):

        for i in self.sectors:
            map[i[0]][i[1]] = 0

    def update(self, dt):

        self.time = self.time - dt

        if self.time < 100:
            self.frame = 2
        elif self.time < 200:
            self.frame = 1
