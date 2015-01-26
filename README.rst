BASC Archiver
=============

The **BASC Archiver** is a Python library used to archive imageboard
threads. It uses the `4chan API`_ with the py4chan wrapper. Developers
are free to use the BASC-Archiver library for some interesting
third-party applications, as it is licensed under the LGPLv3.

It comes with a CLI interface for archiving threads, the
**thread-archiver**. (A GUI interface, the BASC-Archiver, is under
development.)

The **thread-archiver** is designed to archive all content from a 4chan
thread:

-  Download all images and/or thumbnails in given threads.
-  (NEW!) Download all child threads (4chan threads referred to in a
   post)
-  Download a JSON dump of thread comments using the 4chan API.
-  Download the HTML page
-  Convert links in HTML to use the downloaded images
-  Download CSS/JS and convert HTML to use them
-  Keep downloading until 404 (with a user-set delay)
-  Can be restarted at any time

The **thread-archiver** replaces the typical “Right-click Save As, Web
Page Complete” action, which does not save full-sized images or JSON. It
works as a guerilla, static HTML alternative to Fuuka.

Usage
=====

::

    Usage:
      thread-archiver <url>... [options]
      thread-archiver -h | --help
      thread-archiver -v | --version

    Options:
      --path=<string>            Path to folder where archives will be saved [default: ./archive]
      --runonce                  Downloads the thread as it is presently, then exits
      --delay=<float>            Delay between file downloads [default: 0]
      --poll-delay=<float>       Delay between thread checks [default: 20]
      --nothumbs                 Don't download thumbnails
      --thumbsonly               Download thumbnails, no images
      --ssl                      Download using HTTPS
      --follow-children          Follow threads linked in downloaded threads
      --follow-to-other-boards   Follow linked threads, even if from other boards
      --silent                   Suppresses mundane printouts, prints what's important
      --verbose                  Printout more information than normal
      -h --help                  Show help
      -v --version               Show version

Example
=======

::

    thread-archiver http://boards.4chan.org/b/res/423861837 --delay 5 --thumbsonly

Installation
============

The BASC-Archiver works on both Python 2.x and 3.x, and can be installed
on Windows, Linux, or Mac OS X.

Windows
-------

1. Install `ActivePython`_, Either version 2.x and 3.x will work. Make
   sure to enable the PyPM option, or else `pip will not be installed!`_
2. After installation, go to the Start Menu and under the **ActiveState
   ActivePython** programs folder, click **Python Package Manager
   (PyPM)**.
3. A command prompt will appear. Type in the command below and press
   enter:

   ::

       pip install BASC-Archiver

4. 

.. _4chan API: https://github.com/4chan/4chan-API
.. _ActivePython: http://www.activestate.com/activepython/downloads
.. _pip will not be installed!: http://stackoverflow.com/questions/4750806/how-to-install-pip-on-windows/4750846#4750846