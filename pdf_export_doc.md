
To make the pdf_export tool work, you need to add Windows Print Froms of the Paper Sizes you want to print
to your Windows Print Management. 
Ever wanted to print a pdf to a certain format and added a "special" paper format in the print properties of your installed pdf printer. 
When you do this the paper format is also added to your Windows Print Forms. 

![](https://github.com/tillbaum/pytiba/blob/master/pytiba%20documentation/pdf_export/PrintManagementForms.png)

You need to add paper sizes of all the paper formats you usually need to your WindowsPrintForms. 
The WindowsPrintForms are stored in the Windows Registry. You can export a regkey and transfer it to other Windows System. 
In this Repo there is a regkey included which, if added to your registry, adds PrintForms in cm-Format to your Registry. 

PaperSizeFormats are [lengthxheight] 50cmx50cm up to 130cmx90cm, steps of 5cm. A height of 90cm is the limit because usual plotters use paperrolls with a max-height of 915mm. DinA1 - DinA3 Formats are included as well.

The pdf_export tool reads out the length- and height parameters of your TitleBlock, looks for a matching PaperSizeFormat in your WindowsPrintForms (cm Format). 
If it doesn't find the right one it adds 5cm, to the length,
looks again for a matching format, adds 5cm to the height, looks again and so on. This process is repeated 3 times. 
If it doesn't find a matching format it uses 90cmx90cm format.

pdf printer: 

I use PDFCreator. To make the automatic pdf naming work the pdf profile setting must look like this. 

![](https://github.com/tillbaum/pytiba/blob/master/pytiba%20documentation/pdf_export/PDFCreator%20ProfileSettings.png)

The pdf name input one provides in the pdf-print Dialog is a comma separated Revit-parameter list. 
Every Parameter is looked up, extracted and added to a string which is the name of the pdf. 
