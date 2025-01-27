''' Create SheetViews from EXCEL-File        
    v1.1 updated, cleaned up, put in function
    v.1.2 debugged 07.08.2018                
'''
from __future__ import print_function, division 

__title__ = "Sheets\nfrom Excel" 
__author__ = "Tillmann Baumeister" 


from Autodesk.Revit.DB import (FilteredElementCollector, Transaction,  
                    BuiltInParameter, ExternalDefinitionCreationOptions) 
from Autodesk.Revit import DB

import clr 
clr.AddReference("Microsoft.Office.Interop.Excel") 
import Microsoft.Office.Interop.Excel as Excel 
import System 
from System.Runtime.InteropServices import Marshal 


import sys, os 

from rpw.ui.forms import TaskDialog 
from pyrevit import forms 
from pyrevit import Forms 


doc = __revit__.ActiveUIDocument.Document
uiapp = __revit__
app = uiapp.Application  

#__shiftclick__ = True

#todo: CALC Open and REad -----------------------------------

# EXCEL OPEN and READ ---------------------------------------------------------
def lprint(list):
    for i in list: print(i) 


def pick_file(file_ext='', files_filter='', init_dir='',
              restore_dir = True, multi_file = False, unc_paths = False):
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


def excel_read(origin = "A3", worksheetname="Sheets"): 
    try:      
        # grab ActiveObject, if it is not available 
        xlapp = Marshal.GetActiveObject('Excel.Application')
        ws = xlapp.sheets(worksheetname) #Name of the Excel Worksheet 
    except EnvironmentError: 
        try: filepath = pick_file(file_ext='*') 
        except: sys.exit() 
        os.startfile(filepath) # startfile only works on windows, not unix 
        from time import sleep 
        sleep(1) 
        try:     
            xlapp = Marshal.GetActiveObject('Excel.Application')         
            ws = xlapp.sheets(worksheetname) #Name of the Excel Worksheet
        except: 
            forms.alert('Excel Application not open!\nOpen Excel file with worksheet "Sheets" ') 
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



def exc_writearray(origin = "A3", worksheetname= "Sheets"):
    originnr = [i for i in origin if i.isdigit()][0]
    end = len(ex_row) - 1 + int(originnr)               
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



# CREATE sheets and Titleblock2 from filtered excel_datalist
def createsheets(sheetlist): 
    message = [] 
    dic_sheetGuid = {} 
    t = Transaction(doc, "Create SheetViews from EXCEL") 
    try: 
        t.Start()
        for j in sheetlist:
            try: 
                tibl = dic_tibl[j[2]]   
            except: 
                mess1 = 'Error: TitleBlock1 "{}" not found'.format(j[2])
                message.append(mess1) 
                continue 
            a = DB.ViewSheet.Create(doc, tibl.Id) # ViewSheet Class, Create Method
            a.SheetNumber= j[0]  
            a.ViewName= j[1]     
            #dic_sheetGuid[a.SheetNumber] = str(a.UniqueId)   
            #create TitleBlock2 instance  
            message.append('--> {}-{}, TiBl1: {}'.format(a.SheetNumber, a.ViewName, j[2]) + mess2) 
        t.Commit()      
    except:             
        t.RollBack()    
        import traceback
        print(traceback.format_exc()) 
    return (message, dic_sheetGuid)



# EXCEL_row_filter: Filter out sheets already existing in Prj ------------
        #all() if all statements in list are true --> true, if one is none -> none
def ex_row_filter(list): 
    ex_row_create = [] 
    mess = []  
    for i in list:  
        if (i[0] and i[1] and i[2] #if i[2] in dic_tibl else False 
            and not [k for k in FECsheet if k.SheetNumber == str(i[0])]): 
            if i[2] in dic_tibl: 
                ex_row_create.append(i) 
                mess.append(i) 
            else: 
                mess1 = ' --> "{}" TiBl1 not found'.format(i[2]) 
                mess.append(str(i) + mess1) 
    return (ex_row_create, mess)



# ----------------------------------------------------------------------------

# FEC Collect Sheetviews
FECsheetls = FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Sheets) \
                     .WhereElementIsNotElementType() \
                     .ToElements()

dic_tibl1 = {i.SheetNumber : i for i in FECsheetls} 

#Filter out Placeholders 
FECsheet = [x for x in FECsheetls if x.CanBePrinted]

