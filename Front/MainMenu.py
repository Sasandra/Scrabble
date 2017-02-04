"""Main menu to choose mode of game"""
import webbrowser
import pygame


class MainMenu:
    """Class responsible for main menu of game"""

    def __init__(self):

        self.menu_state = True
        self.screen = pygame.display.set_mode((800, 600))

        self.computer_button = pygame.Rect(203, 213, 390, 79)
        self.friends_button = pygame.Rect(203, 308, 390, 79)
        self.instruction_button = pygame.Rect(203, 400, 390, 75)
        self.exit_button = pygame.Rect(203, 488, 390, 79)

        self.set_menu()

        # pygame.draw.rect(self.screen, (0, 255, 0), self.computer_button, 1)
        # pygame.draw.rect(self.screen, (0, 255, 0), self.friends_button, 1)
        # pygame.draw.rect(self.screen, (0, 255, 0), self.instruction_button, 1)
        # pygame.draw.rect(self.screen, (0, 255, 0), self.exit_button, 1)

        pygame.display.flip()

    def set_menu(self):
        """
        Set all buttons on screen
        """
        menu_background = pygame.image.load('Images\\menu_background.png')
        self.screen = pygame.display.get_surface()
        self.screen.blit(menu_background, (0, 0))

        tittle = pygame.image.load('Images\\tittle.png')
        tittle = pygame.transform.scale(tittle, (634, 148))
        self.screen.blit(tittle, (90, 30))

        computer = pygame.image.load('Images\\buttons\\computer.png')
        computer = pygame.transform.scale(computer, (423, 99))
        self.screen.blit(computer, (189, 200))

        friends = pygame.image.load('Images\\buttons\\friends.png')
        friends = pygame.transform.scale(friends, (423, 99))
        self.screen.blit(friends, (189, 295))

        instruction = pygame.image.load('Images\\buttons\\instruction.png')
        instruction = pygame.transform.scale(instruction, (423, 99))
        self.screen.blit(instruction, (189, 385))

        exit_ = pygame.image.load('Images\\buttons\\exit.png')
        exit_ = pygame.transform.scale(exit_, (423, 99))
        self.screen.blit(exit_, (189, 475))

        pygame.display.flip()

    @staticmethod
    def button_on_click(name):
        """
        :param name: button's name to read clicked version
        :return: read image of clicked button and show it
        """
        name = 'Images\\buttons\\' + name + '_click.png'
        button = pygame.image.load(name)
        button = pygame.transform.scale(button, (423, 99))
        return button

    @staticmethod
    def button_out_click(name):
        """
        :param name: button's name to read unclicked version
        :return: read image of unclicked button
        """
        name = 'Images\\buttons\\' + name + '.png'
        button = pygame.image.load(name)
        button = pygame.transform.scale(button, (423, 99))
        return button

    def start(self):
        """
         Main loop of the menu
         """
        while self.menu_state:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.menu_state = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.exit_button.collidepoint(pygame.mouse.get_pos()):
                            self.screen.blit(self.button_on_click('exit'), (189, 475))
                            pygame.display.flip()
                            self.menu_state = False

                        elif self.instruction_button.collidepoint(pygame.mouse.get_pos()):
                            self.screen.blit(self.button_on_click('instruction'), (189, 385))
                            pygame.display.flip()
                            webbrowser.open_new(r'Documentation\\instrukcja.pdf')

                        elif self.friends_button.collidepoint(pygame.mouse.get_pos()):
                            self.screen.blit(self.button_on_click('friends'), (189, 295))
                            pygame.display.flip()
                            return 'friends'

                        elif self.computer_button.collidepoint(pygame.mouse.get_pos()):
                            self.screen.blit(self.button_on_click('computer'), (189, 200))
                            pygame.display.flip()
                            return 'computer'

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if self.exit_button.collidepoint(pygame.mouse.get_pos()):
                            self.screen.blit(self.button_out_click('exit'), (189, 475))
                            pygame.display.flip()

                        elif self.instruction_button.collidepoint(pygame.mouse.get_pos()):
                            self.screen.blit(self.button_out_click('instruction'), (189, 385))
                            pygame.display.flip()

                        elif self.friends_button.collidepoint(pygame.mouse.get_pos()):
                            self.screen.blit(self.button_out_click('friends'), (189, 295))
                            pygame.display.flip()

                        elif self.computer_button.collidepoint(pygame.mouse.get_pos()):
                            self.screen.blit(self.button_out_click('computer'), (189, 200))
                            pygame.display.flip()
