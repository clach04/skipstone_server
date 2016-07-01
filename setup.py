#!/bin/env python2
# -*- coding: ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#

from distutils.core import setup

import py2exe

import wdtv_sim


hiddenimports = []
hidden_excludes = []

options = {
    'py2exe': {
        'includes': hiddenimports,
        'excludes': hidden_excludes,
        "compressed": 1,
        "optimize": 2,  ## NOTE 2 will optimize out __doc__ strings
    }
}


setup(
    console=['wdtv_sim.py'],
    version=wdtv_sim.version,
    options = options
)
