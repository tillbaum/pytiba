""" create ViewSheetSet from selected 
	Views in ProjectBrowser and save
	under Name provided in InputDialog 
	todo: show viewsets in InputWindow 
	todo: show textinput field in selected_sheets Window Not a good idea """

__title__ = "Create/Edit\nViewSheetSet\n(fr.Selection)"

__author__ = 'Tillmann Baumeister'

# import clr
# clr.AddReference("RevitAPI") # .dll file 
from Autodesk.Revit.DB import * # FilteredElementCollector, OfClass, BuiltInCategory, Transaction, TransactionGroup
from pyrevit.script  import exit 
import pyrevit 
from pyrevit import revit, DB 
from pyrevit import forms
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox,
                           Separator, Button, CheckBox, Alert )
import sys 

doc = __revit__.ActiveUIDocument.Document 
uidoc = __revit__.ActiveUIDocument 

#--- ELEMENT SELECTION ----------------------------------------
selec_ids = uidoc.Selection.GetElementIds()
# Filter Selection for Type == ViewSheet 
selec_sheets = [doc.GetElement(i) for i in selec_ids if doc.GetElement(i).GetType()==ViewSheet ] 

if not selec_sheets: #== 0, 0 = False, 1,2,3,4.... = True
	# pyrevit Select_SHEETS Dialog, in forms __init__ file 
	selec_sheets = pyrevit.forms.select_sheets() 

if not selec_sheets:
	sys.exit() 

#---TextInput Dialog: FlexForm from rpw, ------------------------ 
components = [Label('Enter Name: '), 
		TextBox('textbox1', Text=""),
		CheckBox('checkbox1', 'Overwrite, if name exists', default=True),
		Button('OK')]
textin = FlexForm('New ViewSheetSet', components)
textin.show() 
# testin.values returns a dictionary {"textbox1": "SomeText", "checkbox1": True}

new_viewset = ViewSet() 
for i in selec_sheets : 
	new_viewset.Insert(i)
# get the PrintManger from the current document 
printman = doc.PrintManager 
# set this PrintManager to use the "Selected Views/Sheets" option
printman.PrintRange = PrintRange.Select  # PrintRange is a own class in Revit.DB
# get the ViewSheetSetting which manages the view/sheet set information of current document 
viewshsetting = printman.ViewSheetSetting  # returns ViewsheetSetting object, 


# This is the first time using: with revit Transaction( ) statement. 
# error in pyrevit/revit/transaction.py, line 110, in __init__,
# Type _Error: expected Document, got str.


#with revit.Transaction('Created Print Set'): # ...Transaction(doc, ' SomeText ') throws error

FECviewsets = FilteredElementCollector(doc).OfClass(ViewSheetSet).ToElements()
#Dictionary from FECviewsets, key=viewsheetset.Name : value=vss element 
allviewsets = {vss.Name: vss for vss in FECviewsets} # is a set, a dictionary is created

t = Transaction(doc,"Create Viewset")
t.Start() 
try:
	if textin.values["textbox1"] in allviewsets.keys(): 
		if textin.values["checkbox1"]:  # if override = True
			viewshsetting.CurrentViewSheetSet = allviewsets[textin.values["textbox1"]]  
			viewshsetting.Delete()
		else: 
			mess = 'SheetSet exists, \nset override to True'
			Alert('',title="Create ViewSheetSet - ERROR", header = mess, exit=True)
			t.RollBack()
			sys.exit()

	viewshsetting.CurrentViewSheetSet.Views = new_viewset 	
	viewshsetting.SaveAs(textin.values["textbox1"])   # throws ERROR if name exist 
	mess1 = '"' + textin.values["textbox1"] + '" - ViewSheetSet \nwith %s views created.' \
			%(new_viewset.Size)
	Alert('',title="Success", header = mess1)
	t.Commit() 
except: 
	t.RollBack()
	#print("Error")



    # A Simple Revit TaskDialog for displaying quick messages

    # Usage:
        # >>> from rpw.ui.forms import Alert
        # >>> Alert('Your Message', title="Title", header="Header Text")
        # >>> Alert('You need to select Something', exit=True)
