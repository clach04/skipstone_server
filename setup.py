#!/bin/env python2
# -*- coding: ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#

from distutils.core import setup
import os

import py2exe

import wdtv_sim


hiddenimports = []
hidden_excludes = []

options = {
    'py2exe': {
        'includes': hiddenimports,
        'excludes': hidden_excludes,
        "compressed": 1, # create a compressed zip archive
        "optimize": 2,  # NOTE 2 will optimize out __doc__ strings
    }
}

# Avoid cluttering directory containing exe file(s) with pyd files,
# exe(s) directory will have python dll and then sub-directory of dependencies
zipfile = os.path.join('lib', 'shared.zip')


setup(
    console=['wdtv_sim.py'],
    version=wdtv_sim.version,
    options=options,
    zipfile=zipfile
)

# TODO remove w9xpopen.exe
# TODO zip up using version to generate filename.
