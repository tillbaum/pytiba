"""
Copyright (c) 2020 Tillmann Baumeister
Python scripts for Autodesk Revit

"""
#! python3

import sys
print(sys.version)
from Autodesk.Revit import DB, UI
#from Autodesk.Revit.UI import 
from Autodesk.Revit.DB import FilledRegion, FilledRegionType, Line, CurveLoop, ElementId, FilteredElementCollector, Transaction, XYZ
from Autodesk.Revit.UI import IExternalEventHandler, ExternalEvent

from Autodesk.Revit.Exceptions import InvalidOperationException, OperationCanceledException
from Autodesk.Revit import Exceptions
from Autodesk.Revit.UI.Selection import ObjectType

import sys
import System 
from System.Collections.Generic import List 
import traceback

from pyrevit.forms import WPFWindow

uidoc = __revit__.ActiveUIDocument 
doc = __revit__.ActiveUIDocument.Document # doc = DocumentManager.Instance.CurrentDBDocument 
uiapp = uidoc.Application # is the same as uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application 

__doc__ = "Palette FilledRegion"
__title__ = "Palette\nFilledRegion"
__author__ = "Tillmann Baumeister"
__persistentengine__ = True


def createobj(type): 
    try:
        #SetDefaultElementTypeId (for SystemFamilies)
        
        typegroup = DB.ElementTypeGroup.FilledRegionType #ElementTypeGroup Enumeration 
        #famCategoryId = type.Category.Id
        
        t = Transaction(doc, "FilledRegion")
        t.Start()
        doc.SetDefaultElementTypeId(typegroup, type.Id)
        #doc.SetDefaultFamilyTypeId(famCategoryId, type.Id)
        t.Commit()
        
        # Postable Command
        revitcomid= UI.RevitCommandId.LookupPostableCommandId(UI.PostableCommand.FilledRegion)
        if revitcomid:
            uiapp.PostCommand(revitcomid)

    except Exceptions.OperationCanceledException: 
        print("Error")
        
          
def firstrun():

    types = FilteredElementCollector(doc).OfClass(FilledRegionType) \
                             .WhereElementIsElementType().ToElements()
    #types = [i for i in columntypes if not i.FamilyName.Equals("Model Text")]


    typelist = sorted([(i.FamilyName + " - " + i.get_Parameter(DB.BuiltInParameter.SYMBOL_NAME_PARAM)\
            .AsString(), i) for i in types], 
            key = lambda x: x[0] )
    
    return typelist

typelist = firstrun()



# Create a subclass of IExternalEventHandler
class EventHandler(IExternalEventHandler):
    """
    Simple IExternalEventHandler sample
    """

    # __init__ is used to make function from outside of the class to be executed by the handler. \
    # Instructions could be simply written under Execute method only
    def __init__(self, do_this, type):
        self.do_this = do_this
        self.type = type
        
    # Execute method run in Revit API environment.
    def Execute(self, uiapp):
        
        try:
            self.do_this(self.type)
        except InvalidOperationException:
            # If you don't catch this exeption Revit may crash.
            print "InvalidOperationException catched"
            
    def GetName(self):
        return "simple function executed by an IExternalEventHandler in a Form"




ha = { "handler" + str(i) : "EventHandler(createobj, typelist[" + str(i) + "][1])" for i in range(len(typelist))}
for i, j in ha.items():
    exec( "{} = {}".format(i, j))

    
# Create the External Event Handlers
ev = { "ext_event" + str(i) : "ExternalEvent.Create(handler" + str(i) + ")" for i in range(len(typelist))}
for i, j in ev.items():
    exec( "{} = {}".format( i, j))



# A simple WPF form used to call the ExternalEvent
class ModelessForm(WPFWindow):
    """
    Simple modeless form sample
    """
    def __init__(self, xaml_file_name, buttonlist):
        WPFWindow.__init__(self, xaml_file_name)
        self.text1.Text = "FilledRegion (#" + str(len(typelist)) + ")"
        self.text1.FontSize = 16
        self.Title = "GenericModel"
        
        for i in range(len(typelist)):
            button = System.Windows.Controls.Button()
            button.Content = typelist[i][0]
            button.HorizontalContentAlignment = button.HorizontalAlignment.Left
            button.Name = "Button" + str(i)
            button.Height = 25
            button.Margin = System.Windows.Thickness(2,2,2,2)
            button.Click +=  eval("self.button" + str(i) + "_click")
            self.sp.Children.Add(button)    

        self.Show() 
    
    
    de = ["def button" + str(i) + "_click(self, sender, e): ext_event" + str(i) + ".Raise()\n" 
                                    for i in range(len(typelist))]
    for i in de:
        exec( "{}".format(i)) 
    
        
# Let's launch our beautiful and useful form !
modeless_form = ModelessForm("ModelessForm.xaml", typelist)  

     