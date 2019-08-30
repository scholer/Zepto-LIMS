# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
r"""

Settings & configuration:
--------------------------


Overview, storage formats:

* JSON
    * Standard JSON does not support comments. But some packages, e.g. `python-rapidjson` DOES support comments.
    * rapidjson also supports trailing commas, useful for re-organizing lines.
* YAML
    * YAML by default allows comments.
    * Alternative parser reyaml (https://github.com/ralienpp/reyaml) supports inline comments and custom indentation.
    * Also strictyaml (https://hitchdev.com/strictyaml/) for stricter, type-safe YAML parsing with forced schema.
* TOML
* INI
    * OBS: Python's built-in configparser module uses INI.
    * "TOML is not compatible with ConfigParser." - https://github.com/toml-lang/toml/issues/594
* XML (no.)
* HOCON
    * Supports '#' and '//' for comments.
    * Supports advanced features: Self-referencing, includes, merges,
* HCL (HashiCorp Configuration Language)


Ways of specifying config settings:

* Code defaults (should be avoided).
* Default settings file.
* User settings file.
* Environment variables.
* Command line arguments (e.g. as a dedicated `--config key=value`).


Feature: Save/persist config settings:

* Option 1: Don't bother with in-app settings persistence.
    It is much easier to just let the user edit config files, environment variables, and command line arguments.


Feature checklist:

* Load config from YAML and/or TOML (my preferred config formats).
* Load config keys from environment variables.
    * Support for .env files?
    * Environment variable data type conversion (e.g. str -> int).
* Easily merge configs.
* OBS: Loading config from command line arguments is fairly easy if you use
    `--config key=value`. Just use click's `multiple=True` (to get config list), then
    `cmd_args_config = dict(config)`.
* Nesting support.
* dot-notation, e.g. `config["section.subsection.key"]` is equivalent to
    `config["section"]["subsection"]["key"]`.


## Settings/configuration - implementation options and alternatives:

Overview, config objects:

1. Just use a plain dict.
2. `configparser.Configparser` from the standard library.
3. Config class from your Labfluence project.
4. One of the packages below:






Python Config packages:

* ConfigParser:
    * Only supports INI format (AFAIK).
    *
* Environ-Config:
    * https://github.com/hynek/environ-config
* DynaConf:
    * https://dynaconf.readthedocs.io/en/latest/
    * https://github.com/rochacbruno/dynaconf
    * Looks for config files in folder `ROOT_PATH_FOR_DYNACONF`
    * SETTINGS_FILE_FOR_DYNACONF defaults to `settings.{py|toml|json|ini|yaml}` and `.secrets.{py|toml|json|ini|yaml}`
    * "The recommended file format is TOML but you can choose to use any of .{py|toml|json|ini|yaml}."
    * Rather extensive and complex configuration setup.
    * Seems focused towards webapps, rather than generic GUI/CLI apps.
* Configurator:
    * YAML, TOML, JSON built-in, extensible to other formats.
    * 11 Github stars.
    * Last updated May 2019; project started 2011.
    * Supports loading environment variables.
    * Recommends `voluptuous` for config data validation.
    * https://pypi.org/project/configurator/
    * https://github.com/Simplistix/configurator
    * https://configurator.readthedocs.io/en/latest/
* Read-Settings:
    * https://readsettings.richie-bendall.ml/
    * https://github.com/readsettings/readsettings
    * 8 Github stars,
    * Last updated June 2019.
* ConfigObj:
    * https://configobj.readthedocs.io/en/latest/configobj.html
    * INI format only.
* dotenv
    * https://pypi.org/project/python-dotenv/
    * "Reads the key,value pair from .env file and adds them to environment variable. It is great for managing
        app settings during development and in production using 12-factor principles."
* envdir:
    * https://pypi.org/project/envdir/
    * > "envdir runs another program with a modified environment according to files in a specified directory."
* cfg_load
    * https://github.com/MartinThoma/cfg_load
    * 10 github stars
    * Last update August 2019.
* environ-config
    * https://github.com/hynek/environ-config
    * 85 github stars, updated June 2019.
* file-config:
    * https://github.com/stephen-bunn/file-config
    * > "Attrs-like file config definitions inspired from environ-config."
    * 4 Github stars
    * Updated June 2019.
* confight
    * https://github.com/Avature/confight
    * 6 Github stars.
    * Updated March 2019.
    * Pretty Linux-oriented.
* parse_it
    * https://github.com/naorlivne/parse_it
    * 54 github stars
    * Updated August 2019.
* environs
    * https://github.com/sloria/environs
    * > "simplified environment variable parsing."
    * 275 github stars,
    * Last update August 2019.
* pyhocon
    * https://github.com/chimpler/pyhocon
    * > "HOCON parser for Python".
    * 251 github stars,
    * Last update April 2019.
    * Perhaps the most advanced config format.
* pyhcl
    * https://github.com/virtuald/pyhcl
    * > "HCL is a configuration language. pyhcl is a python parser for it."
    * 184 github stars.
    * Last update march 2019.
* reconfigure
    * > "Config-file-to-Python mapping library (ORM)."
    * http://reconfigure.readthedocs.org/
    * https://github.com/Eugeny/reconfigure  (125 stars)
* anyconfig:
    * https://github.com/ssato/python-anyconfig
    * https://pypi.org/project/anyconfig/
    * https://python-anyconfig.readthedocs.io/en/latest/
    * Project started Oct 2015, latest release Apr 2019.
    * Supports: JSON, INI (configparser), pickle, xml, properties, shellvars, YAML, TOML (with dependencies installed).
    * See also:
        * https://github.com/tomtom-international/vault-anyconfig -
            "Integrates anyconfig with the HVAC Vault client to mix Vault secrets into configuration file contents."
* prettyconf
    * > "A extensible library for Settings/Code separation."
    * https://pypi.python.org/pypi/prettyconf
    * https://github.com/osantana/prettyconf
    * > "Inspired by python-decouple."
* python-decouple
    * https://github.com/henriquebastos/python-decouple
    * > "Strict separation of config from code."
    * > "Decouple supports both .ini and .env files."
* confuse
    * > "painless YAML config files for Python."
    * https://pypi.org/project/confuse/
    * https://confuse.readthedocs.io/en/latest/
    * https://github.com/beetbox/confuse
    * Usage:
        * `config = confuse.Configuration('MyGreatApp', __name__)`
        * `value = config['foo'][2]['bar'].get()`
    * Search paths:
        * OS X: `~/.config/app` and `~/Library/Application Support/app`.
        * Other Unix: `$XDG_CONFIG_HOME/app` and `~/.config/app`.
        * Windows: `%APPDATA%\app` where the `APPDATA` environment variable falls back to
            `%HOME%\AppData\Roaming` if undefined.
    * Supports redaction of sensitive key-values, so they are not included when the config is dumped.
* environ-config
    * https://github.com/hynek/environ-config
    * > "Configuration with env variables for Python."
    * > "environ-config allows you to configure your applications using environment variables – as recommended
        in The Twelve-Factor App methodology – with elegant, boilerplate-free, and declarative code."
    * Features:
        * Declarative & boilerplate-free.
        * Nested config from flat env variable names.
        * Default & mandatory values: enforce configuration structure without writing a line of code.
        * Helpful debug logging that will tell you which variables are present and what environ-config is looking for.
        * Built on top of attrs which gives you data validation and conversion for free.
        * Pluggable secrets extraction. Ships with:
        * HashiCorp Vault support via envconsul.
        * INI files, because secrets in env variables are icky.
        * Pass any dict into environ.to_config(AppConfig, {"your": "config"}) instead of loading from the environment.
        * Built in dynamic help documentation generation via environ.generate_help.
* rhea
    * https://github.com/polyaxon/rhea
    * `rhea_config = rhea.Rhea.read_configs([os.environ, 'file1.json', 'file2.yaml', 'override.json', {'foo': 'bar'}])`
    * `rhea_config.get_int/get_float/get_boolean(key, default=default, is_list=True/False)`
    * > "Efficient environment variables management and typing for python."
* figgypy
    * https://github.com/theherk/figgypy
    * > "A simple configuration parser for Python."
    * `cfg = figgypy.set_config(conf_file)`
    * `cfg.get_value('somevalue', optional_default)`
    * Uses gnupg to encode/decode secrets.
    * Uses seria to serialize and deserialize configs (JSON/YAML/XML)
* gconfigs
    * > "gConfigs - Config and Secret parser."
    * https://github.com/douglasmiranda/gconfigs
        * 44 github stars.
        * Last commit Apr 2019.
    * Read configs from:
        * Environment Variables
        * Local Mounted Configs and Secrets
        * .env (dotenv) files
* HiYaPyCo:
    * > "HiYaPyCo - A Hierarchical Yaml Python Config."
    * > "A simple python lib allowing hierarchical overlay of config files in YAML syntax,
        offering different merge methods and variable interpolation based on jinja2."
    * > "The goal was to have something similar to puppets hiera merge_behavior: deeper for python."
    * Supports Jinja2 templating: `second: again {{ first }}`.
    * Requires: PyYAML, Jinja2.
    * https://github.com/zerwes/hiyapyco
        * 38 github stars.
    * https://pypi.org/project/HiYaPyCo/
    * Inspired by Puppet Hiera.
        * https://github.com/voxpupuli/puppet-hiera
        * https://github.com/puppetlabs/hiera
        * https://puppet.com/docs/puppet/5.2/hiera_intro.html
* himl
    * > "A hierarchical yaml config in Python."
    * https://pypi.org/project/himl/
    * https://github.com/adobe/himl (10 github stars)
* layered-yaml-attrdict-config:
    * > "YAML-based configuration module with object-attribute style access, ordering and recursive ops."
    * https://github.com/mk-fg/layered-yaml-attrdict-config  (19 stars)
* conff
    * > "Simple configuration parser with evaluator library for Python."
    * https://github.com/kororo/conff  (19 github stars)
* wasserstoff
    * > "Store your configurations for applications in JSON, INI and text files and dynamically load ones to the scope of object."
    * > "Wasserstoff - is a library that help you store your configurations for applications in JSON, INI and text files."
    * https://github.com/lk-geimfari/wasserstoff  (18 github stars)
        * Latest commit  Oct 31, 2017.
* plaster
    * > "Application config settings abstraction layer."
    * https://github.com/Pylons/plaster  (14 stars)
    * > "plaster is a loader interface around multiple config file formats."
    * https://docs.pylonsproject.org/projects/plaster/en/latest/
    *
* profig:
    * > "A straightforward configuration library for Python."
    * https://github.com/dhagrow/profig  (15 stars)
    * https://pypi.org/project/profig/
    * https://bitbucket.org/dhagrow/profig/src/default/
    * Features:
        * Extensible input/output formats.
        * Built-in support for INI files and the Windows registry.
        * Preserves ordering and comments of INI files.
* hb-config:
    * > "hb-config: easy to configure your python project especially Deep Learning experiments."
    * https://github.com/DongjunLee/hb-config  (18 github stars)
* goodconf:
    * > "Transparently load variables from environment or JSON/YAML file."
    * https://github.com/lincolnloop/goodconf  (17 github stars)
        * Latest commit Apr 2019.
    * > "I took inspiration from logan (used by Sentry) and derpconf (used by Thumbor)."
    * > "I don't like working with environment variables. I prefer a single structured file which is
        explicitly read by the application."
* derpconf:
    * "derpconf abstracts loading configuration files for your app. derpconf was extracted from thumbor."
    * https://github.com/globocom/derpconf  (22 stars)
        * Latest commit Feb 2019.
* settei:
    * > "Configuration utility for common Python applications and services."
    * > "Configuration utility for common Python applications and services.
        FYI, "settei" (設定) means settings in Japanese. :)"
    * https://settei.readthedocs.io/
    * https://github.com/spoqa/settei  (12 github stars)
    *
* python-config2
    * > "Python environment configuration simplified - highly inspired by `node-config`."
    * https://pypi.org/project/config2
    * https://github.com/grimen/python-config2 (7 github stars)
* theconf
    * > "Python Package for Managing Configurations."
    * https://github.com/wbaek/theconf  (7 github stars)
    * Lots of Chinese/Korean in the commits.
* python-json-config
    * > "A config library for python."
    * > "This library allows to load json configs and access the values like members (i.e., config.server.port
        instead of config['server']['port']), validate the data types of fields and transform the values of fields.
    * https://github.com/janehmueller/python-json-config
        * 5 github stars
    * Can merge with environment vars (using prefix).
    * Has `transformers`, which can be used to convert values. P.t. only `to_timedelta`.
* nativeconfig
    * > "Cross-platform Python package that uses native mechanisms such as Windows Registry or
        NSUserDefaults to store user settings."
    * https://github.com/GreatFruitOmsk/nativeconfig  (4 stars)
* octoconf
    * > "Multi-profile supported, flexible config library."
    * https://github.com/andras-tim/octoconf  (4 stars)
* os-config
    * > "Python config object."
* donfig:
    * > "Python library for configuring a package including defaults, env variable loading, and yaml loading."
    * https://donfig.readthedocs.io/en/latest/
    * https://github.com/pytroll/donfig  (17 stars)
    * `conda install -c conda-forge donfig`
* konfetti
    * > "Python configuration management system with an intuitive API."
    * > "konfetti is a Python configuration management library that simplifies the process of setting up your
        application to run on your company’s infrastructure."
    * https://github.com/kiwicom/konfetti  (20 stars)
* settings_parser
    * Load and parse user settings.
    * https://github.com/pedvide/settings_parser  (0 stars)
        * Last update 2017.
* app_settings
    * > "YAML for application configuration, lite version (inspired by Ruby gem "config")."
    * > "Simplify usage of YAML files for application configuration."
    * https://github.com/ivdunin/app_settings  (0 stars).
* py-config:
    * > "Python Application Configuration. Py-config organizes hierarchical configurations for your app deployments."
    * https://github.com/Maples7/py-config  (1 star)
* config42
    * > "Configuration manager for cloud native application, support configuration stored in memory, in files, in databases."
    * > "The config-manager package is a complete configuration reader and manager."
    * https://pypi.org/project/config42/
    * https://github.com/yurilaaziz/config42  (5 stars)
* configloader:
    * > "Python dictionary that supports common app configuration-loading scenarios."
    * > "ConfigLoader is a Python dictionary subclass that provides convenience methods for common app
        configuration-loading scenarios, inspired by flask.Config."
    * Load from: Python modules, classes or objects, JSON files, YAML files, Environment variables.
    * https://configloader.readthedocs.io
    * https://github.com/adblair/configloader  (7 stars)
* ycsettings
    * > "A module for handling app settings."
    * https://github.com/skylander86/ycsettings  (2 stars)
        * Last update 2017.
* appjsonsettings:
    * > "A simple python package for easy application settings in JSON format."
    * https://github.com/jacklinquan/appjsonsettings  (1 star)
* kivy.config:
    * https://kivy.org/doc/stable/api-kivy.config.html#
* climatecontrol
    * > "Python library for loading app configurations from files and/or namespaced environment variables."
    * https://pypi.org/project/climatecontrol/
    * https://github.com/daviskirk/climatecontrol  (2 github stars)
* tweak
    * > "Python application configuration engine."
    * https://github.com/kislyuk/tweak  (7 stars)
    * Environment vars, argparse.Namespace, YAML.
    * Load from:
        * Site-wide configuration source, /etc/NAME/config.(yml|json)
        * User configuration source, ~/.config/NAME/config.(yml|json)
        * Any sources listed in the colon-delimited variable NAME_CONFIG_FILE


### Other packages (including non-python):

* munch:
    * > "A Munch is a Python dictionary that provides attribute-style access (a la JavaScript objects)."
    * https://github.com/Infinidat/munch  (301 github stars)

* pocket_protector:
    * > "People-centric secret management system, built to work with modern distributed version control systems."
    * https://github.com/SimpleLegal/pocket_protector  (26 stars)

* cfgdiff
    * > "diff(1) all your configs."
    * https://github.com/evgeni/cfgdiff  (20 github stars).
    *

* javaproperties:
    * > "Python library for reading & writing Java .properties files."
    * https://github.com/jwodder/javaproperties

* jsonnet:
    * > "Jsonnet - The data templating language."
    * http://jsonnet.org

* crudini
    * > "A utility for manipulating ini files."
    * https://github.com/pixelb/crudini

* poyo:
    * > "A lightweight YAML Parser for Python."
    * https://github.com/hackebrot/poyo

* app-dirs:
    * https://pypi.org/project/appdirs/
    * https://github.com/ActiveState/appdirs
    * > A small Python module for determining appropriate platform-specific dirs, e.g. a "user data dir".
    * Started as a fork of applib.
    * Provides the following:
        * user data dir (user_data_dir)
        * user config dir (user_config_dir)
        * user cache dir (user_cache_dir)
        * site data dir (site_data_dir)
        * site config dir (site_config_dir)
        * user log dir (user_log_dir)
    * Usage:
        * Either use a persistent AppDirs object:
            * `dirs = AppDirs("SuperApp", "Acme")`
            * `dirs.user_data_dir`  # property
        * Or use any of the module-level functions:
            * `appdirs.user_data_dir("App-name", "Author")

* applib
    * "Cross-platform application utilities in Python."
    * https://pypi.org/project/applib/
    * Last release 2011.

* pytablewriter
    * > "pytablewriter is a Python library to write a table in various formats: CSV / Elasticsearch
        / HTML / JavaScript / JSON / LaTeX / LDJSON / LTSV / Markdown / MediaWiki / NumPy / Excel /
        Pandas / Python / reStructuredText / SQLite / TOML / TSV."
    * https://pytablewriter.rtfd.io/
    * https://github.com/thombashi/pytablewriter


* dotfiles:
    * A random person's personal configuration files.
    * https://github.com/ebzzry/dotfiles

* Pure-Config:
    * Scala.
    * https://github.com/pureconfig/pureconfig

* SyncSettings
    * https://github.com/mfuentesg/SyncSettings
    * > "Sync Settings - The cross-platform solution to keep Sublime Text configuration synchronized."
    * Uses Github GIST to sync the config.

* toml
    * > "Python lib for TOML."
    * https://github.com/uiri/toml  (463 stars)

* pytoml
    * > "A TOML-0.4.0 parser/writer for Python."
    * https://github.com/avakar/pytoml  (128 stars)

* tomlkit
    * > "Style-preserving TOML library for Python."
    * https://github.com/sdispater/tomlkit (128 stars - also).

* remarshal
    * > "Convert between JSON, MessagePack, TOML, and YAML."
    * https://github.com/dbohdan/remarshal  (343 stars)
    *

seria:
    * https://github.com/rtluckie/seria
    * > "

Refs:

* https://12factor.net/config
* https://12factor.net
    * > "The twelve-factor app is a methodology for building software-as-a-service apps."
* https://diogomonica.com/2017/03/27/why-you-shouldnt-use-env-variables-for-secret-data/
* https://hackernoon.com/4-ways-to-manage-the-configuration-in-python-4623049e841b
* https://wiki.python.org/moin/ConfigParserShootout
* https://martin-thoma.com/configuration-files-in-python/
* https://www.reddit.com/r/Python/comments/89c9b5/what_config_file_format_do_you_prefer/
* https://github.com/topics/configuration?l=python
* https://flask.palletsprojects.com/en/1.1.x/config/
* https://kivy.org/doc/stable/api-kivy.config.html
* https://www.hackerearth.com/practice/notes/samarthbhargav/a-design-pattern-for-configuration-management-in-python/
* https://hackersandslackers.com/simplify-your-python-projects-configuration/
* https://www.python.org/dev/peps/pep-0518/#other-file-formats

"""
