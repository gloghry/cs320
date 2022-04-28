import pygame
import os
import sys
from classes.LoreSearcher import Searcher
# from lore_searcher.classes.LorePage import Page

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

DEFAULT_FONT = 32

WIDTH_SPACER = 12
HEIGHT_SPACER = 10

# rename the window
pygame.display.set_caption("D&D Cool Cam")

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

COLOR_INACTIVE = BLACK
COLOR_ACTIVE = WHITE


def main():
    clock = pygame.time.Clock()
    path = os.path.join("data", "index")
    searcher = Searcher(path)
    results = searcher.search(sys.argv[1])
    """
    for result in results['results']:
        result.getPage()
    """

    data = []

    for result in results['results']:
        data = result.getSummary()

    for entry in data:
        print(entry, data[entry])

    run = True
    while run:

        MAIN_WINDOW.fill(WHITE)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

        # update should always be last (other than clock tick)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
