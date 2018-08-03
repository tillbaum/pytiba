# pytiba
pytiba is an extension for [pyRevit](http://eirannejad.github.io/pyRevit/)

![pyTiBa](https://github.com/tillbaum/pytiba/blob/master/pytiba%20documentation/pdf_export/pyTiBa%20Tab.png)

## Features
### pdf_export tool
The pdf_export tool exports: 
 +   multiple Revit Sheets to pdf at the same time,  
 +   with filenames specified by sheet  parameters for each sheet, i.e. 
    „SheetNumber_Revision_SheetName_date_time“  
    (ex: “A01_b_Floorplan L00_17.06.18_11:34.pdf“ ).
 +   with papersize format automatically matching the sheetsize format
 +   Sheetview selection is made either by selecting Sheets in Project Browser before the script is run or by Sheet-Selection-Dialog. 
 
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

Other printers that have been tested towork: 
Adobe PDF, bullzip PDF Printer. (Filepath output can not be set in the dialog, directory has to be set in the printer options)

<img src="https://github.com/tillbaum/pytiba/blob/master/pytiba%20documentation/pdf_export/PDFCreator%20ProfileSettings.png" alt="alt text" width="720" height="480">

(PDFCreator Version 3.2.1, there is a newer version available)
It also works with older version, see http://wrw.is/using-free-pdf-printer-rtv-xporter-pro-automatic-batch-pdf-naming-revit/

Adobe PDF printer:

<img src="https://github.com/tillbaum/pytiba/blob/master/pytiba%20documentation/pdf_export/AdobePDF%20printer_filename_working_Creation_dlg.png" alt="alt text" > <!--- width="720" height="480" -->

#### Papersize-format matching Sheetformat Size
To get this function to work properly you have to add Print Forms with the right papersizeformat, to your 
Print Management on Windows. 

<img src="https://github.com/tillbaum/pytiba/blob/master/pytiba%20documentation/pdf_export/PrintManagementForms.png" alt="alt text" width="663" height="210">
Windows Print Management Dialog


<img src="https://github.com/tillbaum/pytiba/blob/master/pytiba%20documentation/pdf_export/Add%20Print%20Forms.png" alt="alt text" width="328" height="374" > 
Print Form Dialog


If you add forms they will be available globaly to most installed pdf printers.
(You can open this dialog by typing "Print Management" in your SearchBox in the WIN10 taskbar, 
from old Win7Style Conrol Panel its ControlPanel>AdministrativeTools>PrintManagement)

The new forms must be named **"width[cm]xheight[cm]"**, ex: "90x65"[cm], A0 format: "118.9x84.1", A3 format "42.0x29.7". (only one position after the decimal point is allowed).
The print forms are saved in the registry "\HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Print\Forms". 
The key can be exported and imported on other system, so you have to create (many) print forms only once.

The pdf_export tool has a function matchPaperSize().
It looks up the **BuiltInParameters Sheet Width an Sheedt Heigth** (which you can find in the Properties panel when a Title Block is selected) builds a **string** out of it **("110x65")** and looks for a **matching name** in the **Print Forms**.

If it can't find one, it rounds up by 0.5 (118.9 --> 119.0, 84.1 --> 85.0) and looks again.
If it still can't find one it rounds up to the last cm digit by a fraction of 5,
(119 --> 120, 42 --> 45, no decimal point).

After rounding up, it adds +5 either to the width or the height, until the created string "widthxheight" matches a print form name. 

CAD sheets get printed out on large format plotters with papersize rolls of width 914mm (36") or lager.
There is no need to use standard DIN formats. I.e.: with 914mm beeing the max. width, subtracting 5mm on each side for paper transport in the plotter, a max. paper width of ca. 900mm is available for printing. (90x55, 120x90, 120x85)
If one uses a parametric variable Titleblock one can easily create plans in the 5cm raster. 

**(work in progress)**

<table>
<tr>
<td>
<img src="https://github.com/tillbaum/pytiba/blob/master/pytiba%20documentation/pdf_export/PrintManagementForms.png" alt="alt text" >
</td>
<td>
<img src="" alt="alt text" width="390" height="390">
</td>
</tr>
</table>

**(work in progress)**

# Credits
Credits and a thank you go to the following: 
+ Ehsan Iran-Najad for providing [PyRevit](https://github.com/eirannejad/pyRevit), the amazing IronPython Script Library / Environment for Revit.
+ Gui Talariko, creator of [RevitPythonWrapper](https://revitpythonwrapper.readthedocs.io/en/latest/)
+ Daren Thomas, creator of [RevitPythonShell](https://github.com/architecture-building-systems/revitpythonshell)
+ Jeremy Tammik, creator of [RevitLookup](https://github.com/jeremytammik/RevitLookup)
+ Icon8 for nice Icons

# License
This package is licensed under GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.




