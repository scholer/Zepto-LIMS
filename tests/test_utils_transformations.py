# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""


"""

import numpy as np

from zepto_lims.utils.transformation import calc_best_grid_rotation_result, align_coords_by_values
from zepto_lims.utils.transformation import rot_90deg, rotate_coords
from zepto_lims.utils.gridpos import values_coords_tup_from_grid


from .test_utils_gridpos import TEST_GRID_3x3, TEST_GRID_3x3_rot90, TEST_GRID_3x3_rot180, TEST_GRID_3x3_rot270
from .test_utils_gridpos import TEST_GRID_3x3_values, TEST_GRID_3x3_rot90_values, TEST_GRID_3x3_rot180_values, TEST_GRID_3x3_rot270_values
from .test_utils_gridpos import TEST_GRID_3x3_coords, TEST_GRID_3x3_rot90_coords, TEST_GRID_3x3_rot180_coords, TEST_GRID_3x3_rot270_coords
from .test_utils_gridpos import TEST_GRID_3x3_rot90_coords_aligned, TEST_GRID_3x3_rot180_coords_aligned, TEST_GRID_3x3_rot270_coords_aligned
from .test_utils_gridpos import (
    TEST_GRID_3x3_rot90_coords_aligned_origin,
    TEST_GRID_3x3_rot180_coords_aligned_origin,
    TEST_GRID_3x3_rot270_coords_aligned_origin
)


def test_align_coords_by_values():
    coords, coords_rot90 = align_coords_by_values(
        TEST_GRID_3x3_values, TEST_GRID_3x3_coords,
        TEST_GRID_3x3_rot90_values, TEST_GRID_3x3_rot90_coords
    )
    # We have the same values, and the implementation aligns by `values1`,
    # so the first should not have changed:
    assert (coords == TEST_GRID_3x3_coords).all()
    assert (coords_rot90 == np.array([(2, 0), (1, 0), (0, 0), (0, 2)])).all()
    assert (coords_rot90 == TEST_GRID_3x3_rot90_coords_aligned).all()

    coords, coords_rot180 = align_coords_by_values(
        TEST_GRID_3x3_values, TEST_GRID_3x3_coords,
        TEST_GRID_3x3_rot180_values, TEST_GRID_3x3_rot180_coords
    )
    assert (coords == TEST_GRID_3x3_coords).all()
    assert (coords_rot180 == np.array([(2, 2), (2, 1), (2, 0), (0, 0)])).all()
    assert (coords_rot180 == TEST_GRID_3x3_rot180_coords_aligned).all()

    coords, coords_rot270 = align_coords_by_values(
        TEST_GRID_3x3_values, TEST_GRID_3x3_coords,
        TEST_GRID_3x3_rot270_values, TEST_GRID_3x3_rot270_coords
    )
    assert (coords == TEST_GRID_3x3_coords).all()
    assert (coords_rot270 == np.array([(0, 2), (1, 2), (2, 2), (2, 0)])).all()
    assert (coords_rot270 == TEST_GRID_3x3_rot270_coords_aligned).all()


def test_rot_90deg():
    points = np.array([
        (0, 0),
        (1, 0),
        (0, 3),
        (2, 2),
    ])
    x, y = points[:, 0], points[:, 1]

    x1, y1 = rot_90deg(x, y, rot90=1)
    assert np.all(x1 == -y)
    assert np.all(y1 == x)

    x2, y2 = rot_90deg(x, y, rot90=2)
    assert np.all(x2 == -x)
    assert np.all(y2 == -y)

    x3, y3 = rot_90deg(x, y, rot90=3)
    assert np.all(x3 == y)
    assert np.all(y3 == -x)

    x4, y4 = rot_90deg(x, y, rot90=4)
    assert np.all(x4 == x)
    assert np.all(y4 == y)


def test_rotate_coords():
    # Coordinates are (row, col):
    cor_shift = np.array([-1, -1])

    # Rotate 0° (0 x 90°):
    assert np.all(TEST_GRID_3x3_coords == rotate_coords(TEST_GRID_3x3_coords, rot90=0))
    # assert np.all(TEST_GRID_3x3_rot90_coords_aligned_origin == rotate_coords(TEST_GRID_3x3_coords, rot90=1))
    # assert np.all(TEST_GRID_3x3_rot180_coords_aligned_origin == rotate_coords(TEST_GRID_3x3_coords, rot90=2))
    # assert np.all(TEST_GRID_3x3_rot270_coords_aligned_origin == rotate_coords(TEST_GRID_3x3_coords, rot90=3))


def test_calc_best_grid_rotation_result():

    avg_dist, rotation, global_shift = calc_best_grid_rotation_result(TEST_GRID_3x3, TEST_GRID_3x3_rot90)
    print(avg_dist, rotation, global_shift)
    assert avg_dist == 0
    assert rotation == 1  # Rotation is in units of 90° (counter-clockwise)

    avg_dist, rotation, global_shift = calc_best_grid_rotation_result(TEST_GRID_3x3, TEST_GRID_3x3_rot180)
    print(avg_dist, rotation, global_shift)
    # assert avg_dist == 0
    # assert rotation == 2  # Rotation is in units of 90° (counter-clockwise)

    avg_dist, rotation, global_shift = calc_best_grid_rotation_result(TEST_GRID_3x3, TEST_GRID_3x3_rot270)
    print(avg_dist, rotation, global_shift)
    # assert avg_dist == 0
    # assert rotation == 3  # Rotation is in units of 90° (counter-clockwise)

    avg_dist, rotation, global_shift = calc_best_grid_rotation_result(TEST_GRID_3x3, TEST_GRID_3x3)
    print(avg_dist, rotation, global_shift)
    assert avg_dist == 0
    assert rotation == 0  # Rotation is in units of 90° (counter-clockwise)


