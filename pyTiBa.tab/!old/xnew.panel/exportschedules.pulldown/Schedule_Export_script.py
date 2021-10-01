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


doc = __revit__.ActiveUIDocument.Document 
uidoc = __revit__.ActiveUIDocument 
uiapp = __revit__ # is the same as uiapp = DocumentManager.Instance.CurrentUIApplication 
app = uiapp.Application 


class ScheduleOption(BaseCheckBoxItem): 
    def __init__(self, schedule_element): 
        super(ScheduleOption, self).__init__(schedule_element)
        
    @property 
    def name(self): 
        return '{}'.format(self.item.Name) 


# create filepath.txt file at first run.  Overwrite filepath when shiftclick! 
def filepath(filename_str): 
    path = os.path.split(sys.argv[0])[0] 
    try: 
        if __shiftclick__ == True: raise Exception() 
        with open(path +"\\" + filename_str, "r+") as f: # a+ mode, because I need "create file" funciton 
            folderpath = f.read() 
            return folderpath 
    except: 
        folderpath = forms.pick_folder() 
        if not folderpath: sys.exit()    
        with open(path + "\\filepath.txt", "w") as f: 
            f.write(folderpath)                       
        return folderpath  



def selectschedule(): 
    FECsched = DB.FilteredElementCollector(doc).OfClass(DB.ViewSchedule).ToElements() 
    #sched = [i for i in FECsched if i.Name == schedName + " Schedule"][0] 
    returnlist = forms.SelectFromList.show(sorted([ScheduleOption(x) for x in FECsched], 
                                            key = lambda x: x.name),
                                            title = "Schedules")
    if returnlist: 
        return [i.item for i in returnlist] 
    else: 
        sys.exit() 



def exportschedule(): 
    # ViewScheduleExportOptions
    options = DB.ViewScheduleExportOptions() 
    options.Title = False 

    folderpath = filepath("filepath.txt") 
    sched_list = selectschedule() 
    if sched_list: 
        for i in sched_list: 
            filenamestr = i.Name + ".csv" 
            i.Export(folderpath, filenamestr, options) 
            #print i.Name, "exported to" , folderpath , filenamestr 
    else: 
        sys.exit()


exportschedule() 


def mergetoexcelfile(): 
    pass







