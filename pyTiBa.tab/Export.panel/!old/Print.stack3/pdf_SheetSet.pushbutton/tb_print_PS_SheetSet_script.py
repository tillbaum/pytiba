"""PDFsOut: - pdfOUT Selection in SheetSet Dialog
		   	"""
 
__title__ = "PDFOut_SheetSet"
	
__author__ = "TBaumeister" 	

import clr # import common language runtime .Net Laufzeitumgebung fuer .Net-anwendungen. / 
#um auf .Net Anwendungen zuzugreifen
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, View # don't need to import that
from System.Collections.Generic import List 

#clr.AddReference("RevitAPI") # .dll file 
from Autodesk.Revit.DB import * # FilteredElementCollector, OfClass, BuiltInCategory, Transaction, TransactionGroup
from pyrevit.script  import exit 
import pyrevit 
from pyrevit import forms 
from pyrevit import output
from pyrevit import revit, DB, UI
from pyrevit import script


from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, \
                           Separator, Button, CheckBox, Alert 

import os  
import sys
pyt_path = (r'C:\Program Files (x86)\IronPython 2.7\Lib') # must be imported in Dynamo Python node, see video GuiTalarico
sys.path.append(pyt_path)
# tb_path 
tblib_path = (r'E:\pyRevit\tblib')
sys.path.append(tblib_path)
import math
from time import sleep 

doc = __revit__.ActiveUIDocument.Document 
uidoc = __revit__.ActiveUIDocument 

### IMPORT END ##########################################################




### FUNCTIONS ###################################################################################

# func to print items in list, 
def lprint(ls):
	for i in ls: print(i) 

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
		return True



# DELETE tempSetName ViewSet -
FECviewSets=FilteredElementCollector(doc).OfClass(ViewSheetSet).ToElements()
try:
	for i in FECviewSets: #TODO: for loop not required, can be done with FEC
		if i.Name== "tempSetName":
			t = Transaction(doc, "Delete tempSetName_viewset")
			t.Start()
			doc.Delete(i.Id)
			t.Commit()
			print("tempsetName deleted" )
			break 
except:
	print("except Error: tempsetname not deleted")
	pass

# if __shiftclick__:
    # print(" SHIFT CLICK MESSAGE")

# Get PrintSetting "!temp", if not exist, create it 
# Could have also done it with FEC OfClass(PrintSettings)
	#doc.GetPrintSettingIds() Set of al PrintSettings, Method of doc. 
printsettingelems = [ doc.GetElement(i) for i in doc.GetPrintSettingIds() ] # returns a List with Ids
temp_printsetting = [ i for i in printsettingelems if i.Name.Equals("!temp")]
if not temp_printsetting: 
	# Create the PrintSetting /PrintSetup with SaveAs-Method 
	t = Transaction(doc, "test") 
	t.Start() 
	doc.PrintManager.PrintSetup.SaveAs("!temp") # Saves the PrintSetting #Error the InSessionPrintSetting cannot be saved 
	t.Commit()
	printsettingelems = [ doc.GetElement(i) for i in doc.GetPrintSettingIds() ]
	temp_printsetting = [ i for i in printsettingelems if i.Name.Equals("!temp")]
	print(" !temp Printsetting Created!" )
tmp_printsetting = temp_printsetting[0]




#--- ELEMENT SELECTION ----------------------------------------
# selec_ids = uidoc.Selection.GetElementIds()
# New List containing only Sheets 
# selec_el = [doc.GetElement(i) for i in selec_ids if doc.GetElement(i).GetType()==ViewSheet ] 
#---END ELEMENT SELECTION -------------------------------------

### FEC VIEWsets -----------------------------------------------------
#FECviewsets = FilteredElementCollector(doc).OfClass(ViewSheetSet) \
#						.ToElements()

sel_shset = forms.select_viewsheetset()
#comment: runs the func select_viewsheetset in forms\__init__* modified by tb 

if not sel_shset:
	pyrevit.script.exit()

viewlist = list(sel_shset[0].Views)

