# pytiba
pytiba is an extension for [pyRevit](http://eirannejad.github.io/pyRevit/)

![pyTiBa](https://github.com/tillbaum/pytiba/blob/master/pytiba%20documentation/pdf_export/pyTiBa%20Tab.png)


## Features
### Hide/Unhide HelpConstruction objects:
Hides/ unhides Help Construction Objects (Hilfskonstruktionen) i.e: Detail- and Modellines, TextNotes, Dimensions. 
All latter objects which contain the letter "HK" in their typename can be hidden and unhidden. 
Useful if you need to draw lines/textnotes/dimensions that should not appear on your sheets you want to print.  
__Video:__ (https://youtu.be/YDGFrxg2Rfw)

### pdf_export tool 
The pdf_export tool exports: 
+   multiple Revit Sheets to pdf at the same time,  
+   with filenames specified by sheet parameters for each sheet, i.e. 
    „SheetNumber_Revision_SheetName_date_time“  
    (ex: “A01_b_Floorplan L00_17.06.18_11:34.pdf“ ).
+   with papersize format automatically matching the sheetsize format
+   Sheetview selection is made either by selecting Sheets in Project Browser
    before the script is run or by Sheet-Selection-Dialog.  
[pdf_export_documentation](pdf_export_doc.md)
(work in progress) 
    
 __Video:__ (https://youtu.be/TtYq2vylD-M)

### dwg/dxf_export tool:
Exports multiple Revit Sheets to dwg or dxf format with user specified filename.
The filename can consist of any parameter found in the properties of the SheetView. 
Current date and/or time letters are also supported. 

### Sheets from Excel:
Lets you easily create RevitSheetViews from an Excel worksheet table. 
Parameters SheetNr, SheetName, IssueDate, Author, manual_Scale are set on the SheetView.
If Sheet already exist in Project, only parameters are updated. 

### Levels from Excel:
Creates Levels from an Excel worksheet table.  
__Video:__ (https://youtu.be/rT_3vCVz4dU)

### Section Tools (collection)
+ Create Sections and SectionViews along lines (Model- or Detaillines).  
Select Detail / Modellines, run tool. By selecting a connected line sequence, one can create a developed view of walls. 
+ Arrange Viewports on SheetView, (Select Viewports on Sheet you want to arrange, run tool)
This tool arranges the Viewports in order. Running the tool again reverses the order.   

__Video:__ Bridge_Sections: https://youtu.be/n2K7Ex94knA, Developed View of Walls: https://youtu.be/dLOM2APDQpQ)

### Schedule csv-Export
Exports selected Schedules to csv-files and combine them in one Excel file.  
__Video:__ (https://youtu.be/6-b6gVSqS5E)

### Family Folder, Project Folder
Just a link to your important Revit Content Folders. 
Open a folder in Windows Explorer. 
Pressing Shift + Click lets you choose the Folder in your File System. 
### SaveAs
Adds the missing SaveAs Button. Can be added to the Quick Launch Toolbar. 
### Update Fam/Prj
Update all project-files/family-files in a folder (including subfolders) to the current running revit version.  
(credits: www.sixtysecondrevit.com by J.Pierson)



-----------------------------------------------------------------------------------------------------


# Credits
Credits go to the following: 
+ Ehsan Iran-Nejad for providing [PyRevit](https://github.com/eirannejad/pyRevit), the amazing IronPython Script Library / Environment for Revit. 
+ Gui Talariko, creator of [RevitPythonWrapper](https://revitpythonwrapper.readthedocs.io/en/latest/)
+ Daren Thomas, creator of [RevitPythonShell](https://github.com/architecture-building-systems/revitpythonshell)
+ Jeremy Tammik, creator of [RevitLookup](https://github.com/jeremytammik/RevitLookup)
+ Icon8 for nice Icons

# License
This package is licensed under GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.




