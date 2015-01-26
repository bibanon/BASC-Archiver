BASC Archiver
=============

The **BASC Archiver** is a Python library (packaged with a **thread-archiver** script) used to archive imageboard
threads. It uses the [4chan API](https://github.com/4chan/4chan-API)
with the py4chan wrapper. Developers are free to use the BASC-Archiver
library for some interesting third-party applications, as it is licensed
under the LGPLv3.

It comes with a CLI interface for archiving threads, the
**thread-archiver**. (A GUI interface, the BASC-Chandler, is under
development.)

The **thread-archiver** is designed to archive all content from a 4chan
thread:

-   Download all images and/or thumbnails in given threads.
-   (NEW!) Download all child threads (4chan threads referred to in a post)
-   Download a JSON dump of thread comments using the 4chan API.
-   Download the HTML page
-   Convert links in HTML to use the downloaded images
-   Download CSS/JS and convert HTML to use them
-   Keep downloading until 404 (with a user-set delay)
-   Can be restarted at any time

The **thread-archiver** replaces the typical "Right-click Save As, Web
Page Complete" action, which does not save full-sized images or JSON. It
works as a guerilla, static HTML alternative to Fuuka.

Usage
=====

```
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
```
    
Example
=======

    thread-archiver http://boards.4chan.org/b/res/423861837 --delay 5 --thumbsonly

Installation
============

The BASC-Archiver works on both Python 2.x and 3.x, and can be installed
on Windows, Linux, or Mac OS X.

Windows
-------

1.  Install
    [ActivePython](http://www.activestate.com/activepython/downloads),
    Either version 2.x and 3.x will work. Make sure to enable the PyPM
    option, or else [pip will not be
    installed!](http://stackoverflow.com/questions/4750806/how-to-install-pip-on-windows/4750846#4750846)
2.  After installation, go to the Start Menu and under the **ActiveState
    ActivePython** programs folder, click **Python Package Manager
    (PyPM)**.
3.  A command prompt will appear. Type in the command below and press
    enter:

        pip install BASC-Archiver

4.  Open up a command prompt and navigate to the folder where the python
    scripts are stored. (In this example we assume it is **Python33**.
    Check the root of your C drive if it isn't)

        cd C:\Python33\Scripts

5.  Now we can use the script. Replace the URL in the example below with
    the one you want to save, and replace the path (keep the quotations)
    with the folder you want to save to.

        python thread-archiver http://boards.4chan.org/b/res/423861837 --path="C:\Users\Danny\4chan-threads"

6.  Sometimes, 4chan will make changes to it's API. We aim to update the
    script as soon as any change occurs, so if something's not working
    right, use the command below to upgrade to the latest version. If
    you're still having problems, raise an issue on our
    [Github.](https://github.com/bibanon/BA-4chan-thread-archiver)

        pip install BASC-Archiver --upgrade

Linux/Mac
---------

1.  Install Python on your computer. On Linux, Python is almost always
    preinstalled.
2.  We also need to install the Pip package manager, to download all the
    dependencies, and Requests, a needed library. For an Ubuntu/Debian
    system, use the following commands:

        sudo apt-get install python3-pip python3-requests
        sudo pip3 install BASC-Archiver

3.  Navigate your terminal to the folder you wish to save the threads
    into, and run the command below to download an entire thread. (you
    may also manually specify a path, using the **--path=** argument)

        thread-archiver http://boards.4chan.org/b/res/423861837

4.  Sometimes, 4chan will make changes to it's API. We aim to update the
    script as soon as any change occurs, so if something's not working
    right, use the command below to upgrade to the latest version. If
    you're still having problems, raise an issue on our
    [Github.](https://github.com/bibanon/BA-4chan-thread-archiver)

        sudo pip3 install BASC-Archiver --upgrade

Where to Post Archived threads
==============================

Your archived threads can be viewed from any web browser. Just enter the
thread's folder, and open the HTML file.

Alternatively, you can upload the entire **archive** folder to any
static HTML host, no PHP required. We strongly recommend that you share
them with the world on some kind of Static HTML host, such as the
following:

-   Github Pages
-   Gitorious Pages
-   Google Pages
-   000webhost
-   And more!

Please make sure that your content follows the chosen host's Terms of
Service policies (keep your pr0n to yourself, etc.).

Wishlist
========

-   **Migrate to BA-py4chan**, the improved fork of Edgeworth's original
    py-4chan wrapper.
-   **.chan.arc** - Standard archival format definition for imageboards.
-   Create a **pyFuuka**, for archiving from Fuuka's API.
-   **index.html list** - In the future we will make an extension that
    records links to currently downloaded threads in an index.html
    file...

License
=======

The 4chan Archiver Class is jointly written and maintained by by
[antonizoon](https://github.com/antonizoon) and [Daniel
Oaks](https://github.com/DanielOaks).

It is based on, and supersedes the Bibliotheca Anonoma's
[BA-4chan-thread-archiver](https://github.com/bibanon/BA-4chan-thread-archiver)
tool, written by [antonizoon.](https://github.com/antonizoon).

The BA-4chan-thread-archiver was originally forked from Socketub's
[4chan-thread-archiver](https://github.com/socketubs/4chan-thread-archiver),
originally licensed under the GNU Affero General Public License v3 or
later.
