# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""


"""

import tempfile
import yaml

from zepto_lims.configs.config import get_by_dot_notation, ZeptoAppConfig, ZeptoFileConfig


TEST_DATA_01 = {
    'first.second.third': 123,
    'one': {
        'two.three': 'abc',
        'other': {
            'item': 'value'
        }
    }
}

TEST_DATA_02 = {
    'first.second.third': 'fst',
    'one': {
        'other': {
            'item': 'othervalue'
        },
        'more': 'time',
    },
    'a.b.c': 'xyz',
}


def test_get_by_dot_notation():
    """ Test the functionality of get_by_dot_notation() """
    d = TEST_DATA_01
    assert get_by_dot_notation(d, 'first.second.third') == 123
    assert get_by_dot_notation(d, 'one.two.three') == 'abc'
    assert get_by_dot_notation(d, 'one.other.item') == 'value'


def test_zeptofileconfig_01():
    """ Test initializing ZeptoFileConfig with a dict data structure. """

    zfc = ZeptoFileConfig(TEST_DATA_01)
    assert zfc.get('first.second.third') == 123
    assert zfc.get('one.two.three') == 'abc'
    assert zfc.get('one.other.item') == 'value'


def test_zeptofileconfig_fileload(tmp_path):
    """ Test initializing ZeptoFileConfig with a filepath pointing to a yaml config file. """

    filepath = tmp_path / 'testconfig.yaml'
    with open(filepath, 'w') as f:
        yaml.safe_dump(TEST_DATA_01, f)

    zfc = ZeptoFileConfig(filepath)
    assert zfc.data
    assert zfc.filepath == filepath
    assert zfc.get('first.second.third') == 123
    assert zfc.get('one.two.three') == 'abc'
    assert zfc.get('one.other.item') == 'value'


def test_zeptoappconfig_01():
    zac = ZeptoAppConfig(runtime=TEST_DATA_01, user=TEST_DATA_02)
    assert zac.get('first.second.third') == 123  # from runtime config
    assert zac.get('one.two.three') == 'abc'  # from runtime config
    assert zac.get('one.more') == 'time'  # from user config
    assert zac.get('a.b.c') == 'xyz'  # from user config


