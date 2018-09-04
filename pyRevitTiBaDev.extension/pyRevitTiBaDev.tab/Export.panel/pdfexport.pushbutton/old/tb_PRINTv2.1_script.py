"""PDFsOut: - Active Sheet Selection in ProjectBrowser
		   	  or, if nothing selected,
            - Selection in Sheet-Selection-Dialog
			- v2.1 machtPaperSize works with A0,A0+,A0++,A0+++, A1, A2, A3; PrintForms added
			- v2.1 SheetSelectDialog: pdfPrinter must be selected from Revit Print Dialog now.
			- v2.1 added set page_orientation.Portrait """

from __future__ import division

__title__ = "Pdf\nExport"

__author__ = "TBaumeister" 	

# TODO, CHECK Imports, what do I need??
from Autodesk.Revit.DB import (FilteredElementCollector, Transaction, 
			BuiltInParameter ,ExternalDefinitionCreationOptions )
from Autodesk.Revit import DB
from Autodesk.Revit.DB import *

import clr # import common language runtime .Net Laufzeitumgebung 
				#fuer .Net-anwendungen; um auf .Net Anwendungen zuzugreifen
from System.Collections.Generic import List 
#from System.Windows import Forms #

#( FilteredElementCollector, BuiltInCategory, Transaction, TransactionGroup, OfClass)
import pyrevit 
from pyrevit import forms 
import rpw.ui.forms as rpwforms # FlexForm, Label, ComboBox, TextBox, \
								# Separator, Button, CheckBox, Alert 
# for timing ------------------------------------------------
from pyrevit.coreutils import Timer
timer = Timer()
from pyrevit import HOST_APP, EXEC_PARAMS
from pyrevit.compat import safe_strtype  # Func
#from pyrevit import coreutils
#from pyrevit.coreutils.logger import get_logger
from pyrevit import framework
from pyrevit.framework import System
#from pyrevit.framework import Threading 
from pyrevit.framework import Interop #What is this?? Excel Interop??  
from pyrevit.framework import wpf, Forms, Controls, Media  # needed?
from pyrevit.api import AdWindows 
from pyrevit import revit, UI
import pyrevit.forms 

import sys
import os
pyt_path = (r'C:\Program Files (x86)\IronPython 2.7\Lib') 
sys.path.append(pyt_path)
# tb_path 
tblib_path = (r'E:\pyRevit\tblib')
sys.path.append(tblib_path)
pyrevitpath = r"E:\pyRevitv4.5\pyRevit\pyrevitlib"
sys.path.append(pyrevitpath)
import string #?
import math	 # math.ceil
import time # sleep() 
import traceback 
import cPickle as pickle 
from functools import wraps
#from collections import OrderedDict 
#import threading

#logger = get_logger(__name__) 

DEFAULT_INPUTWINDOW_WIDTH = 500
DEFAULT_INPUTWINDOW_HEIGHT = 400

doc = __revit__.ActiveUIDocument.Document 
uidoc = __revit__.ActiveUIDocument 

#when running in RPS
try:
	__file__
except NameError: 
	__file__ = "E:\\pyRevit\\tblib\\"

#*** Assign ListContent to multiple variables 
# Revit usage: Sheetlist of size 5: v0 = sheetlist[0], v1 = ....
def list2var(list, string = "a"):
    for i,j in enumerate(list):
        globals()['{}{}'.format(string, i)] = j
    print "len(list)= ",len(list)

# func to print items in list, 
def lprint(ls):
	for i in ls: print(i) 

def pick_folder():
    fb_dlg = Forms.FolderBrowserDialog()
    if fb_dlg.ShowDialog() == Forms.DialogResult.OK:
        return fb_dlg.SelectedPath

class SelectFromCheckBoxes(framework.Windows.Window): 
    """ tb_Modified Standard form to select from a list of check boxes.
    """
    xaml_source = 'tb_SelectFromCheckboxes.xaml' 

