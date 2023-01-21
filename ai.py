from random import choice

from common import tick_counter
from settings import DEFAULT_AI_AGGRESSIVE_RANGE, DEFAULT_AI_LOGIC_MOD
from globals import SLOT_RIGHT_HAND, SLOT_LEFT_HAND
from tile import Creature
from util import calculate_sprite_range, get_vector


class AI(Creature):
    def __init__(self, animations, max_health_points, pos_x, pos_y, enemy, aggressive_range=DEFAULT_AI_AGGRESSIVE_RANGE,
                 logic_mod=DEFAULT_AI_LOGIC_MOD):
        super().__init__(animations, max_health_points, pos_x, pos_y)
        self.__logic_mod = logic_mod
        self.__enemy = enemy
        self.__aggressive_range = aggressive_range

    def update(self, screen):
        self.__action()
        super().update(screen)

    def __action(self):
        if not self.is_dead():
            if tick_counter.check(self.__logic_mod):
                if calculate_sprite_range(self.__enemy, self) < self.__aggressive_range and not self.__enemy.is_dead():
                    choice([self.__move_to_player, self.__attack])()
                else:
                    choice([self.__move_random, self.__do_nothing, self.__do_nothing, self.__do_nothing])()

    def __attack(self):
        if not super().apply(self.__enemy, SLOT_RIGHT_HAND):
            super().apply(self.__enemy, SLOT_LEFT_HAND)

    def __move_random(self):
        dx = choice([-1, 0, 1])
        dy = choice([-1, 0, 1])
        self.step(dx, dy)

    def __do_nothing(self):
        pass

    def __move_to_player(self):
        self.step(*get_vector(*self.rect.center, *self.__enemy.rect.center))
