# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""


"""

from zepto_lims.trackers.tubetracker import TubeTrackerDf
from zepto_lims.scanners.boxscanner import BoxScanner
from zepto_lims.cameras.dummyfilecamera import DummyFileCamera


class TubeTrackerAppBase:

    def __init__(self, config, config_file):
        self.config = config
        self.config_file = config_file
        self.tubetracker = TubeTrackerDf(config)
        self.boxscanner = BoxScanner(config)
        self.camera = DummyFileCamera(config)

    def scan_and_update_box(self):
        image = self.camera.get_image()
        barcodes_grid = self.boxscanner.scan_box_image_grid(image)
        barcodes_set = {barcode for row in barcodes_grid for barcode in row}
        self.tubetracker.get_matching_boxes(barcodes_set)



