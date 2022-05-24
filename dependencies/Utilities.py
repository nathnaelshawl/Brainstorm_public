# Brainstorm drawing application
# created by: @nathnael_shawl(ናትናኤል ሻውል) last edited: 5:16 PM Monday, April 25, 2022, Addis Ababa, Ethiopia
# Utilities.py --> supporting files to manage repetative tasks.
# contains KeyPressed(), CenterSquareRect(), buttonRECT(), buttons(), colorBox() and drawTextBox()
#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------

# import dependencies and modules 
import pygame
from pygame.locals import *
from . import Global_setter

# Captures key press events.
def keyPressed(inputKey):
    keyPressed = pygame.key.get_pressed()
    if keyPressed[inputKey]:
        return True
    else:
        return False 
        
# draws rectangle based on a given center and length value.
def CenterSquareRect(x, y, length):
    RECT= pygame.Rect(x - length/2, y - length/2, length, length)
    return RECT

# Returns the rect object from a given starting points, width and height of a given data. 
def buttonRECT(x, y, buttonWidth, buttonHeight):
    buttonRect = pygame.Rect(x - buttonWidth/2, y -  buttonHeight/2, buttonWidth, buttonHeight)
    RECT = (x, y, buttonWidth, buttonHeight)
    return (buttonRect, RECT)
    
# Draws buttons with different modes. pressed, when the button is hoovered and also when it is in idle mode.
def buttons(RECT, condition):
    x, y, buttonWidth, buttonHeight = RECT
    buttonRect = buttonRECT(x, y, buttonWidth, buttonHeight)[0]
    if condition == 'pressed':  
        QUITSURF = Global_setter.screen.copy()
        QUITSURF = QUITSURF.convert_alpha()     
        pygame.draw.rect(QUITSURF, (150, 200,255, 90), (buttonRect), 0, 2)
        Global_setter.screen.blit(QUITSURF, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
        pygame.draw.rect(Global_setter.screen, (150, 200,255), (buttonRect), 1, 2)
    elif condition == 'hoover':
        pressedSurf = Global_setter.screen.copy()
        pressedSurf.convert_alpha()
        pygame.draw.rect(pressedSurf, (200,200,200), (buttonRect), 1, 2)
        Global_setter.screen.blit(pressedSurf, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
        pygame.display.update()
    elif condition == 'idle':
        #pygame.draw.rect(Global_setter.screen, (20 ,200,200), (buttonRect), 0, 2)
        pygame.draw.rect(Global_setter.screen, (200,200,200), (buttonRect), 1, 2)

# draws color boxes with color fill.
def colorBox(x, y, width, color, fillet=1):   
    # show selected color with box.
    colorBoxRect = pygame.Rect(x, y, width, width)
    pygame.draw.rect(Global_setter.screen, color, (colorBoxRect), 0, fillet)
    pygame.draw.rect(Global_setter.screen, (100,100,100), (colorBoxRect), 2, fillet)
    return colorBoxRect  

# draws text with a transparent background and end outline.
def drawTextBox(text, font, textColor, rect, alpha):
    textsurface=font.render(text, True, textColor)
    surface=pygame.Surface((rect.width, rect.height))
    surface.fill((255, 255, 255))
    surface.blit(textsurface, pygame.Rect(0, 0, rect.width, rect.height))
    surface.set_alpha(alpha)
    pygame.draw.rect(Global_setter.screen, (0, 0, 0), rect, width=1)
    Global_setter.screen.blit(surface, rect)

# changes the type of the cursor.
# code is copy from pygame library example code.
def change_cursor():
    arrow = (
    "                        ",
    "                        ",
    "         XXXXXX         ",
    "       XX......XX       ",
    "      X..........X      ",
    "     X....XXXX....X     ",
    "    X...XX    XX...X    ",
    "   X.....X      X...X   ",
    "   X..X...X      X..X   ",
    "  X...XX...X     X...X  ",
    "  X..X  X...X     X..X  ",
    "  X..X   X...X    X..X  ",
    "  X..X    X.,.X   X..X  ",
    "  X..X     X...X  X..X  ",
    "  X...X     X...XX...X  ",
    "   X..X      X...X..X   ",
    "   X...X      X.....X   ",
    "    X...XX     X...X    ",
    "     X....XXXXX...X     ",
    "      X..........X      ",
    "       XX......XX       ",
    "         XXXXXX         ",
    "                        ",
    "                        ",
    )

    hotspot = None
    for y, line in enumerate(arrow):
        for x, char in enumerate(line):
            if char in ["x", ",", "O"]:
                hotspot = x, y
                break
        if hotspot is not None:
            break
    if hotspot is None:
        raise Exception("No hotspot specified for cursor '%s'!" % arrow)
    s2 = []
    for line in arrow:
        s2.append(line.replace("x", "X").replace(",", ".").replace("O", "o"))
    cursor, mask = pygame.cursors.compile(s2, "X", ".", "o")
    size = len(arrow[0]), len(arrow)
    pygame.mouse.set_cursor(size, hotspot, cursor, mask)
#program_end.