from random import randrange

from ai import AI
from common import player_group, monster_group
from items import SmallHealPotion, Sword, LeftHand, RightHand, Hood, Gold, Axe, Key, Key1
from settings import SLOT_RIGHT_HAND, SLOT_LEFT_HAND, SLOT_ARMOR
from tiles import Creature

from utils import load_animations


class Player(Creature):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_animations("player"), 100, pos_x, pos_y, [player_group, monster_group])
        super().get_inventory().add_item(SmallHealPotion(7))
        super().get_inventory().add_item(Sword())
        self.get_ammunition().assign_default(LeftHand(), SLOT_LEFT_HAND)
        self.get_ammunition().assign_default(RightHand(), SLOT_RIGHT_HAND)


class Chest(Creature):
    def __init__(self, pos_x, pos_y, _=None):
        super().__init__(load_animations("chest"), 0, int(pos_x), int(pos_y), [monster_group])
        super().get_inventory().add_item(SmallHealPotion(7))
        super().get_inventory().add_item(Sword())
        super().get_inventory().add_item(Sword())
        super().get_inventory().add_item(Key1())


class Monster(AI):
    def __init__(self, pos_x, pos_y, game):
        super().__init__(load_animations("player"), 100, int(pos_x), int(pos_y), [monster_group], game)
        self.get_ammunition().assign_default(LeftHand(), SLOT_LEFT_HAND)
        self.get_ammunition().assign_default(RightHand(), SLOT_RIGHT_HAND)
        self.get_inventory().add_item(Gold(randrange(10, 100)))


class Monster0(Monster):
    def __init__(self, pos_x, pos_y, enemy):
        super().__init__(pos_x, pos_y, enemy)
        self.get_inventory().add_item(Hood())
        self.get_inventory().add_item(Axe())
        self.get_inventory().add_item(SmallHealPotion(3))


class Monster1(Monster):
    def __init__(self, pos_x, pos_y, enemy):
        super().__init__(pos_x, pos_y, enemy)
        self.get_ammunition().assign(Hood(), SLOT_ARMOR)
        self.get_inventory().add_item(Hood())
        self.get_inventory().add_item(Sword())
        self.get_inventory().add_item(SmallHealPotion())


class Monster2(Monster):
    def __init__(self, pos_x, pos_y, enemy):
        super().__init__(pos_x, pos_y, enemy)
        self.get_ammunition().assign(Hood(), SLOT_ARMOR)
        self.get_ammunition().assign(Sword(), SLOT_RIGHT_HAND)
        self.get_inventory().add_item(Hood())
        self.get_inventory().add_item(Sword())
        self.get_inventory().add_item(SmallHealPotion(2))


class Zombie(AI):
    def __init__(self, pos_x, pos_y, enemy):
        super().__init__(load_animations("zombie"), 100, int(pos_x), int(pos_y), [monster_group], enemy)
        self.get_ammunition().assign_default(LeftHand(), SLOT_LEFT_HAND)
        self.get_ammunition().assign_default(RightHand(), SLOT_RIGHT_HAND)
        self.get_inventory().add_item(Gold(randrange(10, 100)))