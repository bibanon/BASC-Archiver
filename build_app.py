#!/usr/bin/env python
# coding: utf-8

import os
import sys
from cx_Freeze import setup, Executable

options = {
    'build_exe': {
        'packages': [
            'atexit',
        ],
        'excludes': [
            # 'tkinter',
        ],
    },
    'bdist_mac': {
        'bundle_name': 'BASC-Archiver',
        'iconfile': 'build-files/icon.icns',
        'custom_info_plist': 'build-files/Info.plist',
    },
    'bdist_dmg': {
        'volume_label': 'BASC-Archiver',
    },
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

setup(
    name='BASC-Archiver',
    version='0.8.2',
    description='Makes a complete archive of imageboard threads including images, HTML, and JSON.',
    options=options,
    executables=[Executable('thread-archiver-gui', base=base)],
)

