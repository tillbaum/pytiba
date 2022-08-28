# -*- coding: utf-8 -*-
""" 
PDFsOut, DWGsOut: 
 - Sheet-Selection in ProjectBrowser, 
 - Sheet-Selection in Sheet-Selection-Dialog
 - Pathname, Printer, Filename can be set. 
  
--- Layout in pdfprinter must be set to "Landscape" --- 

Copyright (c) 2017 Tillmann Baumeister
Python scripts for Autodesk Revit
GNU General Public License, version 3
"""  
#! python3
# v2.1 matchsize func updated to support A0 (1189x841), A1, A2, A3 formats, PrintForms included
# v2.3 21.09.2018; !Temp PrintSetting: FitToPage is set; added PrintParameter.ZoomType = ZoomType.Zoom #Enum´    
# v2.4 03.11.2018; Added CurrentPrintSetting.PrintParameter.PaperPlacement= DB.PaperPlacementType.Center 
#!tmp PrintSetting, since in a new Arch_Project_template, PaperPlacementType.Margin is the 
#default value in the PrintSetting !temp. 
#v2.5 07.01.2019, Added Property: "ColorDepthType = Color" in PrintManager; from Adesk.Revit.DB import *
# v20 ; added dwg export of "views", which have the .CanBePrinted property; 
#;there are now 2 Dialog Pickle files dumped, one for the Parameterlist, which is dependend on the Project.
#(It gets dumped in the Folder ExpotDlgValues), one for other Dialog Values: Path, output, pdfexport, dwgexport
# (get dumped in dlgval.pkl file in same folder as script. 
# v21: Added Custom PaperSize Creation with IronPython ctypes
from __future__ import division

__title__ = "Export\nPDF"
__author__ = "TBaumeister"


import sys, os
from functools import wraps
import math	# math.ceil  
import time # sleep()    
import traceback         
import cPickle as pickle #python 2 feature
import ctypes
from ctypes import wintypes
from ctypes.wintypes import DWORD, LPCWSTR, SIZEL, RECTL, UINT

import clr
clr.AddReference("PresentationFramework") 
clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')
clr.AddReference('System.Drawing')

from System.Drawing.Printing import PrinterSettings, PrintDocument, PaperSize
import wpf

import System
from System.Windows import Forms, Controls
from System.Windows import Forms as winforms
from System.Collections.Generic import List

from Autodesk.Revit.DB import *
from Autodesk.Revit import DB, UI

import pyrevit             
# from pyrevit import forms
from pyrevit.compat import safe_strtype # required for py2 cause py2 is asci encoded 

#logger = get_logger(__name__) 

DEFAULT_INPUTWINDOW_WIDTH = 500 
DEFAULT_INPUTWINDOW_HEIGHT = 400

# for timing ------------------------------------------------
from pyrevit.coreutils import Timer
timer = Timer()

pyt_path = (r'C:\Program Files (x86)\IronPython 2.7\Lib') 
sys.path.append(pyt_path) 

doc = __revit__.ActiveUIDocument.Document 
uidoc = __revit__.ActiveUIDocument 

#when copying code to RPS
try:
    __file__
except NameError:
     __file__ = "E:\OneDrive\Pytiba\pytiba\pyTiBaDev.extension\pyTiBaDev.tab\xtest2.panel\pdfexport.pushbutton"

    
def pick_folder(): 
    fb_dlg = winforms.FolderBrowserDialog()             
    if fb_dlg.ShowDialog() == Forms.DialogResult.OK: 
        return fb_dlg.SelectedPath                   


#func lookuppara; paraname as string: ex: "Sheet Number"
#TODO: maybe replace with orderedParameters, or ParameterSet, 
def lookupparaval(element, paraname): 
    try: newp = element.LookupParameter(paraname)
    except: newp = None; pass 
    if newp:
        if newp.StorageType.Equals(StorageType.String):    value = newp.AsString()
        elif newp.StorageType == StorageType.Integer: value = newp.AsInteger()
        elif newp.StorageType == StorageType.Double:  value = newp.AsDouble()
        return value
    else: return False

