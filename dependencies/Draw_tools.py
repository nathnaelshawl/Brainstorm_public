# Brainstorm drawing application
# created by: @nathnael_shawl(ናትናኤል ሻውል) last edited:11:56 PM Monday, April 25, 2022, 2022, Addis Ababa, Ethiopia
# Draw_tools --> responsible for drawing and editing shapes on the screen.
# contains KeyPressed(), CenterSquareRect(), buttonRECT(), buttons(), colorBox() and drawTextBox()
# ---------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------
import pygame
from pygame.locals import *
from pygame import gfxdraw
import numpy as np
from scipy import interpolate
import math
import copy
from . import Global_setter
from . import Utilities
from . import Main_interface
from . import Exit_cntrl

# draw pencil tool
def pencil(x, y, brushType, width, color, antialise=True):
    draw = True
    count = 0
    mousedown = False
    newscreen = Global_setter.screen.copy()
    # drawing main loop
    while draw:
        # event capture
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                Global_setter.screen.blit(newscreen, (0, 0, Global_setter.HEIGHT, Global_setter.WIDTH))
                return
            if event.type == pygame.MOUSEBUTTONUP:
                draw = False
        if count == 0:
            x1, y1 = x, y
            count = 1
        elif count == 1:
            pointConnect(x, y, x1, y1, brushType, width, color, antialise)
            x1, y1 = x, y
        pygame.display.update(Global_setter.drawingArea)
    newscreen = Global_setter.screen.copy()
    Global_setter.SCREENLIST.append(newscreen)
    Main_interface.mainInterface(x, y, False, True, True, True)
    
# edit circle drawing.
def circleEdit(released, radius, color, width, x, y):
    fonts_dir = Global_setter.APP_PATH + '\\fonts\\'
    font = pygame.font.Font(fonts_dir + 'OpenSans-Bold.ttf', 13)
    if released:
        center = [x, y]
        newCenter = [x, y]
        mousedown = False
        move = False
        newscreen = Global_setter.screen.copy()
        boxMove = False
        escape = False
        edit = True
        undoCount = 0
        undo = False
        save = False
        saveas = False
        saveCount = 0
        # drawing main loop
        while edit:
            # event capture
            x1, y1 = pygame.mouse.get_pos()
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT:
                    save = Exit_cntrl.quitWindow()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if Global_setter.drawingArea.collidepoint(x1, y1):
                        boxMove = True
                    mousedown = True
                if event.type == pygame.MOUSEBUTTONUP:
                    mousedown = False
                    boxMove = False
                if keys[pygame.K_ESCAPE]:
                    escape = True
            zPressed = Utilities.keyPressed(pygame.K_z)
            leftControl = Utilities.keyPressed(pygame.K_LCTRL)
            sPressed = Utilities.keyPressed(pygame.K_s)
            if leftControl and not zPressed:
                undoCount = 1
            elif not leftControl and zPressed:
                undoCount = 0
            if undoCount == 1 and zPressed:
                undo = True  

            if leftControl and not sPressed:
                saveCount = 1
            elif not leftControl and sPressed:
                saveCount = 0
            if saveCount == 1 and sPressed:
                save = True
            # movePoints
            movepoints = [[newCenter[0], newCenter[1] - radius], [newCenter[0] + radius, newCenter[1]], [newCenter[0], newCenter[1] + radius], [newCenter[0] - radius, newCenter[1]]] 
            pygame.draw.circle(Global_setter.screen, Global_setter.COLOR, (newCenter[0], newCenter[1]), radius, Global_setter.SIZE)
            moveBoxRect = pygame.Rect(newCenter[0] - radius, newCenter[1] - radius, 2*radius, 2*radius)
            pygame.draw.rect(Global_setter.screen, Global_setter.BLUE, moveBoxRect, 1)
            moveRectCheck = []
            for i in range(len(movepoints)):
                moverect = Utilities.CenterSquareRect(movepoints[i][0], movepoints[i][1], 15)
                moveRectCheck.append(moverect.collidepoint(x1, y1))
                if moverect.collidepoint(x1, y1) and Global_setter.drawingArea.collidepoint(x1, y1):
                    pygame.draw.rect(Global_setter.screen, Global_setter.BLUE, (moverect), 2)
                    move = True
                    j = i
                if not mousedown:
                    move = False
                if move and mousedown:
                    if j == 1 or j == 3:
                        radius = int(math.sqrt((newCenter[0] - x1)**2))
                    if j == 0 or j == 2:
                        radius = int(math.sqrt((newCenter[1] - y1)**2))
                    # display the value of the radius
                    Utilities.drawTextBox((' ' + 'r-' + str(radius) + ' '), font, Global_setter.BLACK, pygame.Rect(x1 + 15, y1,len(' ' + 'r-' + str(radius) + ' ')*7, 20), 150)
                # circle editing rects
                innerPointColor = Global_setter.WHITE
                outerPointColor = Global_setter.BLACK
                innerRECT = Utilities.CenterSquareRect(movepoints[i][0], movepoints[i][1], 4)
                outerRECT = Utilities.CenterSquareRect(movepoints[i][0], movepoints[i][1], 6)
                pygame.draw.rect(Global_setter.screen, innerPointColor, (innerRECT),0)
                pygame.draw.rect(Global_setter.screen, outerPointColor, (outerRECT),1)
                
                if radius < 5:
                    radius = 5
            x5 = newCenter[0] - 7.5
            y5 = newCenter[1] - 7.5
            length = 15
            centerRect = pygame.Rect(x5, y5,length, length)
            # check if cursor is over around the center of the circle.
            if centerRect.collidepoint(x1, y1):
                # Draw center line.
                pygame.draw.line(Global_setter.screen, Global_setter.BLUE, (newCenter[0] + 5, newCenter[1]), (newCenter[0] - 5, newCenter[1]), 1)
                pygame.draw.line(Global_setter.screen, Global_setter.BLUE, (newCenter[0], newCenter[1] + 5), (newCenter[0], newCenter[1] - 5), 1)  
            # box move(change the center point location of the circle by click and drag or click only)
            if mousedown and 1 not in moveRectCheck and not move and moveBoxRect.collidepoint(x1, y1) and boxMove:
                # display the coordinate of the circle center point.
                Utilities.drawTextBox((' ' + str(x1-10) + ', ' + str(y1-50)), font, Global_setter.BLACK, pygame.Rect(x1 + 15, y1,len(' ' + str(x1-10) + ', ' + str(y1-50))*7, 20), 150)
                if center[0] > x1:
                    newCenter[0] = center[0] - (center[0] - x1)
                if center[0] < x1:
                    newCenter[0] = center[0] + (x1 - center[0])
                if center[1] > y1:
                    newCenter[1] = center[1] - (center[1] - y1)
                if center[1] < y1:
                    newCenter[1] = center[1] + (y1 - center[1])
                Main_interface.mainInterface(x1, y1, mousedown, False, False)
            else:
                if Global_setter.drawingArea.collidepoint(x1, y1):
                    Main_interface.mainInterface(x1, y1, False)
                else:
                    otherButton = Main_interface.mainInterface(x1, y1, mousedown, True, False, False, False, True)
                    if otherButton == 'undo':
                        undo = True
                    if otherButton == 'save':
                        save = True
                    if otherButton == 'saveas':
                        saveas = True
                    if otherButton == 'newFile':
                        return 'newFile'
                    mousedown = False
            # check for exit.
            pygame.display.update()
            Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
            if save or saveas:
                Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
                pygame.draw.circle(Global_setter.screen, Global_setter.COLOR, (newCenter[0], newCenter[1]), radius, Global_setter.SIZE)
                pygame.display.update()
                Main_interface.mainInterface(x1, y1, mousedown, True, False, False, False, True, save, saveas)
                newscreen = Global_setter.screen.copy()
                Global_setter.SCREENLIST.append(newscreen)
                edit = False
            if escape:
                edit = False
            if undo:
                edit = False
                pygame.time.wait(200) 
            if (Global_setter.drawingArea.collidepoint(x1, y1) and not moveBoxRect.collidepoint(x1, y1) and mousedown and 1 not in moveRectCheck and not move) or Global_setter.STATE != 'circle':
                Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
                pygame.draw.circle(Global_setter.screen, Global_setter.COLOR, (newCenter[0], newCenter[1]), radius, Global_setter.SIZE)
                Main_interface.mainInterface(x, y, False, False)
                pygame.display.update()
                newscreen = Global_setter.screen.copy()
                Global_setter.SCREENLIST.append(newscreen)
                edit = False           

