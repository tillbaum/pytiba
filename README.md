# pytiba
pytiba is an extension for [pyRevit](http://eirannejad.github.io/pyRevit/)

![](https://github.com/tillbaum/pytiba/blob/master/pytiba%20documentation/pytiba.png)

## Features
### Hide/Unhide HelpConstruction objects:
Hides/ unhides Help Construction Objects (Hilfskonstruktionen) i.e: Detail- and Modellines, TextNotes, Dimensions. 
All latter objects which contain the letter "HK" in their typename can be hidden and unhidden. 
Useful if you need to draw lines/textnotes/dimensions that should not appear on your sheets you want to print.\
__Video:__ https://youtu.be/5SQk24mHIhE

### pdf_export tool (One-Click-PDF-Export-Solution)
The pdf_export tool exports: 
+   multiple Revit Sheets to pdf at the same time, 
+   with filenames specified by sheet parameters for each sheet, i.e. 
    „Sheet Number_Current Revision_Sheet Name_date_time“ \
    (ex: “A01_b_Floorplan L00_17.06.18_11:34.pdf“ ). 
+   with papersize format automatically matching the sheetsize format 
+   Sheetview selection is made either by selecting Sheets in Project Browser 
    before the script is run or by Sheet-Selection-Dialog. \
[pdf_export_documentation](pdf_export_doc.md) (work in progress)   
    
 __Video:__ https://youtu.be/uPb8Xyhw6hk 

### dwg/dxf_export tool:
Exports multiple Revit Sheets to dwg or dxf format with user specified filename.
The filename can consist of any parameter found in the properties of the SheetView. 
Current date and/or time letters are also supported. 

### Palettes (2D objects):
All 2D objects (currently TextNotes, Detail-Lines, Generic Annotations, Detail Items)\
on a modeless Palette:\
__Video:__ https://youtu.be/vMcQCD8qNIM 

### ViewFilterPalette:
Easily manage your ViewFilters from a Modeless Palette.\
__Video:__ https://youtu.be/HfmFzPlSlkI 

### Levels from Excel:
Creates Levels from an Excel worksheet table.  \
__Video:__ (https://www.youtube.com/watch?v=YW9SxNtxfvE)

### Section Tools (collection)
+ Create Sections and SectionViews along lines (Model- or Detail-lines).  
Select Detail / Modellines, run tool. \
By selecting a connected line sequence, one can create a developed view of walls. 
+ Arrange Viewports on SheetView, (Select Viewports on Sheet you want to arrange, run tool).
This tool arranges the Viewports in order. Running the tool again reverses the order.   \

__Video:__ Bridge_Sections: https://youtu.be/n2K7Ex94knA, Developed View of Walls: https://youtu.be/dLOM2APDQpQ)

### Schedule csv-Export
Exports selected Schedules to csv-files and import them in one Excel Workbook file.  \
__Video:__ (https://youtu.be/6-b6gVSqS5E)

### DublicateSheets
Dublicates a selected sheet (ProjectBrowser). Including multiple TitleBlocks and Legend Views. \
Select a Sheet in the ProjectBrowser and hit the Sheet-Dublicate-Button. \
__Video:__ (https://www.youtube.com/watch?v=sUjJq2U34tg)

### Delete SystemCategoryTypes
Easily delete NOT needed FamilyTypes of SystemCategories like "not needed" Texnotes, CAD-imported LineStyles, Filled Regions, GenericAnnotations
in your current Revit-Project and clean it up.\
__Video:__ (https://youtu.be/rk5dsa-9PH0)

### Copy Family-Types from other Projects to your current Project-Tool
Easily transfer/copy all needed FamilyTypes from other Projectfiles to your current Revit Projectfile.\
__Video:__ (https://www.youtube.com/watch?v=0MLAXWrOHQ8&t=2s)

### Transfer/Match Instance Parameter of same category-type
This tool works like the "match properties" tool you find in text processing programs. It works for instance parameters of the same Type.
Ex.: You want to change the level of a Wall it is attached to (Parameters: base- and top-constraint). 
Just choose a scource walltype and pick the destination walltype. Parameters are transferred from source to destination i.e the 
wall changes the level.\
__Video:__ (https://www.youtube.com/watch?v=NOQwtMtklbY)

### Transfer/Match selected Parameters
The same tool as above only that one can choose the parameters that are transferred in a selection dialog.

### Family Folder, Project Folder
Just a link to your important Revit Content Folders. 
Opens a folder in Windows Explorer. 
Pressing Shift + Click lets you choose the Folder in your File System. 

### SaveAs
Adds the missing SaveAs Button. Can be added to the Quick Launch Toolbar. 

### Update Fam/Prj
Update all project-files/family-files in a folder (including subfolders) to the current running revit version.  
(credits: www.sixtysecondrevit.com by J.Pierson)



-----------------------------------------------------------------------------------------------------
# Credits
+ Ehsan Iran-Nejad for providing [PyRevit](https://github.com/eirannejad/pyRevit), the amazing IronPython Script Library / Environment for Revit. 
+ Gui Talariko, creator of [RevitPythonWrapper](https://revitpythonwrapper.readthedocs.io/en/latest/)
+ Daren Thomas, creator of [RevitPythonShell](https://github.com/architecture-building-systems/revitpythonshell)
+ Jeremy Tammik, creator of [RevitLookup](https://github.com/jeremytammik/RevitLookup)
+ Icon8 for nice Icons

# License
This package is licensed under GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.




