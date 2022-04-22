import pygame
import sys
from math import *
pygame.init()


screen = pygame.display.set_mode([1500, 660]) #sets screen size

clock = pygame.time.Clock()
baseFont = pygame.font.Font(None, 20)
userInput = ''

active = True #declares that the program is actively running
trigger = False

class HexBox: #this is the hex boxes which compose the map
    def __init__(self, radius, x, y):
        self.x = x
        self.y = y
        self.xPoint = [0,0,0,0,0,0] #list of the points that make up the hexagon
        self.yPoint = [0,0,0,0,0,0] #list of the points that make up the hexagon
        self.traits = ['','','','','',''] #empty list ready to hold the traits that compose the hex
        self.number = 0 #blank identifier for the number of the hex, assigned when the hex is drawn.
        #self.biome = class for biome call here
        self.active = False #not current active (clicked on)
        self.color = pygame.Color('chartreuse4') #assigns a color for it
        self.radius = radius
        self.collisionBox = Collider(radius, x, y) #gives the hex a collision box

    def draw(self, screen, x, y, q):
        self.number = q
        for i in range(6):
            self.xPoint[i] = x + self.radius * cos(2 * pi * i / 6)
            self.yPoint[i] = y + self.radius * sin(2 * pi * i / 6)
        pygame.draw.polygon(screen, self.color, [(self.xPoint[0],self.yPoint[0]),
            (self.xPoint[1],self.yPoint[1]),
            (self.xPoint[2],self.yPoint[2]),
            (self.xPoint[3],self.yPoint[3]),
            (self.xPoint[4],self.yPoint[4]),
            (self.xPoint[5],self.yPoint[5])], width = 1)

class Collider: #this creates colliders in each hex, which will be checked when seeing if the user has moused over a hex
    def __init__(self, width, x, y):
        self.x1 = x
        self.y1 = y
        self.x2 = x+width
        self.y2 = y+width

def mapDraw(width, height, radius): #this runs all the required information to generate the hex map
    #initial width draw
    map = []
    q = 1

    x = radius
    y = radius
    for a in range(0, height):
        x = radius
        for i in range(0, width):
            currBox = HexBox(radius, x, y)
            currBox.draw(screen, x, y, q)
            map.append(currBox)
            q = q+1
            x = radius*3 + x
            i = i + 1
        y = (radius*2 + y)-4
        a = a + 2
    #have to repeat above code to do the offset hexes
    y = radius*2 - 2
    for a in range(0, height):
        x = radius*2.5
        for i in range(0, (width-1)):
            currBox = HexBox(radius, x, y)
            currBox.draw(screen, x, y, q)
            map.append(currBox)
            q = q+1
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
    screen.fill((255, 211, 211))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
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
    mapDraw(40, 26, 12.5)
    #refreshes screen, to show any updates
    pygame.display.flip()

#after while loop is done (i.e., user wants to quit, pygame closes.)
if(active == False):
    pygame.quit()
