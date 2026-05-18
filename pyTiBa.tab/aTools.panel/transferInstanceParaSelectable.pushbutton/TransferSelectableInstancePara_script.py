"""
Transfers all Instande Parrameters of Same Category 
(except Comment, Mark Parameter. 
Comment-, Mark-Parameter gen transferd if they contain a value other than None)

RebarCover Parameters, available when Structural Par is
activated are appended to a list. 

Copyright (c) 2017 Tillmann Baumeister
Python scripts for Autodesk Revit
GNU General Public License, version 3
"""
#! python3


__title__ = "Selected\nInstanceParas"
__author__ = "Tillmann Baumeister"


from Autodesk.Revit import DB
from Autodesk.Revit.DB import *
import sys, os
import pickle 
from pyrevit import forms 
from pyrevit.forms import TemplateListItem
from Autodesk.Revit.UI.Selection import ObjectType

import System 
from System.Collections.Generic import List 
import traceback

uidoc = __revit__.ActiveUIDocument 
doc = __revit__.ActiveUIDocument.Document # doc = DocumentManager.Instance.CurrentDBDocument 



class textnotetypeoption(TemplateListItem):
    """Sheet wrapper for :func:`select_sheets`."""
    def __init__(self, textnotetype):
        super(textnotetypeoption, self).__init__(textnotetype)
    
    @property
    def name(self):
        """Sheet name."""
        return '{0:<40s}' \
                    .format(self.item.Definition.Name)
           
def select_obj(list): 
    #doctitletxt = doc2.Title
    selected = forms.SelectFromList.show(sorted([textnotetypeoption(x) for x in list],
                        key= lambda x: x.name), 
					   title="Parameters: ",  #+ doctitletxt.ToUpper(), 
					   button_name="SELECT", 
					   width=450, 
                       height=800,
					   multiselect=True, 
					   filterfunc=None) 
                       
    return selected								   										   

#############################################################################################
    
try:
    #__window__.Hide()
    ref1 = uidoc.Selection.PickObject(ObjectType.Element)
    #__window__.Show()
    #__window__.Topmost = True
    
    pick1 = doc.GetElement(ref1) 
    catname = pick1.Category.Name 
except Exception: #The User aboted the pick operation
    pass
    

path = os.path.split(sys.argv[0])[0]

if __shiftclick__:
    so1 = [i for i in pick1.GetOrderedParameters() if not i.IsReadOnly]

    selectedparas = select_obj(so1)  
    if not selectedparas: 
        sys.exit()
    # get the Ids, Note: para.Definition.BuiltInParameter = OST_WALL_Offsett   ....value__  == para.Id
    selectedparIds = [ i.Definition.BuiltInParameter.ToString() for i in selectedparas]
    if selectedparIds:
    
        with open(path + "\\parameterSave.txt", "wb") as f:
            #f.seek(0) ;a = f.read() 
            pickle.dump(selectedparIds, f)
    else:
        sys.exit()

with open(path + "\\parameterSave.txt", "rb") as f:
        #f.seek(0) ;a = f.read() 
        dumpedpa = pickle.load(f)

dumped = ["WALL_BASE_CONSTRAINT", "-2324244", "WALL_BASE_OFFSET" ]

print dumpedpa

so1 = [pick1.get_Parameter(eval("BuiltInParameter." + i)) for i in dumpedpa]


try: 
    counter = 0
    while counter < 5:

        ref2 = uidoc.Selection.PickObject(ObjectType.Element)
        pick2 = doc.GetElement(ref2)

        if pick2.Category.Name.Equals(catname):
            #print "Equal"
            list = []
              
            t = DB.Transaction(doc, "Write Parameters")
            t.Start()
            
            for p in so1: 
                if not p.IsReadOnly:  
                    if p.StorageType.Equals(DB.StorageType.ElementId): pval = p.AsElementId()
                    if p.StorageType.Equals(DB.StorageType.Integer): pval = p.AsInteger()
                    if p.StorageType.Equals(DB.StorageType.String): pval = p.AsString()
                    if p.StorageType.Equals(DB.StorageType.Double): pval = p.AsDouble()
                    
                    try:
                        print p.Definition.Name
                        jpar = pick2.LookupParameter(p.Definition.Name)
                        
                        if jpar:
                            jpar.Set(pval)
                            print "Done"
                        else: 
                            list.append((p, p.Definition.Name, pval))
                    except TypeError: #Comment , Mark Parameter have TypeError: Multiple Values possible.
                        pass
                    except: 
                        list.append((p, p.Definition.Name, pval))
                        print "Error "
                        print traceback.format_exc() 
            t.Commit()
            if list:
                print "---------------------------------------------------------"
                for i in list: print i
        else:    
            forms.alert("Categories not the same", ok=True)
        counter += 1
except Exception: 
    pass
except:
    print traceback.format_exc()

        
