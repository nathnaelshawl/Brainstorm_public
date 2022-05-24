# Brainstorm drawing application
# created by: @nathnael_shawl(ናትናኤል ሻውል) last edited: 11:40 PM Sunday, April 10, 2022, Addis Ababa, Ethiopia
# Drag_box.py --> creates several Drag and drop boxes to manage different values. 
# contains sizeDragBox(), hueDragBox(), saturationDragBox(), luminosityDragBox() and RGBdragbox() functions.
# ---------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------

# import dependencies and modules 
import pygame
from pygame.locals import *
from . import Global_setter
from . import Color_mngt

# Used to set a variable drag and drop slider to set values used for fillet radius, size and number of sides option. 
def sizeDragBox(x, y, color, span, thickness, maxiumAlowedSize, size, forSide=False):

    # draw the drag and drop box
    pygame.draw.line(Global_setter.screen, Global_setter.BLACK, (x, y - (1)), (x + span, y - (1)), thickness)
    pygame.draw.rect(Global_setter.screen, Global_setter.COLOR, (x + span*(size/maxiumAlowedSize), y - round(10 + 5*(size/maxiumAlowedSize))/2, 6 + 5*size/maxiumAlowedSize, 10 + 5*size/maxiumAlowedSize), 0, 2)
    pygame.draw.rect(Global_setter.screen, Global_setter.BLACK, (x + span*(size/maxiumAlowedSize), y - round(10 + 5*(size/maxiumAlowedSize))/2, 6 + 5*size/maxiumAlowedSize, 10 + 5*size/maxiumAlowedSize), 1, 2)
    # import fonts for written values
    fonts_dir = Global_setter.APP_PATH + '\\fonts\\'
    FONT = pygame.font.Font(fonts_dir + 'OpenSans-Light.ttf', 14)
    if forSide:
        sizeSurf = FONT.render(str(size + 2), True, (0, 0, 0), (240, 240, 240))
    else:
        sizeSurf = FONT.render(str(size), True, (0, 0, 0), (240, 240, 240))
    buttonRect = pygame.Rect(x + span + 15, y - 10, 10, 10)
    Global_setter.screen.blit(sizeSurf, buttonRect)
    drag_collision_rect = pygame.Rect(x , y - 15, span + 10, 30)
    # collision area rectangle bounding box 
    #pygame.draw.rect(Global_setter.screen, (0, 0, 0), drag_collision_rect, width=1)
    return drag_collision_rect

# hue varying drag and drop slider
def hueDragBox(x, y, width, colorsList, index, hueValue):
    collision_width = 3*width
    for i in range(len(colorsList)):
        pygame.draw.line(Global_setter.screen, colorsList[i][index], (x + i, y), (x + i, y + width), 1)
    pygame.draw.rect(Global_setter.screen, (100, 100, 100), (x, y, len(colorsList), width + 1), 1)
    pygame.draw.rect(Global_setter.screen, colorsList[hueValue][index], (x + hueValue - 3, y - 1, 6, width + 3))
    pygame.draw.rect(Global_setter.screen, Global_setter.BLACK, (x + hueValue - 3, y - 1, 6, width + 3), 1)
    
    drag_collision_rect = pygame.Rect(x - 10, y - collision_width/4, 174, collision_width)
    # collision area rectangle bounding box 
    # pygame.draw.rect(Global_setter.screen, (0, 0, 0), drag_collision_rect, width=1)
    return drag_collision_rect
    
# saturation varying drag and drop slider.
def saturationDragBox(x, y, width, colorsList, index, saturationValue):
    collision_width = 2*width
    for i in range(len(colorsList[index])):
        pygame.draw.line(Global_setter.screen, colorsList[index][i], (x , y + i), (x + width, y + i), 1)
    pygame.draw.rect(Global_setter.screen, (100, 100, 100), (x, y, width + 1, len(colorsList[1])), 1)
    pygame.draw.rect(Global_setter.screen, colorsList[index][saturationValue], (x - 1, y + saturationValue - 3, width + 3, 6))
    pygame.draw.rect(Global_setter.screen, Global_setter.BLACK, (x - 1, y + saturationValue - 3, width + 3, 6), 1)
    drag_collision_rect = pygame.Rect(x - collision_width/4, y - 5, collision_width, 140)
    # collision area rectangle bounding box 
    # pygame.draw.rect(Global_setter.screen, (0, 0, 0), drag_collision_rect, width=1)
    return drag_collision_rect
   
# luminosity varying drag and drop slider.   
def luminosityDragBox(x, y, width, LUMNOSITY, RAWCOLOR, customColor):
    collision_width = 2.5*width
    pygame.draw.rect(Global_setter.screen, (100,100,100), (x - 1, y - 1, width + 2, 129),1)
    y = y + 126
    for i in range(127):
        if i < 63: 
            color = (int(i*(RAWCOLOR[0]/63)), int(i*(RAWCOLOR[1]/63)), int(i*(RAWCOLOR[2]/63)))
        if i == 63:
            color = RAWCOLOR
        if i > 63:
            color = ((int((((i - 63)*(255 - RAWCOLOR[0]))/63) + RAWCOLOR[0])), (int((((i - 63)*(255 - RAWCOLOR[1]))/63) + RAWCOLOR[1])), (int((((i - 63)*(255 - RAWCOLOR[2]))/63) + RAWCOLOR[2])))
        pygame.draw.line(Global_setter.screen, color, (x, y - i), (x + width -1, y - i), 1)
    luminosityDragRect = pygame.Rect(x - 2, y - LUMNOSITY - 3, width + 4, 6)
    pygame.draw.rect(Global_setter.screen, customColor, (luminosityDragRect))
    pygame.draw.rect(Global_setter.screen, Global_setter.BLACK, (luminosityDragRect), 1)
    
    drag_collision_rect = pygame.Rect(x - collision_width/4, y - 130, collision_width, 140)
    # pygame.draw.rect(Global_setter.screen, (0, 0, 0), drag_collision_rect, width=1)
    return drag_collision_rect

# RGB color selector drag and drop slider.
def RGBdragbox(x, y, width, span, gapSize):
    drag_collision_rects = []
    collision_width = 2*width
    for i in range(3):
        for j in range((span + 1)):
            RGB = [(round(j*(255/(span))), 0, 0), (0, round(j*(255/(span))), 0), (0, 0, round(j*(255/(span))))]
            color = RGB[i]
            pygame.draw.line(Global_setter.screen, color, (x + j, y + i*gapSize), ( x + j, y + width - 1 + i*gapSize),  1)
        pygame.draw.rect(Global_setter.screen, (100,100,100), (x - 1, y + i*gapSize, span + 3, width),1) 
        pygame.draw.rect(Global_setter.screen, Global_setter.BLACK, ( x + int(Global_setter.COLOR[i]*(span/255)), y + width - 1 + i*gapSize - width, 6, width + 2), 0, 1)
        pygame.draw.rect(Global_setter.screen, Global_setter.WHITE, ( x + int(Global_setter.COLOR[i]*(span/255)) + 1, y + width - 1 + i*gapSize - width + 1, 6 - 2, width), 0, 1)
        
        drag_collision_rects.append(pygame.Rect( x- 10, y + i*gapSize - collision_width/4, span + 20, collision_width))
        # drag_collision_rects bounding box
        # pygame.draw.rect(Global_setter.screen, (0, 0, 0), drag_collision_rects[i], width=1)
    return drag_collision_rects   
# program_end.