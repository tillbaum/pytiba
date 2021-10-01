"""
Uncheck ALL Properties/Parameter
in all ViewTemplates
"""

from pyrevit import revit, DB
from pyrevit import forms
from pyrevit import script
import traceback 

doc = __revit__.ActiveUIDocument.Document # doc = DocumentManager.Instance.CurrentDBDocument 

__author__ = 'Tillmann Baumeister'


FECviews = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Views) \
                             .WhereElementIsNotElementType() \
                             .ToElements() 

templateviews = [ i for i in FECviews if i.IsTemplate]
print len(templateviews)



filterparId = DB.ElementId(DB.BuiltInParameter.VIS_GRAPHICS_FILTERS)
print filterparId, "---------"
print type(filterparId) # ElementId


t= DB.Transaction(doc, "Mark Filter in All ViewTemplates")
t.Start()

for view in templateviews: 
    print view.Name
    noncontroledparaList= view.GetNonControlledTemplateParameterIds()
    for para in view.ParametersMap:
        try:
            noncontroledparaList.Remove(filterparId) 
            view.SetNonControlledTemplateParameterIds(noncontroledparaList) 
        except: 
            print traceback.format_exc()
t.Commit()


# v0 = templateviews[0]
# noncontroledparaList = v0.GetNonControlledTemplateParameterIds()

# ---BuiltInParameter. --------
# VIEW_SCALE,  
# VIEW_SCALE_PULLDOWN_IMPERIAL ,
# VIEW_MODEL_DISPLAY_MODE 
# VIEW_DETAIL_LEVEL
# VIEW_PARTS_VISIBILITY

# VIS_GRAPHICS_MODEL   
# VIS_GRAPHICS_ANNOTATION 
# VIS_GRAPHICS_ANALYTICAL_MODEL 
# VIS_GRAPHICS_DESIGNOPTIONS 
# VIS_GRAPHICS_IMPORT  
# VIS_GRAPHICS_FILTERS 

# GRAPHIC_DISPLAY_OPTIONS_MODEL
# GRAPHIC_DISPLAY_OPTIONS_SHADOWS 
# GRAPHIC_DISPLAY_OPTIONS_SKETCHYLINES
# GRAPHIC_DISPLAY_OPTIONS_LIGHTING 	
# GRAPHIC_DISPLAY_OPTIONS_PHOTO_EXPOSURE

# PLAN_VIEW_RANGE
# VIEW_UNDERLAY_ORIENTATION 
# VIEW_PHASE_FILTER
# VIEW_DISCIPLINE 
# VIEW_SHOW_HIDDEN_LINES
# COLOR_SCHEME_LOCATION #Color Scheme Location Background
# VIEW_SCHEMA_SETTING_FOR_BUILDING  "ColorScheme"


# VIS_GRAPHICS_RVT_LINKS 
# VIEW_GRAPH_SUN_PATH 





# GRAPHIC_DISPLAY_OPTIONS_FOG  
# GRAPHIC_DISPLAY_OPTIONS_BACKGROUND 

# GRAPHIC_DISPLAY_OPTIONS_SS_INTENSITY


