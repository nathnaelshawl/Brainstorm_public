# Brainstorm drawing application
# created by: @nathnael_shawl(ናትናኤል ሻውል) last edited: 12:46 AM Monday, April 11, 2022, Addis Ababa, Ethiopia
# Options_screen.py --> create options window to display shortcut showing menu. 
# contains optionsWindow() function.
#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------

# import dependencies and modules 
from tkinter import *
from PIL import ImageTk, Image
from . import Global_setter

def optionsWindow():
    # create and initialize a window.
    root = Tk()
    root.title('Options')
    
    scrWidth = int((root.winfo_screenwidth() - 320)/2)
    scrHeight = int((root.winfo_screenheight() - 300)/2)
    root.geometry("510x250+{}+{}".format(scrWidth, scrHeight))
    
    app_icons_dir = Global_setter.APP_PATH + '\\Icons\\app_icons\\'
    
    root.iconbitmap(app_icons_dir + "BrainstormInstallIcon.ico")
    root.resizable('False', 'False')
    
    # create the necessary labels and buttons.
    
    frame = LabelFrame(root, width=200, height=180, text=" Global shortcuts ", font='TkTextFont 10 bold', relief=RIDGE, bd=4)
    frame.grid_propagate(False)
    frame.grid(row=0, column=0, sticky=W,padx=15, pady=5)
    
    Button(frame, text="CTRL+S", state=DISABLED, disabledforeground='black').grid(row=0, column=0, padx=5,pady=5)
    Button(frame, text="CTRL+Z", state=DISABLED, disabledforeground='black').grid(row=1, column=0, padx=5,pady=5)
    Button(frame, text="CTRL+Y", state=DISABLED, disabledforeground='black').grid(row=2, column=0, padx=5,pady=5)
    Button(frame, text="ESC", state=DISABLED,padx=12, disabledforeground='black').grid(row=3, column=0, padx=5,pady=5)
    
    Label(frame, text="- Save           ", font='TkTextFont 10 ').grid(row=0, column=1)
    Label(frame, text="- Undo           ", font='TkTextFont 10 ').grid(row=1, column=1)
    Label(frame, text="- Redo           ", font='TkTextFont 10 ').grid(row=2, column=1)
    Label(frame, text="- Discard a draft", font='TkTextFont 10 ').grid(row=3, column=1)
    
    frame1 = LabelFrame(root, width=250, height=180, text=" Other shortcuts ", font='TkTextFont 10 bold', relief=RIDGE, bd=4)
    frame1.grid_propagate(False)
    frame1.grid(row=0, column=1, sticky=W,padx=15, pady=5)
    
    Button(frame1, text="ENTER", state=DISABLED, disabledforeground='black').grid(row=0, column=0, padx=5,pady=5)
    Button(frame1, text="SHIFT+LCLICK", state=DISABLED, disabledforeground='black').grid(row=1, column=0, padx=5,pady=5)
    
    
    Label(frame1, text="- Confirm polygon draw", font='TkTextFont 10 ').grid(row=0, column=1)
    Label(frame1, text="- Add new points for   ", font='TkTextFont 10 ').grid(row=1, column=1)
    Label(frame1, text="    spline & polyline  ", font='TkTextFont 10 ').grid(row=2, column=1)
    
    frame2 = Frame(root, width=200, height=50)
    frame2.grid(row=1, column=1, padx=15, pady=5)
    appIcon = ImageTk.PhotoImage(Image.open(app_icons_dir + "BrainstormInstallIcon.png").resize((40,40), Image.ANTIALIAS))
    Label(frame2, image = appIcon).grid(row=0, column=0, padx=15)

    Label(frame2, image = appIcon).grid(row=0, column=0)
    Label(frame2, text="Brainstorm\n Version 1.0\n© Nathnael_Shawl", fg='grey', font='TkTextFont 7 bold').grid(row=0, column=1)

    root.mainloop()
# program_end.