# draw arc to show the value of the angle using arc and text.
def polyAngleDraw(x1, y1, polylist, lastIndex):
    try:
        # calculate the input angle.
        hypLength = math.sqrt((x1 - polylist[lastIndex][0])**2 + (y1 - polylist[lastIndex][1])**2)
        if hypLength < 30:
            length = hypLength
        else:
            length = 30
        if (y1 <= polylist[lastIndex][1] and x1 >= polylist[lastIndex][0]) or  (y1 >= polylist[lastIndex][1] and x1 >= polylist[lastIndex][0]):
            endAngle = math.asin((polylist[lastIndex][1] - y1)/hypLength)
        if (y1 <= polylist[lastIndex][1] and x1 <= polylist[lastIndex][0]) or (y1 >= polylist[lastIndex][1] and x1 <= polylist[lastIndex][0]):
            endAngle = math.pi - math.asin((polylist[lastIndex][1] - y1)/hypLength)
        
        if endAngle < 0:
            previewAngle = 360 + endAngle*180/math.pi
        else:
            previewAngle = endAngle*180/math.pi
        
        # display the value of the angle.
        fonts_dir = Global_setter.APP_PATH + '\\fonts\\' 
        font = pygame.font.Font(fonts_dir + 'OpenSans-Bold.ttf', 13)
        if x1 > Global_setter.drawingArea.topright[0] - 50:
            x_pos = Global_setter.drawingArea.topright[0] - 70
        else:
            x_pos = x1 + 15
        if y1 <  Global_setter.drawingArea.topright[1]:
            y_pos = Global_setter.drawingArea.topright[1]
        elif y1 >  Global_setter.drawingArea.bottomright[1] - 20:
            y_pos = Global_setter.drawingArea.bottomright[1] - 20
        else:
            y_pos = y1
        Utilities.drawTextBox('  ' + str(round(previewAngle, 2)) + '\N{DEGREE SIGN}', font, Global_setter.BLACK, pygame.Rect(x_pos, y_pos,len('  ' + str(round(previewAngle, 2))+ '\N{DEGREE SIGN}')*6, 20), 150)
        
        # draw specific types for selected specific angles.
        if previewAngle == 180:
            pygame.draw.arc(Global_setter.screen, RED, (polylist[lastIndex][0] - length, polylist[lastIndex][1] - length, 2*length, 2*length), 0, endAngle, 1)
        elif previewAngle == 90:
            pygame.draw.line(Global_setter.screen, Global_setter.BLUE, (polylist[lastIndex][0] + length, polylist[lastIndex][1]), (polylist[lastIndex][0] + length , polylist[lastIndex][1] - length), 1)
            pygame.draw.line(Global_setter.screen, Global_setter.BLUE, (polylist[lastIndex][0], polylist[lastIndex][1] - length), (polylist[lastIndex][0] + length , polylist[lastIndex][1] - length), 1)
        elif previewAngle == 270:
            pygame.draw.line(Global_setter.screen, Global_setter.BLUE, (polylist[lastIndex][0] + length, polylist[lastIndex][1]), (polylist[lastIndex][0] + length , polylist[lastIndex][1] + length), 1)
            pygame.draw.line(Global_setter.screen, Global_setter.BLUE, (polylist[lastIndex][0], polylist[lastIndex][1] + length), (polylist[lastIndex][0] + length , polylist[lastIndex][1] + length), 1)
        else:
            pygame.draw.arc(Global_setter.screen, Global_setter.BLUE, (polylist[lastIndex][0] - length, polylist[lastIndex][1] - length, 2*length, 2*length), 0, endAngle, 1)
        pygame.draw.line(Global_setter.screen, Global_setter.BLUE, (polylist[lastIndex][0], polylist[lastIndex][1]), (polylist[lastIndex][0] + length*2, polylist[lastIndex][1]), 1)
    except:
        pass

# shows the length of the line
def polyLengthDraw(starting_point, end_point):
    x0 = starting_point[0]
    y0 = starting_point[1]
    x1 = end_point[0]
    y1 = end_point[1]
    line_length = math.sqrt((x0-x1)**2 + (y0-y1)**2)
    # display the value of the angle.
    fonts_dir = Global_setter.APP_PATH + '\\fonts\\' 
    font = pygame.font.Font(fonts_dir + 'OpenSans-Bold.ttf', 13)
    if x1 > Global_setter.drawingArea.topright[0] - 50:
        x_pos = Global_setter.drawingArea.topright[0] - 70
    else:
        x_pos = x1 + 15
    if y1 <  Global_setter.drawingArea.topright[1]:
        y_pos = Global_setter.drawingArea.topright[1]
    elif y1 >  Global_setter.drawingArea.bottomright[1] - 20:
        y_pos = Global_setter.drawingArea.bottomright[1] - 20
    else:
        y_pos = y1
    Utilities.drawTextBox('  ' + 'len-' + str(round(line_length, 2)), font, Global_setter.BLACK, pygame.Rect(x_pos, y_pos,len('  ' + 'len-' + str(round(line_length, 2)))*6, 20), 200)

# connects two points using linear interpolation(line equation)         
def pointConnect(x, y, x1, y1, brushType, BRUSHSIZE, color, antialise=True):
    # differentiate the line type for pencil and marker options
    BRUSHSIZE = int(BRUSHSIZE/2)
    if brushType == 'circular':
        gfxdraw.filled_circle(Global_setter.screen, x, y, BRUSHSIZE, color)
        if antialise:
            gfxdraw.aacircle(Global_setter.screen, x, y, BRUSHSIZE, color)
    if brushType == 'line':
        pygame.draw.line(Global_setter.screen, color, (x + BRUSHSIZE/2, y - BRUSHSIZE/2), (x - BRUSHSIZE/2, y + BRUSHSIZE/2), 2)

    
    vertical = False
    xm = abs(x-x1)
    ym = abs(y-y1)
    listx = [x, x1]
    listy = [y, y1]
    listx.sort(), listy.sort()
    xa = listx[0]
    ya = listy[0]
    xb = listx[1]
    yb = listy[1]
    # identify the line types and connect the points with more points and draw based on the brush type.
    try:
        slope = ((y - y1) / (x - x1))
    except:
        vertical = True
    if x == x1 and y1 == y:
        skip = True
    elif vertical: 
        yn = yb - ya
        for i in range (0, yn):
            if brushType == 'circular':
                gfxdraw.filled_circle(Global_setter.screen, xa, ya + i, BRUSHSIZE, color)
                if antialise:
                    gfxdraw.aacircle(Global_setter.screen, xa, ya + i, BRUSHSIZE, color)
            if brushType == 'line':
                pygame.draw.line(Global_setter.screen, color, (xa + BRUSHSIZE/2, ya + i - BRUSHSIZE/2), (xa - BRUSHSIZE/2, ya + i + BRUSHSIZE/2), 2)
            
    elif y == y1:
        xn = xb - xa
        for i in range (0, xn):
            if brushType == 'circular':
                gfxdraw.filled_circle(Global_setter.screen, xa + i, ya, BRUSHSIZE, color)
                if antialise:
                    gfxdraw.aacircle(Global_setter.screen, xa + i, ya, BRUSHSIZE, color)
            if brushType == 'line':
                pygame.draw.line(Global_setter.screen, color, (xa + i + BRUSHSIZE/2, ya - BRUSHSIZE/2), (xa + i - BRUSHSIZE/2, ya + BRUSHSIZE/2), 2)
            
    elif abs(slope) < 1:
        for i in range(1, xm):
            yn = slope*(i + xa - x1) + y1
            if brushType == 'circular':
                gfxdraw.filled_circle(Global_setter.screen, int(i + xa), int(yn), BRUSHSIZE, color)
                if antialise:
                    gfxdraw.aacircle(Global_setter.screen, int(i + xa), int(yn), BRUSHSIZE, color)
            if brushType == 'line':
                pygame.draw.line(Global_setter.screen, color, (int(i + xa) + BRUSHSIZE/2, int(yn) - BRUSHSIZE/2), (int(i + xa) - BRUSHSIZE/2, int(yn) + BRUSHSIZE/2), 2)
            
    else:  
        for i in range(1, ym):
            xn = ((i + ya - y1)/slope) + x1
            if brushType == 'circular':
                gfxdraw.filled_circle(Global_setter.screen, int(xn), int(i + ya), BRUSHSIZE, color)
                if antialise:
                    gfxdraw.aacircle(Global_setter.screen, int(xn), int(i + ya), BRUSHSIZE, color)
            if brushType == 'line':
                pygame.draw.line(Global_setter.screen, color, (int(xn) + BRUSHSIZE/2, int(i + ya) - BRUSHSIZE/2), (int(xn) - BRUSHSIZE/2, int(i + ya) + BRUSHSIZE/2), 2)

