from globals import KEY_COLOR
from tiles import Background, Obstacle
from utils import load_image


class Grass(Background):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('grass4.png'), pos_x, pos_y)


class Snow(Background):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('snow.jpg'), pos_x, pos_y)


class Ashes(Background):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('ashes.jpg'), pos_x, pos_y)


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


class SnowRoad1(Background):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('sr1.jpg'), pos_x, pos_y)


class SnowRoad2(Background):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('sr2.jpg'), pos_x, pos_y)


class SnowRoad3(Background):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('sr3.jpg'), pos_x, pos_y)


class SnowRoad4(Background):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('sr4.jpg'), pos_x, pos_y)


class SnowRoad5(Background):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('sr5.jpg'), pos_x, pos_y)


class SnowRoad6(Background):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('sr6.jpg'), pos_x, pos_y)


class Rotate1(Background):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('rotate1.jpg'), pos_x, pos_y)


class Rotate2(Background):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('rotate2.jpg'), pos_x, pos_y)


class Rotate3(Background):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('rotate3.jpg'), pos_x, pos_y)


class Rotate4(Background):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('rotate4.jpg'), pos_x, pos_y)


class Sand(Background):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('sand.png', resize=True), pos_x, pos_y)


class Pine(Obstacle):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('pine.png', color_key=KEY_COLOR, resize=False), pos_x, pos_y)


class SnowPine(Obstacle):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('pine2.png', color_key=KEY_COLOR, resize=False), pos_x, pos_y)


class SnowTree(Obstacle):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('tree2.png', color_key=KEY_COLOR, resize=False), pos_x, pos_y)


class Forest2(Obstacle):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('tree.png', color_key=KEY_COLOR, resize=False), pos_x, pos_y)


class Cactus(Obstacle):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('cactus.png', color_key=KEY_COLOR, resize=True), pos_x, pos_y)


class Beton(Obstacle):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image("beton.jpg", color_key=KEY_COLOR, resize=True), pos_x, pos_y)


class Box(Obstacle):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('wall.png'), pos_x, pos_y)


class Gates(Obstacle):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('gates.png', color_key=KEY_COLOR), pos_x, pos_y)


class Gates2(Obstacle):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('gates.png', color_key=KEY_COLOR), pos_x, pos_y)


class Rock(Obstacle):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('rock.png', color_key=KEY_COLOR), pos_x, pos_y)


class RedPortal(Obstacle):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('portal_2.png', color_key=KEY_COLOR), pos_x, pos_y)


class BrownPortal(Obstacle):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_image('portal_1.png', color_key=KEY_COLOR), pos_x, pos_y)
