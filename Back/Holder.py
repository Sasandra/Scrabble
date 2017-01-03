""" Player's holder for letters"""
# -*- coding: utf-8 -*-
import collections
import pygame


class Holder:
    """ Class to represent player's holder for letters"""
    def __init__(self, player, screen):
        self.player = player
        self.holder = collections.OrderedDict()
        self.read_holder()
        self.screen = screen
        self.window_state = True
        self.end_exchange = pygame.Rect(1020, 260, 120, 40)

    def read_holder(self):
        """
        :return: Generate holder's cooardinates on board
        """
        self.holder = collections.OrderedDict()
        letters = self.player.holder
        coor = 880
        for i in range(len(letters)):
            self.holder.update({i: (pygame.Rect(coor, 120, 55, 55), letters[i])})
            coor += 57

    @staticmethod
    def change_name(letter):
        """
        :param letter: letter which will be change in correct form for filename
        :return: letter if letter isn't polish letter or suitable name for this letter if is polish
        """
        print(letter)
        switcher = {
            'ą': "a1",
            'ć': "c1",
            'ę': "e1",
            'ł': "l1",
            'ń': "n1",
            'ó': "o1",
            'ś': "s1",
            'ź': "z1",
            'ż': "z2",
            '?': "blank"
        }
        print(switcher.get(letter, letter))
        return switcher.get(letter, letter)

    def draw_holder(self):
        """
        :return: read for each holder's letter image and show it on a screen
        """
        holder = pygame.image.load('Images\\holder.png')
        self.screen.blit(holder, (869, 109))
        self.read_holder()
        for i in self.holder:
            left = self.holder[i][0].left
            top = self.holder[i][0].top

            address = 'Images\\letters\\' + self.change_name(str(self.holder[i][1])) + '.png'
            letter = pygame.image.load(address)
            letter = pygame.transform.scale(letter, (55, 55))
            self.screen.blit(letter, (left, top))

    def active_letters(self, index):
        """ display rectangle around chosen letter"""
        pygame.draw.rect(self.screen, (255, 0, 0), self.holder[index][0], 2)
        pygame.display.flip()

    def exchange_holder(self):
        """
        :return: exchange chosen letters from holder
        """
        self.window_state = True
        exchange_button = pygame.image.load('Images\\wymiana.png')
        exchange_button = pygame.transform.scale(exchange_button, (120, 40))
        self.screen.blit(exchange_button, (1020, 260))
        pygame.display.flip()

        letter_to_change = list()
        while self.window_state:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for i in self.holder:
                            if self.holder[i][0].collidepoint(pygame.mouse.get_pos()):
                                letter_to_change.append(self.holder[i][1])
                                self.active_letters(i)
                            if self.end_exchange.collidepoint(pygame.mouse.get_pos()):
                                self.window_state = False
                                exchange_button = pygame.image.load('Images\\wymiana_hide.png')
                                exchange_button = pygame.transform.scale(exchange_button, (120, 40))
                                self.screen.blit(exchange_button, (1020, 260))
                                pygame.display.flip()
        self.player.exchange_letter(letter_to_change)
