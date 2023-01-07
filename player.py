import itertools
import os
from random import choice

from common import player_group, monster_group
from inventory import SmallHealPotion, Sword, LeftHand, RightHand, Hood
from settings import KEY_COLOR, SLOT_RIGHT_HAND, SLOT_LEFT_HAND, DATA_DIR, SLOT_ARMOR
from tiles import Creature

from utils import calculate_sprite_range, load_raw_image, load_animations


class Player(Creature):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_animations("player"), 100, pos_x, pos_y, [player_group, monster_group])
        for i in range(7):
            super().get_inventory().add_item(SmallHealPotion())
        super().get_inventory().add_item(Sword())
        self.get_ammunition().assign_default(LeftHand(), SLOT_LEFT_HAND)
        self.get_ammunition().assign_default(RightHand(), SLOT_RIGHT_HAND)


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
                if calculate_sprite_range(self.enemy, self) < 200 and self.enemy.get_health_points():
                    choice([self.move_to_player, self.attack, self.do_nothing])()
                else:
                    choice([self.move_random, self.do_nothing, self.do_nothing, self.do_nothing])()
            self.logic_tick_counter += 1

    def attack(self):
        if self.can_apply(self.enemy, SLOT_RIGHT_HAND):
            super().apply(self.enemy, SLOT_RIGHT_HAND)
        elif self.can_apply(self.enemy, SLOT_LEFT_HAND):
            super().apply(self.enemy, SLOT_LEFT_HAND)

    def can_attack(self):
        return self.can_apply(self.enemy, SLOT_RIGHT_HAND) or self.can_apply(self.enemy, SLOT_LEFT_HAND)

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


class Monster(AI):
    def __init__(self, pos_x, pos_y, game):
        super().__init__(load_animations("player"), 100, int(pos_x), int(pos_y), [monster_group], game)
        self.get_ammunition().assign_default(LeftHand(), SLOT_LEFT_HAND)
        self.get_ammunition().assign_default(RightHand(), SLOT_RIGHT_HAND)


class Monster0(Monster):
    def __init__(self, pos_x, pos_y, game):
        super().__init__(pos_x, pos_y, game)
        self.get_inventory().add_item(Hood())
        self.get_inventory().add_item(Sword())
        self.get_inventory().add_item(SmallHealPotion())
        self.get_inventory().add_item(SmallHealPotion())
        self.get_inventory().add_item(SmallHealPotion())


class Monster1(Monster):
    def __init__(self, pos_x, pos_y, game):
        super().__init__(pos_x, pos_y, game)
        self.get_ammunition().assign(Hood(), SLOT_ARMOR)
        self.get_inventory().add_item(Hood())
        self.get_inventory().add_item(Sword())
        self.get_inventory().add_item(SmallHealPotion())


class Monster2(Monster):
    def __init__(self, pos_x, pos_y, game):
        super().__init__(pos_x, pos_y, game)
        self.get_ammunition().assign(Hood(), SLOT_ARMOR)
        self.get_ammunition().assign(Sword(), SLOT_RIGHT_HAND)
        self.get_inventory().add_item(Hood())
        self.get_inventory().add_item(Sword())
        self.get_inventory().add_item(SmallHealPotion())
        self.get_inventory().add_item(SmallHealPotion())


