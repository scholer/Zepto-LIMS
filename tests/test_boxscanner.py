# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""


"""

from pathlib import Path
from pprint import pprint
import numpy as np


from zepto_lims.utils.image import imread, imshow


from zepto_lims.scanners.boxscanner import (
    segment_image_to_grid, scan_barcodes_in_grid, scan_lid_barcode,
)

TEST_DATA_DIR = Path(__file__).parent / 'testdata'

RANDOM_IMAGE_160x90 = np.random.randint(0, 256, (160, 90))
RANDOM_IMAGE_100x100 = np.random.randint(0, 256, (100, 100))
RANDOM_IMAGE_260x220 = np.random.randint(0, 256, (260, 220))
for array in (
    RANDOM_IMAGE_160x90,
    RANDOM_IMAGE_100x100,
    RANDOM_IMAGE_260x220,
):
    array.flags.writeable = False

datamatrix_1x_image = imread(TEST_DATA_DIR / 'images' / 'datamatrix_x1_02_25pct-q90.jpg')
datamatrix_4x_image = imread(TEST_DATA_DIR / 'images' / 'datamatrix_x4_50pct-90.jpg')


def test_segment_image_to_grid():
    # `top`, `bottom`, `left`, `right`, `shape`
    grid_params = (35, -35, 0, None, 9)
    img_segments = segment_image_to_grid(RANDOM_IMAGE_160x90, grid_params=grid_params)
    assert len(img_segments) == 9
    assert all(len(row) == 9 for row in img_segments)
    assert all(im.shape == (10, 10) for row in img_segments for im in row)

    # `top`, `bottom`, `left`, `right`, `shape`
    grid_params = (None, None, None, None, 10)
    img_segments = segment_image_to_grid(RANDOM_IMAGE_100x100, grid_params=grid_params)
    assert len(img_segments) == 10
    assert all(len(row) == 10 for row in img_segments)
    assert all(im.shape == (10, 10) for row in img_segments for im in row)

    # `top`, `bottom`, `left`, `right`, `shape`
    grid_params = (30, -30, 10, -10, (10, 10))
    img_segments = segment_image_to_grid(RANDOM_IMAGE_260x220, grid_params=grid_params)
    assert len(img_segments) == 10
    assert all(len(row) == 10 for row in img_segments)
    assert all(im.shape == (20, 20) for row in img_segments for im in row)

    # Test rectangular (non-square) image segments:
    # `top`, `bottom`, `left`, `right`, `shape`
    grid_params = (30, -30, 65, -65, (10, 9))
    img_segments = segment_image_to_grid(RANDOM_IMAGE_260x220, grid_params=grid_params)
    assert len(img_segments) == 10
    assert all(len(row) == 9 for row in img_segments)
    pprint([[im.shape for im in row] for row in img_segments])
    assert all([im.shape == (20, 10) for row in img_segments for im in row])


def test_scan_lid_barcode():

    barcode_str = scan_lid_barcode(datamatrix_1x_image)
    assert barcode_str == '20190729 RS123d1 Sample Test description'


def test_scan_barcodes_in_grid():
    # `top`, `bottom`, `left`, `right`, `shape`
    grid_params = (10, -1, 20, -10, (4, 1))  # rows, cols
    print("datamatrix_4x_image:", datamatrix_4x_image)
    assert datamatrix_4x_image is not None  # cv2.imread just returns None if no image file.
    im_grid = segment_image_to_grid(datamatrix_4x_image, grid_params=grid_params)
    imshow(im_grid[1][0])
    barcodes_grid = scan_barcodes_in_grid(datamatrix_4x_image, grid_params=grid_params)
    pprint(barcodes_grid)
    expected = [
        ['190728 RS123d2 S2Descr'],
        [None],  # For some reason this segment doesn't scan.
        ['190728 RS123d2 S2Descr'],
        ['20190729 RS123d1 Sample Test description']
    ]
    assert barcodes_grid == expected


def adhoc():

    imshow(datamatrix_4x_image)
    grid_params = (10, -1, 20, -10, (4, 1))  # rows, cols
    im_grid = segment_image_to_grid(datamatrix_4x_image, grid_params=grid_params)
    imshow(im_grid[1][0])
    input("Press Enter to continue...")


if __name__ == '__main__':
    adhoc()
