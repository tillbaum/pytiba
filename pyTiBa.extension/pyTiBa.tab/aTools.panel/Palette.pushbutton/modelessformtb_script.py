"""
Copyright (c) 2017 Cyril Waechter
Python scripts for Autodesk Revit
This file is part of pypevitmep repository at https://github.com/CyrilWaechter/pypevitmep
pypevitmep is an extension for pyRevit. It contain free set of scripts for Autodesk Revit:
you can redistribute it and/or modify it under the terms of the GNU General Public License
version 3, as published by the Free Software Foundation.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
See this link for a copy of the GNU General Public License protecting this package.
https://github.com/CyrilWaechter/pypevitmep/blob/master/LICENSE
"""
#! python3


from Autodesk.Revit import DB, UI
#from Autodesk.Revit.UI import 
from Autodesk.Revit.DB import ElementId, FilteredElementCollector, Transaction, TextNote, XYZ
from Autodesk.Revit.Exceptions import InvalidOperationException
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.UI import IExternalEventHandler, ExternalEvent

import os, sys
import rpw
import subprocess 
import pyrevit
from pyrevit import forms
import importlib
import System 
from System.Collections.Generic import List 
import traceback  
from pyrevit.loader.sessionmgr import find_pyrevitcmd , create_tmp_commanddata


from pyrevit.forms import WPFWindow


#for i in dir(importlib): print(i)

from pyrevit.forms import WPFWindow
doc = rpw.revit.doc
uidoc = rpw.revit.uidoc

__doc__ = "A simple modeless form sample"
__title__ = "Palette"
__author__ = "TBaumeister"
__persistentengine__ = True

# print os.path.dirname(__file__) + "\\TextModeless_script.py"


# Simple function we want to run
def textnotes():
    try:
        cmd = find_pyrevitcmd("pytiba-pytiba-atools-detail-modelessformtextnotes")  
        command_instance= cmd() 
        command_instance.Execute(create_tmp_commanddata(),'',DB.ElementSet()) #Execute Method from  UI.IExternelCommand Method
    except: 
        import traceback
        forms.alert(traceback.format_exc(), ok=True)

    
def detaillines():
    try:
        cmd = find_pyrevitcmd("pytiba-pytiba-atools-detail-modelessformlines")  
        command_instance= cmd()
        command_instance.Execute(create_tmp_commanddata(),'',DB.ElementSet()) #Execute Method from  UI.IExternelCommand Method  
        #sessionmgr.execute_command("pytibadev-pytibadev-atools-detail-modelessformlines") #THis is the Command ID, Pressing Shift+WIN + Click on pushbutton
    except:
        import traceback
        forms.alert(traceback.format_exc(), ok=True)

# 
def detailitem():
    try:
        cmd = find_pyrevitcmd("pytiba-pytiba-atools-detail-modelessformdetailitem")  
        command_instance= cmd()
        command_instance.Execute(create_tmp_commanddata(),'',DB.ElementSet()) #Execute Method from  UI.IExternelCommand Method  
        #sessionmgr.execute_command("pytibadev-pytibadev-atools-detail-modelessformlines") #THis is the Command ID, Pressing Shift+WIN + Click on pushbutton
    except:
        import traceback
        forms.alert(traceback.format_exc(), ok=True)

def genericanno():
    try:
        cmd = find_pyrevitcmd("pytiba-pytiba-atools-detail-modelessformgenericannotation")  
        command_instance= cmd()
        command_instance.Execute(create_tmp_commanddata(),'',DB.ElementSet()) #Execute Method from  UI.IExternelCommand Method  
        #sessionmgr.execute_command("pytibadev-pytibadev-atools-detail-modelessformlines") #THis is the Command ID, Pressing Shift+WIN + Click on pushbutton
    except:
        import traceback
        forms.alert(traceback.format_exc(), ok=True)



# Create a subclass of IExternalEventHandler
class SimpleEventHandler1(IExternalEventHandler):
    """
    Simple IExternalEventHandler sample 
    """

    # __init__ is used to make function from outside of the class to be executed by the handler. \
    # Instructions could be simply written under Execute method only
    def __init__(self, do_this):
        self.do_this = do_this
        
    # Execute method run in Revit API environment. See 5 Secrets of Revit API Coding.  
    def Execute(self, uiapp): 
        try: 
            #print "running Execute method of SimpleEventHandler"
            self.do_this() 
        except InvalidOperationException:
            # If you don't catch this exeption Revit may crash.
            print "InvalidOperationException catched"
        except:
            import traceback
            print traceback.format_exc()
            
    def GetName(self):
        return "simple function executed by an IExternalEventHandler in a Form"


# Now we need to make an instance of this handler. Moreover, it shows that the same class could be used to for
# different functions using different handler class instances
simple_event_handler1 = SimpleEventHandler1(textnotes) 
simple_event_handler2 = SimpleEventHandler1(detaillines) 
simple_event_handler3 = SimpleEventHandler1(genericanno) 
simple_event_handler4 = SimpleEventHandler1(detailitem) 


# We now need to create the ExternalEvent
ext_event = ExternalEvent.Create(simple_event_handler1) 
ext_event2 = ExternalEvent.Create(simple_event_handler2) 
ext_event3 = ExternalEvent.Create(simple_event_handler3) 
ext_event4 = ExternalEvent.Create(simple_event_handler4) 



# A simple WPF form used to call the ExternalEvent
class ModelessForm1(WPFWindow):
    """
    Simple modeless form sample
    """
    
    def __init__(self, xaml_file_name):
        WPFWindow.__init__(self, xaml_file_name)
        self.text1.Text = "Detail Palettes" 
        self.Show() 

    def textnotes_click(self, sender, e):
        ext_event.Raise() 

    def detaillines_click(self, sender, e):
        ext_event2.Raise()

    def genanno_click(self, sender, e):
        ext_event3.Raise()

    def detailitem_click(self, sender, e):
        ext_event4.Raise() 



modeless_form = ModelessForm1("ModelessForm.xaml")
