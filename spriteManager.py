import pygame
import glob
from config import *

# TILE_WIDTH = TILE_WIDTH
# TILE_HEIGHT = TILE_HEIGHT
class SpriteManager:
    
    tile_size = 40
    def __init__(self, tile_size):
        self.TILE_SIZE = tile_size
        self.prefix = "images/"
        self.cache = {}
        self.load_pic("explosion/flame7_stand_0_[0-9].png", "bomb_4")
        self.load_pic("explosion/flame1_stand_0_[0-9].png", "bomb_0")
        self.load_pic("explosion/flame2_stand_0_[0-9].png", "bomb_1")
        self.load_pic("explosion/flame5_stand_0_[0-9].png", "bomb_2")
        self.load_pic("explosion/flame6_stand_0_[0-9].png", "bomb_6")
        self.load_pic("explosion/flame8_stand_0_[0-9].png", "bomb_5")
        self.load_pic("explosion/flame9_stand_0_[0-9].png", "bomb_3")
        self.load_pic("status/misc111_stand_0_*.png", "status", 1, 1.3)
        
  
    def load_pic(self, path, key, width = 1, height = 1):
        # print(path)
        print(glob.glob(self.prefix + path))
        tmp = []
        for p in sorted(glob.glob(self.prefix + path)):
            img = pygame.image.load(p).convert_alpha()
            img = pygame.transform.scale(img, (self.TILE_SIZE * 1, self.TILE_SIZE * 1))
            tmp.append(img)
        self.cache[key] = tmp
    
    def get(self, key, frame):
        return self.cache[key][frame]
    
    def explore_img(self, key, frame):
        return self.cache[f"bomb_{key}"][frame]

if __name__ == '__main__':
    sm = SpriteManager()
    sm.load_pic("explosion/flame7_stand_0_[0-9].png", "bomb_top")
    print(sm.get_pic("bomb_top"))