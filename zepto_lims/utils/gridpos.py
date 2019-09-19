# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""

Module with functions for converting between different grid representations.

Representations include:

    grid - 2D matrix consisting of cells organized in rows and columns.
        Typically a list-of-lists, or a 2D numpy array (dtype=object).
        Each cell contains either zero or one elements, with empty cells
        represented by a NaN/None/null value (or alternatively 0, for interger-type matrices).
    val_pos_dict - map of {value: 'A01-pos'}
    (values, coords) tuple - where values is a list of element values (e.g. barcodes),
        and `coords` is the coordinate of each element, as a (n, 2) matrix (2d numpy array).
        This representation is used for calculating box rotation/translation, to check if
        the box has been rotated between scans, or if the scanner-grid was shifted/mis-aligned.

Conversion functions:

    grid <-> val_pos_dict:
        val_pos_dict_from_grid() - Convert a grid of scanned barcodes to barcode positions.

    grid <-> values_coords_tup:
        values_coords_tup_from_grid() - Convert a grid of scanned barcodes to barcode
                                        box-grid coordinates.

    val_pos_dict <-> values_coords_tup:
        values_coords_tup_from_val_pos()  - Convert barcode positions from the database to barcode
        val_pos_dict_from_values_coords()   box-grid coordinates (and back - not needed).


