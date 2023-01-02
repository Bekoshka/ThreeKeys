from math import sqrt
from random import randrange

import pygame

from common import all_sprites, landscape_sprites, obstacle_group
from settings import tile_width, tile_height, STEP


class Animation:
    def __init__(self, images, mod, is_loop=False):
        self.is_loop = is_loop
        self.is_pause = True
        self.mod = mod
        self.images = images
        self.images_idx = 0
        self.tick_counter = 0

    def tick(self):
        image = self.images[self.images_idx]
        changed = False
        if not self.is_pause:
            if self.tick_counter % self.mod == 0:
                self.images_idx = (self.images_idx + 1) % len(self.images)
                changed = True
                if self.images_idx == 0:
                    if not self.is_loop:
                        self.is_pause = True
        self.tick_counter += 1
        return image, changed

    def start(self):
        self.is_pause = False

    def stop(self):
        self.is_pause = True


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y, groups):
        super().__init__(all_sprites, *groups)
        self.image = image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Background(Tile):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(image, pos_x, pos_y, [landscape_sprites])


class Obstacle(Tile):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(image, pos_x, pos_y, [obstacle_group])


class Movable(Tile):
    def __init__(self, animations, pos_x, pos_y, groups):
        self.animation_speed = 40
        self.animations = animations
        self.animation = animations[0, -1]
        self.move_vector = (0, -1)
        super().__init__(animations[0, -1].images[0], pos_x, pos_y, groups)

    def step(self, dx, dy):
        if dx or dy:
            self.change_animation(dx, dy, 0)

    def step_part(self, dx, dy):
        x, y = self.rect.x, self.rect.y
        self.rect.x += dx
        self.rect.y += dy
        if pygame.sprite.spritecollide(self, obstacle_group, False, pygame.sprite.collide_mask):
            self.rect.x, self.rect.y = x, y
            return False
        return True

    def change_animation(self, dx, dy, mod):
        self.mod = mod
        if self.move_vector != (dx, dy) or self.animation.is_pause:
            self.move_vector = (dx, dy)
            self.animation = self.animations[dx, dy]
            self.animation.start()

    def update(self):
        image, changed = self.animation.tick()
        if changed:
            self.image = image
            self.rect = self.image.get_rect(center=self.rect.center)
            if self.mod == 0:
                dx, dy = self.move_vector
                if dx != 0 and dy != 0:
                    step = int(((STEP ** 2) // 2) ** 0.5)
                else:
                    step = STEP
                for i in range(step):
                    if self.step_part(abs(dx * step - i) * dx, abs(dy * step - i) * dy):
                        break


class Creature(Movable):
    def __init__(self, animations, max_health_points, pos_x, pos_y, groups):
        super().__init__(animations, pos_x, pos_y, groups)
        self.health_points = self.max_health_points = max_health_points
        self.health_points = self.max_health_points
        self.armor = 10
        self.ammunition = Ammunition()

    def render_health(self, screen):
        rect = pygame.Rect(0, 0, tile_width, 7)
        rect.midbottom = self.rect.centerx, self.rect.top - tile_height // 5
        pygame.draw.rect(screen, (255, 0, 0), (*rect.bottomleft, *rect.size))
        pygame.draw.rect(screen, (0, 0, 0), (*rect.bottomleft, *rect.size), 1)
        pos = (rect.bottomleft[0] + 1, rect.bottomleft[1] + 1)
        size = (round((rect.size[0] - 2) * self.health_points / self.max_health_points), rect.size[1] - 2)
        pygame.draw.rect(screen, (0, 255, 0), (*pos, *size))

    def update(self, screen):
        super().update()
        if self.health_points:
            self.render_health(screen)

    def recieve_damage(self, damage):
        clean_damage = self.ammunition.reduce_damage(damage)
        if clean_damage > 0:
            self.health_points -= min([clean_damage, self.health_points])
        if not self.health_points:
            self.kill()

    def increase_hp(self, hp):
        self.health_points += hp
        self.health_points = min(self.health_points, self.max_health_points)

    def attack(self, enemy, button):
        super().change_animation(0, 0, 1)
        desired_slot = 0
        if button in BUTTON_TO_SLOT.keys():
            desired_slot = BUTTON_TO_SLOT[button]
        self.ammunition.apply(desired_slot, self, enemy)


class Item:
    def __init__(self, name, description, image, slot_type):
        self.name = name
        self.description = description
        self.image = image
        self.slot_type = slot_type


    # def take_to_inventory(self):


class Inventory:
    def __init__(self, item):
        self.item = item
        self.items = []

    def add_item(self):
        self.items.append(self.item)

    # def drop_item(self):
    #     self.items.append(self.item)

SLOT_ARMOR = 1
SLOT_LEFT_HAND = 2
SLOT_RIGHT_HAND = 4

BUTTON_TO_SLOT = {
    1: SLOT_LEFT_HAND,
    2: SLOT_ARMOR,
    3: SLOT_RIGHT_HAND
}


class Ammunition:
    def __init__(self):
        self.slots = dict()
        self.slots[SLOT_ARMOR] = None
        self.slots[SLOT_LEFT_HAND] = None
        self.slots[SLOT_RIGHT_HAND] = None

    def assign(self, item, button):
        desired_slot = 0
        if button in BUTTON_TO_SLOT.keys():
            desired_slot = BUTTON_TO_SLOT[button]
        if item.slot_type & desired_slot:
            self.slots[desired_slot] = item

    def reduce_damage(self, damage):
        print(self.slots[SLOT_ARMOR], "amm reduce_damage")
        if self.slots[SLOT_ARMOR]:
            reduced_damage = self.slots[SLOT_ARMOR].reduce_damage(damage)
            print(reduced_damage, damage)
            return reduced_damage
        return damage

    def apply(self, slot, actor, creature):
        if slot in self.slots.keys() and self.slots[slot]:
            self.slots[slot].apply(actor, creature)


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
        c = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
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

    def apply(self, actor, creature):
        creature.increase_hp(self.heal_points)











