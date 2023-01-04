import pygame

from common import screen_map_group, landscape_group, obstacle_group
from inventory import Ammunition, Inventory
from settings import tile_width, tile_height, STEP, LOOT_RANGE
from utils import calculate_sprite_range


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
        super().__init__(screen_map_group, *groups)
        self.image = image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Background(Tile):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(image, pos_x, pos_y, [landscape_group])


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
        self.ammunition = Ammunition(self)
        self.inventory = Inventory(self)

    def get_inventory(self):
        return self.inventory

    def get_ammunition(self):
        return self.ammunition

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
        self.inventory.update(screen)
        self.ammunition.update(screen)

    def recieve_damage(self, damage):
        clean_damage = self.ammunition.reduce_damage(damage)
        print(damage, "->", clean_damage)
        if clean_damage > 0:
            self.health_points -= min([clean_damage, self.health_points])

    def recieve_heal(self, hp):
        self.health_points += hp
        self.health_points = min(self.health_points, self.max_health_points)

    def get_health_points(self):
        return self.health_points

    def step(self, dx, dy):
        if self.health_points:
            super().step(dx, dy)

    def apply(self, creature, slot):
        if not self.health_points:
            return
        if not creature.get_health_points():
            return
        super().change_animation(0, 0, 1)
        self.ammunition.apply(slot, self, creature)

    def can_apply(self, creature, slot):
        if not self.health_points:
            return False
        if not creature.get_health_points():
            return False
        return self.ammunition.can_apply(slot, self, creature)

    def loot(self, creature):
        if not self.health_points:
            return
        if calculate_sprite_range(self, creature) < LOOT_RANGE:
            creature.get_inventory().set_visibility(True)

    def apply_or_loot(self, enemy, slot):
        if not enemy.get_health_points():
            self.loot(enemy)
        else:
            self.apply(enemy, slot)














