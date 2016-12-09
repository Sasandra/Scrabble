"""First, welcome module asking about player name"""
import pygame
import TextBox


class HelloMenu:
    """Class responsible for getting player name and create a new one"""
    def __init__(self):

        pygame.init()

        window = pygame.display.set_mode((800, 600))
        menu_background = pygame.image.load('Images\\menu_background.png')
        self.screen = pygame.display.get_surface()
        self.screen.blit(menu_background, (0, 0))
        self.ok_button = pygame.Rect(330, 400, 133, 99)
        self.gamestate = True
        self.input_enetered = None
        self.box = TextBox.TextBox(pygame.Rect(240, 320, 320, 50), 1)

        self.clear()

    def clear(self):
        """Clear the screen, it is needed to show properly entered data"""
        tittle = pygame.image.load('Images\\tittle.png')
        tittle = pygame.transform.scale(tittle, (634, 148))
        self.screen.blit(tittle, (83, 30))

        textbox = pygame.image.load('Images\\input.png')
        self.screen.blit(textbox, (217, 300))

        ok_button = pygame.image.load('Images\\buttons\\ok.png')
        ok_button = pygame.transform.scale(ok_button, (133, 99))
        self.screen.blit(ok_button, (330, 400))

        pygame.display.flip()

    def update(self):
        """Update textbox and screen"""
        self.clear()
        self.box.update(self.screen)
        pygame.display.flip()
        self.input_enetered = ''

    def start(self):
        """Main loop of HelloMenu"""

        while self.gamestate:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gamestate = False

                elif event.type == pygame.KEYDOWN:
                    self.input_entered = self.box.char_add(event)
                    if self.input_entered:
                        print(self.input_entered)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.ok_button.collidepoint(pygame.mouse.get_pos()):
                            ok_button_click = pygame.image.load('Images\\buttons\\ok_click.png')
                            ok_button_click = pygame.transform.scale(ok_button_click, (133, 99))
                            self.screen.blit(ok_button_click, (330, 400))
                            pygame.display.flip()
                            self.gamestate = False

            self.update()
