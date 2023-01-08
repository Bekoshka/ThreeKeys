import pygame

screen_map_group = pygame.sprite.Group()
landscape_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
monster_group = pygame.sprite.Group()

buttons_group = pygame.sprite.Group()
slots_group = pygame.sprite.Group()
items_group = pygame.sprite.Group()

selected_slot = None
right_side_menu_open = None


def init_common():
    # global screen_map_group
    # global landscape_group
    # global obstacle_group
    # global obstacle_group
    # global player_group
    # global monster_group
    # global buttons_group
    # global slots_group
    # global items_group
    # global selected_slot
    # global right_side_menu_open

    screen_map_group.empty()
    landscape_group.empty()
    obstacle_group.empty()
    player_group.empty()
    monster_group.empty()

    buttons_group.empty()
    slots_group.empty()
    items_group.empty()

