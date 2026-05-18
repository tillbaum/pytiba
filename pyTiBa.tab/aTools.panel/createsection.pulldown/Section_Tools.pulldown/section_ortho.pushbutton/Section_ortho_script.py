# -*- coding: utf-8 -*-
"""
Section on LInes (Detail, Model)
"""

__doc__ = """
create Section ortho to DetailLine

 """

__title__ = "Section ortho Line"

__author__ = "Tillmann Baumeister"

from Autodesk.Revit.DB import *
import System 
from System.Collections.Generic import * 
from System.Runtime.InteropServices import Marshal 
import sys
from rpw.ui.forms import TaskDialog 
from pyrevit import forms 

doc = __revit__.ActiveUIDocument.Document
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

    #BoundingBox Wall 
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

    #Set 2pt Min & Max to define BoundaryBox of Section
    minpt = XYZ( -width/2.0, minZ - offset, - depth /2.0 ) #from midpoint of wall. X = wall-length /2  
    maxpt = XYZ(  width/2.0, maxZ + offset, depth + offset)

    midpoint = p1 + 0.5 * v # midpoint of whole wall startpt.X + 0.5 * v.X
    walldir = v.Normalize() # X/ Length, Y/ Length , Z/ Length 
    updir = XYZ.BasisZ      # Basisvektor in Z Richtung (0,0,1)
    viewdir = walldir.CrossProduct( updir ) #  XYZ(0, 1, 0) 

    #set transform of SectionBox 
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


def boundingboxLine(elem):
    # Location Line of Wall
    line = elem.Location.Curve # Everything is a Curve, in Revit
    p1 = line.GetEndPoint(0)
    p2 = line.GetEndPoint(1)
    v = p2 - p1 # vector 

    width = v.GetLength()   #  sqrt(x*x + y*y + z*s)
    height =  4 / 0.3048    # 4m height calculation 1 ft = 0.3048 m ; 1m = 1/0.3048 ft ≈ 3.28..
    offset = 0.5 / 0.3048   #

    #Set 2pt Min & Max to define BoundaryBox of Section
    minpt = XYZ( -width/2.0, -offset , 0) #from midpoint of wall. X = wall-length /2  
    maxpt = XYZ(  width/2.0, height + offset , offset)

    midpoint = p1 + 0.5 * v # midpoint of whole wall startpt.X + 0.5 * v.X
    walldir = v.Normalize() # X/ Length, Y/ Length , Z/ Length 
    updir = XYZ.BasisZ      # Basisvektor in Z Richtung (0,0,1)
    viewdir = walldir.CrossProduct( updir ) #  

    #set transform of SectionBox 
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


def createSection(sectionBox, name_str= None):
    #get ViewFamilyType.Section
    FECvft = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()    
    vftsection = [i for i in FECvft if i.ViewFamily == ViewFamily.Section][0]
    print vftsection
    try:
        t = Transaction(doc, name_str)
        t.Start()
        section = ViewSection.CreateSection(doc, vftsection.Id, sectionBox)
        print "create section ok"
        if name_str:
            section.Name = name_str
        t.Commit()
        return True
    except:
        t.RollBack()
        print "--> Error"
        import traceback
        print(traceback.format_exc())
        return False

# Select Detail-, or Model-Lines
dlinelist = [i for i in selection if i.Category.Name.Equals("Lines")]
print dlinelist

if not dlinelist:
    print " --> No DetailLines selected, exiting"
    import sys
    sys.exit()

for i, j in enumerate(dlinelist):
    #boundingboxDetailLine(i)
    print "\n --> " ,i, j
    namestr = "Section_{}_DLine".format(i)
    print namestr
    bb = boundingboxLine(j)
    print bb
    createSection(bb, namestr)





