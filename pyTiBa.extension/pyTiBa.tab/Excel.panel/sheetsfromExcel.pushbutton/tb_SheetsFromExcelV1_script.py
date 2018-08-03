""" Create SheetViews from EXCEL-File """

__title__ = "Sheets\nfrom Excel"

__author__ = "Tillmann Baumeister"

from Autodesk.Revit.DB import *
import System 
from System.Collections.Generic import * 
from System.Runtime.InteropServices import Marshal 
import sys
from rpw.ui.forms import TaskDialog 
from pyrevit import forms 

doc = __revit__.ActiveUIDocument.Document
app = __revit__
uiapp = __revit__ # is the same as uiapp = DocumentManager.Instance.CurrentUIApplication
# returns:  <Autodesk.Revit.UI.UIApplication object at 0x0000000000000171 [Autodesk.Revit.UI.UIApplication]>
app = uiapp.Application

# func to print items in list, How can I apply multiple optional args in Functions
def lprint(ls):
	for i in ls: print(i) 

# FEC Collect TitleBlocks # FamilySymbol are the Types of the family:
						  #ex, family: column, types: 25x25  ".OfClass(FamilySymbol)" not needed 
tbcol = FilteredElementCollector(doc) \
					.OfCategory(BuiltInCategory.OST_TitleBlocks) \
					.WhereElementIsElementType() \
					.ToElements() 

# for i in tbcol: 
	# typename = i.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
	# print("{:<35} - {}".format( i.FamilyName , typename ))
# print(len(tbcol))
# print("-------------------")
# tbcolTypename = [i.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString() for i in tbcol ]
# for i in tbcolTypename: print(i)
# print("TitleBlocks: ", len(tbcol))

# FEC Collect Sheetviews
sheetcol = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets) \
					.WhereElementIsNotElementType() \
					.ToElements()
#Filter out Placeholders 
FECsheet = [x for x in sheetcol if not x.IsPlaceholder]
print("Sheets: ", len(FECsheet)) 

#todo: CALC Open and REad -----------------------------------

# EXCEL OPEN and READ ---------------------------------------------------------
try:
	xlapp = Marshal.GetActiveObject('Excel.Application')
	ws= xlapp.sheets("Sheets") #Name of the Excel Worksheet
except: 
	forms.alert('Error: \nExcel APPLICATION not open! \
					\nOpen Excel doc with worksheet \"Sheets\" \
					 to read data from') 
	dialogexcelnotopen.show()
	sys.exit()
	
# Konrad Bumblebee Func ---------------------------------------
def GetExtent(ws, extent):
	if extent != None:
		extent = ws.Cells(bb.CellIndex(extent)[1], bb.CellIndex(extent)[0])
	else:
		extent = ws.Cells(ws.UsedRange.Rows(ws.UsedRange.Rows.Count).Row, ws.UsedRange.Columns(ws.UsedRange.Columns.Count).Column)
	return extent

def ReadData(ws, origin, extent, byColumn):
	rng = ws.Range[origin, extent].Value2
	if not byColumn:
		dataOut = [[] for i in range(rng.GetUpperBound(0))]
		for i in range(rng.GetLowerBound(0)-1, rng.GetUpperBound(0), 1):
			for j in range(rng.GetLowerBound(1)-1, rng.GetUpperBound(1), 1):
				dataOut[i].append(rng[i,j])
		return dataOut

	else: # read by column (Spalte): byColumn = True 
		dataOut = [[] for i in range(rng.GetUpperBound(1))]
		for i in range(rng.GetLowerBound(1)-1, rng.GetUpperBound(1), 1):
			for j in range(rng.GetLowerBound(0)-1, rng.GetUpperBound(0), 1):
				dataOut[i].append(rng[j,i])
		return dataOut

origin = "A3" 
extent = None 

# READ EXCEL DATA ---------------------------------------------
try: 
	# ex_col = ReadData(ws, origin, GetExtent(ws, extent), byColumn= True )	
	# for i in ex_col: print(i)
	print("READ EXCEL ROWS DATA--------------------------------")
	ex_row = ReadData(ws, origin, GetExtent(ws, extent), byColumn= False ) 
	for i in ex_row: print(i) 
except:
	# if error accurs anywhere in the process catch it 
	import traceback 
	errorReport = traceback.format_exc() 
	print(errorReport) 
	pass 
finally: 
	# xlapp.Quit() # .Quit()  Closes Excel 
	Marshal.ReleaseComObject(xlapp) 

# this statements could also be done with "with ". 
# Because in any case the excel file must be closed. //IronPython in Action
#  the finally term is rn in any case. 