"""

from collections import OrderedDict
import numpy as np
import re


def alphabet_iterator(start='A', take=None):
    val = ord(start)
    # is_upper = start == start.upper()
    # end = val + take if take is not None else (ord('Z') if is_upper else ord('z'))
    n_taken = 0
    while True:
        yield chr(val)
        val += 1
        n_taken += 1
        if take is not None and n_taken >= take:
            raise StopIteration


def unique_elem_generator(vals):
    visited = set()
    for val in vals:
        if val not in visited:
            visited.add(val)
            yield val


def values_coords_tup_from_grid(grid, exclude=(None, np.NaN), unique=True) -> tuple:
    """ Convert a 2D grid with elements to a 2-tuple with (values, coords). """
    # Original implementation, using a numpy array directly.
    # Determine the number of non-None values:
    # Could use an ordered set for this:
    # linearized = [val for row in grid for val in row]
    # values = list(unique_elem_generator(linearized))
    # n_vals = len(values)
    # coords = np.ndarray(shape=(n_vals, 2))

    # Alternative implementation, using a dict (for uniqueness) and zip:
    if unique:
        elems = OrderedDict(
            (val, [row, col])
            for row, cvals in enumerate(grid) for col, val in enumerate(cvals)
            if val not in exclude
        )
        vals, coords = zip(*list(elems.items()))
    else:
        # Elements does not have to be unique:
        elems = [
            (val, [row, col])
            for row, cvals in enumerate(grid) for col, val in enumerate(cvals)
            if val not in exclude
        ]
        vals, coords = zip(*elems)
    return vals, np.array(coords)


def values_coords_tup_from_val_pos(
        val_pos_dict: dict,
        a01_coord: tuple = (0, 0),
        pos_regex: str = r"(?P<row>[A-z])(?P<col>\d+)",
        transpose: bool = False
) -> tuple:
    """ Convert a {val: pos-str} dict to (values, coords) tuple, where coords is a nx2 matrix.

    Args:
        val_pos_dict: Dict with {value: pos-str}. (Value typically being the unique tube barcode.)
        a01_coord: The coordinate for position "A01" in the grid.
        pos_regex: The regex used to parse numeric row and column indices from position strings (e.g. "A01").
        transpose: Whether to transpose the output, swapping rows and columns.

    Returns:
        A two-tuple of `(values, coords)`,
        where `values` is just the keys from the `val_pos_dict` (as list),
        and `coords` is a (n, 2)-shaped numpy array, i.e. a list of coordinates for each value,
        where n is the number of values.
    """
    row_offset, col_offset = a01_coord
    pos_regex = re.compile(pos_regex)

    def coord_from_pos(pos) -> tuple:
        match = pos_regex.match(pos)
        if match is None:
            raise ValueError(f"Could not parse grid coordinate from pos-string '{pos}'.")
        row, col = match.groups()
        row = ord(row) - ord('A') + row_offset
        col = int(col) - 1 + col_offset
        if transpose:
            return col, row
        else:
            return row, col
    # val_coord_dict = OrderedDict((val, coord_from_pos(pos)) for val, pos in val_pos_dict.items())
    values, coords = zip(*[(val, coord_from_pos(pos)) for val, pos in val_pos_dict.items()])
    coords = np.array(coords)
    return values, coords


def val_pos_dict_from_values_coords(
        values_coords: tuple,
        a01_coord: tuple = (0, 0),
        pos_fmt: str = "{row}{col:02}",
        transpose: bool = False
) -> dict:
    """ Convert a (values, coords) tuple to {val: pos-str} dict. """
    row_offset, col_offset = a01_coord
    if transpose:
        def pos_str(row: int, col: int) -> str:
            return pos_fmt.format(row=col, col=row)
    else:
        def pos_str(row: int, col: int) -> str:
            return pos_fmt.format(row=row, col=col)
    return {val: pos_str(row+row_offset, col+col_offset) for val, (row, col) in values_coords}


def val_pos_dict_from_grid(
        grid,
        pos_fmt: str = "{row}{col:02}",
        transpose: bool = False,
        exclude: tuple = (None, np.NaN),
        col_start: int = 1,
        row_start: str = 'A'
) -> dict:
    """ Convert a 2D grid to a {val: A01-pos} dict.

    Args:
        grid: 2D matrix, list of lists.
        pos_fmt: How to format each position (e.g. 'A1' or 'A01').
        transpose: Transpose columns and rows (flip the matrix 90°).
        exclude: Exclude grid-elements with these values (typically None).
        col_start: Start the grid at this column.
        row_start: Start the grid at this row.

    Returns:
        dict with {val: A01-pos} containing all values on the grid (excluding values in `exclude`).

    """
    if len(row_start) != 1:
        raise ValueError("val_pos_dict_from_grid() `row_start` must be a single character!")
    exclude = set(exclude)
    row_start_ord = ord(row_start)
    if transpose:
        def pos_str(row: int, col: int) -> str:
            return pos_fmt.format(row=chr(col + row_start_ord), col=row + col_start)
    else:
        def pos_str(row: int, col: int) -> str:
            return pos_fmt.format(row=chr(row + row_start_ord), col=col + col_start)

    return {value: pos_str(row=row_i, col=col_j)
            for row_i, rvals in enumerate(grid)
            for col_j, value in enumerate(rvals)
            if value not in exclude}


def pos_val_dict_from_grid(
        grid, pos_fmt="{row}{col:02}", transpose=False, exclude=(None, np.NaN),
        col_start=1, row_start='A'
) -> dict:
    """ Return a dict with {'A1-pos': value for each value in the 2D-matrix}.
    OBS: This representation should not be used for tube barcode tracker.
    Use the {val: pos} dict representation instead (since the barcode is used as element ID/key).

    Args:
        grid: 2D matrix, list of lists.
        pos_fmt: How to format each position (e.g. 'A1' or 'A01').
        transpose: Transpose columns and rows (flip the matrix 90°).
        exclude: Do not include grid elements with these values in the output pos_val_dict.
        col_start: Start the grid at this column.
        row_start: Start the grid at this row.

    Returns:
        dict with {'A1-pos': value for each value in the 2D-matrix}.

    """
    exclude = set(exclude)
    row_start_ord = ord(row_start)
    if transpose:
        def pos_str(row: int, col: int) -> str:
            return pos_fmt.format(row=chr(col + row_start_ord), col=row + col_start)
    else:
        def pos_str(row: int, col: int) -> str:
            return pos_fmt.format(row=chr(row + row_start_ord), col=col + col_start)

    return {pos_str(row=row_i, col=col_j): value
            for row_i, rvals in enumerate(grid)
            for col_j, value in enumerate(rvals)
            if value not in exclude}
