from random import randrange

import pygame
import smokesignal

from settings import SLOT_LEFT_HAND, SLOT_RIGHT_HAND, KEY_COLOR, SLOT_ARMOR, SLOT_NONE, EVENT_BOTTLE_USED, \
    EVENT_DAMAGE_GIVEN
from utils import load_image, calculate_sprite_range


class Item(pygame.sprite.Sprite):
    cls_name = "Item"

    def __init__(self, description, image, slot_type, count=1):
        if type(self).__name__ == self.cls_name:
            raise SystemExit("It is abstract class: " + self.cls_name)
        super().__init__()
        self.description = description
        self.image = image
        self.rect = self.image.get_rect().move(0, 0)
        self.slot_type = slot_type
        self.count = count

    def reduce_amount(self):
        self.count = max([self.count - 1, 0])

    def is_empty(self):
        return self.count <= 0

    def get_count(self):
        return self.count

    def update(self, screen):
        if self.count > 1:
            font = pygame.font.Font(None, 30)
            string_rendered = font.render(str(self.count), True, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            intro_rect.bottom = self.rect.bottom
            intro_rect.right = self.rect.right
            screen.blit(string_rendered, intro_rect)

    def split(self):
        other = None
        if self.count > 1:
            other = globals()[type(self).__name__]()
            other.count = 1
            self.count -= 1
        return other

    def transfer(self, other, all=False):
        if type(self).__name__ == type(other).__name__ and self.count > 0:
            amount = self.count if all else 1
            other.count += amount
            self.count -= amount
        return self.count == 0


class Weapon(Item):
    cls_name = "Weapon"

    def __init__(self, description, image, damage, range, slot_type):
        if type(self).__name__ == self.cls_name:
            raise SystemExit("It is abstract class: " + self.cls_name)
        super().__init__(description, image, slot_type)
        self.damage = damage
        self.range = range

    def apply(self, actor, creature):
        can_apply = self.can_apply(actor, creature)
        if can_apply:
            damage = randrange(*self.damage)
            creature.recieve_damage(damage)
            smokesignal.emit(EVENT_DAMAGE_GIVEN, type(actor).__name__, type(self).__name__, damage)
        return False

    def can_apply(self, actor, creature):
        return calculate_sprite_range(actor, creature) < self.range


class Armor(Item):
    cls_name = "Armor"

    def __init__(self, description, image, absorption, slot_type):
        if type(self).__name__ == self.cls_name:
            raise SystemExit("It is abstract class: " + self.cls_name)
        super().__init__(description, image, slot_type)
        self.absorption = absorption

    def reduce_damage(self, damage):
        clean_damage = damage - self.absorption
        if clean_damage < 0:
            clean_damage = 0
        return clean_damage


class HealPotion(Item):
    cls_name = "HealPotion"

    def __init__(self, description, image, heal_points, slot_type, count):
        if type(self).__name__ == self.cls_name:
            raise SystemExit("It is abstract class: " + self.cls_name)
        super().__init__(description, image, slot_type, count)
        self.heal_points = heal_points
        self.range = 50

    def apply(self, actor, creature):
        if self.can_apply(actor, creature):
            creature.recieve_heal(self.heal_points)
            self.reduce_amount()
            smokesignal.emit(EVENT_BOTTLE_USED, type(creature).__name__, type(self).__name__, self.heal_points)
        return self.is_empty()

    def can_apply(self, actor, creature):
        return self.count and calculate_sprite_range(actor, creature) < self.range


class SmallHealPotion(HealPotion):
    def __init__(self):
        super().__init__("Small Heal Potion description", load_image("shp.png", KEY_COLOR), 10,
                         SLOT_LEFT_HAND | SLOT_RIGHT_HAND, 5)


class Hood(Armor):
    def __init__(self):
        super().__init__("Теплый капюшон. Не даёт много защиты.", load_image("hood.png", KEY_COLOR), 15, SLOT_ARMOR)


class Sword(Weapon):
    def __init__(self):
        super().__init__("Старый добрый ржавый меч.", load_image("sword.png", KEY_COLOR), (15, 90), 70,
                         SLOT_RIGHT_HAND)


class LeftHand(Weapon):
    def __init__(self):
        super().__init__("Твоя левая рука.", load_image("left_hand.png", KEY_COLOR), (1, 2), 30,
                         SLOT_LEFT_HAND)


class RightHand(Weapon):
    def __init__(self):
        super().__init__("Твоя правая рука.", load_image("right_hand.png", KEY_COLOR), (3, 4), 30,
                         SLOT_RIGHT_HAND)


class Gold(Item):
    def __init__(self, count):
        super().__init__("Золото. Приятный бонус, но ты здесь не ради него.", load_image("gold.png", KEY_COLOR),
                         SLOT_NONE, count)
