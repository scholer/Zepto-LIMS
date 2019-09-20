# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>
"""


"""

from setuptools import setup
import os

# Note: Make sure to use `pip -v` when pip-installing, so you can check what is being installed.

PROJECT_ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
try:
    with open(os.path.join(PROJECT_ROOT_DIR, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except IOError:
    long_description = """
Zepto LIMS - Laboratory Inventory Management System for tracking barcoded tubes.

See `README.md` for installation and usage.

"""


# Distribution build and release:
#   python setup.py sdist bdist_wheel
#   twine upload dist/*
setup(
    name='zepto-lims',
    version='2019.9.20',  # remember to also update __init__.py
    packages=['zepto_lims'],  # List all packages (directories) to include in the source dist.
    url='https://github.com/scholer/zepto-lims',
    license='GNU General Public License v3 (GPLv3)',
    author='Rasmus Scholer Sorensen',
    author_email='rasmusscholer@gmail.com',
    description='Zepto LIMS - Laboratory Inventory Management System for tracking barcoded tubes.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['LIMS', 'tracking', 'tubes', 'laboratory inventory management system'],
    entry_points={
        # 'console_scripts': [
        # ],
        # 'gui_scripts': [
        # ]
    },
    # pip will install these modules as requirements.
    install_requires=[
        'pyyaml',           # Config loading.
        'click',            # CLI package. (Only used for auxiliary CLI programs)
        'pylibdmtx',        # Datamatrix barcode scanner.
    ],
    python_requires='>=3.6',  # Type-hints, f-strings,
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        # 'Intended Audience :: Developers',
        # 'Intended Audience :: Education',

        # 'Topic :: Scientific/Engineering',

        # Pick your license as you wish (should match 'license' above)
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',

        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX :: Linux',
    ],
)
