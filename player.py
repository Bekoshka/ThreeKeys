import pygame

from common import player_group, obstacle_group, monster_group
from tiles import Movable, Creature
from utils import load_image


key_color = pygame.Color(0xff, 0x5c, 0xf9)


class Player(Creature):
    def __init__(self, pos_x, pos_y):
        image = [
            load_image('mara.png', key_color),
            load_image('mara2.png', key_color)
        ]
        super().__init__(image, 100, pos_x, pos_y, [player_group])


class Monster(Creature):
    def __init__(self, pos_x, pos_y):
        image = [
            load_image('mara.png', key_color),
            load_image('mara2.png', key_color)
        ]
        super().__init__(image, 100, pos_x, pos_y, [monster_group])