# set up filename_str from csv separates parameterlist
def namefromparalist(view, paralist):
    import datetime
    m = datetime.datetime.now()
    date = m.strftime("%d-%m-%y") #stringformattime fun
    time = m.strftime("%H.%M")
    tmp_filenamelist = []
    for i in paralist: 
        if i in ['_', ' ', '.', '-', ';','']:
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
            tmp_filenamelist.append(str(lookupval) if lookupval else '')
        # else:
            # tmp_filenamelist.append(i)
    filename = ''.join(tmp_filenamelist)
    return filename


def pdfnamelist(viewlist, paralist, dirpath = ''):
    filepathlist = []
    filenamelist = []
    for v in viewlist:
        tmpname = namefromparalist(v, paralist)
        tmpname += ".pdf" # safe_strtype required for python 2
        filenamelist.append(tmpname)
        filepathlist.append(dirpath + "\\" + tmpname )
    return (filepathlist, filenamelist)

def dwgnamelist(viewlist, paralist, dirpath = ''):
    filepathlist = []
    filenamelist = []
    for v in viewlist:
        tmpname = namefromparalist(v, paralist)
        #tmpname += ".pdf" 
        filenamelist.append(tmpname)
        filepathlist.append(dirpath + "\\" + tmpname )
    return (filepathlist, filenamelist)



class SelectFromCheckBoxes(System.Windows.Window): 
    """ tb_modified Standard form to select from a list of check boxes.
    """
    xaml_source = 'tb_SelectFromCheckboxes.xaml' 

# copied from class TemplateUserInputWindow ---------------------------
    def __init__(self, context,
                 title='User Input',
                 width= DEFAULT_INPUTWINDOW_WIDTH,
                 height= DEFAULT_INPUTWINDOW_HEIGHT, **kwargs):
                 
        """Initialize user input window."""
        # wpf.LoadComponent(self, os.path.join(os.path.dirname(__file__), self.xaml_source))
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
            if args.Key == System.Windows.Input.Key.Escape:
                self.Close()                   
                sys.exit() #TODO! sysExit. READ

        self.PreviewKeyDown += handle_ESCinput_key # ESC closes the form

        # in def setup( **kwargs) method
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
        dialogfile= uidoc.Document.Title  + "_dlgval.pkl"
        
        #tb_ADDED: Values from Checkbox and Textinput ----------------------------
        self.dicprj = {}
        self.dicdlg = {}
        
        with open(os.path.dirname(os.path.dirname(__file__)) + "\\ExportDlgValues\\"
                          + uidoc.Document.Title + "_dlgval.pkl", "ab+") as f: # create and read
            f.seek(0) #set cursor to 0 position
            try:
                self.dicprj = pickle.load(f)
            except: 
                pass
                #print dialogfile + "-file created!" 
            
        
        with open(os.path.dirname(__file__) + "\\dlgval.pkl", "ab+") as g:   # create and read 
            g.seek(0)
            try:
                self.dicdlg = pickle.load(g) 
            except: pass
            
        try: 
            self.dicprj
            self.dicdlg# if dicprj not exists -> Except clause 
            #print self.dicprj # testing  
            self.txtbox_paranames.Text = self.dicprj["paranames"]  
            #self.expander.Header = self.dicprj["paranames"]   
            self.txtbox_printername.Text = self.dicdlg["printername"] 
            self.lb_printfilepath.Content = self.dicdlg["printfilepath"]  
            self.chbox_output.IsChecked = self.dicdlg["output"]   
            self.chbox_pdfexport.IsChecked = self.dicdlg["pdfexport"]
            self.chbox_dwgexport.IsChecked = self.dicdlg["dwgexport"]
        except:
            # print "Exception" 
            # print traceback.format_exc()
            #Standard Dialog Values  ------------------------    
            self.txtbox_paranames.Text = "Sheet Number,-,Sheet Name"
            #self.expander.Header += "Sheet Number,_,Sheet Name"
            self.chbox_output.IsChecked = True   
            self.lb_printfilepath.Content = pyrevit.USER_DESKTOP
            self.txtbox_printername.Text = "PDFCreator"
            
            
