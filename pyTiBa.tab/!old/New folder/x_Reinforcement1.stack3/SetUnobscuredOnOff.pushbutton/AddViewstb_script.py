"""Add selected view to selected sheets."""

from pyrevit import revit, DB
from pyrevit import forms
from pyrevit import script
import traceback
from Autodesk.Revit.UI import *

uidoc = __revit__.ActiveUIDocument 
doc = __revit__.ActiveUIDocument.Document # doc = DocumentManager.Instance.CurrentDBDocument 
uiapp = __revit__ # is the same as uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application 

__author__ = 'Dan Mapes + Tillmann Baumeister'

__doc__ = '''
Select views (callouts, sections, elevations, legends, schedules)
and 1 Sheet (or more than 1) in the Prj-Browser. 
The Views will be added to the Sheets if possible. 
Model views will only be added to the first 
selected sheet since they can not exist on multiple sheets. 
If no sheet is selected the SheetSelection-Form will pop up. 
\n\nShift+Click:\n 
Pick source views from list instead of selection or active view.''' 

#logger = script.get_logger()

selected_views = []

if __shiftclick__:    #noqa
    selected_views = forms.select_views()
else:
    # get selection and verify a view is selected
    #selection = revit.get_selection()
    selection = [doc.GetElement(elId) for elId in uidoc.Selection.GetElementIds() ]

    dest_sheets = [selection.pop(i)  for i,j in enumerate(selection) 
                    if j.Category.Name.Equals("Sheets")]
    if selection: 
        for el in selection: 
            if el.Category.Name.Equals("Views"):
                target_view = revit.query.get_view_by_name(el.Name)
                if target_view: 
                    selected_views.append(target_view)
    else:
        # selected_views = revit.activeview
        # if not isinstance(selected_views, DB.View):
        forms.alert('Active view must be placable on a sheet.', exit=True)

if selected_views:
    if not dest_sheets:
        # get the destination sheets from user via forms Selection Dialog
        dest_sheets = forms.select_sheets()
    if dest_sheets:
        with revit.Transaction("Add Views to Sheets"):
            for i in selected_views:
                for sheet in dest_sheets:
                    try:
                        DB.Viewport.Create(revit.doc, sheet.Id, i.Id, DB.XYZ(0, 0, 0))
                    except Exception as place_err:
                        print traceback.format_exc()
else:
    forms.alert('No views selected.')



