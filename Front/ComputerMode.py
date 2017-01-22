""" Board representation for computer mode"""
# -*- coding: utf-8 -*-

from collections import namedtuple
import ctypes
import time
import pygame
from Back import Holder

MovingLetter = namedtuple('MovingLetter', 'letter, position')


class ComputerMode:
    """ Class responsible for board's design and calling functions from backend"""

    def __init__(self, game):
        # 1300 x 670
        # self.screen = pygame.display.set_mode(self.get_screen_size(), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((1300, 670))
        self.game_state = True
        self.game = game
        self.you = self.game.players_list[0]
        self.computer = self.game.players_list[1]

        self.holder = Holder.Holder(self.you, self.screen)

        self.end_move_button = pygame.Rect(890, 220, 120, 40)
        self.exchange_button = pygame.Rect(1020, 220, 120, 40)
        self.pass_button = pygame.Rect(1150, 220, 120, 40)
        self.quit_game_button = pygame.Rect(1150, 600, 120, 40)

        self.clicked_board_positions = list()
        self.temp_clicked_board_positions = list()
        self.current_letter = ''

        self.set_background()
        self.set_board()
        self.set_screen()
        self.holder.draw_holder()
        pygame.display.flip()

    @staticmethod
    def get_screen_size():
        """
        :return: user's screen's resolution
        """
        user32 = ctypes.windll.user32
        screen_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        size = (screen_size)
        return size

    def set_background(self):
        """
        :return: display widgets on screen
        """
        background = pygame.image.load('Images\\game_background.png')
        self.screen = pygame.display.get_surface()
        self.screen.blit(background, (0, 0))

        self.show_text(self.computer.name, 30, (20, 50))
        self.show_text('Wynik:', 30, (20, 80))

        self.show_text(self.you.name, 30, (20, 120))
        self.show_text('Wynik:', 30, (20, 150))

        exchange_button = pygame.image.load('Images\\letter_exchange.png')
        exchange_button = pygame.transform.scale(exchange_button, (120, 40))
        pass_button = pygame.image.load('Images\\pass.png')
        pass_button = pygame.transform.scale(pass_button, (120, 40))
        end_move = pygame.image.load('Images\\move_end.png')
        end_move = pygame.transform.scale(end_move, (120, 40))
        end_game = pygame.image.load('Images\\game-end.png')
        end_game = pygame.transform.scale(end_game, (120, 40))

        self.screen.blit(end_move, (890, 220))
        self.screen.blit(exchange_button, (1020, 220))
        self.screen.blit(pass_button, (1150, 220))
        self.screen.blit(end_game, (1150, 600))

    def set_board(self):
        """
        :return: read board image from file
        """
        board = pygame.image.load('Images\\board_small.jpg')
        self.screen.blit(board, (200, 20))

    def set_screen(self):
        """
        :return: display on screen players' names
        """
        self.show_text(str(self.computer.score), 30, (100, 80))
        self.show_text(str(self.you.score), 30, (100, 150))

    def show_text(self, text, size, coor):
        """Show given text on screen"""
        pygame.font.init()
        myfont = pygame.font.SysFont("Cinnamon Cake", size)

        textsurface = myfont.render(text, False, (255, 255, 255))
        self.screen.blit(textsurface, coor)

    def reset_screen(self):
        """
        :return: set again widgets on screen
        """
        self.holder.draw_holder()
        self.set_screen()
        pygame.display.flip()

    def remove_letter_fromm_board(self, pos):
        """ Function to remove clicked letters from board"""
        if pos in self.temp_clicked_board_positions:
            self.temp_clicked_board_positions.remove(pos)

        print(self.game.get_letter_from_pos(pos))
        # self.holder.return_on_holder(self.game.get_letter_from_pos(pos))

    def display_score(self):
        """ Function to show final result"""
        background = pygame.image.load('Images\\end_score.png')
        self.screen.blit(background, (0, 0))
        self.show_text('Wygrana idzie do:', 100, (300, 200))

        result = self.game.quit_button_press()
        self.show_text(str(result[0]), 120, (400, 400))
        pygame.display.flip()

    def do_want_end(self):
        """
        :return: display window resposible for safe exit from game
        """
        quit_state = True
        if_end_game = pygame.image.load('Images\\if_end.png')
        if_end_game = pygame.transform.scale(if_end_game, (1300, 670))
        self.screen.blit(if_end_game, (0, 0))
        yes_answer = pygame.Rect(120, 440, 220, 130)
        no_answer = pygame.Rect(920, 440, 220, 130)
        pygame.display.flip()

        while quit_state:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if yes_answer.collidepoint(pygame.mouse.get_pos()):
                            self.display_score()
                            time.sleep(2)
                            return False

                        elif no_answer.collidepoint(pygame.mouse.get_pos()):
                            self.set_background()
                            self.set_board()
                            self.reset_screen()
                            pygame.display.flip()
                            return True

    def start(self):
        """ Main loop of computer mode"""
        while self.game_state:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state = self.do_want_end()

                # if event.type is pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                #     if self.screen.get_flags() & pygame.FULLSCREEN:
                #         pygame.display.set_mode((1300, 670))
                #         pygame.display.flip()

                if event.type == pygame.MOUSEBUTTONDOWN and self.game.current_playing_user == self.you:
                    if event.button == 1:
                        for i in range(15):
                            for j in range(15):
                                if self.game.board.fields[(i, j)].collidepoint(pygame.mouse.get_pos()) and (
                                        i, j) not in self.clicked_board_positions and self.current_letter != '':
                                    left = self.game.board.fields[(i, j)].left
                                    top = self.game.board.fields[(i, j)].top
                                    address = 'Images\\letters\\' + self.holder.change_name(
                                        self.current_letter) + '.png'
                                    letter = pygame.image.load(address)
                                    letter = pygame.transform.scale(letter, (38, 38))
                                    self.screen.blit(letter, (left, top))
                                    self.temp_clicked_board_positions.append((i, j))
                                    self.holder.remove_letter(self.current_letter)
                                    self.holder.draw_holder()
                                    pygame.display.flip()
                                    self.game.word.append(MovingLetter(letter=self.current_letter, position=(i, j)))
                                    self.current_letter = ''

                        for i in self.holder.holder:
                            if self.holder.holder[i][0].collidepoint(pygame.mouse.get_pos()):
                                self.holder.draw_holder()
                                self.current_letter = self.holder.holder[i][1]
                                pygame.draw.rect(self.screen, (255, 0, 0), self.holder.holder[i][0], 2)
                                pygame.display.flip()

                        if self.exchange_button.collidepoint(pygame.mouse.get_pos()) and len(self.game.word) == 0:
                            self.holder.exchange_holder()
                            self.reset_screen()
                            self.game.change_player()

                        elif self.quit_game_button.collidepoint(pygame.mouse.get_pos()):
                            self.game_state = self.do_want_end()

                        elif self.pass_button.collidepoint(pygame.mouse.get_pos()):
                            self.game_state = self.game.pass_button_press()

                        elif self.end_move_button.collidepoint(pygame.mouse.get_pos()):
                            self.game.end_move()
                            self.holder.draw_holder()
                            #  self.display_score()
                            pygame.display.flip()
                            print('he?')

                    if event.button == 3:
                        for i in self.temp_clicked_board_positions:
                            temp_rect = self.game.board.fields[i]
                            if temp_rect.collidepoint(pygame.mouse.get_pos()):
                                left = temp_rect.left
                                top = temp_rect.top
                                address = self.game.create_file_name(i)
                                letter = pygame.image.load(address)
                                letter = pygame.transform.scale(letter, (38, 38))
                                self.screen.blit(letter, (left, top))
                                # usun z temporary, word, zwróc na holder
                                self.remove_letter_fromm_board(i)
                                # self.temp_clicked_board_positions.remove(i)
                                pygame.display.flip()

        self.display_score()
        time.sleep(2)