# copied from WMFWindow
    @staticmethod # e.g method can be applied to the class and the instance, both
    def hide_element(*wpf_elements):
        """Collapse elements.

        Args:
            *wpf_elements (str): element names to be collapsed
        """
        for el in wpf_elements:
            el.Visibility = System.Windows.Visibility.Collapsed

    @staticmethod
    def show_element(*wpf_elements):
        """Show collapsed elements.

        Args:
            *wpf_elements (str): element names to be set to visible.
        """
        for el in wpf_elements:
            el.Visibility = System.Windows.Visibility.Visible

    @staticmethod
    def toggle_element(*wpf_elements):
        """Toggle visibility of elements.

        Args:
            *wpf_elements (str): element names to be toggled.
        """
        for el in wpf_elements:
            if el.Visibility == System.Windows.Visibility.Visible:
                self.hide_element(el)
            elif el.Visibility == System.Windows.Visibility.Collapsed:
                self.show_element(el)

# copied from TemplateUserInputWindow END 

    def _verify_context(self):
        new_context = []
        for item in self._context:
            if not hasattr(item, 'state'):
                new_context.append(BaseCheckBoxItem(item))
            else:
                new_context.append(item)

        self._context = new_context

    def _list_options(self, checkbox_filter = None):
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
        self._set_states(flip= True)

    def check_all(self, sender, args):
        """Handle check all button to mark all check boxes as checked."""
        self._set_states(state= True)

    def uncheck_all(self, sender, args):
        """Handle uncheck all button to mark all check boxes as un-checked."""
        self._set_states(state= False)

    def check_selected(self, sender, args):
        """Mark selected checkboxes as checked."""
        self._set_states(state= True, selected= True)

    def uncheck_selected(self, sender, args):
        """Mark selected checkboxes as unchecked."""
        self._set_states(state= False, selected= True)

    def button_select(self, sender, args):
        """Handle select button click."""
        if self.checked_only:
            self.response = [x.item for x in self._context if x.state]
        else:
            self.response = self._context
        #tb folowing lines added!
        self.dicprj["paranames"] = self.txtbox_paranames.Text    
        self.dicdlg["printername"] =  self.txtbox_printername.Text
        self.dicdlg["printfilepath"] = self.lb_printfilepath.Content
        self.dicdlg["output"] = self.chbox_output.IsChecked      
        self.dicdlg["pdfexport"] = self.chbox_pdfexport.IsChecked
        self.dicdlg["dwgexport"] = self.chbox_dwgexport.IsChecked
        self.Close()  

    def savesettings_click(self, sender, args):
        """Handle savesettings button click."""
        self.dicprj["paranames"] = self.txtbox_paranames.Text    
        self.dicdlg["printername"] =  self.txtbox_printername.Text
        self.dicdlg["printfilepath"] = self.lb_printfilepath.Content
        self.dicdlg["output"] = self.chbox_output.IsChecked      
        self.dicdlg["pdfexport"] = self.chbox_pdfexport.IsChecked
        self.dicdlg["dwgexport"] = self.chbox_dwgexport.IsChecked
        #self.expander.Header = self.txtbox_paranames.Text     

        # export dialog settings for each Prj, save to Folder ExportDlgValues
        with open(os.path.dirname(os.path.dirname(__file__)) + "\\ExportDlgValues\\"
                                     + uidoc.Document.Title + "_dlgval.pkl", "w+b") as f:
            pickle.dump(self.dicprj, f)
            
        # export dialog settings to file in same folder as pdfprint-app
        with open(os.path.dirname(__file__) + "\\dlgval.pkl", "w+b") as fa:
            pickle.dump(self.dicdlg, fa)

        winforms.MessageBox.Show("Dialog Settings saved!", "Alert")

    # tb previewbutton: preview_b
    def preview_click(self, sender, event):
        ''' Handle Preview Button click '''
        str2list = self.txtbox_paranames.Text.split(',')
        #stripwhitespacefrlistelem = list(map(str.strip, str2list)) 
        sheetobj = [x.item for x in self._context if x.state]
        try:
            sheetobj =  sheetobj[0] if sheetobj else FilteredElementCollector(doc).OfClass(ViewSheet).FirstElement()
        except: pass           
        paranamesval = namefromparalist(sheetobj, str2list) if sheetobj else "No Sheet selected"
        self.lb_txtbox_preview.Text = paranamesval

    def selectprintfilepath_click(self, sender, event): 
        ''' open folder '''
        self.lb_printfilepath.Content = pick_folder()

    # Test Checkbox, Method not needed! 
    # def checkdwgexport(self, sender, event):
        # print "dwgCheck", self.chbox_dwgexport.IsChecked


    def search_txt_changed(self, sender, args):
        """Handle text change in search box."""
        if self.search_tb.Text == '':
            self.hide_element(self.clrsearch_b)
        else:
            self.show_element(self.clrsearch_b) 

        self._list_options(checkbox_filter = self.search_tb.Text)

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


