"""First, welcome module asking about player name"""
import pygame
from Front import TextBox


class HelloMenu:
    """Class responsible for getting PLAYER NAME and create a new one"""

    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        menu_background = pygame.image.load('Images\\menu_background.png')
        self.screen = pygame.display.get_surface()
        self.screen.blit(menu_background, (0, 0))
        self.ok_button = pygame.Rect(350, 440, 105, 78)
        self.game_state = True
        self.input_entered = ''
        self.box = TextBox.TextBox(pygame.Rect(240, 360, 320, 50), 1)

        self.clear()
        self.show_text('Podaj nick:')

        pygame.display.flip()

    def clear(self):
        """
        Clear the screen, it is needed to show properly entered data
        """
        tittle = pygame.image.load('Images\\tittle.png')
        tittle = pygame.transform.scale(tittle, (634, 148))
        self.screen.blit(tittle, (90, 30))

        textbox = pygame.image.load('Images\\input.png')
        self.screen.blit(textbox, (217, 340))

        ok_button = pygame.image.load('Images\\buttons\\ok.png')
        ok_button = pygame.transform.scale(ok_button, (105, 78))
        self.screen.blit(ok_button, (350, 440))

    def show_text(self, text):
        """
        :param text: text to show on a screen
        :return: text on screen
        """
        pygame.font.init()
        myfont = pygame.font.SysFont("Gabriola", 40)

        textsurface = myfont.render(text, False, (255, 255, 255))
        self.screen.blit(textsurface, (235, 300))

    def update(self):
        """
        Update and clear textbox
        """
        self.clear()
        self.box.update(self.screen)
        pygame.display.flip()

    def start(self):
        """
        Main loop of HelloMenu
        """

        while self.game_state:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state = False

                elif event.type == pygame.KEYDOWN:
                    self.input_entered = self.box.char_add(event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.ok_button.collidepoint(pygame.mouse.get_pos()):
                            ok_button_click = pygame.image.load('Images\\buttons\\ok_click.png')
                            ok_button_click = pygame.transform.scale(ok_button_click, (105, 78))
                            self.screen.blit(ok_button_click, (350, 440))

                            pygame.display.flip()

                            if self.input_entered != '' and self.input_entered != 'Computer':
                                self.game_state = False
                                return self.input_entered
                            else:
                                self.box.str_list = []

            self.update()
