"""
Copyright (c) 2020 Tillmann Baumeister
Python scripts for Autodesk Revit 
"""
#! python3

from Autodesk.Revit import DB, UI
#from Autodesk.Revit.UI import 
from Autodesk.Revit.DB import FilledRegion, FilledRegionType, Line, CurveLoop, ElementId, FilteredElementCollector, Transaction, XYZ
from Autodesk.Revit.UI import IExternalEventHandler, ExternalEvent

from Autodesk.Revit.Exceptions import * #InvalidOperationException, OperationCanceledException
from Autodesk.Revit import Exceptions
from Autodesk.Revit.UI.Selection import ObjectType

import sys
from System.Collections.Generic import List 
import traceback
from pyrevit import framework
from pyrevit.forms import WPFWindow
from pyrevit import framework
from pyrevit.framework import System 
from pyrevit.framework import Threading 
from pyrevit.framework import Interop 
from pyrevit.framework import Input 
from pyrevit.framework import wpf, Forms, Controls, Media 
from pyrevit.framework import CPDialogs 
from pyrevit.framework import ComponentModel 
from pyrevit import forms

import os.path as op

uidoc = __revit__.ActiveUIDocument 
doc = __revit__.ActiveUIDocument.Document # doc = DocumentManager.Instance.CurrentDBDocument 
uiapp = __revit__ # is the same as uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application 


__doc__ = "Palette GenericModel"
__title__ = "Palette_SelecFromList" 
__author__ = "Tillmann Baumeister"
__persistentengine__ = True



class FilterOption(forms.TemplateListItem):
    
   @property
   def name(self):
        return '{}'.format(self.item.Name)
  


fec = FilteredElementCollector(doc).OfClass(DB.FilterElement).ToElements()

fecfilter = FilteredElementCollector(doc).OfClass(DB.FilterElement).ToElements()
ops = sorted([FilterOption(x) for x in fecfilter], key= lambda x: x.name)
res = forms.SelectFromList.show(ops,
                     multiselect=True,
                     button_name='Select Item')

print res
t = Transaction(doc, "hello")
t.Start()

[doc.ActiveView.AddFilter(i.Id) for i in res]
t.Commit()



