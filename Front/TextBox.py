"""Implementation of TextBOX downloaded from internet"""
import pygame


class TextBox:
    """Class that implements textbox"""

    def __init__(self, rect, width=1):
        self.font_size = 30
        self.font = pygame.font.SysFont('Arial', self.font_size)
        self.str_list = []
        self.width = width
        self.color = (0, 0, 0)
        self.rect = rect

    def char_add(self, event):
        """
        modify string list based on event.key
        """
        if event.key == pygame.K_BACKSPACE:
            if self.str_list:
                self.str_list.pop()
        elif event.key == pygame.K_RETURN:
            return ''.join(self.str_list)
        elif event.key in [pygame.K_TAB, pygame.K_KP_ENTER]:  # unwanted keys
            return False
        elif event.key == pygame.K_DELETE:
            self.str_list = []
            return False
        else:
            char = event.unicode
            if char:  # stop emtpy space for shift key adding to list
                self.str_list.append(char)

        return ''.join(self.str_list)

    def update(self, scr):
        """
        show entered word on screen
        """
        temp_word = ''.join(self.str_list)
        label = ''
        if len(temp_word) > 0:
            for index, ite in enumerate(temp_word):
                if self.font.size(temp_word[index:])[0] < self.rect.width:
                    label = self.font.render(temp_word[index:], 1, self.color)
                    break
        else:
            label = self.font.render(temp_word, 1, self.color)

        # pygame.draw.rect(scr, (255, 0, 0), self.rect, 1)
        scr.blit(label, self.rect)
