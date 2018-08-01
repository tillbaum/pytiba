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
**Automatic Filenaming** works best with free **PDFCreator printer** (pdfforge.org). **Filenaming** and the correct **filepath** output can be specified. 
Other printers that have been tested to work: 

Adobe PDF, bullzip PDF Printer. (Filepath output directory has to be set in the printer options)

<img src="https://github.com/tillbaum/pytiba/blob/master/pytiba%20documentation/pdf_export/PDFCreator%20ProfileSettings.png" alt="alt text" width="720" height="480">


(PDFCreator Version 3.2.1, there is a newer version available)
It also works with older version, see http://wrw.is/using-free-pdf-printer-rtv-xporter-pro-automatic-batch-pdf-naming-revit/

Adobe PDF printer:

<img src="https://github.com/tillbaum/pytiba/blob/master/pytiba%20documentation/pdf_export/AdobePDF%20printer_filename_working_Creation_dlg.png" alt="alt text" > <!--- width="720" height="480" -->

(work in progress)

# Credits
Credits and a thank you go to the following: 
+ Ehsan Iran-Najad for providing PyRevit, the IronPython Script Library / Environment for Revit. [Ehsan Iran-Nejad](https://github.com/eirannejad/pyRevit)
+ Gui Talariko, creator of [RevitPythonWrapper](https://revitpythonwrapper.readthedocs.io/en/latest/)
+ Daren Thomas, creator of [RevitPythonShell](https://github.com/architecture-building-systems/revitpythonshell)
+ Jeremy Tammik, creator of [RevitLookup](https://github.com/jeremytammik/RevitLookup)
+ Icon8 for nice Icons

# License
This package is licensed under GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.




