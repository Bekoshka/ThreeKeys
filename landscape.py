import pygame

from tiles import Background, Obstacle, AnimatedObstacle, Trigger
from utils import load_image, load_animations


class Grass(Background):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('grass4.png'), pos_x, pos_y)


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


class Forest4(AnimatedObstacle):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_animations("forest4", loop=True), "default", pos_x, pos_y)


class Box(Obstacle):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('box.png'), pos_x, pos_y)


class Rock(Obstacle):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('rock.png', color_key=pygame.Color(0xff, 0x5c, 0xf9)), pos_x, pos_y)


class YellowPortal(Trigger):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('box.png'), pos_x, pos_y)


class BrownPortal(Trigger):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('box.png'), pos_x, pos_y)
