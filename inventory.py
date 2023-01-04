from common import buttons_group, slots_group, items_group, selected_slot, right_side_menu_open
from settings import WIDTH, HEIGHT, INVENTORY_DIMENTION, INVENTORY_ITEM_SIZE, INVENTORY_BORDER, AMMUNITION_SLOTS
from random import randrange

import pygame

from settings import SLOT_ARMOR, SLOT_LEFT_HAND, SLOT_RIGHT_HAND, BUTTON_TO_SLOT, KEY_COLOR
from utils import load_image, calculate_sprite_range


class Button(pygame.sprite.Sprite):
    def __init__(self, image, method, x, y, groups):
        super().__init__(*groups)
        self.method = method
        self.image = image
        self.rect = self.image.get_rect().move(x, y)

    def click(self):
        self.method()


class Item(pygame.sprite.Sprite):
    def __init__(self, name, description, image, slot_type,):
        super().__init__()
        self.name = name
        self.description = description
        self.image = image
        self.rect = self.image.get_rect().move(0, 0)
        self.slot_type = slot_type


class Slot(pygame.sprite.Sprite):
    def __init__(self, image, x, y, groups, type=None):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect().move(x, y)
        self.item = None
        self.default_item = None
        self.type = type

    def assigned_item(self):
        if self.item:
            return self.item
        else:
            if self.default_item:
                return self.default_item
        return None

    def assign(self, item):
        if self.can_assign_item(item):
            if self.item is None and self.default_item:
                self.default_item.kill()
            self.item = item

    def can_assign_item(self, item):
        if item is None:
            return True
        if self.type is None:
            return True
        return item.slot_type & self.type

    def assign_default(self, item):
        self.default_item = item

    def click(self):
        global selected_slot
        if selected_slot:
            if self.item:
                i = self.item
                si = selected_slot.item
                if selected_slot.can_assign_item(i) and self.can_assign_item(si):
                    selected_slot.assign(i)
                    self.assign(si)
                    selected_slot = None
            else:
                si = selected_slot.item
                if self.can_assign_item(si):
                    selected_slot.assign(None)
                    self.assign(si)
                    selected_slot = None
        else:
            selected_slot = self


