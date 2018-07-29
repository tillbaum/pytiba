# pytiba
pytiba is an extension for [pyRevit](http://eirannejad.github.io/pyRevit/)

![pyTiBa](https://github.com/tillbaum/pytiba/blob/master/pytiba%20documentation/pdf_export/pyTiBa%20Tab.png)

## Features
### pdf_export tool
The pdfOut_sheets tool exports: 
 +   multiple Revit Sheets to pdf at the same time,  
 +   with filenames specified by sheet  parameters for each sheet, i.e. 
    „SheetNumber_Revision_SheetName_date_time“  
    (ex: “A01_b_Floorplan L00_17.06.18_11:34.pdf“ ).
 +   with papersize format automatically matching the sheetsize format
 +   Sheetview selection is made either by selecting Sheets in Project Browser before the script is run or by Sheet-Selection-Dialog (Fig. 1). 

Automatic Filenaming only works with the free PDFCreator printer (pdfforge.org). It must be configured:

![test](https://github.com/tillbaum/pytiba/blob/master/pytiba%20documentation/pdf_export/PDFCreator%20ProfileSettings.png)

<img src="https://github.com/tillbaum/pytiba/blob/master/pytiba%20documentation/pdf_export/PDFCreator%20ProfileSettings.png" alt="alt text" width="840" height="550">


(PDFCreator Version 3.2.1, there is a newer version available)

It also works with older version, see http://wrw.is/using-free-pdf-printer-rtv-xporter-pro-automatic-batch-pdf-naming-revit/

Sheet Selection Dialog 
<!--
![SheetDialog1](https://github.com/tillbaum/pytiba/blob/master/pytiba%20documentation/pdf_export/SheetSelectionDialog.png) 
-->

<img src="https://github.com/tillbaum/pytiba/blob/master/pytiba%20documentation/pdf_export/SheetSelecDia_options.png" alt="alt text" width="200" height="300">

![dialog2](https://github.com/tillbaum/pytiba/blob/master/pytiba%20documentation/pdf_export/SheetSelecDia_options.png){:height="300px" width="350px"}

<img src="https://github.com/tillbaum/pytiba/blob/master/pytiba%20documentation/pdf_export/SheetSelecDia_options.png" alt="alt text" width="200" height="300">
