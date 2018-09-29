# pytiba
pytiba is an extension for [pyRevit](http://eirannejad.github.io/pyRevit/)

![pyTiBa](https://github.com/tillbaum/pytiba/blob/master/pytiba%20documentation/pdf_export/pyTiBa%20Tab.png)


## Features
### Hide/Unhide HelpConstruction objects:
Hides/ unhides Help Construction Objects (Hilfskonstruktionen) i.e: Detail- and Modellines, TextNotes, Dimensions. 
This tool imitates a very useful function available in the Nemetschek Allplan Cad System. 
All Detail- and Modellines, Textnotes and Dimension types which contain the letters "HK" 
in their typename can be hiden and unhiden. 
Useful if you need to draw lines/textnotes/dimensions that should not appear on your sheets you want to print. 
(https://youtu.be/YDGFrxg2Rfw)

### pdf_export tool 
The pdf_export tool exports: 
 +   multiple Revit Sheets to pdf at the same time,  
 +   with filenames specified by sheet  parameters for each sheet, i.e. 
    „SheetNumber_Revision_SheetName_date_time“  
    (ex: “A01_b_Floorplan L00_17.06.18_11:34.pdf“ ).
 +   with papersize format automatically matching the sheetsize format
 +   Sheetview selection is made either by selecting Sheets in Project Browser 
 before the script is run or by Sheet-Selection-Dialog. (https://youtu.be/TtYq2vylD-M)

### dwg/dxf_export tool:
Exports multiple Revit Sheets to dwg or dxf format with user specified filename.
The filename can consist of any parameter found in the properties of the SheetView. Current date and/or time letters are also supported. 
### Sheets from Excel:
Lets you easily create RevitSheetViews from an Excel worksheet table 
Parameters SheetNr, SheetName, IssueDate, Author, manual_Scale are set on the SheetView.
If Sheet already exist in Project, only the parameters get updated.
### Levels from Excel:
Creates Levels from an Excel worksheet table.
(https://youtu.be/rT_3vCVz4dU)
### Section Tools
 - Create Section parallel to lines (Model- or Detaillines), 
   (Select Detail/Modellines, run tool) 
 - Arrange Viewports on SheetView, (Select Viewports on Sheet you want to arrange, run tool)
 - create section orthogonal to line (with GUI) (not yet implemented)
This toolset lets you create Sections parallel to a line and orthogonal to a line.
When more than one line is selected you can create a developed view of walls.
Lets you automatically place the views in the right order on a sheet view 
(there is also a tool on the pyrevit tab for that purpose).
### Schedule csv-Export
Exports selected Schedules to csv-files with on click and also creates a Excel file.
(Under developement)
### Family Folder, Project Folder
Just a link to your important Revit Content Folders. 
Open a folder in Windows Explorer. 
Pressing Shift + Click lets you choose the Folder in your File System. 
### SaveAs
Adds the missing SaveAs Button. Can be added to the Quick Launch Toolbar. 
### Update Fam/Prj
Update all project files or family files in a folder to the current running revit version.
(credits: www.sixtysecondrevit.com by J.Pierson)



-----------------------------------------------------------------------------------------------------
### PDF_export tool: Setup 
*** work in progress ***

#### Sheet Selection Dialog 


<table>
<tr>
<td>
<img src="https://github.com/tillbaum/pytiba/blob/master/pytiba%20documentation/pdf_export/SheetSelectionDialog.png" alt="alt text" width="390" height="390">
</td>
<td>
<img src="https://github.com/tillbaum/pytiba/blob/master/pytiba%20documentation/pdf_export/SheetSelecDia_options.png" alt="alt text" width="390" height="390">
</td>
</tr>
</table>

#### Recommended pdfprinter
The pdfprinter must be configured. 

**Automatic Filenaming** works best with free **PDFCreator printer** (pdfforge.org). **Filenaming** and the correct **filepath output** can be specified. 

Other printers that have been tested to work: 
Adobe PDF, bullzip PDF Printer. (Filepath output can not be set in the dialog, directory has to be set in the printer options)

<img src="https://github.com/tillbaum/pytiba/blob/master/pytiba%20documentation/pdf_export/PDFCreator%20ProfileSettings.png" alt="alt text" width="720" height="480">

(PDFCreator Version 3.2.1, there is a newer version available)
It also works with older version, see http://wrw.is/using-free-pdf-printer-rtv-xporter-pro-automatic-batch-pdf-naming-revit/

Adobe PDF printer:

<img src="https://github.com/tillbaum/pytiba/blob/master/pytiba%20documentation/pdf_export/AdobePDF%20printer_filename_working_Creation_dlg.png" alt="alt text" > <!--- width="720" height="480" -->

#### Papersize-format matching Sheetsize-format
To get this function to work properly you have to add Print Forms with the right papersizeformat, to your 
Print Management on Windows. 

<img src="https://github.com/tillbaum/pytiba/blob/master/pytiba%20documentation/pdf_export/PrintManagementForms.png" alt="alt text" width="663" height="210">
Windows Print Management Dialog


<img src="https://github.com/tillbaum/pytiba/blob/master/pytiba%20documentation/pdf_export/Add%20Print%20Forms.png" alt="alt text" width="328" height="374" > 
Print Form Dialog


If you add forms they will be available globaly to most installed pdf printers.
(You can open this dialog by typing "Print Management" in your SearchBox in the WIN10 taskbar, 
from old Win7Style Conrol Panel its ControlPanel>AdministrativeTools>PrintManagement)

The new forms must be named **"width[cm]xheight[cm]"**, "118.9x84.1" (A0 format), "42.0x29.7" (A3 format). only one position after the decimal point is allowed. Or "90x65", "125x85", without any decimal point, in a raster of 5.

**(work in progress)**

#### FAQ / Errors 
+ PDFCreator switches Page Orientation/ Automatic page orientation doesn't seem to work. --> In PDFCreator Print Profile set Page Orientation manually from  Automatic to Landscape. 
In Revit "!temp" PrintSetting set Page Orientation to Portrait, its the default setting to assure matchPaperSizeFunc finds the right Print Form. 

**(work in progress)**


# Credits
Credits go to the following: 
+ Ehsan Iran-Najad for providing [PyRevit](https://github.com/eirannejad/pyRevit), the amazing IronPython Script Library / Environment for Revit.
+ Gui Talariko, creator of [RevitPythonWrapper](https://revitpythonwrapper.readthedocs.io/en/latest/)
+ Daren Thomas, creator of [RevitPythonShell](https://github.com/architecture-building-systems/revitpythonshell)
+ Jeremy Tammik, creator of [RevitLookup](https://github.com/jeremytammik/RevitLookup)
+ Icon8 for nice Icons

# License
This package is licensed under GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.




