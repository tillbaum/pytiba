"""
Deletes selected FamilyTypes:
Letz the user pick a category and 
opens all Types in a SelectFromList Dialog.
Annotation Elemends (2D) and Model Elements (3D)
c. 6.01.2020 T.Baumeister 
"""
#! python3

__title__ = "DEL_PickFamType_Model/Anno" 
__author__ = "TBaumeister" 	


import sys, os

from Autodesk.Revit.DB import (FilteredElementCollector, TextNoteType, DimensionType, 
                                DimensionStyleType, FilledRegionType, BuiltInCategory, ElementId) 
                                
from Autodesk.Revit import DB
from Autodesk.Revit.UI.Selection import ObjectType  
                          
from pyrevit import forms 
from pyrevit.forms import TemplateListItem, SelectFromList

from rpw import db

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument 

    
class textnotetypeoption(TemplateListItem): 
    """Sheet wrapper for :func:`select_sheets`."""
    def __init__(self, textnotetype):
        super(textnotetypeoption, self).__init__(textnotetype)

    @property
    def name(self):
        """Dim Typename."""
        return '{0:<40} '.format(extract(self.item) )

        
def select_type(typelist):

    selected_types = SelectFromList.show(sorted([textnotetypeoption(x) for x in typelist],
                        key= lambda x: x.name), 
					   title="Select SystemFamilyTypes", 
					   button_name="DELETE PERMANENTLY from PROJECT", 
					   width=600, 
					   multiselect=True, 
					   filterfunc=None) 
                       
    return selected_types 									   										   


def deletefromdoc(obj_del):  
    t= DB.Transaction(doc, "Delete SystemFamilyType")  
    t.Start() 
    for i in obj_del: 
		try: 
			text = i.GetParameters("Type Name")[0].AsString() #> 4mm Arial   
			print " {}, id={}  --> deleting".format(text, i.Id) 
			doc.Delete(i.Id) 
			print " Done"  
		except: 
			import traceback 
			print traceback.format_exc() 
    t.Commit() 


    
def countinstances(doc, type):

    fec = FilteredElementCollector(type.Document).WhereElementIsNotElementType().ToElements()
              #.Where(instance => instance.GetTypeId().IntegerValue.Equals(type.Id.IntegerValue));
    elem = [i for i in fec if i.GetTypeId().IntegerValue.Equals(type.Id.IntegerValue)]                    
    return elem.Count                    
                              
             
    
def extract(obj):
    ls = []
    try: 
        a= obj.Category.Name
        ls.append(a)
    except: pass
    try:
        b= obj.FamilyName
        ls.append(b)
    except: pass
    try:
        c = obj.GetParameters("Type Name")[0].AsString()
        
        ls.append(c)
    except: pass
    try:
        d = obj.Name
        ls.append(d) 
    except: pass
    try:
        e = obj.Id
        ls.append(e)
    except: pass
    try:
        f =  str(countinstances(doc, obj)) + " Instances"
        
        ls.append(f)
    except: pass
    return " / ".join(str(x) for x in ls) 
    
    
    
try:
    sel = [doc.GetElement(elId) for elId in uidoc.Selection.GetElementIds()]
    if sel: type_Ids = sel[0].GetValidTypes()  
    elif not sel:
        reference = uidoc.Selection.PickObject(ObjectType.Element)
        type_Ids = doc.GetElement(reference.ElementId).GetValidTypes()
        
    
    types = [doc.GetElement(elid) for elid in type_Ids] 

    if not types: 
        sys.exit(0) 
    elif types:
        obj_del = select_type(types) 
    if obj_del: 
        deletefromdoc(obj_del)  
except:
    #pass
    import traceback
    print traceback.format_exc()

