"""	Not Implemented yet !!!!!!!
	Get Parameter Info from Excel
	Set Parameters in Revit
	if Parameters not exist:
	create Parameter as SP in DB 
	"""
from __future__ import print_function, division

__title__ = "PrjInfo"
	
__author__ = "TBaumeister" 	

from Autodesk.Revit.DB import FilteredElementCollector, Transaction, BuiltInParameter
from Autodesk.Revit import DB
import System
from System.Runtime.InteropServices import Marshal 
import sys, os
from rpw.ui.forms import TaskDialog 
from pyrevit import forms 
from pyrefit import Forms 

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

paralist = []

# for i in paralist
	# for j in ex_rowfilter:
		# try:
			# bipProject = getnsetbip(doc, i, j)
		
		# except: 
			# pass 
  

