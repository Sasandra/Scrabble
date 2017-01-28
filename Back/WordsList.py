""" Module with class to represent list of all allowed words in the game"""


class Words:
    """ Class which represent list of all allowed words in the game """

    def __init__(self):
        self.words = list()
        self.used_words = list()
        try:
            with open('Back\\words.txt', mode='r', encoding='utf-8') as reader:
                for line in reader:
                    line = line.rstrip()
                    self.words.append(line)
        except IOError:
            print('Plik ze słowami nie został znaleziony.')

    def __iter__(self):
        return iter(self.words)

    def __hash__(self):
        result = ''
        for word in self.words:
            result += word
        return hash(result)

    def add_used_word(self, word):
        """
        :param word: word to put on used_words list
        """
        self.used_words.append(word)

    def find_if_word_in_used_list(self, word):
        """
        :param word: word to chcec if is in list used words list
        :return: true if is, false if not
        """
        return word in self.used_words

    def find_if_word_in_list(self, word):
        """
        :param word:
        :return: True when given word is allowed or False when it isn't
        """
        if isinstance(word, str):
            return word in self.words, None

        for i in word:
            if i in self.words:
                return True, i
        return False, None


    @staticmethod
    def __check_letters_in_word(letters, word):
        for letter in letters:
            if letter not in word:
                return False

        return True

    def find_word_match_to_letters(self, letters):
        """
        :param letters: list of letters from which we want to create word
        :return: list of words we can create from add letters
        """
        words_match_to_letters = list()
        if '?' in letters:
            letters.remove('?')

        for word in self.words:
            if self.__check_letters_in_word(letters, word):
                words_match_to_letters.append(word)

        return words_match_to_letters