# manages editing shapes that rely on rectangle bounding box (rectangle, square and ellipse)
def rectEdit(released, RECT, shape, width, color, filletradii=1):
    fonts_dir = Global_setter.APP_PATH + '\\fonts\\'
    font = pygame.font.Font(fonts_dir + 'OpenSans-Bold.ttf', 13)
    if released:
        movepoints = []
        mousedown = False
        newscreen = Global_setter.screen.copy()
        stateChange = False
        edit = True
        toolButtonPressed = False
        escape = False
        mousedownINTERFACE = False
        undoCount = 0
        undo = False
        save = False
        saveas = False
        saveCount = 0
        while edit:
            # event capture.
            x3, y3 = pygame.mouse.get_pos()
            width = Global_setter.SIZE
            if abs(RECT.topleft[0] - RECT.topright[0]) < 2*Global_setter.SIZE:
               RECT.width += 2*Global_setter.SIZE - abs(RECT.topleft[0] - RECT.topright[0])
            elif abs(RECT.topleft[1] - RECT.bottomleft[1]) < 2*Global_setter.SIZE:
               RECT.height += 2*Global_setter.SIZE - abs(RECT.topleft[1] - RECT.bottomleft[1])
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT:
                    save = Exit_cntrl.quitWindow()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if Global_setter.drawingArea.collidepoint(x3, y3):
                        boxMove = True
                    else:
                        mousedownINTERFACE = True
                    mousedown = True
                if event.type == pygame.MOUSEBUTTONUP:
                    mousedown = False 
                    boxMove = False
                    mousedownINTERFACE = False
                if keys[pygame.K_ESCAPE]:
                    escape = True
            zPressed = Utilities.keyPressed(pygame.K_z)
            leftControl = Utilities.keyPressed(pygame.K_LCTRL)
            sPressed = Utilities.keyPressed(pygame.K_s)
            if leftControl and not zPressed:
                undoCount = 1
            elif not leftControl and zPressed:
                undoCount = 0
            if undoCount == 1 and zPressed:
                undo = True 
                
            if leftControl and not sPressed:
                saveCount = 1
            elif not leftControl and sPressed:
                saveCount = 0
            if saveCount == 1 and sPressed:
                save = True 
            if len(movepoints) >= 0:
                movepoints = []
                movepoints.append(RECT.topleft)
                movepoints.append(RECT.topright)
                movepoints.append(RECT.bottomright)
                movepoints.append(RECT.bottomleft)
                movepoints.append(((RECT.topleft[0] + RECT.topright[0])/2, RECT.topleft[1]))
                movepoints.append((RECT.topright[0], (RECT.topleft[1] + RECT.bottomright[1])/2))
                movepoints.append(((RECT.bottomright[0] + RECT.bottomleft[0])/2, RECT.bottomright[1]))
                movepoints.append((RECT.bottomleft[0], (RECT.bottomleft[1] + RECT.topleft[1])/2))
            if shape == 'ellipse':
                pygame.draw.ellipse(Global_setter.screen, Global_setter.COLOR, (RECT), Global_setter.SIZE)
            if shape == 'rectangle' or shape == 'square' or shape == 'centerrectangle':
                pygame.draw.rect(Global_setter.screen, Global_setter.COLOR, (RECT), Global_setter.SIZE, Global_setter.FILLETRADII)
            pygame.draw.rect(Global_setter.screen, Global_setter.BLUE, (RECT), 1)
            moveRectCheck = []
            for i in range(len(movepoints)):
                moverect = Utilities.CenterSquareRect(movepoints[i][0], movepoints[i][1], 15)
                moveRectCheck.append(moverect.collidepoint(x3, y3))
                if moverect.collidepoint(x3, y3) and Global_setter.drawingArea.collidepoint(x3, y3):
                    pygame.draw.rect(Global_setter.screen, Global_setter.BLUE, (moverect), 2)
                    j = i
                    move = True
                    changeState = False
                innerPointColor = Global_setter.WHITE
                outerPointColor = Global_setter.BLACK
                innerRECT = Utilities.CenterSquareRect(movepoints[i][0], movepoints[i][1], 4)
                outerRECT = Utilities.CenterSquareRect(movepoints[i][0], movepoints[i][1], 6)
                pygame.draw.rect(Global_setter.screen, innerPointColor, (innerRECT),0)
                pygame.draw.rect(Global_setter.screen, outerPointColor, (outerRECT),1)
            if not mousedown:
                move = False 
                changeState = True
            elif mousedown and (x3, y3) not in movepoints and move:
                Utilities.drawTextBox((' ' + str(RECT.size) + ' '), font, Global_setter.BLACK, pygame.Rect(RECT.topright[0], RECT.topright[1] - 30,len(' ' + str(RECT.size) + ' ')*5, 20), 150)
                if j == 0 and abs(x3-movepoints[1][0]) > width*2 and abs(y3-movepoints[3][1]) > width*2:
                    movepoints[j] = (x3, y3)
                    RECT = pygame.Rect(movepoints[0][0], movepoints[0][1], abs(movepoints[2][0] - movepoints[0][0]), abs(movepoints[2][1] - movepoints[0][1]))
                elif j == 1 and abs(x3-movepoints[0][0]) > width*2 and abs(y3-movepoints[3][1]) > width*2:
                    movepoints[j] = (x3, y3)
                    RECT = pygame.Rect(movepoints[3][0], y3, abs(x3 - movepoints[3][0]), abs(y3 - movepoints[3][1]))
                elif j == 2 and abs(x3-movepoints[0][0]) > width*2 and abs(y3-movepoints[0][1]) > width*2:
                    movepoints[j] = (x3, y3)
                    RECT = pygame.Rect(movepoints[0][0], movepoints[0][1], abs(movepoints[0][0] - x3), abs(movepoints[0][1] - y3))
                elif j == 3 and abs(x3-movepoints[2][0]) > width*2 and abs(y3-movepoints[0][1]) > width*2:
                    movepoints[j] = (x3, y3)
                    RECT = pygame.Rect(x3, movepoints[1][1], abs(movepoints[1][0] - x3), abs(movepoints[1][1] - y3))
                elif j == 4 and (movepoints[3][1]-y3) > width*2:
                    movepoints[j] = ((RECT.topleft[0] + RECT.topright[0])/2, y3)
                    RECT = pygame.Rect(movepoints[0][0], y3, abs(movepoints[0][0] - movepoints[2][0]), abs(movepoints[3][1] - y3))
                elif j == 5 and (x3-movepoints[0][0]) > width*2 :
                    movepoints[j] = (x3, (RECT.topleft[1] + RECT.bottomright[1])/2)
                    RECT = pygame.Rect(movepoints[0][0], movepoints[0][1], abs(movepoints[0][0] - x3), abs(movepoints[0][1] - movepoints[3][1]))
                elif j == 6 and (y3-movepoints[0][1]) > width*2:
                    movepoints[j] = ((RECT.bottomright[0] + RECT.bottomleft[0])/2, y3)
                    RECT = pygame.Rect(movepoints[0][0], movepoints[0][1], abs(movepoints[0][0] - movepoints[1][0]), abs(movepoints[0][1] - y3))    
                elif j == 7 and (movepoints[2][0]-x3) > width*2:
                    movepoints[j] = ((x3, (RECT.bottomleft[1] + RECT.topleft[1])/2))
                    RECT = pygame.Rect(x3, movepoints[0][1], abs(movepoints[2][0] - x3), abs(movepoints[0][1] - movepoints[3][1]))
                    changeState = False
            elif mousedown and 1 not in moveRectCheck and RECT.collidepoint(x3, y3) and boxMove:
                Utilities.drawTextBox((' ' + str(RECT.centerx-10) + ', ' + str(RECT.centery-50)), font, Global_setter.BLACK, pygame.Rect(x3 + 15, y3,len(' ' + str(RECT.centerx-10) + ', ' + str(RECT.centery-50))*7, 20), 150)
                LENX = RECT[2]    
                LENY = RECT[3]
                if x8 > x3:
                    movepoints[0] = (firstPos[0] - abs(x8 - x3), RECT[1])
                    RECT = pygame.Rect(movepoints[0][0], movepoints[0][1], LENX, LENY)
                elif x8 < x3:
                    movepoints[0] = (firstPos[0] + abs(x8 - x3), RECT[1])
                    RECT = pygame.Rect(movepoints[0][0], movepoints[0][1], LENX, LENY)
                if y8 > y3:
                    movepoints[0] = (RECT[0], firstPos[1] - abs(y8 - y3))
                    RECT = pygame.Rect(movepoints[0][0], movepoints[0][1], LENX, LENY)
                elif y8 < y3:
                    movepoints[0] = (RECT[0], firstPos[1] + abs(y8 - y3))
                    RECT = pygame.Rect(movepoints[0][0], movepoints[0][1], LENX, LENY)
                changeState = False
            if not mousedown and 1 not in moveRectCheck and RECT.collidepoint(x3, y3):    
                x8 = x3
                y8 = y3
                firstPos = movepoints[0]   
            # Draw center line.
            
            pygame.draw.line(Global_setter.screen, Global_setter.BLUE, (movepoints[4][0] + 5, movepoints[5][1]), (movepoints[4][0] - 5, movepoints[5][1]), 1)
            pygame.draw.line(Global_setter.screen, Global_setter.BLUE, (movepoints[4][0], movepoints[5][1] + 5), (movepoints[4][0], movepoints[5][1] - 5), 1)   
            otherButton = Main_interface.mainInterface(x3, y3, mousedownINTERFACE, changeState, False, False, False, True)
            if otherButton == 'undo':
                undo = True
            if otherButton == 'save':
                save = True
            if otherButton == 'saveas':
                saveas = True
            if otherButton == 'newFile':
                return 'newFile'
            if mousedownINTERFACE == True:
                mousedownINTERFACE = False
                mousedown = False
            pygame.display.update()
            Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
            # check for exit.
            # check if other tool button is pressed.
            if shape != Global_setter.STATE:
                toolButtonPressed = True
            if (mousedown and 1 not in moveRectCheck and not RECT.collidepoint(x3, y3) and not move and Global_setter.drawingArea.collidepoint(x3, y3)) or toolButtonPressed:
                if shape == 'rectangle' or shape == 'square' or shape == 'centerrectangle':
                    Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
                    pygame.draw.rect(Global_setter.screen, Global_setter.COLOR, (RECT), Global_setter.SIZE, Global_setter.FILLETRADII)
                    Main_interface.mainInterface(x3, y3, False, False)
                    pygame.display.update()
                    newscreen = Global_setter.screen.copy()
                    Global_setter.SCREENLIST.append(newscreen)
                    edit = False
                if shape == 'ellipse':
                    Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
                    pygame.draw.ellipse(Global_setter.screen, Global_setter.COLOR, (RECT), Global_setter.SIZE)
                    Main_interface.mainInterface(x3, y3, False, False)
                    pygame.display.update()
                    newscreen = Global_setter.screen.copy()
                    Global_setter.SCREENLIST.append(newscreen)
                    edit = False
            if escape:
                edit = False
            if undo:
                edit = False
                pygame.time.wait(200)
            if shape == 'rectangle' or shape == 'square' or shape == 'centerrectangle':
                if save or saveas:
                    Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
                    pygame.draw.rect(Global_setter.screen, Global_setter.COLOR, (RECT), Global_setter.SIZE, Global_setter.FILLETRADII)
                    pygame.display.update()
                    Main_interface.mainInterface(x3, y3, mousedown, True, False, False, False, True, save, saveas)
                    newscreen = Global_setter.screen.copy()
                    Global_setter.SCREENLIST.append(newscreen)
                    edit = False
            if shape == 'ellipse':
                if save or saveas:
                    Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
                    pygame.draw.ellipse(Global_setter.screen, Global_setter.COLOR, (RECT), Global_setter.SIZE)
                    pygame.display.update()
                    Main_interface.mainInterface(x3, y3, mousedown, True, False, False, False, True, save, saveas)
                    newscreen = Global_setter.screen.copy()
                    Global_setter.SCREENLIST.append(newscreen)
                    edit = False

