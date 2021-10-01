'''
Select views (callouts, sections, elevations, legends, schedules)
and 1 Sheet (or more than 1) in the Prj-Browser. 
The Views will be added to the Sheets if possible. 
Model views will only be added to the first 
selected sheet since they can not exist on multiple sheets. 
If no sheet is selected the SheetSelection-Form will pop up. 
\n\nShift+Click:\n 
Pick source views from list instead of selection or active view.
''' 


from pyrevit import revit, DB
from pyrevit import forms
from pyrevit import script
import traceback
from Autodesk.Revit.UI import * #UIDocument
from Autodesk.Revit import DB

uidoc = __revit__.ActiveUIDocument 
doc = __revit__.ActiveUIDocument.Document # doc = DocumentManager.Instance.CurrentDBDocument 
uiapp = __revit__ # is the same as uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application 

__author__ = 'Dan Mapes + Tillmann Baumeister'

#logger = script.get_logger()

selection = [doc.GetElement(elId) for elId in uidoc.Selection.GetElementIds() ]
selected_views = [i for i in selection if i.Category.Name.Equals("Views")]


dest_sheets = [selection.pop(i)  for i,j in enumerate(selection) 
                    if j.Category.Name.Equals("Sheets")]
#print dest_sheets 

if not selected_views:    #noqa
    selected_views = forms.select_views()
print "selected_views: ", selected_views 

       # if not isinstance(selected_views, DB.View):
       # forms.alert('Active view must be placable on a sheet.', exit=True)
if selected_views:
    if not dest_sheets:
        # check if activeView is Sheet, choose this as dest_sheet
        if __revit__.ActiveUIDocument.ActiveView.ViewType.Equals(DB.ViewType.DrawingSheet):
            dest_sheets.append(__revit__.ActiveUIDocument.ActiveView)
        else:
        # get the destination sheets from user via forms Selection Dialog
            dest_sheets = forms.select_sheets()
    print "dest_sheet: ", dest_sheets
    if dest_sheets:
        with revit.Transaction("Add Views to Sheets"):
            for i in selected_views:
                for sheet in dest_sheets:
                    try:
                        DB.Viewport.Create(revit.doc, sheet.Id, i.Id, DB.XYZ(0, 0, 0))
                    except Exception as place_err:
                        print traceback.format_exc()
    else: 
        forms.alert('No Sheet selected.') 
else:
    forms.alert('No views selected.') 




