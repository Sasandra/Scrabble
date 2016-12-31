"""Main module of game"""

import sys

import pygame
from pygame.locals import *
from Back import PlayerData
from Front import HelloMenu
from Front import MainMenu
from Front import  ComputerMode

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

if czy:
    name = HelloMenu.HelloMenu().start()
    if name:
        player = PlayerData.Player(name)
        print(player.name)
        mode = MainMenu.MainMenu().start()
        if mode == 'computer':
            ComputerMode.ComputerMode(player).start()
        else:
            print('nope')
else:
    pygame.quit()
