"""
Copy FamilyTypes from Prj to Prj"
The Active Prj is the ONE Types are copied to.
"""
#! pyhton3

__title__ = "Import FamTypes from Prj" 
__author__ = "Tillmann Baumeister" 

from Autodesk.Revit.DB import * #(FilteredElementCollector, Transaction, 
                                #BuiltInParameter, Level, ElementId, BuiltInCategory)
from Autodesk.Revit import DB, UI
import sys, os

from pyrevit import forms 
from Autodesk.Revit.UI.Selection import ObjectType
from pyrevit.forms import TemplateListItem, SelectFromList
import traceback

import System 
from System.Collections.Generic import List 

uidoc = __revit__.ActiveUIDocument 
doc = __revit__.ActiveUIDocument.Document # doc = DocumentManager.Instance.CurrentDBDocument 
uiapp = __revit__ # is the same as uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application 


def commandswitch(sourcedoc, activedoc):
    doc = sourcedoc
    #optinos to show in CommandSwitch DialogWindow
    ops = [ "Switch Project", "TextNote", "FilledRegion", "LineStyle", "TemplateView", "Dimension", "Material", "Wall",
                "Floor", "Ceiling", "Roof", "Grid", "GenericAnnotation", "GenericModel", "Stairs", "SectionHeads",
                "DetailComponent", "RebarShape", "Rebar", "FamilyType/FamilySymbol", "AllTagTypes", "ExportDwgSettings" 
                ] 
    global catopt
    
    cfgs = {'Switch Project': { 'backround': '0xFF55AA'}}
    
    if sourcedoc.Title == activedoc.Title:
        titletext = "DELETE MODE: {} ".format(activedoc.Title.ToUpper() )
    else: 
        titletext = "copy from: {}".format(sourcedoc.Title).ToUpper() 
    
    # CommandSwitchWindow Dialog
    catopt = forms.CommandSwitchWindow.show(ops, 
                                    config = cfgs, 
                                    message= titletext
                                    )

    # Dict choosing the elements via the name string
    famtypes = { "TextNote": FilteredElementCollector(doc).OfClass(DB.TextNoteType).ToElements(),
                "FilledRegion": FilteredElementCollector(doc).OfClass(DB.FilledRegionType) \
                                            .ToElements(), 
                "LineStyle":    doc.Settings.Categories.get_Item(DB.BuiltInCategory.OST_Lines) \
                                        .SubCategories,
                "TemplateView":  [x for x in FilteredElementCollector(doc) \
                                        .OfClass(DB.View).ToElements() if x.IsTemplate],
                "Material":     FilteredElementCollector(doc).OfClass(DB.Material).ToElements(), 
                "Wall":         FilteredElementCollector(doc).OfClass(DB.WallType).ToElements(), 
                "Floor":         FilteredElementCollector(doc).OfClass(DB.FloorType).ToElements(), 
                "Grid":         FilteredElementCollector(doc).OfClass(DB.GridType).ToElements(), 
                "Ceiling":         FilteredElementCollector(doc).OfClass(DB.CeilingType).ToElements(), 
                "Roof":         FilteredElementCollector(doc).OfClass(DB.RoofType).ToElements(), 
                "GenericAnnotation": FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_GenericAnnotation).ToElements(), 
                "GenericModel": FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_GenericModel) \
                                                    .WhereElementIsElementType().ToElements(), 
                "Stairs":       FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Stairs) \
                                            .WhereElementIsElementType().ToElements(), 
                "SectionHeads": FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_SectionHeads) \
                                                .WhereElementIsElementType().ToElements(), 
                "DetailComponent":  FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_DetailComponents) \
                                        .WhereElementIsElementType().ToElements(), 
                "RebarShape":   FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RebarShape) \
                                            .WhereElementIsElementType().ToElements(), 
                "Rebar":        FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rebar) \
                                                .WhereElementIsElementType().ToElements(), 
                "FamilyType/FamilySymbol":  FilteredElementCollector(doc).OfClass(FamilySymbol).ToElements(),
                "AllTagTypes":  [i for i in FilteredElementCollector(doc).OfClass(FamilySymbol).ToElements()
                                                if i.Category.Name.Contains("Tag")],
                "ExportDwgSettings": FilteredElementCollector(doc).OfClass(ExportDWGSettings).ToElements(),
                }
                
    if catopt == "Dimension":
        types = commandswitchdimtype(sourcedoc, activedoc)
        return select_types(types)
        
    if catopt == "Switch Project":
        doc2 = switchdocdlg()
        return commandswitch(doc2, activedoc)      
        
    else:
        return select_types(famtypes[catopt], sourcedoc, activedoc)

    
def commandswitchdimtype(sourcedoc, activedoc):
    doc = activedoc
    
    ops = ["dimLinear","dimAngular", "dimRadial", "dimRadial", "dimDiameter", "SpotSlope",
        "SpotElevation", "SpotCoordinate"]
        
    if sourcedoc.Title == activedoc.Title:
        titletext = "DELETE MODE: {} ".format(activedoc.Title.ToUpper() )
    else: 
        titletext = "copy from: {}".format(sourcedoc.Title).ToUpper() 

    dimoption = forms.CommandSwitchWindow.show(
                    ops,
                    message= titletext )
    
    fecdim = FilteredElementCollector(doc).OfClass(DB.DimensionType).ToElements()           
            
    types = {	"dimLinear" : [i for i in fecdim if i.StyleType.Equals(DB.DimensionStyleType.Linear)],
                    "dimAngular" : [i for i in fecdim if i.StyleType.Equals(DB.DimensionStyleType.Angular)],
                    "dimRadial" : [i for i in fecdim if i.StyleType.Equals(DB.DimensionStyleType.Radial)],
                    "dimDiameter" : [i for i in fecdim if i.StyleType.Equals(DB.DimensionStyleType.Diameter)],
                    "SpotCoordinate" : [i for i in fecdim if i.StyleType.Equals(DB.DimensionStyleType.SpotCoordinate)],
                    "SpotElevation" : [i for i in fecdim if i.StyleType.Equals(DB.DimensionStyleType.SpotElevation)],
                    "SpotSlope" : [i for i in fecdim if i.StyleType.Equals(DB.DimensionStyleType.SpotSlope)] }
    		  	  
    # print sysfamtype[dimoption].Count
    # print "{0}, \n Size: {1} ".format(sysfamtype[dimoption], sysfamtype[dimoption].Count)
    
    if dimoption:
        return select_types(types[dimoption], sourcedoc, activedoc)
    elif not dimoption:
        return commandswitch(sourcedoc, activedoc)

    
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
    return " - ".join(str(x) for x in ls) 
    
    
    
