"""

Module for scanning a single box with tubes in a pre-defined pattern, e.g. 9x9 or 10x10 grid.

"""


def estimate_box_grid_params(image):
    # Returns a named GridParams tuple that locates the "box divider" grid on the box image.
    # This basically just performs some image pattern recognition by template matching to a square.
    # Template matching with scaling and maybe rotation.
    # Alternatively, just keep the grid parameters fix/pre-defined,
    # and let the user acquire a suitable image.
    pass


def segment_image_to_grid(image, grid_params):
    # Returns multiple small images as an ordered dict(A1 => tube-image).
    # Grid-params is expected as one of the following:
    # * A GridParams namedtuple with `top`, `bottom`, `left`, `right`, `grid` attributes.
    # * A 5-element tuple: (top, bottom, left, right, grid)
    # If `grid` is an integer, e.g. 10, the grid is a 10x10 square.
    # Otherwise, `grid` is a two-tuple with (width, height).
    pass


def scan_lid_barcode(image):
    # Returns the barcode value from the barcode in the image.
    # This only expects the image to contain a single, easily-identifiable barcode.
    # This function may do some image filtering and processing to make it easier for
    # the barcode scanner to identify the 2D barcode.
    pass


def scan_tubes_in_box(image):
    grid_params = estimate_box_grid_params(image)
    grid_images = segment_image_to_grid(image, grid_params)
    grid_barcodes = {pos: scan_lid_barcode(tube_image) for pos, tube_image in grid_images.items()}
    return grid_barcodes

