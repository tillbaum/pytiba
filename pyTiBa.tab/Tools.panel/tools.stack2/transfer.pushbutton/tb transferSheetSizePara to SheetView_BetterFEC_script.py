""" transfer SheetSize Params from 
	TitleBlock to SheetView
	- add SharedPara BLATTHOEHE, BLATTBREITE to SheetView"""

__title__ = "transfer SheetSizeParas"

__author__ = 'Tillmann Baumeister'

# 10.05.2018; added comments, changed some german Names to english names 
# added Parameter Creation. 

from Autodesk.Revit.DB import * 
from decimal import  Decimal

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application

# GetBuiltIN parameter ID object from BuiltInParameterList (see Revit Docs, its a huge List)in DB namespace 
shwi = BuiltInParameter.SHEET_WIDTH  
shhei = BuiltInParameter.SHEET_HEIGHT

# Test: Better FECollector ----------------------------------
sheetwi_id = ElementId(shwi)

# FilterDoubleRule(ParameterValueProvider(), FilterNumericEquals),"ex.10.0", delta_x)
filter_double_rule = FilterDoubleRule(ParameterValueProvider(sheetwi_id),
                                       FilterNumericGreater(),
                                       0.21 * 3.28,
                                       1E-2)

FECtb2 = FilteredElementCollector(doc) \
			.WhereElementIsNotElementType() \
			.WherePasses(ElementParameterFilter(filter_double_rule)) \
          	.ToElements()

# TEST PRINT ----------------------------------------------------
# print("FECtb2 --------------------------")
# for i in FECtb2: 
	# ovid = i.OwnerViewId
	# name = doc.GetElement(ovid).Name
	# print(name) 
# print(len(FECtb2))

#Test--ParameterValueProvider BIP --to get Parameter_Values---------------------------------
pvp = ParameterValueProvider(ElementId(BuiltInParameter.SHEET_WIDTH))
# TEST END ----------------------------------------------------------

# ViewSheet Collector instance 
sheetcol = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets) \
					.WhereElementIsNotElementType() \
					.ToElements() 

# Filter Out ViewSheets that are placeholders and save all in new list: shlist: DO THIS in FEC, 
# could not find a post in Inet where this is done in the FEC. There must be a workaround.  
shlist = [i for i in sheetcol if not i.IsPlaceholder ]
# End FEC ------------------------------------------------------------------------


# test if Parameters BLATTHOEHE and BLATTBREITE exist in SheetViews. If not create them. 

sh0 = shlist[0]
testp1= sh0.LookupParameter("BLATTHOEHE")
testp2 = sh0.LookupParameter("BLATTBREITE")

# Inputs 
_paramName1 = "BLATTBREITE" # can be anything 
_paramName2 = "BLATTHOEHE"
_groupName  = "Plan"  # ...can be anything , Groupname in ParameterFile 
_paramtype  = ParameterType.Number  # is a namespace, subnamespace from DB Namespace 
_builtincat = BuiltInCategory.OST_Sheets  # is a namespace, Enumeration class 
_paramGroup = BuiltInParameterGroup.PG_IDENTITY_DATA # Namespace, subnamespace from DB,
# ParameterGroup in the property panel in Revit 

if not testp1 and not testp2:  
	
# Create Parameter Blatthoehe and Blattbreite ----------------------------------

# open SharedParameterFile 
	file = app.OpenSharedParameterFile() 

# get GroupName in SharedParameter file, if not exist create new Group  
	group = file.Groups.get_Item(_groupName) 
	if group == None: 
		group = file.Groups.Create(_groupName) 

# Create NewCategorySet()  
	catset = app.Create.NewCategorySet()  

# Insert Category Objects in CatSet  <Autodesk.Revit.DB.Category object 
	catset.Insert(doc.Settings.Categories.get_Item(_builtincat)) # returns True

# create an instance binding object with categoryset
	inst_bind = app.Create.NewInstanceBinding(catset) 

#ExternalDefinitionCreationOptions Class  excpects ( paraname as string, paratype object)
#  An option class used for creating a new shared parameter definition,  
	ED_opt1 = ExternalDefinitionCreationOptions(_paramName1, _paramtype) 
	ED_opt1.Visible = True # True is the default value 

	ED_opt2 = ExternalDefinitionCreationOptions(_paramName2, _paramtype) 
	ED_opt2.Visible = True # True is the default value 

# Create Parameter Definition Object 
 # Test if paraName is in SharedParam file , get Para Name Definition from file, else Create new Name 
	if group.Definitions.Contains(group.Definitions.Item[_paramName1]):
		_exdef1 = group.Definitions.Item[_paramName1] # create parameter definition object from Para in file
	else:
	# _def = group.Definitions.Create(_paramName, _paramType, _visible) 
		_exdef1 = group.Definitions.Create(ED_opt1) #Create para Definition object wit Ext

	if group.Definitions.Contains(group.Definitions.Item[_paramName2]):
		_exdef2 = group.Definitions.Item[_paramName2] # create parameter definition object from Para in file
	else:
	# _def = group.Definitions.Create(_paramName, _paramType, _visible) 
		_exdef2 = group.Definitions.Create(ED_opt2) #Create para Definition object wit Ext

#Create Parameter by inserting the Para Definition in the ParameterBindigs_Map
	t = Transaction(doc, "Parameter Creation")
	t.Start() 

	bind_Map = doc.ParameterBindings.Insert(_exdef1, inst_bind, _paramGroup) 
	bind_Map = doc.ParameterBindings.Insert(_exdef2, inst_bind, _paramGroup) 

	t.Commit()
# END Parameter Creation -----------------------------------------------------------


# Start Transaction, outside the for loop 
t = Transaction(doc, "transfer SheetSize Paras from TitleBlock to Sheetview")
t.Start()


try:
	len(tblist) == len(shlist)
	
except:
	message = "len tblist is not len sheets list"
	print(message)
	 
 
for i in range(len(tblist)):  # example: tblist len = 5 -> 0,1,2,3,4 

	TBelem =tblist[i]
	# from Konrad func 
	if TBelem.get_Parameter(shwi).StorageType == StorageType.Double:
		valuewi = TBelem.get_Parameter(shwi).AsDouble() / 3.28
		valuehei = TBelem.get_Parameter(shhei).AsDouble() / 3.28  # /3.28 ft/m not needed here. Revit does it by itself
	else: print("not of type double") 

	sh= shlist[i] 
	
	sheight =  sh.LookupParameter("BLATTHOEHE")
	swidth = sh.LookupParameter("BLATTBREITE")

	if sheight and swidth: # if bhoehe und bbreite exist, 
		sheight.Set(("{:.3f}".format(valuehei)))
		swidth.Set(valuewi) # Set() returns True if set with new value 

t.Commit()



# "{:.3f}".format(valuehei)

# # FurterFiltering Methods for FEC in RevitAPI 
# Sheetheight_param_id = DB.ElementId(DB.BuiltInParameter.SHEET_HEIGHT)
# Sheetwidth_param_id = DB.ElementId(DB.BuiltInParameter.SHEET_WIDTH)

# height_para_prov = DB.ParameterValueProvider(height_param_id)

# print(height_para_prov)


# param_equality = DB.FilterNumericEquals()

# heigh_value_rule = DB.FilterDoubleRule(height_param_prov,
                                       # param_equality,
                                       # 10.0,
                                       # 1E-6)

# param_filter = DB.ElementParameterFilter(heigh_value_rule)


# walls = DB.FilteredElementCollector(doc) \
          # .WherePasses(param_filter) \
          # .ToElementIds()


# uidoc.Selection.SetElementIds(walls)


