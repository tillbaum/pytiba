"""
Copyright (c) 2017 Cyril Waechter

"""

__doc__ = "simple external event which just delete selection"
__title__ = "ExEvent Delete"
__author__ = "Cyril Waechter"

# noinspection PyUnresolvedReferences
from Autodesk.Revit.UI import IExternalEventHandler, IExternalApplication, Result, ExternalEvent, IExternalCommand
# noinspection PyUnresolvedReferences
from Autodesk.Revit.DB import Transaction
# noinspection PyUnresolvedReferences
from Autodesk.Revit.Exceptions import InvalidOperationException
import pyrevit.forms
import rpw
doc = rpw.revit.doc
uidoc = rpw.revit.uidoc

def pickobject():
    from Autodesk.Revit.UI.Selection import ObjectType
    __window__.Hide()
    picked = uidoc.Selection.PickObject(ObjectType.Element)
    __window__.Show()
    __window__.Topmost = True
    return picked




class ExternalEventMy(IExternalEventHandler):
    def Execute(self, uiapp):
        try:
            #forms.alert("sdlfaf", ok=True)
            
            with rpw.db.Transaction("MyEvent"):
                sel = pickobject()
                for elid in sel.Id:  #uidoc.Selection.GetElementIds():
                    doc.Delete(elid)
        except InvalidOperationException:
            print "exception catched"
        except:
            import traceback
            print traceback.format_exc()

    def GetName(self):
        return "my event"

handler_event = ExternalEventMy()
print handler_event

exEvent = ExternalEvent.Create(handler_event)

print exEvent


rai = exEvent.Raise()

print rai

rai.Pending


#execu = ExternalEventMy.Execute(handler_event, uidoc)


