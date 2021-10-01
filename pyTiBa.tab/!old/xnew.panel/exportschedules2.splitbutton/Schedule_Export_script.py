# -*- coding: utf-8 -*-
'''\nSchedule Export
Default Export Options:
String " "
Cell Separation: tab 
TODO: 
- Add filepath button + Show filepath as Label 
- unicode filename not supported, change that, if possible! 
 '''

__title__ = "Schedule\ncsv-Export"
__author__ = "Tillmann Baumeister"

#import clr
from Autodesk.Revit import DB
import sys, os 
import traceback 
#import pyrevit 
from pyrevit import (forms, revit)
from pyrevit.forms import BaseCheckBoxItem
import io 
import glob 
import csv 
import clr 
clr.AddReferenceByName('Microsoft.Office.Interop.Excel, Version=11.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c')
from Microsoft.Office.Interop import Excel 
from System import Array 
import pyrevit 

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument 
uiapp = __revit__ # is the same as uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application


def open_dic(fn="filepath.txt"):
    dic1 = {"ouput": True, "paranames": 'Sheet Number,_,Sheet Name'}
    with open(os.path.dirname(__file__) + "\\" + fn, "a+b") as f: # create and read
        f.seek(0)
        try:
            txt = f.readline()
            #dic = pickle.load(f)
            return txt
        except: pass


# write dialogData from input boxes as dictionary.
def write_dic(newdic, olddic = open_dic(), fn = "dlgval.pkl"):
    if newdic and not newdic == olddic:
        with open(os.path.dirname(__file__) + "\\" + fn, "wb") as f:
            pickle.dump(newdic, f)


def pick_folder():  
    fb_dlg = Forms.FolderBrowserDialog()
    if fb_dlg.ShowDialog() == Forms.DialogResult.OK:
        return fb_dlg.SelectedPath


class ScheduleOption(BaseCheckBoxItem):
    def __init__(self, schedule_element):
        super(ScheduleOption, self).__init__(schedule_element)

    @property
    def name(self):
        return '{}'.format(self.item.Name)


class AddSelectFromList(pyrevit.forms.SelectFromList):
    def __init__(self, **kwargs):
        super(AddSelectfromList, self).__setup__(self, **kwargs)
        self.lb_filepath.Content = filepath("filepath.txt")

    def pickfolder(self, sender, event):
        self.lb_filepath.Content = pick_folder()


# get filepath ,create filepath.txt file at first run. Overwrite filepath when shiftclick!
def filepath(filename_str):
    path = os.path.split(sys.argv[0])[0]
    try:
        if __shiftclick__ == True: raise Exception()
        with open(path + "\\" + filename_str, "r+") as f: # a+ mode, because I need "create file" function
            folderpath = f.read() 
            return folderpath 
    except:
        folderpath = forms.pick_folder()  
        if not folderpath: sys.exit()     
        with open(path + "\\filepath.txt", "w") as f:
            f.write(folderpath)
        return folderpath


def selectschedule():
    selection = [doc.GetElement(elId) for elId in uidoc.Selection.GetElementIds()
                    if doc.GetElement(elId).ViewType == ViewType.Schedule]
    if selection:       
        return selection
    else:               
        FECsched = DB.FilteredElementCollector(doc).OfClass(DB.ViewSchedule).ToElements()
    #sched = [i for i in FECsched if i.Name == schedName + " Schedule"][0]
        returnlist = AddSelectFromList.show(sorted([ScheduleOption(x) for x in FECsched],
                                            key = lambda x: x.name),
                                            title = "Schedules")
    if returnlist:
        return [i.item for i in returnlist]
    else:
        sys.exit()


def exportschedule():
    # ViewScheduleExportOptions
    options = DB.ViewScheduleExportOptions()
    options.Title = False # no Title in first line of csv file
    mess = []                           
    folderpath = filepath("filepath.txt")
    sched_list = selectschedule()
    if sched_list:               
        for i in sched_list:     
            filenamestr = i.Name + ".csv"
            export =  i.Export(folderpath, filenamestr, options)
            mess.append(filenamestr)
            #print i.Name, "exported to" , folderpath , filenamestr
        return mess
    else:
        sys.exit()

export = exportschedule()
print export


def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]


def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')


path = "C:\\users\\till\\desktop\\NeuburgerStr"
excelfilename = doc.Title[:-3] + "xlsx"
fullpath = path + "\\" + excelfilename  

#Grab active workbook named doc.Title, if open 
#import only the csv exported ?
#import all files to excel


def csv_excel(openexcel = False, fullpath= fullpath):
    ex = Excel.ApplicationClass()   
    ex.Visible = openexcel
    ex.DisplayAlerts = False
    
    if os.path.exists(fullpath):
        wb = ex.Workbooks.Open(fullpath) 
    else: 
        wb = ex.Workbooks.Add()
        wb.SaveAs(fullpath)
    # list of all csv filepaths in directory
    csvlist = glob.glob(os.path.join(path, '*.csv'))
    # csvlist = os.path.join()
    for csvfile in csvlist:
        csvname = os.path.split(csvfile)[1][:-4] 
        if not wb.Worksheets(csvname).Name: 
            sheet = wb.Worksheets.Add() 
            sheet.Name = csvname 
        else:
            print csvname, "exists!!!" 
            sheet = wb.Worksheets(csvname) 
            sheet.UsedRange.ClearContents() 
        try:
            with io.open(csvfile, 'r', encoding='utf_16') as f: 
                reader = unicode_csv_reader(f, delimiter='\t') 
                for i, row in enumerate(reader): 
                    for j, colum in enumerate(row): 
                        sheet.Cells(i+1,j+1).Value = colum 
        except UnicodeError: 
            print "Error ", csvname 
            import traceback 
            print traceback.format_exc() 
            continue 
        except: 
            import traceback 
            print traceback.format_exc() 
    wb.Save() 

csv_excel(openexcel= True)

