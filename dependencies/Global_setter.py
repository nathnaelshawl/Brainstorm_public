# Brainstorm drawing application
# created by: @nathnael_shawl(ናትናኤል ሻውል) last edited:4:32 PM Monday, April 25, 2022, Addis Ababa, Ethiopia
# Global_setter.py --> responsible initializing the app and also controlling every actions as a bridge to other functions. 
# contains init() and buttonCommandProcess() functions.
#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------

# import dependencies and modules 
import pygame
from pygame.locals import *
try:
    from win32api import GetMonitorInfo, MonitorFromPoint
except:
    print('win32api missing!\nThis may affect the window, having win32api is recommended')
import pyautogui
import os, sys
from . import Utilities
from . import Main_interface
from . import Color_mngt
from . import Options_screen
from . import About_screen
from . import File_mngr
from . import Exit_cntrl
from . import Splash_screen


# initializes the interface, all global variables, sets the app path.
def init(app_path):
    global PIC_MAX_WIDTH, PIC_MAX_HEIGHT, SCR_WIDTH, SCR_HEIGHT, drawingArea, RESIZABLE_WINDOW, ORIGWINWIDTH, ORIGWINHEIGHT, APP_PATH, WHITE, BLACK, RED, BLUE, WIDTH, HEIGHT, FPS, BRUSHSIZE, BGCOLOR, running, DRAWING, STATE, CUSTOMCOLORS, SCREENLIST, SIZE, NUMBEROFSIDES, UNDOINDEX, REDO, COLOR, FILLETRADII, SAVED, EARLY_SAVE, space, screens, screen, drawingArea, undoOrRedo, undoCount, redoCount, saveCount
    
    # set app icon for the window.
    APP_PATH = app_path
    app_icons_dir = APP_PATH + '\\Icons\\app_icons\\'
    image = pygame.image.load(app_icons_dir + 'BrainstormInstallIcon.png')
    pygame.display.set_icon(image)
    
    # Monitor screen resolution
    try:
        # this would select the work area by checking the windows task bar size.
        monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
        work_area = monitor_info.get("Work")
        SCR_WIDTH = work_area[2]
        SCR_HEIGHT = work_area[3] - 23
    except:
        # this won't check the task bar size just considers the whole screen.
        SCR_WIDTH, SCR_HEIGHT = pyautogui.size()
        SCR_HEIGHT -=23
        
    # out put image maximum resolution
    PIC_MAX_WIDTH = SCR_WIDTH - 310
    PIC_MAX_HEIGHT = SCR_HEIGHT - 70
    
    # Display the splash screen
    width, height, window_type = Splash_screen.splashScreen()
    ORIGWINWIDTH = width + 310
    ORIGWINHEIGHT = height + 70

    # initialize pygame and create  window
    pygame.init()
    pygame.display.set_caption('Brainstorm')
    CLOCK = pygame.time.Clock()
    
    # define commonly used colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    
    # changing width and height value for resizable window.
    WIDTH = ORIGWINWIDTH
    HEIGHT = ORIGWINHEIGHT
    
    # FPS = 30
    # create a fixed or resizable window
    if window_type == 'fixed':
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        RESIZABLE_WINDOW = False
    if window_type == 'resizable':
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        RESIZABLE_WINDOW = True
    
    # define processes useful global static and dynamic variables.
    BRUSHSIZE = 10
    BGCOLOR = WHITE
    running = True
    DRAWING = False
    STATE = 'pencil'
    CUSTOMCOLORS = [[0]]
    CUSTOMCOLORS = CUSTOMCOLORS*18
    SCREENLIST = []
    SIZE = 1
    NUMBEROFSIDES = 1
    UNDOINDEX = 0
    REDO = []
    COLOR = BLACK
    FILLETRADII = 1
    SAVED = [False, '']
    EARLY_SAVE = SAVED[1]
    space = False
    screens = []
    drawingArea = pygame.Rect(10, 50, ORIGWINWIDTH - 310, ORIGWINHEIGHT - 70)
    mousedown = False
    undoOrRedo = 'none'
    undoCount = 0
    redoCount = 0
    saveCount = 0

