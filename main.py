import pygame

from screen import StartScreen, Game
from settings import size

pygame.init()
pygame.key.set_repeat(200, 70)

screen = pygame.display.set_mode(size) 

StartScreen(screen).run()
Game(screen).run()
