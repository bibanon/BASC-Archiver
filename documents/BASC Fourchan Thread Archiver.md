BASC Fourchan Thread Archiver
=================================

The YS 4chan Thread Archiver is a reference specification for a script that downloads all images, thumbs, JSON (thread data from 4chan API), and HTML (or JSON converted to HTML) from a 4chan thread.

This is a project designed for the *Society for the Study and Research of the Yotsuba Channel*, (The Yotsuba Society), a research group aiming to archive and document the products of the 4chan community. 

The archiver is designed to create archives in the `.chan.zip` standard, a simple compressed folder format having a defined folder structure, and a file with the thread's JSON from the 4chan API. 

Mass adoption of the `.chan.zip` standard will increase the ease of importing or exporting backups, interoperatibility between 4chan archives everywhere. This is a huge matter of importance, due to the constant collapse of 4chan archives throughout history.

What is 4chan?
----------------

4chan is an incredibly interesting, intensely controversial, and culturally significant English-language imageboard.

* Anonymity
* Cultural Powerhouse
* Lack of memory

### The Concept of the Anonymous Discussion Board

Before the rise of the internet, a text-based distributed discussion board system was widespread, known as USENET. Usage of this network was typically restricted to universities and researchers, though they did expand with the rise of the internet to become significant in tech circles by the late-1990s.

But in these networks the first signs began emerging that computer networks had connected people together so well, that they began to create a community; and even a culture. While the effects were limited, USENET users, especially those influenced by the concept of cypherpunk, introduced the concept of anonymous posting by using invalid names and emails, and then anonymous remailers. 

Despite this, later western discussion boards typically demanded user registration, as they looked down upon anonymous discussion, as evidenced by Slashdot's "Anonymous Coward" moniker for those without registration.

But in the mid 1990s, Japanese discussion boards began to embrace anonymous posting as a necessity, viewing the practice with a different perspective characteristic of the island's unique culture. 

Japanese culture tended to run along the lines of a phenonmenon described as "Honne-Tatemae", meaning the sharp contrast between a person's inner beliefs (Honne) and their public facade (tatemae).  Because of the pressures of Japanese society to avoid conflict and promote harmony, one's actual beliefs and attitudes were kept to oneself, shared only with close friends, while people publicly went with the mainstream and acted according to societal norms.

Anonymous posting effectively lifts the pressures of "tatemae" by removing the author's name from the actual content. No longer is the author restricted by fear of societal shame for speaking their mind. If the opinion is unpopular with the community, the author can simply distance themselves and continue the discussion. This ability to express "honne", or opinions, attitudes, and interests that the author truly holds inside, made anonymous discussion boards both powerfully interesting and liberating for Japanese users.

The most prominent example of an anonymous Japanese discussion board is 2channel, which has thus become a significant influence on the Japanese internet, and even Japanese society. 2channel's subboards encompass every major interest that people take interest in. 2channel is also a strong driver of subcultures that tend to be looked down upon by mainstream society, such as Anime. Sometimes even political campaigns or simple research are run by candidates wishing to divine the true beliefs and criticisms of their constituents.

### The Rise of 4chan

### 4chan's Influence

Abstract
---------

The current methods of archiving 4chan threads locally are inefficient, ineffective, and incomplete. Currently, most anons rely on the "Right-click/Save Page As" function, which dumps the whole HTML page vertabrim and only saves thumbnails. To supplement this flaw, image dumping scripts exist, but the full size images are obviously not linked to by the HTML dumps.

While online archives exist, some of which (like fuuka) can continuously archive an entire board, quite a few important boards are left untouched. Also, to save disk space, most of these archivers tend not to save full sized images; quite problematic when the majority of them cannot be found elsewhere. Additionally, these archives tend to face site crushing amounts of visitors, not to mention DDoSes from historical revisionists.

Chanarchive is unique in that it takes on the effort to accept threads from all of 4chan; but the caveat is that for a thread to be permanently saved, more than 10 people that happen to see the thread at the same time must take the time to go to the site, create an account, and vote for archival. 

In theory, this system prevents junk from clogging up the site; in practice, value is the the eye of the beholder, and even a thread that was interesting to 3 people in the whole world is still worth saving. And Chanarchive has had it's share of takedowns, eleventh-hour rescues, and revisionist moderators.

Independent, local archives still have their place. They're under the user's full control, and take whatever the user fancies. They cost almost nothing, and make it possible to view threads when there is no internet.

With the advent of the 4chan API, the site now gives out threads in nice clean JSON, rather than the HTML mess of the past. This makes it possible

Components
-----------

* Archive an entire 4chan thread and all it's images
* Find all links referenced in a thread
* Convert JSON into HTML, or Android/iOS app view
* Create a Metadata standard for Titling, describing, and tagging a thread
* Reference Specification for `.chan.zip` Standard 4chan Thread Archive Format (for archive sharing and transfer)
* Converting Legacy 4chan Thread Archives
* Index Systems: Static HTML and Server-side Scripts

Practical Usage
-----------

4chan's influence on modern internet culture is reason enough to create an archiver. 

4chan archives are used by researchers at the Society for the Study and Preservation of Yotsuba Channel, and 

The `.chan.zip` thread archive format can become a universal standard for all 4chan archivers, and drive the creation and betterment of both personal and and public archives.  

`.chan.zip` Standard 4chan Thread Archive Format
===============================================

Even though every `.chan.zip` file only has one thread from one board and one site, it is still required to follow this folder structure, which makes it easy to store them, and then zip them back up:

