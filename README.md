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

#### Papersize-format matching Sheetformat Size
To get this function to work you have to add Print Forms with the papersizeformat you want to print to your 
Print Management on Windows. 
(From the Windows Conrol Panel its ControlPanel>AdministrativeTools>PrintManagement)

<img src="https://github.com/tillbaum/pytiba/blob/master/pytiba%20documentation/pdf_export/PrintManagementForms.png" alt="alt text" >

<img src="https://github.com/tillbaum/pytiba/blob/master/pytiba%20documentation/pdf_export/Add%20Print%20Forms.png" alt="alt text" >

If you add forms they will be available globaly to most installed pdf printers.
You can open this dialog by typing "Print Management" in your SearchBox in the WIN10 taskbar.
The new forms must be named "widthxheight" i.e. "90x65", "85x
Those print forms are saved in the registry "\HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Print\Forms". 
This key can be exported and imported on other system, so you have to create print forms only once.

Now in the pdf_export tool has a function which collects all the 

Now most AEC firms print on large plotters with 






In the Print Management dialog you can Add Forms by 
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

(work in progress)



# Credits
Credits and a thank you go to the following: 
+ Ehsan Iran-Najad for providing [PyRevit](https://github.com/eirannejad/pyRevit), the IronPython Script Library / Environment for Revit.
+ Gui Talariko, creator of [RevitPythonWrapper](https://revitpythonwrapper.readthedocs.io/en/latest/)
+ Daren Thomas, creator of [RevitPythonShell](https://github.com/architecture-building-systems/revitpythonshell)
+ Jeremy Tammik, creator of [RevitLookup](https://github.com/jeremytammik/RevitLookup)
+ Icon8 for nice Icons

# License
This package is licensed under GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.




