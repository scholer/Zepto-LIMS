# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""


"""

BOXES_DATA_01 = """
boxname
box1
box2
box3
"""
TUBES_DATA_CSV_3x3 = """
boxname,barcode,pos
box1,First,A01
box1,Second,A02
box1,Third,A03
box1,Fourth,C03
box2,tube1,A01
box2,tube2,B01
box2,tube3,A03
box2,tube4,A08
box2,tube9,D08
"""
TUBES_DATA_CSV_3x3_rot90 = """
boxname,barcode,pos
box1,First,C01
box1,Second,B01
box1,Third,A01
box1,Fourth,A03
"""
TUBES_DATA_CSV_MULTI = """
boxname,barcode,pos
box1,First,A01
box1,Second,A02
box1,Third,A03
box1,Fourth,C03
box2,tube1,A01
box2,tube2,B01
box2,tube3,A03
box2,tube4,A08
box2,tube9,D08
box3,One,A01
box3,Two,A02
"""
# Make sure to read with `keep_default_na=False`, if you want "N/A" as text str, not float.NaN.
TUBES_DATA_CSV_MULTI_MOD1 = """
boxname,barcode,pos
box1,First,A01
box1,Second,A02
(missing),Third,N/A
box1,Fourth,C03
box1,tube1,B03
box2,tube2,B01
box2,tube3,A03
box2,tube4,A08
box2,tube9,D08
box3,One,A01
box3,Two,A02
"""
