import collections

named_letter = collections.namedtuple('named_letter', 'amount points')


class LetterSet:
    def __init__(self):
        self.__letters = dict()
        try:
            with open('letters.txt', 'r') as reader:
                data = reader.read()
                data = data.replace('\n', "@")
                data = data.split('@')
                for line in data:
                    line = line.rstrip().split(':')
                    self.__letters.update({line[0]: named_letter(int(line[1]), int(line[2]))})

        except IOError:
            print('Plik z literami nie został znaleziony.')

    def __iter__(self):
        return iter(self.__letters)

    def __hash__(self):
        result = ''
        for word in self.__letters:
            result = result + word + self.__letters[word]
        return hash(result)

    def __getitem__(self, lt):
        if letter in self.__letters:
            return self.__letters[lt]

    def __setitem__(self, lt, value):
        self.__letters[lt] = value

    def get_amount(self, lt):
        return int(self.__letters[lt].amount)

    def get_points(self, lt):
        return int(self.__letters[lt].points)

    def dekrement_amount(self, lt):
        if self.get_amount(lt) > 0:
            self.__letters[lt] = named_letter(self.get_amount(lt)-1, self.get_points(lt))



a = LetterSet()
letter = 'a'
print(a.get_amount('a'))
a.dekrement_amount('a')
a.dekrement_amount('a')
a.dekrement_amount('a')
print(a.get_amount('a'))