# manages editing of lines and polylines
def polyEdit(edit, polylist, width, lineType, color, center = None):
    if edit:
        mousedown = False
        move = False
        movecenter = False
        isRegular = True
        regularPolylist = copy.deepcopy(polylist)
        edit = True
        newscreen = Global_setter.screen.copy()
        escape = False
        enter = False
        undo = False
        undoCount = 0
        saveCount = 0
        save = False
        saveas = False
        try:
            newCenter = [center[0], center[1]]
        except:
            pass
            
        # create a font object.
        fonts_dir = Global_setter.APP_PATH + '\\fonts\\' 
        font = pygame.font.Font(fonts_dir + 'OpenSans-Bold.ttf', 13)
        
        while edit:
            x1, y1 = pygame.mouse.get_pos()
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT:
                    save = Exit_cntrl.quitWindow()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if Global_setter.drawingArea.collidepoint(x1, y1):
                        boxMove = True
                    mousedown = True
                if event.type == pygame.MOUSEBUTTONUP:
                    mousedown = False
                    boxMove = False
                if keys[pygame.K_ESCAPE]:
                    escape = True
                if keys[pygame.K_RETURN]:
                    enter = True
            shift = Utilities.keyPressed(pygame.K_LSHIFT)
            zPressed = Utilities.keyPressed(pygame.K_z)
            leftControl = Utilities.keyPressed(pygame.K_LCTRL)
            sPressed = Utilities.keyPressed(pygame.K_s)
            if leftControl and not zPressed:
                undoCount = 1
            elif not leftControl and zPressed:
                undoCount = 0
            if undoCount == 1 and zPressed:
                undo = True
            
            if leftControl and not sPressed:
                saveCount = 1
            elif not leftControl and sPressed:
                saveCount = 0
            if saveCount == 1 and sPressed:
                save = True 
            
            if lineType == 'line':
                pointConnect(polylist[0][0], polylist[0][1], polylist[1][0], polylist[1][1], 'circular', Global_setter.SIZE, Global_setter.COLOR)
                pygame.draw.line(Global_setter.screen, Global_setter.BLUE, polylist[0], polylist[1], 1)
            elif lineType == 'polygon':
                for i in range(0, len(polylist)):
                    if i == len(polylist)-1:
                        pointConnect(int(polylist[i][0]), int(polylist[i][1]), int(polylist[0][0]), int(polylist[0][1]), 'circular', Global_setter.SIZE, Global_setter.COLOR, False)
                        break
                    pointConnect(int(polylist[i][0]), int(polylist[i][1]), int(polylist[i+1][0]), int(polylist[i+1][1]), 'circular', Global_setter.SIZE, Global_setter.COLOR)
                pygame.draw.polygon(Global_setter.screen, Global_setter.BLUE, polylist, 1)
            elif lineType == 'polyline':
                for i in range(0, len(polylist)):
                    if i == len(polylist)-1:
                        break
                    pointConnect(polylist[i][0], polylist[i][1], polylist[i+1][0], polylist[i+1][1], 'circular', Global_setter.SIZE, Global_setter.COLOR, False)
                    pygame.draw.line(Global_setter.screen, Global_setter.BLUE, (polylist[i][0], polylist[i][1]), (polylist[i+1][0], polylist[i+1][1]), 1)
                   
            moveRectCheck = []
            for i in range(len(polylist)):
                if lineType == 'polyline' and i == len(polylist) - 1:
                    innerPointColor = Global_setter.BLACK
                    outerPointColor = Global_setter.WHITE 
                else:
                    innerPointColor = Global_setter.WHITE
                    outerPointColor = Global_setter.BLACK 
                innerRECT = Utilities.CenterSquareRect(polylist[i][0], polylist[i][1], 4)
                outerRECT = Utilities.CenterSquareRect(polylist[i][0], polylist[i][1], 6)
                pygame.draw.rect(Global_setter.screen, innerPointColor, (innerRECT),0)
                pygame.draw.rect(Global_setter.screen, outerPointColor, (outerRECT),1)
                moverect = Utilities.CenterSquareRect(polylist[i][0], polylist[i][1], 15)
                moveRectCheck.append(moverect.collidepoint(x1, y1))
                if moverect.collidepoint(x1, y1) and Global_setter.drawingArea.collidepoint(x1, y1):
                    pygame.draw.rect(Global_setter.screen, Global_setter.BLUE, (moverect), 2)
                    move = True
                    if not mousedown:
                        moveIndex = i
                    break        
            if not mousedown:
                move = False
            if mousedown and (x1, y1) not in polylist and move:
                try:
                    moveIndex
                except:
                    break
                polylist[moveIndex] = [x1, y1]
                isRegular = False
                # draw length and angle indicators
                if moveIndex == 0:
                    polyAngleDraw(polylist[moveIndex][0], polylist[moveIndex][1], polylist, moveIndex + 1)
                    polyLengthDraw(polylist[moveIndex], polylist[moveIndex+1])
                else:
                    polyLengthDraw(polylist[moveIndex], polylist[moveIndex-1])
                    polyAngleDraw(polylist[moveIndex][0], polylist[moveIndex][1], polylist, moveIndex - 1)
                Main_interface.mainInterface(x1, y1, mousedown, False)
            else:
                if Global_setter.drawingArea.collidepoint(x1, y1):
                    Main_interface.mainInterface(x1, y1, False)
                else:
                    otherButton = Main_interface.mainInterface(x1, y1, mousedown, True, False, False, False, True)
                    if otherButton == 'undo':
                        undo = True
                    if otherButton == 'save':
                        save = True
                    if otherButton == 'saveas':
                        saveas = True
                    if otherButton == 'newFile':
                        return 'newFile'
                    mousedown = False
                    
            if lineType == 'polygon' and isRegular:
                x8 = center[0] - 7.5
                y8 = center[1] - 7.5
                length = 15
                centerRect = pygame.Rect(x8, y8,length, length)
                pygame.draw.line(Global_setter.screen, Global_setter.BLUE, (newCenter[0] + 5, newCenter[1]), (newCenter[0] - 5, newCenter[1]), 1)
                pygame.draw.line(Global_setter.screen, Global_setter.BLUE, (newCenter[0], newCenter[1] + 5), (newCenter[0], newCenter[1] - 5), 1)
                if centerRect.collidepoint(x1, y1):
                    movecenter = True
                
                if mousedown and movecenter and boxMove:
                    if center[0] > x1:
                        for i in range(len(regularPolylist)):
                            polylist[i][0] = regularPolylist[i][0] - abs(center[0] - x1)
                    if center[0] < x1:
                        for i in range(len(regularPolylist)):
                            polylist[i][0] = regularPolylist[i][0] + abs(center[0] - x1)
                    if center[1] > y1:
                        for i in range(len(regularPolylist)):
                            polylist[i][1] = regularPolylist[i][1] - abs(center[1] - y1)
                    if center[1] < y1:
                        for i in range(len(regularPolylist)):
                            polylist[i][1] = regularPolylist[i][1] + abs(center[1] - y1) 
                    newCenter[0] = x1
                    newCenter[1] = y1 
                    Utilities.drawTextBox(('  ' + str(int(newCenter[0])-10) + ' ' + str(int(newCenter[1])-50) + ' '), font, Global_setter.BLACK, pygame.Rect(newCenter[0] + 15, newCenter[1], len('  ' + str(int(newCenter[0])-10) + ' ' + str(int(newCenter[1])-50) + ' ')*6, 20), 150)
                    Main_interface.mainInterface(x1, y1, mousedown, False)
                else:
                    if Global_setter.drawingArea.collidepoint(x1, y1):
                        Main_interface.mainInterface(x1, y1, False)
                    else:
                        otherButton = Main_interface.mainInterface(x1, y1, mousedown, True, False, False, False, True)
                        if otherButton == 'undo':
                            undo = True
                        if otherButton == 'save':
                            save = True
                        mousedown = False
                    
            if lineType == 'polyline' and mousedown and shift and [x1, y1] not in polylist:
                move = False
                polylist.append([x1, y1])
                moveIndex = len(polylist) - 1
            
            pygame.display.update() 
            Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
            if lineType == 'line':
                if (Global_setter.drawingArea.collidepoint(x1, y1) and mousedown and 1 not in moveRectCheck and not move) or Global_setter.STATE != 'line':
                    Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
                    pointConnect(polylist[0][0], polylist[0][1], polylist[1][0], polylist[1][1], 'circular', Global_setter.SIZE, Global_setter.COLOR)
                    Main_interface.mainInterface(x1, y1, False, False)
                    pygame.display.update()
                    newscreen = Global_setter.screen.copy()
                    Global_setter.SCREENLIST.append(newscreen)
                    edit = False
                if escape:
                    edit = False
                if undo:
                    edit = False
                    pygame.time.wait(200) 
                if save or saveas:
                    Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
                    pointConnect(polylist[0][0], polylist[0][1], polylist[1][0], polylist[1][1], 'circular', Global_setter.SIZE, Global_setter.COLOR)
                    pygame.display.update()
                    Main_interface.mainInterface(x1, y1, mousedown, True, False, False, False, True, save, saveas)
                    newscreen = Global_setter.screen.copy()
                    Global_setter.SCREENLIST.append(newscreen)
                    edit = False
                continue
            if lineType == 'polyline':
                if (Global_setter.drawingArea.collidepoint(x1, y1) and mousedown and 1 not in moveRectCheck and not move  and not shift) or Global_setter.STATE != 'polyline':
                    Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
                    for i in range(0, len(polylist)):
                        if i == len(polylist)-1:
                            break
                        pointConnect(polylist[i][0], polylist[i][1], polylist[i+1][0], polylist[i+1][1], 'circular', Global_setter.SIZE, Global_setter.COLOR)
                    Main_interface.mainInterface(x1, y1, False, False)
                    pygame.display.update()
                    newscreen = Global_setter.screen.copy()
                    Global_setter.SCREENLIST.append(newscreen)
                    edit = False
                if escape:
                    edit = False
                if undo:
                    edit = False
                    pygame.time.wait(200) 
                if save or saveas:
                    Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
                    for i in range(0, len(polylist)):
                        if i == len(polylist)-1:
                            break
                        pointConnect(polylist[i][0], polylist[i][1], polylist[i+1][0], polylist[i+1][1], 'circular', Global_setter.SIZE, Global_setter.COLOR)
                    pygame.display.update()
                    Main_interface.mainInterface(x1, y1, mousedown, True, False, False, False, True, save, saveas)
                    newscreen = Global_setter.screen.copy()
                    Global_setter.SCREENLIST.append(newscreen)
                    edit = False
                continue
            if lineType == 'polygon':
                if Global_setter.STATE != 'polygon' or enter:
                    Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
                    for i in range(0, len(polylist)):
                        if i == len(polylist)-1:
                            pointConnect(int(polylist[i][0]), int(polylist[i][1]), int(polylist[0][0]), int(polylist[0][1]), 'circular', Global_setter.SIZE, Global_setter.COLOR)
                            break
                        pointConnect(int(polylist[i][0]), int(polylist[i][1]), int(polylist[i+1][0]), int(polylist[i+1][1]), 'circular', Global_setter.SIZE, Global_setter.COLOR)
                    #pygame.draw.polygon(Global_setter.screen, Global_setter.COLOR, polylist, width)
                    Main_interface.mainInterface(x1, y1, False, False)
                    pygame.display.update()
                    newscreen = Global_setter.screen.copy()
                    Global_setter.SCREENLIST.append(newscreen)
                    edit = False
                if escape:
                    edit = False  
                if undo:
                    edit = False
                    pygame.time.wait(200) 
                if save or saveas:
                    Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
                    for i in range(0, len(polylist)):
                        if i == len(polylist)-1:
                            pointConnect(int(polylist[i][0]), int(polylist[i][1]), int(polylist[0][0]), int(polylist[0][1]), 'circular', Global_setter.SIZE, Global_setter.COLOR)
                            break
                        pointConnect(int(polylist[i][0]), int(polylist[i][1]), int(polylist[i+1][0]), int(polylist[i+1][1]), 'circular', Global_setter.SIZE, Global_setter.COLOR)
                    pygame.display.update()
                    Main_interface.mainInterface(x1, y1, mousedown, True, False, False, False, True, save, saveas)
                    newscreen = Global_setter.screen.copy()
                    Global_setter.SCREENLIST.append(newscreen)
                    edit = False
  
