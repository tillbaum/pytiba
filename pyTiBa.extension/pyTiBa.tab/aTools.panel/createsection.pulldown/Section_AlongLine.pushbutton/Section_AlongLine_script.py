# -*- coding: utf-8 -*-
"""
Create sections along to Lines (Detail, Model)
section Viewdirection is right to line Direction
"""

__title__ = "Section Along Line"

__author__ = "Tillmann Baumeister"

import clr
from Autodesk.Revit.DB import *
from Autodesk.Revit import DB
import System 
#from System.Collections.Generic import List
import sys
from rpw.ui.forms import TaskDialog 
from pyrevit import forms 

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument 
uiapp = __revit__ # is the same as uiapp = DocumentManager.Instance.CurrentUIApplication
# returns:  <Autodesk.Revit.UI.UIApplication object at 0x0000000000000171 [Autodesk.Revit.UI.UIApplication]>
app = uiapp.Application


#wall = [i for i in selection if i.GetType().Name.Equals("Wall") else None][0] 

#get BoundingBox of wall
def boundingboxWall(elem):
    # Location Line of Wall
    line = elem.Location.Curve # Everything is a Curve, in Revit
    p1 = line.GetEndPoint(0)
    p2 = line.GetEndPoint(1)
    v = p2 - p1 # vector 

    # BoundingBox Wall 
    bbwall = elem.get_BoundingBox(None)
    minZ = bbwall.Min.Z
    maxZ = bbwall.Max.Z 
    # print "MIN= ", bbwall.Min
    # print "MAX= ", bbwall.Max
    # print p1 
    # print p2

    width = v.GetLength()   #  sqrt(x*x + y*y + z*s)
    height = maxZ- minZ     # height calculation 
    depth = elem.Width
    offset = 0.2 / 0.3048   #

    # Set 2pt Min & Max to define BoundaryBox of Section
    minpt = XYZ( -width/2.0, minZ - offset, - depth /2.0 ) #from midpoint of wall. X = wall-length /2  
    maxpt = XYZ(  width/2.0, maxZ + offset, depth + offset)

    midpoint = p1 + 0.5 * v # midpoint of whole wall startpt.X + 0.5 * v.X
    walldir = v.Normalize() # X/ Length, Y/ Length , Z/ Length 
    updir = XYZ.BasisZ      # Basisvektor in Z Richtung (0,0,1)
    viewdir = walldir.CrossProduct( updir ) #  XYZ(0, 1, 0) 

    # set transform of SectionBox 
    trans = DB.Transform.Identity #  .Identity has to be called to 
    trans.Origin = midpoint
    trans.BasisX = walldir
    trans.BasisY = updir 
    trans.BasisZ = viewdir  

    # create SectionBox
    sectionBox = DB.BoundingBoxXYZ() # instantiate 
    sectionBox.Transform = trans 
    sectionBox.Min = minpt 
    sectionBox.Max = maxpt
    return sectionBox


#elem = selection[0]

