import pygame
import smokesignal

from common import screen_map_group, landscape_group, obstacle_group, corpse_group
from inventory import Ammunition, Inventory
from settings import STEP, LOOT_RANGE, EVENT_MONSTER_DEAD, EVENT_DAMAGE_RECIEVED, EVENT_TRIGGER_RUN, ANIMATION_MOVE, \
    ANIMATION_DEATH, BUTTON_TO_SLOT
from utils import calculate_sprite_range


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, groups):
        super().__init__(screen_map_group, *groups)
        self.image = image
        self.rect = self.image.get_rect().move(x, y)

    def set_position(self, x, y):
        self.rect = self.rect.move(int(x), int(y))


class AnimatedTile(Tile):
    def __init__(self, animations, start_animation_name, pos_x, pos_y, groups):
        self.animations = animations
        self.animation = animations[start_animation_name]
        super().__init__(self.animation.images[0], pos_x, pos_y, groups)

    def get_animation(self):
        return self.animation

    def update(self, screen):
        image, changed = self.animation.tick()
        if changed:
            self.image = image
            self.rect = self.image.get_rect(center=self.rect.center)
            self.animation_tick(self.animation)

    def change_animation(self, name):
        if self.animation != self.animations[name] or self.animation.is_pause:
            self.animation = self.animations[name]
            self.animation.start()

    def animation_tick(self, animation):
        pass


class Background(Tile):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(image, pos_x, pos_y, [landscape_group])


class AnimatedObstacle(AnimatedTile):
    def __init__(self, animations, start_animation_name, pos_x, pos_y):
        super().__init__(animations, start_animation_name, int(pos_x), int(pos_y), [obstacle_group])
        self.get_animation().start()


class Obstacle(Tile):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(image, int(pos_x), int(pos_y), [obstacle_group])


class Movable(AnimatedTile):
    def __init__(self, animations, pos_x, pos_y, groups):
        self.speed = STEP
        self.move_vector = (0, -1)
        start_animation_name = "_".join([ANIMATION_MOVE, "0", "-1"])
        super().__init__(animations, start_animation_name, pos_x, pos_y, [obstacle_group] + groups)

    def step(self, dx, dy):
        if dx or dy:
            self.move_vector = (dx, dy)
            self.change_animation("_".join([ANIMATION_MOVE, str(dx), str(dy)]))

    def step_part(self, dx, dy):
        x, y = self.rect.x, self.rect.y
        self.rect.x += dx
        self.rect.y += dy

        obstacle_group.remove(self)
        collides = pygame.sprite.spritecollide(self, obstacle_group, False, pygame.sprite.collide_mask)
        obstacle_group.add(self)
        if collides:
            self.rect.x, self.rect.y = x, y
            return False
        return True

    def animation_tick(self, animation):
        if animation.name.startswith("move"):
            dx, dy = self.move_vector
            if dx != 0 and dy != 0:
                step = int(((self.speed ** 2) // 2) ** 0.5)
            else:
                step = self.speed
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
        self.dead = self.health_points == 0

    def is_dead(self):
        return self.dead

    def get_inventory(self):
        return self.inventory

    def get_ammunition(self):
        return self.ammunition

    def render_health(self, screen):
        if not self.is_dead():
            rect = pygame.Rect(0, 0, 50, 7)
            rect.midbottom = self.rect.centerx, self.rect.top - self.rect.height // 5
            pygame.draw.rect(screen, (255, 0, 0), (*rect.bottomleft, *rect.size))
            pygame.draw.rect(screen, (0, 0, 0), (*rect.bottomleft, *rect.size), 1)
            pos = (rect.bottomleft[0] + 1, rect.bottomleft[1] + 1)
            size = (round((rect.size[0] - 2) * self.health_points / self.max_health_points), rect.size[1] - 2)
            pygame.draw.rect(screen, (0, 255, 0), (*pos, *size))

    def update(self, screen):
        super().update(screen)
        self.inventory.update(screen)
        self.ammunition.update(screen)
        self.render_health(screen)

    def recieve_damage(self, damage):
        clean_damage = self.ammunition.reduce_damage(damage)
        smokesignal.emit(EVENT_DAMAGE_RECIEVED, type(self).__name__, damage, clean_damage)
        if clean_damage > 0:
            self.health_points -= min([clean_damage, self.health_points])
        if not self.health_points:
            self.dead = True
            self.change_animation(ANIMATION_DEATH)
            corpse_group.add(self)
            obstacle_group.remove(self)
            self.ammunition.drop_to_inventory(self.inventory)
            smokesignal.emit(EVENT_MONSTER_DEAD, type(self).__name__)

    def recieve_heal(self, hp):
        self.health_points += hp
        self.health_points = min(self.health_points, self.max_health_points)

    def get_health_points(self):
        return self.health_points

    def step(self, dx, dy):
        if not self.is_dead():
            super().step(dx, dy)

    def apply(self, creature, slot):
        can_apply = self.__can_apply(creature, slot)
        if can_apply:
            animation_type = self.ammunition.get_slot_animation_type(slot)
            if animation_type:
                super().change_animation("_".join([animation_type, "0", "-1"]))
            # self.ammunition.apply(slot, self, creature)
            slot_object = self.ammunition.get_slot(slot)
            if slot_object:
                item = slot_object.assigned_item()
                if item:
                    item.apply(self, creature)
        return can_apply

    def __can_apply(self, creature, slot):
        if self.is_dead():
            return
        slot_object = self.ammunition.get_slot(slot)
        if slot_object:
            item = slot_object.assigned_item()
            if item:
                return item.can_apply(self, creature)
        return False

    def loot(self, creature):
        if self.is_dead():
            return
        if calculate_sprite_range(self, creature) < LOOT_RANGE:
            creature.get_inventory().open()

    def handle_click(self, enemy, button):
        if issubclass(enemy.__class__, Creature) and enemy.is_dead():
            self.loot(enemy)
        else:
            self.apply(enemy, BUTTON_TO_SLOT[button])


class Trigger(Obstacle):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(image, pos_x, pos_y)

    def run(self, key):
        smokesignal.emit(EVENT_TRIGGER_RUN, type(self).__name__, type(key).__name__)











