# -*- coding: utf-8 -*-
"""
Replace Chars in Textnotes
"""

__title__ = "Replace Chars in TN"
__author__ = "Tillmann Baumeister"

import clr
from Autodesk.Revit.DB import *
from Autodesk.Revit import DB
import System 
#from System.Collections.Generic import List

import sys, os
from rpw.ui.forms import TaskDialog 
from pyrevit import forms 

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument 
uiapp = __revit__ # is the same as uiapp = DocumentManager.Instance.CurrentUIApplication
# returns:  <Autodesk.Revit.UI.UIApplication object at 0x0000000000000171 [Autodesk.Revit.UI.UIApplication]>
app = uiapp.Application

activeView = uidoc.ActiveView

# Get all Textnotes in active View
FECtxtn =FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TextNotes) \
        .WhereElementIsNotElementType() \
        .OwnedByView(activeView.Id) \
        .ToElements()

fectx = [i for i in FECtxtn if i.Name.Contains("Position")]
print fectx.Count, 

#list2var(fectx, "t")

prjdir = doc.PathName 
print prjdir      
print os.path.dirname(prjdir)
print "------------------------------------------------"


# remove Non Ascii Chars
def removeNonAscii(s): 
    return "".join(i for i in s if ord(i)<126 and ord(i)>1)

t = Transaction(doc, "test")
t.Start()
    
txlist = []
for i in fectx:
    repl = i.Text.replace("4", "1", 1) # nicht optimal!
    print(i.Text, "-->", repl) 
    i.Text = repl
    
t.Commit()
print "done"


# print "--------------------"
# txlist = sorted(txlist)
# print txlist


# with open(os.path.dirname(prjdir) + "\\textnotes.csv", "w+") as f:
  # for i in txlist:
    # f.write(i)
    # f.write("\n")


