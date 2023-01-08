from inventory import HealPotion, Armor, Weapon, Item
from settings import SLOT_LEFT_HAND, SLOT_RIGHT_HAND, KEY_COLOR, SLOT_ARMOR, SLOT_NONE
from utils import load_image


class SmallHealPotion(HealPotion):
    def __init__(self):
        super().__init__("Small Heal Potion", "Small Heal Potion", load_image("shp.png", KEY_COLOR), 10,
                         SLOT_LEFT_HAND | SLOT_RIGHT_HAND, 5)


class Hood(Armor):
    def __init__(self):
        super().__init__("Hood", "Hood description", load_image("hood.png", KEY_COLOR), 15, SLOT_ARMOR)


class Sword(Weapon):
    def __init__(self):
        super().__init__("Sword", "Sword description", load_image("sword.png", KEY_COLOR), (15, 90), 70,
                         SLOT_RIGHT_HAND)


class LeftHand(Weapon):
    def __init__(self):
        super().__init__("Sword", "Sword description", load_image("left_hand.png", KEY_COLOR), (1, 2), 30,
                         SLOT_LEFT_HAND)


class RightHand(Weapon):
    def __init__(self):
        super().__init__("Sword", "Sword description", load_image("right_hand.png", KEY_COLOR), (3, 4), 30,
                         SLOT_RIGHT_HAND)


class Gold(Item):
    def __init__(self,  count):
        super().__init__("Gold", "Gold description", load_image("gold.png", KEY_COLOR), SLOT_NONE, count)
