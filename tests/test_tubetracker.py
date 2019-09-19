# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""

Module for testing the tubetracker module.

"""

import pandas as pd
from io import StringIO
import pytest
import numpy as np

from tests.testdata.table_data import (
    BOXES_DATA_01,
    TUBES_DATA_CSV_3x3, TUBES_DATA_CSV_3x3_rot90,
    TUBES_DATA_CSV_MULTI, TUBES_DATA_CSV_MULTI_MOD1
)
from zepto_lims.trackers import tubetracker
from zepto_lims.utils.gridpos import val_pos_dict_from_grid
from tests.testdata.boxscans import (TEST_GRID_3x3_rot90, TEST_GRID_3x3_mod1)


def test_tubetracker():
    config = {
        'username': 'testuser',
    }
    t = tubetracker.TubeTrackerDf(config=config)

    assert t.username == "testuser"
    assert t.tubes_table_name == "testuser_tubes"
    assert t.boxes_table_name == "testuser_boxes"

    # Monkey-patch data getter methods:
    boxes_df = pd.read_csv(StringIO(BOXES_DATA_01))
    tubes_df_3x3 = pd.read_csv(StringIO(TUBES_DATA_CSV_3x3))
    tubes_df_3x3_rot90 = pd.read_csv(StringIO(TUBES_DATA_CSV_3x3_rot90))
    tubes_df_multi = pd.read_csv(StringIO(TUBES_DATA_CSV_MULTI))
    tubes_df_multi_mod1 = pd.read_csv(StringIO(TUBES_DATA_CSV_MULTI_MOD1), keep_default_na=False)

    # print(boxes_df)
    # print(tubes_df_3x3)
    t.get_boxes_data = lambda: boxes_df
    t.get_tubes_data = lambda: tubes_df_multi
    assert list(t.get_box_tubes('box1')['barcode'].values) == ['First', 'Second', 'Third', 'Fourth']
    assert t.get_barcode_val_pos_for_box('box1') == dict(zip(
        ['First', 'Second', 'Third', 'Fourth'], ['A01', 'A02', 'A03', 'C03']
    ))
    assert t.get_barcode_val_pos_for_box('box2') == dict(zip(
        ['tube1', 'tube2', 'tube3', 'tube4', 'tube9'], ['A01', 'B01', 'A03', 'A08', 'D08']
    ))
    assert t.get_barcode_val_pos_for_box('box3') == dict(zip(
        ['One', 'Two'], ['A01', 'A02']
    ))
    assert t.get_box_tubebarcodesets() == {
        'box1': {'First', 'Second', 'Third', 'Fourth'},
        'box2': {'tube1', 'tube2', 'tube3', 'tube4', 'tube9'},
        'box3': {'One', 'Two'},
    }
    assert t.get_boxes_diff({'First', 'Second', 'Third', 'tube1', 'tube2', 'One'}) == {
        # (intersection, added, removed)
        'box1': ({'First', 'Second', 'Third'}, {'tube1', 'tube2', 'One'}, {'Fourth'}),
        'box2': ({'tube1', 'tube2'}, {'First', 'Second', 'Third', 'One'}, {'tube3', 'tube4', 'tube9'}),
        'box3': ({'One'}, {'First', 'Second', 'Third', 'tube1', 'tube2'}, {'Two'}),
    }
    # t.get_best_matching_boxes({'First', 'Second', 'Third', 'tube1', 'tube2', 'One'})
    # yes_man = lambda x: 'y'
    assert t.get_best_matching_box(
        {'First', 'Second', 'Third', 'tube1', 'tube2', 'One'}) == 'box1'

    # Test add_box:
    with pytest.raises(ValueError):
        t.add_box('box1')

    # avg_dist, rotation, global_shift
    assert t.get_best_box_rotation('box1', val_pos_dict_from_grid(TEST_GRID_3x3_rot90))[1] == 1

    # test update_tubes_from_barcodes:
    t.save_boxes_data = lambda df, flush: None
    t.save_tubes_data = lambda df, flush: None
    t.add_box = lambda boxname: None

    # valpos_dict = val_pos_dict_from_grid(TEST_GRID_3x3_mod1)
    print("Before:")
    print(tubes_df_multi)

    print("Expected:")
    print(tubes_df_multi_mod1)

    # print("Equals?")
    # print(tubes_df_multi == tubes_df_multi_mod1)
    # print((tubes_df_multi == tubes_df_multi_mod1).all())
    # print((tubes_df_multi == tubes_df_multi_mod1).all().all())
    # print("df.value comparison:")
    # print((tubes_df_multi.values == tubes_df_multi_mod1.values).all())

    # Make sure we don't have any changes:
    assert (tubes_df_multi.values == tubes_df_multi.values).all()
    assert not np.any(tubes_df_multi.values != tubes_df_multi.values)
    # Make sure we have some changes (any):
    assert np.any(tubes_df_multi.values != tubes_df_multi_mod1.values)
    t.update_tubes_from_barcodes(
        boxname='box1', barcodes=TEST_GRID_3x3_mod1,
        update_removed=True, boxname_for_removed_tubes='(missing)',
        create_box_if_nonexisting=True,
    )
    # TubeTrackerDf should update in-place:
    print("After:")
    print(tubes_df_multi)
    print("df.value comparison:")
    print((tubes_df_multi.values == tubes_df_multi_mod1.values))
    assert np.all(tubes_df_multi.values == tubes_df_multi_mod1.values)


