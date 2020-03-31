"""
Copyright (c) 2017 Cyril Waechter
Python scripts for Autodesk Revit

This file is part of pypevitmep repository at https://github.com/CyrilWaechter/pypevitmep

pypevitmep is an extension for pyRevit. It contain free set of scripts for Autodesk Revit:
you can redistribute it and/or modify it under the terms of the GNU General Public License
version 3, as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

See this link for a copy of the GNU General Public License protecting this package.
https://github.com/CyrilWaechter/pypevitmep/blob/master/LICENSE
"""
#! python3

import rpw
doc = rpw.revit.doc
uidoc = rpw.revit.uidoc

# noinspection PyUnresolvedReferences
from Autodesk.Revit.DB import Transaction, FamilySymbol
from Autodesk.Revit.UI.Selection import ObjectType

__doc__ = "Delete selected families from project"
__title__ = "Familytype delete"
__author__ = "Cyril Waechter"
__context__ = "Selection"


#from Darren Thomas - StackOverflow
def pickobject():
    from Autodesk.Revit.UI.Selection import ObjectType
    __window__.Hide()
    picked = uidoc.Selection.PickObject(ObjectType.Element)
    __window__.Show()
    __window__.Topmost = True
    return picked

def delete(idlist):
    t = Transaction(doc, "Delete families from project")
    t.Start()   # Find families of selected object and delete it
    try: 
        for id in idlist:
            doc.Delete(id)
    except: 
        import traceback    
        print traceback.format_exc()
    t.Commit()


sel = [doc.GetElement(i) for i in uidoc.Selection.GetElementIds()]

if sel:
    if sel[0].Category.Name.Equals("Lines"): 
        delete([i.LineStyle.Id for i in sel])
    else:
        delete([ i.GetTypeId() for i in sel])
    