# copied from TemplateUserInputWindow ---------------------------
    def __init__(self, context,
                 title='User Input',
                 width=DEFAULT_INPUTWINDOW_WIDTH,
                 height=DEFAULT_INPUTWINDOW_HEIGHT, **kwargs):
        """Initialize user input window."""
        wpf.LoadComponent(self, os.path.join(os.path.dirname(__file__), self.xaml_source))
        self.Title = title
        self.Width = width
        self.Height = height
		# WindowStartup Position Window hast Left + Top Property. 
        self.Left = System.Windows.SystemParameters.FullPrimaryScreenWidth / 2 - self.Width /2
        self.Top = 80

        self._context = context #private attr.
        self.response = None 	#see select button

        def handle_ESCinput_key( sender, args):
            """Handle Escape keyboard input"""
            if args.Key == framework.Windows.Input.Key.Escape:
                self.Close()
                sys.exit() #TODO! sysExit. READ
        self.PreviewKeyDown += handle_ESCinput_key # ESC closes the form

		# in def setup( **kwargs)
        self.hide_element(self.clrsearch_b) # func in WPFWindow
        self.search_tb.Focus()

        self.checked_only = kwargs.get('checked_only', False) # get() builtin

        button_name = kwargs.get('button_name', None)
        if button_name:
            self.select_b.Content = button_name
        self.list_lb.SelectionMode = Controls.SelectionMode.Extended
        self._verify_context()
        self._list_options()
	
        printername = doc.PrintManager.PrinterName

		#tb_ADDED: Values from Checkbox and Textinput --------------------------
        self.dic_dlgval = {}
        with open(os.path.dirname(__file__) + "\\dlgval.pkl", "a+b") as f: # create and read
            f.seek(0)
            try:
                self.dic = pickle.load(f)
            except: print "run again"
        try: 
            self.dic # if dic not exists -> Except clause 
            #print self.dic # testing
            self.txtbox_paranames.Text = self.dic["paranames"]
            self.expander.Header += self.dic["paranames"]
            self.txtbox_printername.Text = printername  #self.dic["printername"]
			
            self.lb_printfilepath.Content = self.dic["printfilepath"]
            self.chbox_output.IsChecked = self.dic["output"]
            self.chbox_pdfexport.IsChecked = self.dic["pdfexport"]
        except:
            import traceback
            errorReport = traceback.format_exc()
            print(errorReport) 
			#Standard Dialog Values
            self.txtbox_paranames.Text = "Sheet Number,-,Sheet Name"
            self.expander.Header += "Sheet Number,_,Sheet Name"
            self.chbox_output.IsChecked = True
            
# copied from WMFWindow
    @staticmethod # e.g can be applied to the class and the instance, both
    def hide_element(*wpf_elements):
        """Collapse elements.

        Args:
            *wpf_elements (str): element names to be collapsed
        """
        for el in wpf_elements:
            el.Visibility = framework.Windows.Visibility.Collapsed

    @staticmethod
    def show_element(*wpf_elements):
        """Show collapsed elements.

        Args:
            *wpf_elements (str): element names to be set to visible.
        """
        for el in wpf_elements:
            el.Visibility = framework.Windows.Visibility.Visible

    @staticmethod
    def toggle_element(*wpf_elements):
        """Toggle visibility of elements.

        Args:
            *wpf_elements (str): element names to be toggled.
        """
        for el in wpf_elements:
            if el.Visibility == framework.Windows.Visibility.Visible:
                self.hide_element(el)
            elif el.Visibility == framework.Windows.Visibility.Collapsed:
                self.show_element(el)

	# copied from TemplateUserInputWindow
    # def handle_ESCinput_key(self, sender, args):
        # """Handle Escape keyboard input"""
        # if args.Key == framework.Windows.Input.Key.Escape:
            # self.Close()
            # sys.exit() #TODO! sysExit. READ