# CREATE VIEWSHEET in Revit DB ------------------------------------------------------------

# CREATE SHEETLIST: 1st to create Sheets from, 
# todo: do it with a set. subtract sets, maybe its faster! 

createSheetls = []
for i, j in enumerate(ex_row):
	# test if any sheetnr in FECsheet matches excel row and first value in row is unequal to None 
	if not [x for k in FECsheet if k.SheetNumber == ex_row[i][0]] and ex_row[i][0] != None : 
		createSheetls.append(j) 

# None-Colums and colums with sheetnr matching SheetNr from sheets in prj filtered out. 
# new List: createSheetls 

print( "\nCreateSheet-List: ----------------------------------")
lprint(createSheetls)

print("\nSheets created: ------------------------------------")

# with Transaction(doc, "Excel") 

# t = Transaction(doc, "Create SheetViews from EXCEL")

if len(createSheetls) != 0:
	t.Start()
	for i,j in enumerate(createSheetls):
		try: 	
			# todo: create a dictionary, with "Titleblocktype Name": elementId, to pick element from 
			
			# search tbcol for TitleBlockTypename matching  name in Excel"Sheets", get element
			tibl = [k for k in tbcol if k.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM) \
						.AsString() == createSheetls[i][2] ] 
			
			tbname = tibl[0].get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM) \
						.AsString()
				
			a = ViewSheet.Create(doc, tibl[0].Id)# ViewSheet Class, Create Method 
			a.SheetNumber= j[0]
			a.ViewName= j[1]
			
			# create TitleBlock2 j[3] = TitleBlock2 in Excel data 
			message2 = "" 
			if j[3] != None: 
				try:
					tibl_2 = [k for k in tbcol if k.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM) \
						.AsString() == j[3] ]
					
					if tibl_2[0].IsActive == False: 
						tibl_2[0].Activate() 
						doc.Regenerate() 

					#create TitleBlock2 instance 
					newtitleblock = doc.Create.NewFamilyInstance(XYZ(0,0,0),tibl_2[0],a) 
					message2 = '; TitleBlock2: "' + str(j[3]) + '" created' 
				except:	
					message2 = '; Could not find TitleBlock2: "' + str(j[3]) + '" in Prj' 
					pass 
			#vsh_list.append(a) 
			
			message =  str(j[0]) + " " + tbname + "-TitleBlock created " + message2 
			print(message) 
		except: 
			error = "Error: " + str(j[0]) +" " + str(tbname) 
			print(error) 
			
	t.Commit()
else: 
	print('"createSheetls" is empty')

#todo: Maybe Create TitleBlock2 separate from ViewSHeet Creation. To be able to change TB2 afterwards 
#todo: Show Altert Dialogs, for Errors, and Creation sucessful, 
# show print-box only when errors occurred. otherwise show nothing, for fast sheet creation. 
# todo: when SHIFT+Click run script: show all print messages. 


# READ and SET SHEET_PARAMETER -----------------------------------------------------

#--- 1. CREATE SharedParameter: man_Massstab ----------------------------------


def createSharedPara(_paramName1,_groupNameinSPfile, _paramtype, _builtInCat,_paramGroupinProperty)
	# open SharedParameterFile 
	file = app.OpenSharedParameterFile()
	# get GroupName in SharedParameter file, if not exist create new Group  
	group = file.Groups.get_Item(_groupNameinSPfile)
	if group == None: 
		group = file.Groups.Create(_groupNameinSPfile)
	# Create NewCategorySet()  
	catset = app.Create.NewCategorySet()
	# Insert Category Objects in CatSet  <Autodesk.Revit.DB.Category object 
	catset.Insert(doc.Settings.Categories.get_Item(_builtincat)) # returns True
	# create an instance binding object with categoryset
	inst_bind = app.Create.NewInstanceBinding(catset) 
	#ExternalDefinitionCreationOptions Class  excpects ( paraname as string, paratype object)
	# An option class used for creating a new shared parameter definition,  
	ED_opt1 = ExternalDefinitionCreationOptions(_paramName1, _paramtype) 
	ED_opt1.Visible = True # True is the default value 
	#Create Parameter Definition Object 
	#Test if paraName is in SharedParam file , get Para Name Definition from file, else Create new Name 
	if group.Definitions.Contains(group.Definitions.Item[_paramName1]):
		_exdef1 = group.Definitions.Item[_paramName1] # create parameter definition object from Para in file
	else:
	# _def = group.Definitions.Create(_paramName, _paramType, _visible) 
		_exdef1 = group.Definitions.Create(ED_opt1) #Create para Definition object wit Ext

	#Create Parameter by inserting the Para Definition in the ParameterBindigs_Map
	t = Transaction(doc, "Parameter Creation")
	t.Start() 
	bind_Map = doc.ParameterBindings.Insert(_exdef1, inst_bind, _paramGroupinProperty) 
	t.Commit()