class textnotetypeoption(TemplateListItem): 
    """Sheet wrapper for :func:`select_sheets`."""
    def __init__(self, textnotetype):
        super(textnotetypeoption, self).__init__(textnotetype)
    
    @property
    def name(self):
        """Sheet name."""
        
        self.list = extract(self.item)
        return '{:<40s} - {} '.format(self.list, self.item.Id)
 
  
def select_types(list, sourcedoc, activedoc): 
    
    if sourcedoc.Title == activedoc.Title:
        titletext = "DELETION MODE: {} ".format(activedoc.Title.ToUpper() )
        buttontext = "DELETE PERMANENTLY from PROJECT"
    else: 
        titletext = "copy from: {}".format(sourcedoc.Title).ToUpper() 
        buttontext = "COPY to {}".format(activedoc.Title.ToUpper())
    doctitletxt = sourcedoc.Title 
    
    selected_types = forms.SelectFromList.show(sorted([textnotetypeoption(x) for x in list],
                        key= lambda x: x.name), 
					   title= titletext, 
					   button_name= buttontext ,
					   width=500, 
                       height=800,
					   multiselect=True, 
					   filterfunc=None) 
    if not selected_types: 
        return commandswitch(sourcedoc, activedoc)
    elif selected_types and not activedoc.Title == sourcedoc.Title:
        
        copyfromdoc(selected_types, sourcedoc, activedoc)
        return commandswitch(sourcedoc, activedoc)
    elif selected_types and activedoc.Title == sourcedoc.Title:
        deletefromdoc(selected_types, activedoc)
        return commandswitch(sourcedoc, activedoc)

def openproject():
    activedoc = doc
    
    fileDlg = UI.FileOpenDialog( "All Revit files (*.rvt, *.rfa, *.rte, *.rft)|*.rvt;*.rfa;*.rte;*.rft" )
    fileDlg.Show()
    modelPath = fileDlg.GetSelectedModelPath()
    openopt = DB.OpenOptions()
 
    if modelPath:
        #doc2 = app.OpenDocumentFile(modelPath, openopt) 
        uidoc2 = uiapp.OpenAndActivateDocument(modelPath, openopt, False)
        doc2 = uidoc2.Document
        
        #Switch Back to doc1 , Make doc1 Active
        doc1path = activedoc.PathName #("String")
        uiapp.OpenAndActivateDocument(doc1path)
        return doc2 
        
    elif not modelPath:
        return switchdocdlg()
        
        
def switchdocdlg():

    docs = __revit__.Application.Documents #returns a set 

    doclist =[i for i in docs] #if not i.Title.Equals(activedoc.Title)]

    doctitle = [i.Title for i in doclist] 
    list = ["Open ProjectFile"] + doctitle
    
    selected = forms.CommandSwitchWindow.show(list ,
                        message="Choose Source Project" )
                        
    dic_docs = {i.Title: i for i in doclist}

    sourcedoc = openproject() if selected == "Open ProjectFile" else dic_docs[selected]
    if sourcedoc: 
        return sourcedoc
        
    else: return switchdocdlg()
    

def copyfromdoc(typelist, sourcedoc, activedoc):    
    idlist = List[ElementId]()
    [idlist.Add(i.Id) for i in typelist]
    
    try:
        t= Transaction(doc, "copy ViewTemplates")
        t.Start()
        DB.ElementTransformUtils.CopyElements(sourcedoc, idlist, activedoc, None, DB.CopyPasteOptions())
        t.Commit()
        for i in typelist: 
            print i.ToString() + "  --> copied "  #"{} - {} --> copied ".format(i.Name , i.Id) 
               
        #forms.alert("Copied from {} to {} : \n{}".format(sourcedoc.Title, activedoc.Title, text ))
    except: 
        print traceback.format_exc() 

        
def deletefromdoc(obj_del, doc):
    ilist = List[ElementId]()
    [ilist.Add(i.Id) for i in obj_del]
    try: 
        t= DB.Transaction(doc, "Delete Types")
        t.Start()
        doc.Delete(ilist)
        t.Commit()			
    except:
        import traceback
        print traceback.format_exc()
    for i in obj_del: 
        print extract(i) + " --> Deleting "

 


#--------------------------------------------------------------------------- 
activedoc = doc  
docs = __revit__.Application.Documents #returns a set  

try: 
    if docs.Size == 1: 
        doc2= switchdocdlg()
        commandswitch(doc2, activedoc)

    elif docs.Size == 2:
        doc2 = [i for i in docs if not i.Title.Equals(activedoc.Title)][0] 
        commandswitch(doc2, activedoc)
        
    elif docs.Size > 2:
        doc2 = switchdocdlg()

        commandswitch(doc2, activedoc)
except KeyError: 
    pass
except:
    import traceback
    print traceback.format_exc()
  


  
