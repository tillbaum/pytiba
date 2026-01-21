'''
Missing SaveAs Button :-),
KeyboardShortcut can be set via 
Revit ks-Dialog
'''
__title__ = "SaveAs\nwithoutprompt"
__author__ = "Tillmann Baumeister"

import sys
from Autodesk.Revit import UI, DB

uiapp = __revit__
uidoc = __revit__.ActiveUIDocument

doc = __revit__.ActiveUIDocument.Document # doc = DocumentManager.Instance.CurrentDBDocument 

# def filesavedlg():
    # savedlg = UI.FileSaveDialog("All Revit files (*.rvt, *.rfa, *.rte, *.rft)|*.rvt;*.rfa;*.rte;*.rft")
    # savedlg.Title = "SaveAs.... "
    # savedlg.InitialFileName = doc.PathName
    # savedlg.Filter = "All Revit files (*.rvt, *.rfa, *.rte, *.rft)|*.rvt;*.rfa;*.rte;*.rft" 
    # test = savedlg.Show()
    # modelpath = savedlg.GetSelectedModelPath()
    # return modelpath
    # modelpath is None if SaveFileDialog is canceled. 
#modelpath = filesavedlg()

options = UI.UISaveAsOptions()
options.ShowOverwriteWarning = True 

uisaveas = UI.UIDocument.SaveAs(uidoc, options)

# if modelpath: 
    # saveasopt = DB.SaveAsOptions() 
    # saveasopt.MaximumBackups = 6  # must be at least 1 or more 
    # saveasopt.OverwriteExistingFile = True 
    # saveasopt.PreviewViewId = doc.ActiveView.Id 
    # saveas = doc.SaveAs(modelpath, saveasopt) 
# else: 
    # sys.exit()

