"""Main module of game"""

import pygame
import sys
import HelloMenu
from pygame.locals import *

pygame.init()
pygame.display.set_caption('Scr@bble')

czy = True


def input(events):
    """Check if program should stop"""
    for event in events:
        if event.type == QUIT:
            czy = False
            print('nope')
            sys.exit(0)
            pygame.quit()
        else:
            print(event)


input(pygame.event.get())
app = HelloMenu.HelloMenu()

if czy:
    app.start()
else:
    pygame.quit()