# FEC TitleBlocks in Project 
FECtibl = FilteredElementCollector(doc) \
                    .OfCategory(DB.BuiltInCategory.OST_TitleBlocks) \
                    .WhereElementIsElementType() \
                    .ToElements()

# CREATE dictionary TitleBlock: "FamilyType Name" : titleblockobj 
dic_tibl = {i.get_Parameter(DB.BuiltInParameter.SYMBOL_NAME_PARAM).AsString(): i for i in FECtibl}  

ex_row = excel_read()

sheetstocreate = ex_row_filter(ex_row)


#if sheetstocreate: # exist/ is not empty/ != 0

createsh = createsheets(sheetstocreate[0])

dic_tibl1 = {i.SheetNumber : i for i in FECsheetls}



def createtibl2(sheetlist):
    message = []
    t = Transaction(doc, "TitleBlock2")
    t.Start()                   
    for j in sheetlist:         
        sheet = dic_tibl1[j[0]]
        try:
            tibl_2 = dic_tibl[j[3]]
            tibl_2 = dic_tibl[j[3]]
            print(tibl_2.Name)
            newtitleblock = doc.Create.NewFamilyInstance(XYZ(0,0,0),tibl_2, sheet)
            print(newtitleblock)
            mess2 = '; TitleBlock2: {}'.format(str(j[3])) 
        except:
            import traceback
            print(traceback.format_exc())
            mess1 = 'Error: TitleBlock1 "{}" not found'.format(j[2]) 
            message.append(mess1)     
            mess2 = '; TitleBlock2: not found'
            pass
    t.Commit()


try:
    createtibl2(ex_row)
except KeyError:
    forms.alert("No second TitleBlock defined", ok=True)
except:
    pass



# OUTPUT -----------------------------------------------
if __shiftclick__:
    print("READ EXCEL DATA------------------------------------------")
    for i in ex_row: print(i) 

    print("\nTITLEBLOCKS IN PRJ ------------------------------------")
    if sheetstocreate[1]:
        for i in dic_tibl: print(i)

    print("\nSHEET-TO-CREATE LIST: ---------------------------------")
    for i in sheetstocreate[1]: print(i)

    print("\nSHEETS IN PROJECT: ", len(FECsheet))

    print("\nSHEETS CREATED: ---------------------------------------")
    if sheetstocreate[0]:
        for i in createsh[0]: print(i)


# -------------------------------------------------------------------

# message = [] 
# dic_sheetGuid = {} 
# row1 = ex_row[0] 
# j = row1
# tibl = dic_tibl[j[3]]
# mess1 = 'Error: TitleBlock1 "{}" not found'.format(row1[2]) 
# message.append(mess1)


# t = Transaction(doc, "Create SheetViews from EXCEL")  
# t.Start()
# a = DB.ViewSheet.Create(doc, tibl.Id) # ViewSheet Class, Create Method 
# a.SheetNumber = j[0]
# a.ViewName = j[1]
 #dic_sheetGuid[a.SheetNumber] = str(a.UniqueId)

# tibl_2 = dic_tibl[j[3]]
# print(j[3])

# newtitleblock = doc.Create.NewFamilyInstance(XYZ(0,0,0),tibl_2,a)

# t.Commit()

# mess2 = '; TitleBlock2: {}'.format(str(j[3]))
# mess2 = '; TitleBlock2: not found'
# message.append('--> {}-{}, TiBl1: {}'.format(a.SheetNumber, a.ViewName, j[2]) + mess2) 

# -------------------------------------------------------------------



# READ and SET SHEET_PARAMETER ---------------------------

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
    try:
        t = Transaction(doc, "Parameter Creation")
        t.Start() 
        bind_Map = doc.ParameterBindings.Insert(_exdef1, inst_bind, _paramGroupinProperty_enum) 
        t.Commit()
    except:
        import traceback
        print(traceback.format_exc())


# --- Inputs to SharedParameter CREATION ----------------------------------------
# _paramName_string = "man_Massstab" 	# ...can be anything, as string 
# _groupNameinSPfile_string  = "Plan"  	# ...can be anything ,as string: Ex."name"  Groupname in ParameterFile 
# _paramtype_enum  = DB.ParameterType.Text   # Enum, list of all Revit Parametertypes i.e. Text, Number, Length, Int, Area, YesNo, Angle
# _builtInCat_enum = DB.BuiltInCategory.OST_Sheets  	# Enum, contains all build in Paras
# _paramGroupinProperty_enum_ = DB.BuiltInParameterGroup.PG_TEXT 
# Enum, ParameterGroup in the property panel in Revit 


