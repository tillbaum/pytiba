'''
update Revit prj/families in folder
inspired and c by
sixtysecondrevit, J.Pierson!
Bulk Upgrade #Revit files with #DynamoBIM
Posted on October 26, 2016
ToDo: update all subdirectories

'''
from __future__ import print_function

__title__ = "Update_Fam/Prj"
                                
__author__ = "Tillmann Baumeister"


from Autodesk.Revit import DB   
import sys, os                  
import traceback                
#import pyrevit                 
from pyrevit import (forms, revit)
from pyrevit.forms import BaseCheckBoxItem 
                                
app = __revit__.Application     
                                
#path to file stored on disk    
folderpath = forms.pick_folder()
if not folderpath:              
    sys.exit()                  
                                
#os.listdir(path) returns a list of strings of filenames and 
#subdirectories from the given path, or current if omitted. 
print('\nUpdateing files ... ------------------------ \n')
                                      
for i in os.listdir(folderpath):      
    fp = os.path.join(folderpath, i)  
    print("updating: ", fp)           
    opendoc=  app.OpenDocumentFile(fp)
    bool = opendoc.Close() # closes the document and saves it

# Remarks
# 