#for i in sel_shset[0].Views: print(i.Name)



# ---FILENAME --------------------------------------------------------------------
# TIME + Date 
from datetime import datetime  # considers Sommer and Winter Time 
# datetime.datetime.now() 
m = datetime.now()
date = "%d-%m-%y" # 05-06-18 leading 0
time = "%H.%M"		#20.15
m.strftime(date) #stringformattime fun
m.strftime(time) 


dirpath = r'C:\Users\Till\Desktop' # can be anything, gets overwritten by pdfPrinter 
						# is Set in Printer Properties, used either AdobePDF or PDFCreator, both work. 
filepathlist = []
filenamelist = []
tmp_fp = [] 
for v in viewlist: 
	paraval_nr = lookupparaval(v, "Sheet Number") 
	paraval_revision = lookupparaval(v, "man_Index") 
	paraval_name = lookupparaval(v, "Sheet Name") 
	sep = "_" 
	tmp_fn = sep.join([ str(paraval_nr), str(paraval_revision) if paraval_revision else "", 
					str(paraval_name), m.strftime(date), m.strftime(time)])
	filenamelist.append(tmp_fn)
	filepathlist.append(dirpath + "\\" + tmp_fn + ".pdf")



# Papersize Obj LIST---########################################################################

# ex: round_up(1.12222, 0.05) = 1.15 0.297 
def round_up(x, a):
    return math.ceil(x / a) * a # TEST rundet down. ???
#ToDO: other method 


#Create Dic from printForms ----------------------------
#TODO: use pickl Module to write dic_ps to file, And Load it back, when script run!  
papersizeset = doc.PrintManager.PaperSizes
psset_sorted = sorted(papersizeset, key = lambda x: x.Name)
dic_ps = {}
for i in psset_sorted: 
	if i.Name[0].isdigit():  # only papersize obj with name "90x50", no "Letter" or "ARCH A" Obj.
		dic_ps[ i.Name ] = i 
	# elif i.Name in ["A1", "A2", "A3", "A4"]: # doesn't work yet. 
			# dic_ps[ a ] = iter.Current

#Create Dic from printForms, as function --------------#to be tested 
def create_papersize_dic(doc):
	papersizes = doc.PrintManager.PaperSizes
	iter = papersizes.ForwardIterator()
	iter.Reset()
	dic_ps = {} 
	while iter.MoveNext():
		#print(iter.Current.Name)
		a = iter.Current.Name
		if a[0].isdigit():  # only papersize obj with name "90x50", no "Letter" or "ARCH A" Obj.
			dic_ps[a ] = iter.Current
		#elif a in ["A1", "A2", "A3", "A4"]: 
			#dic_ps[a ] = iter.Current
	iter.Reset()
	return dic_ps 
#TODO: use pickl Module to write dic_ps to file, And Load it back, when script run!  


# Creat PaperSize_Object-List:  Matching TitleBlock_Sheet_Sizes with PaperSize_Forms

#Create Dic from printForms ----------------------------
#TODO: use pickl Module to write dic_ps to file, And Load it back, when script run!  
papersizeset = doc.PrintManager.PaperSizes
psset_sorted = sorted(papersizeset, key = lambda x: x.Name)
dic_ps = {}
for i in psset_sorted: 
	if i.Name[0].isdigit():  # only papersize obj with name "90x50", no "Letter" or "ARCH A" Obj.
		dic_ps[ i.Name ] = i 
	# elif i.Name in ["A1", "A2", "A3", "A4"]: # doesn't work yet. 
			# dic_ps[ a ] = iter.Current


