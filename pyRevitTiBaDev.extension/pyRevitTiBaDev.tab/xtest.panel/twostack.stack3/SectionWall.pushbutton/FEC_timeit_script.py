
from Autodesk.Revit.DB import *
import clr
import System
from System.Collections.Generic import List 

clr.AddReference('System.Linq')
# Import previously referenced C# libraries like first-class Python modules
import System.Linq
clr.ImportExtensions(System.Linq)  # Import LINQ extension methods (to enable "fluent syntax")


def test2():
    '''FEC test '''
    # ---FEC lines ---------------------- create Instance of FEC, Collect all OST_Lines 
    # BUILDING_CURVE_GSTYLE, BUILDING_CURVE_GSTYLE_PLUS_INVISIBLE
    paraValProvider = ParameterValueProvider(ElementId(BuiltInParameter.BUILDING_CURVE_GSTYLE_PLUS_INVISIBLE))
    rule = FilterStringRule(paraValProvider, FilterStringContains(), "HK", True); # True -> CaseSensitivity
    elemParaFilter = ElementParameterFilter(rule)

    hklines = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Lines) \
                    .WhereElementIsNotElementType().WherePasses(elemParaFilter)

    # --- FEC Dimension ------------witch contains "HK" string  -----------------------------------
    #ELEM_TYPE_PARAM
    paraValProvider = ParameterValueProvider(ElementId(BuiltInParameter.ELEM_TYPE_PARAM))
    rule = FilterStringRule(paraValProvider, FilterStringContains(), "HK", True); # True -> CaseSensitivity
    elemParaFilter = ElementParameterFilter(rule)

    hkdim = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Dimensions) \
                    .WhereElementIsNotElementType().WherePasses(elemParaFilter)

    # --- FEC for Text -----------------------------------------
    #ELEM_TYPE_PARAM
    paraValProvider = ParameterValueProvider(ElementId(BuiltInParameter.ELEM_TYPE_PARAM))
    rule = FilterStringRule(paraValProvider, FilterStringContains(), "HK", True); # True -> CaseSensitivity
    elemParaFilter = ElementParameterFilter(rule)

    hktxt = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TextNotes) \
                    .WhereElementIsNotElementType().WherePasses(elemParaFilter)

    return hktxt.UnionWith(hkdim).UnionWith(hklines)


def test1():
    # --- FEC for LINES -------- create Instance of FEC, Collect all OST_Lines 
    alllines = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Lines)
    hklines = [x for x in alllines if x.LineStyle.Name.Contains("HK")] #.Name == "HK" 

    # --- FEC for Text -----------------------------------------
    txtcol = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TextNotes)
    hktxt = [x for x in txtcol if x.Name.Contains("HK")]

    # --- FEC Dimension --------witch contains "HK" string  -----------------------------------
    dimcol = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Dimensions)
    hkdim = [x for x in dimcol if x.Name.Contains("HK")]

    # put all objects in one list:  hklines + hkdim + hktxt
    hktxt += hklines + hkdim
    return hktxt

def test():
    """Stupid test function"""
    L = []
    for i in range(100):
        L.append(i)

#if __name__ == '__main__':

hktxt2 = test2()
hktxt1 = test1()

t1 ='''\
t = Transaction(doc, "Hide, Unhide Elements")
try:
    t.Start()
    [HideUnhideEl(i, hktxt2) for i in viewlist]
    #ProcessListArg(HideUnhideEl, viewlist, hktxt2)
    t.Commit() 
except:
    t.RollBack()
    import traceback
    print traceback.format_exc()
'''

t2 ='''\
t = Transaction(doc, "Hide, Unhide Elements")
try:
    t.Start()
    #[HideUnhideEl(i, hktxt2) for i in viewlist]
    ProcessListArg(HideUnhideEl, viewlist, hktxt2)
    t.Commit() 
except:
    t.RollBack()
    import traceback
    print traceback.format_exc()
'''

def ProcessListArg(_func, _list, _arg): #_func: underscore has no special meaning in args of func 
    return map(lambda x: ProcessListArg(_func, x, _arg) if isinstance(x, list) else _func(x, _arg), _list )

# type(x) == list  <==># isinstance(x, list)

# Func HideUnhide Elements 
def HideUnhideEl(view, elements):
    ids = List[ElementId]()  # .NET List 
    ids2 =List[ElementId]()  # .NET List  
    for i in elements: 
        if not i.IsHidden(view) and i.CanBeHidden(view): 
            ids.Add(i.Id) 
        elif i.IsHidden(view): 
            ids2.Add(i.Id)
    if not elements[0].IsHidden(view): 
        view.HideElements(ids) 
    else:
        view.UnhideElements(ids2) 
#   return None


vt= ViewType
arraylist = {vt.FloorPlan, vt.CeilingPlan, vt.Elevation, vt.ThreeD, vt.DrawingSheet, vt.DraftingView,
                vt.Legend, vt.EngineeringPlan, vt.AreaPlan, vt.Section, vt.Detail}
#----- FilteredElementCollector of Views , Create Instance of FEC, ----------------------------
FECviews = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views) \
                .WhereElementIsNotElementType() \
                .Where(lambda x: not x.IsTemplate and x.ViewType in arraylist)
viewlist= list(FECviews)



#array = ViewType.GetValues(ViewType) # Gets all objects in Enumeration, that you can iterate over it! 
# FECviews = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views) \
                # .WhereElementIsNotElementType()
# vt= ViewType
# arraylist = {vt.FloorPlan, vt.CeilingPlan, vt.Elevation, vt.ThreeD, vt.DrawingSheet, vt.DraftingView,
                # vt.Legend, vt.EngineeringPlan, vt.AreaPlan, vt.Section, vt.Detail}
# viewlist =[i for i in FECviews if not i.IsTemplate and i.ViewType in arraylist]


import timeit

# print timeit.timeit( stmt = s1 , setup="from __main__ import *", number = 100)




# print "test1  Fec + ListComp ------------------------------------"
# print timeit.timeit( "test1()", setup="from __main__ import *", number = 1000)

# print "test2 only FEC -------------------------"
# print timeit.timeit( "test2()", setup="from __main__ import *", number = 1000)

# Added WhereElementIsNotElementType(), UnionWith(other FEC)
# test1  Fec + ListComp ------------------------------------
# 19.9844894409
# test2 only FEC -------------------------
# 0.328125


# test1  Fec + ListComp ------------------------------------
# 20.8751144409
# test2 only FEC -------------------------
# 16.6563339233

# test1  Fec + ListComp ------------------------------------
# 19.5313491821
# test2 only FEC -------------------------
# 17.7969665527
 

print timeit.timeit(stmt=t1, setup="from __main__ import *", number=10)

print timeit.timeit(stmt=t2, setup="from __main__ import *", number=10)

# Result : t1, t2
# 298.767173767
# 303.423446655
