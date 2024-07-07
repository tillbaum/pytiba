"""
Some Textz
"""

import sys
#print(sys.version)

#import win32api

from Autodesk.Revit import DB, UI
#from Autodesk.Revit.UI import 
from Autodesk.Revit.DB import FilledRegion, FilledRegionType, Line, CurveLoop, ElementId, FilteredElementCollector, Transaction, XYZ
from Autodesk.Revit.UI import IExternalEventHandler, ExternalEvent

from Autodesk.Revit.Exceptions import * #InvalidOperationException, OperationCanceledException
from Autodesk.Revit import Exceptions
from Autodesk.Revit.UI.Selection import ObjectType

from System.Collections.Generic import List 
import traceback

import pyrevit
from pyrevit import forms

import os.path as op

uidoc = __revit__.ActiveUIDocument 
doc = __revit__.ActiveUIDocument.Document # doc = DocumentManager.Instance.CurrentDBDocument 
uiapp = __revit__ # is the same as uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application 


__title__ = "OnViewChangeEvent"
__author__ = "EhsanIranejad"
__persistentengine__ = True 

from System import EventHandler, Uri
from Autodesk.Revit.UI.Events import ViewActivatedEventArgs, ViewActivatingEventArgs


def event_handler_function(sender, args):
    forms.alert("test", ok=True)
    __revit__.ViewActivating -= EventHandler[ViewActivatingEventArgs](event_handler_function)
    # unsubscriping from the ViewActivatedEvent WORKS !! 12.06.2021


# I'm using ViewActivating event here as example.
# The handler function will be executed every time a Revit view is activated:
__revit__.ViewActivating += EventHandler[ViewActivatingEventArgs](event_handler_function)


