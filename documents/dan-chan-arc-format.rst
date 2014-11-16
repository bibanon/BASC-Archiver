.chan.arc File Format
=====================

Abstract
--------
This document specifies the ``.chan.arc`` file extension. This format is designed to provide a simple, standard way to represent and transport archives of imageboard threads.

This format has been created primarily for 4chan threads, but aims to cleanly store threads from other decently compatible image boards (as well as from other imageboard archives themselves).

Status of This Document
-----------------------
This is very much a draft reference, and is not recommended for production use. Because of the early nature of this draft, the version string is "draft-01", the format of which will likely be changed for release.

Introduction
------------
Image boards have proved themselves important parts in the creation of internet culture. However, some of the primary image boards in use today have been founded on ephemerality. This leaves the job of archiving and saving content to third parties or to the users themselves.

Many completely seperate methods of archiving image board threads have been developed, from a user simply going to "Save Page" in their browser to complex scripts and programs designed for backing up content. Because each of these is independently developed, there has not been a standard way to browse or to transfer thread backups from one system to another.

With this format, we hope to create a standard way to store image board threads so that we can be able to, say, import threads from a bunch of different archives into a single, unified display and management system.

To start off with, we will be describing a standard manifest of thread information and a standard folder structure for archives. We do, however, want to also describe a standard way to store the topic and reply posts as well as any other information required to recreate the page from a basic template, further on.

Compression
-----------
The ``.arc`` part of the standard name refers to some form of archive compression. The two standard forms of ``.chan.arc`` compression are listed below:

* ``7zip``

    This format refers to 7zip, a very good open source compression format. Due to the high level of compression of this format, this is the recommended way to compress ``chan.arc`` archives. Archives compressed with this format should have the file extension ``chan.7z``.

* ``zip``

    This format refers to PKZIP, the standard archive format for Windows-based systems. While this format has not proven itself the absolute best for compression's sake, there is a large ecosystem of tools and libraries already familiar with this format, and it is quite simple to decompress and extract files from this. Archives compressed with this format should have the file extension ``chan.zip``.

Other archive formats may be used, but this is not recommended.

Folder Structure
----------------
This lays out the standard folder structure of an archived thread. The specific files and folders are described in-detail below.

This is a reference example of an archived thread::

    /manifest.json
    /index.html
    /images
        /12345.jpg
        /23456.gif
    /thumbs
        /12345.jpg
        /23456.jpg
    /resources
        /css
            /embedded_file_a.css
            /embedded_file_b.css
        /embedded_file.js
        /favicon.png
    /warc
        warc_01.warc.gz
        warc_01.cdx
    /raw
        api.json
        raw_file_a.ext
        raw_file_b.ext

The ``resources`` directory is optional, but should be included where the index.html links to external resources on the image board's website.

manifest.json
^^^^^^^^^^^^^
The manifest file describes the metadata associated with the given image board thread. It includes a variety of details related to when the thread was created, archived, the site/board it was originally on and where it was archived from.

A typical ``manifest.json`` file is laid out as such:

.. code:: json

    {
        "arc_version": "draft-01",
        "thread": {
            "title": "Thread Title",
            "op": {
                "name": "Some Guy",
                "email": "a@example.com",
                "tripcode": "#coolDuD3"
            },
            "sticky": true
        },
        "created": {
            "site": "4chan",
            "board": "etc",
            "thread_id": 123123,
            "datetime": "2014-03-12 21:42:06",
            "timestamp": 49732497592874,
        },
        "archived": {
            "site": "archive.moe",
            "datetime": "2014-05-17 14:24:53",
            "timestamp": 9867378547236,
        }
    }

**arc_version**

This key lists the version of the ``chan.arc`` format that this archive conforms to. Right now, this version string is ``draft-01``, where ``01`` will be incremented for newer version of this chan archive draft.

The final format of this string is not yet decided, but will be closer to the final release of this specification.

**thread**

This contains information about the thread. These should be generated at archive time. Subkeys may be excluded if the information does not or cannot be extracted at archive time. This key itself may be excluded if there are no subkeys.

* ``title``

    This contains the title of the given thread. It is a string, containing any characters necessary.

