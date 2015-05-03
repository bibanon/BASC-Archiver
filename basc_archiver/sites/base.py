#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Site-Specific Archiver Base Class
from __future__ import print_function
from __future__ import absolute_import

import os


class BaseSiteArchiver(object):
    name = 'base'

    def __init__(self, options):
        if self.name == 'base':
            raise Exception('BaseSiteArchiver must be subclassed!')
        self.threads = {}
        self.options = options
        self.base_thread_dir = os.path.join(options.base_dir, '{}/{{board}}/{{thread}}/'.format(self.name))

    def url_valid(self, url):
        """Return true if the given URL is for my site."""
        raise Exception('you must override this method')

    def add_thread(self, url):
        """Try to add the given thread to our internal list."""
        raise Exception('you must override this method')

    def download_threads(self):
        """Download all the threads we currently hold."""
        # we iterate over a copy of self.threads because download_thread
        # deletes it from there if thread 404's
        for thread_id in dict(self.threads):
            self._download_thread(self.threads[thread_id])

    @property
    def existing_threads(self):
        """Return how many threads we have and are downloading."""
        return len(self.threads)

    def _download_thread(self, thread_info):
        """Download the given thread, from the thread info."""
        raise Exception('you must override this method')
