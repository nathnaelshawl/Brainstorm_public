# Brainstorm drawing application
# created by: @nathnael_shawl(ናትናኤል ሻውል) last edited: 4:18 PM Monday, April 25, 2022, Addis Ababa, Ethiopia
# Splash_screen.py --> creates window when program is initialized at first. 
# contains onClick() and splashScreen() functions.
# ---------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------

# import dependencies and modules 
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import webbrowser
import sys
import time
from . import Global_setter

# terminates the program when close button is pressed.
def terminate(root):
    root.destroy()
    sys.exit()
    
def  confirm_presets(root, width_entry, height_entry, window_choice):
    global width, height, window_type
    try:
        int(width_entry.get())
        int(height_entry.get())
    except:
        popup_box("Error", "Invalid entry!", 'showerror')
        width_entry.delete(0, END)
        height_entry.delete(0, END)
        return
    width = int(width_entry.get())
    height = int(height_entry.get())
    window_type = window_choice.get()
    if window_type == 'fixed' and ((width > Global_setter.SCR_WIDTH - 310 or width < 200) or (height > Global_setter.SCR_HEIGHT-70 or height < 400)):
        popup_box("Error", "Invalid entry!", 'showerror')
        width_entry.delete(0, END)
        height_entry.delete(0, END)
        if width >= Global_setter.SCR_WIDTH - 310:
            width_entry.insert(0, Global_setter.SCR_WIDTH - 310)
        elif width <= 200:
            width_entry.insert(0, 200)
        if height >= Global_setter.SCR_HEIGHT-70:
            height_entry.insert(0, Global_setter.SCR_HEIGHT-70)
        elif height <= 400:
            height_entry.insert(0, 400)
        return
    if window_type == 'resizable' and ((width > Global_setter.SCR_WIDTH - 310 or width < 100) or (height > Global_setter.SCR_HEIGHT-70 or height < 100)):
        popup_box("Error", "Invalid entry!", 'showerror')
        width_entry.delete(0, END)
        height_entry.delete(0, END)
        if width >= Global_setter.SCR_WIDTH - 310:
            width_entry.insert(0, Global_setter.SCR_WIDTH - 310)
        elif width <= 100:
            width_entry.insert(0, 100)
        if height >= Global_setter.SCR_HEIGHT-70:
            height_entry.insert(0, Global_setter.SCR_HEIGHT-70)
        elif height <= 100:
            height_entry.insert(0, 400)
        return
    root.destroy()

def manupulate_scr_size(Entry_obj, sign):
    try:
        int(Entry_obj.get())
    except:
        popup_box("Error", "Invalid entry!", 'showerror')
        Entry_obj.delete(0, END)
        return
    if sign == '+':
        scr_size = int(Entry_obj.get()) + 1
        Entry_obj.delete(0, END)
        Entry_obj.insert(0, scr_size)
    elif sign == '-':
        scr_size = int(Entry_obj.get()) - 1
        Entry_obj.delete(0, END)
        Entry_obj.insert(0, scr_size)

def popup_box(title, text, popup_type):
    if popup_type == 'showerror':
        messagebox.showerror(title, text)
    elif popup_type == 'showwarning':
        messagebox.showwarning(title, text)