class Inventory:
    def __init__(self, creature):
        self.creature = creature
        self.is_left = False
        self.items = dict()
        self.is_visible = False
        self.close_button = Button(load_image("close.png", KEY_COLOR), self.close, 0, 0, [])
        self.slots = dict()
        for i in range(INVENTORY_DIMENTION):
            for j in range(INVENTORY_DIMENTION):
                self.slots[i, j] = Slot(
                    load_image("slot.png", resize=True, size=(INVENTORY_ITEM_SIZE - INVENTORY_BORDER * 2)), 0, 0, [])

    def close(self):
        global right_side_menu_open
        if not self.is_left:
            right_side_menu_open = None
        self.is_visible = False

    def set_visibility(self, is_visible, is_left=False):
        global right_side_menu_open
        if not is_left and is_visible:
            if right_side_menu_open:
                right_side_menu_open.close()
            right_side_menu_open = self
        self.is_left = is_left
        self.is_visible = is_visible

    def add_item(self, item):
        for i in range(INVENTORY_DIMENTION):
            for j in range(INVENTORY_DIMENTION):
                slot_item = self.slots[i, j].assigned_item()
                if slot_item:
                    continue
                self.slots[i, j].assign(item)
                return True
        return False

    def update(self, screen):
        global selected_slot
        if not self.is_visible:
            self.close_button.kill()
            for slot in self.slots.values():
                slot.kill()
                if slot == selected_slot:
                    selected_slot = None
                item = slot.assigned_item()
                if item:
                    item.kill()
            return
        x = 0 if self.is_left else WIDTH // 2
        if buttons_group not in self.close_button.groups():
            buttons_group.add(self.close_button)
        rect = pygame.Rect(x, 0, WIDTH // 2, HEIGHT)
        pygame.draw.rect(screen, (50, 50, 50), rect)

        for i in range(INVENTORY_DIMENTION):
            for j in range(INVENTORY_DIMENTION):
                slot = self.slots[i, j]
                if slots_group not in slot.groups():
                    slots_group.add(slot)
                rect = slot.rect
                rect.x = INVENTORY_BORDER + x + INVENTORY_ITEM_SIZE * j
                rect.y = INVENTORY_BORDER + (
                            HEIGHT - INVENTORY_ITEM_SIZE * INVENTORY_DIMENTION) // 2 + INVENTORY_ITEM_SIZE * i
                item = slot.assigned_item()
                if item:
                    item.rect.x = rect.topleft[0]
                    item.rect.y = rect.topleft[1]
                    if items_group not in item.groups():
                        items_group.add(item)
        self.close_button.rect.x = x


class Ammunition:
    def __init__(self, creature):
        self.creature = creature
        self.slots = dict()
        for k in AMMUNITION_SLOTS.keys():
            v = AMMUNITION_SLOTS[k]
            self.slots[k] = Slot(load_image("slot.png", resize=True, size=v[0]), v[1], v[2], [], k)
        self.is_visible = False
        self.close_button = Button(load_image("close.png", KEY_COLOR), self.close, WIDTH // 2, 0, [])

    def close(self):
        global right_side_menu_open
        right_side_menu_open = None
        self.is_visible = False

    def set_visibility(self, is_visible):
        self.is_visible = is_visible
        global right_side_menu_open
        if is_visible:
            if right_side_menu_open:
                right_side_menu_open.close()
            right_side_menu_open = self

    def assign_default(self, item, slot):
        if slot in self.slots.keys():
            self.slots[slot].assign_default(item)
            return True
        return False

    def assign(self, item, slot):
        self.slots[slot].assign(item)

    def reduce_damage(self, damage):
        if self.slots[SLOT_ARMOR].assigned_item():
            reduced_damage = self.slots[SLOT_ARMOR].assigned_item().reduce_damage(damage)
            return reduced_damage
        return damage

    def apply(self, slot, actor, creature):
        if slot in self.slots.keys() and self.slots[slot].assigned_item():
            self.slots[slot].assigned_item().apply(actor, creature)

    def can_apply(self, slot, actor, creature):
        if slot in self.slots.keys() and self.slots[slot].assigned_item():
            return self.slots[slot].assigned_item().can_apply(actor, creature)
        return False

    def update(self, screen):
        global selected_slot
        if not self.is_visible:
            self.close_button.kill()
            for slot in self.slots.values():
                slot.kill()
                if slot == selected_slot:
                    selected_slot = None
                item = slot.assigned_item()
                if item:
                    item.kill()
            return
        if buttons_group not in self.close_button.groups():
            buttons_group.add(self.close_button)
        rect = pygame.Rect(WIDTH // 2, 0, WIDTH // 2, HEIGHT)
        pygame.draw.rect(screen, (50, 50, 50), rect)

        for k in AMMUNITION_SLOTS.keys():
            slot = self.slots[k]
            if slots_group not in slot.groups():
                slots_group.add(slot)
            item = slot.assigned_item()
            if item:
                item.rect.x = slot.rect.topleft[0]
                item.rect.y = slot.rect.topleft[1]
                if items_group not in item.groups():
                    items_group.add(item)


class Weapon(Item):
    def __init__(self, name, description, image, damage, range, slot_type):
        super().__init__(name, description, image, slot_type)
        self.damage = damage
        self.range = range

    def apply(self, actor, creature):
        can_apply = self.can_apply(actor, creature)
        if can_apply:
            creature.recieve_damage(randrange(*self.damage))
        return can_apply

    def can_apply(self, actor, creature):
        return calculate_sprite_range(actor, creature) < self.range


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
        self.range = 50

    def apply(self, actor, creature):
        can_apply = self.can_apply(actor, creature)
        print("CAN HEAL", can_apply)
        if can_apply:
            creature.recieve_heal(self.heal_points)
        return can_apply

    def can_apply(self, actor, creature):
        return calculate_sprite_range(actor, creature) < self.range


class SmallHealPotion(HealPotion):
    def __init__(self):
        super().__init__("Small Heal Potion", "Small Heal Potion", load_image("shp.png", KEY_COLOR), 10,
                         SLOT_LEFT_HAND | SLOT_RIGHT_HAND)


class Hood(Armor):
    def __init__(self):
        super().__init__("Hood", "Hood description", load_image("hood.png", KEY_COLOR), 15, SLOT_ARMOR)


class Sword(Weapon):
    def __init__(self):
        super().__init__("Sword", "Sword description", load_image("sword.png", KEY_COLOR), (15, 30), 70,
                         SLOT_RIGHT_HAND)


class LeftHand(Weapon):
    def __init__(self):
        super().__init__("Sword", "Sword description", load_image("left_hand.png", KEY_COLOR), (1, 2), 30,
                         SLOT_LEFT_HAND)


class RightHand(Weapon):
    def __init__(self):
        super().__init__("Sword", "Sword description", load_image("right_hand.png", KEY_COLOR), (3, 4), 30,
                         SLOT_RIGHT_HAND)