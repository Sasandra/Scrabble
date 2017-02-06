"""Main module of game"""

import pygame
from Back import PlayerData, LettersSet, WordsList, BoardData, Game
from Front import HelloMenu, MainMenu, ComputerMode, AddFriends, FriendsMode
from Back.Tree import Tree, Node

pygame.init()
pygame.display.set_caption('Scr@bble')

WINDOW_STATE = True

BOARD = BoardData.Board()
LETTERS = LettersSet.Letters()
WORDS = WordsList.Words()

if WINDOW_STATE:
    NAME = HelloMenu.HelloMenu().start()
    while NAME:
        PLAYER = PlayerData.Player(name=NAME, letters_set_object=LETTERS)
        PLAYERS = list()
        PLAYERS.append(PLAYER)
        MODE = MainMenu.MainMenu().start()

        if MODE == 'computer':
            COMPUTER = PlayerData.Player(name='Computer', letters_set_object=LETTERS)
            PLAYERS.append(COMPUTER)
            GAME = Game.Game(words_list=WORDS, players=PLAYERS, board=BOARD, letters=LETTERS, ai=True)
            ComputerMode.ComputerMode(GAME).start()
            break

        elif MODE == 'friends':
            NAMES = AddFriends.AddFriends().start()

            if NAMES is not False:
                for i in NAMES:
                    PLAYERS.append(PlayerData.Player(name=i, letters_set_object=LETTERS))

                GAME = Game.Game(words_list=WORDS, players=PLAYERS, board=BOARD, letters=LETTERS)
                FriendsMode.FriendsMode(GAME).start()
                break
        else:
            NAME = ''
            pygame.quit()
else:
    pygame.quit()
