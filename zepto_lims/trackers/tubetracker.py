# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""

The `tubetracker` module contains logic relevant to dealing with tracking tubes in freezer boxes.
(or a similar domain model).

This module is typically used by the app for all its logic.
The app is the part that is actually used by the user.


The job of a tracker is to:

* Use a `boxscanner` from the `scanners` package to scan tube barcodes in a box to extract barcode values.
* Use a the configured client from the `client` package to retrieve box-tube location data.
* Compare the scanned barcodes against existing data box-tubes sets in the database and
    identify which box was just scanned, if possible.
* Identify missing tubes (where the location is now unknown).
* Use the client to update the box-tube location data.


* The `app(s)` are responsible for all logic, but not connected to how to retrieve data
    (other than asking the client for the data).
    The app decides which client to use and how to configure it.






"""

from collections import OrderedDict
from pprint import pprint
import pandas as pd

from zepto_lims.clients.internal_df_client import InternalDfClient


class TubeTrackerDf:
    """
    Tracker class for tracking tubes - uses pandas DataFrame for handling data.

    """

    def __init__(self, config=None, config_file=None):
        # This should probably be a dedicated `Config` object:
        self.config = config
        self.data_client = InternalDfClient(config=config)
        self.tubes_table_name_fmt = "{user}_tubes"
        self.boxes_table_name_fmt = "{user}_boxes"
        self.default_username = self.config.get('username', 'Default')

    @property
    def username(self):
        return self.config.get('username', self.default_username)

    @property
    def tubes_table_name(self):
        return self.tubes_table_name_fmt.format(user=self.username)

    @property
    def boxes_table_name(self):
        return self.tubes_table_name_fmt.format(user=self.config.get('username', 'Default'))

    def get_all_tubes_data(self):
        """ Retrieve a pandas DataFrame with all tubes (for the currently-selected user). """
        return self.data_client.get_table(self.tubes_table_name)

    def get_box_tubes(self):
        tubes_df = self.get_all_tubes_data()
        return tubes_df.groupby('boxname')

    def get_box_tubebarcodesets(self):
        # tubes_by_box = self.get_box_tubes()  # tubes grouped by boxes
        tubes_df = self.get_all_tubes_data()
        boxes_barcodesets = {boxname: set(group_df['barcode'].values)
                               for boxname, group_df in tubes_df.groupby('boxname')}
        return boxes_barcodesets

    def get_boxes_diff(self, barcodes_set):
        tubes_df = self.get_all_tubes_data()
        tubes_grouped_by_box = tubes_df.groupby('boxname')
        boxes_barcodesets = OrderedDict(
            {boxname: set(group_df['barcode'].values)
             for boxname, group_df in tubes_df.groupby('boxname')}
        )
        # common, added, missing
        boxes_diff = {boxname: (
                box_barcodes & barcodes_set,  # intersection
                barcodes_set - box_barcodes,  # added
                box_barcodes - barcodes_set,  # removed
            )
            for boxname, box_barcodes in boxes_barcodesets.items()
        }
        return boxes_diff

    def get_best_matching_boxes(self, barcodes_set):
        boxes_diff = self.get_boxes_diff(barcodes_set)
        boxes_diff_count = OrderedDict((
            boxname, (len(common), len(added), len(removed), len(common) - 0.2*len(added) - 0.1*len(removed))
            for boxname, (common, added, removed) in boxes_diff.items()
        ))
        box_similarity_scores = sorted([
            (len(common) - 0.2*len(added) - 0.1*len(removed), boxname)
            for boxname, (common, added, removed) in boxes_diff.items()
        ], reverse=True)
        pprint(box_similarity_scores)
        boxes_diff_count_df = pd.DataFrame.from_records(
            list(boxes_diff_count.values()),
            columns="common added removed similarity".split(),
            index=boxes_diff_count.keys()
        )
        boxes_diff_count_df.sort_values('common')
        print("Best matching boxes:")
        print(boxes_diff_count_df.head())
        return boxes_diff_count_df

    def get_best_matching_box(self, barcodes_set):
        boxes_diff_count_df = self.get_best_matching_boxes(barcodes_set)
        if len(boxes_diff_count_df) == 0:
            print("Did not find any existng boxes.")
            return
        best_box = boxes_diff_count_df.index[0]
        answer = input(f"Selct Box '{best_box}? [Y/n]").lower()
        if answer and answer[0] != 'y':
            print("OK; please create a new box for the scanned tube.")
            return
        return best_box

        


