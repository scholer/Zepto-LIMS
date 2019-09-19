# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""


"""
import numpy as np

TEST_GRID_3x3_empty = [
    [None, None, None],
    [None, None, None],
    [None, None, None],
]
TEST_GRID_3x3 = [
    ['First', 'Second', 'Third'],
    [None, None, None],
    [None, None, 'Fourth'],
]
TEST_GRID_3x3_values = ('First', 'Second', 'Third', 'Fourth')
TEST_GRID_3x3_coords = np.array([(0, 0), (0, 1), (0, 2), (2, 2)])
TEST_GRID_3x3_valpos = dict(zip(
    ('First', 'Second', 'Third', 'Fourth'),
    ['A01', 'A02', 'A03', 'C03']
))
TEST_GRID_3x3_rot90 = [
    ['Third', None, 'Fourth'],
    ['Second', None, None],
    ['First', None, None],
]
TEST_GRID_3x3_rot90_values = ('Third', 'Fourth', 'Second', 'First')
TEST_GRID_3x3_rot90_coords = np.array([(0, 0), (0, 2), (1, 0), (2, 0)])
TEST_GRID_3x3_rot90_coords_aligned = np.array([(2, 0), (1, 0), (0, 0), (0, 2)])
TEST_GRID_3x3_rot90_coords_aligned_origin = np.array([(0, 0), (-1, 0), (-2, 0), (-2, 2)])
TEST_GRID_3x3_rot90_valpos = {'Third': 'A01', 'Fourth': 'A03', 'Second': 'B01', 'First': 'C01'}
TEST_GRID_3x3_rot180 = [
    ['Fourth', None, None],
    [None, None, None],
    ['Third', 'Second', 'First'],
]
TEST_GRID_3x3_rot180_values = ('Fourth', 'Third', 'Second', 'First')
TEST_GRID_3x3_rot180_coords = np.array([(0, 0), (2, 0), (2, 1), (2, 2)])
TEST_GRID_3x3_rot180_coords_aligned = np.array([(2, 2), (2, 1), (2, 0), (0, 0)])
TEST_GRID_3x3_rot180_coords_aligned_origin = np.array([(0, 0), (-0, -1), (-0, -2), (-2, -2)])
TEST_GRID_3x3_rot270 = [
    [None, None, 'First'],
    [None, None, 'Second'],
    ['Fourth', None, 'Third'],
]
TEST_GRID_3x3_rot270_values = ('First', 'Second', 'Fourth', 'Third')
TEST_GRID_3x3_rot270_coords = np.array([(0, 2), (1, 2), (2, 0), (2, 2)])
TEST_GRID_3x3_rot270_coords_aligned = np.array([(0, 2), (1, 2), (2, 2), (2, 0)])
TEST_GRID_3x3_rot270_coords_aligned_origin = np.array([(0, 0), (-1, 0), (-2, 0), (-2, 2)])

TEST_GRID_3x3_mod1 = [
    ['First', 'Second', None],
    [None, None, 'tube1'],
    [None, None, 'Fourth'],
]

# Make all numpy arrays immutable to prevent accidental mistakes:
for array in (
        TEST_GRID_3x3_coords,
        TEST_GRID_3x3_rot90_coords,
        TEST_GRID_3x3_rot90_coords_aligned,
        TEST_GRID_3x3_rot90_coords_aligned_origin,
        TEST_GRID_3x3_rot180_coords,
        TEST_GRID_3x3_rot180_coords_aligned,
        TEST_GRID_3x3_rot180_coords_aligned_origin,
        TEST_GRID_3x3_rot270_coords,
        TEST_GRID_3x3_rot270_coords_aligned,
        TEST_GRID_3x3_rot270_coords_aligned_origin
):
    array.flags.writeable = False
