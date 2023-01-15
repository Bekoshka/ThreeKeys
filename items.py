from random import randrange

import pygame
import smokesignal

from settings import SLOT_LEFT_HAND, SLOT_RIGHT_HAND, KEY_COLOR, SLOT_ARMOR, SLOT_NONE, EVENT_BOTTLE_USED, \
    EVENT_DAMAGE_GIVEN, ANIMATION_ATTACK
from utils import load_image, calculate_sprite_range


class Item(pygame.sprite.Sprite):
    cls_name = "Item"

    def __init__(self, description, image, slot_type, count=1, stackable=True):
        if type(self).__name__ == self.cls_name:
            raise SystemExit("It is abstract class: " + self.cls_name)
        super().__init__()
        self.stackable = stackable
        self.description = description
        self.image = image
        self.rect = self.image.get_rect().move(0, 0)
        self.slot_type = slot_type
        self.count = count
        self.__delay = 0

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

    def transfer(self, other, all=False):
        if self.count > 0 and self.stackable:
            amount = self.count if all else 1
            if type(self).__name__ == type(other).__name__ and self.count > 0:
                other.count += amount
                self.count -= amount
            elif self and not other:
                other = globals()[type(self).__name__]()
                other.count = amount
                self.count -= amount
        if self.count == 0:
            self.kill()
            return None, other
        return self, other

    def apply(self, actor, creature):
        pass

    def can_apply(self, actor, creature):
        pass

    def get_animation_type(self):
        return None


class Weapon(Item):
    cls_name = "Weapon"

    def __init__(self, description, image, damage, range, slot_type):
        if type(self).__name__ == self.cls_name:
            raise SystemExit("It is abstract class: " + self.cls_name)
        super().__init__(description, image, slot_type, stackable=False)
        self.damage = damage
        self.range = range

    def apply(self, actor, creature):
        if self.can_apply(actor, creature):
            damage = randrange(*self.damage)
            smokesignal.emit(EVENT_DAMAGE_GIVEN, type(actor).__name__, type(creature).__name__, type(self).__name__,
                             damage)
            creature.recieve_damage(damage)

    def can_apply(self, actor, creature):
        return hasattr(creature, 'recieve_damage') and callable(getattr(creature, 'recieve_damage')) \
               and not creature.is_dead() and calculate_sprite_range(actor, creature) < self.range

    def get_animation_type(self):
        return ANIMATION_ATTACK


class Armor(Item):
    cls_name = "Armor"

    def __init__(self, description, image, absorption, slot_type):
        if type(self).__name__ == self.cls_name:
            raise SystemExit("It is abstract class: " + self.cls_name)
        super().__init__(description, image, slot_type, stackable=False)
        self.absorption = absorption

    def reduce_damage(self, damage):
        clean_damage = damage - self.absorption
        if clean_damage < 0:
            clean_damage = 0
        return clean_damage


class HealPotion(Item):
    cls_name = "HealPotion"

    def __init__(self, description, image, heal_points, count):
        if type(self).__name__ == self.cls_name:
            raise SystemExit("It is abstract class: " + self.cls_name)
        super().__init__(description, image, SLOT_LEFT_HAND | SLOT_RIGHT_HAND, count)
        self.heal_points = heal_points
        self.range = 50

    def apply(self, actor, creature):
        if self.can_apply(actor, creature):
            creature.recieve_heal(self.heal_points)
            self.reduce_amount()
            smokesignal.emit(EVENT_BOTTLE_USED, type(creature).__name__, type(self).__name__, self.heal_points)

    def can_apply(self, actor, creature):
        return hasattr(creature, 'recieve_heal') and callable(getattr(creature, 'recieve_heal')) \
               and not creature.is_dead() and self.count and calculate_sprite_range(actor, creature) < self.range


class Key(Item):
    cls_name = "Key"

    def __init__(self, description, image):
        if type(self).__name__ == self.cls_name:
            raise SystemExit("It is abstract class: " + self.cls_name)
        super().__init__(description, image, SLOT_LEFT_HAND | SLOT_RIGHT_HAND, stackable=False)
        self.range = 50

    def apply(self, actor, trigger):
        if self.can_apply(actor, trigger):
            trigger.run(self)

    def can_apply(self, actor, trigger):
        return hasattr(trigger, 'run') and callable(getattr(trigger, 'run')) \
               and calculate_sprite_range(actor, trigger) < self.range


class SmallHealPotion(HealPotion):
    def __init__(self, count=1):
        super().__init__(
            "Small Heal Potion description\nasdkfj kjasdkj ak akjdfaskj kj\n"
            "dfaskj dfask fkkjkj kj akj\kk dfaskj kj kj kj ",
            load_image("shp.png", KEY_COLOR), 10, int(count))


class Hood(Armor):
    def __init__(self):
        super().__init__("Теплый капюшон. Не даёт много защиты.", load_image("hood.png", KEY_COLOR), 15, SLOT_ARMOR)


class Sword(Weapon):
    def __init__(self):
        super().__init__("Старый добрый ржавый меч.", load_image("sword.png", KEY_COLOR), (15, 90), 70,
                         SLOT_RIGHT_HAND)


class Axe(Weapon):
    def __init__(self):
        super().__init__("AXE description", load_image("axe.png", KEY_COLOR), (20, 100), 70,
                         SLOT_RIGHT_HAND)


class LeftHand(Weapon):
    def __init__(self):
        super().__init__("Твоя левая рука", load_image("left_hand.png", KEY_COLOR), (1, 2), 30,
                         SLOT_LEFT_HAND)


class RightHand(Weapon):
    def __init__(self):
        super().__init__("Твоя правая рука", load_image("right_hand.png", KEY_COLOR), (3, 4), 30,
                         SLOT_RIGHT_HAND)


class Gold(Item):
    def __init__(self, count=0):
        super().__init__("Золото. Приятный бонус,\nно ты здесь не ради него", load_image("gold.png", KEY_COLOR),
                         SLOT_NONE, int(count))
