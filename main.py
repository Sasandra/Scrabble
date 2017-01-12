"""Main module of game"""

import sys

import pygame
from pygame.locals import *
from Back import PlayerData
from Back import LettersSet
from Back import WordsList
from Back import BoardData
from Front import HelloMenu
from Front import MainMenu
from Front import ComputerMode
from Back import Game

pygame.init()
pygame.display.set_caption('Scr@bble')

czy = True

board = BoardData.Board()
letters = LettersSet.Letters()
words = WordsList.Words()


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
            print('ola')


input(pygame.event.get())

if czy:
    name = HelloMenu.HelloMenu().start()
    if name:
        player = PlayerData.Player(name=name, letters_set_object=letters)
        print(player.name)
        mode = MainMenu.MainMenu().start()
        if mode == 'computer':
            computer = PlayerData.Player(name='Computer', letters_set_object=letters)
            players = list()
            players.append(player)
            players.append(computer)
            game = Game.Game(words_list=words, players=players, board=board, letters=letters)
            ComputerMode.ComputerMode(game).start()
        else:
            print('nope')
else:
    pygame.quit()
