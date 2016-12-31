import pygame
import collections


class Holder:

    def __init__(self, player, screen):
        self.player = player
        self.holder = collections.OrderedDict()
        self.read_holder()
        self.screen = screen
        self.window_state = True
        self.end_exchange = pygame.Rect(1020, 260, 120, 40)

    def read_holder(self):
        self.holder = collections.OrderedDict()
        letters = self.player.holder
        coor = 880
        for i in range(len(letters)):
            self.holder.update({i: (pygame.Rect(coor, 120, 55, 55), letters[i])})
            coor += 57

    def draw_holder(self):
        self.read_holder()
        for i in self.holder:
            left = self.holder[i][0].left
            top = self.holder[i][0].top

            if self.holder[i][1] == '?':
                i = 'blank'
            else:
                i = self.holder[i][1]

            address = 'Images\\letters\\' + str(i) + '.png'
            letter = pygame.image.load(address)
            letter = pygame.transform.scale(letter, (55, 55))
            self.screen.blit(letter, (left, top))

    def exchange_holder(self):
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
                            if self.end_exchange.collidepoint(pygame.mouse.get_pos()):
                                self.window_state = False
                                exchange_button = pygame.image.load('Images\\wymiana_hide.png')
                                exchange_button = pygame.transform.scale(exchange_button, (120, 40))
                                self.screen.blit(exchange_button, (1020, 260))
                                pygame.display.flip()
        self.player.exchange_letter(letter_to_change)
