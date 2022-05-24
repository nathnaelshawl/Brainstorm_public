# Brainstorm drawing application
# created by: @nathnael_shawl(ናትናኤል ሻውል) last edited: 10:34 AM Sunday, April 24, 2022, Addis Ababa, Ethiopia
# About_screen.py --> display a window about the application 
# ---------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------

# import dependencies and modules 
from tkinter import *
from PIL import ImageTk, Image
import webbrowser
from . import Global_setter

# button event handler
def whenClick(index):
    # forwards links of the developer contact.
    webPages = []
    webPages.append('https://t.me/Brain_Bird')
    webPages.append('https://www.linkedin.com/in/nathnael-shawl-09286b208/')
    webPages.append('https://www.youtube.com/channel/UCauvxAjjOHPCVexWpVIjbTA')
    webbrowser.open(webPages[index])
   
# main about window create.   
def aboutWindow():
    # initialize the window
    
    root = Tk() 
    root.title('About Brainstorm')
    
    scrWidth = int((root.winfo_screenwidth() - 320)/2)
    scrHeight = int((root.winfo_screenheight() - 300)/2)
    root.geometry("510x275+{}+{}".format(scrWidth, scrHeight))
    
    app_icons_dir = Global_setter.APP_PATH + '\\Icons\\app_icons\\'
    link_icons_dir = Global_setter.APP_PATH + '\\Icons\\link_icons\\'
    
    root.iconbitmap(app_icons_dir + "BrainstormInstallIcon.ico")
    root.resizable('False', 'False')
   
    appIcon = ImageTk.PhotoImage(Image.open(app_icons_dir + "BrainstormInstallIcon.png").resize((64,64), Image.ANTIALIAS))
    
    # import button image files
    telegramIcon = ImageTk.PhotoImage(Image.open(link_icons_dir + "Telegram_logo.png").resize((34,34), Image.ANTIALIAS))
    linkedinIcon = ImageTk.PhotoImage(Image.open(link_icons_dir + "Linkedin_logo.png").resize((64,34), Image.ANTIALIAS))
    youtubeIcon = ImageTk.PhotoImage(Image.open(link_icons_dir + "Youtube_logo.png").resize((64,34), Image.ANTIALIAS))
    
    # create button and information labels
    
    label1 = Label(root, image = telegramIcon)
    label2 = Label(root, image = linkedinIcon)
    label3 = Label(root, image = youtubeIcon)
    
    Label(root, image = appIcon).grid(row=0, column=0, padx = 20, pady = 10)
    Label(root, text="Brainstorm\n Version 1.0\n© Nathnael_Shawl", font='TkTextFont 10 bold').grid(row=0, column=1)
    Label(root, text="Description", font='TkTextFont 10 ').grid(row=1, column=0)
    Label(root, text="-------------------------------------------------------------\n"
                    "Brainstorm is a pseudo 2D computer aided design(CAD)\n"\
                    "application. Its intended purpose is to provide a simple  "\
                    "\n brainstorming platform before the actual design in CAD."\
                    "\n-------------------------------------------------------------"\
                    "\nTo contact the developer use the links below '\u2193'\n").grid(row=2, column=1)
    
    frame = Frame(root, width=200, height=50)
    frame.grid(row=3, column=1)
    
    telegram_button = Button(frame, image=telegramIcon, command=lambda: whenClick(0))
    linkedin_button = Button(frame, image=linkedinIcon, command=lambda: whenClick(1))
    youtube_button = Button(frame, image=youtubeIcon, command=lambda: whenClick(2))
    
    telegram_button.grid(row=0, column=0, padx=25)
    linkedin_button.grid(row=0, column=1, padx=25)
    youtube_button.grid(row=0, column=2, padx=25)

    root.mainloop()
# program_end.