FECsheetls = FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Sheets) \
                    .WhereElementIsNotElementType() \
                    .ToElements() 

#Filter out Placeholders 
FECsheet = [x for x in FECsheetls if x.CanBePrinted]

firsttibl = FilteredElementCollector(doc) \
                    .OfCategory(DB.BuiltInCategory.OST_TitleBlocks) \
                    .WhereElementIsElementType() \
                    .FirstElement()

if not FECsheet:
    t = Transaction(doc, "SheetCreation")
    t.Start()
    DB.ViewSheet.Create(doc, firsttibl.Id) # ViewSheet Class, Create Method          
    t.Commit()    



try:
    #CREATE man_Massstab Parameter  
    if not FECsheet[0].LookupParameter("man_Massstab"): # FIX!!! There is no Sheet in Project
        createSharedPara("man_Massstab", "Plan", DB.ParameterType.Text,
                            DB.BuiltInCategory.OST_Sheets,
                            DB.BuiltInParameterGroup.PG_TEXT)
        print('\n--> "{}"  Shared Parameter created'.format("man_Massstab"))
except: pass




if not FECsheet[0].LookupParameter("PBrowser"): 
    createSharedPara("PBrowser", "Plan", DB.ParameterType.Text,
                        DB.BuiltInCategory.OST_Sheets,
                        DB.BuiltInParameterGroup.PG_GENERAL)
    print('\n--> "{}" Shared Parameter created'.format("PBrowser"))



#--- END SharedParameter Creation -----------------------------------------------------------

#### Create Project Parameters via the API --> currently not possible ##############################
# Employee jeremytammik
# in reply to: RankBIMS_Keris
# Re: Create Project Parameter(not shared parameter)
# Sorry, as far as I know these cannot be created programmatically.
# Update Sheet Parameter ----------------------------------------------------


def getnsetBIP(elem, bip, setvalue):
    if setvalue:
        try: para = elem.get_Parameter(bip) #BuiltInParameter.SHEET_WIDTH
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
    if isinstance(setvalue_string, str):
        para.Set(setvalue_string)
        return para.AsString()


def parameterupdate(exel_datalist):
    #Create a list from FECsheets matching ex_row_paralist in Project 
    # using SheetNR for Equality Check, do this with FEC?
    sheetviews = []
    excel_data = []
    for i in exel_datalist:
        if i[0] and i[1] and i[5]:
            for j in FECsheet: 
                if j.SheetNumber == i[0]:
                    sheetviews.append(j)
                    excel_data.append(i)
    #GUID BuiltInParameter ---------------------------
    sheet_issuedate = DB.BuiltInParameter.SHEET_ISSUE_DATE
    sheet_drawnby = DB.BuiltInParameter.SHEET_DRAWN_BY
    mess = []
    t = Transaction(doc, "update sheet parameters")
    t.Start()
    for i,j in zip(sheetviews, excel_data): 
        try: 
            date = getnsetBIP(i, sheet_issuedate, j[5])
            drawnby = getnsetBIP(i, sheet_drawnby, j[6])  
            man_massstab = getnsetSharedPara(i, "man_Massstab", j[7])  
            pbrowser = getnsetSharedPara(i, "PBrowser", j[4])  
            mess2 = '{}-{} --> PBrowser: {}, issue_date: {}, drawnby: {}, M: {}'.format(i.SheetNumber, i.Name, pbrowser, date, drawnby, man_massstab)
            mess.append(mess2)
        except: 
            error = 'Error '
            mess.append(error)
            import traceback
            print("\n",traceback.format_exc())
            continue
    t.Commit()
    return mess

mess = parameterupdate(ex_row)


# OUTPUT --------------------------
if __shiftclick__: 
    print("\nUPDATE SHEETVIEW PARAMETERS ---------------------------------------------")
    for i in mess: print(i)


# collect parameters  back from Sheets() 
# for i in FECsheets: 
# sheetname = get_para # and write them to ex_row list 
# create a array the size of ex_row list 
# write er_row 

#todo: Maybe Create TitleBlock2 separate from ViewSHeet Creation. To be able to change TB2 afterwards 
#todo: Show Altert Dialogs, for Errors, and Creation sucessful, 
# show print-box only when errors occurred. otherwise show nothing, for fast sheet creation. 
# todo: when SHIFT+Click run script: show all print messages. 

# todo: do it with a set. subtract sets, maybe its faster! try it! 
