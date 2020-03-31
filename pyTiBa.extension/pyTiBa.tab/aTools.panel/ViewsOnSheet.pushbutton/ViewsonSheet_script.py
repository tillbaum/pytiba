# -*- coding: utf-8 -*-
'''
Place selected Views on Sheet
author: T.Baumeister
 '''

__title__ = "Place\nViews on Sheet" 
__author__ = "Tillmann Baumeister"


from Autodesk.Revit import DB  
import sys, os   

import pyrevit  
from pyrevit import forms   
from pyrevit import script  



doc = __revit__.ActiveUIDocument.Document 
uidoc = __revit__.ActiveUIDocument 
uiapp = __revit__   
app = uiapp.Application    

# raw_input("Press Enter to continue")


# for i in secviewlist: print i.Name

###> THis doesnt' work because: selection is either current view, or views marked in 
# PBrowser 

secviewlist = [doc.GetElement(elId) for elId in uidoc.Selection.GetElementIds()]

sheetview = list()
viewlist = list()
[viewlist.append(i) if i.Category.Name.Equals("Views") else sheetview.append(i) if i.Category.Name.Equals("Sheets") else False
            for i in secviewlist]


if not viewlist:
    forms.alert("Select Views in the Project Browser to place on Sheet", ok= True)
    sys.exit()
 

if not sheetview:
    forms.alert("You have to select a Sheet also", ok= True)
    sys.exit()


try:
    t = DB.Transaction(doc, "test") 
    t.Start()   
    for i in viewlist:
        viewport = DB.Viewport.Create(doc, sheetview[0].Id, i.Id, DB.XYZ(0,0,0))
        #vplist.append(viewport)
    t.Commit()
    
except:
    t.RollBack()
    t.Dispose()
    import traceback
    print traceback.format_exc()

        









#ToDo: Get Parameter Values from Titleblock:  
#- SheetIssueDate, DrawnBy   



# ViewPortTypes, Change ViewPort Type, Retrieve a List of all Types.    

# validtypes= viewport.GetValidTypes() #returns a List of element id's of all Viewport Types
# with revit.Transaction("Change Vieport Type"):   
    # vp.ChangeTypeId(validtype[2])   

	
# >>> validtypes   
# ﻿List[ElementId]([<Autodesk.Revit.DB.ElementId object at 0x0000000000001A83 [872]>, <Autodesk.Revit.DB.ElementId object at 0x0000000000001A84 [3173]>, <Autodesk.Revit.DB.ElementId object at 0x0000000000001A85 [4212]>, <Autodesk.Revit.DB.ElementId object at 0x0000000000001A86 [56967]>, <Autodesk.Revit.DB.ElementId object at 0x0000000000001A87 [56970]>])
# vptype= doc.GetElement(validtypes[1]) 
# typeParSet= vptype.Parameters 
# for i in typeParSet: print i.Definition.Name 
# ... ss
# ﻿Show Title 
# Category 
# Color    
# Category 
# Design Option
# Family Name  
# Line Weight  
# Type Name    
# Show Extension Line
# Title        
# Line Pattern   ---> Type Parameters of Viewport Type    
     
	 