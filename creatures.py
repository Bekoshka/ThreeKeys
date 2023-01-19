from random import randrange

from ai import AI
from items import SmallHealPotion, Sword, LeftHand, RightHand, Hood, Gold, Axe, YellowKey, BrownKey, Pitchfork, \
    BigHealPotion, Mace, Braid, Spear, Sledgehammer, Knucle, Leftclaw, Rightclaw, Boss1Log, GreenKey
from settings import SLOT_RIGHT_HAND, SLOT_LEFT_HAND, SLOT_ARMOR
from tiles import Creature

from utils import load_animations


class Player(Creature):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_animations("player"), 100, pos_x, pos_y)
        super().get_inventory().add_item(SmallHealPotion(10))
        super().get_inventory().add_item(Pitchfork())
        self.get_ammunition().assign_default(LeftHand(), SLOT_LEFT_HAND)
        self.get_ammunition().assign_default(RightHand(), SLOT_RIGHT_HAND)
        self.get_ammunition().assign(Hood(), SLOT_ARMOR)


class Chest(Creature):
    def __init__(self, pos_x, pos_y, _=None):
        super().__init__(load_animations("chest"), 0, int(pos_x), int(pos_y), lootable=True)
        super().get_inventory().add_item(SmallHealPotion(7))
        super().get_inventory().add_item(Braid())
        super().get_inventory().add_item(GreenKey())


class ClosedChest(Creature):
    def __init__(self, pos_x, pos_y, _=None):
        super().__init__(load_animations("chest"), 0, int(pos_x), int(pos_y), lootable=False)
        super().get_inventory().add_item(BigHealPotion(2))
        super().get_inventory().add_item(Sword())
        super().get_inventory().add_item(YellowKey())


class Chest2(Creature):
    def __init__(self, pos_x, pos_y, _=None):
        super().__init__(load_animations("chest"), 0, int(pos_x), int(pos_y), lootable=True)
        super().get_inventory().add_item(BigHealPotion(2))
        super().get_inventory().add_item(Sword())
        super().get_inventory().add_item(Gold(randrange(100, 250)))


class Chest3(Creature):
    def __init__(self, pos_x, pos_y, _=None):
        super().__init__(load_animations("chest"), 0, int(pos_x), int(pos_y), lootable=True)
        super().get_inventory().add_item(SmallHealPotion(7))
        super().get_inventory().add_item(Axe())
        super().get_inventory().add_item(Gold(randrange(100, 250)))


class Chest4(Creature):
    def __init__(self, pos_x, pos_y, _=None):
        super().__init__(load_animations("chest"), 0, int(pos_x), int(pos_y), lootable=True)
        super().get_inventory().add_item(SmallHealPotion(5))
        super().get_inventory().add_item(Mace())
        super().get_inventory().add_item(Gold(randrange(100, 250)))


class Chest5(Creature):
    def __init__(self, pos_x, pos_y, _=None):
        super().__init__(load_animations("chest"), 0, int(pos_x), int(pos_y), lootable=True)
        super().get_inventory().add_item(BigHealPotion(1))
        super().get_inventory().add_item(Braid())
        super().get_inventory().add_item(Gold(randrange(100, 250)))


class Chest6(Creature):
    def __init__(self, pos_x, pos_y, _=None):
        super().__init__(load_animations("chest"), 0, int(pos_x), int(pos_y), lootable=True)
        super().get_inventory().add_item(SmallHealPotion(6))
        super().get_inventory().add_item(Spear())
        super().get_inventory().add_item(Gold(randrange(100, 250)))


class Chest7(Creature):
    def __init__(self, pos_x, pos_y, _=None):
        super().__init__(load_animations("chest"), 0, int(pos_x), int(pos_y), lootable=True)
        super().get_inventory().add_item(SmallHealPotion(5))
        super().get_inventory().add_item(Sledgehammer())
        super().get_inventory().add_item(Gold(randrange(100, 250)))


class Chest8(Creature):
    def __init__(self, pos_x, pos_y, _=None):
        super().__init__(load_animations("chest"), 0, int(pos_x), int(pos_y), lootable=True)
        super().get_inventory().add_item(BigHealPotion(1))
        super().get_inventory().add_item(Knucle())
        super().get_inventory().add_item(Gold(randrange(100, 250)))


class ClosedChest2(Creature):
    def __init__(self, pos_x, pos_y, _=None):
        super().__init__(load_animations("chest"), 0, int(pos_x), int(pos_y), lootable=False)
        super().get_inventory().add_item(SmallHealPotion(7))
        super().get_inventory().add_item(BrownKey())
        super().get_inventory().add_item(Gold(randrange(100, 250)))


class Monster(AI):
    def __init__(self, pos_x, pos_y, game):
        super().__init__(load_animations("player"), 100, int(pos_x), int(pos_y), game)
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
        super().__init__(load_animations("zombie"), 100, int(pos_x), int(pos_y), enemy)
        self.get_ammunition().assign_default(Leftclaw(), SLOT_LEFT_HAND)
        self.get_ammunition().assign_default(Rightclaw(), SLOT_RIGHT_HAND)
        self.get_inventory().add_item(Gold(randrange(10, 100)))


class Scorpion(AI):
    def __init__(self, pos_x, pos_y, enemy):
        super().__init__(load_animations("scorpion"), 270, int(pos_x), int(pos_y), enemy)
        self.get_ammunition().assign_default(Leftclaw(), SLOT_LEFT_HAND)
        self.get_ammunition().assign_default(Rightclaw(), SLOT_RIGHT_HAND)
        self.get_inventory().add_item(Gold(randrange(100, 200)))


class Skeleton(AI):
    def __init__(self, pos_x, pos_y, enemy):
        super().__init__(load_animations("skeleton"), 130, int(pos_x), int(pos_y), enemy)
        self.get_ammunition().assign_default(Sword(), SLOT_LEFT_HAND)
        self.get_ammunition().assign_default(RightHand(), SLOT_RIGHT_HAND)
        self.get_inventory().add_item(Gold(randrange(50, 150)))


class Wolf(AI):
    def __init__(self, pos_x, pos_y, enemy):
        super().__init__(load_animations("skeleton"), 130, int(pos_x), int(pos_y), enemy)
        self.get_ammunition().assign_default(Leftclaw(), SLOT_LEFT_HAND)
        self.get_ammunition().assign_default(RightHand(), SLOT_RIGHT_HAND)
        self.get_inventory().add_item(Gold(randrange(50, 150)))


class Boss1(AI):
    def __init__(self, pos_x, pos_y, enemy):
        super().__init__(load_animations("boss1"), 2000, int(pos_x), int(pos_y), enemy)
        self.get_ammunition().assign_default(Boss1Log(), SLOT_LEFT_HAND)
        self.get_ammunition().assign_default(RightHand(), SLOT_RIGHT_HAND)
        self.get_inventory().add_item(Gold(randrange(500, 750)))
