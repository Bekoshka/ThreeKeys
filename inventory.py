from common import all_sprites, items_group, inventory_hero_group, ammunition_hero_group
from settings import SIZE, WIDTH, HEIGHT
from random import randrange

import pygame

from settings import SLOT_ARMOR, SLOT_LEFT_HAND, SLOT_RIGHT_HAND, BUTTON_TO_SLOT, KEY_COLOR
from utils import load_image


class Item(pygame.sprite.Sprite):
    def __init__(self, name, description, image, slot_type):
        super().__init__(items_group)
        self.name = name
        self.description = description
        self.image = image
        self.rect = self.image.get_rect().move(0, 0)
        self.slot_type = slot_type


    # def take_to_inventory(self):


class Inventory:
    def __init__(self, is_hero=False):
        self.is_hero = is_hero
        self.items = dict()
        self.is_visible = False

    def toggle_visibility(self):
        self.is_visible ^= 1

    def add_item(self, item):
        for i in range(5):
            for j in range(5):
                if (i, j) in self.items.keys():
                    continue
                self.items[i, j] = item
                return True
        return False

    def update(self, screen):
        if not self.is_visible:
            inventory_hero_group.empty()
            return
        if self.is_hero:
            x = 0
        else:
            x = WIDTH // 2
        rect = pygame.Rect(x, 0, WIDTH // 2, HEIGHT)
        pygame.draw.rect(screen, (50, 50, 50), rect)
        br = 10
        item_size = WIDTH // 10
        for i in range(5):
            for j in range(5):
                rect = pygame.Rect(br + x + item_size * j, br + (HEIGHT - item_size * 5) // 2 + item_size * i,
                                   item_size - br * 2, item_size - br * 2)
                pygame.draw.rect(screen, (100, 100, 100), rect)
                if (i, j) in self.items.keys():
                    item = self.items[i, j]
                    item.rect.x = rect.topleft[0]
                    item.rect.y = rect.topleft[1]
                    inventory_hero_group.add(item)
        inventory_hero_group.draw(screen)



class Ammunition:
    def __init__(self, creature):
        self.creature = creature
        self.slots = dict()
        self.slots[SLOT_ARMOR] = None
        self.slots[SLOT_LEFT_HAND] = None
        self.slots[SLOT_RIGHT_HAND] = None
        self.default_slots = dict()
        self.default_slots[SLOT_ARMOR] = None
        self.default_slots[SLOT_LEFT_HAND] = None
        self.default_slots[SLOT_RIGHT_HAND] = None
        self.is_visible = False

    def toggle_visibility(self):
        self.is_visible ^= 1

    def assign_default(self, item, slot):
        if slot in self.slots.keys():
            self.slots[slot] = item
            self.default_slots = item
            return True
        return False

    def assign(self, item, button):
        desired_slot = 0
        if button in BUTTON_TO_SLOT.keys():
            desired_slot = BUTTON_TO_SLOT[button]
        if item.slot_type & desired_slot:
            self.slots[desired_slot] = item
            return True
        return False

    def unassign(self, button):
        desired_slot = 0
        if button in BUTTON_TO_SLOT.keys():
            desired_slot = BUTTON_TO_SLOT[button]
        if desired_slot in self.slots.keys():
            if desired_slot in self.default_slots.keys():
                self.slots[desired_slot] = self.default_slots[desired_slot]
            else:
                self.slots[desired_slot] = None
            return True
        return False

    def reduce_damage(self, damage):
        if self.slots[SLOT_ARMOR]:
            reduced_damage = self.slots[SLOT_ARMOR].reduce_damage(damage)
            return reduced_damage
        return damage

    def apply(self, slot, actor, creature):
        if slot in self.slots.keys() and self.slots[slot]:
            self.slots[slot].apply(actor, creature)

    def update(self, screen):
        if not self.is_visible:
            ammunition_hero_group.empty()
            return
        rect = pygame.Rect(WIDTH // 2, 0, WIDTH // 2, HEIGHT)
        pygame.draw.rect(screen, (50, 50, 50), rect)
        br = 10
        item_size = WIDTH // 10
        rect_armor = pygame.Rect(WIDTH // 2 + WIDTH // 4 - item_size // 2, (HEIGHT) // 4,
                           item_size - br * 2, item_size - br * 2)

        rect_right_hand = pygame.Rect(WIDTH // 2 + WIDTH // 4 - item_size * 1.5 , (HEIGHT) // 2,
                                 item_size - br * 2, item_size - br * 2)
        rect_left_hand = pygame.Rect(WIDTH // 2 + WIDTH // 4 + item_size * 0.5, (HEIGHT) // 2,
                                    item_size - br * 2, item_size - br * 2)
        pygame.draw.rect(screen, (100, 100, 100), rect_armor)
        pygame.draw.rect(screen, (100, 100, 100), rect_left_hand)
        pygame.draw.rect(screen, (100, 100, 100), rect_right_hand)

        if self.slots[SLOT_LEFT_HAND]:
            item = self.slots[SLOT_LEFT_HAND]
            item.rect.x = rect_left_hand.topleft[0]
            item.rect.y = rect_left_hand.topleft[1]
            ammunition_hero_group.add(item)
        if self.slots[SLOT_RIGHT_HAND]:
            item = self.slots[SLOT_RIGHT_HAND]
            item.rect.x = rect_right_hand.topleft[0]
            item.rect.y = rect_right_hand.topleft[1]
            ammunition_hero_group.add(item)
        if self.slots[SLOT_ARMOR]:
            item = self.slots[SLOT_ARMOR]
            item.rect.x = rect_armor.topleft[0]
            item.rect.y = rect_armor.topleft[1]
            ammunition_hero_group.add(item)

        ammunition_hero_group.draw(screen)


class Weapon(Item):
    def __init__(self, name, description, image, damage, range, slot_type):
        super().__init__(name, description, image, slot_type)
        self.damage = damage
        self.range = range

    def apply(self, actor, creature):
        x1, y1, w, h = creature.rect
        x1, y1 = x1 + w // 2, y1 + h // 2
        x2, y2, w, h = actor.rect
        x2, y2 = x2 + w // 2, y2 + h // 2
        c = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        if c < self.range:
            creature.recieve_damage(randrange(*self.damage))


class Armor(Item):
    def __init__(self, name, description, image, absorption, slot_type):
        super().__init__(name, description, image, slot_type)
        self.absorption = absorption

    def reduce_damage(self, damage):
        clean_damage = damage - self.absorption
        if clean_damage < 0:
            clean_damage = 0
        return clean_damage


class HealPotion(Item):
    def __init__(self, name, description, image, heal_points, slot_type):
        super().__init__(name, description, image, slot_type)
        self.heal_points = heal_points

    def apply(self, _, creature):
        creature.increase_hp(self.heal_points)


class SmallHealPotion(HealPotion):
    def __init__(self):
        super().__init__("Small Heal Potion", "Small Heal Potion", load_image("shp.png", KEY_COLOR), 10, SLOT_LEFT_HAND | SLOT_RIGHT_HAND)


class Hood(Armor):
        def __init__(self):
            super().__init__("Hood", "Hood description", load_image("hood.png", KEY_COLOR), 15, SLOT_ARMOR)

class Sword(Weapon):
     def __init__(self):
        super().__init__("Sword", "Sword description", load_image("sword.png", KEY_COLOR), (15, 20), 50, SLOT_LEFT_HAND)


class LeftHand(Weapon):
    def __init__(self):
        super().__init__("Sword", "Sword description", load_image("left_hand.png", KEY_COLOR), (1, 2), 50, SLOT_LEFT_HAND)


class RightHand(Weapon):
    def __init__(self):
        super().__init__("Sword", "Sword description", load_image("right_hand.png", KEY_COLOR), (3, 4), 50, SLOT_RIGHT_HAND)