# copied from TemplateUserInputWindow END ---------------------

    def _verify_context(self): 
        new_context = []
        for item in self._context:
            if not hasattr(item, 'state'):
                new_context.append(BaseCheckBoxItem(item))
            else:
                new_context.append(item)

        self._context = new_context

    def _list_options(self, checkbox_filter=None):
        if checkbox_filter:
            self.checkall_b.Content = 'Check'
            self.uncheckall_b.Content = 'Uncheck'
            self.toggleall_b.Content = 'Toggle'
            checkbox_filter = checkbox_filter.lower()
            self.list_lb.ItemsSource = \
                [checkbox for checkbox in self._context
                 if checkbox_filter in checkbox.name.lower()]
        else:
            self.checkall_b.Content = 'Check All'
            self.uncheckall_b.Content = 'Uncheck All'
            self.toggleall_b.Content = 'Toggle All'
            self.list_lb.ItemsSource = self._context

    def _set_states(self, state=True, flip=False, selected=False):
        all_items = self.list_lb.ItemsSource
        if selected:
            current_list = self.list_lb.SelectedItems
        else:
            current_list = self.list_lb.ItemsSource
        for checkbox in current_list:
            if flip:
                checkbox.state = not checkbox.state
            else:
                checkbox.state = state

        # push list view to redraw
        self.list_lb.ItemsSource = None
        self.list_lb.ItemsSource = all_items

    def toggle_all(self, sender, args):
        """Handle toggle all button to toggle state of all check boxes."""
        self._set_states(flip=True)

    def check_all(self, sender, args):
        """Handle check all button to mark all check boxes as checked."""
        self._set_states(state=True)

    def uncheck_all(self, sender, args):
        """Handle uncheck all button to mark all check boxes as un-checked."""
        self._set_states(state=False)

    def check_selected(self, sender, args):
        """Mark selected checkboxes as checked."""
        self._set_states(state=True, selected=True)

    def uncheck_selected(self, sender, args):
        """Mark selected checkboxes as unchecked."""
        self._set_states(state=False, selected=True)

    def button_select(self, sender, args):
        """Handle select button click."""
        if self.checked_only:
            self.response = [x.item for x in self._context if x.state]
        else:
            self.response = self._context
        #tb folowing lines added!
        self.dic_dlgval["paranames"] = self.txtbox_paranames.Text
        self.dic_dlgval["printername"] =  self.txtbox_printername.Text
        self.dic_dlgval["output"] = self.chbox_output.IsChecked
        self.dic_dlgval["pdfexport"] = self.chbox_pdfexport.IsChecked
        self.dic_dlgval["printfilepath"] = self.lb_printfilepath.Content
        self.Close()

    # tb previewbutton: breview_b
    def preview_click(self, sender, event):
        ''' Handle Preview Button click '''
        str2list = self.txtbox_paranames.Text.split(',')
        #stripwhitespacefrlistelem = list(map(str.strip, str2list))
        paranameseval = namefromparalist(FilteredElementCollector(doc)
									.OfClass(ViewSheet).FirstElement(),str2list)
        self.lb_txtbox_preview.Text = paranameseval

    def pickprintfolder(self, sender, event):
        self.lb_printfilepath.Content = pick_folder()

    def checkdwgexport(self, sender, event):
        print "dwgCheck"

    def search_txt_changed(self, sender, args):
        """Handle text change in search box."""
        if self.search_tb.Text == '':
            self.hide_element(self.clrsearch_b)
        else:
            self.show_element(self.clrsearch_b)

        self._list_options(checkbox_filter=self.search_tb.Text)

    def clear_search(self, sender, args):
        """Clear search box."""
        self.search_tb.Text = ' '
        self.search_tb.Clear()
        self.search_tb.Focus()

class BaseCheckBoxItem(object):
    """Base class for checkbox option wrapping another object."""

    def __init__(self, orig_item):
        """Initialize the checkbox option and wrap given obj.

        Args:
            orig_item (any): object to wrap (must have name property
                             or be convertable to string with str()
        """
        self.item = orig_item
        self.state = False

    def __nonzero__(self):
        return self.state

    def __str__(self):
        return self.name or str(self.item)

    @property
    def name(self):
        """Name property."""
        return getattr(self.item, 'name', '') #getattr() python built in func 

    def unwrap(self):
        """Unwrap and return wrapped object."""
        return self.item

