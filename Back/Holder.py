""" Player's holder for letters"""
# -*- coding: utf-8 -*-
import collections
import pygame


class Holder:
    """ Class to represent PLAYER's holder for LETTERS"""

    def __init__(self, player, screen):
        self.player = player
        self.holder = collections.OrderedDict()
        self.read_holder()
        self.screen = screen
        self.window_state = True
        self.end_exchange = pygame.Rect(1020, 260, 120, 40)

    def read_holder(self):
        """
        :return: Generate holder's coordinates on BOARD
        """
        self.holder = collections.OrderedDict()
        letters = self.player.holder
        coor = 880
        for i in range(len(letters)):
            self.holder[i] = (pygame.Rect(coor, 120, 55, 55), letters[i])
            coor += 57

    @staticmethod
    def change_name(letter):
        """
        :param letter: letter to change in correct form for filename
        :return: letter if letter isn't polish letter or suitable NAME for this letter if is polish
                e.g ą->a1  b->b
        """
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
        return switcher.get(letter, letter)

    def draw_holder(self):
        """
        :return: for each holder's letter read image and show it on a screen
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
        """
        :param index: index of letter to activate
        :return: active letter -> red backlight -> red rectangle
        """
        pygame.draw.rect(self.screen, (255, 0, 0), self.holder[index][0], 2)
        pygame.display.flip()

    def disabled_letters(self, index):
        """
        :param index: index of letter to deactivate
        :return: disabled letter -> green backlight -> green rectangle
        """
        pygame.draw.rect(self.screen, (0, 255, 0), self.holder[index][0], 2)
        pygame.display.flip()

    def chosen_letters(self, index):
        """
        :param index: index: index of letter to swap
        :return: chosen letter -> blue backlight -> blue rectangle
        """
        pygame.draw.rect(self.screen, (0, 162, 232), self.holder[index][0], 2)
        pygame.display.flip()

    def exchange_holder(self):
        """
        :return: holder with exchanged chosen LETTERS
        """
        if self.player.if_change_letters:
            return

        self.window_state = True
        exchange_button = pygame.image.load('Images\\wymiana.png')
        exchange_button = pygame.transform.scale(exchange_button, (120, 40))
        self.screen.blit(exchange_button, (1020, 260))
        pygame.display.flip()
        clicked_letters = list()

        letter_to_change = list()
        while self.window_state:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for i in self.holder:
                            if self.holder[i][0].collidepoint(pygame.mouse.get_pos()):
                                if self.holder[i][0] not in clicked_letters:
                                    letter_to_change.append(self.holder[i][1])
                                    self.active_letters(i)
                                    clicked_letters.append(self.holder[i][0])
                                else:
                                    self.disabled_letters(i)
                                    letter_to_change.remove(self.holder[i][1])
                                    clicked_letters.remove(self.holder[i][0])
                            elif self.end_exchange.collidepoint(pygame.mouse.get_pos()):
                                self.window_state = False
                                exchange_button = pygame.image.load('Images\\wymiana_hide.png')
                                exchange_button = pygame.transform.scale(exchange_button, (120, 40))
                                self.screen.blit(exchange_button, (1020, 260))
                                pygame.display.flip()

        if len(letter_to_change) == 0:
            return False
        else:
            self.player.amount_of_pass = 0
            self.player.exchange_letter(letter_to_change)
            return True

    def remove_from_holder(self, letter):
        """
        :param letter: letter to remove from holder
        :return: holder without given letter
        """
        for i in self.holder:
            if self.holder[i][1] == letter:
                index = i
                break

        self.holder.pop(index)
        self.player.remove_letter_from_holder(letter)

    def return_on_holder(self, letter):
        """
        :param letter: letter to put on holder
        :return: updated holder with new letter
        """
        holder_keys = list(self.holder.keys())

        if holder_keys:
            max_index = holder_keys[-1]
            start_coor = self.holder[max_index][0].left + 57
            max_index += 1
        else:
            max_index = 0
            start_coor = 880

        self.holder[max_index] = (pygame.Rect(start_coor, 120, 55, 55), letter)
        self.player.return_letter_on_holder(letter)

    def swap_letters(self, positions):
        """
        :param positions: positions' pair of LETTERS to swap on holder
        :return: updated holder with shifted LETTERS
        """
        letter_1 = positions[0]
        letter_2 = positions[1]

        self.holder[letter_1[0]] = (self.holder[letter_1[0]][0], letter_2[1])
        self.holder[letter_2[0]] = (self.holder[letter_2[0]][0], letter_1[1])

        letters = [x[1] for x in self.holder.values()]

        self.player.swap_letter(letters)
