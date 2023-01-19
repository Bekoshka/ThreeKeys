from items import *
from buttons import Button
from common import buttons_group, slots_group, items_group, mouse

from settings import WIDTH, HEIGHT, SLOT_RIGHT_HAND, SLOT_LEFT_HAND, EVENT_ITEM_ASSIGNED

import pygame

from settings import SLOT_ARMOR, KEY_COLOR
from utils import load_image

selected_slot = None
right_side_menu_open = None
description_slot = None

INVENTORY_DIMENTION = 5
INVENTORY_BORDER = 10
INVENTORY_ITEM_SIZE = WIDTH // 10
AMMUNITION_SLOTS = {
    SLOT_ARMOR: (WIDTH // 2 + WIDTH // 4 - INVENTORY_ITEM_SIZE // 2, HEIGHT // 4),
    SLOT_RIGHT_HAND: (WIDTH // 2 + WIDTH // 4 - INVENTORY_ITEM_SIZE * 1.5, HEIGHT // 2),
    SLOT_LEFT_HAND: (WIDTH // 2 + WIDTH // 4 + INVENTORY_ITEM_SIZE * 0.5, HEIGHT // 2)
}


class Slot(pygame.sprite.Sprite):
    def __init__(self, id, creature, images, x=0, y=0, type=None):
        super().__init__()
        self.id = id
        self.creature = creature
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect().move(x, y)
        self.item = None
        self.default_item = None
        self.type = type

    def update(self, _):
        global selected_slot
        self.image = self.images[self == selected_slot]

    def assigned_item(self):
        if self.item:
            return self.item
        else:
            if self.default_item:
                return self.default_item
        return None

    def can_drop(self):
        return bool(self.item)

    def assign(self, item):
        if self.can_assign_item(item):
            if self.item is None and self.default_item:
                self.default_item.kill()
            self.item = item
            count = 0
            if item:
                count = item.get_count()
            smokesignal.emit(EVENT_ITEM_ASSIGNED, self.creature, self.id, item, count)

    def can_assign_item(self, item):
        if item is None:
            return True
        if self.type is None:
            return True
        return item.slot_type & self.type

    def assign_default(self, item):
        self.default_item = item

    def handle_click(self, button, union=False, divide=False):
        global selected_slot
        global description_slot
        x, y = mouse.get_pos()
        if button == 1:
            if selected_slot:
                if not (union or divide):
                    i = self.item
                    si = selected_slot.item
                    if selected_slot.can_assign_item(i) and self.can_assign_item(si):
                        selected_slot.assign(i)
                        self.assign(si)
                        selected_slot = None
                elif union ^ divide:
                    i = self.item
                    si = selected_slot.item
                    if si:
                        if self.can_assign_item(si):
                            si, i = si.transfer(i, union)
                            selected_slot.assign(si)
                            self.assign(i)
                    if union:
                        selected_slot = None
            else:
                selected_slot = self
        elif button == 2:
            description_slot = (self, x, y)
        elif button == 3:
            if self.item:
                self.item.apply(self.creature, self.creature)

    @staticmethod
    def clean_description():
        global description_slot
        description_slot = None

    @staticmethod
    def render_description(screen):
        global description_slot
        if description_slot:
            slot, x, y = description_slot
            item = slot.assigned_item()
            if item:
                blits = []
                max_width = 0
                max_height = 0
                for i, text in enumerate(item.description.split('\n')):
                    bg_color = pygame.Color('white')
                    image = pygame.font.Font(None, 30).render(text, True, pygame.Color('black'), bg_color)
                    rect = image.get_rect()
                    rect.topleft = x, 20 + y + i * rect.height
                    max_width = max([max_width, rect.width])
                    max_height = max([max_height, rect.height])
                    blits.append((image, rect))
                r = (x, 20 + y, max_width, max_height * len(blits))
                pygame.draw.rect(screen, bg_color, pygame.Rect(*r))
                for i in blits:
                    screen.blit(*i)


class Container:
    def __init__(self, is_left):
        self.close_button = Button(load_image("close.png", KEY_COLOR), self.close)
        self.__slots = dict()
        self.__is_left = is_left
        self.__is_visible = False

    def _get_slot_keys(self):
        return self.__slots

    def _get_slot(self, slot):
        return self.__slots[slot]

    def _add_slot(self, name, creature, x=0, y=0, type=None):
        images = [
            load_image("slot.png", resize=True, size=(INVENTORY_ITEM_SIZE - INVENTORY_BORDER * 2)),
            load_image("slot_.png", resize=True, size=(INVENTORY_ITEM_SIZE - INVENTORY_BORDER * 2))
        ]
        self.__slots[name] = Slot(name, creature, images, x, y, type)

    def clean(self):
        self.close()
        self._clean()

    def close(self):
        global right_side_menu_open
        if not self.__is_left:
            right_side_menu_open = None
        self.__is_visible = False

    def open(self, is_left=False):
        global right_side_menu_open
        if not is_left:
            if right_side_menu_open:
                right_side_menu_open.close()
            right_side_menu_open = self
        self.__is_left = is_left
        self.__is_visible = True

    def _clean(self):
        global selected_slot
        self.close_button.kill()
        for slot in self.__slots.values():
            slot.kill()
            if slot == selected_slot:
                selected_slot = None
            item = slot.assigned_item()
            if item:
                item.kill()

    def get_slot_animation_type(self, slot):
        item = self.__slots[slot].assigned_item()
        if item:
            return item.get_animation_type()
        return None

    def update(self, screen):
        global selected_slot
        if not self.__is_visible:
            self._clean()
            return
        x = 0 if self.__is_left else WIDTH // 2
        pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(x, 0, WIDTH // 2, HEIGHT))

        if buttons_group not in self.close_button.groups():
            buttons_group.add(self.close_button)
        self.close_button.rect.x = x

        for k in self.__slots.keys():
            slot = self.__slots[k]
            if slots_group not in slot.groups():
                slots_group.add(slot)
            rect = slot.rect
            if isinstance(k, tuple):
                i, j = k
                rect.x = INVENTORY_BORDER + x + INVENTORY_ITEM_SIZE * j
                rect.y = INVENTORY_BORDER + (
                        HEIGHT - INVENTORY_ITEM_SIZE * INVENTORY_DIMENTION) // 2 + INVENTORY_ITEM_SIZE * i
            item = slot.assigned_item()
            if item and item.is_empty():
                slot.assign(None)
                item.kill()
                item = None
            if item:
                item.rect.centerx = rect.centerx
                item.rect.centery = rect.centery
                if items_group not in item.groups():
                    items_group.add(item)

    def get_slot_by_name(self, slot):
        if slot in self.__slots.keys():
            return self.__slots[slot]
        return None


class Inventory(Container):
    def __init__(self, creature):
        super().__init__(False)
        self.creature = creature
        for i in range(INVENTORY_DIMENTION):
            for j in range(INVENTORY_DIMENTION):
                self._add_slot((i, j), creature)

    def add_item(self, item):
        for i in range(INVENTORY_DIMENTION):
            for j in range(INVENTORY_DIMENTION):
                slot = self._get_slot((i, j))
                slot_item = slot.assigned_item()
                if slot_item:
                    continue
                slot.assign(item)
                return True
        return False


class Ammunition(Container):
    def __init__(self, creature):
        super().__init__(False)
        self.creature = creature
        for k in AMMUNITION_SLOTS.keys():
            x, y = AMMUNITION_SLOTS[k]
            self._add_slot(k, creature, x, y, k)

    def assign_default(self, item, slot):
        if slot in self._get_slot_keys():
            self._get_slot(slot).assign_default(item)
            return True
        return False

    def assign(self, item, slot):
        self._get_slot(slot).assign(item)

    def drop_to_inventory(self, inventory):
        for k in self._get_slot_keys():
            slot = self._get_slot(k)
            if slot.can_drop():
                inventory.add_item(slot.assigned_item())
                slot.assign(None)

    def reduce_damage(self, damage):
        slot = self._get_slot(SLOT_ARMOR)
        if slot.assigned_item():
            reduced_damage = slot.assigned_item().reduce_damage(damage)
            return reduced_damage
        return damage