class SheetOption(BaseCheckBoxItem):
    def __init__(self, sheet_element):
        super(SheetOption, self).__init__(sheet_element)

    @property
    def name(self):
        return '{} - {}{}' \
            .format(self.item.SheetNumber,
                    self.item.Name,
                    ' (placeholder)' if self.item.IsPlaceholder else '')

    @property
    def number(self):
        return self.item.SheetNumber

#func lookuppara; paraname as string: ex: "Sheet Number"
#TODO: maybe replace with orderedParameters, or ParameterSet, 
def lookupparaval(element, paraname): 
	try: newp = element.LookupParameter(paraname)
	except: newp = None; pass 
	if newp:
		if newp.StorageType == StorageType.String:    value = newp.AsString()
		elif newp.StorageType == StorageType.Integer: value = newp.AsInteger()
		elif newp.StorageType == StorageType.Double:  value = newp.AsDouble()
		return value
	else: return False

def namefromparalist(view, paralist):
	import datetime
	m = datetime.datetime.now()
	date = m.strftime("%d-%m-%y") #stringformattime fun
	time = m.strftime("%H.%M")
	tmp_filenamelist = []
	for i in paralist: 
		if i in ['_', ' ', '.', '-', ';']:
			tmp_filenamelist.append(i)
		elif i in ["date", "time"]:
			datetime = m.strftime(eval(i))
			tmp_filenamelist.append(datetime)
		#elif i in ["%d","%m","%y","%Y","%H","%M"]:
		elif i.startswith("%"):
			try:
				datetime = m.strftime(i)
				tmp_filenamelist.append(datetime)
			except: pass
		elif lookupparaval(view, i):
			lookupval = lookupparaval(view, i)
			# str(lookupval) if lookupval else '' 
			tmp_filenamelist.append(str(lookupval) if lookupval else '')
		else: 
			tmp_filenamelist.append(i)
	filename = ''.join(tmp_filenamelist)
	return filename

def pdfnamelist(viewlist, paralist, dirpath = ''):
	filepathlist = []
	filenamelist = []
	for v in viewlist: 
		tmpname = namefromparalist(v, paralist)
		tmpname += ".pdf" 
		filenamelist.append(tmpname)
		filepathlist.append(dirpath + "\\" + tmpname )
	return (filepathlist, filenamelist)

# namels = pdfnamelist(viewlist, paralist)
# print(namels)


def open_dic(fn="dlgval.pkl"):
	dic1 = {"ouput": True, "paranames": 'Sheet Number,_,Sheet Name',"printername": "PDFCreator"}
	with open(os.path.dirname(__file__) + "\\" + fn, "a+b") as f: # create and read
		f.seek(0)
		try:
			dic = pickle.load(f)
			return dic
		except: return dic1

# write dialogData from input boxes as dictionary.
def write_dic(newdic, olddic=open_dic(), fn= "dlgval.pkl"):
	if newdic and not newdic == olddic:
		with open(os.path.dirname(__file__) + "\\" + fn, "wb") as f:
			pickle.dump(newdic, f)


def selectsheets2print():
	all_sheets = DB.FilteredElementCollector(doc).OfClass(DB.ViewSheet) \
                   .WhereElementIsNotElementType().ToElements()
	all_sheets = [i for i in all_sheets if not i.IsPlaceholder]
	sortlist = sorted([SheetOption(x) for x in all_sheets], key=lambda x: x.number)
	selsheet = SelectFromCheckBoxes(sortlist, title = "Select Sheets",
						width = 500, height = 400, 
						button_name = "Select / PRINT")
	selsheet.ShowDialog() #.Net Method, Modal Window, no other window is active
	write_dic(selsheet.dic_dlgval)
	if selsheet.response:
		return ([i.item for i in selsheet.response if i.state], selsheet.dic_dlgval)
	else: 
		sys.exit() #selsheet.response does not exist 

#--- ELEMENT SELECTION ----------------------------------------
selec_ids = uidoc.Selection.GetElementIds()
selec_el = [doc.GetElement(i) for i in selec_ids if doc.GetElement(i) \
			.GetType()==ViewSheet ] 

output = True 
if selec_el: #exist: 1 or 2, or 3 or ... , not 0
	viewlist = selec_el
	dlgdic = open_dic()
	ouput = dlgdic["output"]
	pdfexport = dlgdic["pdfexport"]
