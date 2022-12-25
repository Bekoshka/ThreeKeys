import pygame

from common import all_sprites, landscape_sprites, obstacle_group
from settings import tile_width, tile_height


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
    def __init__(self, images, pos_x, pos_y, groups):
        super().__init__(images[0], pos_x, pos_y, groups)
        self.move_images = images
        self.move_image_idx = 0

    def move(self, dx, dy, step):
        if dx == 0 and dy == 0:
            return
        self.animate_step_safe()
        self.rotate_image_safe(self.calculate_angle(dx, dy))

        dx_sign = dx // step
        dy_sign = dy // step
        for i in range(step):
            if self.move_part(abs(dx - i) * dx_sign, abs(dy - i) * dy_sign):
                break

    def move_part(self, dx, dy):
        x, y = self.rect.x, self.rect.y
        self.rect.x += dx
        self.rect.y += dy
        if pygame.sprite.spritecollide(self, obstacle_group, False, pygame.sprite.collide_mask):
            self.rect.x, self.rect.y = x, y
            return False
        return True

    @staticmethod
    def calculate_angle(dx, dy):
        if dy == 0 and dx != 0:
            if dx > 0:
                angle = -90
            else:
                angle = 90
        elif dx == 0 and dy != 0:
            if dy > 0:
                angle = 180
            else:
                angle = 0
        else:
            if dy > 0:
                if dx > 0:
                    angle = -135
                else:
                    angle = 135
            else:
                if dx > 0:
                    angle = -45
                else:
                    angle = 45
        return angle

    def rotate_image(self, angle):
        self.image = pygame.transform.rotate(self.move_images[self.move_image_idx], angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def rotate_image_safe(self, angle):
        safe_angle = angle
        self.rotate_image(angle)
        if pygame.sprite.spritecollide(self, obstacle_group, False, pygame.sprite.collide_mask):
            self.rotate_image(safe_angle)

    def animate_step(self, idx):
        self.move_image_idx = idx
        self.image = self.move_images[idx]
        self.rect = self.image.get_rect(center=self.rect.center)

    def animate_step_safe(self):
        safe_image_idx = self.move_image_idx
        self.animate_step((safe_image_idx + 1) % len(self.move_images))
        if pygame.sprite.spritecollide(self, obstacle_group, False, pygame.sprite.collide_mask):
            self.animate_step(safe_image_idx)


class Creature(Movable):
    def __init__(self, move_images, max_health_points, pos_x, pos_y, groups):
        super().__init__(move_images, pos_x, pos_y, groups)
        self.health_points = self.max_health_points = max_health_points
        self.health_points = self.max_health_points // 3

    def render_health(self, screen):
        rect = pygame.Rect(0, 0, tile_width, 7)
        rect.midbottom = self.rect.centerx, self.rect.top - tile_height // 5
        pygame.draw.rect(screen, (255, 0, 0), (*rect.bottomleft, *rect.size))
        pygame.draw.rect(screen, (0, 0, 0), (*rect.bottomleft, *rect.size), 1)
        pos = (rect.bottomleft[0] + 1, rect.bottomleft[1] + 1)
        size = (round((rect.size[0] - 2) * self.health_points / self.max_health_points), rect.size[1] - 2)
        pygame.draw.rect(screen, (0, 255, 0), (*pos, *size))

    def update(self, screen):
        self.render_health(screen)

    def calculate_damage(self, attacker):
        pass


class Attackable(Movable):
    def __init__(self, move_images, attack_image, pos_x, pos_y, groups):
        super().__init__(move_images, pos_x, pos_y, groups)
        self.attack_image = attack_image

    def attack(self):
        self.image = self.attack_image
        self.rect = self.image.get_rect(center=self.rect.center)

