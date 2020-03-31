"""
STart Wall Command with selected walltype 
The Goal:
Make a dialog with line buttons to pick one from. 

"""
#! python3
__author__ = "Tillmann Baumeister"

from Autodesk.Revit.DB import * #(FilteredElementCollector, Transaction,
                                #   BuiltInParameter, Level, ElementId )
from Autodesk.Revit import DB
from Autodesk.Revit.UI import (RevitCommandId, PostableCommand)

import sys, os
from pyrevit import forms 
from Autodesk.Revit.UI.Selection import ObjectType

import System 
from System.Collections.Generic import List 


uidoc = __revit__.ActiveUIDocument 
doc = __revit__.ActiveUIDocument.Document # doc = DocumentManager.Instance.CurrentDBDocument 
uiapp = __revit__ # is the same as uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application 


def GetFirstWallTypeNamed(doc, name):
    bip = DB.BuiltInParameter.SYMBOL_NAME_PARAM
    provider = DB.ParameterValueProvider(ElementId(bip))
    evaluator = DB.FilterStringEquals()
    rule = DB.FilterStringRule(provider, evaluator, name, False)
    filter = DB.ElementParameterFilter( rule )

    fec = FilteredElementCollector( doc).OfClass(DB.WallType) \
          .WherePasses(filter) \
          .FirstElement()
    return fec


def GetFirstWallUsingType(doc, walltype):
    bip = DB.BuiltInParameter.ELEM_TYPE_PARAM
    provider = DB.ParameterValueProvider(ElementId( bip ))
    evaluator = DB.FilterNumericEquals()
    rule = DB.FilterElementIdRule(provider, evaluator, walltype.Id )
    filter = DB.ElementParameterFilter( rule )

    fec = DB.FilteredElementCollector(doc).OfClass(Wall) \
          .WherePasses( filter ) \
          .FirstElement()
    return fec
    
    
def createobj(typename):    

    wallType = GetFirstWallTypeNamed(doc, wallTypeName)
    wall = GetFirstWallUsingType(doc, wallType)
       
    if not wall:     
        line = DB.Line.CreateBound(XYZ.Zero, XYZ(2, 0, 0))

        feclevel = FilteredElementCollector(doc).OfClass(Level).FirstElement()  # Level1

        t= Transaction(doc, "Create dummy Wall")
        t.Start()
        # wall.Create(doc, IList(Curve),walltypeId, levelId, bool structural, XYZ normal)
                    #(doc, Curve, wallTypeId, LevelId,height double, offset double, flip bool, struc bools)
                    #(doc, IList(curve), walltypId, levelId, structural bool)
        height = 2* 3.048
        wall = Wall.Create( doc, line, wallType.Id, feclevel.Id, height, 0.0, False, False )
        t.Commit()

    if wall:
        # Select it/Add it to Selection
        listId = List[ElementId]()
        listId.Add(wall.Id)
        # wall gets selected! 
        uidoc.Selection.SetElementIds(listId) 
     
    # Start CreateSimilar Command. 
    try:
        revitcomid= RevitCommandId.LookupPostableCommandId(PostableCommand.CreateSimilar)
        if revitcomid: uiapp.PostCommand(revitcomid)       
    except:
        import traceback
        print traceback.format_exc()
        #forms.alert("Exceptionn", ok=True)

    
wallTypeName = "Generic - 150mm"

createobj(wallTypeName)
 
 
 