BASC Thread Archiver
====================

This script uses the `4chan API <https://github.com/4chan/4chan-API>`_ to:

* Download all images and/or thumbnails in given threads.
* Download a JSON dump of thread comments using the 4chan API.
* Download the HTML page
* Convert links in HTML to use the downloaded images
* Download CSS/JS and convert HTML to use them
* Keep downloading until 404 (with a user-set delay)
* Can be restarted at any time

This script is designed to replace the typical "Right-click Save As, Web Page Complete" action, since that does not save full-sized images or JSON. 

This can also be used as a guerilla, static HTML alternative to Fuuka.

Part of the JSON-based-chanarchiver by Antonizoon Overtwater, built 2013/04/04.

Example
=======

::

    thread-archiver http://boards.4chan.org/b/res/423861837 --delay 5 --thumbsonly

Installation
============

Windows
-------

> **Note:** This script is now fixed for Windows and Python 3.x. PyQt GUI coming soon.

1. Install `ActivePython <http://www.activestate.com/activepython/downloads>`_,  Either version 2.x and 3.x will work. Make sure to enable the PyPM option, or else `pip will not be installed! <http://stackoverflow.com/questions/4750806/how-to-install-pip-on-windows/4750846#4750846>`_
2. After installation, go to the Start Menu and under the **ActiveState ActivePython** programs folder, click **Python Package Manager (PyPM)**.
3. A command prompt will appear. Type in the command below and press enter:

::

    pip install BASC-Archiver
    
4. Open up a command prompt and navigate to the folder where the python scripts are stored. (In this example we assume it is **Python33**. Check the root of your C drive if it isn't)

::

    cd C:\Python33\Scripts

5. Now we can use the script. Replace the URL in the example below with the one you want to save, and replace the path (keep the quotations) with the folder you want to save to.
        
::

        python thread-archiver http://boards.4chan.org/b/res/423861837 --path="C:\Users\Danny\4chan-threads"
  
6. Sometimes, 4chan will make changes to it's API. We aim to update the script as soon as any change occurs, so if something's not working right, first use the command below to update. If you're still having problems, raise an issue on our `Github. <https://github.com/bibanon/BA-4chan-thread-archiver>`_

::

    pip install BASC-Archiver --upgrade

Linux/Mac
---------

1. Install Python on your computer. On Linux, Python is almost always preinstalled.
2. We also need to install the Pip package manager, to download all the dependencies, and Requests, a needed library. For an Ubuntu/Debian system, use the following commands:

::

    sudo apt-get install python3-pip python3-requests
    sudo pip3 install BASC-Archiver

3. Navigate your terminal to the folder you wish to save the threads into, and run the command below to download an entire thread. (you may also manually specify a path, using the **--path=** argument)

::

    thread-archiver http://boards.4chan.org/b/res/423861837

4. Sometimes, 4chan will make changes to it's API. We aim to update the script as soon as any change occurs, so if something's not working right, first use the command below to update. If you're still having problems, raise an issue on our `Github. <https://github.com/bibanon/BA-4chan-thread-archiver>`_

::

    sudo pip3 install BASC-Archiver --upgrade

Where to Post Archived threads
===============================

After archiving your threads, you can just upload the entire `4chan` to any static HTML host (no PHP needed). We strongly recommend that you share them with the world on some kind of Static HTML host, such as the following:

* Github Pages
* Gitorious Pages
* Google Pages
* And more!

Please make sure that your content follows the chosen host's Terms of Service policies (keep your pr0n to yourself, etc.).

In the future we will make an extension that records links to currently downloaded threads in an index.html file...

Modifications to original
==========================

Originally forked from Socketub's `4chan-thread-archiver. <https://github.com/socketubs/4chan-thread-archiver>`_ 

However, all the original has long since been replaced, and the scripts are totally different. Here is a list of additions:

* Based on `py4chan <https://github.com/e000/py-4chan>`_
* Downloads HTML dump of thread
* New --thumbsonly option to download thumbnails and no images
* Code modularization
* More comments in code
* Support for new 4cdn.org server

More info and a full journal can be found in ``documents/log.md``.

License
=======

The 4chan Archiver Class is based on Bibliotheca Anonoma `BA-4chan-thread-archive <https://github.com/bibanon/BA-4chan-thread-archiver>`_ tool, and was originally forked from Socketub's `4chan-thread-archiver. <https://github.com/socketubs/4chan-thread-archiver>`_ The original license of Socketub's archiver is the GNU Affero General Public License v3 or later.

Wishlist
=========

* Prompt user for metadata information.
* Define the ``.chan.zip`` format for 4chan thread archive transfer
* Create a PyQt GUI
