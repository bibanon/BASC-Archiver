BASC Archiver
=============

The **BASC Archiver** is a Python library (packaged with the
**thread-archiver** script) used to archive imageboard threads.
It uses the `4chan API <https://github.com/4chan/4chan-API>`_
with the py4chan wrapper. Developers are free to use the
BASC-Archiver library for some interesting third-party applications,
as it is licensed under the LGPLv3.

It comes with a CLI interface for archiving threads, the
**thread-archiver**, with a GUI interface under development.

The **thread-archiver** is designed to archive all content from a 4chan
thread:

-  Download all images and/or thumbnails in given threads.
-  Download all child threads (threads referred to in a post).
-  Download a JSON dump of thread comments using the 4chan API.
-  Download the HTML page.
-  Convert links in HTML to use the downloaded images.
-  Download CSS/JS and convert HTML to use them.
-  Keep downloading until 404 (with a user-set delay).
-  Can be restarted at any time.
-  Threaded downloading to download multiple files at the same time.

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
      --path=<string>                Path to folder where archives will be saved [default: ./archive]
      --runonce                      Downloads the thread as it is presently, then exits
      --thread-check-delay=<float>   Delay between checks of the same thread [default: 90]
      --delay=<float>                Delay between file downloads [default: 0]
      --poll-delay=<float>           Delay between thread checks [default: 20]
      --dl-threads-per-site=<int>    Download threads to use per site [default: 5]
      --dl-thread-wait=<float>       Seconds to wait between downloads on each thread [default: 0.1]
      --nothumbs                     Don't download thumbnails
      --thumbsonly                   Download thumbnails, no images
      --nojs                         Don't download javascript
      --nocss                        Don't download css
      --ssl                          Download using HTTPS
      --follow-children              Follow threads linked in downloaded threads
      --follow-to-other-boards       Follow linked threads, even if from other boards
      --silent                       Suppresses mundane printouts, prints what's important
      -v --verbose                   Printout more information than normal
      -h --help                      Show help
      -V --version                   Show version


Example
=======

::

    thread-archiver http://boards.4chan.org/b/res/423861837 --delay 5 --thumbsonly


Installation
============
The BASC-Archiver is designed for Python 3.x, and can be installed on Windows, Linux, or Mac OS X.

(Python2 has intractable ascii->unicode conversion errors, whereas Python 3.x stores all strings in unicode, so we strongly recommend using 3.x.)

New stable releases can be found on our `Releases page <https://github.com/bibanon/BASC-Archiver/releases>`_,
or installed with the PyPi package `BASC-Archiver <https://pypi.python.org/pypi/BASC-Archiver>`_.

Linux and OSX
-------------

1. Make sure you have Python3 and pip3 installed. On Debian/Ubuntu, Fedora/Red Hat/CentOS, install the packages `python3` and `python3-pip` . Here's a `Mac OS X Installation Guide. <http://docs.python-guide.org/en/latest/starting/install/osx/>`_ 
2. Run ``pip3 install basc-archiver``

   - Linux users must run this command as root, or prefix the command with `sudo`.
3. Run ``thread-archiver http://boards.4chan.org/etc/thread/12345``

Threads will be saved in ``./archive``, but you can change that by supplying a directory with the ``--path=`` argument.

Windows
-------

1. Download the latest release from `our page <https://github.com/bibanon/BASC-Archiver/releases>`_.
2. Open up a command prompt window (``cmd.exe``), and move to the directory with ``thread-archiver.exe``
3. Run ``thread-archiver.exe http://boards.4chan.org/etc/thread/12345``

Using the Windows version will become simpler once we finish writing the GUI.

Android (CLI)
-------------

    **Note:** This is a temporary solution until we put together some
    kind of Android GUI app.

Thanks to the QPython interpreter, you can effortlessly run the
BASC-Archiver on your Android phone.

1. Install the `QPython app <https://play.google.com/store/apps/details?id=com.hipipal.qpyplus>`_ from Google Play.
2. Open the QPython app, and swipe left to reach the menu.
3. Tap **Package Index**. Then scroll down and tap **Pip Console**.
4. Run the following commands (after starting the pip\_install.py
   script):

   ::

       pip install requests
       pip install basc-archiver

Now you can just open QPython, tap **My QPython**, tap **pip\_console**,
and run the following command with your own thread URL:

::

    thread-archiver --path=/sdcard/ http://boards.4chan.org/qa/thread/23839

To run the script in the background, press the back button, and tap
**OK** at the **Run in Background** prompt. You can stop the script
anytime using ``Vol Down`` + ``C``.

-  **Note**: On Android (CLI), it is important to set the path to
   ``/sdcard/``, so the thread dump can be accessed from the
   ``/sdcard/archives/4chan/`` folder.
-  **Note**: To update the BASC-Archiver on Android (CLI), you must open
   QPython, press the **3-dot menu** button, scroll down and tap **Reset
   Private Space**. Then just reinstall the BASC-Archiver.

License
=======

Bibliotheca Anonoma Imageboard Thread Archiver (BASC Archiver)

Copyright (C) 2014 Antonizoon Overtwater, Daniel Oaks. Licensed under the GNU Lesser General Public License v3.
