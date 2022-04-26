import pygame
import os
import random

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


class Button:
    def __init__(self, x, y, w, h, text='', font_size=DEFAULT_FONT):
        if w < 0 or h < 0:
            raise ValueError("Not a valid window size!")
        self.text = text
        self.font_size = font_size
        self.color = BLUE
        self.font = pygame.font.Font(None, font_size)
        self.txt_surface = self.font.render(text, True, WHITE)
        if not text == '':
            w, h = self.font.size(self.text)
            self.rect = pygame.Rect(x, y, (w + WIDTH_SPACER), (h + HEIGHT_SPACER))
        else:
            self.rect = pygame.Rect(x, y, w, h)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.text == 'Generate Map ':
                    print("Not implemented yet, sorry!")
                elif self.text == 'Generate Character ':
                    print('Loading files....')
                    return generate_new_character()
                else:
                    print("That button isn't recognized...")
                    return None

    def draw(self, screen):
        # Background of the box
        # Width (last tuple value) 0 = fill
        pygame.draw.rect(screen, self.color, self.rect, 0)
        # Transparent box, would like to fill, but need the reverse color

        # Text formatted inside the box
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))


class TextBox:
    def __init__(self, x, y, w, h, text='', editable=False, font_size=DEFAULT_FONT):
        if w < 0 or h < 0:
            raise ValueError("Not a valid window size!")
        self.x_pos = x
        self.y_pos = y
        self.color = COLOR_INACTIVE
        self.text = text
        self.font_size = font_size
        self.font = pygame.font.Font(None, font_size)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False
        self.editable = editable
        if not text == '':
            w, h = self.font.size(self.text)
            # definitely some magic numbers below. The font.size needs to have extra padding to fit the box.
            # this is what I found works the best.
            self.rect = pygame.Rect(x, y, (w + WIDTH_SPACER), (h + HEIGHT_SPACER))
        else:
            self.rect = pygame.Rect(x, y, w, h)

    def handle_event(self, event):
        if self.editable:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = not self.active
                    pass
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
                    self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        # Background of the box
        pygame.draw.rect(screen, self.color, self.rect, 2)
        # Transparent box, would like to fill, but need the reverse color

        # Text formatted inside the box
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

    def update(self, screen):
        if not self.text == '':
            # Need to re-draw with text var, text may be updated by another function
            w, h = self.font.size(self.text)
            self.rect = pygame.Rect(self.x_pos, self.y_pos, (w + WIDTH_SPACER), (h + HEIGHT_SPACER))

            self.txt_surface = self.font.render(self.text, True, self.color)
            # Black text is sort of hard to read, white looks worse. Considered filling the Rectangle
            # And having a border, but that's two boxes and could have collision problems
            # pygame.draw.rect(screen, WHITE, self.rect, 0)
            pygame.draw.rect(screen, self.color, self.rect, 2)
            screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))


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
    welcome_box = TextBox(x, y, BOX_WIDTH, BOX_HEIGHT, "Welcome!", False, 52)
    all_boxes.append(welcome_box)

    # magic number based on how long the text is, not the size of the box really
    x = (WIN_WIDTH / 2) - (BOX_WIDTH / 2) - 200
    y = BOX_HEIGHT * 3
    cool_cam_intro = TextBox(x, y, BOX_WIDTH, BOX_HEIGHT, "To Dungeons, Dragons, and Code", False, 52)
    all_boxes.append(cool_cam_intro)

    x = (WIN_WIDTH / 2) - (BOX_WIDTH / 2)
    y = WIN_HEIGHT - (BOX_HEIGHT * 8)
    credits_box = TextBox(x, y, BOX_WIDTH, BOX_HEIGHT, "Credits", False, 52)
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
        cur_person = TextBox(x, y, BOX_WIDTH, BOX_HEIGHT, name, False, DEFAULT_FONT)
        x += cur_person.rect.width
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
        input_box = TextBox(x, y, BOX_WIDTH, BOX_HEIGHT, text, True, DEFAULT_FONT)
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

    # manually find the size of the font, so we can move it away from the edge of the screen
    button_text = 'Generate Character '
    w, h = pygame.font.Font(None, DEFAULT_FONT).size(button_text)
    w, h = (w + WIDTH_SPACER), (h + HEIGHT_SPACER)
    generate_char = Button(WIN_WIDTH - w - 30, (WIN_HEIGHT / 2) + (5 * h), w, h, button_text, DEFAULT_FONT)

    # manually find the size of the font, so we can move it away from the edge of the screen
    button_text = 'Generate Map '
    w, h = pygame.font.Font(None, DEFAULT_FONT).size(button_text)
    w, h = (w + WIDTH_SPACER), (h + HEIGHT_SPACER)
    generate_map = Button(WIN_WIDTH - w - 30, (WIN_HEIGHT / 2) + (6 * h), w, h, button_text, DEFAULT_FONT)

    buttons.append(generate_map)
    buttons.append(generate_char)

    run = True
    while run:

        MAIN_WINDOW.blit(BACKGROUND_SCALED, (0, 0))
        for event in pygame.event.get():
            for box in input_boxes:
                box.handle_event(event)
            for button in buttons:
                ret = button.handle_event(event)
                if ret is not None:
                    # THIS ALGORITHM SUCKS MAJOR YOU KNOW WHAT, BUT I CAN'T FIGURE OUT HOW TO MAKE IT BETTER???
                    for i in range(len(input_boxes)):
                        input_boxes[i].text = box_texts[i] + ret[i]
                        input_boxes[i].update(MAIN_WINDOW)

            if event.type == pygame.QUIT:
                run = False

        for box in input_boxes:
            box.draw(MAIN_WINDOW)
        for button in buttons:
            button.draw(MAIN_WINDOW)

        # update should always be last (other than clock tick)
        pygame.display.update()
        clock.tick(FPS)


