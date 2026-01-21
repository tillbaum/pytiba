'''Open Revit Family 2019 Folder in WIN Explorer'''


#__title__ = "Family\nFol.2018"

__author__ = "T.Baumeister"

from Autodesk.Revit import DB 
import sys, os
import traceback
#import pyrevit
from pyrevit import (forms, revit)


# create filepath.txt file at first run.  Overwrite filepath when shiftclick! 
def filepath(filename_str): 
    path = os.path.split(sys.argv[0])[0] 
    try: 
        if __shiftclick__ == True: raise Exception()
        with open(path +"\\"+ filename_str, "r+") as f: # a+ mode, because I need "create file" funciton 
            folderpath = f.read()
            return folderpath
    except:
        folderpath = forms.pick_folder() 
        if not folderpath: sys.exit() 
        with open(path + "\\filepath.txt", "w") as f: 
            f.write(folderpath) 
        return folderpath 


path = filepath("filepath.txt")
pathtxt = 'explorer  "' + path + '"'

import subprocess
subprocess.Popen(pathtxt)

