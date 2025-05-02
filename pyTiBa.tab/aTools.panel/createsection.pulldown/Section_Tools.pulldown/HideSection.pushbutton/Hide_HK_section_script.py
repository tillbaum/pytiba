"""
Hide Section-Lines 
identified by Instance Parameter "HK" 
16.08.2019
"""

# for timing -------------------------------------------------------------------
from pyrevit.coreutils import Timer
timer = Timer()

__title__ = "Hide \nSectionLine" 
__author__ = "TBaumeister" 	

import clr  
import System 
from System.Collections.Generic import List  

clr.AddReference('System.Linq')   
# Import previously referenced C# libraries like first-class Python modules
clr.ImportExtensions(System.Linq) 
# Import LINQ extension methods (to enable "fluent syntax")
import System.Linq 


from Autodesk.Revit.DB import Transaction, FilteredElementCollector, BuiltInCategory, View, ViewType, ElementId # don't need to import that

import sys
pyt_path = (r'C:\Program Files (x86)\IronPython 2.7\Lib')
sys.path.append(pyt_path) 

doc = __revit__.ActiveUIDocument.Document

# FEC HK section line -> category: Ost_Viewers-------------------------------------------
viewers = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Viewers) \
                .WhereElementIsNotElementType() \
                .ToElements()

sectionlines = []
for i in viewers:
    p= i.LookupParameter("HK")
    if p and p.AsInteger().Equals(1):
        sectionlines.append(i)

hidelist = sectionlines

FECviews= FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views) \
                .WhereElementIsNotElementType() \
                .ToElements()

viewlist = [i for i in FECviews if i.CanBePrinted]

FECsheets = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets) \
                .WhereElementIsNotElementType().ToElements()

viewlist += list(FECsheets)

def HideEl(view, elements): 
    ids = List[ElementId]()  # .NET List
    for i in elements:
        if not i.IsHidden(view) and i.CanBeHidden(view):
            ids.Add(i.Id)
    view.HideElements(ids)
    return None


def UnhideEl(view, elements):
    ids = List[ElementId]()  # .NET List
    for i in elements:
        if i.IsHidden(view):
            ids.Add(i.Id)
    view.UnhideElements(ids)
    return None

import traceback
t = Transaction(doc, "Hide/Unhide Elements")
t.Start()
for v in viewlist:
    try:
      HideEl(v, hidelist)
    except: pass #print traceback.format_exc()

t.Commit() 





# for timing -------------------------------------------------------------------
# endtime = timer.get_time()
# print(endtime)


