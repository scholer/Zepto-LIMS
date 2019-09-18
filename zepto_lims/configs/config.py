# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""

See package __init__.py file for general discussion of configuration,
config packages, and how to implement a config class.

"""

import os
from collections import OrderedDict
import pathlib
import yaml

from .config_paths import CONFIG_PATH_CANDIDATES, get_existing_config_path


def get_by_dot_notation(dictionary, key, default=None):
    """ Get key from dict using dot notation, recursively.

    E.g.
        dictionary['first.second.third']
    is equivalent to
        dictionary['first']['second']['third'],
    unless 'first.second.third' actually exists.

    Args:
        dictionary:
        key:
        default:

    Returns:
        The value identified by key

    """
    if key in dictionary:
        return dictionary[key]
    if '.' in key:
        first, remaining = key.split('.', 1)
        if first in dictionary:
            return get_by_dot_notation(dictionary[first], remaining)
    return default


class ZeptoAppConfig:
    """ App aggregator config class, combining multiple distinct configs.

    ZeptoAppConfig has several features:

    1. It contains several prioritized sub-configs.
        When a key is requested, the sub-configs are tried in order, returning the first non-None value.
        This makes it possible to have e.g. a global/system/default config,
        which is overridden by a user-level config,
        which is overridden by a runtime config (containing e.g. command line arguments).

    2. It supports dot-notation fallback, e.g.
        ZeptoAppConfig.get('section.subsection.key')
        will first try if any of the following exists for each of the sub-configs, in order:
            ['section.subsection.key']
            ['section']['subsection.key']
            ['section']['subsection']['key']

    """

    def __init__(
            self,
            runtime=None,
            user=None,
            system=None,
            default=None,
            use_standard_configs=('runtime', 'user', 'system', 'default'),
            readonly_configs=('system', 'default'),
            **other_configs
    ):
        self.configs = OrderedDict(**{
            name: ZeptoFileConfig(val, name=name, readonly=(name in readonly_configs))
            for name, val in other_configs.items()
        })
        for name, val in (
                ('runtime', runtime),
                ('user', user),
                ('system', system),
                ('default', default),
        ):
            if use_standard_configs and name in use_standard_configs:
                if val is None:
                    val = get_existing_config_path(name=name)
                if val is None:
                    print(f"OBS: No filepath defined for '{name}' config, skipping...")
                    continue
                # val can be either a filepath, a data-dict, or a (filepath, data-dict) tuple.
                self.configs[name] = ZeptoFileConfig(val, name=name, readonly=(name in readonly_configs))

    def get_containing_config(self, key, skip_none=True):
        for name, cfg_obj in self.configs.items():
            val = cfg_obj.get(key, default=None)
            if val is not None or not skip_none:
                return name, cfg_obj
        else:
            return None

    def get(self, key, default=None, skip_none=True):
        for name, cfg_obj in self.configs.items():
            val = cfg_obj.get(key, default=None)
            if val is not None or not skip_none:
                break
        else:
            val = None

        return val if val is not None else default

    def print_configs(self):
        print("Configs:")
        for name, zfc in self.configs.items():
            print(f" - {name} [{zfc.filepath}]: {len(zfc.data)} keys")


class ZeptoFileConfig:
    """ A "sub-config" class for use by ZeptoAppConfig.

    A ZeptoFileConfig is composed of three things: a name, a data (dict), and an optional filepath.

    If the filepath is set, it can be used to load data from, and save data to.

    """

    def __init__(self, *args, data=None, filepath=None, name=None, readonly=False):
        print(f"{ZeptoFileConfig.__class__}:\n     args = {args}\n     data = {data}\n filepath = {filepath}\n     name = {name}")
        if isinstance(args[0], (tuple, list)):
            args = args[0]
        for arg in args:
            if isinstance(arg, dict):
                data = arg
            elif isinstance(arg, (str, pathlib.Path)):
                filepath = arg
            else:
                raise TypeError(f"Unknown argument type {type(arg)} for arg {arg}.")
        if data is None and filepath is None:
            raise ValueError(f"{self.__class__ } called with no data or filepath.")
        self.data = data
        self.filepath = filepath
        self.file_stat_on_load = None
        self.name = name
        self.readonly = readonly
        if data is None:
            self.load_from_file()

    def load_from_file(self, filepath=None, format=None):
        if filepath is None:
            filepath = self.filepath
        if filepath is None:
            raise RuntimeError(
                f"{self.__class__ } '{self.name}' doesn't have any filepath and none given; cannot load.")
        # TODO: Support multiple file formats (YAML, JSON, TOML)
        with open(filepath) as fp:
            self.data = yaml.safe_load(fp)
            self.file_stat_on_load = pathlib.Path(filepath).stat()
        return self.data

    def get(self, key, default=None):
        return get_by_dot_notation(self.data, key, default=default)

    def __str__(self):
        return f"{type(self).__class__} '{self.name}' [{self.filepath}] containing {len(self.data)} keys."