# draws polygon on canvas  
def drawPolygon(noOfSide, width, color, x, y):
    #Global_setter.drawingArea = pygame.Rect(10, 50, Global_setter.WIDTH - 310, Global_setter.HEIGHT - 70)
    draw = True
    polylist = []
    released = False
    newscreen = Global_setter.screen.copy()
    while draw:
        x3, y3 = pygame.mouse.get_pos()
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                draw = False
            if event.type == pygame.MOUSEBUTTONUP:
                released = True
        for i in range(0, 360, int(360/noOfSide)):
            if len(polylist) > (noOfSide-1):
                break
            length = int(math.sqrt((x3 - x)**2 + (y3 - y)**2)) 
            x4 = x + math.sin(math.radians(i + 180)) * length
            y4 = y + math.cos(math.radians(i + 180)) * length
            polylist.append([x4, y4])
       
        # Draw center line.
        pygame.draw.line(Global_setter.screen, Global_setter.BLUE, (x + 5, y), (x - 5, y), 1)
        pygame.draw.line(Global_setter.screen, Global_setter.BLUE, (x, y + 5), (x, y - 5), 1) 
        for i in range(0, len(polylist)):
            if i == len(polylist)-1:
                pointConnect(int(polylist[i][0]), int(polylist[i][1]), int(polylist[0][0]), int(polylist[0][1]), 'circular', width, color)
                break
            pointConnect(int(polylist[i][0]), int(polylist[i][1]), int(polylist[i+1][0]), int(polylist[i+1][1]), 'circular', width, color)
        pygame.display.update(Global_setter.drawingArea)
        Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
        if released:
            fileMenuCheck = polyEdit(released, polylist, width, 'polygon', color, [x, y])
            if fileMenuCheck == 'newFile':
                Global_setter.screen.fill(Global_setter.BGCOLOR, (Global_setter.drawingArea))
                pygame.display.update()
                newlscreen = Global_setter.screen.copy()
                Global_setter.SCREENLIST.append(newlscreen)
                return
            else:
                Main_interface.mainInterface(x3, y3, False, False)
                draw = False
                Main_interface.mainInterface(x, y, False, True, True, True)
        polylist = []

