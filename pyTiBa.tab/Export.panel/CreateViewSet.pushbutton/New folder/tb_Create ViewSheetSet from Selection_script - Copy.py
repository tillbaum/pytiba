""" create ViewSheetSet from selected 
	Views in ProjectBrowser and save
	under Name provided in InputDialog 
	todo: show viewsets in InputWindow 
	todo: show textinput field in selected_sheets Window"""

__title__ = "Create/Edit ViewSheetset (fr.Selection)"

__author__ = 'Tillmann Baumeister'

import clr

#clr.AddReference("RevitAPI") # .dll file 
from Autodesk.Revit.DB import * # FilteredElementCollector, OfClass, BuiltInCategory, Transaction, TransactionGroup
from pyrevit.script  import exit 
import pyrevit 
from pyrevit import forms 
from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, \
                           Separator, Button, CheckBox, Alert 
import sys 

doc = __revit__.ActiveUIDocument.Document 
uidoc = __revit__.ActiveUIDocument 


# # FEC instance of ViewSheetSet Class --------------------

# viewsetcol = FilteredElementCollector(doc).OfClass(clr.GetClrType(ViewSheetSet)) \
										# .ToElements()
# From Konrad Node GetViewsfromViewSet
FECviewsets = FilteredElementCollector(doc).OfClass(ViewSheetSet).ToElements()
#create a dictionary from FECviewsets, key=viewsheetset-name : value=vss element 
allviewss = {vss.Name: vss for vss in FECviewsets} # is a set, a dictionary is created
																	# key: value; vss.Name, vss
print("ViewSheetSets in doc: ------------------------------")
for i,j in enumerate(FECviewsets): 
	print(str(i) + " " +  str(j.Name) )


#--- ELEMENT SELECTION ----------------------------------------
selec_ids = uidoc.Selection.GetElementIds()
# Filter Selection for Type == ViewSheet 
selec_sheets = [doc.GetElement(i) for i in selec_ids if doc.GetElement(i).GetType()==ViewSheet ] 
#---END ELEMENT SELECTION -------------------------------------

if not selec_sheets: #== 0, 0 = False, 1,2,3,4.... = True
	# pyrevit Select_SHEETS Dialog, in forms __init__ file 
	selec_sheets= pyrevit.forms.select_sheets() 

if not selec_sheets:
	sys.exit() 

print("\nselected ViewSheets: ----------------------------" )
# instantiate a new ViewSet Class()
# ViewSet Class has a public Constructor ViewSheetSet Class does not 
new_viewset = ViewSet() 
for i in selec_sheets : 
	print( i.SheetNumber + " " + i.Name) 
	new_viewset.Insert(i)

# get the PrintManger from the current document 
printman = doc.PrintManager 
	# When this is run, a dialog pops up: Freepdf cannot be used with 95x90 print
	# settings. The "in-session print settings will be used" 
	# - This dialog can not be dissabled. 

# set this PrintManager to use the "Selected Views/Sheets" option
printman.PrintRange = PrintRange.Select  # PrintRange is a different class
	
# get the ViewSheetSetting which manages the view/sheet set information of current document 
viewshsetting = printman.ViewSheetSetting  # returns ViewsheetSetting object, 

# textin Dialog:FlexForm from rpw, 
components = [Label('Enter Name: '),
		TextBox('textbox1', Text=""),
		CheckBox('checkbox1', 'Overwrite, if name exists', default=True),
		Button('OK')]
textin = FlexForm('New ViewSheetSet', components)
textin.show() 

print(textin.values) 

# with Transaction(doc, 'Created Print Set'): 
	
#vsexist = True if textin.values["textbox1"] in allviewss.keys() 
#			else 3 if len(textin.values) == 0  else False

try:
	if textin.values["textbox1"] in allviewss.keys() : 
		vsexist = True	
	else: 
		vsexist = False 
except:
	vsexist = 3
	pyrevit.script.exit()

print(vsexist)

#ViewSheetSet exist and override = True ->Delete existing sheet set 
if vsexist and textin.values["checkbox1"]: 
	t = Transaction(doc,"Delete Existing Viewset")
	t.Start() 
	viewshsetting.CurrentViewSheetSet = allviewss[textin.values["textbox1"]]  
	viewshsetting.Delete()
	t.Commit() 
	vsexist = False 
	print("\nViewSet deleted ")		

# ViewShetSet exist, and override = false -> Message		
elif vsexist and not textin.values["checkbox1"]:    
	out = '\nSheetSet with same name exist, set override to True'
	print(out)
	#Alert(out , title="Error", exit=True)	

# Create new sheet set 		
if not vsexist: 
	t= Transaction(doc, "Create new ViewSheetset")
	t.Start() 
	viewshsetting.CurrentViewSheetSet.Views = new_viewset 	
	viewshsetting.SaveAs(textin.values["textbox1"])   # throws ERROR if name exist 
	t.Commit()
	OUT = '\n "' + textin.values["textbox1"] + '" - ViewSheetSet with %s views created.' %(new_viewset.Size)
	print("-----------------------------")
	print(OUT) 

else: print("Error, Nothing created")
