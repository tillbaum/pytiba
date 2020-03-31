""" DWG Export Sheets 
	ShiftClick: resets Filepath 
	(overwrites/delets filepath-string in path.txt) """

__title__ = "DWG \nExport_v0.1"
	
__author__ = "TBaumeister" 	

__doc__ = "Test blabla"

import clr # import common language runtime .Net Laufzeitumgebung 
from System.Collections.Generic import List 
from Autodesk.Revit.DB import *  # FilteredElementCollector, #OfClass, BuiltInCategory, Transaction, TransactionGroup
from pyrevit import forms 
import os, sys
from math import ceil 	#this way of importing takes much less momory, and is faster! python cookbook! 
from time import sleep # sleep() 
import traceback 
from pyrevit import script

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Filepath-----------------------------------------------

scriptpath = script.get_script_path()
if not scriptpath: 
	scriptpath = "C:\\Users\\Till\\Desktop"
#Overwrite/Delete path.txt, w+ mode
if __shiftclick__: 
	with open(scriptpath + "\\path.txt", "w+") as f: 
		pass	
	forms.alert("filepath deleted!")

mode = "a+" # read, create file, write file, pointer at end.
with open(scriptpath + "\\path.txt", mode) as f: 
	f.seek(0)
	filepath = f.readline()
	print("---Filepath----------------------------------")
	print(filepath)
	if not filepath:
		filepath = forms.pick_folder()
		f.seek(0) # set pointer back to Beginning of file
		f.write(filepath)


# ---FILENAME ------------------------------
#func lookuppara; paraname as string: ex: "Sheet Number"
def lookupparaval(element, paraname):
	try: newp = element.LookupParameter(paraname)
	except: newp = None; pass 
	value = ""
	if newp:
		if newp.StorageType == StorageType.String:    value = newp.AsString()
		elif newp.StorageType == StorageType.Integer: value = newp.AsInteger()
		elif newp.StorageType == StorageType.Double:  value = newp.AsDouble()
		return value
	else: 
		return False

def fileName(viewlist):
	# Time + Date
	from datetime import datetime # considers Sommer and Winter Time 
	m = datetime.now() 
	dateformat = "%d-%m-%y" # 05-06-18 leading 0
	timeformat = "%H.%M"		#20.15
	date = m.strftime(dateformat) #stringformattime function
	time = m.strftime(timeformat)
	#filepathlist = []
	filenamelist = []
	for v in viewlist: 
		paraval_nr = lookupparaval(v, "Sheet Number") 
		paraval_revision = lookupparaval(v, "man_Index") 
		paraval_name = lookupparaval(v, "Sheet Name") 
		sep = "_" 
		tmp_fn = ''.join([ str(paraval_nr), '_', \
					str(paraval_revision) if paraval_revision else '', \
					'_', str(paraval_name),'_', date, '_', time, '.dwg'])
		filenamelist.append(tmp_fn)
	#	filepathlist.append(dirpath + "\\" + tmp_fn )
	return filenamelist

#---Element Selection --------------------------------------
selec_el = [doc.GetElement( elId ) for elId in uidoc.Selection.GetElementIds() \
				if doc.GetElement(elId).GetType() == ViewSheet ] 
#---END ELEMENT SELECTION -------------------------------------

# Forms Dialog: Select ViewSheets -------------------------
if len(selec_el): #exist: 1 or 2, or 3 or ... , not 0
	viewlist = selec_el
else: 
	viewlist = forms.select_sheets()
if not viewlist:
	sys.exit() #pyrevit.script.exit() 

# fun Export DWG ---------------------------------------------
def ExportDwg(filename, view, folder): 
	# DWGExport Options, get Current Active
	firstdwgsetting = FilteredElementCollector(doc).OfClass(ExportDWGSettings) \
													.FirstElement()
	currentactiveset= firstdwgsetting.GetActivePredefinedSettings(doc)
	dwgopt= currentactiveset.GetDWGExportOptions()
	views = List[ElementId]()
	views.Add(view.Id)
	result = doc.Export(folder, filename, views, dwgopt)
	return result 

#call create filename FUN
fnlist = fileName(viewlist)

# Printing Lists
print("--- Viewlist-------------------------------------------------")
for i in viewlist: 
	print( '{} - {}'.format(i.SheetNumber, i.ViewName))
print("--- FileNamelist---------------------------------------------")
for i in fnlist: print(i)
print("\n--- DWG Export -----------------------------------")

# Export DWG --- existing files with same name will be overwritten, No Error
try:
	errorReport = None
	# run export
	for fn, v in zip(fnlist, viewlist):
		ExportDwg(fn, v, filepath)
		print("Sucess")
except:
	# if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()


# TODO Test if the ProcessList is faster than for loop! 
# from Konrad
# def ProcessList(_func, _list):
    # return map( lambda x: ProcessList(_func, x) if type(x)==list else _func(x), _list )

# def ProcessParallelLists(_func, *lists):
	# return map( lambda *xs: ProcessParallelLists(_func, *xs) if all(type(x) is list for x in xs) else _func(*xs), *lists )

# try:
	# errorReport = None
	# run export
	# ProcessParallelLists(ExportDwg, fnlist, viewlist)
# except:
	# if error accurs anywhere in the process catch it
	# import traceback
	# errorReport = traceback.format_exc()







