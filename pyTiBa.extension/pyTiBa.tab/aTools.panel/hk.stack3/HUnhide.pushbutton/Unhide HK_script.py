"""
Hide Hilfskonstruktion objects: 
identified by "HK" in their name, 
HK Notes, 
HK Dimensions, 
HK Linestyle
 29.08.2018 optimized for perfomance 
"""

# for timing -------------------------------------------------------------------
from pyrevit.coreutils import Timer
timer = Timer()

__title__ = "Unhide \nHelpConstruction" 
__author__ = "TBaumeister" 	

import clr  
import System
from System.Collections.Generic import List 

clr.AddReference('System.Linq')
# Import previously referenced C# libraries like first-class Python modules
clr.ImportExtensions(System.Linq) 
# Import LINQ extension methods (to enable "fluent syntax")
import System.Linq


from Autodesk.Revit.DB import * # Transaction, FilteredElementCollector, BuiltInCategory, View, ViewType # don't need to import that
from System.Collections.Generic import List 
import sys
pyt_path = (r'C:\Program Files (x86)\IronPython 2.7\Lib')
sys.path.append(pyt_path) 

doc = __revit__.ActiveUIDocument.Document

#######  FILTERED ELEMENT COLLECTOR  #####################################################

# --- FEC lines, Collect all OST_Lines 
# BUILDING_CURVE_GSTYLE
paraValProvider = ParameterValueProvider(ElementId(BuiltInParameter.BUILDING_CURVE_GSTYLE_PLUS_INVISIBLE))
rule = FilterStringRule(paraValProvider, FilterStringContains(), "HK", True); # True -> CaseSensitivity
elemParaFilter = ElementParameterFilter(rule)

hklines = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Lines) \
                .WherePasses(elemParaFilter) \

# FEC Dimension witch contains "HK" string  -----------------------------------
#ELEM_TYPE_PARAM
paraValProvider = ParameterValueProvider(ElementId(BuiltInParameter.ELEM_TYPE_PARAM))
rule = FilterStringRule(paraValProvider, FilterStringContains(), "HK", True); # True -> CaseSensitivity
elemParaFilter = ElementParameterFilter(rule)

hkdim = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Dimensions) \
                .WherePasses(elemParaFilter) \

# --- FEC for Text -----------------------------------------
#ELEM_TYPE_PARAM
paraValProvider = ParameterValueProvider(ElementId(BuiltInParameter.ELEM_TYPE_PARAM))
rule =            FilterStringRule(paraValProvider, FilterStringContains(), "HK", True); # True -> CaseSensitivity
elemParaFilter =  ElementParameterFilter(rule)

hktxt = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TextNotes) \
                .WherePasses(elemParaFilter) \


# Collect spotSlopes, SpotElevations, Spotcoordinate symbols-------------------------------------------------------------------------------------
hkspotslope = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_SpotSlopes) \
                .WherePasses(elemParaFilter) \

hkspotelevation = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_SpotElevations) \
                .WherePasses(elemParaFilter) \

hkspotcoord = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_SpotCoordinates) \
                .WherePasses(elemParaFilter) \

# Collect AnnotationSymbols which contain "HK"
genann = FilteredElementCollector(doc).OfClass(FamilyInstance) \
          .ToElements()

anno=[]
for i in genann: 
    if i.GetType().Equals(AnnotationSymbol) and i.Name.Contains("HK"):
        anno.append(i)


hktxt.UnionWith(hkdim).UnionWith(hklines) \
        .UnionWith(hkspotslope).UnionWith(hkspotcoord)
hktxt = hktxt.ToElements()

hidelist = list(hktxt)
hidelist += anno


FECviews2 = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views) \
                .WhereElementIsNotElementType() \
                .ToElements()
         #       .Where(lambda x: x.CanBePrinted)

# A Listcomp doesn't cost much performance wise compared to .Where()
viewlist = [i for i in FECviews2 if i.CanBePrinted]
# print len(viewlist)


FECsheets = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets) \
                .WhereElementIsNotElementType().ToElements()
         #       .Where(lambda x: x.CanBePrinted)

viewlist += list(FECsheets)

# PRJ Schlossstrasse, only 20 Views left 
# script run time 1.360 sec. former runtime: ca 4 sec.




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
      UnhideEl(v, hidelist)
    except: pass
t.Commit() 


# for timing -------------------------------------------------------------------
# endtime = timer.get_time()
# print(endtime)

