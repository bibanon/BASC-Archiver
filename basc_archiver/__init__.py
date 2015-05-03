#!/usr/bin/env python
# -*- coding: utf-8 -*-
# BASC Imageboard Archiver
from __future__ import print_function
from __future__ import absolute_import

from .sites import default_archivers

version = '0.8.6'
_default_base_dir = './archive'


class Options:
    """Holds Archiver options."""

    def __init__(self, base_dir, use_ssl=False,
                 silent=False, verbose=False, delay=2,
                 skip_thumbs=False, thumbs_only=False,
                 follow_child_threads=False, follow_to_other_boards=False):
        self.base_dir = base_dir
        self.use_ssl = use_ssl
        self.silent = silent
        self.verbose = verbose
        self.delay = delay          # wait 2 seconds by default
        self.skip_thumbs = skip_thumbs
        self.thumbs_only = thumbs_only
        self.follow_child_threads = follow_child_threads
        self.follow_to_other_boards = follow_to_other_boards


class Archiver:
    """Archives the given imageboard threads."""

    def __init__(self, options=None):
        if options is None:
            options = Options(_default_base_dir)
        self.options = options

        # add our default site-specific archivers
        self.archivers = []
        for archiver in default_archivers:
            self.archivers.append(archiver(self.options))

    def add_thread(self, url):
        """Archive the given thread if possible"""
        url_archived = False
        for archiver in self.archivers:
            if archiver.url_valid(url):
                archiver.add_thread(url)
                url_archived = True

        if url_archived:
            return True
        else:
            print('We could not find a valid archiver for:', url)
            return False

    def download_threads(self):
        """Download all the threads we currently hold."""
        for archiver in self.archivers:
            archiver.download_threads()

    @property
    def existing_threads(self):
        """Return how many threads exist."""
        threads = 0
        for archiver in self.archivers:
            threads += archiver.existing_threads
        return threads
