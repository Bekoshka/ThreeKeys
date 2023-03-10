from random import randrange

from ai import AI
from item import SmallHealPotion, Sword, LeftHand, RightHand, Hood, Gold, Axe, YellowKey, BrownKey, Pitchfork, \
    BigHealPotion, Mace, Braid, Spear, Sledgehammer, Knucle, Leftclaw, Rightclaw, Boss1Log, GreenKey, LeftWolfclaw, \
    RightWolfclaw, Bit, BlueKey, Sickle, PurpleKey, Axe2, RedKey, Axe1, Sword2, Sword3, HellSword, HellSldgehammer, \
    HellAxe, OrangeKey, DemonSword, CheaterSword, CheaterHood, MinusSpeedPotion, PlusSpeedPotion, MetalArmor, \
    HellArmor
from globals import SLOT_RIGHT_HAND, SLOT_LEFT_HAND, SLOT_ARMOR
from tile import Creature

from util import load_animations


class Player(Creature):
    def __init__(self, pos_x, pos_y):
        super().__init__(load_animations("player"), 120, pos_x, pos_y)
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
        super().get_inventory().add_item(Hood())
        super().get_inventory().add_item(GreenKey())


class ClosedChest(Creature):
    def __init__(self, pos_x, pos_y, _=None):
        super().__init__(load_animations("chest"), 0, int(pos_x), int(pos_y))
        super().get_inventory().add_item(BigHealPotion(2))
        super().get_inventory().add_item(Sword())
        super().get_inventory().add_item(YellowKey())


class Chest2(Creature):
    def __init__(self, pos_x, pos_y, _=None):
        super().__init__(load_animations("chest"), 0, int(pos_x), int(pos_y))
        super().get_inventory().add_item(BigHealPotion(2))
        super().get_inventory().add_item(Sword())
        super().get_inventory().add_item(Hood())
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
        super().get_inventory().add_item(Hood())
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


class Cheest1(Creature):
    def __init__(self, pos_x, pos_y, _=None):
        super().__init__(load_animations("chest"), 0, int(pos_x), int(pos_y), lootable=True)
        super().get_inventory().add_item(BigHealPotion(2))
        super().get_inventory().add_item(Bit())
        super().get_inventory().add_item(MetalArmor())
        super().get_inventory().add_item(BlueKey())
        super().get_inventory().add_item(Gold(randrange(100, 250)))


class Cheest2(Creature):
    def __init__(self, pos_x, pos_y, _=None):
        super().__init__(load_animations("chest"), 0, int(pos_x), int(pos_y), lootable=True)
        super().get_inventory().add_item(SmallHealPotion(8))
        super().get_inventory().add_item(Sickle())
        super().get_inventory().add_item(MetalArmor())
        super().get_inventory().add_item(PurpleKey())
        super().get_inventory().add_item(Gold(randrange(100, 250)))


class Cheest3(Creature):
    def __init__(self, pos_x, pos_y, _=None):
        super().__init__(load_animations("chest"), 0, int(pos_x), int(pos_y), lootable=True)
        super().get_inventory().add_item(BigHealPotion(3))
        super().get_inventory().add_item(Axe2())
        super().get_inventory().add_item(RedKey())
        super().get_inventory().add_item(MetalArmor())
        super().get_inventory().add_item(Gold(randrange(100, 250)))


class Cheest4(Creature):
    def __init__(self, pos_x, pos_y, _=None):
        super().__init__(load_animations("chest"), 0, int(pos_x), int(pos_y), lootable=True)
        super().get_inventory().add_item(BigHealPotion(3))
        super().get_inventory().add_item(Axe1())
        super().get_inventory().add_item(Gold(randrange(100, 250)))


class Cheest5(Creature):
    def __init__(self, pos_x, pos_y, _=None):
        super().__init__(load_animations("chest"), 0, int(pos_x), int(pos_y), lootable=True)
        super().get_inventory().add_item(SmallHealPotion(5))
        super().get_inventory().add_item(Sword2())
        super().get_inventory().add_item(MetalArmor())
        super().get_inventory().add_item(Gold(randrange(100, 250)))


class HealChest(Creature):
    def __init__(self, pos_x, pos_y, _=None):
        super().__init__(load_animations("chest"), 0, int(pos_x), int(pos_y), lootable=True)
        super().get_inventory().add_item(SmallHealPotion(10))
        super().get_inventory().add_item(Gold(randrange(100, 250)))


