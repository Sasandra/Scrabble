""" Board representation for computer mode"""
# -*- coding: utf-8 -*-

from collections import namedtuple
import ctypes
import copy
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
        self.current_player_name = None

        self.holder = Holder.Holder(self.you, self.screen)

        self.end_move_button = pygame.Rect(890, 220, 120, 40)
        self.exchange_button = pygame.Rect(1020, 220, 120, 40)
        self.pass_button = pygame.Rect(1150, 220, 120, 40)
        self.quit_game_button = pygame.Rect(1150, 600, 120, 40)

        self.clicked_board_positions = list()
        self.temp_clicked_board_positions = list()
        self.current_letter = ''
        self.positions_to_swap_on_holder = list()
        self.amount_moved_letters = 0

        self.set_background()
        self.set_board()
        self.set_screen()
        self.holder.draw_holder()
        self.set_legenda()
        self.set_current_palyer_name()
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
        :return: display on screen players' score
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

        self.you.return_letter_on_holder(self.game.get_letter_from_pos(pos))
        self.holder.draw_holder()
        self.amount_moved_letters -= 1
        self.game.remove_letter_from_word(self.game.get_letter_from_pos(pos))
        pygame.display.flip()

    def display_final_score(self):
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
                            self.display_final_score()
                            time.sleep(2)
                            return False

                        elif no_answer.collidepoint(pygame.mouse.get_pos()):
                            self.set_background()
                            self.set_board()
                            self.reset_screen()
                            pygame.display.flip()
                            return True

    def set_legenda(self):
        """ show legenda bout premiums"""
        myfont = pygame.font.SysFont("Cinnamon Cake", 30)

        background = pygame.image.load('Images\\menu_background.png')
        background = pygame.transform.scale(background, (185, 238))
        self.screen.blit(background, (875, 420))

        letter_x_2 = pygame.image.load('Images\\empty_l2.png')
        letter_x_2 = pygame.transform.scale(letter_x_2, (40, 40))
        self.screen.blit(letter_x_2, (880, 425))

        letter_x_2_label = myfont.render("2 * litera", 1, (255, 255, 255))
        self.screen.blit(letter_x_2_label, (925, 430))

        letter_x_3 = pygame.image.load('Images\\empty_l3.png')
        letter_x_3 = pygame.transform.scale(letter_x_3, (40, 40))
        self.screen.blit(letter_x_3, (880, 470))

        letter_x_3_label = myfont.render("3 * litera", 1, (255, 255, 255))
        self.screen.blit(letter_x_3_label, (925, 475))

        word_x_2 = pygame.image.load('Images\\empty_w2.png')
        word_x_2 = pygame.transform.scale(word_x_2, (40, 40))
        self.screen.blit(word_x_2, (880, 560))

        word_x_2_label = myfont.render("2 * słowo", 1, (255, 255, 255))
        self.screen.blit(word_x_2_label, (925, 565))

        word_x_3 = pygame.image.load('Images\\empty_w3.png')
        word_x_3 = pygame.transform.scale(word_x_3, (40, 40))
        self.screen.blit(word_x_3, (880, 605))

        word_x_3_label = myfont.render("3 * słowo", 1, (255, 255, 255))
        self.screen.blit(word_x_3_label, (925, 610))

    def set_current_palyer_name(self):
        """ show curent playing player"""
        myfont = pygame.font.SysFont("Cinnamon Cake", 50)
        background = pygame.image.load('Images\\game_background.png')
        background = pygame.transform.scale(background, (450, 60))
        self.screen.blit(background, (870, 45))

        current_player_name = myfont.render(self.game.current_playing_user.name, 1, (255, 255, 255))
        self.screen.blit(current_player_name, (880, 50))

    def display_score(self):
        myfont = pygame.font.SysFont("Cinnamon Cake", 30)
        background = pygame.image.load('Images\\game_background.png')
        background = pygame.transform.scale(background, (60, 28))
        if self.game.current_playing_user != self.you:
            self.screen.blit(background, (100, 150))
            score = myfont.render(str(self.you.score), 1, (255, 255, 255))
            self.screen.blit(score, (100, 150))
        else:
            self.screen.blit(background, (100, 80))
            score = myfont.render(str(self.computer.score), 1, (255, 255, 255))
            self.screen.blit(score, (100, 80))

    def remove_word(self):
        """if validation failed or pass button was clicked unwanted letters must be removed"""
        temp_list = copy.deepcopy(self.temp_clicked_board_positions)

        for i in temp_list:
            temp_rect = self.game.board.fields[i]
            self.clear_field(temp_rect, i)
            self.remove_letter_fromm_board(i)
        self.game.word = list()

    def clear_field(self, rect, i):
        """function to clean filed on board after putting of letter"""
        left = rect.left
        top = rect.top
        address = self.game.create_file_name(i)
        letter = pygame.image.load(address)
        letter = pygame.transform.scale(letter, (38, 38))
        self.screen.blit(letter, (left, top))

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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.game.current_playing_user == self.you:
                        for i in range(15):
                            for j in range(15):
                                if self.game.board.fields[(i, j)].collidepoint(pygame.mouse.get_pos()) and (
                                        i, j) not in self.temp_clicked_board_positions and self.current_letter != '':
                                    left = self.game.board.fields[(i, j)].left
                                    top = self.game.board.fields[(i, j)].top
                                    address = 'Images\\letters\\' + self.holder.change_name(
                                        self.current_letter) + '.png'
                                    letter = pygame.image.load(address)
                                    letter = pygame.transform.scale(letter, (38, 38))
                                    self.screen.blit(letter, (left, top))
                                    self.temp_clicked_board_positions.append((i, j))
                                    self.amount_moved_letters += 1
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
                            if self.holder.exchange_holder():
                                self.game.change_player()
                                self.set_current_palyer_name()
                            self.reset_screen()
                            pygame.display.update()

                        if self.pass_button.collidepoint(pygame.mouse.get_pos()):
                            self.game_state = self.game.pass_button_press()
                            self.set_current_palyer_name()
                            self.remove_word()
                            pygame.display.update()

                        if self.end_move_button.collidepoint(pygame.mouse.get_pos()):
                            if self.game.end_move():
                                self.set_current_palyer_name()
                                self.display_score()
                                self.clicked_board_positions = self.temp_clicked_board_positions
                            else:
                                self.remove_word()

                            self.holder.draw_holder()
                            pygame.display.flip()
                            pygame.display.update()

                    elif event.button == 1:
                        if self.quit_game_button.collidepoint(pygame.mouse.get_pos()):
                            self.game_state = self.do_want_end()

                    elif event.button == 3 and self.game.current_playing_user == self.you:
                        for i in self.temp_clicked_board_positions:
                            temp_rect = self.game.board.fields[i]
                            if temp_rect.collidepoint(pygame.mouse.get_pos()):
                                self.clear_field(temp_rect, i)
                                self.remove_letter_fromm_board(i)
                                pygame.display.flip()

                    elif event.button == 3:
                        for i in self.holder.holder:
                            if self.holder.holder[i][0].collidepoint(pygame.mouse.get_pos()):
                                self.positions_to_swap_on_holder.append((i, self.holder.holder[i][1]))
                                if len(self.positions_to_swap_on_holder) == 2:
                                    self.holder.swap_letters(self.positions_to_swap_on_holder)
                                    self.positions_to_swap_on_holder = list()
                                    self.holder.draw_holder()
                                    pygame.display.flip()

        self.display_final_score()
        time.sleep(2)
