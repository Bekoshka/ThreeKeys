import corpse as corpse
import pygame

screen_map_group = pygame.sprite.Group()
landscape_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
corpse_group = pygame.sprite.Group()
monster_group = pygame.sprite.Group()  # invisible

buttons_group = pygame.sprite.Group()
slots_group = pygame.sprite.Group()
items_group = pygame.sprite.Group()

selected_slot = None
right_side_menu_open = None
