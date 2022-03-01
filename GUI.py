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

COLOR_INACTIVE = BLACK
COLOR_ACTIVE = WHITE


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
            if self.active:
                self.color = COLOR_ACTIVE
            else:
                self.color = COLOR_INACTIVE
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

    def draw(self, screen):
        # Background of the box
        pygame.draw.rect(screen, self.color, self.rect, 2)
        # Transparent box, would like to fill, but need the reverse color

        # Text formatted inside the box
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))


def main():
    if not pygame.display.get_init():
        pygame.display.init()

    clock = pygame.time.Clock()
    MAIN_WINDOW.fill(SAND)

    # NEED TO ACCOUNT FOR A BARE MINIMUM OF:
    # NAME                          1
    # RACE                          2
    # GENDER                        3
    # CLASS                         4
    # QUIRKS                        5
    # BACKGROUND                    6
    #   SUB BACKGROUND - OCCUPATION 7 ?
    x = margin = WIN_HEIGHT/10
    height_offset = int(WIN_HEIGHT - margin)
    # width_offset = WIN_WIDTH - margin
    y = increment = int(height_offset / 7)

    input_boxes = []

    for i in range(7):
        input_box = TextBox(x, y, BOX_WIDTH, BOX_HEIGHT)
        y += increment
        input_boxes.append(input_box)

    input_boxes[0].text = 'Name'
    input_boxes[1].text = 'Race'
    input_boxes[2].text = 'Gender'
    input_boxes[3].text = 'Class'
    input_boxes[4].text = 'Quirks'
    input_boxes[5].text = 'Background'
    input_boxes[6].text = 'Occupation'

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
            box.draw(MAIN_WINDOW)

        # update should always be last
        pygame.display.update()


if __name__ == "__main__":
    main()
