import pygame

from group import CameraGroup
from settings import WIDTH, HEIGHT
from ticker import TickCounter
from mouse import Mouse


landscape_group = CameraGroup()
obstacle_group = CameraGroup()
corpse_group = CameraGroup()

animated_obstacle_group = CameraGroup((WIDTH // 2, HEIGHT // 2))
creature_group = CameraGroup((WIDTH // 2, HEIGHT // 2))

window_groups = pygame.sprite.Group()
buttons_group = pygame.sprite.Group()
slots_group = pygame.sprite.Group()
items_group = pygame.sprite.Group()

mouse = Mouse()
tick_counter = TickCounter()
