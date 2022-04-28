import pygame
import os
import random

pygame.init()
pygame.display.init()
pygame.font.init()


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

COLOR_INACTIVE = BLACK
COLOR_ACTIVE = WHITE

WIDTH_SPACER = 12
HEIGHT_SPACER = 10

DEFAULT_FONT = 32


class SearchBox:
    def __init__(self, x, y, w, h, text='Search for lore here! '):
        if w < 0 or h < 0:
            raise ValueError("Not a valid window size!")
        self.x_pos = x
        self.y_pos = y

        self.color = BLUE
        self.color_text = WHITE
        self.active = False

        self.text = text
        self.font = pygame.font.Font(None, DEFAULT_FONT)
        self.txt_surface = self.font.render(text, True, self.color_text)
        w, h = self.font.size(self.text)
        self.first_click = True

        self.box = BorderedBox(x, y, (w + WIDTH_SPACER), (h + HEIGHT_SPACER), self.color, WHITE)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.box.handle_event(event):
                self.active = not self.active
                if self.first_click:
                    self.text = ''
                    self.first_click = False
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    print("Running the search function")
                    os.system("cd lore_searcher; python3 lore_GUI.py " + self.text)
                else:
                    self.text += event.unicode

        self.txt_surface = self.font.render(self.text, True, self.color_text)

    def draw(self, screen):
        # Background of the box
        self.box.draw(screen)
        # Transparent box, would like to fill, but need the reverse color

        # Text formatted inside the box
        screen.blit(self.txt_surface, (self.x_pos + 5, self.y_pos + 5))


class TextBox:
    def __init__(self, x, y, w, h, text='', editable=False, font_size=DEFAULT_FONT):
        if w < 0 or h < 0:
            raise ValueError("Not a valid window size!")
        self.x_pos = x
        self.y_pos = y

        self.color = COLOR_INACTIVE
        self.color_text = WHITE

        self.text = text
        self.font_size = font_size
        self.font = pygame.font.Font(None, font_size)
        self.txt_surface = self.font.render(text, True, self.color_text)

        self.active = False
        self.editable = editable

        if not text == '':
            w, h = self.font.size(self.text)
            # definitely some magic numbers below. The font.size needs to have extra padding to fit the box.
            # this is what I found works the best.
            self.box = BorderedBox(x, y, (w + WIDTH_SPACER), (h + HEIGHT_SPACER))
        else:
            self.box = BorderedBox(x, y, w, h)

    def handle_event(self, event):
        if self.editable:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.box.handle_event(event):
                    self.active = not self.active
                else:
                    self.active = False
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        self.text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
                    # Re-render the text.
            self.txt_surface = self.font.render(self.text, True, self.color_text)

    def update(self, screen):
        # If update has been called, there should be text in the box now
        if self.text == '':
            raise ValueError('Error, text box is too small')
        w, h = self.font.size(self.text)
        self.box.update(self.x_pos, self.y_pos, (w + WIDTH_SPACER), (h + HEIGHT_SPACER))

        self.box.draw(screen)
        self.draw(screen)

    def draw(self, screen):
        # Background of the box
        self.box.draw(screen)
        # Transparent box, would like to fill, but need the reverse color

        # Text formatted inside the box
        screen.blit(self.txt_surface, (self.x_pos + 5, self.y_pos + 5))


class BorderedBox:
    def __init__(self, x, y, w, h, background_color=COLOR_INACTIVE, border_color=COLOR_ACTIVE):
        self.inner_rect = pygame.Rect(x, y, w, h)
        self.outer_rect = pygame.Rect(x, y, w, h)
        self.active = False
        self.inner_color = background_color
        self.outer_color = background_color
        self.border_color = border_color

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.inner_rect.collidepoint(event.pos) or self.outer_rect.collidepoint(event.pos):
                collision = True
                self.active = not self.active
            else:
                collision = False
                self.active = False
            # Change the current color of the input box.
            if self.active:
                self.outer_color = self.border_color
            else:
                self.outer_color = self.inner_color

            return collision

    def draw(self, screen):
        pygame.draw.rect(screen, self.inner_color, self.inner_rect, 0)
        pygame.draw.rect(screen, self.outer_color, self.outer_rect, 2)

    def update(self, x, y, w, h):
        self.inner_rect = pygame.Rect(x, y, w, h)
        self.outer_rect = pygame.Rect(x, y, w, h)
        return self


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
                    print("Opening and running Map Maker")
                    # os.system use C for system calls. You can run multiple commands with ;
                    os.system("cd MapMaker; python3 mapmaker.py")
                    os.system("pwd")
                elif self.text == 'Generate Character ':
                    print('Loading files....')
                    return generate_new_character()
                elif self.text == 'Search ':
                    pass
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


def generate_new_character():
    gender = generate_gender()
    race = generate_race()
    name = generate_name(race, gender)
    _class = generate_class()
    background = generate_background()
    quirk = generate_quirk()

    # print(name, race, gender, _class, background, quirk)

    return name, race, gender, _class, quirk, background


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