# draws line on canvas
def drawLine(x, y, width, color):
    draw = True
    released = False
    newscreen = Global_setter.screen.copy()
    while draw:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                draw = False
            if event.type == pygame.MOUSEBUTTONUP:
                released = True
        x1, y1 = pygame.mouse.get_pos()
        polylist = [(x, y), (x1, y1)]
        pointConnect(x, y, x1, y1, 'circular', width, color)
        polyAngleDraw(x1, y1, polylist, 0)
        #Global_setter.drawingArea = pygame.Rect(10, 50, Global_setter.WIDTH - 310, Global_setter.HEIGHT - 70)
        pygame.display.update(Global_setter.drawingArea)
        Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
        if released:
            fileMenuCheck = polyEdit(released, polylist, width, 'line', color)
            if fileMenuCheck == 'newFile':
                Global_setter.screen.fill(Global_setter.BGCOLOR, (Global_setter.drawingArea))
                pygame.display.update()
                newlscreen = Global_setter.screen.copy()
                Global_setter.SCREENLIST.append(newlscreen)
                return
            else:
                Main_interface.mainInterface(x, y, False, False)
                draw = False
                Main_interface.mainInterface(x, y, False, True, True, True)

# draws circle on canvas
def drawCircle(x, y, color, width):
    draw = True
    released = False
    newscreen = Global_setter.screen.copy()
    while draw:
        x3, y3 = pygame.mouse.get_pos()
        radius = int(math.sqrt((x3 - x)**2 + (y3 - y)**2))
        pygame.draw.circle(Global_setter.screen, color, (x, y), radius, width)
        #Global_setter.drawingArea = pygame.Rect(10, 50, Global_setter.WIDTH - 310, Global_setter.HEIGHT - 70)
        pygame.display.update((Global_setter.drawingArea))
        Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                    draw = False
            if event.type == pygame.MOUSEBUTTONDOWN: 
                draw = False
            if event.type == pygame.MOUSEBUTTONUP:
                released = True
        if released:
            fileMenuCheck = circleEdit(released, radius, color, width, x, y)
            if fileMenuCheck == 'newFile':
                Global_setter.screen.fill(Global_setter.BGCOLOR, (Global_setter.drawingArea))
                pygame.display.update()
                newlscreen = Global_setter.screen.copy()
                Global_setter.SCREENLIST.append(newlscreen)
                return
            else:
                draw = False
                Main_interface.mainInterface(x, y, False, True, True, True)       

# draws rectangle that increases from center of the rectangle
def drawCenterRectangle(width, color, x, y, filletradii=1):
    #draw = True
    #released = False
    #move = True
    #Global_setter.drawingArea = pygame.Rect(10, 50, Global_setter.WIDTH - 310, Global_setter.HEIGHT - 70)
    draw = True
    released = False
    newscreen = Global_setter.screen.copy()
    while draw:
        x3, y3 = pygame.mouse.get_pos()
        x4 = x3
        y4 = y3
        lengthx = 0
        lengthy = 0
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                    draw = False
            if event.type == pygame.MOUSEBUTTONUP:
                released = True
        if y3 < y and x3 > x:
            if abs(y - y3) < width:
                x4 = 2*x - x3
                y4 = y3
                lengthy = 2*width
                lengthx = 2*x3 - 2*x    
            elif abs(x - x3) < width:
                x4 = 2*x - x3
                y4 = y3
                lengthy = 2*y - 2*y3
                lengthx = 2*width    
            else:
                x4 = 2*x - x3
                y4 = y3
                lengthy = 2*y - 2*y3
                lengthx = 2*x3 - 2*x
        elif y3 < y and x > x3:
            if abs(y - y3) < width:
                x4 = x3
                y4 = y3
                lengthy = 2*width
                lengthx = 2*x - 2*x3  
            elif abs(x - x3) < width:
                x4 = x3
                y4 = y3
                lengthy = 2*y - 2*y3
                lengthx = 2*width       
            else:
                x4 = x3
                y4 = y3
                lengthy = 2*y - 2*y3
                lengthx = 2*x - 2*x3     
        elif y3 > y and x > x3:
            if abs(y - y3) < width:
                x4 = x3
                y4 = 2*y - y3
                lengthy = 2*width
                lengthx = 2*x - 2*x3
            elif abs(x - x3) < width:
                x4 = x3
                y4 = 2*y - y3
                lengthy = 2*y3 - 2*y
                lengthx = 2*width
            else:
                x4 = x3
                y4 = 2*y - y3
                lengthy = 2*y3 - 2*y
                lengthx = 2*x - 2*x3     
        elif y3 > y and x3 > x:
            if abs(y - y3) < width:
                x4 = 2*x - x3
                y4 = 2*y - y3
                lengthy = 2*width
                lengthx = 2*x3 - 2*x   
            elif abs(x - x3) < width:
                x4 = 2*x - x3
                y4 = 2*y - y3
                lengthy = 2*y3 - 2*y
                lengthx = 2*width
            else:
                x4 = 2*x - x3
                y4 = 2*y - y3
                lengthy = 2*y3 - 2*y
                lengthx = 2*x3 - 2*x
                 
        RECT = pygame.Rect(x4, y4, lengthx, lengthy)
        pygame.draw.rect(Global_setter.screen, color, RECT, width, filletradii)
        pygame.display.update((Global_setter.drawingArea))
        Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
        if abs(x-x3) > width or (y-y3) > width:
            if released:
                fileMenuCheck = rectEdit(released, RECT,'centerrectangle',width, color, filletradii)
                if fileMenuCheck == 'newFile':
                    Global_setter.screen.fill(Global_setter.BGCOLOR, (Global_setter.drawingArea))
                    pygame.display.update()
                    newlscreen = Global_setter.screen.copy()
                    Global_setter.SCREENLIST.append(newlscreen)
                    return
                else:
                    Main_interface.mainInterface(x3, y3, False, False)
                    draw = False
                    Main_interface.mainInterface(x, y, False, True, True, False)

