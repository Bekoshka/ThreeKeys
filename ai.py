from random import choice

from settings import SLOT_RIGHT_HAND, SLOT_LEFT_HAND
from tiles import Creature
from utils import calculate_sprite_range


class AI(Creature):
    def __init__(self, animations, max_health_points, pos_x, pos_y, groups, enemy):
        super().__init__(animations, max_health_points, pos_x, pos_y, groups)
        self.spawn_point = self.rect.center
        self.logic_tick_counter = 0
        self.logic_mod = 10
        self.enemy = enemy

    def update(self, screen):
        self.action()
        super().update(screen)

    def action(self):
        if self.health_points:
            if self.logic_tick_counter % self.logic_mod == 0:
                if calculate_sprite_range(self.enemy, self) < 200 and not self.enemy.is_dead():
                    choice([self.move_to_player, self.attack, self.do_nothing])()
                else:
                    choice([self.move_random, self.do_nothing, self.do_nothing, self.do_nothing])()
            self.logic_tick_counter += 1

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
        x2, y2 = self.enemy.rect.center
        x1, y1 = self.rect.center
        dx = 0
        dy = 0
        if x2 > x1:
            dx += 1
        if x2 < x1:
            dx -= 1
        if y2 > y1:
            dy += 1
        if y2 < y1:
            dy -= 1
        self.step(dx, dy)