""" Testing Game module"""
import unittest
import collections

from Back import BoardData
from Back import Game
from Back import LettersSet
from Back import PlayerData
from Back import WordsList

Premium = collections.namedtuple('premium', 'kind factor')


class GameTest(unittest.TestCase):
    def setUp(self):
        players = list()
        letter_set = LettersSet.Letters()
        players.append(PlayerData.Player('Ola', letter_set))
        players.append(PlayerData.Player('Tomek', letter_set))
        self.game = Game.Game(letters=letter_set, words_list=WordsList.Words(), board=BoardData.Board(),
                              players=players)

        self.game.board.set_letter_on_position((1, 4), 's')

        self.vertically_word = [Game.MovingLetter('t', (1, 2)), Game.MovingLetter('a', (1, 3)),
                                Game.MovingLetter('t', (1, 4)), Game.MovingLetter('a', (1, 5))]
        self.horizontally_word = [Game.MovingLetter('m', (1, 1)), Game.MovingLetter('a', (2, 1)),
                                  Game.MovingLetter('m', (3, 1)), Game.MovingLetter('a', (4, 1))]
        self.incorrect_word = [Game.MovingLetter('m', (1, 2)), Game.MovingLetter('o', (2, 2)),
                               Game.MovingLetter('s', (5, 1)), Game.MovingLetter('t', (1, 4))]

        self.incomplete_word = [Game.MovingLetter('m', (1, 2)), Game.MovingLetter('o', (1, 3)),
                                Game.MovingLetter('t', (1, 5))]

        self.center_word = [Game.MovingLetter('t', (7, 7)), Game.MovingLetter('o', (7, 8)),
                            Game.MovingLetter('r', (7, 8))]

    def test_tuple_diff(self):
        tuple_1 = (1, 2)
        tuple_2 = (1, 3)
        result = self.game.tuple_diff(tuple_1, tuple_2)
        self.assertEqual(result, [0, 1])

    def test_is_vertically_fail(self):
        tuples = [(0, 1), (0, 1), (0, 1)]
        result = self.game.is_vertically(tuples)
        self.assertEqual(result, True)

    def test_is_vertically_ok(self):
        tuples = [(1, 0), (1, 0), (1, 0)]
        result = self.game.is_vertically(tuples)
        self.assertEqual(result, False)

    def test_is_horizontally_ok(self):
        tuples = [(0, 1), (0, 1), (0, 1)]
        result = self.game.is_horizontally(tuples)
        self.assertEqual(result, False)

    def test_is_horizontally_fail(self):
        tuples = [(1, 0), (1, 0), (1, 0)]
        result = self.game.is_horizontally(tuples)
        self.assertEqual(result, True)

    def test_find_missing_position(self):
        tuple1 = (1, 2)
        tuple2 = (1, 4)
        missing_tuple = self.game.find_missing_position(tuple1, tuple2)
        self.assertEqual(missing_tuple, (1, 3))

    def test_positions_validation_horizontally(self):
        self.game.word = self.horizontally_word
        result = self.game.positions_validation()
        self.assertEqual(result, True)

    def test_positions_validation_vertically(self):
        self.game.word = self.vertically_word
        result = self.game.positions_validation()
        self.assertEqual(result, True)

    def test_positions_validation_fail(self):
        self.game.word = self.incorrect_word
        result = self.game.positions_validation()
        self.assertEqual(result, False)

    def test_complete_word(self):
        self.game.word = self.incomplete_word
        self.game.complete_word()
        result = ''
        for i in self.game.word:
            result += i.letter
        self.assertEqual(result, 'most')

    def test_check_if_center_ok(self):
        self.game.word = self.center_word
        result = self.game.check_if_center()
        self.assertEqual(result, True)

    def test_check_if_center_fail(self):
        self.game.word = self.vertically_word
        result = self.game.check_if_center()
        self.assertEqual(result, False)

    def test_create_list_of_words_one_blank_polish(self):
        self.game.letter_under_blank = 'a'
        self.game.second_letter_under_blank = ''
        word = 't?'
        result = self.game.create_list_of_words(word)
        self.assertEqual(result, ['ta', 'tą'])

    def test_create_list_of_words_one_blank(self):
        self.game.letter_under_blank = 't'
        self.game.second_letter_under_blank = ''
        word = '?ata'
        result = self.game.create_list_of_words(word)
        self.assertEqual(result, ['tata'])

    def test_create_list_of_words_two_blanks(self):
        self.game.letter_under_blank = 'b'
        self.game.second_letter_under_blank = 'r'
        word = '?a?'
        result = self.game.create_list_of_words(word)
        self.assertEqual(result, ['ba?', 'bar'])

    def test_create_list_of_words_two_blanks_polish(self):
        self.game.letter_under_blank = 'o'
        self.game.second_letter_under_blank = 'a'
        word = '?w?'
        result = self.game.create_list_of_words(word)
        self.assertEqual(result, ['ow?', 'ów?', 'owa', 'ową', 'ówa', 'ówą'])

    def test_create_list_of_words_two_blanks_mixed(self):
        self.game.letter_under_blank = 'b'
        self.game.second_letter_under_blank = 'a'
        word = '??l'
        result = self.game.create_list_of_words(word)
        self.assertEqual(result, ['b?l', 'bal', 'bąl'])

    def test_word_plane_h(self):
        self.game.word = self.vertically_word
        result = self.game.word_plane()
        self.assertEqual(result, 'h')

    def test_word_plane_v(self):
        self.game.word = self.horizontally_word
        result = self.game.word_plane()
        self.assertEqual(result, 'v')

    def test_letter_positions(self):
        self.game.word = self.horizontally_word
        result = self.game.letter_positions()
        self.assertEqual(result, [(1, 1), (2, 1), (3, 1), (4, 1)])

    def test_further_suffixes_pre(self):
        self.game.board.set_letter_on_position((0, 1), 'r')
        self.game.board.set_letter_on_position((0, 2), 'y')
        self.game.board.set_letter_on_position((0,3), 'm')
        self.game.word = [Game.MovingLetter('y', (0, 4))]
        result = self.game.further_suffixes((0, 4), (0, -1))
        self.assertEqual(result, 'myr')

    def test_further_suffixes_suf(self):
        self.game.board.set_letter_on_position((0, 1), 'y')
        self.game.board.set_letter_on_position((0, 2), 'm')
        self.game.board.set_letter_on_position((0, 3), 'y')
        self.game.word = [Game.MovingLetter('r', (0, 0))]
        result = self.game.further_suffixes((0, 0), (0, 1))
        self.assertEqual(result, 'ymy')

    def test_create_letter_under_blank(self):
        self.game.allowed_word = 'mąka'
        self.game.create_letter_under_blank('m?ka')
        self.assertEqual(self.game.allowed_word, 'ą')

    def test_check_range_ok(self):
        result = self.game.check_range((6,7))
        self.assertEqual(result, True)

    def test_check_range_fail(self):
        result = self.game.check_range((16,7))
        self.assertEqual(result, False)

    def test_collision_validation(self):
        self.game.board.set_letter_on_position((1, 1), 'c')
        self.game.board.set_letter_on_position((2, 1), 'u')
        self.game.board.set_letter_on_position((3, 1), 'd')
        self.game.word = [Game.MovingLetter('d', (2, 2)), Game.MovingLetter('o', (2, 3))]
        result = self.game.collision_validation()
        self.assertEqual(result, [Game.MovingLetter('u', (2, 1))])

    def test_collision_validation_empty(self):
        self.game.board.set_letter_on_position((1, 1), 'c')
        self.game.board.set_letter_on_position((2, 1), 'u')
        self.game.board.set_letter_on_position((3, 1), 'd')
        self.game.word = [Game.MovingLetter('d', (15, 4)), Game.MovingLetter('o', (15, 5))]
        result = self.game.collision_validation()
        self.assertEqual(result, [])

    def test_collision_validation_double(self):
        self.game.board.set_letter_on_position((1, 1), 'c')
        self.game.board.set_letter_on_position((2, 1), 'u')
        self.game.board.set_letter_on_position((3, 1), 'd')
        self.game.board.set_letter_on_position((3, 3), 'd')
        self.game.word = [Game.MovingLetter('d', (2, 2)), Game.MovingLetter('o', (2, 3))]
        result = self.game.collision_validation()
        self.assertEqual(result, [Game.MovingLetter('u', (2, 1)), Game.MovingLetter('d', (3, 3))])

    def test_put_word_on_board(self):
        self.game.word = [Game.MovingLetter('o', (12, 12))]
        self.game.put_word_on_board()
        self.assertEqual(self.game.board.get_letter_from_position((12, 12)), 'o')

    def test_put_word_on_board_blank(self):
        self.game.word = [Game.MovingLetter('?', (12, 12))]
        self.game.allowed_word = 'ó'
        self.game.put_word_on_board()
        self.assertEqual(self.game.board.get_letter_from_position((12, 12)), 'ó')

    def test_change_player(self):
        self.game.change_player()
        self.assertEqual(self.game.current_playing_user, self.game.players_list[1])

    def test_remove_letter_from_word(self):
        self.game.word = [Game.MovingLetter('d', (15, 4)), Game.MovingLetter('o', (15, 5))]
        self.game.remove_letter_from_word('o')
        self.assertEqual(self.game.word, [Game.MovingLetter('d', (15, 4))])

    def test_calculate_score_first(self):
        self.game.word = self.center_word
        score = self.game.calculate_score()
        self.assertEqual(score, 8)

    def test_calculate_score_without(self):
        self.game.word = [Game.MovingLetter('d', (6, 4)), Game.MovingLetter('o', (7, 4))]
        self.game.moves_counter = 2
        score = self.game.calculate_score()
        self.assertEqual(score, 3)

    def test_calculate_score_word(self):
        self.game.word = [Game.MovingLetter('d', (14, 0)), Game.MovingLetter('o', (14, 1))]
        self.game.moves_counter = 2
        score = self.game.calculate_score()
        self.assertEqual(score, 9)

    def test_calculate_score_letter(self):
        self.game.word = [Game.MovingLetter('d', (14, 3)), Game.MovingLetter('o', (14, 4))]
        self.game.moves_counter = 2
        score = self.game.calculate_score()
        self.assertEqual(score, 5)

    def test_calculate_score_both(self):
        self.game.word = [Game.MovingLetter('d', (14, 0)), Game.MovingLetter('o', (14, 1)), Game.MovingLetter('m', (14, 2)), Game.MovingLetter('u', (14, 3))]
        self.game.moves_counter = 2
        score = self.game.calculate_score()
        self.assertEqual(score, 33)

    def test_end_move_moves_counter(self):
        self.game.word = self.center_word
        self.game.end_move()
        self.assertEqual(self.game.moves_counter, 1)

    def test_end_move_scores(self):
        self.game.word = self.center_word
        self.game.end_move()
        self.assertEqual(self.game.players_list[0].score, 8)

    def test_end_move_next_player(self):
        self.game.word = self.center_word
        self.game.end_move()
        self.assertEqual(self.game.current_playing_user, self.game.players_list[1])

    def test_end_move_next_board(self):
        self.game.word = self.center_word
        self.game.end_move()
        self.assertEqual(self.game.board.get_letter_from_position((7, 7)), 't')

    def test_end_move_next_true(self):
        self.game.word = self.center_word
        self.assertEqual(self.game.end_move(), True)

    def test_end_move_next_false(self):
        self.game.word = self.horizontally_word
        self.assertEqual(self.game.end_move(), False)

    def test_pass_button_press(self):
        self.game.pass_button_press()
        self.assertEqual(self.game.current_playing_user.amount_of_pass, 1)

    def test_quit_button_press_draw_name(self):
        result = self.game.quit_button_press()
        self.assertEqual(result[0], 'Ola')

    def test_quit_button_press_draw_points(self):
        result = self.game.quit_button_press()
        self.assertEqual(result[1], 0)

    def test_quit_button_press_name(self):
        self.game.players_list[1].score = 20
        result = self.game.quit_button_press()
        self.assertEqual(result[0], 'Tomek')

    def test_quit_button_press_points(self):
        self.game.players_list[1].score = 20
        result = self.game.quit_button_press()
        self.assertEqual(result[1], 20)

    def test_check_pass_true(self):
        self.game.players_list[0].amount_of_pass = 2
        self.game.players_list[1].amount_of_pass = 2
        result = self.game.check_pass()
        self.assertEqual(result, True)

    def test_check_pass_false(self):
        self.game.players_list[0].amount_of_pass = 0
        self.game.players_list[1].amount_of_pass = 5
        result = self.game.check_pass()
        self.assertEqual(result, False)

    def test_check_type_of_field_none(self):
        result = self.game.check_type_of_field((0, 1))
        self.assertEqual(result, None)

    def test_check_type_of_field_word(self):
        result = self.game.check_type_of_field((0, 0))
        self.assertEqual(result, BoardData.Premium(kind='word', factor=3))

    def test_check_type_of_field_letter(self):
        result = self.game.check_type_of_field((0, 3))
        self.assertEqual(result, BoardData.Premium(kind='letter', factor=2))

    def test_get_letter_from_pos_ok(self):
        self.game.word = self.center_word
        result = self.game.get_letter_from_pos((7, 7))
        self.assertEqual(result, 't')

    def test_get_letter_from_pos_fail(self):
        self.game.word = self.center_word
        result = self.game.get_letter_from_pos((15, 7))
        self.assertEqual(result, None)

    def test_create_file_name_empty(self):
        result = self.game.create_file_name((0, 1))
        self.assertEqual(result, 'Images\\empty_field.png')

    def test_create_file_name_word(self):
        result = self.game.create_file_name((0, 0))
        self.assertEqual(result, 'Images\\empty_w3.png')

    def test_create_file_name_letter(self):
        result = self.game.create_file_name((1, 5))
        self.assertEqual(result, 'Images\\empty_l3.png')

    def test_check_new_word_without_blank_ok(self):
        word_prefix = 'ram'
        word = ''
        recv_word = 'm'
        word_suffix = 'olada'
        result = self.game.check_new_word(word_prefix, word, recv_word, word_suffix)
        self.assertEqual(result, True)

    def test_check_new_word_without_blank_fail(self):
        word_prefix = 'ram'
        word = ''
        recv_word = 'm'
        word_suffix = 'ada'
        result = self.game.check_new_word(word_prefix, word, recv_word, word_suffix)
        self.assertEqual(result, False)

    def test_check_new_word_with_blank_ok(self):
        self.game.allowed_word = 'marmolada'
        self.game.letter_under_blank = 'm'
        self.game.second_letter_under_blank = ''
        word_prefix = 'ra?'
        word = ''
        recv_word = 'm'
        word_suffix = 'olada'
        result = self.game.check_new_word(word_prefix, word, recv_word, word_suffix)
        self.assertEqual(result, True)

    def test_check_new_word_with_blank_fail(self):
        self.game.allowed_word = 'marmolada'
        self.game.letter_under_blank = 'm'
        self.game.second_letter_under_blank = ''
        word_prefix = 'ra?'
        word = ''
        recv_word = 'm'
        word_suffix = 'ada'
        result = self.game.check_new_word(word_prefix, word, recv_word, word_suffix)
        self.assertEqual(result, False)

    def test_check_new_word_with_two_blanks_ok(self):
        self.game.allowed_word = 'marmolada'
        self.game.letter_under_blank = 'm'
        self.game.second_letter_under_blank = 'o'
        word_prefix = 'ra?'
        word = ''
        recv_word = 'm'
        word_suffix = '?lada'
        result = self.game.check_new_word(word_prefix, word, recv_word, word_suffix)
        self.assertEqual(result, True)

    def test_check_new_word_with_two_blanks_fail(self):
        self.game.allowed_word = 'marmolada'
        self.game.letter_under_blank = 'm'
        self.game.second_letter_under_blank = 'o'
        word_prefix = 'ra?'
        word = ''
        recv_word = 'm'
        word_suffix = '?lda'
        result = self.game.check_new_word(word_prefix, word, recv_word, word_suffix)
        self.assertEqual(result, False)

    def test_word_suffixes_one_letter_pre_ok(self):
        self.game.word = [Game.MovingLetter('a', (7, 10))]
        self.game.board.set_letter_on_position((7, 7), 'c')
        self.game.board.set_letter_on_position((7, 8), 'u')
        self.game.board.set_letter_on_position((7, 9), 'd')
        self.game.collisions = self.game.collision_validation()
        result = self.game.word_suffixes_one_letter('a')
        self.assertEqual(result, True)

    def test_word_suffixes_one_letter_pre_fail(self):
        self.game.word = [Game.MovingLetter('d', (7, 10))]
        self.game.board.set_letter_on_position((7, 7), 'c')
        self.game.board.set_letter_on_position((7, 8), 'u')
        self.game.board.set_letter_on_position((7, 9), 'd')
        self.game.collisions = self.game.collision_validation()
        result = self.game.word_suffixes_one_letter('d')
        self.assertEqual(result, False)

    def test_word_suffixes_one_letter_post_fail(self):
        self.game.word = [Game.MovingLetter('a', (7, 6))]
        self.game.board.set_letter_on_position((7, 7), 'u')
        self.game.board.set_letter_on_position((7, 8), 'd')
        self.game.board.set_letter_on_position((7, 9), 'a')
        self.game.collisions = self.game.collision_validation()
        result = self.game.word_suffixes_one_letter('a')
        self.assertEqual(result, False)

    def test_word_suffixes_one_letter_post_ok(self):
        self.game.word = [Game.MovingLetter('c', (7, 6))]
        self.game.board.set_letter_on_position((7, 7), 'u')
        self.game.board.set_letter_on_position((7, 8), 'd')
        self.game.board.set_letter_on_position((7, 9), 'a')
        self.game.collisions = self.game.collision_validation()
        result = self.game.word_suffixes_one_letter('c')
        self.assertEqual(result, True)

    def test_word_suffixes_one_letter_few_ok(self):
        self.game.word = [Game.MovingLetter('d', (8, 8))]
        self.game.board.set_letter_on_position((7, 7), 'c')
        self.game.board.set_letter_on_position((7, 8), 'u')
        self.game.board.set_letter_on_position((7, 9), 'd')
        self.game.board.set_letter_on_position((8, 7), 'o')
        self.game.board.set_letter_on_position((9, 7), 'ś')
        self.game.collisions = self.game.collision_validation()
        result = self.game.word_suffixes_one_letter('d')
        self.assertEqual(result, True)

    def test_word_suffixes_one_letter_few_fail(self):
        self.game.word = [Game.MovingLetter('s', (8, 8))]
        self.game.board.set_letter_on_position((7, 7), 'c')
        self.game.board.set_letter_on_position((7, 8), 'u')
        self.game.board.set_letter_on_position((7, 9), 'd')
        self.game.board.set_letter_on_position((8, 7), 'o')
        self.game.board.set_letter_on_position((9, 7), 'ś')
        self.game.collisions = self.game.collision_validation()
        result = self.game.word_suffixes_one_letter('s')
        self.assertEqual(result, False)

    def test_word_suffixes_pre_ok(self):
        self.game.word = [Game.MovingLetter('n', (7, 10)), Game.MovingLetter('a', (7, 11))]
        self.game.board.set_letter_on_position((7, 7), 'c')
        self.game.board.set_letter_on_position((7, 8), 'u')
        self.game.board.set_letter_on_position((7, 9), 'd')
        self.game.collisions = self.game.collision_validation()
        result = self.game.word_suffixes('na')
        self.assertEqual(result, True)

    def test_word_suffixes_pre_fail(self):
        self.game.word = [Game.MovingLetter('o', (7, 10)), Game.MovingLetter('n', (7, 11))]
        self.game.board.set_letter_on_position((7, 7), 'c')
        self.game.board.set_letter_on_position((7, 8), 'u')
        self.game.board.set_letter_on_position((7, 9), 'd')
        self.game.collisions = self.game.collision_validation()
        result = self.game.word_suffixes('on')
        self.assertEqual(result, False)

    def test_word_suffixes_post_ok(self):
        self.game.word = [Game.MovingLetter('c', (7, 10)), Game.MovingLetter('u', (7, 11)), Game.MovingLetter('d', (7, 12))]
        self.game.board.set_letter_on_position((7, 13), 'n')
        self.game.board.set_letter_on_position((7, 14), 'a')
        self.game.collisions = self.game.collision_validation()
        result = self.game.word_suffixes('cud')
        self.assertEqual(result, True)

    def test_word_suffixes_post_fail(self):
        self.game.word = [Game.MovingLetter('c', (7, 10)), Game.MovingLetter('u', (7, 11)),
                          Game.MovingLetter('d', (7, 12))]
        self.game.board.set_letter_on_position((7, 13), 'o')
        self.game.board.set_letter_on_position((7, 14), 'n')
        self.game.collisions = self.game.collision_validation()
        result = self.game.word_suffixes('cud')
        self.assertEqual(result, False)

    def test_word_suffixes_post_both_ok(self):
        self.game.word = [Game.MovingLetter('u', (7, 10)), Game.MovingLetter('d', (7, 11))]
        self.game.board.set_letter_on_position((7, 9), 'c')
        self.game.board.set_letter_on_position((7, 11), 'd')
        self.game.collisions = self.game.collision_validation()
        result = self.game.word_suffixes('ud')
        self.assertEqual(result, True)

    def test_word_suffixes_post_both_fail(self):
        self.game.word = [Game.MovingLetter('p', (7, 10)), Game.MovingLetter('o', (7, 11))]
        self.game.board.set_letter_on_position((7, 9), 'c')
        self.game.board.set_letter_on_position((7, 12), 'o')
        self.game.collisions = self.game.collision_validation()
        result = self.game.word_suffixes('po')
        self.assertEqual(result, False)

    def test_random_created_word__post_ok(self):
        self.game.board.set_letter_on_position((7, 7), 'z')
        self.game.board.set_letter_on_position((7, 8), 'l')
        self.game.board.set_letter_on_position((7, 9), 'e')
        self.game.board.set_letter_on_position((7, 10), 'w')
        self.game.word = [Game.MovingLetter('t', (6, 11)), Game.MovingLetter('y', (7, 11))]
        self.game.collisions = self.game.collision_validation()
        result = self.game.random_created_word('ty')
        self.assertEqual(result, True)

    def test_random_created_word_post_fail_word(self):
        self.game.board.set_letter_on_position((7, 7), 'z')
        self.game.board.set_letter_on_position((7, 8), 'l')
        self.game.board.set_letter_on_position((7, 9), 'e')
        self.game.board.set_letter_on_position((7, 10), 'w')
        self.game.word = [Game.MovingLetter('e', (6, 11)), Game.MovingLetter('y', (7, 11))]
        self.game.collisions = self.game.collision_validation()
        result = self.game.random_created_word('ey')
        self.assertEqual(result, False)

    def test_random_created_word_post_fail_collision(self):
        self.game.board.set_letter_on_position((7, 7), 'z')
        self.game.board.set_letter_on_position((7, 8), 'l')
        self.game.board.set_letter_on_position((7, 9), 'e')
        self.game.board.set_letter_on_position((7, 10), 'w')
        self.game.word = [Game.MovingLetter('i', (6, 11)), Game.MovingLetter('ł', (7, 11))]
        self.game.collisions = self.game.collision_validation()
        result = self.game.random_created_word('ił')
        self.assertEqual(result, False)

    def test_random_created_word_pre_ok(self):
        self.game.board.set_letter_on_position((7, 7), 'l')
        self.game.board.set_letter_on_position((7, 8), 'e')
        self.game.board.set_letter_on_position((7, 9), 'w')
        self.game.board.set_letter_on_position((7, 10), 'y')
        self.game.word = [Game.MovingLetter('z', (7, 6)), Game.MovingLetter('a', (8, 6))]
        self.game.collisions = self.game.collision_validation()
        result = self.game.random_created_word('za')
        self.assertEqual(result, True)

    def test_random_created_word_pre_fail_word(self):
        self.game.board.set_letter_on_position((7, 7), 'l')
        self.game.board.set_letter_on_position((7, 8), 'e')
        self.game.board.set_letter_on_position((7, 9), 'w')
        self.game.board.set_letter_on_position((7, 10), 'y')
        self.game.word = [Game.MovingLetter('z', (7, 6)), Game.MovingLetter('b', (8, 6))]
        self.game.collisions = self.game.collision_validation()
        result = self.game.random_created_word('zb')
        self.assertEqual(result, False)

    def test_random_created_word_pre_fail_collision(self):
        self.game.board.set_letter_on_position((7, 7), 'l')
        self.game.board.set_letter_on_position((7, 8), 'e')
        self.game.board.set_letter_on_position((7, 9), 'w')
        self.game.board.set_letter_on_position((7, 10), 'y')
        self.game.word = [Game.MovingLetter('o', (7, 6)), Game.MovingLetter('d', (8, 6))]
        self.game.collisions = self.game.collision_validation()
        result = self.game.random_created_word('od')
        self.assertEqual(result, False)

    def test_random_created_word_perpendicularly_ok(self):
        self.game.board.set_letter_on_position((7, 7), 'k')
        self.game.board.set_letter_on_position((7, 8), 'r')
        self.game.board.set_letter_on_position((7, 9), 'ó')
        self.game.board.set_letter_on_position((7, 10), 'l')
        self.game.word = [Game.MovingLetter('t', (6, 8)), Game.MovingLetter('r', (7, 8)),
                          Game.MovingLetter('o', (8, 8)), Game.MovingLetter('n', (9, 8))]
        self.game.collisions = self.game.collision_validation()
        result = self.game.random_created_word('tron')
        self.assertEqual(result, True)

    def test_random_created_word_perpendicularly_fail(self):
        self.game.board.set_letter_on_position((7, 7), 'k')
        self.game.board.set_letter_on_position((7, 8), 'r')
        self.game.board.set_letter_on_position((7, 9), 'ó')
        self.game.board.set_letter_on_position((7, 10), 'l')
        self.game.word = [Game.MovingLetter('t', (6, 8)), Game.MovingLetter('r', (7, 8)),
                          Game.MovingLetter('r', (8, 8)), Game.MovingLetter('a', (9, 8))]
        self.game.collisions = self.game.collision_validation()
        result = self.game.random_created_word('trra')
        self.assertEqual(result, False)

    def test_random_created_word_few_fail(self):
        self.game.board.set_letter_on_position((6, 7), 'd')
        self.game.board.set_letter_on_position((7, 7), 'a')
        self.game.board.set_letter_on_position((8, 7), 't')

        self.game.board.set_letter_on_position((8, 8), 'e')
        self.game.board.set_letter_on_position((8, 9), 'm')
        self.game.board.set_letter_on_position((8, 10), 'u')

        self.game.word = [Game.MovingLetter('m', (7, 6)), Game.MovingLetter('a', (7, 7)),
                          Game.MovingLetter('g', (7, 8))]
        self.game.collisions = self.game.collision_validation()
        result = self.game.random_created_word('mag')
        self.assertEqual(result, False)

    def test_random_created_word_few_ok(self):
        self.game.board.set_letter_on_position((6, 7), 'd')
        self.game.board.set_letter_on_position((7, 7), 'a')
        self.game.board.set_letter_on_position((8, 7), 't')

        self.game.board.set_letter_on_position((8, 8), 'e')
        self.game.board.set_letter_on_position((8, 9), 'm')
        self.game.board.set_letter_on_position((8, 10), 'u')

        self.game.word = [Game.MovingLetter('m', (7, 6)), Game.MovingLetter('a', (7, 7)),
                          Game.MovingLetter('t', (7, 8))]
        self.game.collisions = self.game.collision_validation()
        result = self.game.random_created_word('mat')
        self.assertEqual(result, True)




suite = unittest.TestLoader().loadTestsFromTestCase(GameTest)
print(unittest.TextTestRunner(verbosity=3).run(suite))
