import os

from creatures import Player
from items import Sword, Hood
from landscape import *
from creatures import *
from settings import SLOT_RIGHT_HAND, SLOT_ARMOR, tile_width, tile_height, LEVEL_DIR
from tiles import Obstacle, AnimatedObstacle, Tile


LANDSCAPES = {
    ".": Grass,
    "#": Sand
}


class Landscape:
    def __init__(self, level):
        self.level = level

    def load_map(self):
        filename = os.path.join(LEVEL_DIR, self.level, 'background.txt')
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        landscape = list(map(lambda x: x.ljust(max_width, '.'), level_map))
        for y in range(len(landscape)):
            for x in range(len(landscape[y])):
                t = landscape[y][x]
                if t in LANDSCAPES.keys():
                    LANDSCAPES[t](tile_width * x, tile_height * y)

    def load_objects(self):
        with open(os.path.join(LEVEL_DIR, self.level, 'objects.txt'), 'r') as f:
            for line in f:
                element = line.strip().split()
                cls = globals()[element[0]]
                params = element[1:]
                if issubclass(cls, Obstacle) or issubclass(cls, AnimatedObstacle):
                    cls(*params)

    def load_creatures(self, enemy):
        with open(os.path.join(LEVEL_DIR, self.level, "creatures.txt"), 'r') as f:
            for line in f:
                i = line.strip().split()
                cls = globals()[i[0]]
                params = i[1:]
                if issubclass(cls, Tile):
                    cls(*params, enemy)

    def generate(self):
        player = Player(3, 5)
        player.get_ammunition().assign(Sword(), SLOT_RIGHT_HAND)
        player.get_ammunition().assign(Hood(), SLOT_ARMOR)

        self.load_map()
        self.load_objects()
        self.load_creatures(player)
        return player
