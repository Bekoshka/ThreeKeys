import pygame

from groups import CameraGroup
from utils import Mouse


landscape_group = CameraGroup()
obstacle_group = CameraGroup()
corpse_group = CameraGroup()

animated_obstacle_group = pygame.sprite.Group()
creature_group = pygame.sprite.Group()

buttons_group = pygame.sprite.Group()
slots_group = pygame.sprite.Group()
items_group = pygame.sprite.Group()

mouse = Mouse()