# Inputs to SharedParameter CREATION 
# _paramName1 = "man_Massstab" # can be anything, as string 
# _groupName  = "Plan"  # ...can be anything ,as string: Ex."name"  Groupname in ParameterFile 
# _paramtype  = ParameterType.Text  #PType found in Parameter Dialog,
									#is a namespace in API, subnamespace from DB Namespace 
# _builtincat = BuiltInCategory.OST_Sheets  # is a subnamespace from DB in API, Enumeration class 
# _paramGroup = BuiltInParameterGroup.PG_TEXT # ParameterGroup in the property panel in Revit 

#def createSharedPara(_paramName1,_groupName, _paramtype, _builtInCat,_paramGroup)
# test if sharedParameter "man_Massstab" exist in SheetViews. If not create them. 
if not FECsheet[0].LookupParameter("man_Massstab"):
	createSharedPara("man_Massstab", "Plan", ParameterType.Text, \
				BuiltInCategory.OST_Sheets, \
				BuiltInParameterGroup.PG_TEXT)
	
#--- END SharedParameter Creation -----------------------------------------------------------

# --- WRITE SHEETVIEW PARAMETER -----------------------------------------------------
Sheetls_forPara = [ j for i,j in enumerate(ex_row) if ex_row[i][0] != None] 

# FEC Collect "ALL" Sheetviews: NEWLY Created and OLD, Filter out Placeholders
sheetcol = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets) \
					.WhereElementIsNotElementType() \
					.ToElements()
FECsheet = [x for x in sheetcol if not x.IsPlaceholder]
print("Sheets: ", len(FECsheet)) 

#Create new list from FECsheets matching Sheetls_forPara
# using SheetNR for Equality Check, do this with FEC?

sheetviewElems = []
for i in range(len(Sheetls_forPara)): 
	for j in FECsheet: 
		if j.SheetNumber == Sheetls_forPara[i][0]:
	 		sheetviewElems.append(j)

#Test if both list have the same length 
if len(Sheetls_forPara) == len(sheetviewElems):
	mess = str(len(Sheetls_forPara)) + " = " +  str(len(sheetviewElems))
	print(mess)
else: 
	print("Error: Sheets_forPara and sheetviewElems not the same length")

#GUID BuiltInParameter ---------------------------
sheet_issue_dateGUID = BuiltInParameter.SHEET_ISSUE_DATE
sheet_drawn_byGUID = BuiltInParameter.SHEET_DRAWN_BY 

# bip: SHEET_DRAWN_BY, SHEET_NUMBER 
def getnsetBIP(elem, bip, value):
	try: para = elem.get_Parameter(BuiltInParameter.bip)
	except: pass
	para.Set(value)
	return para.AsString()

def getnsetSharedPara(elem, ShParaname, value):
	try: para = elem.LookupParameter(ShParaname)
	except: pass
	para.Set(value)
	return para.AsString()

with Transaction(doc, "bla") as t: 
	for i,j in enumerate(sheetviewElems): 
		a = getnsetBIP(j, SHEET_ISSUE_DATE, Sheetls_forPara[i][5])
		b= getnsetBIP(j, SHEET_DRAWN_BY, Sheetls_forPara[i][6])
		c = getnsetSharedPara(j, "man_Massstab", Sheetls_forPara[i][7])
		mess = mess = 'set: ' + para_date.AsString() + ', ' + para_author.AsString() + ', M:' + para_massstab.AsString()
		print(mess)

t = Transaction(doc, "Set Sheetview Parameter")
t.Start()
for i,j in enumerate(sheetviewElems): 
	para_date = j.get_Parameter(sheet_issue_dateGUID)
	para_author = j.get_Parameter(sheet_drawn_byGUID)
	para_massstab= j.LookupParameter("man_Massstab")
	
	# ValueType of paras = string 
	para_date.Set(Sheetls_forPara[i][5])
	para_author.Set(Sheetls_forPara[i][6])
	para_massstab.Set(Sheetls_forPara[i][7])
	mess = 'set: ' + para_date.AsString() + ', ' + para_author.AsString() + ', M:' + para_massstab.AsString()
	print(mess)
t.Commit() 

# BuiltInParameter List: 
# SHEET_SCALE			ok , # read only 
# SHEET_ISSUE_DATE  ok, Blatt Ausgabedatum!  
# SHEET_DATE 
# SHEET_CURRENT_REVISION 
# SHEET_DRAWN_BY 		ok 

