"""
Transfers all Instance Parrameters of Same Category Elements.
except: Comment, Mark Parameter.
RebarCover Parameters, which are available when Structural Par is
activated are appended to a list. 
09.01.2020.  
New Idea: Make Transferable Parameter be selelctable. 
Selection-Dialog. 
"""
__title__ = "TransferALL\nInstanceParas"
__author__ = "Tillmann Baumeister"


from Autodesk.Revit import DB
#from Autodesk.Revit.DB import *
import sys
from pyrevit import forms 
from Autodesk.Revit.UI.Selection import ObjectType

import System 
from System.Collections.Generic import List 
import traceback

uidoc = __revit__.ActiveUIDocument 
doc = __revit__.ActiveUIDocument.Document # doc = DocumentManager.Instance.CurrentDBDocument 

try:
    #__window__.Hide()
    ref1 = uidoc.Selection.PickObject(ObjectType.Element)
    #__window__.Show()
    #__window__.Topmost = True
    
    pick1 = doc.GetElement(ref1) 
    catname = pick1.Category.Name 

    so1 = pick1.GetOrderedParameters()
    
except Exception: #The User aboted the pick operation
    pass


try: 
    counter = 0
    while counter < 10:

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
                        #print p.Definition.Name
                        jpar = pick2.LookupParameter(p.Definition.Name)
                        
                        if jpar:
                            jpar.Set(pval)
                            #print "Done"
                        else: 
                            list.append((p, p.Definition.Name, pval))
                    except TypeError: #Comment , Mark Parameter have TypeError: Multiple Values possible.
                        pass
                    except: 
                        list.append((p, p.Definition.Name, pval))
                        #print "Error "
                        #print traceback.format_exc() 
            t.Commit()
            if list:
                print "---------------------------------------------------------"
                for i in list: print i
        else:    
            forms.alert("Categories not the same", ok=True)
        counter += 1
except Exception: 
    pass #print traceback.format_exc()
except:
    print traceback.format_exc()

        
# def getnsetBIP(elem, bip, setvalue):
    # try: para = elem.get_Parameter(bip) #BuiltInParameter.SHEET_WIDTH
    # except: pass
    # para.Set(setvalue)
    # return para.AsString()
        
        
        
# def readsetparas(readP, writeP)
    # value = {"String": p.AsString(), "Double":p.AsDouble() * 0.3048, "ElementId": p.AsElementId()}

    # value[p.StorageType.ToString()] 


# class ElemFilterinterface (Selection.ISelectionFilter):
	
  # def AllowElement(self, element, catname):
        # if element.Category.Name == catname:
            # return True
        # return False 


	
# class ElemFilterinterface (Selection.ISelectionFilter):
	# def AllowElement(self, element):
		# if element.Category.Name == "Walls"
            # return True
        # return False 
