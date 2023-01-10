from random import randrange

from ai import AI
from common import player_group, monster_group
from items import SmallHealPotion, Sword, LeftHand, RightHand, Hood, Gold
from settings import SLOT_RIGHT_HAND, SLOT_LEFT_HAND, SLOT_ARMOR
from tiles import Creature

from utils import load_animations


class Player(Creature):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_animations("player"), 100, pos_x, pos_y, [player_group, monster_group])
        for i in range(7):
            super().get_inventory().add_item(SmallHealPotion())
        super().get_inventory().add_item(Sword())
        self.get_ammunition().assign_default(LeftHand(), SLOT_LEFT_HAND)
        self.get_ammunition().assign_default(RightHand(), SLOT_RIGHT_HAND)


class Monster(AI):
    def __init__(self, pos_x, pos_y, game):
        super().__init__(load_animations("player"), 100, int(pos_x), int(pos_y), [monster_group], game)
        self.get_ammunition().assign_default(LeftHand(), SLOT_LEFT_HAND)
        self.get_ammunition().assign_default(RightHand(), SLOT_RIGHT_HAND)
        self.get_inventory().add_item(Gold(randrange(10, 100)))


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


