''' Create SheetViews from EXCEL-File
	v1.1 updated, cleaned up, put in function
'''
from __future__ import print_function

__title__ = "Sheets\nTO Excel"

__author__ = "Tillmann Baumeister"

from Autodesk.Revit.DB import FilteredElementCollector, Transaction, BuiltInParameter
from Autodesk.Revit import DB
import System
from System.Runtime.InteropServices import Marshal 
import sys, os
from rpw.ui.forms import TaskDialog 
from pyrevit import forms 

doc = __revit__.ActiveUIDocument.Document
uiapp = __revit__
app = uiapp.Application

#todo: CALC Open and REad -----------------------------------

# EXCEL OPEN and READ ---------------------------------------------------------

def excel_read(origin = "A3", worksheetname="Sheets"):
	try:
		xlapp = Marshal.GetActiveObject('Excel.Application')
		ws = xlapp.sheets(worksheetname) #Name of the Excel Worksheet
	except EnvironmentError:
		forms.alert('Excel Application not open!\nOpen Excel file with worksheet "Sheets" ')
		dialogexcelnotopen.show()
		sys.exit()
	except:
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


def exc_writearray(origin = "A3", worksheetname= "Sheets"):
	originnr = [i for i in origin if i.isdigit()][0]
	end = len(ex_row) -1 + int(originnr)
	
	xlapp = Marshal.GetActiveObject('Excel.Application')
	worksheet = xlapp.sheets(worksheetname) #Name of the Excel Worksheet
	xlrange_id = worksheet.Range["I" + str(originnr), "I" + str(end)]
	#from System.Reflection import Missing
	from System import Array 
	array_id = Array.CreateInstance(object, len(ex_row), 1) 

	# set array_id with values from dic_sheetGuid
	for i,j in zip(range(len(ex_row)), ex_row):
		if j[0] in dic_sheetGuid:
			array_id[i, 0] = dic_sheetGuid[j[0]]
	#write array to cellrange_sheetid
	if (xlrange_id.Value2.GetLength(0), xlrange_id.Value2.GetLength(1)) \
			== (array_id.GetLength(0), array_id.GetLength(1)): # (7,1) == ( 7,1)
		xlrange_id.Value2 = array_id
	Marshal.ReleaseComObject(xlapp)
	return True
	
# CREATE sheets and Titleblock2 from filterd excel_datalist
def createsheets(sheetlist):
	message = []
	dic_sheetGuid = {}
	t = Transaction(doc, "Create SheetViews from EXCEL")
	try:
		t.Start()
		for j in sheetlist: 
			try:
				tibl = dic_tibl[j[2]]
				a = ViewSheet.Create(doc, tibl.Id)# ViewSheet Class, Create Method 
				a.SheetNumber= j[0]
				a.ViewName= j[1]
				dic_sheetGuid[a.SheetNumber] = str(a.UniqueId)
				#create TitleBlock2 instance 
				try:
					tibl_2 = dic_tibl[j[3]]
					newtitleblock = doc.Create.NewFamilyInstance(XYZ(0,0,0),tibl_2,a) 
					mess2 = '; TitleBlock2: {}'.format(str(j[3])) 
				except:	
					mess2 = '; TitleBlock2: {}'.format(str(j[3]))
					pass 
				message.append('{} - {}, TitleBlock1: {}'.format(a.SheetNumber, a.ViewName, j[2]) + mess2)
			except: 
				mess2 = "Error: TitleBlock ",j[2],"not found"
				message.append(mess2)
				pass
		t.Commit()
	except:
		t.RollBack() 
		import traceback	
		print(traceback.format_exc())
		sys.exc_info()
	return (message, dic_sheetGuid)


# EXCEL_row_filter: Filter out sheets already existing in Prj ------------
		#all() if all statements in list are true --> true, if one is none -> none
def ex_row_filter(list):
	ex_row_create = []
	for i in list: 
		if i[0] and i[1] and i[2] in dic_tibl \
			and not [k for k in FECsheet if k.SheetNumber == str(i[0])]:
		#if all([i[0], i[1], i[2] if i[2] in dic_tibl else False]) and not [k for k in FECsheet if k.SheetNumber != str(i[0])]:
			ex_row_create.append(i)
	return ex_row_create

# ----------------------------------------------------------------------------

# FEC Collect Sheetviews
FECsheetls = FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Sheets) \
					.WhereElementIsNotElementType() \
					.ToElements()
#Filter out Placeholders 
FECsheet = [x for x in FECsheetls if not x.IsPlaceholder]

