# Brainstorm drawing application, version-1.0.2
# created by: @nathnael_shawl(ናትናኤል ሻውል) last edited:10:34 AM Sunday, April 24, 2022, Addis Ababa, Ethiopia
# Email - nathnaels4@gmail.com
# main.py --> entry point and also a center to execute commands.
# ---------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------

# Check if the necessary modules are available and download them
#from dependencies import Check_module
#Check_module.check()

# import dependencies and modules 
from dependencies import Global_setter
from dependencies import Main_interface
from dependencies import Draw_tools
from dependencies import Action_tools
from dependencies import Utilities
from dependencies import Exit_cntrl
from dependencies import Splash_screen

import pygame, sys
from pygame.locals import *
from tkinter import *
from PIL import ImageTk, Image
import os

# Set default path to acess files

if getattr(sys, 'frozen', False):
    app_path = os.path.dirname(sys.executable)
else:
    app_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(app_path)

# initialize the global variables and setting a current path
Global_setter.init(app_path)


# entry point
def main():
    # prepare interface layer

    Global_setter.screen.fill(Global_setter.WHITE)
    mousedown = False
    Main_interface.mainInterface(0, 0, mousedown)
    pygame.display.update()
    newscreen = Global_setter.screen.copy()
    Global_setter.SCREENLIST.append(newscreen)
    FIRSTSCREEN = Global_setter.SCREENLIST
    
    # App main loop
    while Global_setter.running:
        # Event handeler
        sPressed = Utilities.keyPressed(pygame.K_s)
        zPressed = Utilities.keyPressed(pygame.K_z)
        yPressed = Utilities.keyPressed(pygame.K_y)
        leftControl = Utilities.keyPressed(pygame.K_LCTRL)
        # check for undo
        if leftControl and not zPressed:
            Global_setter.undoCount = 1
        elif not leftControl and zPressed:
            Global_setter.undoCount = 0
        # check for redo    
        if leftControl and not yPressed:
            Global_setter.redoCount = 1
        elif not leftControl and yPressed:
            Global_setter.redoCount = 0
            # check if it is undo or redo
        if Global_setter.undoCount == 1 and zPressed:
            Global_setter.undoOrRedo = 'undo'
            Global_setter.undoCount = 0
        elif Global_setter.redoCount == 1 and yPressed:
            Global_setter.undoOrRedo = 'redo'
            Global_setter.redoCount = 0
        x, y = pygame.mouse.get_pos()
        if Global_setter.undoOrRedo != 'none':
            Main_interface.mainInterface(x, y, mousedown, True, False, False, Global_setter.undoOrRedo)
            Global_setter.undoOrRedo = 'none'
        else:
            Main_interface.mainInterface(x, y, mousedown, True)
        mousedown = False
        if leftControl and not sPressed:
            Global_setter.saveCount = 1
        elif not leftControl and sPressed:
            Global_setter.saveCount = 0
        if Global_setter.saveCount == 1 and sPressed:
            Main_interface.mainInterface(x, y, mousedown, True, False, False, False, False, True)
        
        # screen update for resizable window option.
        intermidSurf = pygame.Surface(Global_setter.drawingArea.size)
        captureArea = pygame.Rect(Global_setter.drawingArea.left, Global_setter.drawingArea.top, Global_setter.WIDTH-310, Global_setter.HEIGHT- 50)
        try:
            intermidSurf.blit(Global_setter.screen.subsurface(captureArea),(0,0))
        except:
            captureArea = pygame.Rect(10, 50, Global_setter.drawingArea.width, Global_setter.drawingArea.height)
            intermidSurf.blit(Global_setter.SCREENLIST[Global_setter.UNDOINDEX-1].subsurface(captureArea), (0, 0))
            Global_setter.windowSizeSetter(intermidSurf)
            continue
        # Event manager
        # perform drawing or other functions based on the events.
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            # capture window resize event.
            if event.type == VIDEORESIZE:
                Global_setter.windowSizeSetter(intermidSurf)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousedown = True
                if Global_setter.drawingArea.collidepoint(x, y) and mousedown:
                    # Use eraser tool
                    if Global_setter.STATE == 'eraser':
                        Draw_tools.pencil(x, y, 'circular', Global_setter.SIZE, Global_setter.BGCOLOR, False)
                    # Draw with circular end marker
                    elif Global_setter.STATE == 'pencil':
                        Draw_tools.pencil(x, y, 'circular', Global_setter.SIZE, Global_setter.COLOR)
                    # Draw with circular end marker
                    elif Global_setter.STATE == 'marker':
                        Draw_tools.pencil(x, y, 'line', Global_setter.SIZE, Global_setter.COLOR)
                    # Use the fill color tool
                    elif Global_setter.STATE == 'fill':
                        Action_tools.fill(x, y, Global_setter.COLOR)
                    # draw line
                    elif Global_setter.STATE == 'line':
                        Draw_tools.drawLine(x, y, Global_setter.SIZE, Global_setter.COLOR)
                    # draw circle
                    elif Global_setter.STATE == 'circle':
                        Draw_tools.drawCircle(x, y, Global_setter.COLOR, Global_setter.SIZE)
                    # draw rectangle.
                    elif Global_setter.STATE == 'rectangle':
                        Draw_tools.drawRectangle(Global_setter.SIZE, Global_setter.COLOR, x, y, Global_setter.FILLETRADII)
                    # draw center rectangle.
                    elif Global_setter.STATE == 'centerrectangle':
                        Draw_tools.drawCenterRectangle(Global_setter.SIZE, Global_setter.COLOR, x, y,
                                                       Global_setter.FILLETRADII)
                    # draw bezier curve
                    elif Global_setter.STATE == 'beziercurve':
                        Draw_tools.drawBezier(Global_setter.SIZE, Global_setter.COLOR, x, y)
                    # draw elipse
                    elif Global_setter.STATE == 'ellipse':
                        Draw_tools.drawEllipse(Global_setter.SIZE, Global_setter.COLOR, x, y)
                    # draw square
                    elif Global_setter.STATE == 'square':
                        Draw_tools.drawSquare(Global_setter.SIZE, Global_setter.COLOR, x, y, Global_setter.FILLETRADII)
                    # draw polygon  
                    elif Global_setter.STATE == 'polygon':
                        Draw_tools.drawPolygon(Global_setter.NUMBEROFSIDES + 2, Global_setter.SIZE, Global_setter.COLOR,
                                               x, y)
                        # draw a polyline
                    elif Global_setter.STATE == 'polyline':
                        Draw_tools.drawPolyline(x, y, Global_setter.SIZE, Global_setter.COLOR)
                    mousedown = False
                    
            if event.type == pygame.MOUSEBUTTONUP:
                mousedown = False
            if event.type == pygame.QUIT:
                save = Exit_cntrl.quitWindow()
                if save:
                    Main_interface.mainInterface(x, y, mousedown, True, False, False, False, False, True)
        # use the eye droper tool.
        if Global_setter.STATE == 'eyedroper':
            COLOR1 = Action_tools.eyeDroper()
            if COLOR1 != None:
                Global_setter.COLOR = COLOR1
        pygame.display.update()


# run_main
if (__name__ == '__main__'):
    main()
# system exit
pygame.quit()
sys.exit()

# program_end.
# 3534
