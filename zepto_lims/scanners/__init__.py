# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""

The `scanner` package is responsible for scanning barcodes (from a camera picture)
and extracting barcode data.



Prior art - libraries and tools for scanning barcodes:
------------------------------------------------------


### Major barcode libraries:

Overview:

* ZBar (C)
* ZXing (Java) - "Zebra crossing".
* Android:
    * Google Vision API
* libdmtx - datamatrix barcode reader and generator library
    * http://libdmtx.sourceforge.net/



libdmtx:
* https://github.com/dmtx/libdmtx
* https://github.com/dmtx
* dmtx-utils provides `dmtxread` and `dmtxwrite` utilities:
    * https://github.com/dmtx/dmtx-utils
* Has official wrappers/bindings for most languages:
    * https://github.com/dmtx/dmtx-wrappers
    * https://github.com/dmtx/dmtx-wrappers/tree/master/python - "pydmtx".
*



### Python libraries and bindings:



#### Based on libdmtx:



Forks:

* There are plenty of forks, all named "pydmtx"
* https://github.com/Scurri/pydmtx
* https://pypi.org/project/pydmtx/ - no longer maintained, website offline.
* https://pypi.org/project/pylibdmtx
    * Fork by NaturalHistoryMuseum.
    * Actively maintained, latest release Feb 2019.
    * Initial commit from Nov 2016.

NaturalHistoryMuseum also has another barcode reader:
* https://github.com/NaturalHistoryMuseum/gouda
* Last update Dec 2016.
* Uses one of the following engines:
    * libdmtx
    * zbar
    * zxing
    * Commercial:
        * Accusoft
        * Data Symbol
        * Inlite
        * Stecos
        * Softek



pydatamatrix:
* Super fucking old and not available anymore.
* http://pydatamatrix.sourceforge.net/
    * > " I have used Python 1.4.5"
* https://sourceforge.net/projects/pydatamatrix/files/
    * LOL:
        > "Hi!
        > I'm sorry, but there were some severe bugs in the code - am working on it.
        > Do check back in a week or so, it should be up by then.
        > Sorry for the inconvenience.
        > Cheers!
        > mangobasket
* pydmtx



#### Based on ZBar:

pyzbar:
* https://github.com/NaturalHistoryMuseum/pyzbar
* "Read one-dimensional barcodes and QR codes from Python 2 and 3."
* What about datamatrix codes?


ZBar (The C++ library):
* http://zbar.sourceforge.net/
* https://cocoapods.org/pods/ZBarSDK
* Mostly for QR codes; datamatrix barcodes still not very well supported.
    * https://sourceforge.net/p/zbar/feature-requests/31/
* It seems the main library repository has python bindings?
*

zbarlight:
* https://github.com/Polyconseil/zbarlight/
* "A simple wrapper for zbar."
* Does not support Windows.
    * Edit, maybe it supports windows with some tricks:
        https://gist.github.com/Zephor5/aea563808d80f488310869b69661f330
* Uses PIL.

zbar-py:
* Bindings to ZBar. Last update 2016.
* https://pypi.org/project/zbar-py/
* https://github.com/zplab/zbar-py

zbar-ctypes
* https://github.com/brettatoms/zbar-ctypes
* last github update 2015
*

zbar:
* No updates since 2011, still on Python 2.

Blog posts using ZBar/pyzbar:
* https://www.learnopencv.com/barcode-and-qr-code-scanner-using-zbar-and-opencv/



#### Based on ZXing:


ZXing libraries::
* python-zxing (github) - last github update 2016.
* zxinglight (github) - last github update 2017.
* python-zxing-fast (github) - last github update 2018.



python-zxing:
* https://github.com/oostendo/python-zxing
* last github update 2016.


zxinglight
* https://github.com/lubo/zxinglight
* last github update 2017.


python-zxing-fast:
* https://github.com/daweim0/python-zxing-fast
* last github update 2018.





### Commercial barcode scanning libraries:

Overview:
* Cognex
* DynamSoft
* Accusoft
* DataSymbol
* DTK
* Inlite
* Softek
* Stecos
*




DynamSoft Barcode Reader SDK, dbr:


* Has python bindings: https://github.com/dynamsoft-dbr/python
* Blog: Barcode reader using DynamSoft Barcode Reader and OpenCV:
    * https://www.dynamsoft.com/blog/imaging/webcam-barcode-reader-opencv-python/  (2015)
    * https://github.com/yushulx/webcam-barcode-reader

DynamSoft blog posts:

* https://www.codepool.biz/multiprocessing-optimize-python-barcode-reader.html
*


Cognex:
* https://cmbdn.cognex.com/
* Cognex makes really good barcode readers and has a great Android Framework SDK.
* It has: Android, iOS, React Native (JS), and Web Assembly.
* But I don't thing there are any Python bindings for the Cognex SDK.
* I have been in contact with Cognex (Nov '18 and Aug '19), and they don't have anything that works
    for our use case.



### Python barcode-scanning apps:


dmtxscann:
* "webcam datamatrix reader in python + libdmtx + opencv"
* https://github.com/llpassarelli/dmtxscann

Barcode-scanner:
* https://pypi.org/project/barcode-scanner/
* gtk, zbar, gstreamer
* Github page no longer available. https://github.com/wheeler-microfluidics/barcode-scanner

garden.zbarcam:
* https://github.com/kivy-garden/garden.zbarcam
* Kivy Android python app.
* Uses pyzbar for barcode scanning.


pyBarcodeScan:
* https://github.com/kitsook/pyBarcodeScan
* Uses zbar and OpenCV to scan barcodes. From 2016.


RaspberryPiBarcodeScanner:
* https://github.com/briandorey/RaspberryPiBarcodeScanne
* I think this just connects to an external barcode scanner.
*


ViktorStiskala/barcode:
* https://github.com/ViktorStiskala/barcode
* Reads EAN13, EAN8, etc, barcodes.
* Uses evdev library.



Inventory:
* https://github.com/wbrenna/inventory
* Python 2.
*


### Barcode generators:


* https://github.com/WhyNotHugo/python-barcode - creates SVG barcodes using just the python standard library.




"""


