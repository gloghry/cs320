import pygame
import sys
from math import *
pygame.init()
#sys.path.append(".")
from classesForMap import *

screen = pygame.display.set_mode([1500, 660]) #sets screen size

clock = pygame.time.Clock()
baseFont = pygame.font.Font(None, 20)
userInput = ''

#boxActive = False
active = True #declares that the program is actively running
trigger = False

def hexDraw(surface, color, radius, position):
    x, y = position
    xPoint = [0,0,0,0,0,0]
    yPoint = [0,0,0,0,0,0]
    for i in range(6):
        xPoint[i] = x + radius * cos(2 * pi * i / 6)
        yPoint[i] = y + radius * sin(2 * pi * i / 6)
    pygame.draw.polygon(surface, color, [(xPoint[0],yPoint[0]),
        (xPoint[1],yPoint[1]),
        (xPoint[2],yPoint[2]),
        (xPoint[3],yPoint[3]),
        (xPoint[4],yPoint[4]),
        (xPoint[5],yPoint[5])], width = 1)

def mapDraw(width, height, radius):
    #initial width draw
    x = radius
    y = radius
    for a in range(0, height):
        x = radius
        for i in range(0, width):
            hexDraw(screen, (0,0,0), radius, (x,y))
            x = radius*3 + x
            i = i + 1
        y = (radius*2 + y)-4
        a = a + 2
    #have to repeat above code to do the offset hexes
    y = radius*2 - 2
    for a in range(0, height):
        x = radius*2.5
        for i in range(0, (width-1)):
            hexDraw(screen, (0,0,0), radius, (x,y))
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
