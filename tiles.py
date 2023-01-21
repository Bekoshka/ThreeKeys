import pygame
import smokesignal

from camera import camera
from common import landscape_group, obstacle_group, corpse_group, mouse, creature_group, animated_obstacle_group
from inventory import Ammunition, Inventory
from settings import DEFAULT_STEP, DEFAULT_LOOT_RANGE
from globals import EVENT_MONSTER_DEAD, EVENT_DAMAGE_RECIEVED, EVENT_TRIGGER_RUN, ANIMATION_MOVE, \
    ANIMATION_DEATH, SLOT_LEFT_HAND, SLOT_RIGHT_HAND, ANIMATION_MOVE_PREFIX
from utils import calculate_sprite_range, get_vector, load_sound

BUTTON_TO_SLOT = {
    3: SLOT_LEFT_HAND,
    1: SLOT_RIGHT_HAND
}


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, groups):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect().move(x, y)

    def set_position(self, x, y):
        self.rect.topleft = (int(x), int(y))


class Trigger(Tile):
    def __init__(self, image, x, y, groups):
        super().__init__(image, x, y, groups)

    def run_trigger(self, key):
        smokesignal.emit(EVENT_TRIGGER_RUN, self, key)


class AnimatedTile(Trigger):
    def __init__(self, animations, start_animation_name, pos_x, pos_y, groups):
        self.__animations = animations
        self.__animation = animations[start_animation_name]
        super().__init__(self.__animation.get_image(), pos_x, pos_y, groups)

    def update(self, screen):
        image, changed = self.__animation.tick()
        if changed:
            self.image = image
            self.rect = self.image.get_rect(center=self.rect.center)
            self._animation_tick(self.__animation)

    def _get_animation(self):
        return self.__animation

    def _change_animation(self, name):
        if self.__animation != self.__animations[name]:
            self.__animation = self.__animations[name]
            self.__animation.start()

    def _animation_tick(self, animation):
        pass


class Background(Tile):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(image, pos_x, pos_y, [landscape_group])


class AnimatedObstacle(AnimatedTile):
    def __init__(self, animations, start_animation_name, pos_x, pos_y):
        super().__init__(animations, start_animation_name, int(pos_x), int(pos_y),
                         [animated_obstacle_group, obstacle_group])
        self._get_animation().start()


class Obstacle(Trigger):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(image, int(pos_x), int(pos_y), [obstacle_group])


