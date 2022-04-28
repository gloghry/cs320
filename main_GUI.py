import pygame
import os
import gui.Classes.gui_classes as gc

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

# Import background image
BACKGROUND_LARGE = pygame.image.load(
    os.path.join('gui', 'Assets/desert.jpg'))
BACKGROUND_SCALED = pygame.transform.scale(
    BACKGROUND_LARGE, (WIN_WIDTH, WIN_HEIGHT))

COLOR_INACTIVE = BLACK
COLOR_ACTIVE = WHITE


def opening_window():
    if not pygame.display.get_init():
        pygame.display.init()

    clock = pygame.time.Clock()
    MAIN_WINDOW.fill(BLACK)
    run = True

    all_boxes = []

    # Box doesn't size to fit text, so we have to plug in magic numbers to format
    # there is a magic "random" number at the end here to better center. Not precise.
    x = (WIN_WIDTH / 2) - (BOX_WIDTH / 2) - 25
    y = BOX_HEIGHT
    welcome_box = gc.TextBox(x, y, BOX_WIDTH, BOX_HEIGHT, "Welcome!", False, 52)
    all_boxes.append(welcome_box)

    # magic number based on how long the text is, not the size of the box really
    x = (WIN_WIDTH / 2) - (BOX_WIDTH / 2) - 200
    y = BOX_HEIGHT * 3
    cool_cam_intro = gc.TextBox(x, y, BOX_WIDTH, BOX_HEIGHT, "To Dungeons, Dragons, and Code", False, 52)
    all_boxes.append(cool_cam_intro)

    x = (WIN_WIDTH / 2) - (BOX_WIDTH / 2)
    y = WIN_HEIGHT - (BOX_HEIGHT * 8)
    credits_box = gc.TextBox(x, y, BOX_WIDTH, BOX_HEIGHT, "Credits", False, 52)
    all_boxes.append(credits_box)

    our_names = []
    # ALPHABETICAL BY LAST NAME
    # Jared Diamond
    # Garett Loghry
    # Julion Oddy
    # Levicy Radeleff
    # Peter Wanner
    names = ["Jared Diamond,", "Garett Loghry,", "Julion Oddy,", "Levicy Radeleff,", "Peter Wanner"]
    y = WIN_HEIGHT - (BOX_HEIGHT * 6)
    x = 30

    for name in names:
        cur_person = gc.TextBox(x, y, BOX_WIDTH, BOX_HEIGHT, name, False, DEFAULT_FONT)
        x += cur_person.box.outer_rect.width
        our_names.append(cur_person)
        all_boxes.append(cur_person)

    timer = 0

    while run:
        for event in pygame.event.get():
            for box in all_boxes:
                box.handle_event(event)
            if event.type == pygame.QUIT:
                run = False

        for box in all_boxes:
            box.txt_surface = box.font.render(box.text, True, WHITE)
            box.draw(MAIN_WINDOW)

        # update should always be last (other than clock tick)
        pygame.display.update()
        clock.tick(FPS)

        # Check to see if it's been more than 4 seconds
        if timer > 4:
            # Close this window if > than timer
            run = False
        else:
            # increment timer and wait 1 second
            pygame.time.wait(1000)
            timer += 1


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
    x = margin = WIN_HEIGHT / 10
    height_offset = int(WIN_HEIGHT - margin)
    # width_offset = WIN_WIDTH - margin
    y = increment = int(height_offset / 7)

    input_boxes = []
    # occupation not used yet/ever
    box_texts = ['Name: ', 'Race: ', 'Gender: ', 'Class: ', 'Quirk: ', 'Background: ']  # , 'Occupation: ']

    for text in box_texts:
        input_box = gc.TextBox(x, y, BOX_WIDTH, BOX_HEIGHT, text, True, DEFAULT_FONT)
        y += increment
        input_boxes.append(input_box)

    """
    input_boxes[0].text = 'Name'
    input_boxes[1].text = 'Race'
    input_boxes[2].text = 'Gender'
    input_boxes[3].text = 'Class'
    input_boxes[4].text = 'Quirks'
    input_boxes[5].text = 'Background'
    input_boxes[6].text = 'Occupation'
    """

    buttons = []
    button_text_list = ['Generate Character ', 'Generate Map ', 'Open Database ']
    last_button_height = 0
    y_spacer = 15

    # manually find the size of the font, so we can move it away from the edge of the screen
    for string in button_text_list:
        w, h = pygame.font.Font(None, DEFAULT_FONT).size(string)
        w, h = (w + WIDTH_SPACER), (h + HEIGHT_SPACER)
        button = gc.Button(WIN_WIDTH - w - 30, (WIN_HEIGHT / 2) + last_button_height, w, h, string, DEFAULT_FONT)
        buttons.append(button)
        last_button_height += h + y_spacer

    w, h = pygame.font.Font(None, DEFAULT_FONT).size('Search for lore here! ')
    search_box = gc.SearchBox(WIN_WIDTH - w - margin, margin, w, h)

    run = True
    while run:

        MAIN_WINDOW.blit(BACKGROUND_SCALED, (0, 0))
        for event in pygame.event.get():
            for box in input_boxes:
                box.handle_event(event)
                box.update(MAIN_WINDOW)
            for button in buttons:
                ret = button.handle_event(event)
                if ret is not None:
                    for i in range(len(input_boxes)):
                        input_boxes[i].text = box_texts[i] + ret[i]
                        input_boxes[i].update(MAIN_WINDOW)
            search_box.handle_event(event)

            if event.type == pygame.QUIT:
                run = False

        for box in input_boxes:
            box.draw(MAIN_WINDOW)
        for button in buttons:
            button.draw(MAIN_WINDOW)
        search_box.draw(MAIN_WINDOW)

        # update should always be last (other than clock tick)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    # opening_window()
    main()