# Creat PaperSize_Object-List:  Matching TitleBlock_Sheet_Sizes with PaperSize_Forms
bip_shwi = BuiltInParameter.SHEET_WIDTH  
bip_shhei = BuiltInParameter.SHEET_HEIGHT
psmess = [] 
papersizeobjls = [] 
ind_nops=[]
for i,v in enumerate(viewlist): 
	# Get TitleBlock with Para Sheet_Width > 21cm 
		# FilterDoubleRule(ParameterValueProvider(), FilterNumericEquals),"ex.10.0", delta_x)
	filter_double_rule = FilterDoubleRule(ParameterValueProvider(ElementId(bip_shwi)),
                                       FilterNumericGreater(),
                                       0.21 * 3.28084,
                                       1E-2)
	FECtb = FilteredElementCollector(doc, v.Id) \
			.WherePasses(ElementParameterFilter(filter_double_rule)) \
          	.ToElements()
				
	val_wi = FECtb[0].get_Parameter(bip_shwi).AsDouble() / 3.28084 # feet to Meter conversion: 1 ft = 1/3.28 m
	val_hei = FECtb[0].get_Parameter(bip_shhei).AsDouble() / 3.28084
	wi = int(round_up(val_wi, 0.05) *100)  
	hei = int(round_up(val_hei, 0.05) *100)  
	shsize_str = str(wi) + "x" + str(hei) 
	mess= []
	mess.append(shsize_str)
	# find a matching papersize, 
	cntr =0 
	while shsize_str not in dic_ps and cntr < 9: 
		if cntr % 3 == 0: 	# not cntr % 3: meaning if False == False;  0%3 = 0  1%3 = 1, 2%3 = 2, 3%3=0, 4%3=1, 5%3=2 ... 
			shsize_str = ''.join([str(wi), 'x' ,str(hei + 5)])
			mess.append(shsize_str) 
			cntr += 1 
		elif cntr % 3 == 1: 
			shsize_str = str(wi + 5) + "x" + str(hei)
			mess.append(shsize_str)
			cntr += 1
		else: # cntr % 3 == 2:
			wi = wi + 5
			hei = hei + 5
			shsize_str = str(wi) + "x" + str(hei)
			mess.append(shsize_str)
			cntr += 1

	if shsize_str in dic_ps: 	
		papersize_el = dic_ps[shsize_str]
		papersizeobjls.append(papersize_el)
	else: 
		papersize_el = dic_ps["90x90"]
		papersizeobjls.append(papersize_el)
		mess.append(" no match ")
	psmess.append(mess)




#---START of printFunction ----------------------------------------------------------------------------------------------------
# only prints one sheet at a time, creates Viewset with one Sheet, This is done to be able
# to provide a specific filename. 
# a printsetting !temp is permanently used for pdf printing.
#  this can be used to edit futher print parameters in an edit dialog. or 

