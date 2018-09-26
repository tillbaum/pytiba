# -*- coding: utf-8 -*-
'''Create Viewport on Sheet'''

__title__ = "ViewPort on Sheet"

__author__ = "Tillmann Baumeister"

import clr
from Autodesk.Revit.DB import *
from Autodesk.Revit import DB
import System 
#from System.Collections.Generic import List
import sys
import os
from rpw.ui.forms import TaskDialog 
from pyrevit import forms 
import traceback
import pyrevit

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument 
uiapp = __revit__ # is the same as uiapp = DocumentManager.Instance.CurrentUIApplication
# returns:  <Autodesk.Revit.UI.UIApplication object at 0x0000000000000171 [Autodesk.Revit.UI.UIApplication]>
app = uiapp.Application


# FECsec = DB.FilteredElementCollector(doc).OfClass(DB.ViewSection) \
                   # .WhereElementIsNotElementType().ToElements()
# secviewlist = [i for i in FECsec if i.Name.Contains("SecA")]
# secviewlist = list(reversed(secviewlist))
# for i in secviewlist: print i.Name


secviewlist = [doc.GetElement(elId) for elId in uidoc.Selection.GetElementIds()]

if secviewlist:
    secviewlist[0].Name.Contains("Sec")
    for i in secviewlist: print i.Name

    
    currentsheet = uidoc.ActiveView
    print currentsheet.Name 

    vplist = []
    t = Transaction(doc, "test")
    t.Start()
    try:
        for i, view in enumerate(secviewlist):
            viewport = Viewport.Create(doc, currentsheet.Id, view.Id, XYZ(0,0,0))
            vplist.append(viewport)
        t.Commit()
        t.Dispose()
    except:
        t.RollBack()
        t.Dispose()
        import traceback
        print traceback.format_exc()

        
#vplist = [doc.GetElement(i) for i in uidoc.ActiveView.GetAllViewports()]
# vp_names = [doc.GetElement(vp.ViewId).Name for vp in vplist]
# print vp_names
#secviewlist = [doc.GetElement(vp.ViewId) for vp in vplist]


# X Coordinates: XYZ (0,0,0), (x1, 0, 0) (x1+x2,0,0)
ptlist = []
ptlist.append(XYZ(0,0,0))
temp = []
for view in secviewlist:
    X_pred = view.CropBox.Max.X / view.Scale
    temp.append(X_pred)
    point = XYZ(sum(temp), 0, 0)
    ptlist.append(point)

def movevp( vec_translat, viewport):
    scale = doc.GetElement(viewport.ViewId).Scale
    boxoutline = viewport.GetBoxOutline()
    pt1 = boxoutline.MaximumPoint + XYZ(-1, -1, 0) /scale # 1ft in x & y direction
    ptcenter = viewport.GetBoxCenter()
    vecToNewCenter = pt1 - ptcenter
    try:
        t = Transaction(doc, "move")
        t.Start()
        viewport.SetBoxCenter(vecToNewCenter + vec_translat)
        t.Commit()
    except:
        t.RollBack()
        print "Error"
        import traceback
        print traceback.format_exc()

# bipwidth = DB.BuiltInParameter(SHEET_WIDTH)
# shnr =uidoc.ActiveView.SheetNumber
# FilteredElementCollector(doc).OfCategory(TitleBlock).WhereElementIsNotElementType().ToElements()


ptglobal = XYZ(-0.5 , 0.05 , 0) / 0.3048
ptend = [i + ptglobal for i in ptlist]

        
for i,j in enumerate(vplist):
    movevp( ptend[i] , vplist[i])

    
ori = XYZ(0.10,0.1,0)
for i,j in enumerate(vplist):
    movevp( ori /0.3048, vplist[i])


