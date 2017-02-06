""" Board representation for friends mode"""
# -*- coding: utf-8 -*-

from collections import namedtuple
import ctypes
import copy
import time
import pygame
from Back import Holder

MovingLetter = namedtuple('MovingLetter', 'letter, position')


class FriendsMode:
    """ Class responsible for BOARD's design and calling functions from backend"""

    def __init__(self, game):
        # 1300 x 670
        # self.screen = pygame.display.set_mode(self.get_screen_size(), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((1300, 670))
        self.game_state = True
        self.game = game

        self.create_holders()
        self.holder = self.holders[self.game.current_playing_user]

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
        self.set_premiums_key()
        self.set_current_player_name()
        pygame.display.flip()

    def create_holders(self):
        """
        create holder for all users
        """
        self.holders = dict()
        for i in self.game.players_list:
            self.holders[i] = Holder.Holder(i, self.screen)

    @staticmethod
    def get_screen_size():
        """
        :return: user's screen's resolution
        """
        user32 = ctypes.windll.user32
        screen_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        size = (screen_size)
        return size

    def set_buttons(self):
        """
        draw buttons on left side of BOARD: pass, end_move, exchange, end_game
        """
        exchange_button = pygame.image.load('Images\\letter_exchange.png')
        exchange_button = pygame.transform.scale(exchange_button, (120, 40))
        pass_button = pygame.image.load('Images\\pass.png')
        pass_button = pygame.transform.scale(pass_button, (120, 40))
        end_move = pygame.image.load('Images\\move_end.png')
        end_move = pygame.transform.scale(end_move, (120, 40))
        end_game = pygame.image.load('Images\\GAME-end.png')
        end_game = pygame.transform.scale(end_game, (120, 40))

        self.screen.blit(end_move, (890, 220))
        self.screen.blit(exchange_button, (1020, 220))
        self.screen.blit(pass_button, (1150, 220))
        self.screen.blit(end_game, (1150, 600))

    def set_background(self):
        """
        load background image, display widgets on screen
        """
        background = pygame.image.load('Images\\game_background.png')
        self.screen = pygame.display.get_surface()
        self.screen.blit(background, (0, 0))

        difference = 0
        for player in self.game.players_list:
            self.show_text(player.name, 30, (20, 50 + difference), (255, 255, 255), "Gabriola")
            self.show_text('Wynik:', 30, (20, 80 + difference), (255, 255, 255), "Gabriola")
            difference += 70

        self.set_buttons()

    def set_board(self):
        """
        read BOARD image from file
        """
        board = pygame.image.load('Images\\board_small.jpg')
        self.screen.blit(board, (200, 20))

    def set_screen(self):
        """
        display on screen PLAYERS' score
        """
        difference = 0
        for player in self.game.players_list:
            self.show_text(str(player.score), 30, (100, 80 + difference), (255, 255, 255), "Gabriola")
            difference += 70

    def show_text(self, text, size, coor, color, style):
        """
        :param text: text to show on screen
        :param size: font's size
        :param coor: coordinates where to show the text
        :param color: font's colour
        :param style: font's style
        :return: text on the screen
        """
        pygame.font.init()
        myfont = pygame.font.SysFont(style, size)

        textsurface = myfont.render(text, False, color)
        self.screen.blit(textsurface, coor)

    def reset_screen(self):
        """
        draw holder and set widgets on screen again
        """
        self.holder.draw_holder()
        self.set_screen()
        pygame.display.flip()

    def remove_letter_from_board(self, pos):
        """
        :param pos: position to remove letter from BOARD
        :return: updated BOARD without given letter
        """
        if pos in self.temp_clicked_board_positions:
            self.temp_clicked_board_positions.remove(pos)

        self.game.current_playing_user.return_letter_on_holder(self.game.get_letter_from_pos(pos))
        self.holder.draw_holder()
        self.amount_moved_letters -= 1
        self.game.remove_letter_from_word(self.game.get_letter_from_pos(pos))
        pygame.display.flip()

    def display_final_score(self):
        """
        Display winner's NAME
        """
        background = pygame.image.load('Images\\end_score.png')
        self.screen.blit(background, (0, 0))
        self.show_text('Wygrana idzie do:', 100, (300, 200), (255, 255, 255), "Gabriola")

        result = self.game.quit_button_press()
        self.show_text(str(result[0]), 120, (400, 400), (255, 255, 255), "Gabriola")
        pygame.display.flip()

    def do_want_end(self):
        """
        loop for question if quiting GAME
        """
        quit_state = True
        if_end_game = pygame.image.load('Images\\if_end.png')
        if_end_game = pygame.transform.scale(if_end_game, (415, 200))
        self.screen.blit(if_end_game, (872, 100))
        yes_answer = pygame.Rect(908, 220, 78, 60)
        no_answer = pygame.Rect(1165, 220, 75, 60)
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
                            if_end_game = pygame.image.load('Images\\game_background.png')
                            if_end_game = pygame.transform.scale(if_end_game, (415, 200))
                            self.screen.blit(if_end_game, (872, 100))
                            self.set_buttons()
                            self.holder.draw_holder()
                            pygame.display.flip()
                            return True

    def set_premiums_key(self):
        """
        display key with colourful fileds' meaning
        """
        myfont = pygame.font.SysFont("Gabriola", 30)

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

    def set_current_player_name(self):
        """
        display current PLAYER
        """
        myfont = pygame.font.SysFont("Gabriola", 50)
        background = pygame.image.load('Images\\game_background.png')
        background = pygame.transform.scale(background, (450, 60))
        self.screen.blit(background, (870, 45))

        current_player_name = myfont.render(self.game.current_playing_user.name, 1, (255, 255, 255))
        self.screen.blit(current_player_name, (880, 50))

    def display_score(self):
        """
        display and update PLAYERS' scores
        """
        background = pygame.image.load('Images\\game_background.png')
        background = pygame.transform.scale(background, (60, 28))

        difference = 0
        number_of_players = len(self.game.players_list)
        for i in range(number_of_players):
            if self.game.current_playing_user == self.game.players_list[i]:
                self.screen.blit(background, (100, 80 + ((i - 1) % number_of_players) * 70))
                self.show_text(str(self.game.players_list[(i - 1) % number_of_players].score), 30,
                               (100, 80 + ((i - 1) % number_of_players) * 70),
                               (255, 255, 255), "Gabriola")
                return
            difference += 70

    def remove_word(self):
        """
        after validation's failure or after pass_button clicking remove unwanted letter from BOARD
        """
        temp_list = copy.deepcopy(self.temp_clicked_board_positions)
        for i in temp_list:
            temp_rect = self.game.board.fields[i]
            self.clear_field(temp_rect, i)
            self.remove_letter_from_board(i)
        self.game.word = list()

    def clear_field(self, rect, i):
        """
        load empty filed's image to put off letter from BOARD
        """
        left = rect.left
        top = rect.top
        address = self.game.create_file_name(i)
        letter = pygame.image.load(address)
        letter = pygame.transform.scale(letter, (38, 38))
        self.screen.blit(letter, (left, top))

    def set_textbox_for_blank(self, pos):
        """
        create blank with textbox on it
        """
        textbox = pygame.image.load('Images\\LETTERS\\blank.png')
        left = self.game.board.fields[pos].left
        top = self.game.board.fields[pos].top
        textbox = pygame.transform.scale(textbox, (38, 38))
        self.screen.blit(textbox, (left, top))
        return [left, top]

    def take_letter_for_blank(self, pos):
        """
        display letter from BOARD on blank, or take letter from PLAYER
        """
        coor = self.set_textbox_for_blank(pos)
        coor = coor[0] + 8, coor[1] - 2
        pygame.display.update()

        letter = self.game.board.get_letter_from_position(pos)

        if letter is not None:
            self.show_text(str(letter).upper(), 30, coor, (0, 84, 45), "Times New Roman")
            pygame.display.update()

        else:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if self.game.letter_under_blank == "":
                            self.game.letter_under_blank = event.unicode
                        else:
                            self.game.second_letter_under_blank = event.unicode
                        self.show_text(str(event.unicode).upper(), 30, coor, (0, 84, 45), "Times New Roman")
                        pygame.display.update()
                        return

    def hide_holder(self):
        """
        hide holder when PLAYERS are changing
        """
        changing = True
        change = pygame.image.load('Images\\changing.png')
        change = pygame.transform.scale(change, (415, 200))
        self.screen.blit(change, (872, 100))
        pygame.display.flip()

        while changing:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        change = pygame.image.load('Images\\game_background.png')
                        change = pygame.transform.scale(change, (415, 200))
                        self.screen.blit(change, (872, 100))
                        self.set_buttons()
                        self.holder.draw_holder()
                        pygame.display.flip()
                        return

    def start(self):
        """
        Main loop of friends MODE
        """
        blank_pos = None
        second_blank_pos = None
        while self.game_state:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state = self.do_want_end()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for i in range(15):
                            for j in range(15):
                                if self.game.board.fields[(i, j)].collidepoint(pygame.mouse.get_pos()) and (
                                        i,
                                        j) not in self.temp_clicked_board_positions and self.current_letter != '' and (
                                        i, j) not in self.clicked_board_positions:
                                    self.positions_to_swap_on_holder = list()
                                    left = self.game.board.fields[(i, j)].left
                                    top = self.game.board.fields[(i, j)].top
                                    address = 'Images\\LETTERS\\' + self.holder.change_name(
                                        self.current_letter) + '.png'
                                    letter = pygame.image.load(address)
                                    letter = pygame.transform.scale(letter, (38, 38))
                                    self.screen.blit(letter, (left, top))

                                    if self.current_letter == '?':
                                        if blank_pos is None:
                                            blank_pos = (i, j)
                                        else:
                                            second_blank_pos = (i, j)
                                        self.take_letter_for_blank((i, j))

                                    self.temp_clicked_board_positions.append((i, j))
                                    self.amount_moved_letters += 1
                                    self.holder.remove_from_holder(self.current_letter)
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
                            self.holder.draw_holder()
                            if self.holder.exchange_holder():
                                self.game.change_player()
                                self.set_current_player_name()
                                self.holder = self.holders[self.game.current_playing_user]
                                self.hide_holder()
                                self.holder.draw_holder()
                            self.reset_screen()
                            pygame.display.update()
                            self.current_letter = ''

                        if self.pass_button.collidepoint(pygame.mouse.get_pos()):
                            self.game_state = self.game.pass_button_press()
                            self.remove_word()
                            self.game.change_player()
                            self.set_current_player_name()
                            self.holder = self.holders[self.game.current_playing_user]
                            self.hide_holder()
                            self.holder.draw_holder()
                            pygame.display.update()
                            self.current_letter = ''

                        if self.end_move_button.collidepoint(pygame.mouse.get_pos()):
                            if self.game.end_move():
                                self.set_current_player_name()
                                self.display_score()
                                self.clicked_board_positions += self.temp_clicked_board_positions
                                self.temp_clicked_board_positions = list()
                                self.holder = self.holders[self.game.current_playing_user]
                                self.hide_holder()

                                if blank_pos is not None:
                                    self.take_letter_for_blank(blank_pos)
                                if second_blank_pos is not None:
                                    self.take_letter_for_blank(second_blank_pos)
                            else:
                                self.remove_word()

                            self.game.letter_under_blank = ''
                            self.game.second_letter_under_blank = ''
                            self.holder.draw_holder()
                            pygame.display.flip()
                            pygame.display.update()
                            self.current_letter = ''

                    if event.button == 1:
                        if self.quit_game_button.collidepoint(pygame.mouse.get_pos()):
                            self.game_state = self.do_want_end()
                            self.current_letter = ''

                    if event.button == 3:
                        for i in self.temp_clicked_board_positions:
                            temp_rect = self.game.board.fields[i]
                            if temp_rect.collidepoint(pygame.mouse.get_pos()):
                                self.clear_field(temp_rect, i)
                                self.remove_letter_from_board(i)
                                pygame.display.flip()

                    if event.button == 3:
                        for i in self.holder.holder:
                            if self.holder.holder[i][0].collidepoint(pygame.mouse.get_pos()):
                                self.positions_to_swap_on_holder.append((i, self.holder.holder[i][1]))
                                self.holder.chosen_letters(i)
                                if len(self.positions_to_swap_on_holder) == 2:
                                    self.holder.swap_letters(self.positions_to_swap_on_holder)
                                    self.positions_to_swap_on_holder = list()
                                    self.holder.draw_holder()
                                    pygame.display.flip()

                if self.game.stop_condition():
                    continue
                else:
                    self.game_state = False

        self.display_final_score()
        time.sleep(2)
