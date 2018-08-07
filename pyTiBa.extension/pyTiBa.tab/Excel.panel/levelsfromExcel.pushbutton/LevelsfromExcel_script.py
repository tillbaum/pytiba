"""
- creates LEvels from ExcelTable
- creates FloorPlan and/or CeilingPlan 
- uses last used LevelType 
"""
from __future__ import print_function, division

__title__ = "Levels\nfrom Excel"

__author__ = "Tillmann Baumeister"

from Autodesk.Revit.DB import FilteredElementCollector, Transaction, BuiltInParameter, Level
from Autodesk.Revit import DB
import System
from System.Runtime.InteropServices import Marshal 
import sys, os
from rpw.ui.forms import TaskDialog 
from pyrevit import forms 
from pyrevit import Forms 
import math 
import decimal 
doc = __revit__.ActiveUIDocument.Document
uiapp = __revit__
app = uiapp.Application

#todo: CALC Open and REad -----------------------------------

# EXCEL OPEN and READ ---------------------------------------------------------

import clr 
clr.AddReference("Microsoft.Office.Interop.Excel")
import Microsoft.Office.Interop.Excel as Excel

def pick_file(file_ext='', files_filter='', init_dir='',
              restore_dir=True, multi_file=False, unc_paths=False):
    of_dlg = Forms.OpenFileDialog()
    if files_filter:
        of_dlg.Filter = files_filter
    else:
        of_dlg.Filter = '|*.{}'.format(file_ext)
    of_dlg.RestoreDirectory = restore_dir
    of_dlg.Multiselect = multi_file
    if init_dir:
        of_dlg.InitialDirectory = init_dir
    if of_dlg.ShowDialog() == Forms.DialogResult.OK:
        if unc_paths:
            return coreutils.dletter_to_unc(of_dlg.FileName)
        return of_dlg.FileName

def excel_read(origin = "A3", worksheetname="Levels"):
	try:
		xlapp = Marshal.GetActiveObject('Excel.Application')
		ws = xlapp.sheets(worksheetname) #Name of the Excel Worksheet
	except EnvironmentError:
		try: 
			filepath = pick_file(file_ext='*')
		except: sys.exit()
		os.startfile(filepath)
		from time import sleep
		sleep(1)
		try:
			xlapp = Marshal.GetActiveObject('Excel.Application')
			ws = xlapp.sheets(worksheetname) #Name of the Excel Worksheet
		except:
			forms.alert('Excel Application not open!\nOpen Excel file with worksheet "Levels" ')
			dialogexcelnotopen.show()
			sys.exit()
	except:
		print("Error")
		import traceback
		print(traceback.format_exc())
	
	extent =  ws.Cells(ws.UsedRange.Rows(ws.UsedRange.Rows.Count).Row, 
					ws.UsedRange.Columns(ws.UsedRange.Columns.Count).Column)

	xlrng = ws.Range[origin, extent].Value2 # 2dimensional array 

	data_list = [[] for i in range(xlrng.GetUpperBound(0))]
	for i in range(xlrng.GetLowerBound(0)-1, xlrng.GetUpperBound(0), 1):
		for j in range(xlrng.GetLowerBound(1)-1, xlrng.GetUpperBound(1), 1):
			data_list[i].append(xlrng[i,j])
	Marshal.ReleaseComObject(xlapp) 
	return data_list

# filter ex_row function, filter out none rows!!! 
def filter_excel_data(data_list):
	ex_rowfilter = []
	for i in data_list:
		if i[0] and i[1] and not [k for k in DB.FilteredElementCollector(doc).OfClass(DB.Level) if k.Name == i[0]]:
			ex_rowfilter.append(i)
	return ex_rowfilter

ex_row = filter_excel_data(data_list = excel_read())

if __shiftclick__:
	print("--- EXCEL-LEVEL-LIST -------------------------------------------")
	for i in ex_row: print(i)
	print("\n--- CREATED --------------------------------------------")


import decimal
from decimal import Decimal 
decimal.getcontext().prec = 5

FECviewfamtype = DB.FilteredElementCollector(doc).OfClass(DB.ViewFamilyType)
floorplantype = [k for k in FECviewfamtype if k.FamilyName == "Floor Plan"][0]
ceilingplantype = [k for k in FECviewfamtype if k.FamilyName == "Ceiling Plan"][0]

t = DB.Transaction(doc, "Create Levels from Excel")
t.Start()
for i in ex_row:
	try:
		elev = Decimal(i[1]).quantize(Decimal('0.01'),
									rounding="ROUND_HALF_UP") 
		elev1 = elev / Decimal(0.3048)
		lev = DB.Level.Create(doc, elev1)
		lev.Name = str(i[0])
		# Create FloorPlan, CeilingPlan
		if i[2]: 
			floorplan = DB.ViewPlan.Create(doc, floorplantype.Id, lev.Id)
		if i[3]:
			ceilingplan = DB.ViewPlan.Create(doc, ceilingplantype.Id, lev.Id)
		if __shiftclick__:
			print("Level ", lev.Name, "Floorplan ", floorplan.Name, "CeilingPlan ", ceilingplan.Name) 
	except:
		import traceback 
		print(traceback.format_exc()) 
		continue 
t.Commit()


