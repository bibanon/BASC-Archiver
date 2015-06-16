#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 4chan Archiver Class
from __future__ import print_function
from __future__ import absolute_import

from .base import BaseSiteArchiver
from .. import utils

import basc_py4chan

import os
import re
import time
import codecs

# finding board name/thread id
THREAD_REGEX = re.compile(r"""https?://(?:boards\.)?4chan\.org/([0-9a-zA-Z]+)/(?:res|thread)/([0-9]+)""")

# top level domains
FOURCHAN_BOARDS = 'boards.4chan.org'
FOURCHAN_CDN = '4cdn.org'

# cdn domains
FOURCHAN_API = 'a.' + FOURCHAN_CDN
FOURCHAN_IMAGES = 'i.' + FOURCHAN_CDN
FOURCHAN_THUMBS = 'i.' + FOURCHAN_CDN
FOURCHAN_STATIC = 's.' + FOURCHAN_CDN

# retrieval footer regex
FOURCHAN_BOARDS_FOOTER = '/%s/thread/%s'
FOURCHAN_API_FOOTER = FOURCHAN_BOARDS_FOOTER + '.json'
FOURCHAN_IMAGES_FOOTER = '/%s/%s'
FOURCHAN_THUMBS_FOOTER = '/%s/%s'

# download urls
FOURCHAN_BOARDS_URL = FOURCHAN_BOARDS + FOURCHAN_BOARDS_FOOTER
FOURCHAN_API_URL = FOURCHAN_API + FOURCHAN_API_FOOTER
FOURCHAN_IMAGES_URL = FOURCHAN_IMAGES + FOURCHAN_IMAGES_FOOTER
FOURCHAN_THUMBS_URL = FOURCHAN_THUMBS + FOURCHAN_THUMBS_FOOTER

# html parsing regex
HTTP_HEADER_UNIV = r"https?://"  # works for both http and https links
FOURCHAN_IMAGES_REGEX = r"/\w+/([0-9]+\.[a-zA-Z0-9]+)"
FOURCHAN_THUMBS_REGEX = r"/\w+/([0-9]+s\.[a-zA-Z0-9]+)"
FOURCHAN_CSS_REGEX = r"/css/([\w\.\d]+.css)"
FOURCHAN_JS_REGEX = r"/js/([\w\.\d]+.js)"
CHILDREGEX = re.compile(r"""href="/([0-9a-zA-Z]+)/(?:res|thread)/([0-9]+)""")

# regex links to 4chan servers
FOURCHAN_IMAGES_URL_REGEX = re.compile(HTTP_HEADER_UNIV + FOURCHAN_IMAGES + FOURCHAN_IMAGES_REGEX)
FOURCHAN_THUMBS_URL_REGEX = re.compile(HTTP_HEADER_UNIV + FOURCHAN_THUMBS + FOURCHAN_THUMBS_REGEX)
FOURCHAN_CSS_URL_REGEX = re.compile(HTTP_HEADER_UNIV + FOURCHAN_STATIC + '/css/')
FOURCHAN_JS_URL_REGEX = re.compile(HTTP_HEADER_UNIV + FOURCHAN_STATIC + '/js/')

# default folder and file names
_DEFAULT_FOLDER = '4chan'
_IMAGE_DIR_NAME = 'images'
_THUMB_DIR_NAME = 'thumbs'
_CSS_DIR_NAME = 'css'
_JS_DIR_NAME = 'js'
EXT_LINKS_FILENAME = 'external_links.txt'

# The Ultimate URL Regex
# http://stackoverflow.com/questions/520031/whats-the-cleanest-way-to-extract-urls-from-a-string-using-python
URLREGEX = re.compile(r"""((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.‌​][a-z]{2,4}/)(?:[^\s()<>]+|(([^\s()<>]+|(([^\s()<>]+)))*))+(?:(([^\s()<>]+|(‌​([^\s()<>]+)))*)|[^\s`!()[]{};:'".,<>?«»“”‘’]))""", re.DOTALL)


