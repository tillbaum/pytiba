# -*- coding: utf-8 -*-
'''
dublicates the chosen Sheet: 
TitleBlocks(multiple), Legends are copied and placed at the same 
location
created 24.08.2019
author: T.Baumeister
 '''

__title__ = "dublicate \nSheet" 
__author__ = "Tillmann Baumeister"


from Autodesk.Revit import DB 
import sys, os  
from pyrevit import (forms, revit)  
from pyrevit import script

import clr 
import pyrevit 

doc = __revit__.ActiveUIDocument.Document 
uidoc = __revit__.ActiveUIDocument 
uiapp = __revit__ 
app = uiapp.Application 


sel = [doc.GetElement(elId) for elId in uidoc.Selection.GetElementIds()]
if sel:
    try:
        sheet= [i for i in sel if i.ViewType.Equals(DB.ViewType.DrawingSheet)][0]
    except: pass
elif uidoc.ActiveView.ViewType.Equals(DB.ViewType.DrawingSheet):
    sheet =uidoc.ActiveView
else: 
    forms.alert("No sheet selected", ok=True)
    sys.exit()

vportIdlist= sheet.GetAllViewports() #returns elementIds

viewtypelist = [DB.ViewType.Legend]

# listcomp: tuple (3elem: view, XYZ-Point, vportTypeId)
view_xyz_vptypeId= [(doc.GetElement(doc.GetElement(vpid).ViewId),
                            doc.GetElement(vpid).GetBoxCenter(), 
                            doc.GetElement(vpid).GetTypeId())
                    for vpid in vportIdlist if doc.GetElement(doc.GetElement(vpid).ViewId).ViewType in viewtypelist]


# get TitleBlock of Sheet to dublicate
tibl = DB.FilteredElementCollector(doc).OwnedByView(sheet.Id).OfCategory(DB.BuiltInCategory.OST_TitleBlocks) \
            .ToElements()

#Get the Type of the TitleBlock Instance 
tibltype = tibl[0].Symbol 
tiblXYZ = tibl[0].Location.Point 

with revit.Transaction("dublicate Sheet"):
    sheetA = DB.ViewSheet.Create(doc, tibltype.Id)

    #Place 2nd TitleBlock, if it exists
    if len(tibl) >1:
        doc.Create.NewFamilyInstance(DB.XYZ(0,0,0), tibl[1].Symbol, sheetA)
    elif len(tibl) >2: print "MORE Than 2 TitleBlocks on Sheet"
    
    #create legend viewports
    for view, xyzpt, vptypeid in view_xyz_vptypeId:
        vp= DB.Viewport.Create(doc, sheetA.Id, view.Id, xyzpt.Subtract(tiblXYZ))
        
        # Match the Type of the Viewport with ChangeTypeId-Method
        vp.ChangeTypeId(vptypeid)



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
# ... 
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


