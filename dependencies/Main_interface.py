# Brainstorm drawing application
# created by: @nathnael_shawl(ናትናኤል ሻውል) last edited: 12:30 AM Monday, April 11, 2022, Addis Ababa, Ethiopia
# Main_interface.py --> responsible drawing all front window user interface. 
# contains mainInterface() function.
#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------

# import dependencies and modules 
import pygame
from pygame.locals import *
from . import Global_setter
from . import Utilities
from . import Drag_box
from . import Color_mngt

# mainInterface fuction draws all the user interface components and sends the location and other datas to the buttonCommandProcess for proccesing.
def mainInterface(x, y, mousedown,changeState=True, addredoindex=False, removeredo=False, undo='none', drawing=False, save=False, saveas=False):
    button_icons_dir = Global_setter.APP_PATH + '\\Icons\\button_icons\\'
    fonts_dir = Global_setter.APP_PATH + '\\fonts\\'
    
    try:
        intermidSurf = pygame.Surface(Global_setter.drawingArea.size)
        intermidSurf.blit(Global_setter.screen.subsurface(Global_setter.drawingArea),(0,0))
        Global_setter.windowSizeSetter(intermidSurf, drawing)
    except:
        print('error')
        pass
    outLineColor = (200,200,200)
    # bottom
    bottomRECT = pygame.Rect(0, Global_setter.HEIGHT - 20, Global_setter.WIDTH, 20)
    pygame.draw.rect(Global_setter.screen, (240,240,240), (bottomRECT))
    # side
    sideRECT = pygame.Rect(0, 50, 10, Global_setter.HEIGHT - 70)
    pygame.draw.rect(Global_setter.screen, (240,240,240), (sideRECT))
    # draw top drawer
    topDrawerRECT = pygame.Rect(0, 0, Global_setter.WIDTH, 50)
    pygame.draw.rect(Global_setter.screen, (240,240,240), (topDrawerRECT))
    # tool selector.
    toolSelectorRECT = pygame.Rect(Global_setter.WIDTH - 300, 50, 300, Global_setter.HEIGHT - 70)
    pygame.draw.rect(Global_setter.screen, (240,240,240), (toolSelectorRECT))
    pygame.draw.rect(Global_setter.screen, outLineColor, (Global_setter.WIDTH - 295, 50, 36, Global_setter.HEIGHT - 70),1, 4)
    # selected tool type selector box.
    toolTypeRECT = pygame.Rect(Global_setter.WIDTH - 300 + 8 + 36 + 2, 50 + 2, 300 - 10 - 36 - 4, 24)
    pygame.draw.rect(Global_setter.screen, (200,200,200), (toolTypeRECT),1, 4)
    # drawing area
    #drawingArea = pygame.Rect(10, 50, Global_setter.WIDTH - 310, Global_setter.HEIGHT - 70)
    pygame.draw.rect(Global_setter.screen, outLineColor, (10-1, 50-1, Global_setter.WIDTH - 310+2, Global_setter.HEIGHT - 70+2), 1)
    # preference box
    if Global_setter.STATE == 'square' or Global_setter.STATE == 'rectangle' or Global_setter.STATE == 'centerrectangle' or Global_setter.STATE == 'polygon':
        pygame.draw.rect(Global_setter.screen, outLineColor, ( Global_setter.WIDTH - 254, 78, 250, 336), 0, 4)
    else:
        pygame.draw.rect(Global_setter.screen, outLineColor, ( Global_setter.WIDTH - 254, 78, 250, 300), 0, 4)
    # tools Utilities.buttons.
    # tool Utilities.buttons data toolButton = [xfirst button, yfirst button, buttonPresets.WIDTH, buttonePresets.HEIGHT]
    toolButton = [Global_setter.WIDTH - 295 + (36/2), 50 + 20/2 + 2, 32, 20]
    toolButtonNumber = 12 
    for i in range(toolButtonNumber):
        iconslist = ['pencil.png', 'filltool.png', 'eraserpaint.png', 'eyedropper.png', 'circle.png', 'line.png', 'polygon.png', 'square.png', 'rectangle.png', 'elipse.png', 'polyline.png', 'bezier.png']
        image = pygame.image.load(button_icons_dir + iconslist[i])
        image = pygame.transform.scale(image, (32, 20))
        Global_setter.screen.blit(image, (toolButton[0] - 16, toolButton[1] + i*(toolButton[3] + 2) - 10, 64, 40))
    for i in range(toolButtonNumber):
        if i == 0 and (Global_setter.STATE == 'pencil' or Global_setter.STATE == 'marker'):
            condition = 'pressed'
        elif i == 1 and Global_setter.STATE == 'fill':
            condition = 'pressed'
        elif i == 2 and Global_setter.STATE == 'eraser':
            condition = 'pressed'
        elif i == 3 and Global_setter.STATE == 'eyedroper':
            condition = 'pressed'
        elif i == 4 and Global_setter.STATE == 'circle':
            condition = 'pressed'
        elif i == 5 and Global_setter.STATE == 'line':
            condition = 'pressed'
        elif i == 6 and Global_setter.STATE == 'polygon':
            condition = 'pressed'
        elif i == 7 and Global_setter.STATE == 'square':
            condition = 'pressed'
        elif i == 8 and (Global_setter.STATE == 'rectangle' or Global_setter.STATE == 'centerrectangle'):
            condition = 'pressed'
        elif i == 9 and Global_setter.STATE == 'ellipse':
            condition = 'pressed'
        elif i == 10 and Global_setter.STATE == 'polyline':
            condition = 'pressed'
        elif i == 11 and  Global_setter.STATE == 'beziercurve':
            condition = 'pressed'
        else:
            condition = 'idle'
        Utilities.buttons((toolButton[0] , toolButton[1] + i*(toolButton[3] + 2), toolButton[2], toolButton[3]), condition)
    #toolTypeButtons.
    #tool type Utilities.buttons data topButton = [xfirst button, yfirst button, buttonPresets.WIDTH, buttonePresets.HEIGHT]
    toolTypeButton = [Global_setter.WIDTH - 295 + (59), 52 + 20/2 + 2, 32, 20]
    if Global_setter.STATE == 'pencil' or Global_setter.STATE == 'marker' or Global_setter.STATE == 'centerrectangle' or Global_setter.STATE == 'rectangle':
        toolTypeButtonNumber = 2  
    else:
        toolTypeButtonNumber = 1
    for i in range(toolTypeButtonNumber):
        if (Global_setter.STATE == 'pencil' or Global_setter.STATE == 'marker'):
            if i == 0 and Global_setter.STATE == 'pencil':
                condition = 'pressed'
                Utilities.buttons((toolTypeButton[0]  + 0*(toolTypeButton[2] + 2), toolTypeButton[1], toolTypeButton[2], toolTypeButton[3]), condition)
            elif i == 1 and Global_setter.STATE == 'marker':
                condition = 'pressed'
            else:
                condition = 'idle'
            iconslist = ['pencil.png', 'marker.png']
        elif (Global_setter.STATE == 'rectangle' or Global_setter.STATE == 'centerrectangle'):
            if i == 0 and Global_setter.STATE == 'rectangle':
                condition = 'pressed'
            elif i == 1 and Global_setter.STATE == 'centerrectangle':
                condition = 'pressed'
            else:
                condition = 'idle'
            iconslist = ['rectangle.png', 'centerrectangle.png']
        elif Global_setter.STATE == 'fill':
            condition = 'pressed'
            iconslist = ['filltool.png']
        elif Global_setter.STATE == 'eraser':
            condition = 'pressed'
            iconslist = ['eraserpaint.png']
        elif Global_setter.STATE == 'eyedroper':
            condition = 'pressed'
            iconslist = ['eyedropper.png']
        elif Global_setter.STATE == 'circle':
            condition = 'pressed'
            iconslist = ['circle.png']
        elif Global_setter.STATE == 'line':
            condition = 'pressed'
            iconslist = ['line.png']
        elif Global_setter.STATE == 'polygon':
            condition = 'pressed'
            iconslist = ['polygon.png']
        elif Global_setter.STATE == 'square':
            condition = 'pressed'
            iconslist = ['square.png']
        elif Global_setter.STATE == 'ellipse':
            condition = 'pressed'
            iconslist = ['elipse.png']
        elif Global_setter.STATE == 'polyline':
            condition = 'pressed'
            iconslist = ['polyline.png']
        elif Global_setter.STATE == 'beziercurve':
            iconslist = ['bezier.png']
            condition = 'pressed'
        
        image = pygame.image.load(button_icons_dir + iconslist[i])
        image = pygame.transform.scale(image, (32, 20))
        Global_setter.screen.blit(image, (toolTypeButton[0]  + i*(toolTypeButton[2] + 2) - 16, toolTypeButton[1] - 10, 64, 40))
        Utilities.buttons((toolTypeButton[0]  + i*(toolTypeButton[2] + 2), toolTypeButton[1], toolTypeButton[2], toolTypeButton[3]), condition)
    # top Utilities.buttons.
    # top Utilities.buttons data topButton = [xfirst button, yfirst button, buttonPresets.WIDTH, buttonePresets.HEIGHT]
    topButton = [45, 14, 70, 24]
    topButtonNumber = 3
    for i in range(topButtonNumber): 
        FONT = pygame.font.Font(fonts_dir + 'OpenSans-Light.ttf', 14)
        if i == 0:
            buttonSurf = FONT.render('File', True, (120, 120, 120), (240, 240, 240))
            buttonRect = pygame.Rect(topButton[0] + i*(topButton[2] + 2) - 10, topButton[1] - 10, topButton[2], topButton[3])
            Global_setter.screen.blit(buttonSurf, buttonRect)
        if i == 1:
            buttonSurf = FONT.render('Options', True, (120, 120, 120), (240, 240, 240))
            buttonRect = pygame.Rect(topButton[0] + i*(topButton[2] + 2) - 25, topButton[1] - 10, topButton[2], topButton[3])
            Global_setter.screen.blit(buttonSurf, buttonRect)
        if i == 2:
            buttonSurf = FONT.render('About', True, (120, 120, 120), (240, 240, 240))
            buttonRect = pygame.Rect(topButton[0] + i*(topButton[2] + 2) - 25, topButton[1] - 10, topButton[2], topButton[3])
            Global_setter.screen.blit(buttonSurf, buttonRect)
        Utilities.buttons((topButton[0] + i*(topButton[2] + 2), topButton[1], topButton[2], topButton[3]), 'idle')
   
   # other Utilities.buttons.
    # other Utilities.buttons data topButton = [xfirst button, yfirst button, buttonPresets.WIDTH, buttonePresets.HEIGHT]
    otherButton = [26, 38, 32, 20]
    otherButtonNumber = 4
    for i in range(otherButtonNumber):
        iconslist = ['save.png', 'undo.png', 'redo.png', 'clear.png']
        if Global_setter.UNDOINDEX <= 1:
            iconslist[1] = 'undoinactive.png'
        if len(Global_setter.REDO) == 0:
            iconslist[2] = 'redoinactive.png'
        image = pygame.image.load(button_icons_dir + iconslist[i])
        image = pygame.transform.scale(image, (32, 20))
        Global_setter.screen.blit(image, ((otherButton[0] + i*(otherButton[2] + 2) - 16, otherButton[1] - 10, otherButton[2], otherButton[3])) )
    for i in range(otherButtonNumber):
        Utilities.buttons((otherButton[0] + i*(otherButton[2] + 2), otherButton[1], otherButton[2], otherButton[3]), 'idle')
    
    #tool preferences box.
    # toolpreferences.
    toolPreferencesRECT = pygame.Rect(Global_setter.WIDTH - 256, 50, 254, Global_setter.HEIGHT - 70)
    pygame.draw.rect(Global_setter.screen, outLineColor, (toolPreferencesRECT), 1, 4)
 
    # color selector.
    # color preference box
    pygame.draw.rect(Global_setter.screen, (240,240,240), (Global_setter.WIDTH - 252, 80, 246, 260), 0, 4)
    pygame.draw.rect(Global_setter.screen, outLineColor, (Global_setter.WIDTH - 252, 80, 246, 260), 1, 4)
    # activeColor
    Utilities.colorBox(Global_setter.WIDTH - 240, 100, 50, Global_setter.COLOR, 3)
    FONT = pygame.font.Font(fonts_dir + 'OpenSans-Light.ttf', 12)
    colorSurf = FONT.render('Color', True, (0, 0, 0), (240, 240, 240))
    colorRect = pygame.Rect(Global_setter.WIDTH - 240 + 10, 100 + 50, 10, 10)
    Global_setter.screen.blit(colorSurf, colorRect)
    
    #Drag_box.RGBdragbox(x, y, Global_setter.WIDTH, span, gapSize)
    RGBX = Global_setter.WIDTH - 240
    RGBY = 170
    span = 200
    RGBdragboxrects = Drag_box.RGBdragbox(RGBX, RGBY, 10, span, 25)
    RGBdragboxdata = [RGBdragboxrects, RGBX, span]
    
    FONT = pygame.font.Font(fonts_dir + 'OpenSans-Light.ttf', 10)
    RSurf = FONT.render('R', True, (0, 0, 0), (240, 240, 240))
    GSurf = FONT.render('G', True, (0, 0, 0), (240, 240, 240))
    BSurf = FONT.render('B', True, (0, 0, 0), (240, 240, 240))
    RRect = pygame.Rect(RGBX - 10, RGBY - 5, 10, 10)
    GRect = pygame.Rect(RGBX - 10, RGBY - 5 + 25, 10, 10)
    BRect = pygame.Rect(RGBX - 10, RGBY - 5 + 25*2, 10, 10)
    Global_setter.screen.blit(RSurf, RRect)
    Global_setter.screen.blit(GSurf, GRect)
    Global_setter.screen.blit(BSurf, BRect)
    
    RSurf = FONT.render(str(Global_setter.COLOR[0]), True, (0, 0, 0), (240, 240, 240))
    GSurf = FONT.render(str(Global_setter.COLOR[1]), True, (0, 0, 0), (240, 240, 240))
    BSurf = FONT.render(str(Global_setter.COLOR[2]), True, (0, 0, 0), (240, 240, 240))
    RRect = pygame.Rect(RGBX + 10 + span, RGBY - 5, 10, 10)
    GRect = pygame.Rect(RGBX + 10 + span, RGBY - 5 + 25, 10, 10)
    BRect = pygame.Rect(RGBX + 10 + span, RGBY - 5 + 25*2, 10, 10)
    Global_setter.screen.blit(RSurf, RRect)
    Global_setter.screen.blit(GSurf, GRect)
    Global_setter.screen.blit(BSurf, BRect)

    # editcolors window.
    editcolorx = Global_setter.WIDTH - 185
    editcolory = 330 
    widtheditcolor = 48 + 10
    heighteditcolor = 90
    gap = 5
    Color_mngt.colorSelector(int((widtheditcolor - 2*gap)/6), editcolorx - widtheditcolor + gap, editcolory - heighteditcolor + gap, 50, 3, 2)
    editColorsRect = Utilities.buttonRECT( editcolorx, editcolory, widtheditcolor, heighteditcolor)
    Utilities.buttons((editColorsRect[0]), 'idle')
    editColorsData = (editColorsRect[0], editColorsRect[1])
    FONT = pygame.font.Font(fonts_dir + 'OpenSans-Light.ttf', 12)
    sizeSurf = FONT.render('Edit', True, (0, 0, 0), (240, 240, 240))
    sizeRect = pygame.Rect(editcolorx - widtheditcolor/2 - 10, editcolory - heighteditcolor/2 + 12, 10, 10)
    Global_setter.screen.blit(sizeSurf, sizeRect)
    sizeSurf = FONT.render('colors', True, (0, 0, 0), (240, 240, 240))
    sizeRect = pygame.Rect(editcolorx - widtheditcolor/2 - 15, editcolory - heighteditcolor/2 + 27, 10, 10)
    Global_setter.screen.blit(sizeSurf, sizeRect)
    #Drag_box.sizeDragBox
    #Drag_box.sizeDragBox(x, y, color, span, thickness, maxiumAlowedSize, size)
    maximumAllowedSize = 20
    sizex              = Global_setter.WIDTH - 210
    sizey              = 360
    span               = 160
    pygame.draw.rect(Global_setter.screen, (240,240,240), (sizex - 42, sizey - 19, 246, 35), 0, 4)
    pygame.draw.rect(Global_setter.screen, outLineColor, (sizex - 42, sizey - 19, 246, 35), 1, 4)
    sizeDragBoxRect = Drag_box.sizeDragBox(sizex, sizey, Global_setter.COLOR, span, 5, maximumAllowedSize, Global_setter.SIZE)
    sizeData = [sizeDragBoxRect, sizex, span, maximumAllowedSize]
    # size text
    FONT = pygame.font.Font(fonts_dir + 'OpenSans-Light.ttf', 12)
    sizeSurf = FONT.render('Size', True, (0, 0, 0), (240, 240, 240))
    sizeRect = pygame.Rect(sizex - 35, sizey - 10, 10, 10)
    Global_setter.screen.blit(sizeSurf, sizeRect)
    if Global_setter.STATE == 'square' or Global_setter.STATE == 'rectangle' or Global_setter.STATE == 'centerrectangle':
        #filletDragBox
        #Drag_box.sizeDragBox(x, y, color, span, thickness, maxiumAlowedSize, size)
        maximumAllowedFillet = 50
        filletx              = Global_setter.WIDTH - 210
        fillety              = 396
        span                 = 160 
        pygame.draw.rect(Global_setter.screen, (240,240,240), (filletx - 42, fillety - 19, 246, 35), 0, 4)
        pygame.draw.rect(Global_setter.screen, outLineColor, (filletx - 42, fillety - 19, 246, 35), 1, 4)
        filletDragBoxRect = Drag_box.sizeDragBox(filletx, fillety, Global_setter.COLOR, span, 5, maximumAllowedFillet, Global_setter.FILLETRADII)
        filletData = [filletDragBoxRect, filletx, span, maximumAllowedFillet]
        FONT = pygame.font.Font(fonts_dir + 'OpenSans-Light.ttf', 12)
        filletSurf = FONT.render('FilletR', True, (0, 0, 0), (240, 240, 240))
        filletRect = pygame.Rect(filletx - 35, fillety - 10, 10, 10)
        Global_setter.screen.blit(filletSurf, filletRect)
    else:
        filletData = None
    if Global_setter.STATE == 'polygon':
        #filletDragBox
        #Drag_box.sizeDragBox(x, y, color, span, thickness, maxiumAlowedSize, size)
        maximumAllowedSide = 8
        sidex              = Global_setter.WIDTH - 210
        sidey              = 396
        span               = 160 
        pygame.draw.rect(Global_setter.screen, (240,240,240), (sidex - 42, sidey - 19, 246, 35), 0, 4)
        pygame.draw.rect(Global_setter.screen, outLineColor, (sidex - 42, sidey - 19, 246, 35), 1, 4)
        sideDragBoxRect = Drag_box.sizeDragBox(sidex, sidey, Global_setter.COLOR, span, 5, maximumAllowedSide, Global_setter.NUMBEROFSIDES, True)
        sideData = [sideDragBoxRect, sidex, span, maximumAllowedSide]
        FONT = pygame.font.Font(fonts_dir + 'OpenSans-Light.ttf', 12)
        sideSurf = FONT.render('Sides', True, (0, 0, 0), (240, 240, 240))
        sideRect = pygame.Rect(sidex - 35, sidey - 10, 10, 10)
        Global_setter.screen.blit(sideSurf, sideRect)
    else:
        sideData = None
    #custom colors.
    customColorsRects = []
    for i in range(3):
        for j in range(6):
            if len(Global_setter.CUSTOMCOLORS[(i)*6 + j]) < 3:
                color = (255, 255, 255)
            else:
                color = Global_setter.CUSTOMCOLORS[(i)*6 + j]
            customColorsRects.append(Utilities.colorBox(Global_setter.WIDTH - 180 + 10 + 25*j, 250 + 25*i, 18, color, 2))
    buttonPositionData = [toolButton, toolTypeButton, topButton, otherButton]
    buttonNumberData = [toolButtonNumber, toolTypeButtonNumber, topButtonNumber, otherButtonNumber]
    if changeState:
        otherButton = Global_setter.buttonCommandProcess(x, y, mousedown , buttonPositionData, buttonNumberData, addredoindex, removeredo, RGBdragboxdata, sizeData, filletData, sideData, customColorsRects, editColorsData, drawing, undo, save, saveas)
        return otherButton
# program_end