### FUNCTIONS ############################################################
# ---FILENAME -------------------------------------------------------
clr.AddReference('System.Drawing')
from System.Drawing.Printing import PrinterSettings, PrintDocument, PaperSize
import ctypes
from ctypes import wintypes
from ctypes.wintypes import DWORD, LPCWSTR, SIZEL, RECTL, UINT

kernel32 = ctypes.WinDLL('kernel32.dll', use_last_error=True)
winspool = ctypes.WinDLL('winspool.drv', use_last_error=True)

# define LPHANDLE, PDWORD, and PWORD for Python 2
if not hasattr(wintypes, 'LPHANDLE'):
    setattr(wintypes, 'LPHANDLE', ctypes.POINTER(wintypes.HANDLE))
if not hasattr(wintypes, 'PDWORD'):
    setattr(wintypes, 'PDWORD', ctypes.POINTER(wintypes.DWORD))
if not hasattr(wintypes, 'PWORD'):
    setattr(wintypes, 'PWORD', ctypes.POINTER(wintypes.WORD))

class PRINTER_INFO_1(ctypes.Structure):
    _fields_ = [
        ("Flags", DWORD),
        ("pDescription", LPCWSTR),
        ("pName", LPCWSTR),
        ("pComment", LPCWSTR),
    ]

class PRINTER_DEFAULTS(ctypes.Structure):
    _fields_ = [
        ("pDatatype", LPCWSTR),      
        ("pDevMode", LPCWSTR),
        ("DesiredAccess", DWORD),
    ]

class FORM_INFO_1(ctypes.Structure):
    _fields_ = [
        ("Flags", DWORD),
        ("pName", LPCWSTR),
        ("Size", SIZEL),
        ("ImageableArea", RECTL),
    ]

class PRINTER_OPTIONS(ctypes.Structure):
    _fields_ = [
        ("cbSize", UINT),
        ("dwFlags", DWORD),
                ]

def createPaperSize(name, x, y):    
    printerDef = PRINTER_DEFAULTS(None , "1" , 0x20000000) 
#I changed the value of PRINTER_DEFAULT “DesiredAccess” to 0x20000000.
# This is the value for a GENERIC_EXECUTE access request, shown on this page: 
# https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-smb/27f99d29-7784-4684-b6dd-264e9025b286
    printerOpt = PRINTER_OPTIONS(1, DWORD(2))
    hPrinter = wintypes.HANDLE()    
    pd = PrintDocument()
    sPrinterName = pd.PrinterSettings.PrinterName
    bOpenPrinter = winspool.OpenPrinterW("PDFCreator", 
                                ctypes.byref(hPrinter), printerDef)
    formName = name

    # delete the form incase it already exists
    try:
        bDeleteForm = winspool.DeleteFormW(hPrinter, formName)
    except Exception as e:
        print (e)
  
    # create and initialize the FORM_INFO_1 structure

    sizeX = y*1000
    sizeY = x*1000
    formInfo = FORM_INFO_1(DWORD(0), formName, (sizeX, sizeY), (0, 0, sizeX, sizeY))    
    bFormAdded = winspool.AddFormW(hPrinter, DWORD(1), formInfo)# returns boolval 1
    bClosePrinter = winspool.ClosePrinter(hPrinter), #returns boolval 1
    return formName

createPaperSize("200x200", 200, 200)


# example: round_up(1.12222, 0.05) = 1.15 0.297 
def round_up(x, a):
    return math.ceil(x / a) * a # TEST rundet down. ???
#ToDO: other method : round_up(0.2078, 0.005) ; returns 0.20999999 



