import os

import pygame


from settings import tile_width, tile_height, DATA_DIR
from tiles import Background, Obstacle, AnimatedObstacle, Tile
from utils import load_image, load_animations
from player import Player, Monster1, Monster2, Monster


class Grass(Background):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('grass2.png'), pos_x, pos_y)


class Sand(Background):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('sand.png'), pos_x, pos_y)


class Forest1(AnimatedObstacle):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_animations("forest1", loop=True), "default", pos_x, pos_y)


class Forest2(AnimatedObstacle):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_animations("forest2", loop=True), "default", pos_x, pos_y)


class Forest3(AnimatedObstacle):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_animations("forest3", loop=True), "default", pos_x, pos_y)


class Box(Obstacle):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('box.png'), pos_x, pos_y)


class Rock(Obstacle):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('rock.png', color_key=pygame.Color(0xff, 0x5c, 0xf9)), pos_x, pos_y)


LANDSCAPES = {
    ".": Grass,
    "#": Sand
}


class Landscape:
    @staticmethod
    def load_map(filename):
        filename = os.path.join(DATA_DIR, filename)
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))

        return list(map(lambda x: x.ljust(max_width, '.'), level_map))

    @staticmethod
    def load_objects(filename):
        with open(os.path.join(DATA_DIR, filename), 'r') as f:
            for line in f:
                element = line.strip().split()
                cls = globals()[element[0]]
                params = element[1:]
                if issubclass(cls, Obstacle) or issubclass(cls, AnimatedObstacle):
                    cls(*params)

    @staticmethod
    def load_creatures(filename, enemy):
        with open(os.path.join(DATA_DIR, filename), 'r') as f:
            for line in f:
                i = line.strip().split()
                cls = globals()[i[0]]
                params = i[1:]
                if issubclass(cls, Tile):
                    cls(*params, enemy)

    def generate_level(self, player):
        landscape = self.load_map('landscape.txt')
        for y in range(len(landscape)):
            for x in range(len(landscape[y])):
                t = landscape[y][x]
                if t in LANDSCAPES.keys():
                    LANDSCAPES[t](tile_width * x, tile_height * y)

        self.load_objects('objects.txt')
        self.load_creatures("creatures.txt", player)
