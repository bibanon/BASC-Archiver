#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Site-Specific Archiver Base Class
from __future__ import print_function
from __future__ import absolute_import

import os
import time
import threading

DEFAULT_NOITEM_WAIT = 1
DEFAULT_OK_WAIT = 0.1


class DownloadItem(object):
    def __init__(self, dl_type, info):
        self.dl_type = dl_type
        self.info = info
        self.next_dl_timestamp = 0

    def can_dl(self):
        """True if you can download this item."""
        return time.time() >= self.next_dl_timestamp

    def delay_dl_timestamp(self, delay_in_seconds=90):
        """Delay the download of this item for 90 seconds."""
        self.next_dl_timestamp = time.time() + delay_in_seconds


class DownloadThread(threading.Thread):
    def __init__(self, site,
                 noitem_wait_seconds=DEFAULT_NOITEM_WAIT,
                 nextitem_wait_seconds=DEFAULT_OK_WAIT):
        threading.Thread.__init__(self)
        self.site = site
        self.noitem_wait_seconds = noitem_wait_seconds
        self.nextitem_wait_seconds = nextitem_wait_seconds
        self.daemon = True
        self.start()

    def run(self):
        while True:
            # check if shutdown
            if self.site.is_shutdown:
                break

            # get next item to dl
            next_item = None
            with self.site.to_dl_lock:
                # make sure dl timestamp on selected item has passed
                for i in range(len(self.site.to_dl)):
                    next_item = self.site.to_dl[i]

                    if next_item.can_dl():
                        self.site.to_dl.pop(i)
                        break
                    else:
                        next_item = None

            # download
            if next_item is not None:
                self.site.download_item(next_item)

            # wait
            if next_item is None:
                time.sleep(self.noitem_wait_seconds)
            else:
                time.sleep(self.nextitem_wait_seconds)


class BaseSiteArchiver(object):
    name = 'base'

    def __init__(self, handler_callback, options):
        if self.name == 'base':
            raise Exception('BaseSiteArchiver must be subclassed!')
        self.options = options
        self.base_thread_dir = os.path.join(options.base_dir,
                                            '{}/{{board}}/{{thread}}/'.format(self.name))
        self.base_images_dir = os.path.join(self.base_thread_dir, 'images')
        self.base_thumbs_dir = os.path.join(self.base_thread_dir, 'thumbs')

        self.threads_lock = threading.Lock()
        self.threads = {}

        # setup thread info
        self.is_shutdown = False
        self.to_dl_lock = threading.Lock()
        self.to_dl = []

        self._handler_callback = handler_callback

        # start download threads
        for i in range(getattr(self, 'dl_threads', options.dl_threads_per_site)):
            DownloadThread(self, **{
                'noitem_wait_seconds': getattr(self, 'noitem_wait_seconds',
                                               DEFAULT_NOITEM_WAIT),
                'nextitem_wait_seconds': getattr(self, 'nextitem_wait_seconds',
                                                 options.dl_thread_wait),
            })

    def shutdown(self):
        """Shutdown this archiver."""
        self.is_shutdown = True

    def update_status(self, cb_type, info):
        """Update thread status, call callbacks where appropriate."""
        # mostly convenience function
        info['site'] = self.name
        self._handler_callback(cb_type, info)

    # download
    def add_to_dl(self, dl_type=None, item=None, **kwargs):
        """Add an item to our download list."""
        if item is not None:
            new_item = item
        else:
            new_item = DownloadItem(dl_type, kwargs)

        with self.to_dl_lock:
            self.to_dl.append(new_item)

    # adding threads
    def url_valid(self, url):
        """Return true if the given URL is for my site."""
        raise Exception('you must override this method')

    def add_thread(self, url):
        """Try to add the given thread to our internal list."""
        raise Exception('you must override this method')

    @property
    def existing_threads(self):
        """Return how many threads we have and are downloading."""
        return len(self.threads)

    # downloading specific items
    def download_item(self, item):
        """Download the given item"""
        raise Exception('you must override this method')
