from random import randrange

import pygame
import smokesignal

from globals import SLOT_LEFT_HAND, SLOT_RIGHT_HAND, KEY_COLOR, SLOT_ARMOR, SLOT_NONE, EVENT_BOTTLE_USED, \
    EVENT_DAMAGE_GIVEN, ANIMATION_ATTACK
from utils import load_image, calculate_sprite_range, load_sound


class Item(pygame.sprite.Sprite):
    def __init__(self, description, image, slot_type, count=1, stackable=True):
        if type(self).__name__ == Item.__name__:
            raise SystemExit("It is abstract class: " + Item.__name__)
        super().__init__()
        self.__stackable = stackable
        self.__description = description
        self.image = image
        self.rect = self.image.get_rect().move(0, 0)
        self.__slot_type = slot_type
        self.__count = count

    def get_description(self):
        return self.__description

    def get_slot_type(self):
        return self.__slot_type

    def _reduce_amount(self):
        self.__count = max([self.__count - 1, 0])

    def is_empty(self):
        return self.__count <= 0

    def get_count(self):
        return self.__count

    def update(self, screen):
        if self.__count > 1:
            font = pygame.font.Font(None, 30)
            string_rendered = font.render(str(self.__count), True, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            intro_rect.bottom = self.rect.bottom
            intro_rect.right = self.rect.right
            screen.blit(string_rendered, intro_rect)

    def transfer(self, other, all=False):
        if self.__count > 0 and self.__stackable:
            amount = self.__count if all else 1
            if type(self).__name__ == type(other).__name__ and self.__count > 0:
                other.__count += amount
                self.__count -= amount
            elif self and not other:
                other = globals()[type(self).__name__]()
                other.__count = amount
                self.__count -= amount
        if self.__count == 0:
            self.kill()
            return None, other
        return self, other

    def apply(self, actor, creature):
        pass

    def can_apply(self, actor, creature):
        pass

    def get_animation_type(self):
        return None

    def get_sound(self):
        return None


class Weapon(Item):
    def __init__(self, description, image, sound, damage, range, slot_type):
        if type(self).__name__ == Weapon.__name__:
            raise SystemExit("It is abstract class: " + Weapon.__name__)
        super().__init__(description, image, slot_type, stackable=False)
        self.__damage = damage
        self.__range = range
        self.__sound = sound

    def apply(self, actor, creature):
        if self.can_apply(actor, creature):
            damage = randrange(*self.__damage)
            smokesignal.emit(EVENT_DAMAGE_GIVEN, actor, creature, self, damage)
            creature.recieve_damage(damage)

    def can_apply(self, actor, creature):
        return hasattr(creature, 'recieve_damage') and callable(getattr(creature, 'recieve_damage')) \
               and not creature.is_dead() and calculate_sprite_range(actor, creature) < self.__range

    def get_animation_type(self):
        return ANIMATION_ATTACK

    def get_sound(self):
        return self.__sound


class Armor(Item):
    def __init__(self, description, image, absorption, slot_type):
        if type(self).__name__ == Armor.__name__:
            raise SystemExit("It is abstract class: " + Armor.__name__)
        super().__init__(description, image, slot_type, stackable=False)
        self.__absorption = absorption

    def reduce_damage(self, damage):
        clean_damage = damage - self.__absorption
        if clean_damage < 0:
            clean_damage = 0
        return clean_damage


class HealPotion(Item):
    def __init__(self, description, image, heal_points, count, range):
        if type(self).__name__ == HealPotion.__name__:
            raise SystemExit("It is abstract class: " + HealPotion.__name__)
        super().__init__(description, image, SLOT_LEFT_HAND | SLOT_RIGHT_HAND, count)
        self.__heal_points = heal_points
        self.__range = range

    def apply(self, actor, creature):
        if self.can_apply(actor, creature):
            creature.recieve_heal(self.__heal_points)
            self._reduce_amount()
            smokesignal.emit(EVENT_BOTTLE_USED, actor, creature, self)

    def can_apply(self, actor, creature):
        return hasattr(creature, 'recieve_heal') and callable(getattr(creature, 'recieve_heal')) \
               and not creature.is_dead() and calculate_sprite_range(actor, creature) < self.__range


class Key(Item):
    def __init__(self, description, image, range):
        if type(self).__name__ == Key.__name__:
            raise SystemExit("It is abstract class: " + Key.__name__)
        super().__init__(description, image, SLOT_LEFT_HAND | SLOT_RIGHT_HAND, stackable=False)
        self.__range = range

    def apply(self, actor, trigger):
        if self.can_apply(actor, trigger):
            trigger.run_trigger(self)

    def can_apply(self, actor, trigger):
        return hasattr(trigger, 'run_trigger') and callable(getattr(trigger, 'run_trigger')) \
               and calculate_sprite_range(actor, trigger) < self.__range


class SmallHealPotion(HealPotion):
    def __init__(self, count=1):
        super().__init__(
            "Small Heal Potion description",
            load_image("shp.png", KEY_COLOR), 25, int(count), range=50)


class BigHealPotion(HealPotion):
    def __init__(self, count=1):
        super().__init__(
            "Small Heal Potion description",
            load_image("big_bottle.png", KEY_COLOR), 50, int(count), range=50)


class Hood(Armor):
    def __init__(self):
        super().__init__("Теплый капюшон. Не\nдаёт много защиты.", load_image("hood.png", KEY_COLOR), 25, SLOT_ARMOR)


class Sword(Weapon):
    def __init__(self):
        super().__init__("Старый добрый железный меч.", load_image("sword.png", KEY_COLOR),
                         load_sound("sword.mp3"), (50, 60), 80, SLOT_RIGHT_HAND)


class SkeletonSword(Weapon):
    def __init__(self):
        super().__init__("Старый добрый железный меч.", load_image("sword.png", KEY_COLOR),
                         load_sound("sword.mp3"), (45, 50), 45, SLOT_RIGHT_HAND)


class Mace(Weapon):
    def __init__(self):
        super().__init__("Мощная и неуклюжая булава, сделана на совесть", load_image("mace.png", KEY_COLOR), (60, 90),
                         load_sound("sword.mp3"), 60, SLOT_RIGHT_HAND)


class Braid(Weapon):
    def __init__(self):
        super().__init__("Что в мультиках, что и здесь, всё равно забирает жизни.", load_image("braid.png", KEY_COLOR),
                         load_sound("sword.mp3"), (60, 70), 100, SLOT_RIGHT_HAND)


class Boss1Log(Weapon):
    def __init__(self):
        super().__init__("Бревно.", load_image("braid.png", KEY_COLOR), load_sound("sword.mp3"), (60, 80), 100,
                         SLOT_RIGHT_HAND)


class Knucle(Weapon):
    def __init__(self):
        super().__init__("Откуда он здесь?", load_image("knucle.png", KEY_COLOR), load_sound("sword.mp3"), (50, 60), 60,
                         SLOT_RIGHT_HAND)


class Sword1(Weapon):
    def __init__(self):
        super().__init__("Свежий и качественный стальной меч", load_image("sword1.png", KEY_COLOR),
                         load_sound("sword.mp3"), (80, 90), 80, SLOT_RIGHT_HAND)


class Sledgehammer(Weapon):
    def __init__(self):
        super().__init__("Кувалда, что тут ещё сказать, мощно и громоздко", load_image("sledgehammer.png", KEY_COLOR),
                         load_sound("sword.mp3"), (110, 130), 130, SLOT_RIGHT_HAND)


class Pitchfork(Weapon):
    def __init__(self):
        super().__init__("Всё таки для огрода подходит лучше.", load_image("pitchfork.png", KEY_COLOR),
                         load_sound("sword.mp3"), (35, 45), 55, SLOT_RIGHT_HAND)


class Spear(Weapon):
    def __init__(self):
        super().__init__("Бьёт далеко, но урона не хватает.", load_image("spear.png", KEY_COLOR),
                         load_sound("sword.mp3"), (60, 67), 140, SLOT_RIGHT_HAND)


class Axe(Weapon):
    def __init__(self):
        super().__init__("Старый топор для рубки дров.", load_image("axe.png", KEY_COLOR),
                         load_sound("sword.mp3"), (70, 80), 110, SLOT_RIGHT_HAND)


class Axe2(Weapon):
    def __init__(self):
        super().__init__("Огромный, тяжёлый топор.", load_image("axe2.png", KEY_COLOR),
                         load_sound("sword.mp3"), (70, 80), 110, SLOT_RIGHT_HAND)


class Bit(Weapon):
    def __init__(self):
        super().__init__("Длинная и увесистая и с железными кольями, была сделана местными мастерами.",
                         load_image("бита.png", KEY_COLOR), load_sound("sword.mp3"), (70, 80), 110, SLOT_RIGHT_HAND)


class Sickle(Weapon):
    def __init__(self):
        super().__init__("Он остался здесь с момента бегства фермеров от глобального похолодания.",
                         load_image("серп.png", KEY_COLOR), load_sound("sword.mp3"), (70, 80), 110, SLOT_RIGHT_HAND)


class Sword2(Weapon):
    def __init__(self):
        super().__init__("После убийства короля  поклониками великой звезды, все забыли про его меч.",
                         load_image("sword2.png", KEY_COLOR), load_sound("sword.mp3"), (70, 80), 110, SLOT_RIGHT_HAND)


class Axe1(Weapon):
    def __init__(self):
        super().__init__("Новенький стальной меч.", load_image("axe1.png", KEY_COLOR), load_sound("sword.mp3"),
                         (80, 96), 120, SLOT_RIGHT_HAND)


class LeftHand(Weapon):
    def __init__(self):
        super().__init__("Твоя левая рука", load_image("left_hand.png", KEY_COLOR), load_sound("sword.mp3"), (1, 2), 30,
                         SLOT_LEFT_HAND)


class Leftclaw(Weapon):
    def __init__(self):
        super().__init__("Его левая рука", load_image("left_hand.png", KEY_COLOR), load_sound("sword.mp3"),
                         (30, 45), 55, SLOT_LEFT_HAND)


class LeftWolfclaw(Weapon):
    def __init__(self):
        super().__init__("Его левая рука", load_image("left_hand.png", KEY_COLOR), load_sound("sword.mp3"),
                         (42, 45), 55, SLOT_LEFT_HAND)


class RightWolfclaw(Weapon):
    def __init__(self):
        super().__init__("Его правая рука", load_image("left_hand.png", KEY_COLOR), load_sound("sword.mp3"),
                         (42, 45), 55, SLOT_LEFT_HAND)


class Rightclaw(Weapon):
    def __init__(self):
        super().__init__("Его правая рука", load_image("left_hand.png", KEY_COLOR),
                         load_sound("sword.mp3"), (30, 38), 55, SLOT_LEFT_HAND)


class RightHand(Weapon):
    def __init__(self):
        super().__init__("Твоя правая рука", load_image("right_hand.png", KEY_COLOR), load_sound("sword.mp3"),
                         (3, 4), 30, SLOT_RIGHT_HAND)


class Gold(Item):
    def __init__(self, count=0):
        super().__init__("Золото. Приятный бонус,\nно ты здесь не ради него", load_image("gold.png", KEY_COLOR),
                         SLOT_NONE, int(count))


class YellowKey(Key):
    def __init__(self):
        super().__init__("Используется для откыртия ворот в левом ниженм углу карты",
                         load_image("yellow_key.png", KEY_COLOR), 500)


class BrownKey(Key):
    def __init__(self):
        super().__init__("Нужен для использования портала в правом нижнем углу карты", load_image("key.png", KEY_COLOR),
                         500)


class GreenKey(Key):
    def __init__(self):
        super().__init__("Открываает сундук в левом верхнем углу карты", load_image("green_key.png", KEY_COLOR), 500)


class BlueKey(Key):
    def __init__(self):
        super().__init__("Открываает ворота в правом нижнем углу карты", load_image("blue_key.png", KEY_COLOR), 500)


class PurpleKey(Key):
    def __init__(self):
        super().__init__("Открываает ворота в правом нижнем углу карты", load_image("purple_key.png", KEY_COLOR), 500)


class RedKey(Key):
    def __init__(self):
        super().__init__("Нужен для использования портала в правом нижнем углу карты",
                         load_image("red_key.png", KEY_COLOR), 500)