# Passes tasks to other functions by accepting data from the the main_interface.
def buttonCommandProcess(x, y, mousedown , buttonPositionData, buttonNumberData, addredoindex, removeredo, rgbPickerData, sizeData, filletData, sideData, customColorsRects, editColorsData, drawing,undoOrRedo, save, saveas):
    global ORIGWINHEIGHT, ORIGWINWIDTH, EARLY_SAVE, STATE, SCREENLIST, UNDOINDEX, REDO, COLOR, SIZE, CUSTOMCOLORS, FILLETRADII, SAVED, NUMBEROFSIDES, WIDTH, HEIGHT, screen
    
    # change window caption to include the location of the file if it is saved.
    if EARLY_SAVE != SAVED[1]:
        if RESIZABLE_WINDOW:
            app_icons_dir = APP_PATH + '\\Icons\\app_icons\\'
            image = pygame.image.load(app_icons_dir + 'BrainstormInstallIcon.png')
            pygame.display.set_icon(image)
        pygame.display.set_caption(SAVED[1] + '-Brainstorm')
        EARLY_SAVE = SAVED[1]
    
    # set the directories for button icons and font files
    button_icons_dir = APP_PATH + '\\Icons\\button_icons\\'
    fonts_dir = APP_PATH + '\\fonts\\'
    
    #sizeDragBox editor.
    #sizeData = [sizeDragBoxRect, sizex, span, maximumAllowedSize]
    sizeDragBoxRect    = sizeData[0]
    sizex              = sizeData[1]
    span               = sizeData[2]
    maximumAllowedSize = sizeData[3]
    if sizeDragBoxRect.collidepoint(x, y) and mousedown:
        drag = True
        while drag:
            x1, y1 = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    drag = False
                if event.type == pygame.MOUSEBUTTONUP:
                    drag = False
                    mousedown = False
            locationOfPointer = sizex + (SIZE*(span/maximumAllowedSize))
            GAP = abs(locationOfPointer - x1)
            if x1 > sizex + (span/maximumAllowedSize) and x1 < sizex + span:
                if x1 > locationOfPointer:
                    SIZE = SIZE + round(GAP*(maximumAllowedSize/span))
                if x1 < locationOfPointer:
                    SIZE = SIZE - round(GAP*(maximumAllowedSize/span))
            Main_interface.mainInterface(x, y, False, False)
            pygame.display.update() 
    if STATE == 'square' or STATE == 'rectangle' or STATE == 'centerrectangle':        
        # filletDragBox editor.
        # filletData = [filletDragBoxRect, filletx, span, maximumAllowedFillet]
        filletDragBoxRect    = filletData[0]
        filletx              = filletData[1]
        span                 = filletData[2]
        maximumAllowedFillet = filletData[3] 
        if filletDragBoxRect.collidepoint(x, y) and mousedown:
            drag = True
            while drag:
                x1, y1 = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        drag = False
                    if event.type == pygame.MOUSEBUTTONUP:
                        drag = False 
                        mousedown = False
                locationOfPointer = filletx + (FILLETRADII*(span/maximumAllowedFillet))
                GAP = abs(locationOfPointer - x1)
                if x1 > filletx + (span/maximumAllowedFillet) and x1 < filletx + span:
                    if x1 > locationOfPointer:
                        FILLETRADII = FILLETRADII + round(GAP*(maximumAllowedFillet/span))
                    if x1 < locationOfPointer:
                        FILLETRADII = FILLETRADII - round(GAP*(maximumAllowedFillet/span))
                Main_interface.mainInterface(x, y, False, False)
                pygame.display.update() 
    if STATE == 'polygon':        
        # sideDragBox editor.
        # sideData = [sideDragBoxRect, filletx, span, maximumAllowedFillet]
        sideDragBoxRect    = sideData[0]
        sidex              = sideData[1]
        span               = sideData[2]
        maximumAllowedSide = sideData[3] 
        if sideDragBoxRect.collidepoint(x, y) and mousedown:
            drag = True
            while drag:
                x1, y1 = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        drag = False
                    if event.type == pygame.MOUSEBUTTONUP:
                        drag = False 
                        mousedown = False
                locationOfPointer = sidex + (NUMBEROFSIDES*(span/maximumAllowedSide))
                GAP = abs(locationOfPointer - x1)
                if x1 > sidex + (span/maximumAllowedSide) and x1 < sidex + span:
                    if x1 > locationOfPointer:
                        NUMBEROFSIDES = NUMBEROFSIDES + round(GAP*(maximumAllowedSide/span))
                    if x1 < locationOfPointer:
                        NUMBEROFSIDES = NUMBEROFSIDES - round(GAP*(maximumAllowedSide/span))
                Main_interface.mainInterface(x, y, False, False)
                pygame.display.update()    
    #drawingArea = pygame.Rect(10, 50, WIDTH - 310, HEIGHT - 70)
    toolRect = []
    topRect = []
    otherRect = []
    toolTypeRect = []
    #buttonPositionData = [toolButton, toolTypeButton, topButton, otherButton]
    toolButton     = buttonPositionData[0]
    toolTypeButton = buttonPositionData[1]
    topButton      = buttonPositionData[2]
    otherButton    = buttonPositionData[3]
    #buttonNumberData = [toolButtonNumber, toolTypeButtonNumber, topButtonNumber, otherButtonNumber]
    toolButtonNumber     = buttonNumberData[0]
    toolTypeButtonNumber = buttonNumberData[1]
    topButtonNumber      = buttonNumberData[2]
    otherButtonNumber    = buttonNumberData[3]
    for i in range(toolButtonNumber):
        buttonRect = Utilities.buttonRECT(toolButton[0] , toolButton[1] + i*(toolButton[3] + 2), toolButton[2], toolButton[3])
        toolRect.append((buttonRect[0], buttonRect[1]))
    for i in range(topButtonNumber):
        buttonRect = Utilities.buttonRECT(topButton[0] + i*(topButton[2] + 2), topButton[1], topButton[2], topButton[3])
        topRect.append((buttonRect[0], buttonRect[1]))
    for i in range(otherButtonNumber):
        buttonRect = Utilities.buttonRECT(otherButton[0] + i*(otherButton[2] + 2), otherButton[1], otherButton[2], otherButton[3])
        otherRect.append((buttonRect[0], buttonRect[1]))
    for i in range(toolTypeButtonNumber):
        buttonRect = Utilities.buttonRECT(toolTypeButton[0]  + i*(toolTypeButton[2] + 2), toolTypeButton[1], toolTypeButton[2], toolTypeButton[3])
        toolTypeRect.append((buttonRect[0], buttonRect[1]))
    
    # the 3 for loops below manage the clicking and also hoovering functions on buttons
    show_hoovering_text = False
    text = ''
    xpos, ypos = pygame.mouse.get_pos()
    list_of_states = ['pencil', 'fill', 'eraser', 'eyedroper', 'circle', 'line', 'polygon', 'square', 'rectangle', 'ellipse', 'polyline', 'beziercurve']
    for i in range(len(toolRect)):
        if toolRect[i][0].collidepoint(x, y) and mousedown:
            Utilities.buttons((toolRect[i][1]), 'pressed')
            STATE = list_of_states[i]
        if toolRect[i][0].collidepoint(x, y):
            Utilities.buttons((toolRect[i][1]), 'pressed')
            # creat hoovering written text 
            list_of_hoovering_text = [' Pencil', ' Fill', ' Eraser', ' Eyedroper', ' Circle', ' Line', ' Polygon', ' Square', ' Rectangle', ' Ellipse', ' Polyline', ' Beziercurve']
            if toolRect[i][0].collidepoint(x, y):
                text = list_of_hoovering_text[i]
                show_hoovering_text = True
        if show_hoovering_text:
            font = pygame.font.Font(fonts_dir + 'OpenSans-Bold.ttf', 13)
            Utilities.drawTextBox(text, font, BLACK, pygame.Rect(WIDTH - 255, ypos,len(text)*7.5, 20), 200)
            show_hoovering_text = False
    
    list_of_states.remove('pencil')
    list_of_states.remove('rectangle')
    for i in range(len(toolTypeRect)):
        if toolTypeRect[i][0].collidepoint(x, y) and mousedown:
            Utilities.buttons((toolTypeRect[i][1]), 'pressed')
            if STATE == 'pencil' or STATE == 'marker':
                if i == 0:
                    STATE = 'pencil'
                elif i == 1:
                    STATE = 'marker'
            elif (STATE == 'rectangle' or STATE == 'centerrectangle'):
                if i == 0:
                    STATE = 'rectangle'
                elif i == 1:
                    STATE = 'centerrectangle'
            elif STATE in list_of_states:
                condition = 'pressed'
                
        if toolTypeRect[i][0].collidepoint(x, y):
            Utilities.buttons((toolTypeRect[i][1]), 'pressed')  
            if STATE == 'pencil' or STATE == 'marker':
                if i == 0:
                    text = ' Pencil'
                elif i == 1:
                    text = ' Marker'
            elif (STATE == 'rectangle' or STATE == 'centerrectangle'):
                if i == 0:
                    text = ' Rectangle'
                elif i == 1:
                    text = ' Center-rectangle'
            show_hoovering_text = True
        if show_hoovering_text:
            font = pygame.font.Font(fonts_dir + 'OpenSans-Bold.ttf', 13)
            Utilities.drawTextBox(text, font, BLACK, pygame.Rect(xpos, 30, len(text)*8, 20), 170)
            show_hoovering_text = False
    
    for i in range(len(otherRect)):
        list_of_hoovering_text = [' Save', ' Undo', ' Redo', ' Clear']
        if otherRect[i][0].collidepoint(x, y):
            text = list_of_hoovering_text[i]
            show_hoovering_text = True
        if show_hoovering_text:
            font = pygame.font.Font(fonts_dir + 'OpenSans-Bold.ttf', 13)
            Utilities.drawTextBox(text, font, BLACK, pygame.Rect(xpos + 5, 5,len(text)*10, 20), 170)
            show_hoovering_text = False
    
    #filemenu handeler
    newFile = False
    openExsistingImage = False
    Exit = False
    # to halt possible window size change the 'window_freez' flag is used.
    window_freez = False
    for i in range(len(topRect)):
        if topRect[i][0].collidepoint(x, y):
            Utilities.buttons((topRect[i][1]), 'pressed')   
        if i == 0 and topRect[i][0].collidepoint(x, y) and mousedown:
            Utilities.buttons((topRect[i][1]), 'pressed')
            showMenu = True
            firstscreen = screen.copy()
            mousedown = False
            fileMenuRect = []
            fileMenuNumber = 5
            fileMenuButton = [85, 45, 140, 30]
            
            intermidSurf = pygame.Surface(drawingArea.size)
            intermidSurf.blit(screen.subsurface(drawingArea),(0,0))
            window_freez = True
            
            for k in range(fileMenuNumber):
                buttonRect = Utilities.buttonRECT(fileMenuButton[0], fileMenuButton[1]  + k*(fileMenuButton[3] + 2), fileMenuButton[2], fileMenuButton[3])
                fileMenuRect.append((buttonRect[0], buttonRect[1]))  
            pygame.draw.rect(screen, (240, 240, 240), (10, 26, 150, 158 - 24 + 32))
            pygame.draw.rect(screen, (255, 255, 255), (80, 2, 80, 24))
            pygame.draw.rect(screen, (120, 120, 120), (10, 26, 150, 158 - 24 + 32), 1)
            fileRect = pygame.Rect(10, 2, 150, 158 + 32)
            pygame.draw.rect(screen, (120, 120, 120), (fileRect), 1)
            iconslist = ['new.png', 'open.png', 'save.png', 'saveas.png', 'exit.png']
            buttonName = ['New', 'Open', 'Save', 'Save as', 'Exit']
            for j in range(fileMenuNumber):
                    image = pygame.image.load(button_icons_dir + iconslist[j])
                    image = pygame.transform.scale(image, (32, 20))
                    screen.blit(image, (fileMenuButton[0] - fileMenuButton[2]/2, fileMenuButton[1]  + j*(fileMenuButton[3] + 2) - fileMenuButton[3]/3, fileMenuButton[2], fileMenuButton[3]))
                    FONT = pygame.font.Font(fonts_dir + 'OpenSans-Light.ttf', 13)
                    colorSurf = FONT.render(buttonName[j], True, (0, 0, 0), (240, 240, 240))
                    colorRect = pygame.Rect(fileMenuButton[0] - fileMenuButton[2]/5, fileMenuButton[1]  + j*(fileMenuButton[3] + 2) - fileMenuButton[3]/3, 10, 10)
                    screen.blit(colorSurf, colorRect)
                    Utilities.buttons((fileMenuButton[0], fileMenuButton[1]  + j*(fileMenuButton[3] + 2), fileMenuButton[2], fileMenuButton[3]), 'idle')
            newscreen = screen.copy()
            pygame.display.update()
            windowSizeSetter(intermidSurf, True, window_freez)         
            while showMenu:
                x, y = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        showMenu = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mousedown = True
                    if event.type == pygame.MOUSEBUTTONUP:
                        mousedown = False
                
                for j in range(fileMenuNumber):
                    if fileMenuRect[j][0].collidepoint(x, y):
                        Utilities.buttons((fileMenuRect[j][1]), 'pressed')   
                    if mousedown and fileMenuRect[j][0].collidepoint(x, y):
                        if j == 0:
                            newFile = True
                            showMenu = False
                        if j == 1:
                            openExsistingImage = True
                            showMenu = False
                        if j == 2:
                            #screen.blit(SCREENLIST[UNDOINDEX-1] ,(0, 0, WIDTH, HEIGHT))
                            #pygame.display.update()
                            if drawing:
                                return 'save'
                            else:
                                save = True
                                showMenu = False
                        if j == 3:
                            #screen.blit(SCREENLIST[UNDOINDEX-1] ,(0, 0, WIDTH, HEIGHT))
                            #pygame.display.update()
                            if drawing:
                                return 'saveas'
                            else:
                                saveas = True
                                showMenu = False
                        if j == 4:
                            Exit = True
                            showMenu = False
                            
                if mousedown and ((not fileRect.collidepoint(x, y)) or topRect[i][0].collidepoint(x, y)):
                    showMenu = False
                pygame.display.update()
                screen.blit(newscreen, (0, 0, WIDTH, HEIGHT))
                if not showMenu:
                    screen.blit(firstscreen, (0, 0, WIDTH, HEIGHT))
                    pygame.display.update()
        # new file menu
        if newFile:
            if drawing:
                check = Exit_cntrl.quitWindow('check')
                if check == True:
                    return 'save'
                elif check=='dontsave':
                    SCREENLIST = []
                    SAVED = [False, '']
                    UNDOINDEX = 0
                    REDO = []
                    return 'newFile'
                newFile = False
            else:
                check = Exit_cntrl.quitWindow('check')
                if check == 'dontsave':
                    screen.fill(BGCOLOR ,drawingArea)
                    pygame.display.update()
                    newscreen = screen.copy()
                    SCREENLIST = []
                    SAVED = [False, '']
                    SCREENLIST.append(newscreen)
                    screen.blit(SCREENLIST[0], (0, 0, WIDTH, HEIGHT))
                    pygame.display.update()
                    UNDOINDEX = 0
                    REDO = []
                    mousedown = False
                elif check == True:
                    if not SAVED[0]:
                        SAVED[1] = File_mngr.saveImage(SAVED[0], SAVED[1])
                        if SAVED[1] != '':
                            screen.fill(BGCOLOR ,drawingArea)
                            pygame.display.update()
                            SCREENLIST = []
                            SAVED = [False, '']
                            newscreen = screen.copy()
                            SCREENLIST.append(newscreen)
                            screen.blit(SCREENLIST[0], (0, 0, WIDTH, HEIGHT))
                            UNDOINDEX = 0
                            REDO = []
                            mousedown = False
                    else:
                        File_mngr.saveImage(SAVED[0], SAVED[1]) 
                        screen.fill(BGCOLOR ,drawingArea)
                        pygame.display.update()
                        SCREENLIST = []
                        SAVED = [False, '']
                        newscreen = screen.copy()
                        SCREENLIST.append(newscreen)
                        screen.blit(SCREENLIST[0], (0, 0, WIDTH, HEIGHT))
                        UNDOINDEX = 0
                        REDO = []
                        mousedown = False
            pygame.display.update()
            return
            
        # open image
        if openExsistingImage:
            newscreen = screen.copy()
            check = Exit_cntrl.quitWindow('check')
          
            #screen.blit(SCREENLIST[UNDOINDEX-1] ,(0, 0, WIDTH, HEIGHT))
            screen.blit(newscreen ,(0, 0, WIDTH, HEIGHT))
            pygame.display.update()
            
            if check == True:
                File_mngr.saveImage(SAVED[0], SAVED[1], True)
                
            if check == True or check == 'dontsave':
                openImageFile = File_mngr.openImage()
                #screen.blit(newscreen, (0, 0, WIDTH, HEIGHT))
                #pygame.display.update()
                if openImageFile != '':
                    SCREENLIST = []
                    UNDOINDEX = 0
                    REDO = []
                    try:
                        
                        drawingSurface = screen.subsurface(drawingArea)
                        image = pygame.image.load(openImageFile)
                        
                        if (image.get_size())[0] > PIC_MAX_WIDTH:
                            image = pygame.transform.scale(image, (PIC_MAX_WIDTH, (image.get_size())[1]))
                        if (image.get_size())[1] > PIC_MAX_HEIGHT:
                            image = pygame.transform.scale(image, ((image.get_size())[0], PIC_MAX_HEIGHT))
                            
                        drawingArea[2] = (image.get_size())[0]
                        drawingArea[3] = (image.get_size())[1]
                        ORIGWINWIDTH = drawingArea[2] + 310
                        ORIGWINHEIGHT = drawingArea[3] + 70
                        WIDTH = ORIGWINWIDTH
                        HEIGHT = ORIGWINHEIGHT 
                        pygame.display.set_mode((drawingArea[2] + 310, drawingArea[3] + 70))
                        pygame.display.update()
                        
                        surf = pygame.Surface(drawingArea.size)
                        surf.fill(BGCOLOR)
                        screen.blit(surf, (drawingArea))
                        pygame.display.update()
                        
                        screen.blit(image, (drawingArea))
                        pygame.display.update()
                        newscreen = screen.copy()
                        SCREENLIST.append(newscreen)
                        SAVED[0] = True
                        SAVED[1] = openImageFile
                    except:
                        pass
            #screen.blit(newscreen, (0, 0, WIDTH, HEIGHT))
            pygame.display.update()
            return
            
        if Exit:
            check = Exit_cntrl.quitWindow('check')
            if drawing:
                if check == True and SAVED[0]:
                    File_mngr.saveImage(Global_setter.SAVED[0], Global_setter.SAVED[1])
                    Exit_cntrl.terminate()
                elif check == True and not SAVED[0]:
                    return 'save'
                elif check=='dontsave':
                    Exit_cntrl.terminate()
            else:
                if check == True and SAVED[0]:
                    File_mngr.saveImage(SAVED[0], SAVED[1])
                    Exit_cntrl.terminate()
                elif check == True and not SAVED[0]:
                    filename = File_mngr.saveImage(SAVED[0], SAVED[1])
                    if (filename != ''):
                        Exit_cntrl.terminate()
                elif check=='dontsave':
                    Exit_cntrl.terminate()

            mousedown = False
            Exit = False
            return

        # Options screen
        if i == 1 and topRect[i][0].collidepoint(x, y) and mousedown:
            intermidSurf = pygame.Surface(drawingArea.size)
            intermidSurf.blit(screen.subsurface(drawingArea),(0,0))
            window_freez = True
            windowSizeSetter(intermidSurf, True, window_freez)

            Options_screen.optionsWindow()
        # About screen   
        if i == 2 and topRect[i][0].collidepoint(x, y) and mousedown:
            intermidSurf = pygame.Surface(drawingArea.size)
            intermidSurf.blit(screen.subsurface(drawingArea),(0,0))
            window_freez = True
            windowSizeSetter(intermidSurf, True, window_freez)

            About_screen.aboutWindow()
    if window_freez:
        windowSizeSetter(intermidSurf, False)
        window_freez = False
    
    # undo redo and save Utilities.buttons.
    for i in range(len(otherRect)):
        if otherRect[i][0].collidepoint(x, y):
            Utilities.buttons((otherRect[i][1]), 'pressed')
        if otherRect[i][0].collidepoint(x, y) and mousedown:
            if not drawing:
                if i == 0:
                    if not SAVED[0]:
                        SAVED[1] = File_mngr.saveImage(SAVED[0], SAVED[1])
                        if SAVED[1] != '':
                            SAVED[0] = True
                    else:
                        File_mngr.saveImage(SAVED[0], SAVED[1])
                if i == 1 and UNDOINDEX > 1:     
                    surface = SCREENLIST[UNDOINDEX-2]
                    screen.blit(surface, (0, 0, WIDTH, HEIGHT))
                    REDO.append(SCREENLIST[UNDOINDEX-1])
                    del SCREENLIST[UNDOINDEX-1]
                    UNDOINDEX = len(SCREENLIST)
                    Main_interface.mainInterface(x, y, False)
                    pygame.display.update()
                if i == 2 and len(REDO) > 0:
                    surface = REDO[len(REDO) - 1]
                    screen.blit(surface, (0, 0, WIDTH, HEIGHT))
                    SCREENLIST.append(REDO[len(REDO) - 1])
                    UNDOINDEX = len(SCREENLIST)
                    del REDO[len(REDO) - 1]
                    Main_interface.mainInterface(x, y, False)
                    pygame.display.update()
                if i == 3:
                    screen.fill(BGCOLOR)
                    Main_interface.mainInterface(x, y, False, False)
            
            if drawing:
                if i == 0:
                    return 'save'
                if i == 1:
                    return 'undo'
                    return 'undo'
    if saveas:
        save_as_filename = SAVED[1]
        SAVED[1] = File_mngr.saveImage(False, '')
        if SAVED[1] != '':
            SAVED[0] = True
        elif SAVED[0]:
            File_mngr.saveImage(True, save_as_filename)
            SAVED[1] = save_as_filename
            SAVED[0] = True
    if save:
        if not SAVED[0]:
            SAVED[1] = File_mngr.saveImage(SAVED[0], SAVED[1])
            if SAVED[1] != '':
                SAVED[0] = True
        else:
            File_mngr.saveImage(SAVED[0], SAVED[1])          
    if undoOrRedo == 'undo' and UNDOINDEX > 1:
        surface = SCREENLIST[UNDOINDEX-2]
        screen.blit(surface, (0, 0, WIDTH, HEIGHT))
        REDO.append(SCREENLIST[UNDOINDEX-1])
        del SCREENLIST[UNDOINDEX-1]
        UNDOINDEX = len(SCREENLIST)
        Main_interface.mainInterface(x, y, False)
        pygame.display.update()
        return
    if undoOrRedo == 'redo' and len(REDO) > 0:
        surface = REDO[len(REDO) - 1]
        screen.blit(surface, (0, 0, WIDTH, HEIGHT))
        SCREENLIST.append(REDO[len(REDO) - 1])
        UNDOINDEX = len(SCREENLIST)
        del REDO[len(REDO) - 1]
        Main_interface.mainInterface(x, y, False)
        pygame.display.update()
        return
    # add to undoindex.
    if addredoindex: 
        UNDOINDEX = len(SCREENLIST)
    if removeredo:
        REDO = []
    # undolimit.
    if len(SCREENLIST) > 15:
        SCREENLIST = SCREENLIST[len(SCREENLIST) - 15:len(SCREENLIST)]
        UNDOINDEX = len(SCREENLIST)
        
    # customColors.
    for i in range(len(customColorsRects)):
        if customColorsRects[i].collidepoint(x, y) and len(CUSTOMCOLORS[i]) > 2:
            pygame.draw.rect(screen, (150, 200,255), (customColorsRects[i]), 2, 1)
            if mousedown:
                COLOR = CUSTOMCOLORS[i]
 
    # editColors editor.
    editColorsRect = editColorsData[1]
    editColorsRect = pygame.Rect(editColorsData[1][0] - editColorsData[1][2], editColorsData[1][1] - editColorsData[1][3],editColorsData[1][2], editColorsData[1][3])
    if editColorsRect.collidepoint(x, y):
        Utilities.buttons((editColorsData[0]), 'pressed')
        if mousedown:
            mousedown = False
            chooseColor = True
            editcolorsWinX = int((WIDTH/2) - 100)
            editcolorsWinY = int((HEIGHT/2) - 200)
            isColorBoxPressed = [False]
            isColorBoxPressed = isColorBoxPressed*18
            nextCustomColorsIndex = 0
            LUMNOSITY = 0
            RAWCOLOR = (127, 127, 127)
            customColor = BLACK
            newscreen = screen.copy()
            intermidSurf = pygame.Surface(drawingArea.size)
            intermidSurf.blit(screen.subsurface(drawingArea),(0,0))
            window_freez = True
            windowSizeSetter(intermidSurf, True, window_freez)
            
            while chooseColor:
                x, y = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        chooseColor = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mousedown = True
                    if event.type == pygame.MOUSEBUTTONUP:
                        mousedown = False
                editColorsWindowData = Color_mngt.editColorsWindow(RAWCOLOR, LUMNOSITY, editcolorsWinX, editcolorsWinY, isColorBoxPressed, customColor)
                #editColorsWindowData = (colorSelectorRect, luminosityDragData, saturationDragData, hueDragData, ALLCOLORS, COLORINDEX, QuitRect, colorwindowDragRect, customColorsRects, addToCustomColorsRect)
                colorSelectorRect     = editColorsWindowData[0]
                luminosityDragData    = editColorsWindowData[1]
                saturationDragData    = editColorsWindowData[2]
                hueDragData           = editColorsWindowData[3]
                colorsList            = editColorsWindowData[4]
                currentColorIndex     = editColorsWindowData[5]
                quitRect              = editColorsWindowData[6]
                colorwindowDragRect   = editColorsWindowData[7]
                customColorsRects     = editColorsWindowData[8]
                addToCustomColorsRect = editColorsWindowData[9]
                if mousedown and colorwindowDragRect.collidepoint(x, y) and not quitRect.collidepoint(x, y):
                    drag = True 
                    x1, y1 = x, y
                    while drag:
                        x1, y1 = pygame.mouse.get_pos()
                        GAPX = abs(x - x1)
                        GAPY = abs(y - y1)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                drag = False
                            if event.type == pygame.MOUSEBUTTONUP:
                                drag = False
                                mousedown = False
                        if x > x1:
                            editcolorsWinX = editcolorsWinX - GAPX
                        elif x < x1:
                            editcolorsWinX = editcolorsWinX + GAPX
                        if y > y1:
                            editcolorsWinY = editcolorsWinY - GAPY
                        elif y < y1:
                            editcolorsWinY = editcolorsWinY + GAPY
                        x, y = x1, y1   
                        Color_mngt.editColorsWindow(RAWCOLOR, LUMNOSITY, editcolorsWinX, editcolorsWinY, isColorBoxPressed, customColor)
                        pygame.display.update()
                        screen.blit(newscreen, (0, 0, WIDTH, HEIGHT))
                if quitRect.collidepoint(x, y):
                    if mousedown:
                        chooseColor = False
                        mousedown = False
                    quitColor = (225, 0, 0)
                    Color_mngt.editColorsWindow(RAWCOLOR, LUMNOSITY, editcolorsWinX, editcolorsWinY, isColorBoxPressed, customColor,quitColor)
                else:
                    Color_mngt.editColorsWindow(RAWCOLOR, LUMNOSITY, editcolorsWinX, editcolorsWinY, isColorBoxPressed, customColor)
                for i in range(18):  
                    if customColorsRects[i].collidepoint(x, y):
                        pygame.draw.rect(screen, (150, 200,255), (customColorsRects[i]), 2, 1)
                        if mousedown:
                            if True in isColorBoxPressed:
                                isColorBoxPressed[isColorBoxPressed.index(True)] = False
                            isColorBoxPressed[i] = True
                if addToCustomColorsRect.collidepoint(x, y):
                    pygame.draw.rect(screen, (150, 200,255), (addToCustomColorsRect), 1, 4)
                    if mousedown:
                        if True in isColorBoxPressed:
                            CUSTOMCOLORS[isColorBoxPressed.index(True)] = customColor
                            nextCustomColorsIndex = isColorBoxPressed.index(True) + 1
                            isColorBoxPressed[isColorBoxPressed.index(True)] = False
                        elif [0] in CUSTOMCOLORS:
                            CUSTOMCOLORS[CUSTOMCOLORS.index([0])] = customColor
                        else:
                            CUSTOMCOLORS[nextCustomColorsIndex] = customColor
                            nextCustomColorsIndex = nextCustomColorsIndex + 1
                            if nextCustomColorsIndex > 17:
                                nextCustomColorsIndex = 0
                        mousedown = False

                # color changing.
                #if False:
                if colorSelectorRect.collidepoint(x, y) and mousedown:
                    drag = True
                    while drag:
                        x1, y1 = pygame.mouse.get_pos()
                        if colorSelectorRect.collidepoint(x1, y1):
                            RAWCOLOR = screen.get_at((x1, y1))
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                drag = False
                            if event.type == pygame.MOUSEBUTTONUP:
                                drag = False
                                mousedown = False
                        customColor = Color_mngt.currentColor(LUMNOSITY, RAWCOLOR)
                        Color_mngt.editColorsWindow(RAWCOLOR, LUMNOSITY, editcolorsWinX, editcolorsWinY, isColorBoxPressed, customColor)
                        pygame.display.update()

                # lumnosity control 
                #if False:
                if luminosityDragData[0].collidepoint(x, y):
                    if mousedown:
                        drag = True
                        while drag:
                            x1, y1 = pygame.mouse.get_pos()
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    drag = False
                                if event.type == pygame.MOUSEBUTTONUP:
                                    drag = False
                                    mousedown = False
                            locationOfPointer = luminosityDragData[1] + 128 - LUMNOSITY
                            if y1 > luminosityDragData[1] + 1 and y1 < luminosityDragData[1] + 128 + 1:
                                if y1 > locationOfPointer:
                                    GAP = y1 - locationOfPointer
                                    LUMNOSITY = LUMNOSITY - GAP
                                if y1 < locationOfPointer:
                                    GAP = locationOfPointer - y1
                                    LUMNOSITY = LUMNOSITY + GAP

                            customColor = Color_mngt.currentColor(LUMNOSITY, RAWCOLOR) 
                            Color_mngt.editColorsWindow(RAWCOLOR, LUMNOSITY, editcolorsWinX, editcolorsWinY, isColorBoxPressed, customColor)
                            pygame.display.update()
 
                #hue control.
                #if False:
                if hueDragData[0].collidepoint(x, y) and mousedown:
                    drag = True
                    while drag:
                        x1, y1 = pygame.mouse.get_pos()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                drag = False
                            if event.type == pygame.MOUSEBUTTONUP:
                                drag = False
                                mousedown = False
                        locationOfPointer =  hueDragData[1] + currentColorIndex[0]
                        if x1 > hueDragData[1] - 1 and x1 < hueDragData[1] + 155:
                            GAP = abs(locationOfPointer - x1)
                            if x1 < locationOfPointer:
                                RAWCOLOR = colorsList[currentColorIndex[0] - GAP][currentColorIndex[1]]
                            if x1 > locationOfPointer:
                                RAWCOLOR = colorsList[currentColorIndex[0] + GAP][currentColorIndex[1]]
                        RAWCOLORRGB = RAWCOLOR
                        for i in range(len(colorsList)):
                            if RAWCOLORRGB in colorsList[i]:
                                currentColorIndex = (i, colorsList[i].index(RAWCOLORRGB))
                        
                        customColor = Color_mngt.currentColor(LUMNOSITY, RAWCOLOR)   
                        Color_mngt.editColorsWindow(RAWCOLOR, LUMNOSITY, editcolorsWinX, editcolorsWinY, isColorBoxPressed, customColor)
                        pygame.display.update()

                # saturation control
                #if False:
                if saturationDragData[0].collidepoint(x, y) and mousedown:
                    drag = True
                    while drag:
                        x1, y1 = pygame.mouse.get_pos()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                drag = False
                            if event.type == pygame.MOUSEBUTTONUP:
                                drag = False
                                mousedown = False
                        saturationValue = 128  - currentColorIndex[1]
                        locationOfPointer =  saturationDragData[1] + currentColorIndex[1]
                        if y1 > saturationDragData[1] and y1 < saturationDragData[1] + 128:
                            GAP = abs(locationOfPointer - y1)
                            if y1 < locationOfPointer:
                                RAWCOLOR = colorsList[currentColorIndex[0]][currentColorIndex[1] - GAP]
                            if y1 > locationOfPointer:
                                RAWCOLOR = colorsList[currentColorIndex[0]][currentColorIndex[1] + GAP]
                        RAWCOLORRGB = RAWCOLOR
                        for i in range(len(colorsList)):
                            if RAWCOLORRGB in colorsList[i]:
                                currentColorIndex = (i, colorsList[i].index(RAWCOLORRGB))
                        customColor = Color_mngt.currentColor(LUMNOSITY, RAWCOLOR)   
                        Color_mngt.editColorsWindow(RAWCOLOR, LUMNOSITY, editcolorsWinX, editcolorsWinY, isColorBoxPressed, customColor)
                        pygame.display.update()
                
                pygame.display.update()
                screen.blit(newscreen, (0, 0, WIDTH, HEIGHT)) 
    if window_freez:
        intermidSurf = pygame.Surface(drawingArea.size)
        intermidSurf.blit(screen.subsurface(drawingArea),(0,0))
        windowSizeSetter(intermidSurf, False)
        window_freez = False
        
    #RGB dragbox editor:
    #RGBdragboxdata = [RGBdragboxrects, RGBX, span]
    REDdragRect   = rgbPickerData[0][0]
    GREENdragRect = rgbPickerData[0][1]
    BLUEdragRect  = rgbPickerData[0][2]
    RGBX          = rgbPickerData[1]
    span          = rgbPickerData[2]
    if REDdragRect.collidepoint(x, y) and mousedown:
        drag = True
        while drag:
            x1, y1 = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    drag = False
                if event.type == pygame.MOUSEBUTTONUP:
                    drag = False
            locationOfPointer = RGBX + COLOR[0]*(span/255)
            GAP = abs(locationOfPointer - x1)
            if x1 > RGBX - 1 and x1 < RGBX + span + 1:
                if x1 > locationOfPointer:
                    COLOR = (COLOR[0] + round(GAP*(255/span)), COLOR[1], COLOR[2])
                if x1 < locationOfPointer:
                    COLOR = (COLOR[0] - round(GAP*(255/span)), COLOR[1], COLOR[2])
            Main_interface.mainInterface(x, y, False, False)
            pygame.display.update()  
    if GREENdragRect.collidepoint(x, y) and mousedown:
        drag = True
        while drag:
            x1, y1 = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    drag = False
                if event.type == pygame.MOUSEBUTTONUP:
                    drag = False
            locationOfPointer = RGBX + COLOR[1]*(span/255)
            GAP = abs(locationOfPointer - x1)
            if x1 > RGBX - 1 and x1 < RGBX + span + 1:
                if x1 > locationOfPointer:
                    COLOR = (COLOR[0], COLOR[1] + round(GAP*(255/span)), COLOR[2])
                if x1 < locationOfPointer:
                    COLOR = (COLOR[0], COLOR[1] - round(GAP*(255/span)), COLOR[2])
            Main_interface.mainInterface(x, y, False, False)
            pygame.display.update()  
    if BLUEdragRect.collidepoint(x, y) and mousedown:
        drag = True
        while drag:
            x1, y1 = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    drag = False
                if event.type == pygame.MOUSEBUTTONUP:
                    drag = False
            locationOfPointer = RGBX + COLOR[2]*(span/255)
            GAP = abs(locationOfPointer - x1)
            if x1 > RGBX - 1 and x1 < RGBX + span + 1:
                if x1 > locationOfPointer:
                    COLOR = (COLOR[0], COLOR[1], COLOR[2] + round(GAP*(255/span)))
                if x1 < locationOfPointer:
                    COLOR = (COLOR[0], COLOR[1], COLOR[2] - round(GAP*(255/span)))
            Main_interface.mainInterface(x, y, False, False)
            pygame.display.update()

