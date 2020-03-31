"""
Copy TemplateViews from 2 open documents

"""

__title__ = "Copy TEmplateViews from doc"
__author__ = "Tillmann Baumeister"

from Autodesk.Revit.DB import FilteredElementCollector, Transaction, BuiltInParameter, Level, ElementId
from Autodesk.Revit import DB
import sys, os

from pyrevit import forms 
from Autodesk.Revit.UI.Selection import ObjectType
from pyrevit.forms import TemplateListItem, SelectFromList


import System 
from System.Collections.Generic import List 

uidoc = __revit__.ActiveUIDocument 
doc = __revit__.ActiveUIDocument.Document # doc = DocumentManager.Instance.CurrentDBDocument 
uiapp = __revit__ # is the same as uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application 




class textnotetypeoption(TemplateListItem): 
    """Sheet wrapper for :func:`select_sheets`."""
    def __init__(self, textnotetype):
        super(textnotetypeoption, self).__init__(textnotetype)

    @property
    def name(self):
        """Dim Typename."""
        return '{0:<40} {1:<30s}'.format(self.item.Name, self.item.Id)
     
def select_template(list): 
    selected_types = SelectFromList.show(sorted([textnotetypeoption(x) for x in list],
                        key= lambda x: x.name), 
					   title="Select SystemFamilyTypes", 
					   button_name="Select", 
					   width=500, 
					   multiselect=True, 
					   filterfunc=None) 
                       
    return selected_types 									   										   

    
docs = __revit__.Application.Documents #returns a set 

activedoc = doc 

if docs.Size == 1:
    forms.alert("Open 2nd Revit-Project \n to copy from", ok=True)
    sys.exit()
    # copy from doc2 to doc
    
elif docs.Size == 2:
    copyfromdoc = [i for i in docs if not i.Title.Equals(activedoc.Title)][0] 
       
else:
    doclist =[i for i in docs if not i.Title.Equals(activedoc.Title)]
    
    selectedtitle = forms.CommandSwitchWindow.show([i.Title for i in doclist],
                        message="Select System-Category to copy ")
    
    dict_docs = {i.Title:i for i in doclist}
    copyfromdoc = dict_docs[selectedtitle]



fecvt = FilteredElementCollector(copyfromdoc).OfClass(DB.View).ToElements()
viewtemps = [i for i in fecvt if i.IsTemplate]  
    
    
try:
    selectedvt = select_template(viewtemps)
    if not selectedvt:
        sys.exit()
    idlist = List[ElementId]()
    [idlist.Add(i.Id) for i in selectedvt]

    t= Transaction(doc, "copy ViewTemplates")
    t.Start()
    DB.ElementTransformUtils.CopyElements(copyfromdoc, idlist, activedoc, None, DB.CopyPasteOptions())
    t.Commit()
except SystemExit as e: pass
except: 
    import traceback
    print traceback.format_exc()


