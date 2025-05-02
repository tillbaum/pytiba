# -*- coding: utf-8 -*-
'''
Exports Schedules to csv file
Selection: Project Browser or Selection Dialog

Default Export Options: 
    Text qualifier: "
    Cell Separation: tab
    Export Title: No
 '''


# TODO: 
# - Add filepath button + Show filepath as Label
# - unicode filename not supported, change that, if possible! 

__title__ = "Schedule\ncsv-Export_1" 

__author__ = "Tillmann Baumeister"


#import clr
from Autodesk.Revit import DB 
import sys, os    
import traceback  
#import pyrevit   
from pyrevit import (forms, revit)  
from pyrevit.forms import TemplateListItem #BaseCheckBoxItem
from pyrevit import script

import io 
import glob # 
import csv 
import clr 
clr.AddReferenceByName('Microsoft.Office.Interop.Excel, Version=11.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c')
from Microsoft.Office.Interop import Excel 
from System import Array 
import pyrevit 
import System                     
import System.Collections.Generic 
import System.Threading.Tasks     
import System.Runtime.InteropServices  

from System.Runtime.InteropServices import Marshal 
import System.Runtime.InteropServices 



#output window: see pyrevit doc, Anatomy of a pyrevit_script
output = script.get_output()
# output.set_height(400)
# output.set_width(500) 

doc = __revit__.ActiveUIDocument.Document 
uidoc = __revit__.ActiveUIDocument 
uiapp = __revit__ 
app = uiapp.Application 


class ScheduleOption(BaseCheckBoxItem): 
    def __init__(self, schedule_element): 
        super(ScheduleOption, self).__init__(schedule_element)

    @property 
    def name(self): 
        return '{}'.format(self.item.Name) 


# create filepath.txt file to save filepath, Overwrite filepath when shiftclick! 
def filepath(filename_str): 
    path = os.path.split(sys.argv[0])[0]  
    try:    
        if __shiftclick__ == True: raise Exception() 
        with open(path +"\\" + filename_str, "r+") as f:  
            folderpath = f.read() 
            return folderpath 
    except: 
        folderpath = forms.pick_folder() 
        if not folderpath: sys.exit()    
        with open(path + "\\filepath.txt", "w") as f: 
            f.write(folderpath) 
        return folderpath       


# Select Schedule function   
def selectschedule():        
    selection = [doc.GetElement(elId) for elId in uidoc.Selection.GetElementIds() 
                    if doc.GetElement(elId).ViewType == DB.ViewType.Schedule]     
    if selection:          
        return selection   
    else:                  
        FECsched = DB.FilteredElementCollector(doc).OfClass(DB.ViewSchedule).ToElements() 
        fecsched = [i for i in FECsched if not i.IsTemplate] # filter out all template sched
        returnlist = forms.SelectFromList.show(sorted([ScheduleOption(x) for x in fecsched],
                                            key = lambda x: x.name),
                                            title = "Schedules")    
    if returnlist:       
        return [i.item for i in returnlist]  
    else:  
        #print("No Schedule selected \nExiting...")
        sys.exit()  


# Export selected Revit Schedules as csv file
def exportschedule():
    # ViewScheduleExportOptions
    options = DB.ViewScheduleExportOptions()  
    options.Title = False  
    folderpath = filepath("filepath.txt")
    sched_list = selectschedule()
    list = []
    print "sched_list: " ,len(sched_list)
    if sched_list:
        for i in sched_list: 
            filenamestr = i.Name + ".csv" 
            list.append(filenamestr)
            i.Export(folderpath, filenamestr, options)
            out = "{} --> exported".format(filenamestr)
            print(out) 
            #print i.Name, "exported to" , folderpath , filenamestr
        return (folderpath, list)
    else:
        sys.exit()


path, list = exportschedule() 


# ---- Create EXCEL FILE!!!! 

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


title = doc.Title[:-4] + "_Schedules.xlsx"  

fullpathsched = path + "\\" +  title  


try:
    exapp = Marshal.GetActiveObject('Excel.Application') # throws error, if no exapp is found
    # iterating over them 
    workbooks = [wb for wb in exapp.Workbooks if wb.Name == fullpathsched] 
    wb = workbooks[0]
    print wb 
    #if not wb: raise Exception  # True if wb is None

except:

    # marshal = Marshal.ReleaseComObject(exapp)
    print " Exception opening excelfile" 
    exapp = Excel.ApplicationClass() 
    openexcel = True  
    exapp.Visible = openexcel   
    exapp.DisplayAlerts = False 

    if os.path.exists(fullpathsched): 
        print("path exitst ", fullpathsched) 
        wb = exapp.Workbooks.Open(fullpathsched) 
    else: 
        #create a new workbook. 
        print "Creating new workbook" 
        wb = exapp.Workbooks.Add() 
        wb.SaveAs(fullpathsched)   


print "------------------------------------------------------   "
print wb.Name 
print "------------------------------------------------------   "


# list of all csv filepaths in directory, glob module 
csvlist = glob.glob(os.path.join(path, '*.csv')) 

newlist = []
for i in list:   
    [newlist.append(j) for j in csvlist if os.path.basename(j) == i] 
print(newlist)


print "  Iterating starts -------------------------------------- "

for csvfile in newlist: 
    # print "------- " , csvfile
    csvfilename = os.path.split(csvfile)[1][:-4]  
    print csvfilename    
    try: 
        sheet = wb.Worksheets(csvfilename) 
#        print sheet 
        # wb.Worksheets(csvfilename)         
 #       print '"',csvfilename, '"', "  exists !!... " 
        # sheet = wb.Worksheets(csvfilename)   
        sheet.UsedRange.ClearContents() 
    except EnvironmentError:            
        print "Error", csvfilename      
        sheet = wb.Worksheets.Add()     
        sheet.Name = csvfilename        
    except:
        print "Error: Something went wrong" 
        print traceback.format_exc()
    #print wb
    #print wb.Name 
    # read from the csvfile, write to Excel-sheet: 
    try: 
        with io.open(csvfile, 'r', encoding='utf_16') as f: 
            reader = unicode_csv_reader(f, delimiter='\t') 
            for i, row in enumerate(reader): 
                for j, colum in enumerate(row): 
                    sheet.Cells(i+1,j+1).Value = colum
    except UnicodeError:
        print "Error ", csvfilename 
        import traceback 
        print traceback.format_exc() 
        # continue
    except:
        import traceback
        print traceback.format_exc()
    Marshal.ReleaseComObject(sheet)



wb.Save()
Marshal.ReleaseComObject(wb)  
Marshal.ReleaseComObject(exapp)  














