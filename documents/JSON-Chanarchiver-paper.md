JSON Chanarchiver
================

Abstract
---------

The current methods of archiving 4chan threads locally are inefficient, ineffective, and incomplete. Currently, most anons rely on the "Right-click/Save Page As" function, which dumps the whole HTML page vertabrim and only saves thumbnails. To supplement this flaw, image dumping scripts exist, but the full size images are obviously not linked to by the HTML dumps.

While online archives exist, some of which (like fuuka) can continuously archive an entire board, quite a few important boards are left untouched. Also, to save disk space, most of these archivers tend not to save full sized images; quite problematic when the majority of them cannot be found elsewhere. Additionally, these archives tend to face site crushing amounts of visitors, not to mention DDoSes from historical revisionists.

Chanarchive is unique in that it takes on the effort to accept threads from all of 4chan; but the caveat is that for a thread to be permanently saved, more than 10 people that happen to see the thread at the same time must take the time to go to the site, create an account, and vote for archival. 

In theory, this system prevents junk from clogging up the site; in practice, value is the the eye of the beholder, and even a thread that was interesting to 3 people in the whole world is still worth saving. And Chanarchive has had it's share of takedowns, eleventh-hour rescues, and revisionist moderators.

Independent, local archives still have their place. They're under the user's full control, and take whatever the user fancies. They cost almost nothing, and make it possible to view threads when there is no internet.

With the advent of the 4chan API, the site now gives out threads in nice clean JSON, rather than the HTML mess of the past. This makes it possible

Reference Implementation
--------------------------

Since an actual JSON to HTML converter is not the easiest thing to build, we will dump the plain HTML along with the JSON for the moment.

* Dump images, thumbs, JSON
  * Using a modded version of `4chandownloader.py`, now modded to use `py-4chan` wrapper 
* (FUTURE) Convert JSON to HTML
  * Not implemented in reference implementation yet
* Dump HTML page and convert to local links
  * using dump_html() and file_replace()
* (FUTURE) Save CSS locally each time
  * file_replace() function already made to convert HTML to use local links. Now need to actually save the CSS for each dump.
* (FUTURE) PyQt GUI
  * Based on the Chandler?

Implementation
--------------

There are two systems we will consider:

* PURE JSON Templating - HTML/Javascript/JQuery-based JSON templating system. A lot of time was wasted on this, but it was not possible to use since AJAX could not use local files for security reasons.
  1. (FAILURE: Webkit does not allow AJAX to import local files for security reasons.) Find a way to import an external file for PURE to work on, using the example.
* JSON-Template (Python) - A Python-based JSON Templating layer using dictionaries.
  1b. Create a script that builds
  2. Create a basic HTML templating system that pulls from JSON.

Background
---------

4chan is an extremely controversial, yet culturally important community on the English language internet. A great majority of posts are unremarkable and unworthy, to be at the very least, beauty is in the eye of the beholder.

The Interface
-----------

There should be three versions of the interface; a command line UI, a cross-platform GUI, and a web-based system. This way we can just dump it on any random python webhost, and people can wget the whole site to their computers, or just a thread folder.

We can build off this PyQt python script to make a cross-platform, computer based GUI. (It uses WTFPL) https://github.com/Dhole/4chan-image-dl

* Continuously monitor 4chan for images and threads until the page 404s.
* Make it possible to set times between tries.
* Make an option to save full sized images or simply thumbnails (to save space).
* Make it possible to archive multiple threads at once (GUI and web only)
* Just in case your computer disconnects, make it possible to start again until 404.
* When a thread is archived, the script should prompt the user to write a quick title, description, and danbooru-style tags of the contents of the thread. This, along with the date, time, and ID of the OP post will be placed into a `metadata.json` file in the same folder.

Folder Design (Description)
-------------------------

The folder for a thread should contain everything it needs to function; CSS, HTML, images, thumbs, and JSON, as a kind of source code. It should be possible to just 7zip the thread folder up and distribute for any web browser to read.

* First, copy the style.css file from the folder above (the section folder) into the thread folder. (See the chart below for clarification)
* Once a thread is archived, it should call a script that adds the thread ID and the title and description in the `metadata.json` file into a `list.json` file at the root of the section. (See the chart below for clarification)
* Once the `list.json` file is updated, the script should end by regenerating the `list.html` file.
* Since the threads never change after archival is complete, we should generate the HTML only once in the same directory. Then we don't need to screw around with databases.
* Link to the CSS and other content with relative links; avoid hard links. Like, style.css , or img/122933400.jpg .

Folder Design (Chart)
===========

    - /             # root of static website/archive
    |
    |-- /b/
    |
    |-- /b/list.json    # "database" of current threads archived in the site. 
    |-- /b/list.html
    |-- /b/style.css    # custom section style for all threads. This is copied into every thread folder.
    |-- /b/28392029
        |
        |-- /b/28392029/images/
        |-- /b/28392029/thumbs/
        |-- /b/28392029/style.css   # An Exact Copy of the `style.css` file in the folder above.
        |-- /b/28392029/thread.json
        |-- /b/28392029/thread.html
        |-- /b/28392029/metadata.json   # contains useful metadata about the thread.

Metadata.json
-----------

A quick and dirty example. Generally has all the information of the OP post in the 4chan API JSON, but with an archiver added title and description (if any).

* Title - Sums up what the thread is about. Written by archivist.
* Description - Sums up what happens in the thread. Written by archivist.
* Tags - Just like in hydrus; danbooru style tags.
* Thread ID - OP's post number for this thread; it's important, since this will be the title of the folder containing the content of the thread.
* OP Image - Filename of OP's image used when posting to 4chan. Generally unrelated to the thread.
* Date & Time - When the thread was posted, found in the OP post
* Date & Time of Final Post - When the thread 404'ed, found in the last post.

HTML Thread Lists (list.json, list.html)
-----------------

* The thread lists are just an HTML page with links to the threads in question, titles and description if added by the archiver, time, and OP image.
* This HTML page is generated by a script that is called each time the list.json "database" is changed.
* The list.json "database" should be automatically added to whenever a thread has completed archival, using the metadata.json and thread.json files.

* On top of all this, a section list should be made, linking to all the section list.html pages. This should be generated when the script is told to register and setup a folder (so other unrelated folders will be unaffected).

Hydrus Integration
-----------

Since every thread will have a metadata.json file, we can even extend Hydrus to index thread archives, so it can be even more awesome!

* Create a script that simply 7zips up a thread folder for distribution, so people can download the whole archive if we host the archive on a webserver.
* The filename should follow the format: 0000000_Title.chan.7z , which still keeps it recognizable as a 7z archive, but tells Hydrus that it is special, and to index it.
* (Actually, the .chan.xxx part is the identifier. To reduce system load, err could just use plain old .zip, which would look like .chan.zip. Your script would have to support it though, so that is the only limit.)
* Hydrus throws this file in it's database, and allows the user to index, tag, and edit the metadata.json file inside 

Libraries used
-----------

* [JSON-Template for Python](https://code.google.com/p/json-template/) - Used easily turn JSON into HTML with the power of templating.
* 4chan json-to-html - Created by the developer of Hydrus as a quick and dirty example.