else: 
	viewlist, dlgdic = selectsheets2print()
	output = dlgdic["output"] # True or False 
	pdfexport = dlgdic["pdfexport"]
if not viewlist: 
	sys.exit() #pyrevit.script.exit() 



### FUNCTIONS ############################################################

# ---FILENAME -------------------------------------------------------

# example: round_up(1.12222, 0.05) = 1.15 0.297 
def round_up(x, a):
    return math.ceil(x / a) * a # TEST rundet down. ???
#ToDO: other method : round_up(0.2078, 0.005) ; returns 0.20999999 

# Creat PaperSize_Object-List: Matching TitleBlock_Sheet_Size with PaperSize in 
	# Revit doc.PrintManager.PaperSizes, (a Set) -> WinPrintForms
def matchPaperSize(viewlist, pdfPrinterName, counterlimit = 7):
	#create dictionary from PaperSizeSet - class
	doc.PrintManager.SelectNewPrintDriver(pdfPrinterName) #line needed, 
												# when a non-pdf printer is set up.
	papersizeset = doc.PrintManager.PaperSizes
	#dic_ps = {i.Name: i for i in papersizeset if i.Name[0].isdigit()}
	dic_ps = {}
	# put it in try statement because Foxitpdfprinter hat a form with Blank Name, None  -> Error
	for i in papersizeset: 
		try:
			if i.Name[0].isdigit(): #or i.Name in ["119x84.5 A0", "59.5x42 A2", "84.5x59.5 A1" ]: 
				dic_ps[i.Name]= i
		except: pass
	bip_shwi =  BuiltInParameter.SHEET_WIDTH  
	bip_shhei = BuiltInParameter.SHEET_HEIGHT
	psmess = []; papersizeobjls = []; 
	try:
		for i,v in enumerate(viewlist):
			# Get TitleBlock with Para Sheet_Width > 20 cm 
			# note: FilterDoubleRule(ParameterValueProvider(), FilterNumericEquals),
			# "ex.10.0", delta_x)
			filter_double_rule = \
						FilterDoubleRule(ParameterValueProvider(ElementId(bip_shwi)), \
						FilterNumericGreater(), 0.20 / 0.3048, 1E-2)
			FECtb = FilteredElementCollector(doc, v.Id) \
						.WherePasses(ElementParameterFilter(filter_double_rule)) \
						.ToElements()
			bip_wi = int(FECtb[0].get_Parameter(bip_shwi).AsDouble() * 0.3048 *1000) 	# from m to cm
			bip_hei = int(FECtb[0].get_Parameter(bip_shhei).AsDouble() * 0.3048 *1000)
			# print bip_wi, bip_hei , float(bip_wi), float(bip_hei), int(bip_wi), int(bip_hei) 
			# cut of all irelevant  0.750000011 = 750 mm
			wi_cm = bip_wi / 10 	#__future__ division ex: 297 / 10 = 29.7 
			hei_cm = bip_hei / 10
			shsize_str = ''.join([str(wi_cm), "x", str(hei_cm)])
			shsize_str_round = ''.join([str(round_up(wi_cm, 0.5)), "x", str(round_up(hei_cm, 0.5))]) 
			mess = []
			mess.append(shsize_str)
			# Check if original sheetformat or sheetformat roundedUp by 0.5cm is in papersize dic
			try:
				if any([papersizeobjls.append(dic_ps[i]) for i in [shsize_str, shsize_str_round] if i in dic_ps]):
					mess.append('match--> worked')
					mess.append(i)
					psmess.append(mess)
					print " any() worked"
					continue	# go back to header of for loop/ continue with for loop 
			except: print "any didn' work"
			# round to cm values 45.11 --> 50 , 73.0 --> 75 
			wi= int(round_up(wi_cm, 5))
			hei = int(round_up(hei_cm, 5))
			shsize_str = ''.join([str(wi), "x", str(hei)])
			mess.append(shsize_str)
			cntr = 0
			while shsize_str not in dic_ps and cntr < counterlimit:
				if cntr % 3 == 0: 	# 0%3 = 0  1%3 = 1, 2%3 = 2, 3%3=0, 4%3=1, 5%3=2 ... 
					shsize_str = ''.join([str(wi), 'x' ,str(hei + 5)])
					mess.append(shsize_str) 
					cntr += 1 
				elif cntr % 3 == 1: 
					shsize_str = ''.join([str(wi + 5), "x", str(hei)])
					mess.append(shsize_str)
					cntr += 1
				else: # cntr % 3 == 2:
					wi = wi + 5
					hei = hei + 5
					shsize_str = ''.join([str(wi), "x", str(hei)])															
					mess.append(shsize_str)
					cntr += 1
			if shsize_str in dic_ps:
				mess.append("match-->")
				mess.append(shsize_str)
				papersizeobjls.append(dic_ps[shsize_str])
			else: #when no papersize found, after while loop, use default = 90x90
				papersizeobjls.append(dic_ps["90x90"])
				mess.append("no match, ps= 90x90")
			psmess.append(mess)
	except:
		import traceback
		print(traceback.format_exc())
	return (papersizeobjls, psmess)

