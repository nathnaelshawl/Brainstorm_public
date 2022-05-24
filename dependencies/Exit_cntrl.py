# Brainstorm drawing application
# created by: @nathnael_shawl(ናትናኤል ሻውል) last edited: 11:51 PM Sunday, April 10, 2022, Addis Ababa, Ethiopia
# Exit_cntrl.py --> manages the exit or closing of the app. 
# contains terminate(), quitWindowDraw() and quitWindow() functions.
#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------

# import dependencies and modules 
import pygame
from pygame.locals import *
from . import Global_setter, Utilities, File_mngr, About_screen
import sys

# Automatically terminates the program with no prompt
def terminate():
    pygame.quit()
    sys.exit()
    
# Draws quit prompt window that asks the user what to do with the files. the function returns the data for further handeling
def quitWindowDraw(quitwindowX, quitwindowY, QuitColor=(255, 255, 255)):
        # load font file
        button_icons_dir = Global_setter.APP_PATH + '\\Icons\\button_icons\\'
        fonts_dir = Global_setter.APP_PATH + '\\fonts\\'
        
        # changes the color of the close button for the window.
        if QuitColor == (225, 0, 0):
            QuitXcolor = (240, 240, 240)
        else:
            QuitXcolor = (120, 120, 120)
       
        # Draws the rest of the quit_window.
        pygame.draw.rect(Global_setter.screen, (235, 235, 235), (quitwindowX, quitwindowY, 300, 130))
        quitwindowDragRect = pygame.Rect(quitwindowX, quitwindowY, 300, 30)
        pygame.draw.rect(Global_setter.screen, (255, 255, 255), (quitwindowDragRect))
        QuitRect = pygame.Rect(quitwindowX + 270, quitwindowY, 30, 30)
        
        FONT = pygame.font.Font(fonts_dir + 'OpenSans-Bold.ttf', 16)
        questionSurf = FONT.render('Do you want to save changes?', True, (100, 150, 200), (235, 235, 235))
        questionRect = pygame.Rect(quitwindowX + 28, quitwindowY + 45, 70, 25)
        Global_setter.screen.blit(questionSurf, questionRect)
        
        image = pygame.image.load(button_icons_dir + "quitCheck.png")
        Global_setter.screen.blit(image, (quitwindowX, quitwindowY, 30, 30))

        quitCheckButton = [quitwindowX + 60, quitwindowY + 100, 70, 25]
        quitCheckButtonNumber = 3
        for i in range(quitCheckButtonNumber):
            FONT = pygame.font.Font(fonts_dir + 'OpenSans-light.ttf', 12)
            if i == 0:
                buttonSurf = FONT.render('Save', True, (0, 0, 0), (235, 235, 235))
                buttonRect = pygame.Rect(quitCheckButton[0] + i*(quitCheckButton[2] + 20) - 10, quitCheckButton[1] - 10, quitCheckButton[2], quitCheckButton[3])
                Global_setter.screen.blit(buttonSurf, buttonRect)
            if i == 1:
                buttonSurf = FONT.render('Don\'t Save', True, (0, 0, 0), (235, 235, 235))
                buttonRect = pygame.Rect(quitCheckButton[0] + i*(quitCheckButton[2] + 20) - 27, quitCheckButton[1] - 10, quitCheckButton[2], quitCheckButton[3])
                Global_setter.screen.blit(buttonSurf, buttonRect)
            if i == 2:
                buttonSurf = FONT.render('Cancel', True, (0, 0, 0), (235, 235, 235))
                buttonRect = pygame.Rect(quitCheckButton[0] + i*(quitCheckButton[2] + 20) - 18, quitCheckButton[1] - 10, quitCheckButton[2], quitCheckButton[3])
                Global_setter.screen.blit(buttonSurf, buttonRect)
            Utilities.buttons((quitCheckButton[0] + i*(quitCheckButton[2] + 20), quitCheckButton[1], quitCheckButton[2], quitCheckButton[3]), 'idle')
        for i in range(quitCheckButtonNumber):
            Utilities.buttons((quitCheckButton[0] + i*(quitCheckButton[2] + 20), quitCheckButton[1], quitCheckButton[2], quitCheckButton[3]), 'idle')
        pygame.draw.rect(Global_setter.screen, QuitColor, (quitwindowX + 270, quitwindowY, 30, 30))
        pygame.draw.line(Global_setter.screen, QuitXcolor, (quitwindowX + 300 - 30 + 10, quitwindowY + 10), (quitwindowX + 270 + 20, quitwindowY + 20), 2)
        pygame.draw.line(Global_setter.screen, QuitXcolor, (quitwindowX + 300 - 30 + 10 + 10 , quitwindowY + 10), (quitwindowX + 270 + 20 - 10, quitwindowY + 20), 2)
        pygame.draw.rect(Global_setter.screen, (100, 100, 100), (quitwindowX, quitwindowY, 300, 130), 1)
        
        quitWindowData = [quitCheckButton, quitCheckButtonNumber, quitwindowDragRect, QuitRect]
        return quitWindowData

