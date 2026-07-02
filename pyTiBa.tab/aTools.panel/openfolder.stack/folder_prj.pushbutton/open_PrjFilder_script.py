'''Open Revit Prj Folder in WIN Explorer'''


#__title__ = "Prj\nFolder" 
__author__ = "T.Baumeister" 

from Autodesk.Revit import DB 
import sys, os 
import traceback 
import pyrevit 
from pyrevit import (forms, revit) 
import subprocess

# Get the current Revit document path
pathname = __revit__.ActiveUIDocument.Document.PathName

if pathname:
    # Extract the folder path
    folderpath = os.path.split(pathname)[0]
    # print("Opening folder: {}".format(folderpath))
    
    # Correct way to open a folder in Windows Explorer
    subprocess.Popen(['explorer', folderpath])
else:
    pyrevit.forms.alert("Warning: This model hasn't been saved yet, so there is no folder to open!", title="Open Project Folder", warn_icon=True)
    # print("Warning: This model hasn't been saved yet, so there is no folder to open!")



