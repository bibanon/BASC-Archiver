#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
import sys
import time
from basc_archiver import version, Options, Archiver

# check dor arguments
if len(sys.argv) < 2:
    sys.exit('Usage: %s <board> (e.g. diy )' % sys.argv[0])

# Grab JSON
board = sys.argv[1]
url = 'http://a.4cdn.org/%s/archive.json' % board
response = requests.get(url)
if response.status_code != 200:
	print('Status:', response.status_code, 'Problem with the request. Exiting.')
	exit()

# set up BASC-Archiver
options = Options('./archive', run_once=True)
archiver = Archiver(options)

# Obtain thread_ids from the board's archives
thread_list = response.json()

# add threads to our archiver
for thread in thread_list:
	archiver.add_thread("http://boards.4chan.org/%s/thread/%d" % (board , thread))

# download thread loop
try:
	while True:
		if archiver.existing_threads < 1:
			print('')
			print("All threads have either 404'd or no longer exist, exiting.")
			break

		time.sleep(float(1))
except KeyboardInterrupt:
	print('')
	print('Dump stopped. To obtain more threads, run this script again.')