# quitWindow is a function used when we want the users choice when exiting or changing secisons
def quitWindow(state=''):
    mousedown = False
    quitWindowOpen = True
    quitwindowX = Global_setter.WIDTH/2 - 100
    quitwindowY = Global_setter.HEIGHT/2 - 100
    QuitColor  = (0, 0, 0)
    newscreen = Global_setter.screen.copy()
    
    # window main loop
    while quitWindowOpen:
    
        # event capture
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousedown = True
            if event.type == pygame.MOUSEBUTTONUP:
                mousedown = False
        quitWindowData = quitWindowDraw(quitwindowX, quitwindowY)
        quitCheckButton       = quitWindowData[0]
        quitCheckButtonNumber = quitWindowData[1]
        quitwindowDragRect    = quitWindowData[2]
        quitRect              = quitWindowData[3]
        if mousedown and quitwindowDragRect.collidepoint(x, y) and not quitRect.collidepoint(x, y):
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
                    quitwindowX = quitwindowX - GAPX
                elif x < x1:
                    quitwindowX = quitwindowX + GAPX
                if y > y1:
                    quitwindowY = quitwindowY - GAPY
                elif y < y1:
                    quitwindowY = quitwindowY + GAPY
                x, y = x1, y1   
                quitWindowDraw(quitwindowX, quitwindowY)
                pygame.display.update()
                Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
        quitButtonRect = []
        for i in range(quitCheckButtonNumber):
            buttonRect = Utilities.buttonRECT(quitCheckButton[0] + i*(quitCheckButton[2] + 20), quitCheckButton[1], quitCheckButton[2], quitCheckButton[3])
            quitButtonRect.append((buttonRect[0], buttonRect[1]))
        for i in range(len(quitButtonRect)):
            if quitButtonRect[i][0].collidepoint(x, y):
                Utilities.buttons((quitButtonRect[i][1]), 'pressed')
                if mousedown:
                    if i == 0:
                        Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
                        pygame.display.update()
                        if state == 'check':
                            return True
                        else:
                            if (Global_setter.SAVED[0]): 
                                File_mngr.saveImage(Global_setter.SAVED[0], Global_setter.SAVED[1])
                                terminate()
                            else:
                                filename = File_mngr.saveImage(Global_setter.SAVED[0], '')
                                if (filename != ''):
                                    terminate()
                                else:
                                    return True
                    if i == 1:
                        if state == 'check':
                            return 'dontsave'
                        else:
                            terminate()
                    if i == 2:
                        pygame.display.update()
                        Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
                        return
        if quitRect.collidepoint(x, y):
            quitWindowDraw(quitwindowX, quitwindowY, (225, 0, 0))
            if mousedown:
                pygame.display.update()
                Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
                return
        
       
        pygame.display.update()
        Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
#program_end.