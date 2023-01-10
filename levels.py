import os

from landscape import *
from creatures import *
from settings import SLOT_RIGHT_HAND, SLOT_ARMOR, tile_width, tile_height, LEVEL_DIR
from tiles import Obstacle, AnimatedObstacle, Tile


LANDSCAPES = {
    ".": Grass,
    "#": Sand
}


class Landscape:
    def __init__(self, level, player):
        self.background = self.load_background(str(level), player)
        self.objects = self.load_objects(str(level))
        self.creatures = self.load_creatures(str(level), player)

    def clean(self):
        for i in self.background + self.objects + self.creatures:
            i.kill()
        self.background = []
        self.objects = []
        self.creatures = []


    @staticmethod
    def load_background(level, player):
        result = []
        with open(os.path.join(LEVEL_DIR, level, 'background.txt'), 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        landscape = list(map(lambda x: x.ljust(max_width, '.'), level_map))
        for y in range(len(landscape)):
            for x in range(len(landscape[y])):
                t = landscape[y][x]
                if t in LANDSCAPES.keys():
                    result.append(LANDSCAPES[t](tile_width * x, tile_height * y))
        return result

    @staticmethod
    def load_objects(level):
        result = []
        with open(os.path.join(LEVEL_DIR, level, 'objects.txt'), 'r') as f:
            for line in f:
                element = line.strip().split()
                cls = globals()[element[0]]
                params = element[1:]
                if issubclass(cls, Obstacle) or issubclass(cls, AnimatedObstacle):
                    result.append(cls(*params))
                else:
                    raise SystemExit("Object can't be loaded: " + element[0])
        return result


    @staticmethod
    def load_creatures(level, player):
        result = []
        with open(os.path.join(LEVEL_DIR, level, "creatures.txt"), 'r') as f:
            for line in f:
                i = line.strip().split()
                cls = globals()[i[0]]
                params = i[1:]
                if issubclass(cls, Player):
                    player.set_position(*params)
                elif issubclass(cls, Tile):
                    print(*params, player)
                    result.append(cls(*params, player))
        return result
