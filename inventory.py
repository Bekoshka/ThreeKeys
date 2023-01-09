import json

import smokesignal

from items import *
from buttons import Button
from common import buttons_group, slots_group, items_group, selected_slot, right_side_menu_open
from settings import WIDTH, HEIGHT, SLOT_RIGHT_HAND, SLOT_LEFT_HAND, EVENT_BOTTLE_USED, EVENT_ITEM_ASSIGNED
from random import randrange

import pygame

from settings import SLOT_ARMOR, KEY_COLOR
from utils import load_image, calculate_sprite_range

INVENTORY_DIMENTION = 5
INVENTORY_BORDER = 10
INVENTORY_ITEM_SIZE = WIDTH // 10
AMMUNITION_SLOTS = {
    SLOT_ARMOR: (INVENTORY_ITEM_SIZE - INVENTORY_BORDER * 2,
                 WIDTH // 2 + WIDTH // 4 - INVENTORY_ITEM_SIZE // 2, HEIGHT // 4),
    SLOT_RIGHT_HAND: (INVENTORY_ITEM_SIZE - INVENTORY_BORDER * 2,
                      WIDTH // 2 + WIDTH // 4 - INVENTORY_ITEM_SIZE * 1.5, HEIGHT // 2),
    SLOT_LEFT_HAND: (INVENTORY_ITEM_SIZE - INVENTORY_BORDER * 2,
                     WIDTH // 2 + WIDTH // 4 + INVENTORY_ITEM_SIZE * 0.5, HEIGHT // 2)
}


class Slot(pygame.sprite.Sprite):
    def __init__(self, creature, image, x, y, type=None):
        super().__init__()
        self.creature = creature
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
            count = 0
            if item:
                count = item.get_count()
            smokesignal.emit(EVENT_ITEM_ASSIGNED, type(self.creature).__name__, type(item).__name__, count)

    def can_assign_item(self, item):
        if item is None:
            return True
        if self.type is None:
            return True
        return item.slot_type & self.type

    def assign_default(self, item):
        self.default_item = item

    def exchange(self):
        pass

    def click(self, union=False, divide=False):
        print(union, divide)
        global selected_slot
        if selected_slot:
            if not union and not divide:
                # if self.item:
                i = self.item
                si = selected_slot.item
                if selected_slot.can_assign_item(i) and self.can_assign_item(si):
                    selected_slot.assign(i)
                    self.assign(si)
                    selected_slot = None
                # else:
                #     si = selected_slot.item
                #     if self.can_assign_item(si):
                #         selected_slot.assign(None)
                #         self.assign(si)
                #         selected_slot = None
            elif union and not divide:
                if self.item:
                    si = selected_slot.item
                    if si:
                        if si.transfer(self.item, True):
                            si.kill()
                            selected_slot.assign(None)
                selected_slot = None
            elif not union and divide:
                if self.item:
                    si = selected_slot.item
                    if si:
                        if si.transfer(self.item):
                            si.kill()
                            selected_slot.assign(None)
                else:
                    si = selected_slot.item
                    if si:
                        other = si.split()
                        if self.can_assign_item(other):
                            self.assign(other)

        else:
            selected_slot = self


class Inventory:
    def __init__(self, creature):
        self.creature = creature
        self.is_left = False
        self.items = dict()
        self.is_visible = False
        self.close_button = Button(load_image("close.png", KEY_COLOR), self.close, 0, 0)
        self.slots = dict()
        for i in range(INVENTORY_DIMENTION):
            for j in range(INVENTORY_DIMENTION):
                self.slots[i, j] = Slot(creature,
                                        load_image("slot.png", resize=True,
                                                   size=(INVENTORY_ITEM_SIZE - INVENTORY_BORDER * 2)), 0, 0)

    def close(self):
        global right_side_menu_open
        if not self.is_left:
            right_side_menu_open = None
        self.is_visible = False

    def open(self, is_left=False):
        global right_side_menu_open
        if not is_left:
            if right_side_menu_open:
                right_side_menu_open.close()
            right_side_menu_open = self
        self.is_left = is_left
        self.is_visible = True

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
            self.slots[k] = Slot(creature, load_image("slot.png", resize=True, size=v[0]), v[1], v[2], k)
        self.is_visible = False
        self.close_button = Button(load_image("close.png", KEY_COLOR), self.close, WIDTH // 2, 0)

    def close(self):
        global right_side_menu_open
        right_side_menu_open = None
        self.is_visible = False

    def open(self):
        global right_side_menu_open
        if right_side_menu_open:
            right_side_menu_open.close()
        right_side_menu_open = self
        self.is_visible = True

    def assign_default(self, item, slot):
        if slot in self.slots.keys():
            self.slots[slot].assign_default(item)
            return True
        return False

    def assign(self, item, slot):
        self.slots[slot].assign(item)

    def drop_to_inventory(self, inventory):
        for k in self.slots.keys():
            inventory.add_item(self.slots[k].assigned_item())
            self.slots[k].assign(None)

    def reduce_damage(self, damage):
        if self.slots[SLOT_ARMOR].assigned_item():
            reduced_damage = self.slots[SLOT_ARMOR].assigned_item().reduce_damage(damage)
            return reduced_damage
        return damage

    def apply(self, slot, actor, creature):
        if slot in self.slots.keys() and self.slots[slot].assigned_item():
            item = self.slots[slot].assigned_item()
            if item.apply(actor, creature):
                self.slots[slot].assign(None)
                item.kill()

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