def boundingboxLine(elem):
    # Location Line of Wall
    line = elem.Location.Curve # Every 2D line geometrie is a Curve, in Revit
    p1old = line.GetEndPoint(0)
    p1 = XYZ(p1old.X,p1old.Y, 0)
    
    p2old = line.GetEndPoint(1)
    p2 = XYZ(p2old.X, p2old.Y, 0)
    v = p2 - p1 # vector 

    # define Section Box 
    length = v.GetLength()   #  sqrt(x*x + y*y + z*z)
    height =  4 / 0.3048    # 4m height calculation 1 ft = 0.3048 m ; 1m = 1/0.3048 ft ≈ 3.28..
    offset = 0.5 / 0.3048   #
    minZ = min(p1old.Z, p2old.Z)

    #Set 2pts, to define BoundaryBox of Section: Min (lower-left-back)& Max (upper-right-front),
    minpt = XYZ( -length/2.0, minZ -offset , 0) #from midpoint of wall. X = wall-length /2  
    maxpt = XYZ(  length/2.0, height + offset , offset)
    midpoint = p1 + 0.5 * v # midpoint of Line startpt.X + 0.5 * v.X

    walldir = v.Normalize() # X/ Length, Y/ Length , Z/ Length 
    updir = XYZ.BasisZ      # Basisvektor in Z Richtung (0,0,1)
    viewdir = walldir.CrossProduct( updir ) #  !!!!------------------------

    #set transform of SectionBox 
    trans = DB.Transform.Identity   #Identity has to be called to
    trans.Origin = midpoint
    trans.BasisX = walldir
    trans.BasisY = updir 
    trans.BasisZ = viewdir 

    # create SectionBox
    sectionBox = DB.BoundingBoxXYZ() # instantiate 
    sectionBox.Transform = trans
    sectionBox.Min = minpt
    sectionBox.Max = maxpt
    return sectionBox

# get % set ViewProperties Active View/ SectiontView
def viewPropertiesTransfer(section):
    #get current active View
    activeview = uidoc.ActiveView
    section.Scale = activeview.Scale
    section.DisplayStyle = activeview.DisplayStyle
    section.DetailLevel = activeview.DetailLevel
    # Turn off categories: Levels, Sections, Grids
    catlevel = DB.Category.GetCategory(doc, BuiltInCategory.OST_Levels)
    catsection = DB.Category.GetCategory(doc, BuiltInCategory.OST_Sections)
    catgrids = DB.Category.GetCategory(doc, BuiltInCategory.OST_Grids)
    # Hide categories in View, necessary for Viewport Creation and placement
    section.SetCategoryHidden(catlevel.Id, True)
    section.SetCategoryHidden(catsection.Id, True)
    section.SetCategoryHidden(catgrids.Id, True)
    return True

def createSections():
    #get ViewFamilyType.Section: vft
    FECvft = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()    
    vftsection = [i for i in FECvft if i.ViewFamily == ViewFamily.Section][0]
    
    # create namestr
    FECsection =FilteredElementCollector(doc).OfClass(ViewSection).ToElements()
    secnames = {i.Name[0:4] for i in FECsection} #set 
    abc = list("ABCDEFHKIJKLMNOPQRSTUVWXYZabcdefghijklmnop")
    k = 0
    namestr = "Sec{}".format(abc[k])
    while namestr in secnames:
        k += 1
        namestr = "Sec{}".format(abc[k])
    #Create 
    mess=[]
    t = Transaction(doc, namestr)
    t.Start()
    try:
        for i, j in enumerate(linelist):
            namestr = "Sec{}_{}_Line".format(abc[k], i)
            mess.append(namestr)
            bb = boundingboxLine(j)# function 
            section = ViewSection.CreateSection(doc, vftsection.Id, bb)
            # get ActiveView Properties and transfer them to sectionView
            viewPropertiesTransfer(section)
            mess.append(" --> create Section")
            if namestr:
                section.Name = namestr
        t.Commit()
        return mess
    except:
        t.RollBack()
        t.Dispose()
        print " --> Error"
        import traceback
        print(traceback.format_exc())


# Select Detail-, or Model-Lines
selection = [doc.GetElement(elId) for elId in uidoc.Selection.GetElementIds() ]
linelist = [i for i in selection if i.Category.Name.Equals("Lines")] #Filter out everything else
#linelist is sorted after selection. 

if not linelist:
    print " --> No DetailLines selected, --> exiting"
    import sys
    sys.exit()

#sort after X coordinate of startpoint = (EndPoint(0))
#linesorted = sorted(linelist, key = lambda x: x.Location.Curve.GetEndPoint(0).X )
#linesorted = sorted(linesorted, key = lambda x: x.Location.Curve.GetEndPoint(0).Y )

run = createSections()
#for i in run: print i



