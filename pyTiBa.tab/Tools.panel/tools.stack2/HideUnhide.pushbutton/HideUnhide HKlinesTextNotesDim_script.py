""" Hide Hilfskonstruktion objects: 
	HK TextNotes, 
	HK Dimensions, 
	HK Linetyle"""

__title__ = "Hide/Unhide \nHelpConstruction" 
	
__author__ = "TBaumeister" 	

import clr # import common language runtime .Net Laufzeitumgebung fuer .Net-anwendungen. / um auf .Net Anwendungen

from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, View # don't need to import that
from System.Collections.Generic import List 


import sys
pyt_path = (r'C:\Program Files (x86)\IronPython 2.7\Lib')
sys.path.append(pyt_path) 

doc = __revit__.ActiveUIDocument.Document

#######  FILTERED ELEMENT COLLECTOR  #####################################################

# --- create Instance of FEC, Collect all OST_Lines 
alllines = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Lines).ToElements()
# Filter for Name: "HK" (Hilfskonstruktion)  : list comprehension
hklines = [x for x in alllines if x.LineStyle.Name == "HK" ] 

# --- FEC for Text -----------------------------------------
txtcol = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TextNotes).ToElements()
hktxt = [x for x in txtcol if x.Name.Contains("HK")]

# FEC Dimension witch contains "HK" string  -----------------------------------
dimcol = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Dimensions).ToElements()
hkdim = [x for x in dimcol if x.Name.Contains("HK")]

#----- FilteredElementCollector of Views , Create Instance of FEC, ----------------------------
viewcol = FilteredElementCollector(doc).OfClass(View).ToElements() 

viewlist = []
for view in viewcol:
	if view.ViewType == ViewType.ThreeD:
		if not(view.IsTemplate): # make sure that view is not a Template-view, 3D views can be TemplateViews???, didn't know that
			viewlist.append(view)
	else:
		viewlist.append(view)
# ---End View Collector -------------------------------------------


# -- FUNCTIONS  from Konrad in Dynamo ---------------------------------------
# I don'T understand these functions fully! See StackOverflow entry, question answerd by Konrad

def ProcessList(_func, _list):
    return map( lambda x: ProcessList(_func, x) if type(x) == list else _func(x), _list )

def ProcessListArg(_func, _list, _arg): #_func: underscore has no special meaning in args of func 
    return map( lambda x: ProcessListArg(_func, x, _arg) if type(x) == list else _func(x, _arg), _list )

# Func Hide Elements 
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

# # Tests --------------------------------------------------------
# v13= viewlist[13]
# tx1=hktxt[0]

# print("v13= ", v13.Name)
# print("tx1= ", tx1.Name)
# print("-----------------------")

# put all objects in one list:  hklines + hkdim + hktxt
hktxt += hklines + hkdim

try:
	errorReport = None
	# create a instance of Transaction class , start instance with start() method
	t = Transaction(doc, "Hide, Unhide Elements")
	t.Start()
	ProcessListArg(HideUnhideEl, viewlist, hktxt)
	t.Commit() 
except:
	# if error accurs anywhere in the process catch it
	t.Rollback()
	import traceback
	errorReport = traceback.format_exc()
	print(errorReport)



