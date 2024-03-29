# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""

Module for scanning a single box with tubes in a pre-defined pattern, e.g. 9x9 or 10x10 grid.

TODO: "Aggregating" scanner, which scans multiple images, using the barcodes to relate
TODO: barcode positions and build up the full grid of barcodes.
TODO: This is mostly useful if it turns out to be really hard to take a single image
TODO: from which all barcodes can be properly read.


"""

from collections import namedtuple
import numpy as np

try:
    from PIL.ImageFile import ImageFile as PilImageFile
except ImportError:
    def is_pil_image(image):
        # https://github.com/NaturalHistoryMuseum/pylibdmtx/blob/master/pylibdmtx/pylibdmtx.py#L188
        return 'PIL' in str(type(image))
    PilImageFile = None
else:
    def is_pil_image(image):
        return isinstance(image, PilImageFile)


from .dmtx_reader import decode_barcode_from_image


def estimate_box_grid_params(image):
    # Returns a named GridParams tuple that locates the "box divider" grid on the box image.
    # This basically just performs some image pattern recognition by template matching to a square.
    # Template matching with scaling and maybe rotation.
    # Alternatively, just keep the grid parameters fix/pre-defined,
    # and let the user acquire a suitable image.
    pass


def segment_image_to_grid(image, grid_params):
    """ Split image into n×m smaller images according to the specified grid parameters.

    Args:
        image:
        grid_params: A 5-element tuple: (top, bottom, left, right, grid_shape)
            If `grid_shape` is an integer, e.g. 10, the grid_shape is a 10x10 square.
            Otherwise, `grid_shape` is a two-tuple with (width, height).

    Returns:
        Returns a list-of-lists of smaller images.

    Returns multiple small images as a list of lists.
    Actually, maybe this could be done by re-shaping to a 4D matrix?
    Except there may be some rounding errors because the number of pixels may not be
    a multiple of the grid shape?

    Grid-params is expected as one of the following:
    * A GridParams namedtuple with `top`, `bottom`, `left`, `right`, `grid_shape` attributes.
    * A 5-element tuple: (top, bottom, left, right, grid_shape)
    * A dict, with items: 'margin', 'shape', 'type'
        * Currently, we only support type='rectangle', but not type='square'.
    If `grid_shape` is an integer, e.g. 10, the grid_shape is a 10x10 square.
    Otherwise, `grid_shape` is a two-tuple with (width, height).

    """

    # if is_pil_image(image):
    #     image = np.array(image)
    # This doesn't work for opencv images from cv2.imread.
    # Probably better to always just cast as numpy array:
    assert image
    image = np.array(image)
    print("image.shape", image.shape)
    if isinstance(grid_params, (tuple, namedtuple)):
        top, bottom, left, right, grid_shape = grid_params
    elif isinstance(grid_params, dict):
        top, bottom, left, right = grid_params['margin']
        grid_shape = grid_params['shape']
        grid_type = grid_params.get('type', 'rectangular')
    else:
        raise TypeError(f"Unrecognized type {type(grid_params)} for argument `grid_params` = {grid_params}.")
    if isinstance(grid_shape, int):
        grid_shape = (grid_shape, grid_shape)
    original_height, original_width = image.shape
    # Negative numbers for `bottom` and right` mean "margin from right/bottom".
    # Slicing to negative works just fine, no need to convert to positive offset:
    # if bottom < 0:
    #     bottom = original_height + bottom
    # if right < 0:
    #     right = original_width + right
    if isinstance(top, float) and -2.0 < top < +2.0:
        print(f"Converted `top` to  {image.shape[0]} * {top} = ", end="")
        top = int(image.shape[0] * top)
        print(f"{top}")
    if isinstance(bottom, float) and -2.0 < bottom < +2.0:
        print(f"Converted `bottom` to  {image.shape[0]} * {bottom} = ", end="")
        bottom = int(image.shape[0] * bottom)
        print(f"{bottom}")
    if isinstance(left, float) and -2.0 < left < +2.0:
        print(f"Converted `left` to  {image.shape[0]} * {left} = ", end="")
        left = int(image.shape[0] * left)
        print(f"{left}")
    if isinstance(right, float) and -2.0 < right < +2.0:
        print(f"Converted `top` to  {image.shape[0]} * {right} = ", end="")
        right = int(image.shape[0] * right)
        print(f"{right}")
    if top or bottom or left or right:
        # Origin is in UPPER LEFT corner.
        if bottom is not None and 0 <= bottom <= (top if top is not None else 0):
            msg = (f"ERROR, `bottom`={bottom} is smaller than `top={top}`! "
                   "The `top`, `bottom`, `left`, `right` parameters are ABSOLUTE coordinates "
                   "with origin at TOP LEFT corner. If you meant to use margin offsets, use negative values for "
                   "`bottom` and `right` arguments.")
            print(msg)
            raise ValueError(msg)
        if right is not None and 0 <= right <= (left if left is not None else 0):
            msg = (f"ERROR, `right={right}` is smaller than `left`={left}! "
                   "The `top`, `bottom`, `left`, `right` parameters are ABSOLUTE coordinates "
                   "with origin at TOP LEFT corner. If you meant to use margin offsets, use negative values for "
                   "`bottom` and `right` arguments.")
            print(msg)
            raise ValueError(msg)
        im_cropped = image[top:bottom, left:right]
    else:
        im_cropped = image
    nrows, ncols = grid_shape
    height, width = im_cropped.shape
    print("im_cropped.shape:", im_cropped.shape)
    print("nrows, ncols:", nrows, ncols)
    print("image height, width:", height, width)

    im_grid = [[
            im_cropped[
                int(height*r/nrows):int(height*(r+1)/nrows),
                int(width*c/ncols):int(width*(c+1)/ncols)
            ]
            for c in range(ncols)]
        for r in range(nrows)
    ]
    print("segment shapes:", [[im.shape for im in row] for row in im_grid])
    return im_grid


def scan_lid_barcode(image):
    # Returns the barcode value from the barcode in the image.
    # This only expects the image to contain a single, easily-identifiable barcode.
    # This function may do some image filtering and processing to make it easier for
    # the barcode scanners to identify the 2D barcode.
    try:
        data = decode_barcode_from_image(image, encoding=None)
    except StopIteration:
        return None
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        return str(data)


def scan_barcodes_in_grid(image, grid_params=None):
    """ Returns a matrix of decoded barcode data (list of lists of strings).
    """
    if grid_params is None:
        grid_params = estimate_box_grid_params(image)
    grid_images = segment_image_to_grid(image, grid_params)
    grid_barcodes = [[scan_lid_barcode(tube_image) for tube_image in image_row] for image_row in grid_images]
    return grid_barcodes


class BoxScanner:

    def __init__(self, config):
        self.config = config
        self.last_box_scan = None
        self.best_box_scan = None

    @property
    def box_margin(self):
        """ Return box margin as defined by the config. Defaults to a 10 pixel margin all around."""
        return self.config.get('boxscanner_box_margin', (10, 10, -10, -10))

    @property
    def box_grid(self):
        """ Return box grid as defined by the config. Defaults to a 10x10 grid."""
        box_grid = self.config.get('boxscanner_box_margin', (10, 10))
        # if isinstance(box_grid, int):
        #     box_grid = (box_grid, box_grid)
        return box_grid

    @property
    def box_grid_params(self):
        """ grid_params is a tuple of (nmargin_top, nmargin_bottom, nmargin_left, nmargin_right, grid_shape)"""
        return self.box_margin + (self.box_grid,)

    def scan_box_image_grid(self, image):
        grid_barcodes = scan_barcodes_in_grid(image=image, grid_params=self.box_grid_params)
        self.last_box_scan = grid_barcodes
        if self.best_box_scan is None or self.best_box_scan <= len(grid_barcodes):
            self.best_box_scan = grid_barcodes
        return grid_barcodes


class AggregatingBoxScanner(BoxScanner):
    """
    Special BoxScanner that is capable of repeatedly acquiring images and scanning for barcodes,
    building up a grid of barcodes gradually as it gains more information on barcodes and
    their relative location.

    """