# FEC TitleBlocks in Project
FECtibl = FilteredElementCollector(doc) \
					.OfCategory(DB.BuiltInCategory.OST_TitleBlocks) \
					.WhereElementIsElementType() \
					.ToElements() 
# CREATE dictionary TitleBlock: "FamilyType Name" : titleblockobj
dic_tibl = {i.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString() : i for i in FECtibl}


ex_row = excel_read()

sheet_createlist = ex_row_filter(ex_row)
if sheet_createlist: # exist/ is not empty/ != 0
	created = createsheets(sheet_createlist)


# OUTPUT -------------------------------------------
#if shiftclick:
print("READ EXCEL DATA---------------------------------------")
for i in ex_row: print(i) 

print("\nSheet-To-Create List: ------------------------------")
for i in sheet_createlist: print(i)

print("\nSheets in Prj: ", len(FECsheet)) 

print("\nSheets created: ------------------------------------")
if sheet_createlist:
	for i in created[0]: print(i)

# else: 
	# print('Sheets exist, No Sheets created')


# collect parameters  back from Sheets() 
# for i in FECsheets:
# sheetname = get_para # and write them to ex_row list
# create a array the size of ex_row list
# write er_row 

#todo: Maybe Create TitleBlock2 separate from ViewSHeet Creation. To be able to change TB2 afterwards 
#todo: Show Altert Dialogs, for Errors, and Creation sucessful, 
# show print-box only when errors occurred. otherwise show nothing, for fast sheet creation. 
# todo: when SHIFT+Click run script: show all print messages. 

# READ and SET SHEET_PARAMETER -----------------------------------------------------

#--- 1. CREATE SharedParameter: man_Massstab ----------------------------------

# Create Shared Parameter func: 
def createSharedPara(_paramName_string,_groupNameinSPfile_string, \
					_paramtype_enum, _builtInCat_enum,_paramGroupinProperty_enum):
	# open SharedParameterFile 
	file = uiapp.Application.OpenSharedParameterFile()
	# get GroupName in SharedParameter file, if not exist create new Group  
	group = file.Groups.get_Item(_groupNameinSPfile_string)
	if group == None: 
		group = file.Groups.Create(_groupNameinSPfile_string)
	# Create NewCategorySet()  
	catset = app.Create.NewCategorySet()
	# Insert Category Objects in CatSet  <Autodesk.Revit.DB.Category object 
	catset.Insert(doc.Settings.Categories.get_Item(_builtInCat_enum)) # returns True
	# create an instance binding object with categoryset
	inst_bind = app.Create.NewInstanceBinding(catset) 
	#ExternalDefinitionCreationOptions Class  excpects ( paraname as string, paratype object)
	# An option class used for creating a new shared parameter definition,  
	ED_opt1 = ExternalDefinitionCreationOptions(_paramName_string, _paramtype_enum) 
	ED_opt1.Visible = True # True is the default value 
	#Create Parameter Definition Object 
	#Test if paraName is in SharedParam file , get Para Name Definition from file, else Create new Name 
	if group.Definitions.Contains(group.Definitions.Item[_paramName_string]):
		_exdef1 = group.Definitions.Item[_paramName_string] # create parameter definition object from Para in file
	else:
	# _def = group.Definitions.Create(_paramName, _paramtype_enum, _visible) 
		_exdef1 = group.Definitions.Create(ED_opt1) #Create para Definition object wit Ext
	#Create Parameter by inserting the Para Definition in the ParameterBindigs_Map
	t = Transaction(doc, "Parameter Creation")
	t.Start() 
	bind_Map = doc.ParameterBindings.Insert(_exdef1, inst_bind, _paramGroupinProperty_enum) 
	t.Commit()

# --- Inputs to SharedParameter CREATION ----------------------------------------
# _paramName_string = "man_Massstab" 	# ...can be anything, as string 
# _groupNameinSPfile_string  = "Plan"  	# ...can be anything ,as string: Ex."name"  Groupname in ParameterFile 
# _paramtype_enum  = DB.ParameterType.Text   # Enum ParameterType Enum listing all Parameters found in Parameter Dialog,
# _builtInCat_enum = DB.BuiltInCategory.OST_Sheets  	# Enum, contains all build in Paras
# _paramGroupinProperty_enum_ = DB.BuiltInParameterGroup.PG_TEXT 	# Enum, ParameterGroup in the property panel in Revit 

#CREATE man_Massstab Parameter
# test if sharedParameter "man_Massstab" exist in SheetViews. If not create it. 
if not FECsheet[0].LookupParameter("man_Massstab"):
	createSharedPara("man_Massstab", "Plan", DB.ParameterType.Text, \
						DB.BuiltInCategory.OST_Sheets,
						DB.BuiltInParameterGroup.PG_TEXT)
	print("man_Massstab SP parameter created")
	
