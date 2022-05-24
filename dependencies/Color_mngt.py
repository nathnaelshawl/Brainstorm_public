# Brainstorm drawing application
# created by: @nathnael_shawl(ናትናኤል ሻውል) last edited:2:39 PM Sunday, April 10, 2022, Addis Ababa, Ethiopia
# Color_mngt.py --> manages color and color related components. 
# contains editColorsWindow(), currentColor(), columnHueSat() and colorSelector() functions.
# ---------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------

# import dependencies and modules 
import pygame
from pygame.locals import *
from pygame import gfxdraw
from . import Global_setter
from . import Drag_box
from . import Utilities

# creates the editColorsWindow based on data.
def editColorsWindow(RAWCOLOR, LUMNOSITY,editcolorsWinX, editcolorsWinY, isColorBoxPressed, customColor, QuitColor=(255, 255, 255)):
    
    # create a shadow for the window
    #shadowScreen = Global_setter.screen.copy()
    #shadowScreen = shadowScreen.convert_alpha()
    #for i in range(10, 0, -1):
        #pygame.draw.rect(shadowScreen, (0, 0, 0, int(1.5*i)), (editcolorsWinX - ((10 - i)/1), editcolorsWinY - ((10 - i)/1), 300 + 2*(((10 - i)/1)), 300 + 2*(((10 - i)/1))), 1, 10)
    #Global_setter.screen.blit(shadowScreen, ( 0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
    
    # import the font files 
    fonts_dir = Global_setter.APP_PATH + '\\fonts\\'
    FONT = pygame.font.Font(fonts_dir + 'OpenSans-Light.ttf', 12)
    
    # build the interface
    
    pygame.draw.rect(Global_setter.screen, (235, 235, 235), (editcolorsWinX, editcolorsWinY, 300, 300))
    colorwindowDragRect = pygame.Rect(editcolorsWinX, editcolorsWinY, 300, 30)
    pygame.draw.rect(Global_setter.screen, (255, 255, 255), (colorwindowDragRect))
    QuitRect = pygame.Rect(editcolorsWinX + 270, editcolorsWinY, 30, 30)
    pygame.draw.rect(Global_setter.screen, QuitColor, (editcolorsWinX + 270, editcolorsWinY, 30, 30))
    if QuitColor == (225, 0, 0):
        QuitXcolor = (240, 240, 240)
    else:
        QuitXcolor = (120, 120, 120)
    pygame.draw.line(Global_setter.screen, QuitXcolor, (editcolorsWinX + 300 - 30 + 10, editcolorsWinY + 10), (editcolorsWinX + 270 + 20, editcolorsWinY + 20), 2)
    pygame.draw.line(Global_setter.screen, QuitXcolor, (editcolorsWinX + 300 - 30 + 10 + 10 , editcolorsWinY + 10), (editcolorsWinX + 270 + 20 - 10, editcolorsWinY + 20), 2)
    
    pygame.draw.rect(Global_setter.screen, (120, 120, 120), (editcolorsWinX, editcolorsWinY, 300, 300), 1, 1)
    #color selector 
    #colorSelector(spanLength, x, y)
    
    colorSelectorX = editcolorsWinX + 90
    colorSelectorY = editcolorsWinY + 40
     
    # luminosity preference.
    luminosityX = colorSelectorX + 166 + 25
    luminosityY = colorSelectorY 
    luminositywidth = 9
    luminosityDragRect = Drag_box.luminosityDragBox(luminosityX, luminosityY, luminositywidth, LUMNOSITY, RAWCOLOR, customColor)
    luminosityDragData = (luminosityDragRect, luminosityY)
    
    # hue saturation drag box, find selected color/RAWCOLOR/ hue and sat values.
    
    colorSelectorRect, ALLCOLORS = (colorSelector(26, colorSelectorX, colorSelectorY))
    rawcolorRGB = (RAWCOLOR[0], RAWCOLOR[1], RAWCOLOR[2])
    for i in range(len(ALLCOLORS)):
        if rawcolorRGB in ALLCOLORS[i]:
            COLORINDEX = (i, ALLCOLORS[i].index(rawcolorRGB))
    #Drag_box.saturationDragBox
    #Drag_box.saturationDragBox(x, y, width, colorsList, index, saturationValue):
   
    saturationX     = colorSelectorX + 166
    saturationY     = colorSelectorY
    saturationWidth = 11
    saturationDragRect = Drag_box.saturationDragBox(saturationX, saturationY, saturationWidth, ALLCOLORS, COLORINDEX[0], COLORINDEX[1])
    saturationDragData = (saturationDragRect, saturationY)
    
    #Drag_box.hueDragBox
    #Drag_box.hueDragBox(x, y, width, colorsList, index, hueValue)
    hueX     = colorSelectorX
    hueY     = colorSelectorY + 131 + 10 
    hueWidth = 11
    hueDragRect = Drag_box.hueDragBox(hueX, hueY, hueWidth, ALLCOLORS, COLORINDEX[1], COLORINDEX[0])
    hueDragData = (hueDragRect, hueX)
    customColorsRects = []
    
    # list of custom colors.
    for i in range(2):
        for j in range(9): 
            if len(Global_setter.CUSTOMCOLORS[(i)*9 + j]) < 3:
                color = (255, 255, 255)
            else:
                color = Global_setter.CUSTOMCOLORS[(i)*9 + j]
            customColorsRects.append(Utilities.colorBox(colorSelectorX + 25*j - 20, colorSelectorY + 25*i + 170, 18, color, 2))
    for i in range(18):  
        if isColorBoxPressed[i]:
            pygame.draw.rect(Global_setter.screen, (150, 200,255), (customColorsRects[i]), 3, 1)
            
    # show active color
    Utilities.colorBox(colorSelectorX - 80, colorSelectorY + 170, 50, customColor, 3)
    
    #Add to custom colors.
    addToCustomColorsRect = pygame.Rect(colorSelectorX - 20, colorSelectorY + 225, 218, 25)
    pygame.draw.rect(Global_setter.screen, (200, 200, 200), (addToCustomColorsRect), 1, 4)
    editColorsWindowData = (colorSelectorRect, luminosityDragData, saturationDragData, hueDragData, ALLCOLORS, COLORINDEX, QuitRect, colorwindowDragRect, customColorsRects, addToCustomColorsRect)
    
    # Build the system icons labeles.
    
    colorSurf = FONT.render('Color', True, (0, 0, 0), (235, 235, 235))
    colorRect = pygame.Rect(colorSelectorX - 70, colorSelectorY + 220, 10, 10)
    Global_setter.screen.blit(colorSurf, colorRect)
    
    addCustomColorSurf = FONT.render('Add to Custom Colors', True, (0, 0, 0), (235, 235, 235))
    addCustomColorRect = pygame.Rect(colorSelectorX + 30, colorSelectorY + 228, 10, 10)
    Global_setter.screen.blit(addCustomColorSurf, addCustomColorRect)
    
    iconSurf = FONT.render('Edit Colors', True, (0, 0, 0), (255, 255, 255))
    iconRect = pygame.Rect(editcolorsWinX + 10, editcolorsWinY + 5, 10, 10)
    Global_setter.screen.blit(iconSurf, iconRect)
    
    lumSurf = FONT.render('Lum:', True, (0, 0, 0), (235, 235, 235))
    lumRect = pygame.Rect(editcolorsWinX + 10, colorSelectorY, 10, 10)
    Global_setter.screen.blit(lumSurf, lumRect)
    
    lumSurf = FONT.render(str(LUMNOSITY), True, (0, 0, 0), (235, 235, 235))
    lumRect = pygame.Rect(editcolorsWinX + 45, colorSelectorY , 30, 15)
    Global_setter.screen.blit(lumSurf, lumRect)
    pygame.draw.rect(Global_setter.screen, (120, 120, 120),(editcolorsWinX + 40, colorSelectorY , 30, 15), 1)
    
    satSurf = FONT.render('Sat:', True, (0, 0, 0), (235, 235, 235))
    satRect = pygame.Rect(editcolorsWinX + 10, colorSelectorY + 30, 10, 10)
    Global_setter.screen.blit(satSurf, satRect)
    
    satSurf = FONT.render(str(COLORINDEX[0]), True, (0, 0, 0), (235, 235, 235))
    satRect = pygame.Rect(editcolorsWinX + 45, colorSelectorY + 30, 10, 10)
    Global_setter.screen.blit(satSurf, satRect)
    pygame.draw.rect(Global_setter.screen, (120, 120, 120),(editcolorsWinX + 40, colorSelectorY + 30, 30, 15), 1)
    
    hueSurf = FONT.render('Hue:', True, (0, 0, 0), (235, 235, 235))
    hueRect = pygame.Rect(editcolorsWinX + 10, colorSelectorY + 60, 10, 10)
    Global_setter.screen.blit(hueSurf, hueRect)
    
    hueSurf = FONT.render(str(COLORINDEX[1]), True, (0, 0, 0), (235, 235, 235))
    hueRect = pygame.Rect(editcolorsWinX + 45, colorSelectorY + 60, 10, 10)
    Global_setter.screen.blit(hueSurf, hueRect)
    
    pygame.draw.rect(Global_setter.screen, (120, 120, 120),(editcolorsWinX + 40, colorSelectorY + 60, 30, 15), 1)
    return editColorsWindowData

