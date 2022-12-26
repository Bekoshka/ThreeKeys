import pygame

from common import all_sprites, landscape_sprites, obstacle_group
from settings import tile_width, tile_height, STEP


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
        self.move_images = images[(0, -1)]
        self.move_image_idx = 0
        super().__init__(self.move_images[0], pos_x, pos_y, groups)
        self.all_move_images = images

    def step(self, dx, dy):
        if dx != 0 and dy != 0:
            step = int(((STEP ** 2) // 2) ** 0.5)
        else:
            step = STEP
        self.rotate_image_safe(dx, dy)
        self.animate_step_safe()
        for i in range(step):
            if self.step_part(abs(dx * step - i) * dx, abs(dy * step - i) * dy):
                break

    def step_part(self, dx, dy):
        x, y = self.rect.x, self.rect.y
        self.rect.x += dx
        self.rect.y += dy
        if pygame.sprite.spritecollide(self, obstacle_group, False, pygame.sprite.collide_mask):
            self.rect.x, self.rect.y = x, y
            return False
        return True

    def rotate_image_safe(self, dx, dy):
        self.move_images = self.all_move_images[(dx, dy)]

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

