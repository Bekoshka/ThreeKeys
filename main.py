import pygame

from screen import StartScreen, GameScreen, FailScreen, WinScreen
from settings import SIZE, GAME_PAUSED, GAME_FAILED, GAME_COMPLETED

pygame.init()
# pygame.key.set_repeat(200, 70)

screen = pygame.display.set_mode(SIZE)

menu = StartScreen(screen)
fail = FailScreen(screen)
win = WinScreen(screen)
game = GameScreen(screen)
while True:
    while True:
        menu.run()
        game.run()
        status = game.get_status()
        if status == GAME_PAUSED:
            continue
        break
    if status == GAME_FAILED:
        fail.run()
    elif status == GAME_COMPLETED:
        win.run()
    game.clean()
    game = GameScreen(screen)





# GAME_RUNNING = 0
# GAME_PAUSED = 1
# GAME_FAILED = 2
# GAME_COMPLETED = 3