# Creat PaperSize_Object-List: Matching TitleBlock_Sheet_Size with PaperSize in 
# Revit doc.PrintManager.PaperSizes, (a Set) -> WinPrintForms
def matchPaperSize(viewlist, pdfPrinterName):

    doc.PrintManager.SelectNewPrintDriver("PDFCreator") #line needed, 
                                            # when a non-pdf printer is set up. 
    papersizeset = doc.PrintManager.PaperSizes

    bip_shwi =  DB.BuiltInParameter.SHEET_WIDTH  
    bip_shhei = DB.BuiltInParameter.SHEET_HEIGHT
    psmess, papersizeobjls = [], []

    try:
        for i,v in enumerate(viewlist):
            # Get TitleBlock with Para Sheet_Width > 20 cm cause TB with width < 20 cm is Plankopf
            # note: FilterDoubleRule(ParameterValueProvider(), FilterNumericEquals),
            # "ex.10.0", delta_x)
            filter_double_rule = \
                  FilterDoubleRule(ParameterValueProvider(
                  ElementId(BuiltInParameter.SHEET_WIDTH)), \
                  FilterNumericGreater(), 0.20 / 0.3048, 1E-2) 

            fectb = FilteredElementCollector(doc, v.Id) \
                     .WherePasses(ElementParameterFilter(filter_double_rule)) \
                     .ToElements()

            bip_wi = int(fectb[0].get_Parameter(bip_shwi).AsDouble() * 0.3048 *1000)  # from m to mm
            bip_hei = int(fectb[0].get_Parameter(bip_shhei).AsDouble() * 0.3048 *1000)
            # print bip_wi, bip_hei , float(bip_wi), float(bip_hei), int(bip_wi), int(bip_hei) 
            # cut of all irelevant decimalplaces  0.750000011 = 750 mm

            shsize_str = ''.join([str(bip_wi), "x", str(bip_hei)])

            # shsize_str_round = ''.join([str(round_up(wi_cm, 0.5)),
                                        # "x", str(round_up(hei_cm, 0.5))]) 

            psls = [i for i in papersizeset if i.Name.ToString() == shsize_str]
            ps = psls[0] if psls else None
            if ps:
                papersizeobjls.append(ps)
            if not ps:
                createPaperSize(shsize_str, bip_wi, bip_hei)
                papersizeset = doc.PrintManager.PaperSizes

                psls = [i for i in papersizeset if i.Name.ToString() == shsize_str]
                ps = psls[0] if psls else None
                if ps:
                    papersizeobjls.append(ps)
    except:
        print (traceback.format_exc())

    return (papersizeobjls, psmess )


# createTmpPrintSetting FUNC: Create RevitAPI-PrintSetting "!temp", if not exist, create it
    # Could have also done it with FEC OfClass(PrintSetting) 
    # doc.GetPrintSettingIds() Set of all PrintSettingsIds, Method of doc.
