#!/usr/bin/env python
# -*- coding: utf-8 -*-
# BASC Imageboard Archiver
from __future__ import absolute_import
from __future__ import print_function
import threading

from .sites import default_archivers

version = '0.9.3'
_default_base_dir = './archive'


class Options:
    """Holds Archiver options."""

    def __init__(self, base_dir, use_ssl=False,
                 silent=False, verbose=False,
                 delay=2, thread_check_delay=90,
                 dl_threads_per_site=5, dl_thread_wait=1,
                 skip_thumbs=False, thumbs_only=False,
                 skip_js=False, skip_css=False,
                 follow_child_threads=False, follow_to_other_boards=False,
                 run_once=False,):
        self.base_dir = base_dir
        self.use_ssl = use_ssl
        self.silent = silent
        self.verbose = verbose
        self.delay = float(delay)  # wait 2 seconds by default
        self.thread_check_delay = float(thread_check_delay)  # between checks of the same thread
        self.dl_threads_per_site = int(dl_threads_per_site)
        self.dl_thread_wait = float(dl_thread_wait)
        self.skip_thumbs = skip_thumbs
        self.thumbs_only = thumbs_only
        self.skip_js = skip_js
        self.skip_css = skip_css
        self.follow_child_threads = follow_child_threads
        self.follow_to_other_boards = follow_to_other_boards
        self.run_once = run_once


class Archiver:
    """Archives the given imageboard threads."""

    def __init__(self, options=None):
        if options is None:
            options = Options(_default_base_dir)
        self.options = options
        self.callbacks_lock = threading.Lock()
        self.callbacks = {
            'all': []
        }  # info callbacks

        # add our default site-specific archivers
        self.archivers = []
        for archiver in default_archivers:
            self.archivers.append(archiver(self.update_status, self.options))

    def shutdown(self):
        """Shutdown the archiver."""
        for archiver in self.archivers:
            archiver.shutdown()

    # threads
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

    @property
    def existing_threads(self):
        """Return how many threads exist."""
        threads = 0
        for archiver in self.archivers:
            threads += archiver.existing_threads
        return threads

    @property
    def files_to_download(self):
        """Return whether we still have files to download."""
        for archiver in self.archivers:
            if archiver.files_to_download:
                return True
        return False

    # callbacks
    def register_callback(self, cb_type, handler):
        """Register a callback."""
        with self.callbacks_lock:
            if cb_type not in self.callbacks:
                self.callbacks[cb_type] = []

            if handler not in self.callbacks[cb_type]:
                self.callbacks[cb_type].append(handler)

    def unregister_callback(self, cb_type, handler):
        """Remove a callback."""
        with self.callbacks_lock:
            if cb_type in self.callbacks and handler in self.callbacks[cb_type]:
                self.callbacks[cb_type].remove(handler)

    def update_status(self, cb_type, info):
        """Update thread status, call callbacks where appropriate."""
        with self.callbacks_lock:
            # to stop us calling same handler twice
            called = []

            if cb_type in self.callbacks:
                for handler in self.callbacks[cb_type]:
                    handler(cb_type, info)
                    called.append(handler)

            for handler in self.callbacks['all']:
                if handler not in called:
                    handler(cb_type, info)