# returns the current color.
def currentColor(lumnosity, rawcolor):            
    if lumnosity < 63:
        color = (int(lumnosity*(rawcolor[0]/63)), int(lumnosity*(rawcolor[1]/63)), int(lumnosity*(rawcolor[2]/63)))
    if lumnosity > 63:
        color = ((int((((lumnosity - 63)*(255 - rawcolor[0]))/63) + rawcolor[0])), (int((((lumnosity - 63)*(255 - rawcolor[1]))/63) + rawcolor[1])), (int((((lumnosity - 63)*(255 - rawcolor[2]))/63) + rawcolor[2])))
    if lumnosity == 63:
        color = rawcolor
    return color

# creates the hue saturation list of colors in the editColorsWindow.
def columnHueSat(spanLength, place, x, y, height=128):
    listOfColors = []
    for i in range(0, spanLength):
        RGB = [(255, i*int(255/spanLength), 0), (255 - i*int(255/spanLength), 255, 0), (0, 255, i*int(255/spanLength)), (0, 255 - i*int(255/spanLength), 255), (i*int(255/spanLength), 0, 255), (255, 0, 255 - i*int(255/spanLength))]
        R = RGB[place][0]
        G = RGB[place][1]
        B = RGB[place][2]
        gfxdraw.pixel(Global_setter.screen, i + spanLength * place + x, y, (R, G, B))
        listOfColors.append([(R, G, B)])
        for j in range(0, height):
            if R > height-1:
                R = R - 1
            elif R < height-1:
                R = R + 1
            if G > height-1:
                G = G - 1
            elif G < height-1:
                G = G + 1
            if B > height-1:
                B = B - 1
            elif B < height-1:
                B = B + 1
            gfxdraw.pixel(Global_setter.screen, i + spanLength * place + x, j + y + 1, (R, G, B)) 
            listOfColors[i].append((R, G, B))
    return listOfColors
    
# draws the colorSelector in the editColorsWindow.
def colorSelector(spanLength, x, y, height=128, filletradii=0, thickness=1):
    ALLCOLORS = []
    for j in range(6):
        listOfColors = columnHueSat(spanLength, j, x, y, height)
        for i in range(len(listOfColors)):
            ALLCOLORS.append(listOfColors[i])
    if filletradii > 0:
        pygame.draw.rect(Global_setter.screen, (90, 90, 90), (x - 1, y - 1, (spanLength*6) + 2, height+3), thickness, filletradii)
    else:
        pygame.draw.rect(Global_setter.screen, (100, 100, 100), (x - 1, y - 1, (spanLength*6) + 1, height+3), thickness, filletradii)
    return (pygame.Rect(x, y, (spanLength*6) - 1, 129), ALLCOLORS)
# program_end.