class Cheeest1(Creature):
    def __init__(self, pos_x, pos_y, _=None):
        super().__init__(load_animations("chest"), 0, int(pos_x), int(pos_y), lootable=True)
        super().get_inventory().add_item(SmallHealPotion(8))
        super().get_inventory().add_item(Sword3())
        super().get_inventory().add_item(HellArmor())
        super().get_inventory().add_item(Gold(randrange(100, 250)))


class Cheeest2(Creature):
    def __init__(self, pos_x, pos_y, _=None):
        super().__init__(load_animations("chest"), 0, int(pos_x), int(pos_y), lootable=True)
        super().get_inventory().add_item(BigHealPotion(3))
        super().get_inventory().add_item(HellSword())
        super().get_inventory().add_item(Gold(randrange(100, 250)))


class Cheeest3(Creature):
    def __init__(self, pos_x, pos_y, _=None):
        super().__init__(load_animations("chest"), 0, int(pos_x), int(pos_y), lootable=True)
        super().get_inventory().add_item(SmallHealPotion(4))
        super().get_inventory().add_item(HellSldgehammer())
        super().get_inventory().add_item(Gold(randrange(100, 250)))


class Cheeest4(Creature):
    def __init__(self, pos_x, pos_y, _=None):
        super().__init__(load_animations("chest"), 0, int(pos_x), int(pos_y), lootable=True)
        super().get_inventory().add_item(SmallHealPotion(5))
        super().get_inventory().add_item(HellAxe())
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


class KnightDemon(AI):
    def __init__(self, pos_x, pos_y, enemy):
        super().__init__(load_animations("demon_knight"), 368, int(pos_x), int(pos_y), enemy)
        self.get_ammunition().assign_default(DemonSword(), SLOT_LEFT_HAND)
        self.get_ammunition().assign_default(RightHand(), SLOT_RIGHT_HAND)
        self.get_inventory().add_item(Gold(randrange(50, 150)))


class Wolf(AI):
    def __init__(self, pos_x, pos_y, enemy):
        super().__init__(load_animations("wolf"), 130, int(pos_x), int(pos_y), enemy)
        self.get_ammunition().assign_default(LeftWolfclaw(), SLOT_LEFT_HAND)
        self.get_ammunition().assign_default(RightWolfclaw(), SLOT_RIGHT_HAND)
        self.get_inventory().add_item(Gold(randrange(100, 250)))


class Bandit(AI):
    def __init__(self, pos_x, pos_y, enemy):
        super().__init__(load_animations("bandit"), 100, int(pos_x), int(pos_y), enemy)
        self.get_ammunition().assign_default(LeftWolfclaw(), SLOT_LEFT_HAND)
        self.get_ammunition().assign_default(RightWolfclaw(), SLOT_RIGHT_HAND)
        self.get_inventory().add_item(Gold(randrange(100, 250)))


class Boss1(AI):
    def __init__(self, pos_x, pos_y, enemy):
        super().__init__(load_animations("boss1"), 2000, int(pos_x), int(pos_y), enemy)
        self.get_ammunition().assign_default(Boss1Log(), SLOT_LEFT_HAND)
        self.get_ammunition().assign_default(RightHand(), SLOT_RIGHT_HAND)
        self.get_inventory().add_item(Gold(randrange(500, 750)))


class Boss2(AI):
    def __init__(self, pos_x, pos_y, enemy):
        super().__init__(load_animations("boss2"), 3700, int(pos_x), int(pos_y), enemy)
        self.get_ammunition().assign_default(Boss1Log(), SLOT_LEFT_HAND)
        self.get_ammunition().assign_default(RightHand(), SLOT_RIGHT_HAND)
        self.get_inventory().add_item(Gold(randrange(500, 750)))


class Boss3(AI):
    def __init__(self, pos_x, pos_y, enemy):
        super().__init__(load_animations("boss3"), 5000, int(pos_x), int(pos_y), enemy)
        self.get_ammunition().assign_default(Boss1Log(), SLOT_LEFT_HAND)
        self.get_ammunition().assign_default(RightHand(), SLOT_RIGHT_HAND)
        super().get_inventory().add_item(OrangeKey())
        self.get_inventory().add_item(Gold(randrange(1500, 2000)))


class CheaterChest(Creature):
    def __init__(self, pos_x, pos_y, _=None):
        super().__init__(load_animations("cheater_chest"), 0, int(pos_x), int(pos_y), lootable=True)
        super().get_inventory().add_item(CheaterSword())
        super().get_inventory().add_item(CheaterHood())
        super().get_inventory().add_item(BrownKey())
        super().get_inventory().add_item(PlusSpeedPotion(9999999))
        super().get_inventory().add_item(MinusSpeedPotion(9999999))
