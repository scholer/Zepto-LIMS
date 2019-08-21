# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""

Creating an long-running "textual user interface" (TUI).
(This is different from both GUIs and CLIs).

OBS: The information below is only for *terminal user interfaces*.
See parent package for overviews on GUI and CLI packages.

Packages for making terminal user interfaces:

* curses, ncurses, unicurses, cursed, blessed.
* urwid - Has widgets, etc. This might be best option?
* npyscreen
* asciimatics
* prompt_toolkit -  for building a REPL like interface.
* curtsies - created for the bpython REPL.
* PyInquirer
* Console-menu - looks pretty good as well.
* Bullet
* Cooked Input
* Questionnaire




Curses:
* https://docs.python.org/3/library/curses.html
* Uses the ncurses C-library.
* Has many wrapper libraries, including:
    * unicurses
    * cursed - https://github.com/johannestaas/cursed
    * blessed - https://github.com/jquast/blessed
    * blessings - https://github.com/erikrose/blessings
*

Urwid:
* This is probably the most "fully-featured" textual user interface of the lot.
* http://urwid.org/
* https://github.com/urwid/urwid
* https://lwn.net/Articles/172998/



npyscreen:
* https://npyscreen.readthedocs.io/introduction.html


Python Prompt Toolkit:
* https://github.com/prompt-toolkit/python-prompt-toolkit


asciimatics
* https://github.com/peterbrittain/asciimatics


Console-menu:
* https://github.com/aegirhall/console-menu


PyInquirer:
* Mostly for CLIs,
* Based on Inquirer.js?
* Define a list of questions and appropriate answer types, prompt user and return answers.
*


Other packages that might be useful:

* Humanfriendly - for converting numbers to and from human-readable form, e.g. "16 GB".
* bpython - python REPL/interpreter, adds autocompletions and more.
* ptpython - yet another python REPL.
* clint.textui - has a bunch of methods for making nice-looking terminal UI.
* Gooey - turn a Python CLI program into a GUI.
* python-cli-ui - "Tools for better command line interfaces" (progress bar, etc)
    * https://github.com/TankerHQ/python-cli-ui
    * https://pypi.org/project/cli-ui/

Further refs:

* https://awesome-python.com/


"""
