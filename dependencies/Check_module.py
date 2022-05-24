# Brainstorm drawing application
# created by: @nathnael_shawl(ናትናኤል ሻውል) last edited:10:38 AM Sunday, April 24, 2022, Addis Ababa, Ethiopia
# Check_module.py --> checks if certain model exists and if it doesnt it would download it
# ---------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------

# import dependencies and modules 
import pip
import imp

# list of packages
packages=[]
packages.append('pygame')
packages.append('numpy')
packages.append('scipy')
packages.append('webbrowser')
packages.append('pillow')
packages.append('pyautogui')
#packages.append('pywin32')
#packages.append('win32api')

# fuction that checks and downloads modules
def check():
    for i in range(len(packages)):
        try:
            imp.find_module(packages[i])
        except ImportError:
            try:
                pip.main(['install', packages[i]])
            except:
                raise Exception("Can't install {}".format(i))
                sys.exit()
# program_end.