def generate_new_character():
    gender = generate_gender()
    race = generate_race()
    name = generate_name(race, gender)
    _class = generate_class()
    background = generate_background()
    quirk = generate_quirk()

    # print(name, race, gender, _class, background, quirk)

    return name, race, gender, _class, background, quirk


def generate_gender():
    _gender = random.randint(1, 2)  # Range should be increased to 3 for NB
    if _gender == 2:
        gender = 'Male'
    elif _gender == 1:
        gender = 'Female'
    else:
        gender = 'NB'
        # Used for error checking right now, could be used for NB in the future
        # files not implemented for NB
    return gender


def generate_race():
    race_path = os.path.join('Code Work-Julion', 'CharDatabase', 'Race', '$List.txt')
    try:
        with open(race_path, 'r+') as race_file:
            all_races = race_file.readlines()  # store the entire file in mem (should be small)
            count = len(all_races)  # line count
            race = all_races[(random.randint(1, count) - 1)].rsplit('\n', 1)[0]  # get one of the random lines
            if 'Human' in race:  # Remove whether standard or variant human subtype
                race = 'Human'
    except FileNotFoundError:
        print("Race file moved, deleted, or otherwise changed. Check position")
        race = 'ERR'
    return race


def generate_name(race, gender):
    if race == 'ERR': return "ERR"

    if random.randint(1, 4) == 1:
        use_title = True
    else:
        use_title = False

    name_filename = '' + str(race) + '_' + str(gender) + '.txt'
    name_path = os.path.join('gui', 'Names', name_filename)
    try:
        with open(name_path, 'r+') as name_file:
            all_names = name_file.readlines()  # store the entire file in mem. I won't have more than maybe 15 names per file
            count = len(all_names)
            name = all_names[(random.randint(1, count) - 1)].rsplit('\n', 1)[0]
    except FileNotFoundError:
        name = "Boaty McBoatface"

    if use_title:
        title_path = os.path.join('gui', 'Titles', 'Titles')
        try:
            with open(title_path, 'r+') as title_file:
                all_titles = title_file.readlines()
                count = len(all_titles)
                title = all_titles[(random.randint(1, count) - 1)].rsplit('\n', 1)[0]
                name += " " + title
        except FileNotFoundError:
            print("Titles file moved, or otherwise unreadable")

    return name


def generate_class():
    _class_path = os.path.join('Code Work-Julion', 'CharDatabase', 'Class', '$List.txt')
    try:
        with open(_class_path, 'r+') as _class_file:
            all_classes = _class_file.readlines()  # store the entire file in mem (should be small)
            count = len(all_classes)  # line count
            _class = all_classes[(random.randint(1, count) - 1)].rsplit('\n', 1)[0]  # get one of the random lines
    except FileNotFoundError:
        print("Class file moved, deleted, or otherwise changed. Check position")
        _class = 'ERR'

    return _class


def generate_background():
    background_path = os.path.join('Code Work-Julion', 'CharDatabase', 'Background', '$List.txt')
    try:
        with open(background_path, 'r+') as background_file:
            all_backgrounds = background_file.readlines()  # store the entire file in mem (should be small)
            count = len(all_backgrounds)  # line count
            background = all_backgrounds[(random.randint(1, count) - 1)].rsplit('\n', 1)[
                0]  # get one of the random lines
    except FileNotFoundError:
        print("Class file moved, deleted, or otherwise changed. Check position")
        background = 'ERR'

    return background


def generate_quirk():
    quirk_path = os.path.join('gui', 'Quirks', 'Quirks.txt')
    try:
        with open(quirk_path, 'r+') as quirk_file:
            all_quirks = quirk_file.readlines()  # store the entire file in mem (should be small)
            count = len(all_quirks)  # line count
            quirk = all_quirks[(random.randint(1, count) - 1)].rsplit('\n', 1)[0]  # get one of the random lines
    except FileNotFoundError:
        print("Class file moved, deleted, or otherwise changed. Check position")
        quirk = 'You stare into the void... Often...'

    return quirk


if __name__ == "__main__":
    # opening_window()
    main()
