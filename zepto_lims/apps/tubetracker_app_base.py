# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""


"""

from zepto_lims.trackers.tubetracker import TubeTrackerDf
from zepto_lims.scanners.boxscanner import BoxScanner
from zepto_lims.utils.gridpos import val_pos_dict_from_grid
from zepto_lims.cameras.dummyfilecamera import DummyFileCamera
from zepto_lims.configs.config import ZeptoAppConfig
from zepto_lims.configs.default_config import DEFAULTS


class TubeTrackerAppBase:

    def __init__(self, config=None):
        if config is None:
            config = ZeptoAppConfig()
        self.config = config
        self.tubetracker = TubeTrackerDf(config)
        self.boxscanner = BoxScanner(config)
        self.camera = DummyFileCamera(config)

    def scan_and_update_box(self):
        image = self.camera.get_image()
        barcodes_grid = self.boxscanner.scan_box_image_grid(image)
        barcodes_dict = val_pos_dict_from_grid(barcodes_grid)
        barcodes_set = set(barcodes_dict.keys())   # Using .keys() is not strictly needed.
        best_box_match = self.tubetracker.get_best_matching_box(barcodes_set)
        answer = input(f"Is the scanned box '{best_box_match}'? [Y/n]").lower()
        if answer and answer[0] == 'n':
            print("OK. These are the existing freezer boxes:")
            print(list(self.tubetracker.get_boxes_data()['boxname']))
            boxname = input("Please type the name of the box: ")
        else:
            boxname = best_box_match
        self.tubetracker.update_tubes_from_barcodes(boxname, barcodes_dict)

    def add_box(self, boxname):
        self.tubetracker.add_box(boxname)

    # def scan_box_barcodes_and_update_database(self):
    #     image = self.camera.

