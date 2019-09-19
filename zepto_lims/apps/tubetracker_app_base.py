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
            config = ZeptoAppConfig(default=DEFAULTS)
        self.config = config
        self.tubetracker = TubeTrackerDf(config)
        self.boxscanner = BoxScanner(config)
        self.camera = DummyFileCamera(config)

    def scan_and_update_box(self):
        image = self.camera.get_image()
        barcodes_grid = self.boxscanner.scan_box_image_grid(image)
        barcodes_dict = val_pos_dict_from_grid(barcodes_grid)  # {barcode: pos} dict
        barcodes_set = set(barcodes_dict.keys())   # Using .keys() is not strictly needed.
        best_box_match = self.tubetracker.get_best_matching_box(barcodes_set)
        answer = input(f"Is the scanned box '{best_box_match}'? [Y/n]").lower()
        if answer and answer[0] == 'n':
            print("OK. These are the existing freezer boxes:")
            print(list(self.tubetracker.get_boxes_data()['boxname']))
            boxname = input("Please type the name of the box: ")
        else:
            boxname = best_box_match
            avg_dist, rotation, global_shift = self.tubetracker.get_best_box_rotation(
                boxname=best_box_match, barcodes_val_pos_dict=barcodes_dict
            )
            if rotation != 0:
                print("The scanned box was rotated since it was last scanned.")
                print("avg_dist, rotation, global_shift:", [avg_dist, rotation, global_shift])
                old_or_new = input("Would you like to use OLD rotation or NEW rotation? [o/N]  ").lower() or 'n'
                use_old_rotation = (old_or_new[0] == 'o')
                if use_old_rotation:
                    # This requires rotating the barcodes_grid,
                    print("Sorry, using old rotation is not yet supported.")
        self.tubetracker.update_tubes_from_barcodes(boxname, barcodes_dict)

    def add_box(self, boxname):
        self.tubetracker.add_box(boxname)

    # def scan_box_barcodes_and_update_database(self):
    #     image = self.camera.

