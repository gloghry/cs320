import pygame
import sys
import random
from math import *

pygame.init()

screen = pygame.display.set_mode([1500, 800]) #sets screen size

random.seed(None) #initializes random number generator, with a seed of the current system date

#have 1014 tiles.
WATERTOTAL = random.randrange(100, 700) #min of about 10% water, to a maximum of about 75%
RUNBEFORE = False

clock = pygame.time.Clock()
baseFont = pygame.font.Font(None, 20)
userInput = ''
pygame.display.set_caption('Map Maker - V 0.1')

#color definitions
BLACK = (00,00,00)
WHITE = (255,255,255)
RED = (255, 139, 148) #extra color if needed
GREEN = (220, 237, 193) #grass
MOREGREEN = (139, 198, 147)#forest
BLUE = (168, 230, 207) #water
TANCOLOR = (255, 211, 182) #deserts
WHITECOLOR = (253, 243, 236) #tundra
TANCOLORTWO = (224, 198, 181) #beach
PINK = (255, 170, 165) #background

#font definitions
titleFont = pygame.font.Font(None, 40)
otherFont = pygame.font.Font(None, 20)

#define locations for where the text will be going for hex info.
textTitleBox = (1500/2-80, 570)

textLocBox = (10, 600)
#textLocBoxResponse =

textBiomeBox = (10, 640)
#textBiomeBoxResponse =

textTOneBox = (1500/2-300, 600)
#textTOneBoxResponse =

textTTwoBox = (1500/2-300, 640)
#textTTwoBoxResponse =

textTThreeBox = (1500/2-300, 680)
#textTThreeBoxResponse =

textTFourBox = (1500/2, 600)
#textTFourBoxResponse =

textTFiveBox = (1500/2, 640)
#textTFiveBoxResponse =

textTSixBox = (1500/2, 680)
#textTSixBoxResponse =

textDescBox = (10, 680)
#textDescBoxResponse =

#define the text that is static and unchanging
textTitle = titleFont.render('Info Pane', True, BLACK, None)
textLoc = otherFont.render('Location', True, BLACK, None)
textBiome = otherFont.render('Biome', True, BLACK, None)
textTOne = otherFont.render('Trait One:', True, BLACK, None)
textTTwo = otherFont.render('Trait Two:', True, BLACK, None)
textTThree = otherFont.render('Trait Three:', True, BLACK, None)
textTFour = otherFont.render('Trait Four:', True, BLACK, None)
textTFive = otherFont.render('Trait Five:', True, BLACK, None)
textTSix = otherFont.render('Trait Six:', True, BLACK, None)
textDesc = otherFont.render('Description', True, BLACK, None)

active = True #declares that the program is actively running
trigger = False
map = []

class HexBox: #this is the hex boxes which compose the map
    def __init__(self, radius, x, y):
        self.x = x
        self.y = y
        self.xPoint = [0,0,0,0,0,0] #list of the points that make up the hexagon
        self.yPoint = [0,0,0,0,0,0] #list of the points that make up the hexagon
        self.traits = ['TraitOne','TraitTwo','TraitThree','TraitFour','TraitFive','TraitSix'] #empty list ready to hold the traits that compose the hex
        self.number = 0 #blank identifier for the number of the hex, assigned when the hex is drawn.
        self.biome = '' #string to hold the biome name
        self.active = False #not current active (clicked on)
        self.color = GREEN #assigns a color for the lines
        self.radius = radius
        self.collisionBox = pygame.Rect(x, y, radius, radius) #gives the hex a collision box
        self.location = (0,0)

    def traitAssign(self):
        global RUNBEFORE
        global WATERTOTAL
        if not RUNBEFORE: #don't run this more than once per map.
            #if water total max isn't reached, this can also be a water tile, so random between 1 - 6 biomes
            biomeNum = random.randrange(100)
            if(WATERTOTAL != 0):
                #this can be a water tile, so it has a 30% chance of being one, until max is reached.
                #Aquatic - 30%
                #Beach - 10%
                #Grassland - 25%
                #Forest - 25%
                #Desert - 5%
                #Tundra - 5%
                if(biomeNum < 31): #aquatic
                    self.biome = 'Aquatic'
                    self.color = BLUE
                    WATERTOTAL = WATERTOTAL - 1
                elif(biomeNum < 41): #Beach
                    self.biome = 'Beach'
                    self.color = TANCOLORTWO
                elif(biomeNum < 66): #grassland
                    self.biome = 'Grassland'
                    self.color = GREEN
                elif(biomeNum < 91): #Forest
                    self.biome = 'Forest'
                    self.color = MOREGREEN
                elif(biomeNum < 96): #Desert
                    self.biome = 'Desert'
                    self.color = TANCOLOR
                else: #Tundra
                    self.biome = 'Tundra'
                    self.color = WHITECOLOR
            else: #if water total has been reached, this cannot be a water tile, so random between 1 - 5 biomes
                #Beach - 14%
                #Grassland - 36%
                #Forest - 36%
                #Desert - 7%
                #Tundra - 7%
                if(biomeNum < 15): #Beach
                    self.biome = 'Beach'
                    self.color = TANCOLORTWO
                elif(biomeNum < 51): #grassland
                    self.biome = 'Grassland'
                    self.color = GREEN
                elif(biomeNum < 87): #Forest
                    self.biome = 'Forest'
                    self.color = MOREGREEN
                elif(biomeNum < 94): #Desert
                    self.biome = 'Desert'
                    self.color = TANCOLOR
                else: #Tundra
                    self.biome = 'Tundra'
                    self.color = WHITECOLOR

        #now that biome is assigned, we need to read in the biome text file & assign traits

        #change trait text of this biome


    def draw(self, screen, x, y, q):
        self.location = q
        for i in range(6): #this draws the colored polygon
            self.xPoint[i] = x + self.radius * cos(2 * pi * i / 6)
            self.yPoint[i] = y + self.radius * sin(2 * pi * i / 6)
        pygame.draw.polygon(screen, self.color, [(self.xPoint[0],self.yPoint[0]),
            (self.xPoint[1],self.yPoint[1]),
            (self.xPoint[2],self.yPoint[2]),
            (self.xPoint[3],self.yPoint[3]),
            (self.xPoint[4],self.yPoint[4]),
            (self.xPoint[5],self.yPoint[5])])
        for i in range(6): #this draws the outline on the polygon
            self.xPoint[i] = x + self.radius * cos(2 * pi * i / 6)
            self.yPoint[i] = y + self.radius * sin(2 * pi * i / 6)
        pygame.draw.polygon(screen, BLACK, [(self.xPoint[0],self.yPoint[0]),
            (self.xPoint[1],self.yPoint[1]),
            (self.xPoint[2],self.yPoint[2]),
            (self.xPoint[3],self.yPoint[3]),
            (self.xPoint[4],self.yPoint[4]),
            (self.xPoint[5],self.yPoint[5])], width = 1)

