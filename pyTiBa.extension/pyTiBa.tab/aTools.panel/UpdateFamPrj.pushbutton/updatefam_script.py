'''
update Revit prj/families in folder
inspired and c by
sixtysecondrevit, J.Pierson! - Bulk Upgrade #Revit files with #DynamoBIM
Posted on October 26, 2016
'''

from __future__ import print_function    

__title__ = "Update\nFam/Prj\ninFolder"  

__author__ = "Tillmann Baumeister"       


from Autodesk.Revit import DB
import sys, os                  
import traceback                
import pyrevit                 
from pyrevit import (forms, revit)
from pyrevit.forms import BaseCheckBoxItem 
                                
app = __revit__.Application     
                                
#path to file stored on disk    
folderpath = forms.pick_folder()
if not folderpath:              
    sys.exit()                  


# Get List of Files in Dir and SubDir. 
def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = []
    # Iterate over all the entries 
    for entry in listOfFile: 
        # Create full path   
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath): 
            allFiles = allFiles + getListOfFiles(fullPath)
        else:  
            allFiles.append(fullPath) if entry.endswith(("rfa", "rfv", "rft")) else  None
    return allFiles


def updatefiles(folderpath):
    for fp in getListOfFiles(folderpath):
        print("updating: ", fp)         
        opendoc=  app.OpenDocumentFile(fp)
        bool = opendoc.Close() # closes the document and saves it 

print("\n ---------------------------------------------------")
updatefiles(folderpath)

# Remarks
# 