def createTmpPrintSetting():
    temp_printsetting = [ doc.GetElement(i) for i in doc.GetPrintSettingIds() 
                            if doc.GetElement(i).Name.Equals("pytiba") ] 

    def setPrintSetupOptions():
        printsetup = doc.PrintManager.PrintSetup
        printpara = printsetup.CurrentPrintSetting.PrintParameters 
        #PaperPlacement & Zoom
        printpara.PaperPlacement = DB.PaperPlacementType.Center
        printpara.ZoomType = DB.ZoomType.Zoom # enum 
        printpara.Zoom = 100 # ????
        # Orientation, HiddenLineViews, Appearance
        printpara.PageOrientation = DB.PageOrientationType.Landscape # enum  
        printpara.HiddenLineViews = DB.HiddenLineViewsType.VectorProcessing 
        #Appearance 
        printpara.RasterQuality = DB.RasterQualityType.High
        printpara.ColorDepth = DB.ColorDepthType.Color
        #Options
        printpara.ViewLinksinBlue = True  
        printpara.HideCropBoundaries = True
        printpara.HideScopeBoxes = True  
        printpara.HideReforWorkPlanes = True
        printpara.HideUnreferencedViewTags = True
        printpara.MaskCoincidentLines = False  
        printpara.ReplaceHalftoneWithThinLines = False
        printsetup.Save
        return printsetup

    if not temp_printsetting:
        #print "Creating PrintSetting..."
        # Create the PrintSetting /PrintSetup with SaveAs-Method 
        _printsetup = setPrintSetupOptions()
        t = Transaction(doc, "Create pytiba PrintSetting")
        t.Start()
        _printsetup.SaveAs("pytiba") # Saves the PrintSetting
        t.Commit()
        temp_printsetting = [ doc.GetElement(i) for i in doc.GetPrintSettingIds() 
                            if doc.GetElement(i).Name.Equals("pytiba")]
        #print("\npytiba PrintSetting created" )
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
    # filepathname must be different, everytime SubmitPrint() is called,
    # else Exception: file exists is raised
    while os.path.exists(filepathname):
        filepathname = filepathname.replace(".pdf", "_.pdf")
    printmanager.PrintToFileName = filepathname #as string,
    printmanager.Apply() 
    printmanager.CombinedFile = True 
    _printsetup = printmanager.PrintSetup 

    t = Transaction(doc, "Print")
    t.Start() 
    _printsetup.CurrentPrintSetting = tmp_printsetupobj #needs a TransactionProcess, when changed
    _printsetup.CurrentPrintSetting.PrintParameters.PaperSize = papersizeobj 
    try:  #if there are no changes to the PrintSetup obj (ie change to PrintParameters)
          # .Save() method throws an exception, catch Exc. needed.  
        _printsetup.Save() #returns True or throws Exception: Save of print was unsuccessful
    except: pass
    t.Commit()
    t = Transaction(doc, "Print")
    t.Start()
    try:
        # collect ViewSheetSet with name!tmpViewSheetSet and delete it if it exists, which is unlikely
        FECviewSets=FilteredElementCollector( doc ).OfClass( ViewSheetSet ).ToElements()
        ( doc.Delete(i.Id) for i in FECviewSets if i.Name =="!tmpViewSheetSet" )
        viewSheetSetting.SaveAs("!tmpViewSheetSet")
        printmanager.SubmitPrint()
        t.RollBack() # chose to use RollBack()- Way, see ForumEntry 
        #??? Error, needed!!. 
        time.sleep(1) # 1 sec, necessary, because PDF Printer will cause error 
                      # if too many docs submitted too fast. see Revit API ForumEntry
        # viewSheetSetting.Delete() # replaced with t.RollBack() 
        errorReport = "Success"
        return errorReport
    except:             
        import traceback
        errorReport = traceback.format_exc()
        print(errorReport)
        try: t.RollBack() 
        except: pass 
    return errorReport


# fun Export DWG ---------------------------------------------
def exportDwg(filename, view, folderpath): 
    # DWGExport Options, get Current Active
    firstdwgsetting = DB.FilteredElementCollector(doc).OfClass(ExportDWGSettings) \
                                                      .FirstElement()
    if not firstdwgsetting:
        winforms.MessageBox.Show("No DWG Setting in Project!\n Create a DWG Setting", "Alert")
        # forms.alert("There is NO DwgSetting in Project", ok=True)

    currentactiveset= firstdwgsetting.GetActivePredefinedSettings(doc)
    if not currentactiveset:
        dwgopt = firstdwgsetting.GetDWGExportOptions()
    else: 
        dwgopt= currentactiveset.GetDWGExportOptions()
    views = List[ElementId]() # empty .Net List
    views.Add(view.Id)
    result = doc.Export(folderpath, filename, views, dwgopt) #Revit API func
    return result


# Sheet selection dialog
def selectsheets2print(): 
    FECall_sheets = DB.FilteredElementCollector(doc).OfClass(DB.ViewSheet) \
                   .WhereElementIsNotElementType().ToElements()
    FECall_sheets = [i for i in FECall_sheets if i.CanBePrinted]
    
    sortlist = sorted([SheetOption(x) for x in FECall_sheets], key = lambda x: x.number)
    selsheet = SelectFromCheckBoxes(sortlist, 
                        title = "Select Sheets", 
                        width = 500, height = 400, 
                        button_name = "Select / PRINT") 
    selsheet.ShowDialog() #.Net Method, Modal Window, no other window is active
    if selsheet.response:
        return ([i.item for i in selsheet.response 
                    if i.state], selsheet.dicprj, selsheet.dicdlg)
    else: 
        sys.exit() #selsheet.response does not exist


# "printfilepath" in most printers it gets overwritten
# by pdfPrinter, is set in Printer Properties, AdobePDF or PDFCreator work.


