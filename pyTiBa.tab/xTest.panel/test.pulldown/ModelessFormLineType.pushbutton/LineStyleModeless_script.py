"""
Copyright (c) 2017 TIllmann Baumeister

"""
#! python3


from Autodesk.Revit import DB, UI
#from Autodesk.Revit.UI import 
from Autodesk.Revit.DB import ElementId, Element, FilteredElementCollector, Transaction, TextNote, XYZ
import sys, os
import pickle 
from pyrevit import forms 
from pyrevit.forms import TemplateListItem
from Autodesk.Revit.UI.Selection import ObjectType

import System 
from System.Collections.Generic import List 
import traceback

uidoc = __revit__.ActiveUIDocument 

from Autodesk.Revit.UI import IExternalEventHandler, ExternalEvent

from Autodesk.Revit.Exceptions import InvalidOperationException
import rpw
from pyrevit.forms import WPFWindow

uidoc = __revit__.ActiveUIDocument 
doc = __revit__.ActiveUIDocument.Document # doc = DocumentManager.Instance.CurrentDBDocument 
uiapp = __revit__ # is the same as uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application 


__doc__ = "DetailLine Palette"
__title__ = "LineStyle\nPalette"
__author__ = "Cyril Waechter"
__persistentengine__ = True


def GetFirstDetailLineUsingType(doc, type, bip):
    bip = DB.BuiltInParameter.ELEM_TYPE_PARAM
    provider = DB.ParameterValueProvider(ElementId( bip ))
    evaluator = DB.FilterNumericEquals()
    rule = DB.FilterElementIdRule(provider, evaluator, type.Id )
    filter = DB.ElementParameterFilter( rule )

    fec = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Lines) \
          .WherePasses( filter ) \
          .FirstElement()
    return fec


# bip = DB.BuiltInParameter.ELEM_FAMILY
# provider = DB.ParameterValueProvider(ElementId( bip ))

# evaluator = DB.FilterStringRuleEvaluator().FilterStringEquals()

# rule = DB.FilterStringRule(provider, evaluator, "xForm", True )

# filter = DB.ElementParameterFilter( rule )

# fec = DB.FilteredElementCollector(doc).OfClass(View)) \ 
      # .WherePasses( filter ) \
      # .FirstElement()

    
def createobj(type): 
          
    # get Drafting View named "xForm" for object creation and Selection.
    fecv = DB.FilteredElementCollector(doc).OfClass(DB.ViewDrafting) \
            .WhereElementIsNotElementType().ToElements()
    dv = [i for i in fecv if i.ViewName.Equals("xForm")]
    draftview = dv[0] if dv else None
    
    # if not draftview: 
        # t = Transaction(doc, "xForm")
        # t.Start()
        # fec = DB.FilteredElementCollector(doc).OfClass(DB.ViewFamilyType).ToElements()
        # viewdrafttype = [i for i in fec if i.ViewFamily.Equals(DB.ViewFamily.Drafting)][0]
        # draftview = DB.ViewDrafting.Create(doc, viewdrafttype.Id)
        # draftview.Name = "xForm"  
        # t.Commit()
        #print draftview.Name
    
    # Get line of linestyle = type
    fec = FilteredElementCollector(doc, draftview.Id).OfCategory(DB.BuiltInCategory.OST_Lines) \
                .ToElements()           
    detailc = [i for i in  fec if i.CurveElementType.Equals(DB.CurveElementType.DetailCurve)] 
    li = [i for i in detailc if i.LineStyle.Id.Equals(type.Id)]
    line = li[0] if li else None  
        
    if line and draftview:
        # Select it/Add it to Selection
        listId = List[ElementId]()
        listId.Add(line.Id)
        uidoc.Selection.SetElementIds(listId) 
        # Start CreateSimilar Command. 
        try:
            revitcomid= UI.RevitCommandId.LookupPostableCommandId(UI.PostableCommand.CreateSimilar)
            if revitcomid: 
                uiapp.PostCommand(revitcomid)       
        except:
            import traceback
            print traceback.format_exc()
            #forms.alert("Exceptionn", ok=True) 

   
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


# lstylescat = doc.Settings.Categories.get_Item(DB.BuiltInCategory.OST_Lines) \
                                        # .SubCategories 

# lstyletypes = [(i.GetGraphicsStyle(DB.GraphicsStyleType.Projection).Name, 
                # i.GetGraphicsStyle(DB.GraphicsStyleType.Projection) ) for i in lstylescat]

#################################################

def firstrun():
    # get Drafting View named "xForm" for object creation and Selection.
    fecv = DB.FilteredElementCollector(doc).OfClass(DB.ViewDrafting) \
            .WhereElementIsNotElementType().ToElements()
    dv = [i for i in fecv if i.ViewName.Equals("xForm")]
    draftview = dv[0] if dv else None 
    #print "no draftview, create one", draftview

    if not draftview: 
        t = Transaction(doc, "xForm")
        t.Start() 
        fec = DB.FilteredElementCollector(doc).OfClass(DB.ViewFamilyType).ToElements()
        viewdrafttype = [i for i in fec if i.ViewFamily.Equals(DB.ViewFamily.Drafting)][0]
        draftview = DB.ViewDrafting.Create(doc, viewdrafttype.Id)
        draftview.Name = "xForm"  
        t.Commit()
        #print draftview, draftview.Name

    lines = FilteredElementCollector(doc, draftview.Id) \
                .OfCategory(DB.BuiltInCategory.OST_Lines) \
                .ToElements()
                   
    if not lines: 
        #print "NO line"
        t = Transaction(doc, "Draw Line")
        t.Start() 
        linee = DB.Line.CreateBound(XYZ.Zero, XYZ(0, 10, 0))
        singleline = doc.Create.NewDetailCurve( draftview, linee)
        t.Commit()
        lines = List[Element]()
        lines.Add(singleline)

    lstyles= sorted([(doc.GetElement(i).Name, doc.GetElement(i)) for i in lines[0].GetLineStyleIds() ])
    #print len(lstyles), len(lines)

    if not len(lstyles) == len(lines): 
        t = Transaction(doc, "Create Lines with Linestyles")
        t.Start()
        [doc.Delete(i.Id) for i in lines]
        for i in range(len(lstyles)):
            linee = DB.Line.CreateBound(XYZ(i*2,0,0), XYZ(i*2, 10, 0))
            line = doc.Create.NewDetailCurve( draftview, linee) 
            line.LineStyle = lstyles[i][1]
        t.Commit()    
    return lstyles
   
typelist = firstrun()       


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
        self.simple_text.Text = "Detail Lines"
        self.simple_text.FontSize = 20
        
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
            for i in range(len(typelist)) ]
    for i in de:
        exec( "{}".format(i))
    
        
# Let's launch form !
modeless_form = ModelessForm("ModelessForm.xaml", typelist)  

     

     
     
     
     
     
     
     
     
     
     