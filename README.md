# Zepto-LIMS-Inventory-tube-tracker

Zepto-LIMS: Laboratory inventory tracker for tubes and freezer boxes using 2D barcodes (QR codes, datamatrix, etc).



## Usage and examples:


Zepto-LIMS inventory tracker is primarily designed for one purpose: 
Tracking tubes in freezer boxes.

Whenever you place a box with tubes back in the freezer,
you take a picture of tubes sitting in the box with the lid barcodes visible.

Zepto-LIMS scans the image and recognizes the tubes by their barcodes.

If most of the tubes belong to a known freezer box already in the Zepto-LIMS database,
the box is simply updated to reflect any new or missing tubes compared to 
the last time the box was scanned.

If the software does not recognize the box based on the tubes within, 
you have the option to either create a new freezer box, 
or select to manually update an existing freezer box.

You can also add information about each freezer box, specifying which freezer
and what shelf in the freezer the box is located in. This can, of course, be
updated whenever you scan the box when you are putting the box back in the freezer.

When you need to find a specific tube, you can simply use the "search" feature
to locate which freezer box the tube is placed in (which will also tell you which 
freezer and shelf the box is placed on, if you've added that info about the box).














## Appendix: How to generate tube labels with 2D barcodes

The solution I personally use is to print labels using Sublime Text 
with the ZPL-Label-Print plugin/package.
This allows you to print labels using a zpl label template containing 
values from the currently opened file (or a selection of the current file)
or values from the clipboard (e.g. clipboard values copied from Excel).

Using this, I can in just a few seconds start a print job for all the tubes 
that I need labels for.

The "ZPL label template" that I use is created using the free (no cost) 
ZebraDesigner software. But there are many other applications that can be
used to create ZPL labels.


In all cases, the most efficient way to print your tube labels is to:

* FIRST you need to CREATE a general label *template*, which defines where to print 
	and barcode(s) and the different text fields (e.g. date, sample ID, 
	sample description).
	I personally have a datamatrix barcode on the lid, and the date, 
	sample ID, and sample description on the side of the tube.

* THEN you use some system to actually print labels, where your actual data values
	are inserted into the template and printed on your label printer.
	This could be the free [ZPL-Label-Print](https://github.com/scholer/sublime-zpl-label-print)
	package for Sublime Text, or it could be some other label printing system.




Here is a brief list of applications and methods to generate and print labels:

* Zebra has some commercial software (ZebraDesigner Pro, ZebraDesigner for XML)
	that allows you to connect to a database with sample data (e.g. sample ID)
	and use this to print multiple labels using a predefined template.
	* OBS: Zebra also has free (no-cost) application (ZebraDesigner Free), but you can 
	only use this to generate and print one label at a time, and you have to manually
	update the label file for every distinct tube you want to print. This is obviously
	*not* a scalable solution for most laboratories, but the free ZebraDesigner 
	application *can* be used to create the initial template.

* The [QZ-Tray](https://qz.io/) and accompanying utilities allows you to generate and print 
	labels from a web browser. 
	QZ-Tray open source, sporting a fairly simple-to-use API and easy printer setup,
	and it supports most of the popular thermal transfer label printers.

* Brother has a pretty decent "P-Touch Editor" label software, which you can use both
 	for creating your label template, and print labels using data values from a database.

* Dymo's Label Software itself is not really suitable for printing multiple labels
	on an ad-hoc basis. The Dymo DLS software *does* provide an option to connect 
	the software to a database, but it is not very convenient to update the database
	and then print a label, the way a researcher would often like to.
	(The Dymo Label Software seems to mostly target the use-case where you need to print
	a bunch of address labels using a database with contact information.)
	However, Dymo *does* provide a JavaScript SDK with a web service API 
	that can be used to create your own application for printing multiple 
	labels using a label template.

* Additionally, a quick Google search will reveal a bunch of commercial software that
	can be used to print labels, either from a database or from e.g. Office documents.
	Many of these are focused on printing shipping labels.
	For example:
	* [dlSoft Labelling software](https://www.dlsoft.com/label_software.htm)
	* NiceLabel
	* Maestro Label Designer
	* BarTender - for printing barcodes.
	* Endicia
	* Loftware Enterprise Label solutions
	* Esko Software Platform
	* MarkMagick
	* Aulux Barcode Label Maker
	* CQL Pro
	* LabelJoy
	* cristallight Labels And Databases.


