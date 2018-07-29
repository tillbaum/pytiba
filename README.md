# pytiba
pytiba is an extension for [pyRevit](http://eirannejad.github.io/pyRevit/)

![pyTiBa](https://github.com/tillbaum/pytiba/blob/master/pytiba%20documentation/pyTiBa%20Tab.png)

## Features
### pdf_export
The pdfOut_sheets tool exports: 
+   multiple Revit Sheets to pdf at the same time,  
+   with filenames specified by sheet  parameters for each sheet, i.e. 
    „SheetNumber_Revision_SheetName_date_time“  
    (ex: “A01_b_Floorplan L00_17.06.18_11:34.pdf“ ).
+   with papersize format automatically matching the sheetsize format
+   Sheetview selection is made either by selecting Sheets in Project Browser before the script is run or by Sheet-Selection-Dialog (Fig. 1). 
Automatic Filenaming only works with the free PDFCreator printer (pdfforge.org). It must be configured
![test](https://github.com/tillbaum/pytiba/blob/master/pytiba%20documentation/PDFCreator%20ProfileSettings.png)


