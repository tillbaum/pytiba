'''
Missing SaveAs Button :-),
KeyboardShortcut can be set via 
Revit ks-Dialog
'''
__title__ = "SaveAs\n6"
__author__ = "Tillmann Baumeister"

import sys
from Autodesk.Revit import UI, DB

uidoc = __revit__
doc = __revit__.ActiveUIDocument.Document # doc = DocumentManager.Instance.CurrentDBDocument 
def filesavedlg():
	savedlg = UI.FileSaveDialog("All Revit files (*.rvt, *.rfa, *.rte, *.rft)|*.rvt;*.rfa;*.rte;*.rft")
	savedlg.Title = "SaveAs.... "
	savedlg.InitialFileName = doc.PathName
	#savedlg.Filter = "All Revit files (*.rvt, *.rfa, *.rte, *.rft)|*.rvt;*.rfa;*.rte;*.rft" 
	test = savedlg.Show()
	modelpath = savedlg.GetSelectedModelPath()
	return modelpath
	# modelpath is None if SaveFileDialog is canceled. 
modelpath = filesavedlg()

if modelpath: 
	saveasopt = DB.SaveAsOptions()
	saveasopt.MaximumBackups = 1 # must be at least 1 or more 
	saveasopt.OverwriteExistingFile = True
	saveasopt.PreviewViewId = doc.ActiveView.Id
	saveas = doc.SaveAs(modelpath, saveasopt)
else: 
	sys.exit()