class FourChanSiteArchiver(BaseSiteArchiver):
    name = '4chan'

    def __init__(self, options):
        BaseSiteArchiver.__init__(self, options)

        self.boards = {}

    def url_valid(self, url):
        """Return true if the given URL is for my site."""
        return THREAD_REGEX.match(url)

    def _url_info(self, url):
        """INTERNAL: Takes a url, returns board name, thread info."""
        if self.url_valid(url):
            return THREAD_REGEX.findall(url)[0]
        else:
            return [None, None]

    def add_thread(self, url):
        """Add the given thread to our download list."""
        board_name, thread_id = self._url_info(url)
        thread_id = int(thread_id)
        return self._add_thread_from_info(board_name, thread_id)

    def _add_thread_from_info(self, board_name, thread_id):
        """Add a thread to our internal list from direct board name/thread id."""
        # already exists
        if thread_id in self.threads:
            return True

        # running board object
        if board_name not in self.boards:
            self.boards[board_name] = basc_py4chan.Board(board_name, https=self.options.use_ssl)
        running_board = self.boards[board_name]

        if not running_board.thread_exists(thread_id):
            print('4chan Thread /{}/{} does not exist.'.format(board_name, thread_id))
            print("Either the thread already 404'ed, your URL is incorrect, or you aren't connected to the internet.")
            return False

        # add thread to download list
        self.threads[thread_id] = {
            'board': board_name,
            'dir': self.base_thread_dir.format(board=board_name, thread=thread_id),
            'id': thread_id,
        }

    def _download_thread(self, thread):
        """Download the given thread, from the thread info."""
        # skip if no new posts
        if 'thread' in thread:
            new_replies = thread['thread'].update()
            if new_replies < 1:
                # skip if no new posts
                return True
            elif thread['thread'].is_404:
                # thread 404'd
                print("Thread /{}/{} 404'd.".format(thread['board'], thread['id']))
                del self.threads[thread['id']]
                return True
        else:
            running_board = self.boards[thread['board']]
            self.threads[thread['id']]['thread'] = running_board.get_thread(thread['id'])
            thread['thread'] = self.threads[thread['id']]['thread']

        # download
        if not self.options.silent:
            print('4chan Thread: /{}/{}'.format(thread['board'], thread['id']))

        utils.mkdirs(thread['dir'])

        http_header = ('https://' if self.options.use_ssl else 'http://')

        # images
        if not self.options.thumbs_only:
            image_dir = os.path.join(thread['dir'], _IMAGE_DIR_NAME)
            utils.mkdirs(image_dir)

            for filename in thread['thread'].filenames():
                file_url = http_header + FOURCHAN_IMAGES_URL % (thread['board'], filename)
                file_path = os.path.join(image_dir, filename)

                if not os.path.exists(file_path):
                    # delay the download to reduce stress on server
                    time.sleep(float(self.options.delay))
                    if utils.download_file(file_path, file_url):
                        if not self.options.silent:
                            print('  Image:', filename, 'downloaded.')

        # thumbs
        if self.options.thumbs_only or not self.options.skip_thumbs:
            thumb_dir = os.path.join(thread['dir'], _THUMB_DIR_NAME)
            utils.mkdirs(thumb_dir)

            for thumbname in thread['thread'].thumbnames():
                thumb_url = http_header + FOURCHAN_THUMBS_URL % (thread['board'], thumbname)
                file_path = os.path.join(thumb_dir, thumbname)

                if not os.path.exists(file_path):
                    # delay the download to reduce stress on server
                    time.sleep(float(self.options.delay))
                    if utils.download_file(file_path, thumb_url):
                        if not self.options.silent:
                            print('  Thumbnail:', thumbname, 'downloaded.')

        # record external urls and follow child threads
        external_urls_filename = os.path.join(thread['dir'], EXT_LINKS_FILENAME)
        with codecs.open(external_urls_filename, 'w', encoding='utf-8') as external_urls_file:
            # all posts, including topic
            all_posts = [thread['thread'].topic]
            all_posts.extend(thread['thread'].replies)
            for reply in all_posts:
                if reply.comment is None:
                    continue

                # 4chan puts <wbr> in middle of urls for word break, remove them
                cleaned_comment = re.sub(r'\<wbr\>', '', reply.comment)

                # child threads
                if self.options.follow_child_threads:
                    for child_board, child_id in CHILDREGEX.findall(cleaned_comment):
                        is_same_board = child_board == thread['board']
                        child_id = int(child_id)

                        if child_id not in self.threads:
                            if self.options.follow_to_other_boards or not self.options.follow_to_other_boards and is_same_board:
                                print('  Child thread /{}/{} found and being added/downloaded'.format(child_board, child_id))
                                self._add_thread_from_info(child_board, child_id)
                                try:
                                    self._download_thread(self.threads[child_id])
                                except:
                                    # assume recursion got us, skip and do on next download
                                    print('    There was a problem downloading this thread. Skipping for now.')

                # external urls
                if not URLREGEX.findall(reply.comment):
                    continue

                for found in URLREGEX.findall(cleaned_comment):
                    for url in found:
                        if url:
                            external_urls_file.write('{}\n'.format(url))

        # dump 4chan json file, pretty printed
        local_filename = os.path.join(thread['dir'], '{}.json'.format(thread['id']))
        url = http_header + FOURCHAN_API_URL % (thread['board'], thread['id'])

        if utils.download_json(local_filename, url, clobber=True):
            if not self.options.silent:
                print('  Thread JSON downloaded.')

        # and output thread html file
        local_filename = os.path.join(thread['dir'], '{}.html'.format(thread['id']))
        url = http_header + FOURCHAN_BOARDS_URL % (thread['board'], thread['id'])

        if utils.download_file(local_filename, url, clobber=True):
            # get css files
            css_dir = os.path.join(thread['dir'], _CSS_DIR_NAME)
            utils.mkdirs(css_dir)

            css_regex = re.compile(FOURCHAN_CSS_REGEX)
            found_css_files = css_regex.findall(codecs.open(local_filename, encoding='utf-8').read())
            for css_filename in found_css_files:
                local_css_filename = os.path.join(css_dir, css_filename)
                url = http_header + FOURCHAN_STATIC + '/css/' + css_filename
                utils.download_file(local_css_filename, url)

            # get js files
            js_dir = os.path.join(thread['dir'], _JS_DIR_NAME)
            utils.mkdirs(js_dir)

            js_regex = re.compile(FOURCHAN_JS_REGEX)
            found_js_files = js_regex.findall(codecs.open(local_filename, encoding='utf-8').read())
            for js_filename in found_js_files:
                local_js_filename = os.path.join(js_dir, js_filename)
                url = http_header + FOURCHAN_STATIC + '/js/' + js_filename
                utils.download_file(local_js_filename, url)

            # convert links to local links
            utils.file_replace(local_filename, '"//', '"' + http_header)
            utils.file_replace(local_filename, FOURCHAN_IMAGES_URL_REGEX, _IMAGE_DIR_NAME + r'/\1')
            utils.file_replace(local_filename, FOURCHAN_THUMBS_URL_REGEX, _THUMB_DIR_NAME + r'/\1')
            utils.file_replace(local_filename, FOURCHAN_CSS_URL_REGEX, _CSS_DIR_NAME + '/')
            utils.file_replace(local_filename, FOURCHAN_JS_URL_REGEX, _JS_DIR_NAME + '/')

            if not self.options.silent:
                print('  Thread HTML downloaded.')

            if thread['thread'].closed:
                print("4chan Thread /{}/{} is closed.".format(thread['board'], thread['id']))
                del self.threads[thread['id']]