# creates the splash window
def splashScreen():
    # initialize the screen.
    root = Tk()
    root.title('About Brainstorm')
    root.overrideredirect(1)

    scrWidth = int((Global_setter.SCR_WIDTH - 320)/2)
    scrHeight = int((Global_setter.SCR_HEIGHT - 500)/2)
    root.geometry("320x500+{}+{}".format(scrWidth, scrHeight))
    app_icons_dir = Global_setter.APP_PATH + '\\Icons\\app_icons\\'
    
    appIcon = ImageTk.PhotoImage(Image.open(app_icons_dir + "BrainstormInstallIcon.png").resize((150,155), Image.ANTIALIAS))
    root.iconbitmap(app_icons_dir + "BrainstormInstallIcon.ico")
    
    frame = LabelFrame(root, width=250, height=150, text='Set canvas size', font='TkTextFont 10 bold', relief=RIDGE, bd=4)
    frame.grid_propagate(False)
    
    window_choice = StringVar()
    window_choice.set('fixed')
    radio_button1 = Radiobutton(frame, text='Fixed Window\n(Recommended)', variable=window_choice, value='fixed')
    radio_button2 = Radiobutton(frame, text='Resizable Window\n(unstable)', variable=window_choice, value='resizable', command=lambda: popup_box('Warning', 'Unstable build !!!\nApp may crash without warning.', 'showwarning'))
    set_width_btn = Button(frame, text="Fixed window", font='TkTextFont 9 bold', fg='red', command=lambda: onClick(root))
    set_height_btn = Button(frame, text="Ma", font='TkTextFont 9 bold', fg='red', command=lambda: onClick(root))

    # Other window components.
    Label(root, image = appIcon).pack(pady=20)
    Label(root, text="Brainstorm ",font='TkTextFont 25 bold').pack()
    Label(root, text="Version 1.0\n© Nathnael Shawl\n", fg='gray',font='TkTextFont 8 bold').pack()
    frame.pack()
    radio_button1.grid(row=0, column=0)
    radio_button2.grid(row=0, column=1)
    Label(frame, text="Width\n({}-max)".format(Global_setter.SCR_WIDTH - 310)).grid(row=1, column=0)
    Label(frame, text="Height\n({}-max)".format(Global_setter.SCR_HEIGHT-70)).grid(row=2, column=0)
    
    width_frame = LabelFrame(frame, width=120, height=30, relief=FLAT)
    width_frame.grid_propagate(False)
    width_frame.grid(row=1, column=1)
    height_frame = LabelFrame(frame, width=120, height=30, relief=FLAT)
    height_frame.grid_propagate(False)
    height_frame.grid(row=2, column=1)
    
    width_entry = Entry(width_frame, width=4, borderwidth=2, font='Helvetica 11')
    height_entry = Entry(height_frame, width=4, borderwidth=2, font='Helvetica 11')
    

    width_entry.grid(row=0, column=0, padx=5)
    width_entry.insert(0, Global_setter.SCR_WIDTH-310)
    height_entry.grid(row=0, column=0, padx=5)
    height_entry.insert(0, Global_setter.SCR_HEIGHT-70)
    
    Button(width_frame, text=" + ", command=lambda: manupulate_scr_size(width_entry, '+')).grid(row=0,column=1, padx=5)
    Button(width_frame, text=" - ", command=lambda: manupulate_scr_size(width_entry, '-')).grid(row=0,column=2, padx=5)
    
    Button(height_frame, text=" + ", command=lambda: manupulate_scr_size(height_entry, '+')).grid(row=0,column=1, padx=5)
    Button(height_frame, text=" - ", command=lambda: manupulate_scr_size(height_entry, '-')).grid(row=0,column=2, padx=5)
    
    confirmation_frame = LabelFrame(root, width=250, height=30, relief=FLAT)
    confirmation_frame.grid_propagate(False)
    confirmation_frame.pack()

    # 'Close' button.
    close_button = Button(confirmation_frame, text="Close" , font='TkTextFont 10 bold', fg='red', command=lambda: terminate(root))
    close_button.grid(row=0, column=0, padx=50)

    # 'Next' button
    
    next_button = Button(confirmation_frame, text=" Next " , font='TkTextFont 10 bold', fg='green', command=lambda: confirm_presets(root, width_entry, height_entry, window_choice))
    next_button.grid(row=0, column=1)
   
    start = time.time()

    # The window self distructs itself after some time to allow the program to start.
    #root.after(3000,lambda:root.destroy())
    root.mainloop()
    return width, height, window_type
#program_end.