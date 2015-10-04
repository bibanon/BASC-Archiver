#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Fuuka Archiver Class
from __future__ import print_function
from __future__ import absolute_import

from .base import BaseSiteArchiver


class FuukaSiteArchiver(BaseSiteArchiver):
    name = 'fuuka'

    def __init__(self, callback_handler, options):
        BaseSiteArchiver.__init__(self, callback_handler, options)

    def url_valid(self, url):
        """Return true if the given URL is for my site."""
        pass

    def add_thread(self, url):
        """Try to add the given thread to our internal list."""
        pass

    def download_threads(self):
        """Download all the threads we currently hold."""
        pass

    def _download_thread(self, thread_info):
        """Download the given thread, from the thread info."""
        pass
