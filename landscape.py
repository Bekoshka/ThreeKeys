import pygame

from tiles import Background, Obstacle
from utils import load_image


class Grass(Background):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('grass.png'), pos_x, pos_y)


class Sand(Background):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('sand.png', resize=True), pos_x, pos_y)


class Forest(Obstacle):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('forest2.png', color_key=pygame.Color(0xff, 0x5c, 0xf9), resize=True), pos_x, pos_y)


class Box(Obstacle):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('box.png'), pos_x, pos_y)


class Rock(Obstacle):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('rock.png', color_key=pygame.Color(0xff, 0x5c, 0xf9), resize=True), pos_x, pos_y)


landscape_dict = {
    ".": Grass,
    "#": Sand
}

obstacle_dict = {
    "#": Box,
    "$": Rock,
    '!': Forest
}


class Landscape:
    @staticmethod
    def load_map(filename):
        filename = "data/" + filename
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))

        return list(map(lambda x: x.ljust(max_width, '.'), level_map))

    def generate_level(self):
        landscape = self.load_map('landscape.txt')
        x, y = None, None
        for y in range(len(landscape)):
            for x in range(len(landscape[y])):
                t = landscape[y][x]
                if t in landscape_dict.keys():
                    landscape_dict[t](x, y)

        obstacles = self.load_map('obstacle.txt')
        for y in range(len(obstacles)):
            for x in range(len(obstacles[y])):
                t = obstacles[y][x]
                if t in obstacle_dict.keys():
                    obstacle_dict[t](x, y)

        return x, y