# draws rectangle that increases from the top corner
def drawRectangle(width, color, x, y, filletradii=1):
    #Global_setter.drawingArea = pygame.Rect(10, 50, Global_setter.WIDTH - 310, Global_setter.HEIGHT - 70)
    draw = True
    released = False
    newscreen = Global_setter.screen.copy()
    while draw:
        x3, y3 = pygame.mouse.get_pos()
        x4 = x3
        y4 = y3
        lengthx = 0
        lengthy = 0
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                    draw = False
            if event.type == pygame.MOUSEBUTTONUP:
                released = True
        if y3 < y and x3 > x:
            
            if abs(y - y3) < width*2:
                x4 = x
                y4 = y3
                lengthx = abs(x - x3)
                lengthy = width*2
            elif abs(x - x3) < width*2:
                x4 = x
                y4 = y3
                lengthx = width*2
                lengthy = abs(y - y3)
            else:
                x4 = x
                y4 = y3
                lengthx = abs(x - x3)
                lengthy = abs(y - y3)
        elif y3 < y and x > x3: 
            
            if abs(y - y3) < width*2:
                x4 = x3
                y4 = y3
                lengthx = abs(x - x3)
                lengthy = width*2
            elif abs(x - x3) < width*2:
                x4 = x3
                y4 = y3
                lengthx = width*2
                lengthy = abs(y - y3)
            else:
                x4 = x3
                y4 = y3
                lengthx = abs(x - x3)
                lengthy = abs(y - y3)
        elif y3 > y and x > x3:
            if abs(y - y3) < width*2:
                x4 = x3
                y4 = y
                lengthx = abs(x - x3)
                lengthy = width*2
            elif abs(x - x3) < width*2:
                x4 = x3
                y4 = y
                lengthx = width*2
                lengthy = abs(y - y3)
            else:
                x4 = x3
                y4 = y
                lengthx = abs(x - x3)
                lengthy = abs(y - y3)
        elif y3 > y and x3 > x:
            if abs(y - y3) < width*2:
                x4 = x
                y4 = y
                lengthx = abs(x - x3)
                lengthy = width*2
            elif abs(x - x3) < width*2:
                x4 = x
                y4 = y
                lengthx = width*2
                lengthy = abs(y - y3)
            else:
                x4 = x
                y4 = y
                lengthx = abs(x - x3)
                lengthy = abs(y - y3)
        RECT = pygame.Rect(x4, y4, lengthx, lengthy)
        pygame.draw.rect(Global_setter.screen, color, RECT, width, filletradii)
        pygame.display.update((Global_setter.drawingArea))
        Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
        if abs(x-x3) > width or (y-y3) > width:
            if released:
                fileMenuCheck = rectEdit(released, RECT,'rectangle',width, color, filletradii)
                if fileMenuCheck == 'newFile':
                    Global_setter.screen.fill(Global_setter.BGCOLOR, (Global_setter.drawingArea))
                    pygame.display.update()
                    newlscreen = Global_setter.screen.copy()
                    Global_setter.SCREENLIST.append(newlscreen)
                    return
                else:
                    Main_interface.mainInterface(x3, y3, False, False)
                    draw = False
                    Main_interface.mainInterface(x, y, False, True, True, False)

# draws ellipse on canvas
def drawEllipse(width, color, x, y):
    draw = True
    released = False
    move = True
    #Global_setter.drawingArea = pygame.Rect(10, 50, Global_setter.WIDTH - 310, Global_setter.HEIGHT - 70)
    newscreen = Global_setter.screen.copy()
    while draw:
        
        x3, y3 = pygame.mouse.get_pos()
        x4 = x3
        y4 = y3
        lengthx = 0
        lengthy = 0
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                    draw = False
            if event.type == pygame.MOUSEBUTTONUP:
                released = True
        if y3 < y and x3 > x:
            if abs(y - y3) < width:
                x4 = 2*x - x3
                y4 = y3
                lengthy = 2*width
                lengthx = 2*x3 - 2*x    
            elif abs(x - x3) < width:
                x4 = 2*x - x3
                y4 = y3
                lengthy = 2*y - 2*y3
                lengthx = 2*width    
            else:
                x4 = 2*x - x3
                y4 = y3
                lengthy = 2*y - 2*y3
                lengthx = 2*x3 - 2*x
        elif y3 < y and x > x3:
            if abs(y - y3) < width:
                x4 = x3
                y4 = y3
                lengthy = 2*width
                lengthx = 2*x - 2*x3  
            elif abs(x - x3) < width:
                x4 = x3
                y4 = y3
                lengthy = 2*y - 2*y3
                lengthx = 2*width       
            else:
                x4 = x3
                y4 = y3
                lengthy = 2*y - 2*y3
                lengthx = 2*x - 2*x3     
        elif y3 > y and x > x3:
            if abs(y - y3) < width:
                x4 = x3
                y4 = 2*y - y3
                lengthy = 2*width
                lengthx = 2*x - 2*x3
            elif abs(x - x3) < width:
                x4 = x3
                y4 = 2*y - y3
                lengthy = 2*y3 - 2*y
                lengthx = 2*width
            else:
                x4 = x3
                y4 = 2*y - y3
                lengthy = 2*y3 - 2*y
                lengthx = 2*x - 2*x3     
        elif y3 > y and x3 > x:
            if abs(y - y3) < width:
                x4 = 2*x - x3
                y4 = 2*y - y3
                lengthy = 2*width
                lengthx = 2*x3 - 2*x   
            elif abs(x - x3) < width:
                x4 = 2*x - x3
                y4 = 2*y - y3
                lengthy = 2*y3 - 2*y
                lengthx = 2*width
            else:
                x4 = 2*x - x3
                y4 = 2*y - y3
                lengthy = 2*y3 - 2*y
                lengthx = 2*x3 - 2*x
                
        RECT = pygame.Rect(x4, y4,lengthx, lengthy)
        pygame.draw.ellipse(Global_setter.screen, color, RECT, width)
        pygame.display.update((Global_setter.drawingArea))
        Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
        if abs(x-x3) > width or (y-y3) > width:
            if released:
                fileMenuCheck = rectEdit(released, RECT,'ellipse',width, color)
                if fileMenuCheck == 'newFile':
                    Global_setter.screen.fill(Global_setter.BGCOLOR, (Global_setter.drawingArea))
                    pygame.display.update()
                    newlscreen = Global_setter.screen.copy()
                    Global_setter.SCREENLIST.append(newlscreen)
                    return
                else:
                    Main_interface.mainInterface(x3, y3, False, False)
                    draw = False
                    Main_interface.mainInterface(x, y, False, True, True, True)