#--- END SharedParameter Creation -----------------------------------------------------------

# Create Project Parameters via the API --> currently not possible 
# Employee jeremytammik
# in reply to: RankBIMS_Keris
# Re: Create Project Parameter(not shared parameter)
# Sorry, as far as I know these cannot be created programmatically.

# Update Sheet Parameter ----------------------------------------------------

# FEC Collect "ALL" Sheetviews: NEWLY Created and OLD, Filter out Placeholders

# bip: SHEET_DRAWN_BY, SHEET_NUMBER, DB.BuiltInParameter.SHEET_ISSUE_DATE
def getnsetBIP(elem, bip, setvalue):
	if setvalue:
		try: para = elem.get_Parameter(bip)
		except: pass
		para.Set(setvalue)
		return para.AsString()

def lookupparaval(element, paraname): 
	try: newp = element.LookupParameter(paraname)
	except: newp = None; pass 
	if newp:
		if newp.StorageType == StorageType.String:    value = newp.AsString()
		elif newp.StorageType == StorageType.Integer: value = newp.AsInteger()
		elif newp.StorageType == StorageType.Double:  value = newp.AsDouble()
		return value
	else: return False

# ParameterType = Text
def getnsetSharedPara(elem, SharedParaname_string, setvalue_string):
	try:
		para = elem.LookupParameter(SharedParaname_string)
	except: 
		pass
	if setvalue_string:
		para.Set(setvalue_string)
		return para.AsString()

def parameterupdate(exel_datalist):
	FECsheetcol = FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Sheets) \
					.WhereElementIsNotElementType() \
					.ToElements()
	FECsheet = [x for x in FECsheetcol if not x.IsPlaceholder]

	ex_row_paralist = [i for i in exel_datalist if i[0] != None]

	#Create a list from FECsheets matching ex_row_paralist in Project 
	# using SheetNR for Equality Check, do this with FEC?
	sheetviewelems = []
	for i in ex_row_paralist: 
		for j in FECsheet: 
			if j.SheetNumber == i[0]:
				sheetviewelems.append(j)
	#GUID BuiltInParameter ---------------------------
	sheet_issuedate = DB.BuiltInParameter.SHEET_ISSUE_DATE
	sheet_drawnby = DB.BuiltInParameter.SHEET_DRAWN_BY
	mess = []
	t = Transaction(doc, "update sheet parameters")
	t.Start()
	for i,j in zip(sheetviewelems,ex_row_paralist): 
		try: 
			date = getnsetBIP(i,sheet_issuedate, j[5])
			drawnby = getnsetBIP(i,sheet_drawnby, j[6])
			man_massstab = getnsetSharedPara(i, "man_Massstab", j[7])
			pbrowser = getnsetSharedPara(i, "PBrowser", j[4])
			mess2 = 'SheetNr: {} Parameters: prjbrowser: {}, issue_date: {}, drawnby: {}, M: {}'.format(i.SheetNumber, pbrowser, date, drawnby, man_massstab) 
			mess.append(mess2)
		except:
			error = 'Error '
			mess.append(error)
			import traceback
			print("\n",traceback.format_exc())
			continue
	t.Commit()
	return mess

try:
	mess = parameterupdate(ex_row)
except: 
	import traceback
	print("\n",traceback.format_exc())

# OUTPUT --------------------------
print("\nUPDATE SHEETVIEW PARAMETERS ---------------------------------------------")
for i in mess: print(i)


# t = Transaction(doc, "Set Sheetview Parameter")
# t.Start()
# for i,j in enumerate(sheetviewelems): 
	# para_date = j.get_Parameter(sheet_issue_dateGUID)
	# para_author = j.get_Parameter(sheet_drawn_byGUID)
	# para_massstab= j.LookupParameter("man_Massstab")
	

	# para_date.Set(ex_row_paralist[i][5])
	# para_author.Set(ex_row_paralist[i][6])
	# para_massstab.Set(ex_row_paralist[i][7])
	# mess = 'set: ' + para_date.AsString() + ', ' + para_author.AsString() + ', M:' + para_massstab.AsString()
	# print(mess)
# t.Commit() 

# BuiltInParameter List: 
# SHEET_SCALE			ok , # read only 
# SHEET_ISSUE_DATE  ok, Blatt Ausgabedatum!  
# SHEET_DATE 
# SHEET_CURRENT_REVISION 
# SHEET_DRAWN_BY 		ok 

# todo: do it with a set. subtract sets, maybe its faster! try it!
