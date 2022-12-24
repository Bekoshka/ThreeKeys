import pygame

from common import player_group
from tiles import Movable
from utils import load_image


class Player(Movable):
    def __init__(self, pos_x, pos_y):
        image = load_image('mara.png', pygame.Color(0xff, 0x5c, 0xf9))
        super().__init__(image, pos_x, pos_y, [player_group])