# draws bezier curve on canvas
def drawBezier(width, color, x, y):
    pointercircles = [(x, y)]
    newscreen = Global_setter.screen.copy()
    innerPointColor = Global_setter.WHITE
    outerPointColor = Global_setter.BLACK 
    innerRECT = Utilities.CenterSquareRect(x, y, 4)
    outerRECT = Utilities.CenterSquareRect(x, y, 6)
    pygame.draw.rect(Global_setter.screen, innerPointColor, (innerRECT),0)
    pygame.draw.rect(Global_setter.screen, outerPointColor, (outerRECT),1)
    pygame.display.update()
    out = []
    space = False
    index = 0
    move = False
    mousedown = False
    draw = True
    #Global_setter.drawingArea = pygame.Rect(10, 50, Global_setter.WIDTH - 310, Global_setter.HEIGHT - 70)
    boxMove = False
    canMove = False
    mousedownINTERFACE = False
    undoCount = 0
    saveCount = 0
    undo = False
    save = False
    saveas = False
    while draw: 
        x3, y3 = pygame.mouse.get_pos()
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                save = Exit_cntrl.quitWindow()
            if keys[pygame.K_ESCAPE]:
                Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Global_setter.drawingArea.collidepoint(x3, y3):
                    boxMove = True
                else:
                    mousedownINTERFACE = True
                mousedown = True
            if event.type == pygame.MOUSEBUTTONUP:
                mousedown = False 
                boxMove = False
                mousedownINTERFACE = False
        if undo:
            Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
            return 
        shift = Utilities.keyPressed(pygame.K_LSHIFT)
        zPressed = Utilities.keyPressed(pygame.K_z)
        leftControl = Utilities.keyPressed(pygame.K_LCTRL)
        sPressed = Utilities.keyPressed(pygame.K_s)
        if leftControl and not zPressed:
            undoCount = 1
        elif not leftControl and zPressed:
            undoCount = 0
        if undoCount == 1 and zPressed:
            undo = True
            
        if leftControl and not sPressed:
            saveCount = 1
        elif not leftControl and sPressed:
            saveCount = 0
        if saveCount == 1 and sPressed:
            save = True 
        moveRectCheck = []
        if len(pointercircles) < 4:
            otherButton = Main_interface.mainInterface(x3, y3, mousedownINTERFACE, True, False, False, False, True)
            if otherButton == 'undo':
                undo = True
            if otherButton == 'save':
                save = True
            if otherButton == 'saveas':
                saveas = True
            if otherButton == 'newFile':
                Global_setter.screen.fill(Global_setter.BGCOLOR, (Global_setter.drawingArea))
                pygame.display.update()
                newlscreen = Global_setter.screen.copy()
                Global_setter.SCREENLIST.append(newlscreen)
                return
            if mousedownINTERFACE:
                mousedownINTERFACE = False
                mousedown = False
            pygame.display.update()
            if Global_setter.STATE != 'beziercurve':
                Global_setter.screen.blit(newscreen, (0, 0, Global_setter.HEIGHT, Global_setter.WIDTH))
                draw = False
            if save or saveas:
                Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
                pygame.display.update()
                Main_interface.mainInterface(x3, y3, mousedown, True, False, False, False, True, save, saveas)
                return
        if mousedown and len(pointercircles) < 4 and Global_setter.drawingArea.collidepoint(x3, y3):
            if (x3,y3) not in pointercircles:
                innerPointColor = Global_setter.WHITE
                outerPointColor = Global_setter.BLACK 
                innerRECT = Utilities.CenterSquareRect(x3, y3, 4)
                outerRECT = Utilities.CenterSquareRect(x3, y3, 6)
                pygame.draw.rect(Global_setter.screen, innerPointColor, (innerRECT),0)
                pygame.draw.rect(Global_setter.screen, outerPointColor, (outerRECT),1)
                pointercircles.append((x3, y3))
                length = len(pointercircles)
                pygame.display.update()
            if len(pointercircles) >= 2:
                pygame.draw.line(Global_setter.screen, Global_setter.BLUE, pointercircles[length - 2], pointercircles[length - 1], 1)
                pygame.display.update()
        if len(out) > 0:
            for i in range(len(out[0])):
                gfxdraw.filled_circle(Global_setter.screen, int(out[0][i]), int(out[1][i]), round(Global_setter.SIZE/2), Global_setter.COLOR)
                #pygame.draw.line(Global_setter.screen, Global_setter.COLOR, (int(out[0][i]) + Global_setter.SIZE/2, int(out[1][i]) - Global_setter.SIZE/2), (int(out[0][i]) - Global_setter.SIZE/2, int(out[1][i]) + Global_setter.SIZE/2), 2)
            for i in range(len(pointercircles)):
                moverect = Utilities.CenterSquareRect(pointercircles[i][0], pointercircles[i][1], 15)
                moveRectCheck.append(moverect.collidepoint(x3, y3))
                if moverect.collidepoint(x3, y3):
                    pygame.draw.rect(Global_setter.screen, Global_setter.BLUE, (moverect), 2)
                    
                    if not mousedown:
                        index = i
                        move = False
                    elif mousedown:
                        move = True
                if (x3, y3) not in pointercircles and move and boxMove:
                    pointercircles[index] = (x3, y3)
                if i == len(pointercircles) - 1:
                    innerPointColor = Global_setter.BLACK
                    outerPointColor = Global_setter.WHITE 
                else:
                    innerPointColor = Global_setter.WHITE
                    outerPointColor = Global_setter.BLACK 
                innerRECT = Utilities.CenterSquareRect(pointercircles[i][0], pointercircles[i][1], 4)
                outerRECT = Utilities.CenterSquareRect(pointercircles[i][0], pointercircles[i][1], 6)
                pygame.draw.rect(Global_setter.screen, innerPointColor, (innerRECT),0)
                pygame.draw.rect(Global_setter.screen, outerPointColor, (outerRECT),1)
                canMove = True
            otherButton = Main_interface.mainInterface(x3, y3, mousedownINTERFACE, True, False, False, False, True)
            if otherButton == 'undo':
                undo = True
            if otherButton == 'save':
                save = True
            if otherButton == 'saveas':
                saveas = True
            if otherButton == 'newFile':
                Global_setter.screen.fill(Global_setter.BGCOLOR, (Global_setter.drawingArea))
                pygame.display.update()
                newlscreen = Global_setter.screen.copy()
                Global_setter.SCREENLIST.append(newlscreen)
                return
            if mousedownINTERFACE:
                mousedownINTERFACE = False
                mousedown = False
            pygame.display.update()
            Global_setter.screen.blit(newscreen, (0, 0, Global_setter.HEIGHT, Global_setter.WIDTH))
        if len(pointercircles) >= 4:
            data = np.array(pointercircles)
            tck,u = interpolate.splprep(data.transpose(), s=0)
            unew = np.arange(0, 1.0, 0.0001)
            out = interpolate.splev(unew, tck)
        
        # add more points
        if shift and mousedown and (x3, y3) not in pointercircles and len(pointercircles) < 15:    
            pointercircles.append((x3, y3))
            space = False 
            
        # Check for exit.
        if Global_setter.STATE != 'beziercurve':
            draw = False
        if len(out) > 0 and mousedown and Global_setter.drawingArea.collidepoint(x3, y3) and 1 not in moveRectCheck and not move and canMove and not shift:
            Global_setter.screen.blit(newscreen, (0, 0, Global_setter.HEIGHT, Global_setter.WIDTH))
            for i in range(len(out[0])):
                gfxdraw.filled_circle(Global_setter.screen, int(out[0][i]), int(out[1][i]), round(Global_setter.SIZE/2), Global_setter.COLOR)
            Main_interface.mainInterface(x, y, False)
            pygame.display.update()
            newscreen = Global_setter.screen.copy()
            Global_setter.SCREENLIST.append(newscreen)
            Main_interface.mainInterface(x, y, False, True, True)
            draw = False
            Main_interface.mainInterface(x, y, False, True, True, True)
        if len(out) > 0:
            if save or saveas:
                Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
                for i in range(len(out[0])):
                    gfxdraw.filled_circle(Global_setter.screen, int(out[0][i]), int(out[1][i]), round(Global_setter.SIZE/2), Global_setter.COLOR)
                pygame.display.update()
                newscreen = Global_setter.screen.copy()
                Global_setter.SCREENLIST.append(newscreen)
                Main_interface.mainInterface(x3, y3, mousedown, True, False, False, False, True, save, saveas)
                Main_interface.mainInterface(x, y, False, True, True)
                draw = False
                Main_interface.mainInterface(x, y, False, True, True, True)       

# draws square on canvas
def drawSquare(width, color, x, y, filletradii=1):
    released = False
    draw = True
    #Global_setter.drawingArea = pygame.Rect(10, 50, Global_setter.WIDTH - 310, Global_setter.HEIGHT - 70)
    newscreen = Global_setter.screen.copy()
    while draw:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                    draw = False
            if event.type == pygame.MOUSEBUTTONUP:
                released = True 
            
        x3, y3 = pygame.mouse.get_pos()
        x4 = x - abs(x3-x)
        y4 = y - abs(x3-x)
        lengthx = 2*abs(x3-x)
        lengthy = 2*abs(x3-x)
        RECT = pygame.Rect(x4, y4, lengthx, lengthy)
        pygame.draw.rect(Global_setter.screen, color, RECT, width, filletradii)
        pygame.display.update((Global_setter.drawingArea))
        Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
        if abs(x-x3) > width or (y-y3) > width:
            if released:
                fileMenuCheck = rectEdit(released, RECT, 'square',width, color, filletradii)
                if fileMenuCheck == 'newFile':
                    Global_setter.screen.fill(Global_setter.BGCOLOR, (Global_setter.drawingArea))
                    pygame.display.update()
                    newlscreen = Global_setter.screen.copy()
                    Global_setter.SCREENLIST.append(newlscreen)
                    return
                else:
                    Main_interface.mainInterface(x3, y3, False, False)
                    draw = False
                    Main_interface.mainInterface(x, y, False, True, True, True)

# draws a poly line(combination of chained lines) on canvas
def drawPolyline(x, y, width, color):
    draw = True
    released = False
    polylist = [[x, y]]
    edit = False
    newscreen = Global_setter.screen.copy()
    while draw:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                    draw = False
            if event.type == pygame.MOUSEBUTTONUP:
                released = True
            if keys[pygame.K_RETURN]:
                edit = True
        
        x1, y1 = pygame.mouse.get_pos()
        
        lastIndex = len(polylist) - 1
        pointConnect(polylist[lastIndex][0], polylist[lastIndex][1], x1, y1, 'circular', width, color)
        polyAngleDraw(x1, y1, polylist, lastIndex)
        if released:
            if [x1, y1] not in polylist and Global_setter.drawingArea.collidepoint(x1, y1):
                polylist.append([x1, y1])
            released = False
        if len(polylist) >= 2:
            for i in range(0, len(polylist)):
                if i == len(polylist)-1:
                    break
                pointConnect(polylist[i][0], polylist[i][1], polylist[i+1][0], polylist[i+1][1], 'circular', width, color)
        
        #Global_setter.drawingArea = pygame.Rect(10, 50, Global_setter.WIDTH - 310, Global_setter.HEIGHT - 70)
        pygame.display.update(Global_setter.drawingArea)
        Global_setter.screen.blit(newscreen, (0, 0, Global_setter.WIDTH, Global_setter.HEIGHT))
        if edit:
            fileMenuCheck = polyEdit(edit, polylist, width, 'polyline',color)
            if fileMenuCheck == 'newFile':
                Global_setter.screen.fill(Global_setter.BGCOLOR, (Global_setter.drawingArea))
                pygame.display.update()
                newlscreen = Global_setter.screen.copy()
                Global_setter.SCREENLIST.append(newlscreen)
                return
            else:
                draw = False   
                Main_interface.mainInterface(x, y, False, True, True, True)

# program_end.