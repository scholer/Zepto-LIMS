# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""

Module for calculating transformation (rotation, translation) between scanned barcodes in a
discrete grid.

The discrete grid means we have points on a discrete plane with integer coordinates.
    A01 = (0,0), A02 = (0,1), B01 = (1,0), H08 = (8,8), ...
Alternatively, we can use an origin around E05, which is the center of a 9x9 grid,
which may make it easier to calculate rotations.


How to calculate transformation of two vectors:

* https://math.stackexchange.com/questions/180418/calculate-rotation-matrix-to-align-vector-a-to-vector-b-in-3d


How to calculate transformation of a set of points:

* https://stats.stackexchange.com/questions/186111/find-the-rotation-between-set-of-points
    * Kabsch Algorithm

Since we only have 90° rotations, it is perhaps easier to just do all four rotations,
and then calculate the best translation between the two grids.


"""

import numpy as np
# import snoop

from .gridpos import values_coords_tup_from_grid


def align_coords_by_values(values1, coords1, values2, coords2):
    # OBS: Need to make sure the newly-scanned coords are "aligned" with the old,
    # i.e. we can only use values that are in common, and coords must be in the same order:
    coords1_by_value = dict(zip(values1, coords1))
    coords2_by_value = dict(zip(values2, coords2))
    common_values_set = set(values1) & set(values2)
    common_values = [val for val in values1 if val in common_values_set]
    coords1_aligned = np.array([coords1_by_value[val] for val in common_values])
    coords2_aligned = np.array([coords2_by_value[val] for val in common_values])
    return coords1_aligned, coords2_aligned


def calc_best_grid_rotation_result(grid1, grid2):
    """ Calculate the best rotation for two discrete grids. """
    values1, coords1 = values_coords_tup_from_grid(grid1)
    values2, coords2 = values_coords_tup_from_grid(grid2)
    return calc_best_values_coords_rotation_result(values1, coords1, values2, coords2)


def calc_best_values_coords_rotation_result(values1, coords1, values2, coords2):
    """ This just aligns the coordinates of shared values before passing to calc_best_coords_rotation_result. """
    coords1_aligned, coords2_aligned = align_coords_by_values(values1, coords1, values2, coords2)
    return calc_best_coords_rotation_result(coords1_aligned, coords2_aligned)


def calc_best_coords_rotation_result(coords1: np.ndarray, coords2: np.ndarray) -> tuple:
    """ Calculate the optimal rotation to align one set of coordinates onto another set of coordinates.
    This assumes the coordinates are integer-values cooresponding to indices on a 2D grid (e.g. a box grid),
    such that the only valid rotations are multiples of 90° (a quarter revolution).

    This is used to determine if a scanned box was rotated compared to the last time it was scanned.
    In this use case, `coords1` would be the tube-barcode box-grid coordinates in the database,
    and `coords2` would be the grid coordinates for the barcodes that were just scanned.

    Args:
        coords1: Element coordinates, as a numpy matrix of shape (n, 2),
            where n is the number of values.
        coords2: Element coordinates for a different set of elements.
            It is important that the points are aligned.
            The i-th entry in grid1 should correspont to the i-th entry in grid2.

    Returns:
        A three-tuple of: (err, rot, trans)
        Where:
            err is the average error distance after performing rot and trans
            rot is the optimal rotation in integers of 90°,
            trans is the translation after rotating around the origin,

    OBS: You can use `zepto_lims.utils.gridpos.values_coords_tup_from_val_pos()` to convert
    position-strings ("A01" to coordinates).
    """
    # print(f"calc_best_grid_rotation_result():")
    # print(f"  coords2:")
    # print(coords1)
    # print(f"  coords1:")
    # print(coords2)
    rot_results = []
    for rotation in (0, 1, 2, 3):
        # Get rotated coordinates:
        coords2_rot = rotate_coords(coords2, rotation)
        # First, calculate global transformation:
        displacements = coords2_rot - coords1  # List of vectors shifting each point from from one coords to the other.
        global_shift = np.mean(displacements, axis=0)
        coords2_rt = coords2_rot - global_shift  # Rotated and shifted.
        displacements = coords2_rt - coords1
        # OK, we should probably just use centroids for both coords2 and coords1,
        # and eliminate one matrix subtraction, but this is slightly easier to understand.
        distances = np.linalg.norm(displacements, axis=1)  # Same as `asq = a*a; np.sqrt(asq[:, 0] + asq[:, 1])`
        avg_dist = np.mean(distances)
        if avg_dist == 0:
            # Perfect match:
            return avg_dist, rotation, global_shift
        rot_results.append((avg_dist, rotation, global_shift))
    # No perfect overlaps (e.g. one or more of the tubes have been moved around).
    # Just return the best one:
    return sorted(rot_results)[0]  # Result with lowest avg_dist is sorted first


def rotate_coords(coords, rot90):
    """ Rotate coordinates by an integer of 90° counter-clockwise.
    coords are (row, col), which visually corresponds to (y, x),
    and for coords, the y-axis is inverted (down is positive y).
    so we need this adapter function to convert the two.
    """
    row, col = coords[:, 0], coords[:, 1]
    # coords are in (row, col), which corresponds to (y, x) not (x, y) !
    xr, yr = rot_90deg(x=col, y=row, rot90=rot90)
    rot = np.empty_like(coords)
    rot[:, 1], rot[:, 0] = xr, yr
    return rot


def rotate_points(points, rot90):
    """ Rotate points, an array of (x, y) positions.

    Args:
        points: A matrix with shape (n, 2) specifying n points on a 2D plane.
        rot90: The rotation, in multiples of 90° (i.e. the number of quater-turns).

    Returns:
        points, after rotation.

    """
    rot = np.empty_like(points)  # np.asarray() will return input if already array
    rot[:, 1], rot[:, 0] = rot_90deg(x=points[:, 0], y=points[:, 1], rot90=rot90)
    return rot


def rot_90deg(x, y, rot90):
    """ Rotate points by an integer of 90°.

    Args:
        x: x-coordinate.
        y: y-coordinate.
        rot90: Rotation, in units of 90° (integer).

    Returns:
        (x, y) after rotation.
    """
    rot90 = rot90 % 4
    assert rot90 in (0, 1, 2, 3)
    if rot90 == 0:
        # No rotation; just return grid unchanged.
        return x, y
    if rot90 == 1:
        # Rotation 90° counter-clockwise.
        # (2, 1) -> (-1, 2)
        # x-values -> y-values
        # y-values -> negative x-values
        return -y, x
    if rot90 == 2:
        # Rotation 180° counter-clockwise.
        # (2, 1) -> (-1, -2)
        # x-values -> negative x-values
        # y-values -> negative y-values
        return -x, -y
    if rot90 == 3:
        # Rotation 270° counter-clockwise = 90° clockwise.
        # (2, 1) -> (1, -2)
        # x-values -> negative y-values
        # y-values -> x-values
        return y, -x
