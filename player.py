import itertools
from random import choice

from common import player_group, monster_group
from inventory import SmallHealPotion, Sword, LeftHand, RightHand
from settings import KEY_COLOR, VECTORS_TO_DIRECTION, FPS, SLOT_RIGHT_HAND, SLOT_LEFT_HAND
from tiles import Animation, Creature
from utils import load_image, calculate_sprite_range


def load_creature_images(name, frames):
    images = {}
    for dx, dy, n in itertools.product([-1, 0, 1], [-1, 0, 1], range(frames)):
        fname = f'{name}\\{name}_{VECTORS_TO_DIRECTION[dx, dy]}_{n}.png'
        image = load_image(fname, KEY_COLOR)
        if (dx, dy) in images.keys():
            images[dx, dy].append(image)
        else:
            images[dx, dy] = [image]
    return images


class Player(Creature):
    def __init__(self, pos_x, pos_y):
        images = load_creature_images("mara", 2)
        animations = dict()
        for k in images.keys():
            if k == (0, 0):
                animations[k] = Animation(images[k], 10, False)
            else:
                animations[k] = Animation(images[k], 10, False)
        super().__init__(animations, 100, pos_x, pos_y, [player_group, monster_group])
        for i in range(7):
            super().get_inventory().add_item(SmallHealPotion())
        super().get_inventory().add_item(Sword())
        self.get_ammunition().assign_default(LeftHand(), SLOT_LEFT_HAND)
        self.get_ammunition().assign_default(RightHand(), SLOT_RIGHT_HAND)


class AI(Creature):
    def __init__(self, animations, max_health_points, pos_x, pos_y, groups, game):
        super().__init__(animations, max_health_points, pos_x, pos_y, groups)
        self.spawn_point = self.rect.center
        self.logic_tick_counter = 0
        self.logic_mod = 10
        self.game = game

    def update(self, screen):
        self.action()
        super().update(screen)

    def action(self):
        if self.health_points:
            if self.logic_tick_counter % self.logic_mod == 0:
                if calculate_sprite_range(self.game.player, self) < 200 and self.game.player.get_health_points():
                    choice([self.move_to_player, self.attack, self.do_nothing])()
                else:
                    choice([self.move_random, self.do_nothing, self.do_nothing, self.do_nothing])()
            self.logic_tick_counter += 1

    def attack(self):
        if self.can_apply(self.game.player, SLOT_RIGHT_HAND):
            super().apply(self.game.player, SLOT_RIGHT_HAND)
        elif self.can_apply(self.game.player, SLOT_LEFT_HAND):
            super().apply(self.game.player, SLOT_LEFT_HAND)

    def can_attack(self):
        return self.can_apply(self.game.player, SLOT_RIGHT_HAND) or self.can_apply(self.game.player, SLOT_LEFT_HAND)

    def move_random(self):
        dx = choice([-1, 0, 1])
        dy = choice([-1, 0, 1])
        self.step(dx, dy)

    def do_nothing(self):
        pass

    def move_to_player(self):
        x2, y2 = self.game.player.rect.center
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
        images = load_creature_images("mara", 2)
        animations = dict()
        for k in images.keys():
            if k == (0, 0):
                animations[k] = Animation(images[k], 10, False)
            else:
                animations[k] = Animation(images[k], 10, False)
        super().__init__(animations, 100, pos_x, pos_y, [monster_group], game)
        self.get_ammunition().assign_default(LeftHand(), SLOT_LEFT_HAND)
        self.get_ammunition().assign_default(RightHand(), SLOT_RIGHT_HAND)







