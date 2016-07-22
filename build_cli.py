#!/usr/bin/env python3
# coding: utf-8
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

setup(
    name='BASC-Archiver',
    version='0.9.4',
    description='Makes a complete archive of imageboard threads including images, HTML, and JSON.',
    options=options,
    executables=[Executable('thread-archiver')],
)
