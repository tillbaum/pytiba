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
from Autodesk.Revit import UI, DB
from Autodesk.Revit.DB import Transaction
import os, sys
from Autodesk.Revit.Exceptions import InvalidOperationException
import rpw
import subprocess 
import pyrevit
from pyrevit import forms
import importlib
import System 
from System.Collections.Generic import List 
import traceback  
from pyrevit.loader.sessionmgr import *


from pyrevit.forms import WPFWindow


#for i in dir(importlib): print(i)

from pyrevit.forms import WPFWindow
doc = rpw.revit.doc
uidoc = rpw.revit.uidoc

__doc__ = "A simple modeless form sample"
__title__ = "Modeless Form"
__author__ = "Cyril Waechter"
__persistentengine__ = True

# print os.path.dirname(__file__) + "\\TextModeless_script.py"


# Simple function we want to run
def runscript():
    try:
        #path1 = os.path.dirname(__file__) #+ "\\test.py" 
        #forms.alert(path1, ok=True) 
        #forms.alert(path1, ok=True) 
        #sys.path.append(path1) 
        #importlib.import_module("TextModeless_script")  
        cmd = find_pyrevitcmd("pytibadev-pytibadev-atools-detail-modelessformlines")
        print cmd
        forms.alert(str(cmd))
        command_instance= cmd()
        type = command_instance.Execute()
        
        
        #sessionmgr.execute_command("pytibadev-pytibadev-atools-detail-modelessformlines") #THis is the Command ID, Pressing Shift+WIN + Click on pushbutton
        
        #os.system("TextModeless_script.py")    
        #subprocess.call(path)
        #import TextModeless_script 
        #test.warn() 
        #execfile(path)
    except:
        import traceback
        forms.alert(traceback.format_exc(), ok=True)
    #forms.alert(typelist, ok=True)
    #import TextModeless_script as s1
    #s1.firstrun()
           # path = os.path.dirname(os.path.dirname(__file__)) + "TextModeless_script.py"
       # execfile("test.py")
    
    #subprocess.Popen("TextModeless_script.py")
    




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
simple_event_handler1 = SimpleEventHandler1(runscript)

# We now need to create the ExternalEvent
ext_event = ExternalEvent.Create(simple_event_handler1)


# A simple WPF form used to call the ExternalEvent
class ModelessForm1(WPFWindow):
    """
    Simple modeless form sample
    """
    
    def __init__(self, xaml_file_name):
        WPFWindow.__init__(self, xaml_file_name)
        self.simple_text.Text = "Hello World"
        self.Show()

    def delete_click(self, sender, e):
        # This Raise() method launch a signal to Revit to tell him you want to do something in the API context
        ext_event.Raise()

modeless_form = ModelessForm1("ModelessForm.xaml")  
