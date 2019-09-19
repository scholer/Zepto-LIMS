# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""


"""

import numpy as np

from tests.testdata.boxscans import TEST_GRID_3x3_empty, TEST_GRID_3x3, TEST_GRID_3x3_values, TEST_GRID_3x3_coords, \
    TEST_GRID_3x3_valpos, TEST_GRID_3x3_rot90, TEST_GRID_3x3_rot90_values, TEST_GRID_3x3_rot90_coords, \
    TEST_GRID_3x3_rot90_coords_aligned, TEST_GRID_3x3_rot90_coords_aligned_origin, TEST_GRID_3x3_rot90_valpos, \
    TEST_GRID_3x3_rot180, TEST_GRID_3x3_rot180_values, TEST_GRID_3x3_rot180_coords, TEST_GRID_3x3_rot180_coords_aligned, \
    TEST_GRID_3x3_rot180_coords_aligned_origin, TEST_GRID_3x3_rot270, TEST_GRID_3x3_rot270_values, \
    TEST_GRID_3x3_rot270_coords, TEST_GRID_3x3_rot270_coords_aligned, TEST_GRID_3x3_rot270_coords_aligned_origin
from zepto_lims.utils.gridpos import val_pos_dict_from_grid
from zepto_lims.utils.gridpos import pos_val_dict_from_grid
from zepto_lims.utils.gridpos import values_coords_tup_from_grid
from zepto_lims.utils.gridpos import values_coords_tup_from_val_pos



def test_val_pos_dict_from_grid():

    # OBS: val_pos_dict_from_grid returns a dict {`val`: `pos`}
    # OBS: pos_val_dict_from_grid returns a dict {`pos`: `val`}

    val_pos_dict = val_pos_dict_from_grid(TEST_GRID_3x3_empty)
    assert val_pos_dict == {}

    val_pos_dict = val_pos_dict_from_grid(TEST_GRID_3x3)
    assert val_pos_dict == {
        'First': 'A01',
        'Second': 'A02',
        'Third': 'A03',
        'Fourth': 'C03',
    }

    val_pos_dict = val_pos_dict_from_grid(TEST_GRID_3x3_rot90)
    assert val_pos_dict == {
        'First': 'C01',
        'Second': 'B01',
        'Third': 'A01',
        'Fourth': 'A03',
    }

    val_pos_dict = val_pos_dict_from_grid(TEST_GRID_3x3_rot180)
    assert val_pos_dict == {
        'First': 'C03',
        'Second': 'C02',
        'Third': 'C01',
        'Fourth': 'A01',
    }

    val_pos_dict = val_pos_dict_from_grid(TEST_GRID_3x3_rot270)
    assert val_pos_dict == {
        'First': 'A03',
        'Second': 'B03',
        'Third': 'C03',
        'Fourth': 'C01',
    }


def test_pos_val_dict_from_grid():

    # OBS: val_pos_dict_from_grid returns a dict {`val`: `pos`}
    # OBS: pos_val_dict_from_grid returns a dict {`pos`: `val`}

    val_pos_dict = pos_val_dict_from_grid(TEST_GRID_3x3_empty)
    assert val_pos_dict == {}

    val_pos_dict = pos_val_dict_from_grid(TEST_GRID_3x3)
    assert val_pos_dict == {
        'A01': 'First',
        'A02': 'Second',
        'A03': 'Third',
        'C03': 'Fourth',
    }

    val_pos_dict = pos_val_dict_from_grid(TEST_GRID_3x3_rot90)
    assert val_pos_dict == {
        'C01': 'First',
        'B01': 'Second',
        'A01': 'Third',
        'A03': 'Fourth',
    }

    val_pos_dict = pos_val_dict_from_grid(TEST_GRID_3x3_rot180)
    assert val_pos_dict == {
        'C03': 'First',
        'C02': 'Second',
        'C01': 'Third',
        'A01': 'Fourth',
    }

    val_pos_dict = pos_val_dict_from_grid(TEST_GRID_3x3_rot270)
    assert val_pos_dict == {
        'A03': 'First',
        'B03': 'Second',
        'C03': 'Third',
        'C01': 'Fourth',
    }


def test_values_coords_tup_from_grid():

    values, coords = values_coords_tup_from_grid(TEST_GRID_3x3)
    assert values == TEST_GRID_3x3_values
    assert (coords == TEST_GRID_3x3_coords).all()
    # Manual verification:
    assert values == ('First', 'Second', 'Third', 'Fourth')
    assert (coords == np.array([(0, 0), (0, 1), (0, 2), (2, 2)])).all()

    # Technically, the *order* of the coordinates is not specified, so the above
    # test is implementation specific. We should test as follows instead:
    coord_tups = [tuple(xy) for xy in coords]
    assert set(values) == {'First', 'Second', 'Third', 'Fourth'}
    # Is zero-indexed:
    assert set(coord_tups) == {(0, 0), (0, 1), (0, 2), (2, 2)}
    assert dict(zip(values, coord_tups)) == dict(
        zip(['First', 'Second', 'Third', 'Fourth'],
            [(0, 0), (0, 1), (0, 2), (2, 2)])
    )

    # Check the rotated grids:
    values, coords = values_coords_tup_from_grid(TEST_GRID_3x3_rot90)
    assert values == TEST_GRID_3x3_rot90_values
    assert (coords == TEST_GRID_3x3_rot90_coords).all()

    values, coords = values_coords_tup_from_grid(TEST_GRID_3x3_rot180)
    assert values == TEST_GRID_3x3_rot180_values
    assert (coords == TEST_GRID_3x3_rot180_coords).all()

    values, coords = values_coords_tup_from_grid(TEST_GRID_3x3_rot270)
    assert values == TEST_GRID_3x3_rot270_values
    assert (coords == TEST_GRID_3x3_rot270_coords).all()


def test_values_coords_tup_from_val_pos():

    values, coords = values_coords_tup_from_val_pos(TEST_GRID_3x3_valpos)
    assert values == TEST_GRID_3x3_values
    assert np.all(coords == TEST_GRID_3x3_coords)

    values, coords = values_coords_tup_from_val_pos(TEST_GRID_3x3_rot90_valpos)
    assert values == TEST_GRID_3x3_rot90_values
    assert np.all(coords == TEST_GRID_3x3_rot90_coords)