import pygame
import os

pygame.init()
pygame.display.init()
pygame.font.init()

# python does NOT support constants, but these will be defined here for the idea of constants
# Window size - maybe should depend on screen resolution?
WIN_WIDTH = 900
WIN_HEIGHT = 600

# To keep boxes uniform stored here
BOX_WIDTH = int(WIN_WIDTH * .15)
BOX_HEIGHT = int(WIN_HEIGHT * .05)
# Frames per Second - we likely won't even need this many for a GUI. Consider downscaling
FPS = 30

# rename the window
pygame.display.set_caption("D&D Cool Cam")

# set default font size
FONT_SIZE = 32
FONT = pygame.font.Font(None, FONT_SIZE)

# Colors that will be used, so I don't have to reference the RGB value every time
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SAND = (215, 208, 94)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 120, 0)
PINK = (255, 0, 255)
CYAN = (0, 255, 255)

# create the window var
MAIN_WINDOW = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# Import background image
BACKGROUND_LARGE = pygame.image.load(
    os.path.join('Assets', 'desert.jpg'))
BACKGROUND_SCALED = pygame.transform.scale(BACKGROUND_LARGE, (WIN_WIDTH, WIN_HEIGHT))



COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')


class TextBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


def main():
    if not pygame.display.get_init():
        pygame.display.init()

    clock = pygame.time.Clock()
    MAIN_WINDOW.fill(SAND)

    x = 50
    y = 50

    input_boxes = []

    for i in range(6):
        input_box = TextBox(x, y, BOX_WIDTH, BOX_HEIGHT)
        y += 50
        input_boxes.append(input_box)

    run = True
    while run:
        clock.tick(FPS)
        MAIN_WINDOW.blit(BACKGROUND_SCALED, (0, 0))
        for event in pygame.event.get():
            for box in input_boxes:
                box.handle_event(event)
            if event.type == pygame.QUIT:
                run = False

        for box in input_boxes:
            box.update()
            box.draw(MAIN_WINDOW)

        # update should always be last
        pygame.display.update()


if __name__ == "__main__":
    main()
