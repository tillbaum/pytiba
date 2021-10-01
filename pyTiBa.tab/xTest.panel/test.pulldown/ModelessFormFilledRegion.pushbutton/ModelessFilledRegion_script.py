"""
Copyright (c) 2020 Tillmann Baumeister
Python scripts for Autodesk Revit

"""
#! python3

from Autodesk.Revit import DB, UI
from Autodesk.Revit.UI import * 
from Autodesk.Revit.DB import FilledRegion, FilledRegionType, Line, CurveLoop, ElementId, FilteredElementCollector, Transaction, XYZ
from Autodesk.Revit.UI import IExternalEventHandler, ExternalEvent

from Autodesk.Revit.Exceptions import InvalidOperationException
from Autodesk.Revit.UI.Selection import ObjectType
import System.Windows

import sys
import System 
from System.Collections.Generic import List 
import traceback

from pyrevit.forms import WPFWindow

uidoc = __revit__.ActiveUIDocument 
doc = __revit__.ActiveUIDocument.Document # doc = DocumentManager.Instance.CurrentDBDocument 
uiapp = __revit__ # is the same as uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application 

__doc__ = "FilledRegion Palette" 
__title__ = "Palette\nFilledRegion" 
__author__ = "Tillmann Baumeister" 
__persistentengine__ = True



def createobj(type): 
    fecv = DB.FilteredElementCollector(doc).OfClass(DB.ViewDrafting) \
            .WhereElementIsNotElementType().ToElements()
    dv = [i for i in fecv if i.ViewName.Equals("xFilledReg")] 
    draftview = dv[0] if dv else None

    def GetFirstTextNoteUsingType(doc, texttype):
        bip = DB.BuiltInParameter.ELEM_TYPE_PARAM
        provider = DB.ParameterValueProvider(ElementId( bip ))
        evaluator = DB.FilterNumericEquals()
        rule = DB.FilterElementIdRule(provider, evaluator, texttype.Id )
        filter = DB.ElementParameterFilter( rule )

        fec = DB.FilteredElementCollector(doc, draftview.Id).OfClass(FilledRegion) \
              .WherePasses( filter ) \
              .FirstElement()
        return fec

    #fregiontype = FilteredElementCollector(doc).OfClass(FilledRegionType).ToElements()

    freg = GetFirstTextNoteUsingType(doc, type)

    if freg and draftview:
        # Select it/Add it to Selection
        listId = List[ElementId]()
        listId.Add(freg.Id)
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
    dv = [i for i in fecv if i.ViewName.Equals("xFilledReg")]
    draftview = dv[0] if dv else None 

    if not draftview: 
        t = Transaction(doc, "xFilledReg DrawingView")
        t.Start() 
        fec = DB.FilteredElementCollector(doc).OfClass(DB.ViewFamilyType).ToElements()
        viewdrafttype = [i for i in fec if i.ViewFamily.Equals(DB.ViewFamily.Drafting)][0]
        draftview = DB.ViewDrafting.Create(doc, viewdrafttype.Id)
        draftview.Name = "xFilledReg"  
        draftview.Scale = 100
        t.Commit()
        #print draftview, draftview.Name

    fr = FilteredElementCollector(doc, draftview.Id).OfClass(FilledRegion) \
                .WhereElementIsNotElementType() \
                .ToElements()

    frt = sorted(FilteredElementCollector(doc).OfClass(FilledRegionType).ToElements(),
                key = lambda x: x.get_Parameter(DB.BuiltInParameter.SYMBOL_NAME_PARAM).AsString().ToUpper() )
    #print len(fr), len(frt)
    lenfr = len(fr) if fr else 0
    #print lenfr

    if not lenfr == len(frt):
        if not lenfr == 0:
            t=Transaction(doc, "Delete FilledRegion")
            t.Start()
            [doc.Delete(i.Id) for i in fr]
            t.Commit()

        #create filled region rectangle in draftview xFilledReg
        def createfrs(frt):  
            #print "createfrs"
            ctr = 0 ; b = 7 ; c = -7 
            t = Transaction(doc, "Create TextNotes of all TextTypes in DraftingView")
            t.Start() 

            #for i, j in enumerate(frtypes):
            for k in range(10):
                if ctr == len(frt): 
                    break
                for l in range(10):
                    if ctr == len(frt):
                        break
                    profileloops = List[CurveLoop]()
                    curveloop = CurveLoop()
                    #curveList = List(Curve)[]
                    p = [XYZ(l*b, k*c, 0), XYZ(5+l*b, k*c, 0), XYZ(5+l*b, 5+k*c, 0), XYZ(l*b, 5+k*c, 0), XYZ(l*b, k*c, 0)]

                    for i in range(4):    
                        line = DB.Line.CreateBound(p[i], p[i+1])
                        curveloop.Append(line)

                    profileloops.Add(curveloop)
                    filledreg = FilledRegion.Create(doc, frt[ctr].Id, draftview.Id, profileloops)
                    ctr += 1 
            t.Commit() 
       
        createfrs(frt) 

    return  [(i.get_Parameter(DB.BuiltInParameter.SYMBOL_NAME_PARAM).AsString(), i) for i in frt] # Tupel


typelist = firstrun()
#for i in typelist: print i[0]
 
#createobj(typelist[1][1])
    


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
    exec("{} = {}".format(i, j))

    
# Create the External Event Handlers
ev = { "ext_event" + str(i) : "ExternalEvent.Create(handler" + str(i) + ")" for i in range(len(typelist))}
for i, j in ev.items(): 
	exec("{} = {}".format( i, j))



# A simple WPF form used to call the ExternalEvent
class ModelessForm(WPFWindow):
    """
    Simple modeless form sample
    """
   
    def __init__(self, xaml_file_name, buttonlist):
        WPFWindow.__init__(self, xaml_file_name)
        self.simple_text.Text = "FilledRegion <" + str(len(typelist)) + ">" 
        self.simple_text.FontSize = 18
        self.Title = "FilledRegion"
        
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

     