# Comment:
# This was not an easy thing. int(FEC..................* 1000) ; TitleBlock with A0 Format  returns 1188[mm] != 1189, without int() it returns 1189.0 
# When I set a Variable TitleBlock manually to 1189x841  int(FEC...) returns 1189 ,841. --> works. If you check the dimensions in the family
# everything has the right size: width = 1189.000 

# Get PrintSetting "!temp", if not exist, create it 
	# Could have also done it with FEC OfClass(PrintSetting)
	# doc.GetPrintSettingIds() Set of al PrintSettings, Method of doc. 
def createTmpPrintSetting():
	printsettingelems = [doc.GetElement(i) for i in doc.GetPrintSettingIds()] 
							# returns a List[ElementId] with Ids
	temp_printsetting = [ i for i in printsettingelems if i.Name.Equals("!temp")]
	if not temp_printsetting:
		# Create the PrintSetting /PrintSetup with SaveAs-Method 
		t = Transaction(doc, "test") 
		t.Start() 
		doc.PrintManager.PrintSetup.SaveAs("!temp") # Saves the PrintSetting 
		t.Commit()			#Error the InSessionPrintSetting cannot be saved 
		printsettingelems = [ doc.GetElement(i) for i in doc.GetPrintSettingIds() ]
		temp_printsetting = [ i for i in printsettingelems if i.Name.Equals("!temp")]
		print(" !temp PrintSetting created" )
	return temp_printsetting[0]

#---START of printFunction ----------------------------------------------------
# prints one sheet at a time, uses !temp-Viewset with one Sheet, 
# This is done to be able to provide a specific filename. 
# printsetting !temp is permanently used for pdf printing.
# this can be used to edit further print parameters, either in "!temp" Revit PrintSetup-Dialog
# or in an in_future created edit-dialog. 

