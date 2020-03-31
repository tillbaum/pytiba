"""
Copyright (c) 2020 Tillmann Baumeister
Python scripts for Autodesk Revit

"""



from Autodesk.Revit import DB, UI
#from Autodesk.Revit.UI import 
from Autodesk.Revit.DB import ElementId, FilteredElementCollector, Transaction, TextNote, XYZ
from Autodesk.Revit.UI import IExternalEventHandler, ExternalEvent

from Autodesk.Revit.Exceptions import InvalidOperationException
from Autodesk.Revit.UI.Selection import ObjectType

import sys
import System 
from System.Collections.Generic import List 
import traceback

from pyrevit.forms import WPFWindow

uidoc = __revit__.ActiveUIDocument 
doc = __revit__.ActiveUIDocument.Document # doc = DocumentManager.Instance.CurrentDBDocument 
uiapp = __revit__ # is the same as uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application 

__doc__ = "TextNotes in a ModelessForm"
__title__ = "Palette\nTextNote"
__author__ = "Tillmann Baumeister"
__persistentengine__ = True


def createobj(type): 

    fecv = DB.FilteredElementCollector(doc).OfClass(DB.ViewDrafting) \
            .WhereElementIsNotElementType().ToElements()
    dv = [i for i in fecv if i.ViewName.Equals("xForm")]
    draftview = dv[0] if dv else None
    
    def GetFirstTextNoteUsingType(doc, texttype):
        bip = DB.BuiltInParameter.ELEM_TYPE_PARAM
        provider = DB.ParameterValueProvider(ElementId( bip ))
        evaluator = DB.FilterNumericEquals()
        rule = DB.FilterElementIdRule(provider, evaluator, texttype.Id )
        filter = DB.ElementParameterFilter( rule )

        fec = DB.FilteredElementCollector(doc, draftview.Id).OfClass(TextNote) \
              .WherePasses( filter ) \
              .FirstElement()
        return fec

    textnote = GetFirstTextNoteUsingType(doc, type)
        
    if textnote and draftview:
        # Select it/Add it to Selection
        listId = List[ElementId]()
        listId.Add(textnote.Id)
        # wall gets selected! 
        uidoc.Selection.SetElementIds(listId) 
     
        # Start CreateSimilar Command. 
        try:
            revitcomid= UI.RevitCommandId.LookupPostableCommandId(UI.PostableCommand.CreateSimilar)
            if revitcomid: 
                uiapp.PostCommand(revitcomid)       
        except:
            import traceback
            print traceback.format_exc()
        

def firstrun():
    # get Drafting View named "xForm" for object creation and Selection.
    fecv = DB.FilteredElementCollector(doc).OfClass(DB.ViewDrafting) \
            .WhereElementIsNotElementType().ToElements()
    dv = [i for i in fecv if i.ViewName.Equals("xForm")]
    draftview = dv[0] if dv else None 

    if not draftview: 
        t = Transaction(doc, "xForm")
        t.Start() 
        fec = DB.FilteredElementCollector(doc).OfClass(DB.ViewFamilyType).ToElements()
        viewdrafttype = [i for i in fec if i.ViewFamily.Equals(DB.ViewFamily.Drafting)][0]
        draftview = DB.ViewDrafting.Create(doc, viewdrafttype.Id)
        draftview.Name = "xForm"  
        draftview.Scale = 100
        t.Commit()
        #print draftview, draftview.Name

    notes = FilteredElementCollector(doc, draftview.Id).OfClass(TextNote) \
                .WhereElementIsNotElementType() \
                .ToElements()

    notetypes = sorted(DB.FilteredElementCollector(doc).OfClass(DB.TextNoteType).ToElements(),
                    key = lambda x: x.GetParameters("Type Name")[0].AsString() )
      
    if not notes or not len(notes) == len(notetypes):       
        
        # TextNote Create( Document document, ElementId viewId, XYZ position, string text, ElementId typeId )
        t= DB.Transaction(doc, "Create TextNotes of all TextTypes in DraftingView")
        t.Start() 
        if not len(notes) == len(notetypes): 
            [doc.Delete(i.Id) for i in notes]

        for i, j in enumerate(notetypes):
            text = j.GetParameters("Type Name")[0].AsString()
            textnote = DB.TextNote.Create(doc, draftview.Id, XYZ(0,-i*3.5, 0), text , j.Id)
        t.Commit()    


    return  [(i.GetParameters("Type Name")[0].AsString(), i) for i in notetypes] # Tupel


typelist = firstrun() 
#forms.alert(str(len(typelist)), ok=True)


#typelist = [j for i, j in enumerate(typelist) if i<21 ]
    

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
            #print "running Execute method of SimpleEventHandler"
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
    
    def __init__(self, xaml_file_name, typelist):
        WPFWindow.__init__(self, xaml_file_name)
        self.simple_text.Text = "TextNotes"
        self.simple_text.FontSize = 20
        self.typelist = typelist
        
        
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
    
    
    de = ["def button" + str(i) + "_click(self, sender, e): ext_event" + str(i) + ".Raise()\n" for i in range(15)]
    #forms.alert(str(de), ok=True)
    for i in de:
        exec( "{}".format(i))
    
        
# Let's launch our beautiful and useful form !
modeless_form = ModelessForm("ModelessFormText.xaml", typelist)  

  
