
import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import *

clr.AddReference("System")
from System.Collections.Generic import List

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.GeometryConversion)
clr.ImportExtensions(Revit.Elements)

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

#Preparing input from dynamo to revit
rebarElements = UnwrapElement(IN[0])
views = UnwrapElement(IN[1])
solid=IN[2];

#Change rebar in transaction
TransactionManager.Instance.EnsureInTransaction(doc)
for view in views:
	for rebarElement in rebarElements:
		rebarElement.SetSolidInView(view,solid)
TransactionManager.Instance.TransactionTaskDone()

OUT = rebarElements

