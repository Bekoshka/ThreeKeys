import pygame

from tiles import Background, Obstacle, AnimatedObstacle, Trigger
from utils import load_image, load_animations


class Grass(Background):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('grass4.png'), pos_x, pos_y)


class Road(Background):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('road1.png'), pos_x, pos_y)


class Road2(Background):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('road2.png'), pos_x, pos_y)


class Road3(Background):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('road3.png'), pos_x, pos_y)


class Road4(Background):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('road4.png'), pos_x, pos_y)


class Road5(Background):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('road5.png'), pos_x, pos_y)


class Road6(Background):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('road6.png'), pos_x, pos_y)


class Road7(Background):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('road7.png'), pos_x, pos_y)


class Sand(Background):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('sand.png', resize=True), pos_x, pos_y)


class Forest(Obstacle):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('pine.png', color_key=pygame.Color(0xff, 0x5c, 0xf9), resize=False), pos_x, pos_y)


class Forest2(Obstacle):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('tree.png', color_key=pygame.Color(0xff, 0x5c, 0xf9), resize=False), pos_x, pos_y)


class Cactus(Obstacle):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('cactus.png', color_key=pygame.Color(0xff, 0x5c, 0xf9), resize=True), pos_x, pos_y)


class Beton(Obstacle):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image("beton.jpg", color_key=pygame.Color(0xff, 0x5c, 0xf9), resize=True), pos_x, pos_y)


class Box(Obstacle):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('wall.png'), pos_x, pos_y)


class Rock(Obstacle):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('rock.png', color_key=pygame.Color(0xff, 0x5c, 0xf9)), pos_x, pos_y)


class YellowPortal(Trigger):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('wall.png'), pos_x, pos_y)


class BrownPortal(Trigger):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('portal_1.png', color_key=pygame.Color(0xff, 0x5c, 0xf9)), pos_x, pos_y)
