# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""


The `trackers` package contain different trackers for tracking various things.
(Currently I only have a `tubetracker`, for tracking tubes in freezer boxes.)

The job of a tracker is to:

* Use a scanner from the `scanners` package to scan objects (e.g. tube barcodes in a box) to extract barcode values.
* Use a client from the `client` package to retrieve data (e.g. box-tube location data).
* Compare the scanned barcodes against existing data box-tubes sets in the database and
    identify which box was just scanned, if possible.
* Identify missing tubes (where the location is now unknown).
* Use the `server` package to update the box-tube location data.



"""




