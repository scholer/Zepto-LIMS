# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""


Packages for taking user-input from the command line:

* bullet - Windows not currently supported.
* questionnaire
* prompt_toolkit
*

"""

from .tubetracker_app_base import TubeTrackerAppBase
from zepto_lims.configs.config import ZeptoAppConfig
from zepto_lims.configs.default_config import DEFAULTS


def tubetracker_questionaire_cli():
    """ A basic CLI that repeatedly asks the user what he would like to do and then does that. """

    config = ZeptoAppConfig(default=DEFAULTS)
    config.print_configs()
    app = TubeTrackerAppBase(config=config)

    while True:

        print("""
    Available actions:
    
        1. Scan tubes in box.
        2. Add new box.
        0. Quit.
    
    """)

        answer = input("What would you like to do?  ").lower()

        if not answer:
            continue

        if answer[0] in ('1', 's'):
            app.scan_and_update_box()
        elif answer[0] in ('2', 'a'):
            boxname = input("Enter name for new box:  ")
            if boxname:
                app.add_box(boxname)
        elif answer[0] in ('0', 'q', 'e'):
            return
        else:
            print("\nAnswer not recognized.\n")
