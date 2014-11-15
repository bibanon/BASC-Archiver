#!/usr/bin/env python
# -*- coding: utf-8 -*-
# BASC Imageboard Archiver Utilities
import os
import re
import json
import fileinput

import requests


def mkdirs(path):
    """Make directory, if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)


def download_file(local_filename, url, clobber=False):
    """Download the given file. Clobber overwrites file if exists."""
    dir_name = os.path.dirname(local_filename)
    mkdirs(dir_name)

    if clobber or not os.path.exists(local_filename):
        i = requests.get(url)

        # if not exists
        if i.status_code == 404:
            print('Downloading file failed:', local_filename, url)
            return False

        # write out in 1MB chunks
        chunk_size_in_bytes = 1024*1024  # 1MB
        with open(local_filename, 'wb') as local_file:
            for chunk in i.iter_content(chunk_size=chunk_size_in_bytes):
                local_file.write(chunk)

    return True


def download_json(local_filename, url, clobber=False):
    """Download the given JSON file, and pretty-print before we output it."""
    if download_file(local_filename, url, clobber):
        # read original json
        original_data = json.loads(open(local_filename).read())

        # write reformatted json
        with open(local_filename, 'w') as json_file:
            json_file.write(json.dumps(original_data, sort_keys=True, indent=2, separators=(',', ': ')))


def file_replace(local_filename, pattern, replacement):
    """Regex replace in the given file."""
    for line in fileinput.input(local_filename, inplace=True):
        print(re.sub(pattern, replacement, line))


def timestamp():
    """Return a timestamp for right now."""
    now = time.time()
    localtime = time.localtime(now)
    return time.strftime('%Y-%m-%d %H:%M:%S', localtime)
