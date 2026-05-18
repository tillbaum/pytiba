"""
Deletes dimension, textnotes, filledRegions,
LineStyles permanently from the 
Project-file
""" 

#! python3

__title__ = "DEL_TextNote,FilledReg,LineStyle,TemplateView" 
__author__ = "TBaumeister" 


import sys
import System
from System.Collections.Generic import List 

from Autodesk.Revit.DB import * #(FilteredElementCollector, TextNoteType, DimensionType,
                                #FilledRegionType, BuiltInCategory)
from Autodesk.Revit import DB 
from pyrevit import forms
from pyrevit.forms import TemplateListItem, SelectFromList

from rpw import db


doc = __revit__.ActiveUIDocument.Document


def commandswitch(doc):  

    #optinos to show in CommandSwitch DialogWindow
    ops = [ "TextNote", "FilledRegion", "LineStyle", "TemplateView", "Dimension", "Material", "Wall",
            "Floor", "Ceiling", "Roof", "Grid", "GenericAnnotation", "GenericModel", "Stairs", "SectionHeads",
            "DetailComponent/Item", "RebarShape", "Rebar", "FamilyType/FamilySymbol", "AllTagTypes", "ExportDwgSettings" 
                ] 
    
    # CommandSwitchWindow Dialog
    catopt = forms.CommandSwitchWindow.show(ops, message="Select Category-Types ") 

    # Dict choosing the elements via the name string
    alltypes = {    "TextNote": FilteredElementCollector(doc).OfClass(DB.TextNoteType).ToElements(), 
                    "FilledRegion": FilteredElementCollector(doc).OfClass(DB.FilledRegionType) \
                                            .ToElements(), 
                    "LineStyle":    doc.Settings.Categories.get_Item(DB.BuiltInCategory.OST_Lines) \
                                        .SubCategories,
                    "TemplateView":  [x for x in FilteredElementCollector(doc) \
                                        .OfClass(DB.View).ToElements() if x.IsTemplate],
                    "Material":     FilteredElementCollector(doc).OfClass(DB.Material).ToElements(), 
                    "Wall":         FilteredElementCollector(doc).OfClass(DB.WallType).ToElements(), 
                    "Floor":        FilteredElementCollector(doc).OfClass(DB.FloorType).ToElements(), 
                    "Grid":         FilteredElementCollector(doc).OfClass(DB.GridType).ToElements(), 
                    "Ceiling":      FilteredElementCollector(doc).OfClass(DB.CeilingType).ToElements(), 
                    "Roof":         FilteredElementCollector(doc).OfClass(DB.RoofType).ToElements(), 
                    "GenericAnnotation": FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_GenericAnnotation).ToElements(), 
                    "GenericModel": FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_GenericModel) \
                                                    .WhereElementIsElementType().ToElements(), 
                    "Stairs":       FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Stairs) \
                                            .WhereElementIsElementType().ToElements(), 
                    "SectionHeads": FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_SectionHeads) \
                                                .WhereElementIsElementType().ToElements(), 
                    "DetailComponent/Item":  FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_DetailComponents) \
                                        .WhereElementIsElementType().ToElements(), 
                    "RebarShape":   FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RebarShape) \
                                            .WhereElementIsElementType().ToElements(), 
                    "Rebar":        FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rebar) \
                                                .WhereElementIsElementType().ToElements(), 
                    "FamilyType/FamilySymbol": FilteredElementCollector(doc).OfClass(FamilySymbol) \
                                                .WhereElementIsElementType().ToElements(),
                    "AllTagTypes":  [i for i in FilteredElementCollector(doc).OfClass(FamilySymbol).ToElements()
                                                if i.Category.Name.Contains("Tag")],
                    "ExportDwgSettings" : FilteredElementCollector(doc).OfClass(ExportDWGSettings).ToElements()
                    } 
                    
    if catopt== "Dimension": 
        alltypes = commandswitchdimtype(doc)
        selected = select_types(alltypes)
        if selected: 
            deletefromdoc(selected)
        elif not selected:
            return commandswitch(doc)
    elif catopt:
        selected = select_types(alltypes[catopt])
        if selected: 
            deletefromdoc(selected)
        return commandswitch(doc) 
    else: 
        return sys.exit() 


def commandswitchdimtype(doc): 
    ops = ["dimLinear","dimAngular", "dimRadial", "dimRadial", "dimDiameter", "SpotSlope",
                "SpotElevation", "SpotCoordinate"]
    dimoption = forms.CommandSwitchWindow.show(ops, message="Select DimensionType") 
    fecdim = FilteredElementCollector(doc).OfClass(DB.DimensionType).ToElements()           
            

    sysfamtype = {  "dimLinear" : [i for i in fecdim if i.StyleType.Equals(DB.DimensionStyleType.Linear)],
                    "dimAngular" : [i for i in fecdim if i.StyleType.Equals(DB.DimensionStyleType.Angular)],
                    "dimRadial" : [i for i in fecdim if i.StyleType.Equals(DB.DimensionStyleType.Radial)],
                    "dimDiameter" : [i for i in fecdim if i.StyleType.Equals(DB.DimensionStyleType.Diameter)],
                    "SpotCoordinate" : [i for i in fecdim if i.StyleType.Equals(DB.DimensionStyleType.SpotCoordinate)],
                    "SpotElevation" : [i for i in fecdim if i.StyleType.Equals(DB.DimensionStyleType.SpotElevation)],
                    "SpotSlope" : [i for i in fecdim if i.StyleType.Equals(DB.DimensionStyleType.SpotSlope)] }
        
    return sysfamtype[dimoption] 

 
    
def countinstances(doc, type): 
    type = GetFirstTypeNamed(doc, name)    

    fec = FilteredElementCollector(type.Document).WhereElementIsNotElementType().ToElements()
              #.Where(instance => instance.GetTypeId().IntegerValue.Equals(type.Id.IntegerValue)).ToList();
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
    

    
class textnotetypeoption(TemplateListItem): 
    """   """
    def __init__(self, textnotetype):
        super(textnotetypeoption, self).__init__(textnotetype)
    
    @property
    def name(self):
        """Sheet name."""
        
        return '{:<40s} '.format(extract(self.item)) #extract func

        
           
def select_types(sysfam): #list alltypes
    selected_types = SelectFromList.show(sorted([textnotetypeoption(x) for x in sysfam], 
                                                    key= lambda x: x.name),
                                               title='FamilyTYPES: ',
                                               button_name='DELETE PERMANENTLY from PROJECT',
                                               width=800,
                                               height=850,
                                               multiselect=True,
                                               filterfunc=None)
    return selected_types  



def deletefromdoc(obj_del):
    print "DEleting test"
    print type(obj_del) 
    
    t= DB.Transaction(doc, "Delete SystemFamilyType")
    t.Start()
    for i in obj_del:
        try: 
            print " {}, id={}  --> deleting".format(extract(i), i.Id)
            doc.Delete(i.Id)
            print " Done" 
        except:
            import traceback
            print traceback.format_exc()
    t.Commit()  

    
# sysfam = commandswitch()
# if not sysfam:
    # print "Sysfam is empt", sysfam
    # sys.exit()
# typelist= select_types(sysfam)
    
    
try: 
    commandswitch(doc)
    print "done"
except SystemExit as e: pass
except KeyError: pass
except:
    import traceback 
    print traceback.format_exc()  

            