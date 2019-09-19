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



OBS: Pandas is absolutely NOT optimal for appending data.
We could consider having the data in another format,
e.g. just sqlite.

Sqlite alternatives:

* MongoDB

Pandas alternatives:

* Astropy.table
* HDF5, HDFStore
* CDF
* xarray
* python-table - https://pypi.org/project/tabel/
* static-frame (immutable dataframes).
* SFrame - Scalable Frames, by Graphlab Create.
*


"""

from typing import Union  # Optional
from collections import OrderedDict
from pprint import pprint
import pandas as pd

from zepto_lims.dataclients.internal_df_client import InternalDfClient
from zepto_lims.utils.gridpos import val_pos_dict_from_grid, values_coords_tup_from_val_pos
from zepto_lims.utils.transformation import calc_best_values_coords_rotation_result


class TubeTrackerDf:
    """
    Tracker class for tracking tubes.
    This implementation uses pandas DataFrame for handling data (InternalDfClient).

    """

    def __init__(self, config: dict):
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
        return self.boxes_table_name_fmt.format(user=self.config.get('username', 'Default'))

    def get_tubes_data(self):
        """ Retrieve a pandas DataFrame with all tubes (for the currently-selected user). """
        return self.data_client.get_table(self.tubes_table_name)

    def get_boxes_data(self):
        """ Retrieve a pandas DataFrame with all tubes (for the currently-selected user). """
        return self.data_client.get_table(self.boxes_table_name)

    def save_tubes_data(self, df, flush=None):
        """ Retrieve a pandas DataFrame with all tubes (for the currently-selected user). """
        self.data_client.set_table(self.tubes_table_name, df, flush=flush)

    def save_boxes_data(self, df, flush=None):
        """ Retrieve a pandas DataFrame with all tubes (for the currently-selected user). """
        self.data_client.set_table(self.boxes_table_name, df, flush=flush)

    def get_box_tubes(self, boxname):
        """ Get dataframe with tubes in a single box. """
        df = self.get_tubes_data()
        return df.loc[df['boxname'] == boxname, :]

    def get_barcode_val_pos_for_box(self, boxname):
        df = self.get_box_tubes(boxname)
        return dict(zip(df['barcode'], df['pos']))

    def get_tubes_groupedby_box(self):
        """ Reference function for how to group a pandas DataFrame. """
        tubes_df = self.get_tubes_data()
        return tubes_df.groupby('boxname')

    def get_box_tubebarcodesets(self):
        # tubes_by_box = self.get_tubes_groupedby_box()  # tubes grouped by boxes
        tubes_df = self.get_tubes_data()
        boxes_barcodesets = {
            boxname: set(group_df['barcode'].values)
            for boxname, group_df in tubes_df.groupby('boxname')
        }
        return boxes_barcodesets

    def get_boxes_diff(self, barcodes_set):
        """ Calculate differences between a given set of barcodes and the boxes in the database. """
        boxes_barcodesets = self.get_box_tubebarcodesets()
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
        """ Compare all boxes' barcodes with the given barcodes_set. """
        boxes_diff = self.get_boxes_diff(barcodes_set)
        boxes_diff_count = OrderedDict((
            (boxname, (len(common), len(added), len(removed), len(common) - 0.2*len(added) - 0.1*len(removed)))
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

    def get_best_matching_box(
            self, barcodes_set,
            # user_input_callback=lambda best_box: input(f"Select Box '{best_box}? [Y/n] ").lower()
    ):
        """ Get the box with most barcodes in common with the given barcodes_set. """
        boxes_diff_count_df = self.get_best_matching_boxes(barcodes_set)
        if len(boxes_diff_count_df) == 0:
            print("Did not find any existing boxes.")
            return
        best_box = boxes_diff_count_df.index[0]
        # TODO: This should be moved to the `app` part of the program:
        # # answer = input(f"Select Box '{best_box}? [Y/n] ").lower()
        # answer = user_input_callback(best_box)
        # if answer and answer[0] != 'y':
        #     print("OK; please create a new box for the scanned tube.")
        #     return
        return best_box

    def get_best_box_rotation(self, boxname, barcodes_val_pos_dict):
        existing_val_pos_dict = self.get_barcode_val_pos_for_box(boxname)
        values1, coords1 = values_coords_tup_from_val_pos(existing_val_pos_dict)
        values2, coords2 = values_coords_tup_from_val_pos(barcodes_val_pos_dict)
        avg_dist, rotation, global_shift = calc_best_values_coords_rotation_result(
            values1, coords1, values2, coords2
        )
        return avg_dist, rotation, global_shift

    def add_box(self, boxname):
        """ Add a new box to the boxes table.
        This does not add any tubes.
        """
        df = self.get_boxes_data()
        boxnames = df['boxname']
        if boxname in boxnames.values:
            raise ValueError(f"Boxname '{boxname}' already present in boxes table!")
        self.data_client.append_row(
            table=self.boxes_table_name, row={'boxname': boxname})

    def update_tubes_from_barcodes(
            self, boxname: str,
            barcodes: Union[list, dict],
            update_removed=True,
            boxname_for_removed_tubes='(missing)',
            pos_for_removed_tubes='N/A',
            # mark_removed_as='(missing)',
            create_box_if_nonexisting=True,
            flush=True
    ):
        """ Update the given box based on scanned barcodes in a box grid.

        Args:
            boxname: The box from which the barcodes was just scanned.
            barcodes: The barcodes that were just scanned.
                Either a List of list of strings, representing the grid in a box:
                    [['t1', 't2', None],
                     [None, None, 't3'],
                     [None, 't4', None]]
                Or, alternatively, a dict with {barcode: A01-position}
            update_removed: Whether to update removed tubes.
                (Removed tubes = tubes that were previously in the box but not anymore /
                 with a barcode not in `barcodes`.)
            boxname_for_removed_tubes: Explicitly set the boxname for removed tubes.
                Special boxnames includes:
                    (checked-out)   For tubes that I'm currently working with (so they are "checked out").
                    (missing)       For missing tubes that I've lost track of.
                    (removed)       For removed tubes. This is a generic label that covers
                                    both 'missing' and 'checked-out'.
                    (depleted)      For tubes that have been depleted.
                    (trashed)       For tubes that have been thrown out.
            create_box_if_nonexisting: Whether to automatically create `boxname` if it doesn't exist
                in the database.
            flush: Flush changes (typically to disk).

        Args to be added later:
            mark_removed_as: This is for implementing a secondary way of marking the status of
                removed tubes, e.g. by having a single ENUM 'stattus' column.

        Returns:
            None
        """
        if not barcodes:
            print(f"Empty `barcodes` value {barcodes}. Aborting.")
            return
        if isinstance(barcodes, list):
            barcodes = val_pos_dict_from_grid(grid=barcodes)
        tubes_df = self.get_tubes_data()
        boxes_df = self.get_boxes_data()
        # Sanity checks of the provided DataFrames:
        if 'barcode' not in tubes_df:
            print("INFO: Adding column 'barcode' to tubes_df !")
            tubes_df['barcode'] = 'N/A'
        if 'boxname' not in tubes_df:
            print("INFO: Adding column 'boxname' to tubes_df !")
            tubes_df['boxname'] = 'N/A'
        if 'pos' not in tubes_df:
            print("INFO: Adding column 'pos' to tubes_df !")
            tubes_df['pos'] = 'N/A'
        if 'boxname' not in boxes_df:
            print("INFO: Adding column 'boxname' to tubes_df !")
            boxes_df['boxname'] = 'N/A'

        # Check that the box we are using is present in the boxes table:
        boxnames = boxes_df['boxname'].values
        if boxname not in boxnames:
            print(f"WARNING: `boxname` '{boxname}' is not present in 'boxes' table.")
            # TODO: All user-input should be either callbacks or refactored out to app:
            if create_box_if_nonexisting is None or create_box_if_nonexisting == 'ask':
                answer = (input(
                    f"Create new box with boxname '{boxname}'? [Yes/no/abort] "
                ).lower() or 'y')[0]
                if answer and answer[0] == 'a':
                    print("OK, aborting...")
                    return
                create_box_if_nonexisting = (answer[0] == 'y')
            if create_box_if_nonexisting is True:
                self.add_box(boxname)
            elif create_box_if_nonexisting == 'raise':
                raise ValueError(f"`boxname` '{boxname}' does not exist in the database.")

        # Before we update the scanned barcodes, we should identify the barcodes that have
        # been removed and update the box on these to '(missing)' or similar.
        previous_box_barcodes = set(tubes_df['barcode'][tubes_df['boxname'] == boxname])
        barcodes_set = set(barcodes.keys())
        removed = previous_box_barcodes - barcodes_set
        added = barcodes_set - previous_box_barcodes
        print(f"Removed barcodes from box '{boxname}':", sorted(removed))
        if update_removed:
            # Eliminate for-loop by using pd.Series.isin(collection) instead of pd.Series == val
            for barcode in removed:
                # tubes_df['boxname'].where(tubes_df['barcode'] == barcode, boxname_for_removed_tubes, inplace=True)
                # tubes_df['pos'].where(tubes_df['barcode'] == barcode, 'N/A', inplace=True)
                tubes_df.loc[tubes_df['barcode'] == barcode, 'boxname'] = boxname_for_removed_tubes
                tubes_df.loc[tubes_df['barcode'] == barcode, 'pos'] = pos_for_removed_tubes

        ## RANT: WHY IS PANDAS SO WEIRD??
        ## FROM pandas.DataFramw.where() docstring:
        ## > "Replace values where the condition is False."
        ## Why should the condition be False, instead of True?
        ## From the docs:
        ## > "Roughly `df1.where(m, df2)` is equivalent to `np.where(m, df1, df2)`."
        ## Maybe just use df.loc[mask, col] = (new value)

        # Update 'boxname' and 'pos' for the scanned barcodes:
        # This could perhaps also be done without a for-loop, by using `in barcodes.keys()`,
        # tubes_df.loc[tubes_df['barcode'] in barcode, 'boxname'] = boxname
        # or by creating a DataFrame from barcodes and then using df.update().
        # Using df.update() probably requires using `barcode` as the index of the DataFrame.
        # Using df.update() would also make it easier to add new tubes.
        for barcode, pos in barcodes.items():
            # tubes_df['boxname'].where(tubes_df['barcode'] == barcode, boxname, inplace=True)
            # tubes_df['pos'].where(tubes_df['barcode'] == barcode, pos, inplace=True)
            # Alternative to using where:
            tubes_df.loc[tubes_df['barcode'] == barcode, 'boxname'] = boxname
            tubes_df.loc[tubes_df['barcode'] == barcode, 'pos'] = pos

        # TODO: Add new tubes!

        # Finally, make sure to save the updated dataframes:
        self.save_boxes_data(boxes_df, flush=flush)
        self.save_tubes_data(tubes_df, flush=flush)