def pdfexportsheet(dicprj, dicdlg, sheetlist):

    fnlist= pdfnamelist(sheetlist, dicprj["paranames"].split(","), dicdlg["printfilepath"]) 
        #returns tuple: (filepathnamelist, filenamelist) 

    pslist = matchPaperSize(sheetlist, dicdlg["printername"]) 
        # returns tuple: (papersizeobjlist, printername )
    # for i in fnlist: print i

    # for i in pslist: print i
    # Print viewlist ----------------------------------------
    try:
        for v, fp, ps in zip(sheetlist, fnlist[0], pslist[0]):
            pview = printview(v, fp ,ps ,dicdlg["printername"])
            if dicdlg["output"]: 
                print(pview)
        # forms.alert("{} PDF Sheet printed!".format(len(sheetlist)) , ok=True )
        # winforms.MessageBox.Show("{} PDF Sheet printed!".format(len(sheetlist)), "Alert")
    except:
        # when error accurs anywhere in the process catch it 
        print traceback.format_exc() 


def dwgexportsheet(dicprj, dicdlg, sheetlist): 
    #returns tuple: (filepathnamelist, filenamelist)
    fnlistdwg = dwgnamelist(sheetlist, dicprj["paranames"].split(","), dicdlg["printfilepath"])
    
    try: 
        for fn, v in zip(fnlistdwg[1], sheetlist): 
            exportDwg(fn, v, dicdlg["printfilepath"]) 

        # forms.alert("{} dwgs exported".format(len(sheetlist)), ok=True)    
    except:
        ##when error accurs anywhere in the process catch it
        import traceback
        print traceback.format_exc()



def dwgexportview(viewlist):
    # Chars not allowed in WindowsFileSystem:  \ / : * ? <> " |
    namelist = [ i.Name.replace('/', '_').replace(':', '_').replace('*', '_').replace('?', '')
                        for i in viewlist]
    try:
        for name, view  in zip( namelist, viewlist):
            exportDwg(name, view, dicdlg["printfilepath"])
        alerttext = "DWG-Files: \n {} exported \n to: {}".format(namelist, dicdlg["printfilepath"])
        winforms.MessageBox.Show(alerttext, "Alert")
        
    except: 
        import traceback
        print traceback.format_exc()
        


#---Manual ELEMENT SELECTION in ProjectBrowser ----------------------------------------
selec_ids = uidoc.Selection.GetElementIds()

sheetlist = [doc.GetElement(i) for i in selec_ids if doc.GetElement(i) \
            .ViewType.Equals(ViewType.DrawingSheet) and doc.GetElement(i).CanBePrinted]

viewlist = [doc.GetElement(i) for i in selec_ids if not doc.GetElement(i) \
            .ViewType.Equals(ViewType.DrawingSheet) and doc.GetElement(i).CanBePrinted]

# if sheetlist: print len(sheetlist)
# if viewlist: print len(viewlist)


if __shiftclick__:
    sheetlist, dicprj, dicdlg = selectsheets2print() 


# open dictionaries or reading dlg values, and filenamelist. 
try:
    with open(os.path.dirname(__file__) + "\\dlgval.pkl", "rb+" ) as fa:
        #fa.seek(0) 
        dicdlg = pickle.load(fa)

    with open(os.path.dirname(os.path.dirname(__file__)) + "\\ExportDlgValues" + 
                      "\\" + uidoc.Document.Title + "_dlgval.pkl", "rb+") as f: # create and read
        dicprj = pickle.load(f)
except: 
    # if no files can be found ( first time run) oben selection dialog. 
    sheetlist, dicprj, dicdlg = selectsheets2print() 

#print dicdlg


#----------------------------------------------------------------------------------------
if dicdlg["pdfexport"] and sheetlist and not viewlist:
    #print " pdfexport with sheetlist"
    pdfexportsheet(dicprj, dicdlg, sheetlist)


if dicdlg["dwgexport"] and sheetlist and not viewlist: 
    #print "dwgexport with sheetlist"
    dwgexportsheet(dicprj, dicdlg, sheetlist)


if not sheetlist and not viewlist: 
    #print "pdfexport/dwgexport no sheetlist" 
    sheetlist, dicprj, dicdlg = selectsheets2print() 
    if sheetlist and dicdlg["pdfexport"]: 
        pdfexportsheet(dicprj, dicdlg, sheetlist) 
    if sheetlist and dicdlg["dwgexport"]: 
        dwgexportsheet(dicprj, dicdlg, sheetlist) 


if dicdlg["dwgexport"] and viewlist: 
    #print "viewlisit" 
    dwgexportview( viewlist)


endtime = timer.get_time() 
if dicdlg["output"]: 
    print(endtime)