# it controls the window when the selected window type is resizable.
def windowSizeSetter(surf, in_process=False, window_freeze=False):
    if not RESIZABLE_WINDOW:
        return
    global screen, HEIGHT, WIDTH
    if window_freeze:
        pygame.display.set_mode((WIDTH, HEIGHT))
        return
    if not in_process:
        WIDTH, HEIGHT = pygame.display.get_surface().get_size()
        if WIDTH < ORIGWINWIDTH or  HEIGHT < ORIGWINHEIGHT:
            pygame.display.set_mode((ORIGWINWIDTH, ORIGWINHEIGHT), pygame.RESIZABLE)
            WIDTH, HEIGHT = ORIGWINWIDTH, ORIGWINHEIGHT
        else:
            pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        screen.fill((180, 230, 255))
        pygame.draw.rect(screen, (170, 220, 255), pygame.Rect(drawingArea.left, drawingArea.top, drawingArea.width + 5, drawingArea.height + 5))
        screen.blit(surf, drawingArea)
    else:
        pygame.display.set_mode((WIDTH, HEIGHT))
        screen.fill((180, 230, 255))
        pygame.draw.rect(screen, (170, 220, 255), pygame.Rect(drawingArea.left, drawingArea.top, drawingArea.width + 5, drawingArea.height + 5))
        screen.blit(surf, drawingArea)
    return
#program_end.