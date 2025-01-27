""" transfer SheetSize Params from 
	TitleBlock to SheetView
	if not exist, add SharedPara SheetHeigt, SheetWidth to SheetView"""

__title__ = "transfer SheetSizeParas\ntoSheetView"
__author__ = 'Tillmann Baumeister'

# 10.05.2018; added comments, changed some german Names to english names 
# added Parameter Creation. 
import sys
from Autodesk.Revit.DB import * 
from Autodesk.Revit import DB
from decimal import  Decimal

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application

# --- TitlBlock Collector, SheetView- Collector -------------------------------

# GetBuiltIN parameter ID object from BuiltInParameterList (see Revit Docs, its a huge List)in DB namespace 
shwi = DB.BuiltInParameter.SHEET_WIDTH  
shhei = DB.BuiltInParameter.SHEET_HEIGHT

# Filter out TitleBlocks which width <= 21cm (No Sheet HEaders)
# FilterDoubleRule(ParameterValueProvider(), FilterNumericEquals),"ex.10.0", delta_x)
filter_double_rule = FilterDoubleRule(ParameterValueProvider(ElementId(shwi)),
                                       FilterNumericGreater(),
                                       0.21 * 3.28084,
                                       1E-2)

FECtitleblock = FilteredElementCollector(doc) \
            .WhereElementIsNotElementType() \
            .WherePasses(ElementParameterFilter(filter_double_rule)) \
            .ToElements()

tblist = FECtitleblock
shlist = [doc.GetElement(i.OwnerViewId) for i in tblist]

def createSP(_paramName, _groupName):
    # open SharedParameterFile 
    file = app.OpenSharedParameterFile() #throws error, no file chosen! 
    if file:
    # get GroupName in SharedParameter file, if not exist create new Group  
        group = file.Groups.get_Item(_groupName) 
        if group == None: 
            group = file.Groups.Create(_groupName) 
    else: 
        print "Error: No Shared Parameter File specified! " 
        sys.exit()
    # Create NewCategorySet()  
    catset = app.Create.NewCategorySet() 

    # Insert Category Objects in CatSet  <Autodesk.Revit.DB.Category object 
    catset.Insert(doc.Settings.Categories.get_Item(_builtincat)) # returns True

    # create an instance binding object with categoryset
    inst_bind = app.Create.NewInstanceBinding(catset)

    #ExternalDefinitionCreationOptions Class  excpects ( paraname as string, paratype object)
    #  An option class used for creating a new shared parameter definition,  
    ED_opt1 = ExternalDefinitionCreationOptions(_paramName, _paramtype)
    ED_opt1.Visible = True # True is the default value 

    # Create Parameter Definition Object 
    # Test if paraName is in SharedParam file , get Para Name Definition from file, else Create new Name 
    if group.Definitions.Contains(group.Definitions.Item[_paramName]):
        _exdef1 = group.Definitions.Item[_paramName] # create parameter definition object from Para in file
    else:
    # _def = group.Definitions.Create(_paramName, _paramType, _visible) 
        _exdef1 = group.Definitions.Create(ED_opt1) #Create para Definition object wit Ext

    #Create Parameter by inserting the Para Definition in the ParameterBindigs_Map
    t = Transaction(doc, "crete Parameter")
    t.Start() 
    bind_Map = doc.ParameterBindings.Insert(_exdef1, inst_bind, _paramGroup) 
    # bind_Map = doc.ParameterBindings.Insert(_exdef2, inst_bind, _paramGroup) 
    t.Commit()
    print "\nSharedParameter {} created!".format(_paramName)
    # END Parameter Creation -----------------------------------------------------------

# Inputs 
_paramName1 = "SHEETHEIGHT" # can be anything 
_paramName2 = "SHEETWIDTH" 
_groupName  = "Plan"  # ...can be anything , Groupname in ParameterFile 
_paramtype  = ParameterType.Number  # is a namespace, subnamespace from DB Namespace 
_builtincat = BuiltInCategory.OST_Sheets  # is a namespace, Enumeration Type 
_paramGroup = BuiltInParameterGroup.PG_IDENTITY_DATA # Namespace, subnamespace from DB,


if shlist:
    sh0 = shlist[0]
    testp1= sh0.LookupParameter("SHEETHEIGHT") 
    testp2 = sh0.LookupParameter("SHEETWIDTH") 

# test if Parameters BLATTHOEHE and BLATTBREITE exist in SheetViews. If not create them. 
    if not testp1:
        createSP(_paramName1, _groupName)
    if not testp2:
        createSP(_paramName2, _groupName)
else:
    print "No Sheet found"


# --- Transfer Parameters -------------------------------------
# Start Transaction, outside the for loop 
t = Transaction(doc, "transfer SheetSize Paras from TitleBlock to Sheetview")
t.Start()

try:
    len(tblist) == len(shlist)
    for i in range(len(tblist)):  #example: tblist len = 5 -> 0,1,2,3,4 
        TBelem =tblist[i]
        # from Konrad func
        if TBelem.get_Parameter(shwi).StorageType == StorageType.Double:
            valuewi = TBelem.get_Parameter(shwi).AsDouble() / 3.28084  
            valuehei = TBelem.get_Parameter(shhei).AsDouble() / 3.28084
        else: print("not of type double")

        sh= shlist[i]
        sheight =  sh.LookupParameter("SHEETHEIGHT")   
        swidth = sh.LookupParameter("SHEETWIDTH")   

        if sheight and swidth: # if bhoehe und bbreite exist, 
            sheight.Set(valuehei)  
            swidth.Set(valuewi) # Set() returns True if set with new value  
            print "Sheet: {0:<15s}, {1:<10s}: {2:<5.4f}/{3:<5.4f}" \
                        .format(str(sh.SheetNumber)+ "_"+ str(sh.Name), 
                                "Height/Width", valuehei, valuewi)

except:
    import traceback
    print traceback.format_exc() 
    try: t.RollBack() 
    except: pass

t.Commit()