* ``op``

    This contains information about the posted who created the thread. These may be excluded if the information does not exist or cannot be extracted, but this is not recommended. The subkeys are detailed below.

    * ``name``

        This key contains what is in the ``name`` field of the topic post of the thread. This is a string, and can contain any characters the original site supports in its name field.

    * ``email``

        This key contains what is in the ``email`` field of the topic post of the thread. This is a string, and can contain any characters the original site supports in its name field. It is important to note that this may contain a string that is not a valid email address. This is by design, as some sites let users post with this in their email field.

    * ``tripcode``

        This key contains what the ``tripcode`` of the topic post of the thread is displayed as. This may contain a standard tripcode or a secure tripcode, depending on what is supported by the base site and what the post contains. This is a string that can contain any characters necessary to represent the generated tripcode, but is expected to conform to standard tripcode formats. Leading and trailing whitespace should be stripped from this field.

* ``sticky``

    This boolean represents whether the post is a 'sticky' post. That is, whether the site management has 'stuck' it to the top of the image board. It may contain the value ``true`` or ``false``, and is generated at archive time.

**created**

This lists the site the thread was created on, the board the thread was created on, the thread's ID and the datetime it was created.

**archived**

This lists the site the thread was archived from, as well as the time and date of archival. This key is primarily for archiving threads from other imageboard archival websites. For instance, ``archive.moe``, ``4archive``, and ``4chandata``. If the thread has been archived from a third-party service, the ``site`` key must be different from the ``site`` key in **created**

**created/archived keys**

* ``site``

    This is a simplified representation of the site name and should be fairly easy to guess for most sites. This is usually the part of the domain name before the TLD. As an example, ``4chan.org`` becomes ``4chan``. However, this may be whatever best represents the given site.

    In another example, the archival website ``archive.moe``'s site key would be ``archive.moe``, since a shortening cannot properly represent the site name. It may contain numbers, lowercase letters, dots, dashes, and underscores. It may not contain spaces or any other character not mentioned.

* ``board``

    This represents the 'board' the thread was archived from. For instance, ``/tg/`` would be represented as ``tg``, ``/g/`` would be represented as ``g``. This is usually the url slug the board occupies. The first and last slashes are recommended to be removed from this.

    If an image board implements recursive sub-boards or other similar features, this is recommended to be represented with slashes in the board name, such as ``tch/cmp``. However, if the board does support slashes within board names, this should be represented as a list such as ``['tch/cmp', 'g']``.

    This may contain any characters necessary to represent the board, but is recommended to be lowercase letters, numbers, and dashes and underscores if required.

* ``thread_id``

    This is the id of the thread. Generally, this is the id of the topic post (OP), or the first post of the thread. This is an integer.

* ``datetime``

    This is a human-readable representation of the given time, taking the format ``YYYY-MM-DD hh:mm:ss``. This is recommended to be in Coordinated Universal Time (UTC).

* ``timestamp``

    This is a unix timestamp representing the given time. This is primarily a machine-readable representation, and is recommended to be in Coordinated Universal Time (UTC).


index.html
^^^^^^^^^^
This is a purely human-readable file. It is created at archive time, and is essentially a download of the thread HTML with resource URLs (pointing towards the original site) replaced with ones pointing towards our created ``/resources/`` folder instead. If this is not possible to due the nature of the site, this should be created at archive time from something like a template – anything that lets users double-click this file and browse the thread from the archive folder.

images/
^^^^^^^
This folder contains the original images posted in the thread. This folder may be excluded, but this is not recommended as it takes value away from the archive. Images in this folder will be named from the post ID followed by the file extension of the image.

thumbs/
^^^^^^^
This folder contains the original thumbnails posted in the thread. This folder must be included if possible. Images in this folder will be named by the post ID followed by the file extension of the image.

resources/
^^^^^^^^^^
This folder contains resources linked by the ``index.html`` file. This folder may have subdirectories. It is only recommended to create subdirectories if the created folder will have more than a single file. The recommended subdirectories include ``css``, ``js``, and ``images``. If the favicon is a single file, it should be put in the root ``resources/`` directory as shown. If there are multiple favicon files, they should be put in a ``resources/favicons/`` folder.

warc/
^^^^^
This folder is for storing files in the Web ARChive file format. These files may take any file name deemed appropriate, depending on how the archiver downloads and stores these files. Storing WARC files allow external archives such as the `Wayback Machine <http://archive.org/web/>`_ to import thread information and allow users to browse the thread exactly as it existed at archive time. This directory and storing WARC files is recommended, but not required.

raw/
^^^^
This folder is for storing files which may be of use and importance, but are not described in this specification. It is also for storing files which have been described, but are site-specific and do not have widespread enough adoption to warrant putting them in another location.

**List of files officially available under the raw/ directory**

* ``api.json`` (4chan)


Unfinished
==========
This specification is still in heavy development. There are many other things we need to store, and other pieces of information we need to generate for these to be extremely useful.
