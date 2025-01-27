"""
Transfers all Instande Parrameters of Same Category 
except Comment, Mark Parameter.
REbarCover Parameters, which are available when Structural Par is
activated are appended to a list. 
09.01.2020.  
New Idea: Make Transferable Parameter be selelctable. 
Selection-Dialog. 
"""
#! python3
__title__ = "PostableCommand\nText"
__author__ = "Tillmann Baumeister"


from Autodesk.Revit import DB
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
import sys, os
import pickle 
from pyrevit import forms 
from pyrevit.forms import TemplateListItem
from Autodesk.Revit.UI.Selection import ObjectType

import System 
from System.Collections.Generic import List 
import traceback

uidoc = __revit__.ActiveUIDocument 
doc = __revit__.ActiveUIDocument.Document # doc = DocumentManager.Instance.CurrentDBDocument 
uiapp = uidoc.Application


try:
    revitcomid= RevitCommandId.LookupPostableCommandId(PostableCommand.Text)
    if revitcomid:
        uiapp.PostCommand(revitcomid)
        
except:
    forms.alert("Test", ok=True)

    
    
    