def printview(singlesheet, filepathname , papersizeobj, pdfprinterName,
				 tmp_printsetupobj = createTmpPrintSetting()): 
	# instantiate new_viewset Instance of ViewSetclass and insert single sheet
	new_viewset = ViewSet() #ViewSet Class
	new_viewset.Insert(singlesheet) 
	printmanager = doc.PrintManager 
	# set pdfprinterName = PDFCreator, Adobe PDF ..
	printmanager.SelectNewPrintDriver(pdfprinterName)
	# determine print range to Select option 
	printmanager.PrintRange = PrintRange.Select  # PrintRange is a own subclass 
	# make the new_viewset current 
	viewSheetSetting = printmanager.ViewSheetSetting
	viewSheetSetting.CurrentViewSheetSet.Views = new_viewset
	# set file path ---------------, add filend "_.pdf", "__.pdf" to fileend
	while os.path.exists(filepathname):
		filepathname = filepathname.replace(".pdf", "_.pdf")
		# filepathname must be different, everytime SubmitPrint() is called, 
		# else Exception: file exists is raised
	printmanager.PrintToFileName = filepathname #as string, 
	printmanager.Apply()

	printmanager.CombinedFile = True
	
	_printsetup = printmanager.PrintSetup
	page_orient = DB.PageOrientationType.Portrait
	t = Transaction(doc, "Testprint") #each Transaction must have a name. else: Error
	t.Start()
	_printsetup.CurrentPrintSetting = tmp_printsetupobj #needs a TransactionProcess, when changed
	_printsetup.CurrentPrintSetting.PrintParameters.PageOrientation = page_orient
	_printsetup.CurrentPrintSetting.PrintParameters.PaperSize = papersizeobj 
	try:  #if there are no changes to the PrintSetup obj (ie change to PrintParameters)
		  # .Save() method throws an exception, catch Exc. needed.
		_printsetup.Save() #returns True or throws Exception: Save of print was unsuccessful
	except: pass
	try: 
		#FECviewSets=FilteredElementCollector(doc).OfClass(ViewSheetSet).ToElements()
		#(doc.Delete(i.Id) for i in FECviewSets if i.Name =="!tmpViewSheetSet")
		viewSheetSetting.SaveAs("!tmpViewSheetSet") 
		printmanager.SubmitPrint()
		t.RollBack() # chose to use RollBack()-Way, see ForumEntry
		import time # ??? Error, needed!!. 
		time.sleep(1) 	# 3 sec, necessary, because PDF Printer will cause error
						#if too many docs submitted too fast. see ForumEntry
		#viewSheetSetting.Delete() # replaced with t.RollBack()
		errorReport = "Sucess" 
	except:
		import traceback 
		errorReport = traceback.format_exc() 
		print(errorReport) 
		try: t.RollBack() 
		except: pass
	return errorReport

#Users\Till\Desktop\RevitPrint'

dirpath = dlgdic["printfilepath"]  # in most printers it gets overwritten
			# by pdfPrinter, is set in Printer Properties, AdobePDF or PDFCreator work.

str2list = dlgdic["paranames"].split(",")
fnlist= pdfnamelist(viewlist, str2list, dirpath)
#returns tuple: (filepathnamelist, filenamelist) 

pslist = matchPaperSize(viewlist, dlgdic["printername"])
# returns tuple: (papersizeobjlist, psmess)

if output:
	print " SelectSheets-DialogValues -------------------------"
	for i in dlgdic.items(): print i

	print("\n ViewList ----------------------------------")
	for i in viewlist: print i.SheetNumber + " - " + i.Name

	print("\n FileNameList-------------------------------")
	for i in fnlist[1] : print(i)

	print("\n PaperSizeObjList---------------------------")
	for i in pslist[1]: print(i)

	print("\n----------------------------------------------")
	for v, fp, ps in zip(viewlist, fnlist[0], pslist[0]):
		print(v.Name, fp, ps.Name) 

	print("\n LoopPrint, Printer: {} ----------------------".format(dlgdic["printername"]))

# Print viewlist --------------------------------

if pdfexport:
	try:
		for v, fp, ps in zip(viewlist, fnlist[0], pslist[0]):
			pview = printview(v, fp ,ps , dlgdic["printername"])
			if output: print(pview)
		if output: print("\n{} Sheets printed!".format(len(viewlist)))
	except:
		# when error accurs anywhere in the process catch it
		errorReport = traceback.format_exc()
		print(errorReport)

endtime = timer.get_time()
if output:
	print(endtime)

#TODO: t.Rollback(), Instead of commiting, Roll it Back, proposition in Forum, done 
#TODO: Dialog for sheet Selection, if Selection is empty, open Dialog, done 
#TODO: Select views from Project Browser, done 
#ToDO: If Papersize_obj could not be found, python fails to
		#print any sheet at all, implement exception, done 03.08.2018
#TODO: If Select Sheets Dialog is Excaped or closed: stop script,
		#close window(), done 12.06.2018 
#ToDO: turn code into functions , done, 13.06.2018
#TODO: implement printing to A4,A3,A2,A1 Forms , 03.08.2018 done
#TODO: pickl dic_ps failed. not working, you can't pickl c# objects , done
#TODO: matchPaperSize fun: rewrite,, done
