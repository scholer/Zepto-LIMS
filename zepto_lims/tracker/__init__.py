"""

The job of the `tracker` package is to:

* Use the `scanner` package to scan tube barcodes in a box to extract barcode values.
* Use the `server` package to retrieve box-tube location data.
* Compare the scanned barcodes against existing box-tubes sets in the database and
    identify which box was just scanned, if possible.
* Identify missing tubes (where the location is now unknown).
* Use the `server` package to update the box-tube location data.



"""