* `<website-name>` - The common name of the website.
  * `<board-url-acronym>` - On Futaba style imageboards, each board has a URL acronym, such as `/b/` or `/r9k/`.
    * `<thread-id>` - The folder that actually contains the archive in question. It is differentiated and dated by it's thread id (ex. 172839).
      * **Contents of the archive go here**

Folder Design (Chart)
===========

Here is an example in practice, for a thread with the URL `http://boards.4chan.org/b/thread/28392029/` :

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

----

Here is the standard format for the contents of the archive itself:

* `thumbs/` - A folder containing the thumbnails from the 4chan thread.
* `images/` (optional) - A folder containing the full size images from the 4chan thread.
* `<thread-id>.json` - The full thread in JSON format, generated by the 4chan API. Perfect for mobile viewing apps or import/export by databases.
* `external_links.txt` - A file that contains every single web link referenced in the thread. Useful for creating a [Webcite](http://www.webcitation.org/) snapshot to prevent link rot.
* `<thread-id>.html` - Contains an HTML-viewable version of the 4chan thread. (*we currently just slurp down the entire HTML from 4chan, but one day we will create a JSON-to-HTML converter for cleaner and smaller dumps*)
* `css/` - *Contains any CSS that the HTML file needs.* (will be depreciated and embedded in HTML after we create a JSON to HTML converter)
* `metadata.json` - Contains metadata in JSON format about the thread, such as titles, tags, or comments. Very useful for large thread archives.

Converting Existing Legacy 4chan Archives
----------------------------------------

Before the invention of this script, the 4chan API. and the `.chan.zip` standard, 4chan anons typically used the `Right-click, Save As (Webpage, Complete)` function in Firefox or IE.  This would save only the thumbnails and a snapshot of the HTML thread itself.

However, this method had serious caveats. It wouldn't save the full size images, and the threads were stored in ugly HTML that is difficult to work with. 

While we can't restore the lost full size images, we can reorganize the files and folders to fit the `.chan.zip` standard, and retroactively convert the HTML into the new 4chan API JSON format.

This way, we can convert these legacy archives into the new universal `.chan.zip` standard.

Archive Indexing System (Static HTML for non-database systems)
====================================

Here is a simple thread archive indexing system, that uses static HTML and does not require any software or database on the HTML host. It only needs to be compiled again whenever a thread is added.

This static HTML indexing system will create new files, looking like this:

* `index.html`
* `index.json`
* `saved-threads` - Contains the threads, either extracted or still in `.chan.zip` files

(no changes of any kind are made to the thread archives themselves)

### Procedure

The first step will depend on whether the system is running on a webserver or locally. If the system is on a local computer, filesize is more important, so the `.chan.zip` files will be left alone and extracted on the fly using [zip.js](http://stuk.github.io/jszip/) or something. If the system is on a webserver, speed and lower stress on the server is more important, so extract all the archives.

* (local) Place all `.chan.zip` files in the folder `saved-threads`.
* (webservers) Extract all `.chan.zip` files to the folder `saved-threads`.
  * The zip files will automatically sort their content into the right folders when extracted, using the folder structure specified in the standard.
  
An example folder structure with all `.chan.zip` files extracted looks like this:

* `index.html`
* `index.json`
* `archive`
  * `4chan`
    * `a`
      * `198456`
      * `343258`
      * `554058`
  * `7chan`
    * `i`
      * `3367`
      * `4452`
      
---

Next, we will need to generate the `index.json` file that contains information and file path of every thread in the archive.

An `index.html` file is generated from that file, which is categoried by site and board, uses the metadata of each thread archive for a title and description, and links to the HTML files of every thread archive. It could have embedded CSS for some better looks and mobile viewing support. Maybe even have Disqus for comments.

The `index.html` file should also give the user the option to download an entire thread as a `.chan.zip` file, choosing whether to include full images or not. A full archive download script should also be made which slurps down the entire archive with wait limits (30s-1min?) between each, to conserve server bandwidth.

If the index was generated for unextracted archives (local), it will just link to that file. If the index was generated for extracted archives (webserver), the webserver will easily repack and generate the zip file (probably using [zip.js](http://stuk.github.io/jszip/), which conserves server resources by having the client do the zipping)

### JSON Templating Implementation

Issues:

* What Javascript on-the-fly templating system to use?
* How do we open a local JSON dump as a Javascript object? (do we ask the user to input it in?) Do we embed them into the HTML file?
  * We can't, because Javascript is not allowed to access local files for security reasons. However, we can embed the JSON as a javascript object, like so: `var data = [ <insert_json_object_here> ];`
* What should the output look like? Just like 4chan, or an improved version?
* Should everything be embedded in the HTML file (CSS, JS, etc.) or kept separate?

Templating Engines:

* JSON2HTML
* PURE - Uses HTML-based template
* Tempo - Simplest and most logical template.

Proof-of-Concept: Display a JSON list of the names of bassists, randomized.

### Deployment

To put the indexed archives online, no software is needed on the server itself, it's just static HTML, so just dump it there and go, and everything works. All you need is the software on your computer to add to and generate the index.

However, static HTML has it's limits. When the index is on your computer, you can just recompile to add threads. But when the static HTML archive is placed online, only you, and no other user can contribute. For user contribution, server-side scripts are needed, which are described below:

### Server-Side User Contributable Index

* An index that has the user create the archive (with our script), and then upload it when they feel that it's done
* An index that takes requests for threads to archive (just like chanarchive)
* An index that archives every single thread (maybe create an extension to fuuka that allows `.chan.zip` export, rather than creating a whole new one)

---

When using server-side indexes, the threads and their JSON should be imported and stored in databases, but exportable to `.chan.zip` format upon request. Otherwise, the design is the same as the static HTML index.