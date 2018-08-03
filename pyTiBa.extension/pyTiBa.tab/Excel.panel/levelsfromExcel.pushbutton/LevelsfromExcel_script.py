"""LEVELS from Excel 
   EASY
	"""
 
__title__ = "Levels"
	
__author__ = "TBaumeister" 	


import clr # import common language runtime .Net Laufzeitumgebung fuer .Net-anwendungen. / um auf .Net Anwendungen

from Autodesk.Revit.DB import *
# from Autodesk.Revit.DB.Architecture import *
# from Autodesk.Revit.DB.Analysis import * # 
# from Autodesk.Revit.UI import *	

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, View # don't need to import that
from System.Collections.Generic import List 
 

import sys
pyt_path = (r'C:\Program Files (x86)\IronPython 2.7\Lib')
sys.path.append(pyt_path)

doc = __revit__.ActiveUIDocument.Document


#######  FILTERED ELEMENT COLLECTOR  #####################################################

# --- create Instance of FEC, Collect all OST_Lines 
alllines = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Lines)
alllines.ToElements() 
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

