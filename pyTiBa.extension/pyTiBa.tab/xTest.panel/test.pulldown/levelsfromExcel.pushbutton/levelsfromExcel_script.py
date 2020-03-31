"""
Copyright (c) 2017 Cyril Waechter
Python scripts for Autodesk Revit
This file is part of pypevitmep repository at https://github.com/CyrilWaechter/pypevitmep
pypevitmep is an extension for pyRevit. It contain free set of scripts for Autodesk Revit:
you can redistribute it and/or modify it under the terms of the GNU General Public License
version 3, as published by the Free Software Foundation.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
See this link for a copy of the GNU General Public License protecting this package.
https://github.com/CyrilWaechter/pypevitmep/blob/master/LICENSE
"""
#! python3


from Autodesk.Revit import DB, UI
#from Autodesk.Revit.UI import 
from Autodesk.Revit.DB import ElementId, FilteredElementCollector, Transaction, TextNote, XYZ

from Autodesk.Revit.Exceptions import InvalidOperationException
from Autodesk.Revit.UI.Selection import ObjectType

from Autodesk.Revit.UI import IExternalEventHandler, ExternalEvent
from Autodesk.Revit import UI, DB
from Autodesk.Revit.DB import Transaction
import os, sys
from Autodesk.Revit.Exceptions import InvalidOperationException
import rpw
import subprocess 
import pyrevit
from pyrevit import forms
import importlib
import System 
from System.Collections.Generic import List 
import traceback  
from pyrevit.loader.sessionmgr import *


from pyrevit.forms import WPFWindow


#for i in dir(importlib): print(i)

from pyrevit.forms import WPFWindow
doc = rpw.revit.doc
uidoc = rpw.revit.uidoc

__doc__ = "A simple modeless form sample"
__title__ = "Modeless Form"
__author__ = "Cyril Waechter"
__persistentengine__ = True

# print os.path.dirname(__file__) + "\\TextModeless_script.py"

cmd = find_pyrevitcmd("pytibadev-pytibadev-atools-detail-modelessformlines")  
command_instance= cmd()
command_instance.Execute(create_tmp_commanddata(),'',DB.ElementSet()) #Execute Method from  UI.IExternelCommand Method




