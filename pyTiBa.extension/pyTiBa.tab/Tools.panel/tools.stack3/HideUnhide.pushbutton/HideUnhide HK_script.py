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

__title__ = "Hide/Unhide \nHelpConstruction" 
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

hktxt.UnionWith(hkdim).UnionWith(hklines)
hktxt = hktxt.ToElements()


#----- FilteredElementCollector of Views  ----------------------------
FECviews2 = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views) \
                .WhereElementIsNotElementType() 
         #       .Where(lambda x: x.CanBePrinted)
# A Listcomp doesn't cost much performance wise compared to .Where()
viewlist = [i for i in FECviews2 if i.CanBePrinted]


# PRJ Schlossstrasse, only 20 Views left 
# script run time 1.360 sec. former runtime: ca 4 sec.

viewlist= list(FECviews2)


# Func HideUnhide Elements 
def HideUnhideEl(view, elements):
    ids = List[ElementId]()  # .NET List 
    ids2 =List[ElementId]()  # .NET List  
    for i in elements: 
        if not i.IsHidden(view) and i.CanBeHidden(view): 
            ids.Add(i.Id) 
        elif i.IsHidden(view): 
            ids2.Add(i.Id)
    if not elements[0].IsHidden(view): 
        view.HideElements(ids) 
    else:
        view.UnhideElements(ids2) 
    return None

t = Transaction(doc, "Hide, Unhide Elements")
try:
    t.Start()
    [HideUnhideEl(i, hktxt) for i in viewlist]
    #ProcessListArg(HideUnhideEl, viewlist, hktxt)
    t.Commit() 
except:
    t.RollBack()
    import traceback
    print traceback.format_exc()


# for timing -------------------------------------------------------------------
# endtime = timer.get_time()
# print(endtime)



# OLD FEC
# FECviews = FilteredElementCollector(doc).OfClass(View) \ #OfCategory(BultInCategory.OST_Views)
                # .WhereElementIsNotElementType().ToElements()
# print len(FECviews)

# ==> THIS has less views in it  !!! only OfCategory has only 44 vvies. ofClass has 68.


#array = ViewType.GetValues(ViewType) # Gets all objects in Enumeration, that you can iterate over it! 
# vt= ViewType
# arraylist = {vt.FloorPlan, vt.CeilingPlan, vt.Elevation, vt.ThreeD, vt.DrawingSheet, vt.DraftingView,
                # vt.Legend, vt.EngineeringPlan, vt.AreaPlan, vt.Section, vt.Detail}
# viewlist =[i for i in FECviews if not i.IsTemplate and i.ViewType in arraylist]

# vt= ViewType
# arraylist = {vt.FloorPlan, vt.CeilingPlan, vt.Elevation, vt.ThreeD, vt.DrawingSheet, vt.DraftingView,
                # vt.Legend, vt.EngineeringPlan, vt.AreaPlan, vt.Section, vt.Detail}
# ----- FilteredElementCollector of Views , Create Instance of FEC, ----------------------------

# FECviews = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views) \
                # .WhereElementIsNotElementType() \
                # .Where(lambda x: not x.IsTemplate  and x.ViewType in arraylist)
#print len(list(FECviews))
# 20



# -- FUNCTIONS  from Konrad in Dynamo ---------------------------------------
# See StackOverflow entry, question answerd by Konrad
# def ProcessList(_func, _list):
    # return map( lambda x: ProcessList(_func, x) if isinstance(x, list) else _func(x), _list )

# def ProcessListArg(_func, _list, _arg): #_func: underscore has no special meaning in args of func 
    # return map( lambda x: ProcessListArg(_func, x, _arg) if isinstance(x, list) else _func(x, _arg), _list )

# Func Hide Elements 
# def HideEl(view, elements):
	# ids = List[ElementId]()  # .NET List 
	# for i in elements:
		# if not i.IsHidden(view) and i.CanBeHidden(view):
			# ids.Add(i.Id)
	# view.HideElements(ids)
	# return None
	
# def UnhideEl(view, elements):
	# ids = List[ElementId]()  # .NET List 
	# for i in elements:
		# if i.IsHidden(view):
			# ids.Add(i.Id)
	# view.UnhideElements(ids)
	# return None