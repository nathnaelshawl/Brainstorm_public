# Brainstorm drawing application
# created by: @nathnael_shawl(ናትናኤል ሻውል) last edited:5:09 PM Monday, April 25, 2022, 2022, Addis Ababa, Ethiopia
# Action_tools.py --> contains action tools i.e eye_dropper and fill tool
# ---------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------

# import dependencies and modules 
import pygame
from pygame.locals import *
from pygame import gfxdraw
from . import Global_setter
from . import Utilities
from . import Main_interface

# eye droper tool captures the color of the pressed screen location.
def eyeDroper():
    # setup
    mousedown = False
    select = True
    newscreen = Global_setter.screen.copy()
    
    # tool_main_loop 
    while select:
        # event_capture
        xPos, yPos = pygame.mouse.get_pos()
        try:
            color = Global_setter.screen.get_at((xPos,yPos))
        except:
            break
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                select = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousedown = True
            if event.type == pygame.MOUSEBUTTONUP:
                mousedown = False
        Main_interface.mainInterface(xPos, yPos, mousedown, True)
        
        # perform the eye droper function
        if Global_setter.drawingArea.collidepoint(xPos, yPos):
            pygame.draw.rect(Global_setter.screen, color, (xPos - 15, yPos - 15, 15, 15))
            pygame.draw.rect(Global_setter.screen, (0, 0, 0), (xPos - 15, yPos - 15, 15, 15), 1)
            if Global_setter.STATE != 'eyedroper':
                pygame.display.update()
                Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
                Main_interface.mainInterface(xPos, yPos, mousedown)
                return None
            elif mousedown:
                pygame.display.update()
                Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
                Main_interface.mainInterface(xPos, yPos, mousedown)
                return color
        else:
            select = False
        # update the interface
        pygame.display.update()
        Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))

# The fill tool 
# "The Fill Tool is used to pour large areas of paint on to the Canvas that expand until they find a border they cannot flow over."
# This version of fill tool uses the Four-way flood fill algorithm
# It checks the four neighbours(north, east, west and south sides) of the selected point wheather they have to be filled or not.
# It performs these checks on the new spawned points until it reaches a border at all ends.
#----------------------------------------------------------------------------------------------------------------------------------

def fill(x, y, color): 
    # setup
    
    checklist = [(x, y)]
    tobefilled = Global_setter.screen.get_at((x, y))
    blacklist = []
    fill = True
 
    # if the selected point has the same color with the fill color operation will be halted.
    if tobefilled == color:
        return None
        
    # tool main_loop
    # change the cursor to unavilable symbol
    Utilities.change_cursor()
    while fill:
        minilist = []
        for i in range(0, len(checklist)):
            xx, yy = checklist[i]
            minilist.append((xx, yy - 1))
            minilist.append((xx, yy + 1))
            minilist.append((xx - 1, yy))
            minilist.append((xx + 1, yy))
            blacklist.append((xx, yy))   
            for i in range(0, len(minilist)):
                xxx, yyy = minilist[i]
                if Global_setter.drawingArea.collidepoint(xxx, yyy) and Global_setter.screen.get_at((xxx,yyy)) == tobefilled:
                    gfxdraw.pixel(Global_setter.screen, xxx, yyy, color)
                    checklist.append((xxx,yyy))
            minilist = []  
        for i in range(0, len(blacklist)):
            flag = checklist.index(blacklist[i])        
            del checklist[flag]
        blacklist = []
        if len(checklist) <= 1:
            break     
# to look the fill tool work in slow motion remove the comment of the lines bellow
        # pygame.display.update()
    # manage the interface and show the fill
    pygame.display.update()
    # change back the default cursor.
    pygame.mouse.set_cursor()
    newscreen = Global_setter.screen.copy()
    Global_setter.SCREENLIST.append(newscreen)
    Main_interface.mainInterface(x, y, False, True, True, True)
# program_end.