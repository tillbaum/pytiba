# -*- coding: utf-8 -*-
'''
Arrange Viewports on SheetView
Select Viewports, run tool
'''

__title__ = "Arrange_ViewPorts"

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

path = os.path.split(sys.argv[0])[0]
print path


with open(path + "\\onezero.txt", "a+") as f:
    f.seek(0) ;a = f.read()
    if not a:
        a = "0" 
        f.write(a) # set default value


selection = [doc.GetElement(elId) for elId in uidoc.Selection.GetElementIds() ]
if not selection:
    sys.exit()

if a == "1":
    vplist = list(reversed(selection))
elif a == "0":
    vplist = selection

# vp_names = [doc.GetElement(vp.ViewId).Name for vp in vplist]
# print vp_names
secviewlist = [doc.GetElement(vp.ViewId) for vp in vplist]
print " ViewNames --------------------------------"
for i in secviewlist: print i.Name

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
    ptcenter = viewport.GetBoxCenter()      # The distance between CropBox and BoxOutline is 
    vecToNewCenter = pt1 - ptcenter         # 1 foot in x & y direction, see test_script
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

ptglobal = XYZ(-0.5 , 0.1 , 0) / 0.3048
ptend = [i + ptglobal for i in ptlist]

for i,j in enumerate(vplist):
    movevp( ptend[i] , vplist[i])
print "--> Done"
    
# write a = 1 or a=1  to file
with open(path + "\\onezero.txt", "w") as f:
    if a == "0":
        a = "1"
    elif a == "1":
        a = "0"
    f.write(a)


# ori = XYZ(0.10,0.1,0)
# for i,j in enumerate(vplist):
    # movevp( ori /0.3048, vplist[i])
