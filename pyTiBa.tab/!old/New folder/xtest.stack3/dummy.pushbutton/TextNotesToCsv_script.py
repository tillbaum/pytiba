# -*- coding: utf-8 -*-
"""
Textnotes to CSV file
"""

__title__ = "TxtNotesToCSV"

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

#-----------------------------------------------------------------------
activeView = uidoc.ActiveView

# Get all Textnotes in active View
FECtxtn =FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TextNotes) \
        .WhereElementIsNotElementType() \
        .OwnedByView(activeView.Id) \
        .ToElements()

fectx = [i for i in FECtxtn if i.Name.Contains("Position")]
print fectx.Count 

#list2var(fectx, "t")

prjdir = doc.PathName 
print prjdir      
print os.path.dirname(prjdir)

# remove Non Ascii Chars
def removeNonAscii(s): 
    return "".join(i for i in s if ord(i)<126 and ord(i)>1)

txlist = []
for i in fectx:
    text = i.Text.replace("\r", ", ")
    print text
    if not text.startswith("wie"):  

        #text = removeNonAscii(i.Text)
        txlist.append(text)

# txlist = sorted(txlist)
# for i in txlist:
    # if i.Contains("W01"):
        # int = i.index
        # txtlist.Add(int, "Wände")
    # if i.Contains("B01"):
        # txlist.Add(index, )

    # if i.Contains("S01")
    # if i.Contains("T01")
    # if i.Contains("D01")
    
#[print(i) for i in txlist ]

print txlist

with open(os.path.dirname(prjdir) + "\\textnotes.csv", "w+") as f:
  for i in txlist:
    f.write(i)
    f.write("\n")


