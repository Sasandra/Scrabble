""" Module for textboxes for your friends' names"""
import pygame
from Front import TextBox


class AddFriends:
    """Class responsible for getting PLAYER NAME and create a new one"""

    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        background = pygame.image.load('Images\\menu_background.png')
        self.screen = pygame.display.get_surface()
        self.screen.blit(background, (0, 0))

        self.window_state = True
        self.entered_names = list()
        self.input_entered = ''

        self.box = TextBox.TextBox(pygame.Rect(415, 145, 310, 43), 1)
        self.clear_textbox()
        self.show_text('Podaj imiona znajomych:', (90, 30), 60)
        self.show_text('Podaj nick gracza', (90, 150), 30)
        self.load_ok_button()
        self.load_add_button()
        self.load_back_button()

        pygame.display.flip()

    def add_labels(self):
        """
        show on screen label with new PLAYER's NAME after button_add clicking
        """
        if len(self.entered_names) == 1:
            self.show_text('Gracz 1:', (90, 260), 30)
            self.show_text(self.entered_names[-1], (250, 260), 30)
        elif len(self.entered_names) == 2:
            self.show_text('Gracz 2:', (90, 330), 30)
            self.show_text(self.entered_names[-1], (250, 330), 30)
        elif len(self.entered_names) == 3:
            self.show_text('Gracz 3:', (90, 400), 30)
            self.show_text(self.entered_names[-1], (250, 400), 30)
        else:
            pass

    def load_ok_button(self):
        """
        load image for ok_button and create rectangle for it
        """
        self.ok_button = pygame.Rect(350, 460, 105, 78)
        ok_button = pygame.image.load('Images\\buttons\\ok.png')
        ok_button = pygame.transform.scale(ok_button, (105, 78))
        self.screen.blit(ok_button, (350, 460))

    def load_add_button(self):
        """
        read image for add_button and create rectangle for it
        """
        self.add_button = pygame.Rect(350, 200, 100, 60)
        add_button = pygame.image.load('Images\\buttons\\add.png')
        add_button = pygame.transform.scale(add_button, (100, 60))
        self.screen.blit(add_button, (350, 200))

    def load_back_button(self):
        """
        read image for bac_button and create rectangle for it
        """
        self.back_button = pygame.Rect(500, 480, 100, 60)
        back_button = pygame.image.load('Images\\buttons\\back.png')
        back_button = pygame.transform.scale(back_button, (100, 60))
        self.screen.blit(back_button, (500, 480))

    def clear_textbox(self):
        """
        Clear the textbox, it is needed to show properly entered data
        """
        textbox = pygame.image.load('Images\\input.png')
        textbox = pygame.transform.scale(textbox, (330, 55))
        self.screen.blit(textbox, (400, 135))

    def show_text(self, text, coordinates, size):
        """
        :param text: text to show
        :param coordinates: coordinates where to show given text
        :param size: font's size
        :return: show given text, in given place and with given size
        """
        pygame.font.init()
        myfont = pygame.font.SysFont("Gabriola", size)

        textsurface = myfont.render(text, False, (255, 255, 255))
        self.screen.blit(textsurface, coordinates)

    def update(self):
        """
        Update and clear textbox
        """
        self.clear_textbox()
        self.box.update(self.screen)
        pygame.display.flip()
        pygame.display.update()

    def start(self):
        """
        Main loop for AddFriends
        """

        while self.window_state:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.window_state = False

                elif event.type == pygame.KEYDOWN:
                    self.input_entered = self.box.char_add(event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.ok_button.collidepoint(pygame.mouse.get_pos()):
                            ok_button_click = pygame.image.load('Images\\buttons\\ok_click.png')
                            ok_button_click = pygame.transform.scale(ok_button_click, (105, 78))
                            self.screen.blit(ok_button_click, (350, 460))

                            pygame.display.flip()

                            if len(self.entered_names) != 0:
                                self.window_state = False
                                return self.entered_names

                        elif self.add_button.collidepoint(pygame.mouse.get_pos()):
                            if self.input_entered != '' and len(self.entered_names) <= 2:
                                self.entered_names.append(self.input_entered)
                                self.add_labels()
                                self.input_entered = ''
                                self.box.str_list = []

                        elif self.back_button.collidepoint(pygame.mouse.get_pos()):
                            self.window_state = False
                            return False

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if self.add_button.collidepoint(pygame.mouse.get_pos()):
                            add_button_click = pygame.image.load('Images\\buttons\\add_click.png')
                            add_button_click = pygame.transform.scale(add_button_click, (100, 60))
                            self.screen.blit(add_button_click, (350, 200))
                            pygame.display.flip()

                        elif self.back_button.collidepoint(pygame.mouse.get_pos()):
                            back_button_click = pygame.image.load('Images\\buttons\\back_click.png')
                            back_button_click = pygame.transform.scale(back_button_click, (100, 60))
                            self.screen.blit(back_button_click, (500, 480))
                            pygame.display.flip()

                        elif self.ok_button.collidepoint(pygame.mouse.get_pos()):
                            ok_button_click = pygame.image.load('Images\\buttons\\ok.png')
                            ok_button_click = pygame.transform.scale(ok_button_click, (105, 78))
                            self.screen.blit(ok_button_click, (350, 460))
                            pygame.display.flip()

                self.load_add_button()

            self.update()
