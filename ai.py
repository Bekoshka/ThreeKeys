from random import choice

from common import tick_counter
from settings import SLOT_RIGHT_HAND, SLOT_LEFT_HAND, AGGRESSIVE_RANGE
from tiles import Creature
from utils import calculate_sprite_range, get_vector


class AI(Creature):
    def __init__(self, animations, max_health_points, pos_x, pos_y, enemy):
        super().__init__(animations, max_health_points, pos_x, pos_y)
        self.spawn_point = self.rect.center
        self.logic_mod = 3
        self.enemy = enemy

    def update(self, screen):
        self.action()
        super().update(screen)

    def action(self):
        if self.health_points:
            if tick_counter.check(self.logic_mod):
                if calculate_sprite_range(self.enemy, self) < AGGRESSIVE_RANGE and not self.enemy.is_dead():
                    choice([self.move_to_player, self.attack, self.do_nothing])()
                else:
                    choice([self.move_random, self.do_nothing, self.do_nothing, self.do_nothing])()

    def attack(self):
        if not super().apply(self.enemy, SLOT_RIGHT_HAND):
            super().apply(self.enemy, SLOT_LEFT_HAND)

    def move_random(self):
        dx = choice([-1, 0, 1])
        dy = choice([-1, 0, 1])
        self.step(dx, dy)

    def do_nothing(self):
        pass

    def move_to_player(self):
        self.step(*get_vector(*self.rect.center, *self.enemy.rect.center))
