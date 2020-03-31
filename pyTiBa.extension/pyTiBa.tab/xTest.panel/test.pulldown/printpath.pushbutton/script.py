"""
Transfers all I
"""
__title__ = "printpath"
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


print os.path.dirname(__file__)

#print os.path.join(os.getcwd(), os.listdir(os.getcwd() )[0]

print os.path.dirname(os.path.dirname(__file__)) + "\\dlgvalues" 


print "__file__: {}".format(__file__) 

print "__name__ :{}".format(__name__)

scriptDir = os.path.dirname(os.path.realpath(__file__))

print scriptDir