"""

09.01.2020.  
New Idea: Make Transferable Parameter be selelctable. 
Selection-Dialog. 
"""
#! python3
__title__ = "PromptFor\nFamilyPlacement"
__author__ = "Tillmann Baumeister"


from Autodesk.Revit import DB
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
import sys, os
import pickle 
from pyrevit import forms 
from pyrevit.forms import TemplateListItem
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.Exceptions import OperationCanceledException
from Autodesk.Revit import Exceptions

import System 
from System.Collections.Generic import List 
import traceback

uidoc = __revit__.ActiveUIDocument 
doc = __revit__.ActiveUIDocument.Document # doc = DocumentManager.Instance.CurrentDBDocument 
uiapp = uidoc.Application

frt = FilteredElementCollector(doc).OfClass(FilledRegionType).ToElements()
sym = FilteredElementCollector(doc).OfClass(FamilySymbol).ToElements()


genmod = sorted( FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_GenericModel) \
                         .WhereElementIsElementType().ToElements(), 
                key = lambda x: x.FamilyName )

#frt = FilteredElementCollector(doc).OfClass(FilledRegion).WhereElementIsNotElementType().ToElements()

try:
    uidoc.PromptForFamilyInstancePlacement(genmod[1])
except Exceptions.OperationCanceledException: # This Exception is needed for PromptForFamilyInstancePlacement Symbol. 
    import traceback
    forms.alert(str(traceback.format_exc()), ok=True)
    #print traceback.format_exc()

    
    