class Movable(AnimatedTile):
    def __init__(self, animations, pos_x, pos_y, step_size=DEFAULT_STEP, groups=None):
        if groups is None:
            groups = []
        self.__step_size = step_size
        self.__move_vector = (0, -1)
        self.__sound = load_sound("step.mp3")
        start_animation_name = "_".join([ANIMATION_MOVE, "0", "-1"])
        super().__init__(animations, start_animation_name, pos_x, pos_y, groups + [obstacle_group])

    def _add_step_size(self, ds):
        self.__step_size += ds
        if self.__step_size <= 0:
            self.__step_size = 0

    def step(self, dx, dy):
        if dx or dy:
            self.__move_vector = (dx, dy)
            animation = "_".join([ANIMATION_MOVE, str(dx), str(dy)])
            if self._get_animation().get_name().startswith(ANIMATION_MOVE_PREFIX):
                self._change_animation(animation)
                if self._get_animation().is_pause():
                    self._get_animation().start()
                    self.__sound.play()
            else:
                if self._get_animation().is_pause():
                    self._change_animation(animation)
                    self.__sound.play()
        else:
            if self._get_animation().get_name().startswith(ANIMATION_MOVE_PREFIX):
                self._get_animation().stop()

    def __try_step(self, dx, dy):
        pos = self.rect.topleft
        self.rect.x += dx
        self.rect.y += dy

        obstacle_group.remove(self)
        copy = obstacle_group.filtered_copy()
        collides = pygame.sprite.spritecollide(self, copy, False, pygame.sprite.collide_mask)
        copy.empty()
        obstacle_group.add(self)
        if collides:
            self.rect.topleft = pos
            return False
        return True

    def _animation_tick(self, animation):
        if animation.get_name().startswith(ANIMATION_MOVE_PREFIX):
            dx, dy = self.__move_vector
            if dx != 0 and dy != 0:
                step = int(((self.__step_size ** 2) // 2) ** 0.5)
            else:
                step = self.__step_size
            self.__try_step(abs(dx * step) * dx, abs(dy * step) * dy)


class Creature(Movable):
    def __init__(self, animations, max_health_points, pos_x, pos_y, lootable=False, step_size=DEFAULT_STEP):
        super().__init__(animations, pos_x, pos_y, step_size=step_size, groups=[creature_group])
        self.__health_points = self.__max_health_points = max_health_points
        self.__ammunition = Ammunition(self)
        self.__inventory = Inventory(self)
        self.__dead = self.__health_points == 0
        self.__lootable = lootable

    def set_lootable(self, lootable):
        self.__lootable = lootable

    def clean(self):
        self.__ammunition.clean()
        self.__inventory.clean()

    def is_dead(self):
        return self.__dead

    def get_inventory(self):
        return self.__inventory

    def get_ammunition(self):
        return self.__ammunition

    def __render_health(self, screen):
        if not self.__dead:
            rect = pygame.Rect(0, 0, 50, 7)
            rect_t = camera.translate(self.rect)
            rect.midbottom = rect_t.centerx, rect_t.top - rect_t.height // 5
            pygame.draw.rect(screen, (255, 0, 0), (*rect.bottomleft, *rect.size))
            pygame.draw.rect(screen, (0, 0, 0), (*rect.bottomleft, *rect.size), 1)
            pos = (rect.bottomleft[0] + 1, rect.bottomleft[1] + 1)
            size = (round((rect.size[0] - 2) * self.__health_points / self.__max_health_points), rect.size[1] - 2)
            pygame.draw.rect(screen, (0, 255, 0), (*pos, *size))

    def update(self, screen):
        self.__render_health(screen)
        super().update(screen)
        self.__inventory.update(screen)
        self.__ammunition.update(screen)

    def recieve_damage(self, damage):
        clean_damage = self.__ammunition.reduce_damage(damage)
        smokesignal.emit(EVENT_DAMAGE_RECIEVED, self, damage, clean_damage)
        if clean_damage > 0:
            self.__health_points -= min([clean_damage, self.__health_points])
        if not self.__health_points:
            self.__dead = True
            self.__lootable = True
            self._change_animation(ANIMATION_DEATH)
            corpse_group.add(self)
            obstacle_group.remove(self)
            self.__ammunition.drop_to_inventory(self.__inventory)
            smokesignal.emit(EVENT_MONSTER_DEAD, self)

    def recieve_heal(self, hp):
        self.__health_points += hp
        self.__health_points = min(self.__health_points, self.__max_health_points)

    def recieve_speed(self, agility):
        self._add_step_size(agility)

    def step(self, dx, dy):
        if not self.__dead:
            super().step(dx, dy)

    def apply(self, creature, slot):
        can_apply = self.__can_apply(creature, slot)
        if can_apply:
            animation_type = self.__ammunition.get_slot_animation_type(slot)
            if animation_type:
                vector = [str(x) for x in get_vector(self.rect.x, self.rect.y, *mouse.get_pos())]
                self._change_animation("_".join([animation_type, *vector]))
            sound = self.__ammunition.get_slot_sound(slot)
            if sound:
                sound.play()
            slot_object = self.__ammunition.get_slot_by_name(slot)
            if slot_object:
                item = slot_object.assigned_item()
                if item:
                    item.apply(self, creature)
        return can_apply

    def __can_apply(self, creature, slot):
        if self.__dead:
            return False
        if not self._get_animation().get_name().startswith(
                ANIMATION_MOVE_PREFIX) and not self._get_animation().is_pause():
            return False
        slot_object = self.__ammunition.get_slot_by_name(slot)
        if slot_object:
            item = slot_object.assigned_item()
            if item:
                return item.can_apply(self, creature)
        return False

    def show_loot(self, creature):
        can_loot = self.__can_loot(creature)
        if can_loot:
            creature.get_inventory().open()
        return can_loot

    def __can_loot(self, creature):
        return not self.__dead and hasattr(creature, 'show_loot') and callable(getattr(creature, 'show_loot')) \
               and creature.__lootable and calculate_sprite_range(self, creature) < DEFAULT_LOOT_RANGE

    def handle_click(self, obstacle, button):
        if button == 2:
            return self.show_loot(obstacle)
        elif button in (1, 3):
            return self.apply(obstacle, BUTTON_TO_SLOT[button])
