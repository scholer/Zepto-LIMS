# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""

See package __init__.py file for general discussion of configuration,
config packages, and how to implement a config class.

Module with config path candidates.


"""

import sys
import os
import pathlib


# TODO: Use the `appdirs` package to find good default config file locations.
CONFIG_PATH_CANDIDATES = {
    'win32': {
        'user': [
            '~/.config/zepto_lims/zepto_lims.yaml',
        ]
    }
}


def get_existing_config_path(name='user', platform=None, create_default=True):
    """ Find existing config filename, for a given config name and platform.

    For example, the 'user' config on Windows would be a different filepath
    than the 'user' config on macOS, or the 'system' config on Windows.

    """
    if platform is None:
        platform = sys.platform
    paths = CONFIG_PATH_CANDIDATES[platform][name]
    paths = [pathlib.Path(path) for path in paths]
    path = next((path for path in paths if path.exists()), None)
    if path is None and create_default:
        path = pathlib.Path(CONFIG_PATH_CANDIDATES[platform][name][0])
        path.parent.mkdir(parents=True, exist_ok=True)
    return path




