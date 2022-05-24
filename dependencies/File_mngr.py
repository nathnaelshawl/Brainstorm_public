# Brainstorm drawing application
# created by: @nathnael_shawl(ናትናኤል ሻውል) last edited: 9:19 PM Sunday, April 17, 2022, Addis Ababa, Ethiopia
# File_mngr.py --> responsible when opening existing files, creating newfiles and also saving files. 
# contains terminate(), quitWindowDraw() and quitWindow() functions.
# ---------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------

# import dependencies and modules 
import pygame
from pygame.locals import *
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
from . import Global_setter
from . import Exit_cntrl

# saves image files
def saveImage(saved, filename, openImage=False):
    # load app icon
    app_icons_dir = Global_setter.APP_PATH + '\\Icons\\app_icons\\'
    # if the file is not saved.
    if not saved:
        filedialogbox = Tk()
        filedialogbox.withdraw()
        filedialogbox.iconbitmap(app_icons_dir + "BrainstormInstallIcon.ico")
        try:
            filedialogbox.filename = filedialog.asksaveasfilename(initialdir = "c/", title = 'Save file', filetypes=(("png files" ,"*.png"), ("all files", "*.*"))) 
        except:
            print("can't open")
            filedialogbox.destroy()
            return '' 
        # Global_setter.drawingArea = pygame.Rect(10, 50, Global_setter.WIDTH - 310, Global_setter.HEIGHT - 70)
        # drawingSurface = Global_setter.screen.subsurface(Global_setter.drawingArea)
        captureArea = pygame.Rect(10, 50, Global_setter.drawingArea.width, Global_setter.drawingArea.height)
        drawingSurface = Global_setter.SCREENLIST[Global_setter.UNDOINDEX-1].subsurface(captureArea)
        if (filedialogbox.filename != ''):
            if (filedialogbox.filename)[len(filedialogbox.filename)-4:] == '.png':
                filename = filedialogbox.filename
            else:
                filename = filedialogbox.filename + '.png'
            pygame.image.save(drawingSurface, filename)
            saved_file_name = filedialogbox.filename
            filedialogbox.destroy()
            return saved_file_name
        else:
            filedialogbox.destroy()
            return ''
    # if the file is saved.
    if (filename != '.png'):
        # Global_setter.drawingArea = pygame.Rect(10, 50, Global_setter.WIDTH - 310, Global_setter.HEIGHT - 70)
        drawingSurface = Global_setter.screen.subsurface(Global_setter.drawingArea)
        pygame.image.save(drawingSurface, filename)

# returns the location of the file we want to open.
def openImage(): 
    app_icons_dir = Global_setter.APP_PATH + '\\Icons\\app_icons\\'
    filedialogbox = Tk()
    filedialogbox.withdraw()
    filedialogbox.iconbitmap(app_icons_dir + "BrainstormInstallIcon.ico")
    filedialogbox.filename = filedialog.askopenfilename(initialdir = "c/", title = 'select a file', filetypes=(("PNG files" ,"*.png"),("JPEG files", "*.jpeg;*.jpg"))) 
    opened_file_name = filedialogbox.filename
    filedialogbox.destroy()
    return opened_file_name
# program_end