def mapDraw(width, height, radius): #this runs all the required information to generate the hex map
    #initial width draw
    c = 0
    r = 0
    q = (c, r)
    x = radius
    y = radius
    for a in range(0, height):
        x = radius
        r = r + 1
        for i in range(0, width):
            currBox = HexBox(radius, x, y)
            currBox.traitAssign()
            currBox.draw(screen, x, y, q)
            map.append(currBox)
            c = c + 2
            x = radius*3 + x
            i = i + 1
        y = (radius*2 + y)-4
        a = a + 2
    #have to repeat above code to do the offset hexes
    c = 0
    r = 2
    y = radius*2 - 2
    for a in range(0, height):
        x = radius*2.5
        for i in range(0, (width)):
            currBox = HexBox(radius, x, y)
            currBox.draw(screen, x, y, q)
            map.append(currBox)
            c = c + 2
            x = radius*3 + x
            i = i + 1
        y = (radius*2 + y)-4
        a = a + 2

#main stuff below here
while active: #while the program is running...
    #if the user wants to quit, change active to false
    #textBox1 = TextBox(100, 100, 140, 32)
    #textBox2 = TextBox(100, 300, 140, 32)
    #textBoxes = [textBox1, textBox2]
    screen.fill(PINK)

    #now add in all the static text
    screen.blit(textTitle, textTitleBox)
    screen.blit(textLoc, textLocBox)
    screen.blit(textBiome, textBiomeBox)
    screen.blit(textTOne, textTOneBox)
    screen.blit(textTTwo, textTTwoBox)
    screen.blit(textTThree, textTThreeBox)
    screen.blit(textTFour, textTFourBox)
    screen.blit(textTFive, textTFiveBox)
    screen.blit(textTSix, textTSixBox)
    screen.blit(textDesc, textDescBox)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        if event.type == pygame.MOUSEBUTTONUP:
            mousePosX, mousePosY = pygame.mouse.get_pos()

            column = mousePosX / 39
            row = mousePosY / 26

            for hex in map:
                if((column, row) == hex.location):
                    print("a")
                    #display the info about the hexes
            #now we've identified that mouse is over a specific hex.

        #for box in textBoxes:
            #box.handle_event(event)
            #for box in textBoxes:
                #box.update()
                #screen.fill((255, 211, 211))
            #for box in textBoxes:
                #box.draw(screen)
                #pygame.display.flip()
                #clock.tick(30)

        #if event.type == pygame.MOUSEBUTTONDOWN:
            #if textBox.collidepoint(event.pos):
            #    active = True
            #else:
            #    active = False

        #if event.type == pygame.KEYDOWN:
        #    if event.key == pygame.K_BACKSPACE:
        #        userInput = userInput[:-1]
        #    else:
        #        userInput += event.unicode

    #screen.fill((211, 211, 211)) #fills background with a nice grey

    #pygame.draw.rect(screen, color, textBox)
    #textSurface = baseFont.render(userInput, True, (255, 255, 255))

    #screen.blit(textSurface, (textBox.x+5, textBox.y+5))

    #textBox.w = max(100, textSurface.get_width()+10)
    #pygame.display.flip()
    mapDraw(39, 26, 12.5)
    #refreshes screen, to show any updates
    pygame.display.flip()

#after while loop is done (i.e., user wants to quit, pygame closes.)
if(active == False):
    pygame.quit()
