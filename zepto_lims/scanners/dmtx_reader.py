# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""

Module for scanning DataMatrix barcodes, based on libdmtx.

libdmtx:
* https://github.com/dmtx/libdmtx
* https://github.com/dmtx
* dmtx-utils provides `dmtxread` and `dmtxwrite` utilities:
    * https://github.com/dmtx/dmtx-utils
* Has official wrappers/bindings for most languages:
    * https://github.com/dmtx/dmtx-wrappers
    * https://github.com/dmtx/dmtx-wrappers/tree/master/python - "pydmtx".
* http://libdmtx.wikidot.com/libdmtx-python-wrapper



call signature for pylibdmtx.pylibdmtx.decode():

    decode(image, timeout=None, gap_size=None, shrink=1, shape=None,
           deviation=None, threshold=None, min_edge=None, max_edge=None,
           corrections=None, max_count=None




"""


from pylibdmtx.pylibdmtx import decode


def decode_barcodes_from_image(image):
    """ Returns a list of decoded barcodes (data and region) from *all* recognized barcodes in the image.

    Args:
        image:

    Returns:
        List of NamedTuples with (data, rect) values,
        where data is the decoded binary data,
        and rect is a rectangle(left, top, width, height) indicating where the barcode was found.

    """
    return decode(image)


def decode_barcode_from_image(image, encoding='utf-8'):
    """ Returns the decoded barcode data from *the first* recognized barcode in the image.
    If 'binary_encoding' is provided, will decode the value to yield a string,
    otherwise returns a bytes.

    Args:
        image:
        encoding: If given, decode the binary barcode to a text string.

    Returns:
        A single string or bytes from form the first parsed barcode in the image.

    Raises:
        StopIteration exception if no barcodes was found in the image.
        UnicodeDecodeError, if the binary barcode data could not be decoded with the given encoding/character set.

    Examples:

        >>> # from PIL import Image
        >>> # image = Image.open('datamatrix.png')
        >>> from zepto_lims.scanners.dmtx_reader import decode_barcode_from_image
        >>> decode_barcode_from_image(image)

    """
    barcode_data = next(iter(decode(image))).data
    if encoding:
        return barcode_data.decode(encoding)
    else:
        return barcode_data
