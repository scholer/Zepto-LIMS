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
    try:
        paths = CONFIG_PATH_CANDIDATES[platform][name]
    except KeyError as exc:
        print(f"NOTICE: No config path candidates for config '{name}': {exc}")
        return None
    paths = [pathlib.Path(path) for path in paths]
    path = next((path for path in paths if path.exists()), None)
    if path is None and create_default:
        try:
            path = pathlib.Path(CONFIG_PATH_CANDIDATES[platform][name][0])
        except (KeyError, IndexError) as exc:
            print(f"NOTICE: No config path candidates for config '{name}': {exc}")
            return None
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
    return path




