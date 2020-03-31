"""
Transfers all I
"""
#! python3

from Autodesk.Revit import DB, UI
#from Autodesk.Revit.UI import 
from Autodesk.Revit.DB import ElementId, FilteredElementCollector, Transaction, TextNote, XYZ
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


__doc__ = "PostCommand_DetailLine"
__title__ = "Modeless Form"
__author__ = "Cyril Waechter"
__persistentengine__ = True

 
lstylescat = doc.Settings.Categories.get_Item(DB.BuiltInCategory.OST_Lines) \
                                        .SubCategories 

lstyletypes = [(i.GetGraphicsStyle(DB.GraphicsStyleType.Projection).Name, 
                i.GetGraphicsStyle(DB.GraphicsStyleType.Projection) ) for i in lstylescat]
  
type = lstyletypes[9][1]


          
def createobj(type): 
          
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
        t.Commit()
        print draftview.Name
    
    # Get line of linestyle = type
    fec = FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Lines) \
                .ToElements()           
    detailc = [i for i in  fec if i.CurveElementType.Equals(DB.CurveElementType.DetailCurve)] 
    li = [i for i in detailc if i.LineStyle.Id.Equals(type.Id)]
    line = li[0] if li else None  
        
        
    if not line:       
        print "line not found"
        
        try:
            t = Transaction(doc, "Draw Line")
            t.Start()
            linee = DB.Line.CreateBound(XYZ.Zero, XYZ(0, 10, 0))
            line = doc.Create.NewDetailCurve( draftview, linee)
            print type
            line.LineStyle = type
            t.Commit()   
        except:
            import traceback
            print traceback.format_exc()

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



type = lstyletypes[8][1]
            
createobj(type)            


        
        