"""
Hide Hilfskonstruktion objects: 
identified by "HK" letter in their TypeName, 
HK Notes, 
HK Dimensions, 
HK Linestyle
"""

# for timing -------------------------------------------------------------------
from pyrevit.coreutils import Timer
timer = Timer()



__title__ = "Hide/Unhide \nHelpConstruction" 

__author__ = "TBaumeister" 	

import clr # import common language runtime .Net Laufzeitumgebung fuer .Net-anwendungen. / um auf .Net Anwendungen

from Autodesk.Revit.DB import * # Transaction, FilteredElementCollector, BuiltInCategory, View, ViewType # don't need to import that
from Autodesk.Revit import DB

from System.Collections.Generic import List 
import sys
pyt_path = (r'C:\Program Files (x86)\IronPython 2.7\Lib')
sys.path.append(pyt_path) 

doc = __revit__.ActiveUIDocument.Document

#######  FILTERED ELEMENT COLLECTOR  #####################################################

# --- create Instance of FEC, Collect all OST_Lines 
alllines = FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Lines)\
						.ToElements()

# Filter for Name: "HK" (Hilfskonstruktion)  : list comprehension
hklines = [x for x in alllines if x.LineStyle.Name.Contains("HK")] #.Name == "HK" 

# --- FEC for Text -----------------------------------------
txtcol = FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_TextNotes) \
						.ToElements()

hktxt = [x for x in txtcol if x.Name.Contains("HK")]

# FEC Dimension witch contains "HK" string  -----------------------------------
dimcol = FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Dimensions) \
						.ToElements()

hkdim = [x for x in dimcol if x.Name.Contains("HK")]

# put all objects in one list:  hklines + hkdim + hktxt
hktxt += hklines + hkdim


#----- FilteredElementCollector of Views , Create Instance of FEC, ----------------------------
FECviews = FilteredElementCollector(doc).OfClass(View).ToElements() 

#viewlistsort = sorted(viewlist, key = lambda x: x.Name)
# viewtypelist = ["FloorPlan", "CeilingPlan","Elevation", "ThreeD" ,"DrawingSheet", \
                # "DraftingView", "Legend", "EngineeringPlan", "AreaPlan", "Section", "Detail"]
viewlist =[i for i in FECviews if i.CanBePrinted]



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

def ProcessListArg(_func, _list, _arg): #_func: underscore has no special meaning in args of func 
    return map( lambda x: ProcessListArg(_func, x, _arg) if type(x) == list else _func(x, _arg), _list )



t = Transaction(doc, "Hide, Unhide Elements")
try:
    # create a instance of Transaction class , start instance with start() method

    t.Start()
    #[HideUnhideEl(i, hktxt) for i in viewlist] 
    ProcessListArg(HideUnhideEl, viewlist, hktxt)
    t.Commit() 
except:
    # if error accurs anywhere in the process catch it
    t.RollBack()
    import traceback
    errorReport = traceback.format_exc()
    print(errorReport)


# for timing -------------------------------------------------------------------
endtime = timer.get_time()
print("endtime", endtime)
# ------------------------------------------------------------------------------





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

# -- FUNCTIONS  from Konrad in Dynamo ---------------------------------------
# See StackOverflow entry, question answerd by Konrad

# def ProcessList(_func, _list):
    # return map( lambda x: ProcessList(_func, x) if type(x) == list else _func(x), _list )