def printview(doc, sheet, filepath , papersizeobj, pdfprinterName, combined, \
				 tmp_printsettingf): 
	# create new_view set class 
	new_viewset = ViewSet() #ViewSet Class
	new_viewset.Insert(sheet) 
	# determine print range to Select option 
	printmanager = doc.PrintManager 
	printmanager.PrintRange = PrintRange.Select  # PrintRange is a own subclass of DB 
	printmanager.Apply()   
	# make the new_viewset current 
	viewSheetSetting = printmanager.ViewSheetSetting 
	viewSheetSetting.CurrentViewSheetSet.Views = new_viewset 
	# set pdfprinterName = PDFCreator, Adobe PDF ..
	printmanager.SelectNewPrintDriver(pdfprinterName) 
	printmanager.Apply()
	# set combined and print to file, combined is not relevant, since only 1 sheet gets printed 
	if printmanager.IsVirtual: # THIS lines have to be executed, that Revit prints to given filepath 
		printmanager.CombinedFile = combined #=True by default, makes no difference, since
		printmanager.Apply()				# every sheet is printed in "tempSetName" ViewSheetSet 
		printmanager.PrintToFile = True	# after Setting manually PrintToFile is still false, has to do with pdfprinter
		printmanager.Apply() 
	else: # Is this needed 
		printmanager.CombinedFile = combined
		printmanager.Apply()
		printmanager.PrintToFile = False
		printmanager.Apply()
	# set file path, 
	while os.path.exists(filepath):
		filepath = filepath.replace(".pdf", "_.pdf")
		#countr += 1 #geht aber  futher Tests necessary! 
	printmanager.PrintToFileName = filepath #as string , add filend that pdf_Name
	printmanager.Apply()						# fn must be different, everytime SubmitPrint() is called. else Exception; file exists 
	#---Papersizes ----------------------------------------
	# Set CurrentPrintSetting to "!temp"-Setting and save, #Set PaperSize in PrintSetup/PrintSetting
	message1 = ""
	_printsetup = printmanager.PrintSetup
	t = Transaction(doc, "test1")
	t.Start() 
	_printsetup.CurrentPrintSetting = tmp_printsettingf # "!temp"; Sometimes needs an TransactionProcess, Sometimes not
	_printsetup.CurrentPrintSetting.PrintParameters.PaperSize = papersizeobj # doesnt need a Transaction 
	_printsetup.CurrentPrintSetting.PrintParameters.PageOrientation = PageOrientationType.Portrait #doesn't need a Transaction 
	try: #if there are no changes to the PrintSetup obj (ie. PrintSettings or PrintParameters)
		 # .Save() method throws an exception
		_printsetup.Save()
	except:
		message1 = "Error Saving _printsetup ,"
		pass
	t.Commit()
	# save settings and submit print 
	t = Transaction(doc, "Testprint") #each Transaction must have a name. else: Error 
	t.Start()
	try: 
		viewSheetSetting.SaveAs("tempSetName")
		printmanager.Apply()
		printmanager.SubmitPrint()
		t.RollBack()
		sleep(3) # 3 sec, necessary because PDF Printer will cause error when many docs submitted to fast.
		#viewSheetSetting.Delete()
		errorReport = "Sucess"
	except:
		t.RollBack()
		import traceback
		errorReport = traceback.format_exc()
		print(errorReport)
	#t.Commit()
	mess = message1 + errorReport
	return  mess

#TODO: t.Rollback(), Instead of commiting, Roll it Back, proposition in Forum, done 
#TODO: Dialog for sheet Selection, if Selection is empty, open Dialog, done 
#TODO: Select views from Project Browser, done 
#ToDO: If Papersize_obj could not be found, python fails to print any sheet at all, done 10.06.2018
#TODO: If Select Sheets Dialog is Excaped of closed: stop script, close window()
#ToDO:	

# print("\n VIEWLIST-.Name -------------")
# for i in viewlist: print(i.SheetNumber, i.Name)

# print("--- FilePathList-------------------------------")
# for i in filenamelist : print(i)
# fp0 = filepathlist[0]

# print("--PaperSize_Obj--------------------------------")
# for i in ps_mess: print(i)
# print("-------------------------------")

fmt = '{:<16}  {:<35}  {}'

print(fmt.format( " Viewlist---------", " FilePathList------------", "PaperSizeList-----------------"))
print ""
for v,fp, ps in zip(viewlist, filenamelist, ps_mess):
	print fmt.format(v.SheetNumber + " " + v.Name, fp, ps)

print("-------------------------------------------------------------")

#remove colums in viewlist and filepathlist with no matching papersizeObj
if ind_nops: 
	for i in reversed(ind_nops): 
		viewlist.pop(i) 
		filepathlist.pop(i) 

for v, fp, ps in zip(viewlist, filepathlist, papersizeobj_list):
	print(v.Name, fp, ps.Name) 

#---INPUT----------------------------------------
pdfprinterName = "PDFCreator" 
combined = True #default, since 1 sheet per print function 

print("\n LoopPrint, printer: {} -----------------------------".format(pdfprinterName))

# Print List of views -------------------------------------------
try:
	if isinstance(viewlist, list):
		for v, fp, ps in zip(viewlist, filepathlist, papersizeobj_list):
			pview = printview(doc, v, fp ,ps ,pdfprinterName, combined ,tmp_printsetting)
			print(pview)
	else: 
		print "Error: viewlist not exist "
except:
	# if error accurs anywhere in the process catch it
	errorReport = traceback.format_exc()
	print(errorReport)


