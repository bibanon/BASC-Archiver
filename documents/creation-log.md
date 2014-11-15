This is a long journal and explanation of the process of creating the `BA-4chan-thread-archiver` script. It provides a rare insight into the process that goes into making even the simplest scripts.

Before making this script, I knew next to nothing about Python (although I did have a background in basic programming and bash scripting), so the entire thing was a

## Commenting

Generally, the comments in the source code of a program is it's most important portion. Even experienced programmers may need an explanation why something is done the way it is. It's like annotations on music for musicians.

While I was learning programming, I sometimes tried my hand at reading and commenting source code of certain scripts and programs; this helped to make sure that I actually knew what it was doing, and that I would know that in the future.

Something that annoys me is when I have to work on source code with a general dearth of comments. Apparently, all programmers enter a state where they become fluent in the language and no longer need an explanation in English; however, this doesn't last forever, and definitely causes an impediment for those who may take over the effort.

## Setting HTML to local folders

Originally, my plan was to automatically generate HTML from the JSON downloaded. However, perhaps the easier way was to download the HTML that 4chan already generated, and convert it to use the images the script already downloaded.

To do so, these find and replace functions converted absolute links to relative links to the downloaded images.

* `"//` -> `"http://`
* `http://images.4chan.org/\w/src/` -> `img/`
* `http://\d.thumbs.4chan.org/\w/thumb/` -> `thumb/`

### The function

To perform the regex, I needed a suitable function. Rather than reinvent the wheel, I borrowed code from StackOverflow.

    # Regex function originally by steveha on StackOverflow: 
    # http://stackoverflow.com/questions/1597649/replace-strings-in-files-by-python
    import re
    import os
    def file_replace(fname, pat, s_after):
    # first, see if the pattern is even in the file.
    with open(fname) as f:
        if not any(re.search(pat, line) for line in f):
        return # pattern does not occur in file so we are done.

    # pattern is in the file, so perform replace operation.
    with open(fname) as f:
        out_fname = fname + ".tmp"
        out = open(out_fname, "w")
        for line in f:
        out.write(re.sub(pat, s_after, line))
        out.close()
        os.rename(out_fname, fname)

## The Regex Expressions

This is the test file I created to work with the regex, known as `testfile.html`

    <html>"//images.4chan.org/k/src/4238749327.img"</html>
    <a="//9.thumbs.4chan.org/k/thumb/"<test>
    <"//static.4chan.org/css/jfoajweaf.478.css">
    <"//static.4chan.org/css/yuiyiiu.283.css">

So we can now use our regex.

    html_path = "testfile.html"
    file_replace(html_path, '"//', "http://")
    file_replace(html_path, "http://images.4chan.org/\w/src/", "img/")
    file_replace(html_path, "http://\d.thumbs.4chan.org/\w/thumb/", "thumb/")

## Downloading and linking to a local copy of the CSS

CSS can just stay linked to 4chan, but 4chan tends to change the CSS all the time, so it's a good idea to use a local snapshot for best compatiblity.

In the HTML of threads, they have some weird CSS number in addition, for some reason... It seems to be consistent, so we should have a copy locally.

Convert link to plain file path:

`http://static.4chan.org/css/(\w+).\d+.css` -> `css/\1.css`

### (FUTURE) Downloading a local copy of the CSS

We need to grab the names of all those css files, and use them to save a copy of the stylesheets locally under `css/`.

I used [this tutorial](http://palewi.re/posts/2008/04/05/python-recipe-open-a-file-read-through-it-print-each-line-matching-a-search-term/) and this [stackoverflow](http://stackoverflow.com/questions/6174825/getting-filenames-matching-an-extension-using-beautifulsoup) to understand how to grab all matching lines.

* Use beautifulsoup to find links with `<link href=>` tag

#### Function to find text in file

    # Return lines matching a regex, code by Ben Welsh
    # http://palewi.re/posts/2008/04/05/python-recipe-open-a-file-read-through-it-print-each-line-matching-a-search-term/
    # Notice: `\1` notation could be interpreted by python as `\x01`! Escape it with a second backslash: `\\1`
    def file_find(fname, pat)
    f = open(fname, "r")

    for line in f:
        if re.match(pat, line):
        print line,

### Regex for linking to a local copy of the CSS

The below regex used a `\1` replace, but it was giving me problems in python. Apparently, since this character was in a string literal, python converted the `\1` to a `\x01` character before it got to the regex replace function. The recommended way to send this raw string was to use `r"\1"`. However, since the function added an extra layer of abstraction,  there was no way to use that.

After hours of searching, the solution was to escape the `\1` with a backslash, resulting in `\\1`. When the string finally reached the replace function, it would be interpreted as `\1`.

    file_replace(html_path, "http://static.4chan.org/css/(\w+).\d+.css", "css/\\1.css")

## Pretty Print JSON

By adding `sort_keys=True, indent=2, separators=(',', ': ')` as arguments to the `json.dump()` function, we can make the JSON much more readable. It only takes a kilobyte or two extra, so it's worth it.

## Make a list of all external links quoted in comments

In the original version of the 4chandownloader script, the script would create a list of all rapidshare download links found in the thread; however, this function was removed when the new author transitioned to 4chan API.

Sometimes the external links form an integral part of the story, or contain links to filesharing services of interest. The user might want to download such files, or save those sites in case they go down.

I created a restored version that searches comments from the 4chan API and grabs all external URLs, rather than 3 filesharing sites. This set of commands is tacked to the image download loop. It then stores the URLs in an `external_links.txt` file subdivided with newlines, for the user to read or for `wget` to parse. 

This presents a challenge; 4chan generally does not allow certain URL links on their site (to combat spam), so users tend to write URLs in ways that fool the site's URL regex (insert spaces, etc). We need something that will pull in even those links.

[On DaringFireball](http://daringfireball.net/2010/07/improved_regex_for_matching_urls), there is a monster regex that will match nearly any URL. A version for Python can be found on [StackOverflow.](http://stackoverflow.com/questions/520031/whats-the-cleanest-way-to-extract-urls-from-a-string-using-python). We use this one.

Additionally, when rendering to HTML, 4chan often adds `<wbr>` tags, indicating an optional line break. This tag tends to end up in the middle of URLs, screwing them up. So this statement is added to get rid of them:

    # We need to get rid of all <wbr> tags before parsing
    cleaned_com = re.sub(r'\<wbr\>', '', post['com'])

## Using the py4chan API wrapper

After searching github repositories, I discovered that Edgeworth Euler of ED.ch fame created a python wrapper for the 4chan API. This simplified and replaced some of the messy code for handling JSON that I was using.

I had to upload the py4chan code to PyPI so that the entire library could be installed using `pip`.

py4chan had a very nice `Thread.Files()` function that returns all the URLs to images in the thread on 4chan. However, there was no equivalent for thumbnails, so I created a `Thread.Thumbs()` function to do so, and sent a pull request to the author.

py4chan allowed me to add a 404 checking subroutine, so that the script will stop if the thread is deleted or the user's connection drops.

I still maintain the original script as `4chan-thread-archiver-orig` and keep it up-to-date, just in case.

## Save to default path if a path is not given.

The original script required users to input a path. I believed that it should set a default path if none is given instead.

Because the argument didn't work otherwise, I changed the argument to use `[--path=<string>]` rather than `<path>`. Thanks to `docopts`, changing the parameters is a very easy and visual process.

The below code checks if the `path` argument is not given, and substitutes a default folder name. 

    if (path == None):
      path = os.path.join(os.getcwd() + os.path.sep + _DEFAULT_FOLDER)

The path is composed of the current working directory and the default folder name. Since `os.path.join` did not add a path seperator for some reason, I added my own with `os.path.sep`. This variable is used because Windows uses a `\` for path seperators, while Linux and Mac use `/`.

## (FUTURE) Moving the functions to a class, and making a GUI

## (FUTURE) Metadata file

The metadata file would be in JSON or YAML format, and contain information about the thread useful to a reader.

The script could prompt the user to add a title or quick description

## (FUTURE) Abstracted Interface and PyQt GUI

Something like the Chandler.

We would have to convert all the functions into a class, with a GUI and CLI interface script.

## (FUTURE) chan.zip file format

For ease of transmission, this script should give the ability to transfer in `.chan.zip` format. All this does is zip up the folder, just like an `.epub`; saving a bit of space. This will provide a universal archive format for transferring information between archives, or between anons on 4chan, which may happen a lot.

We don't have to restrict ourselves to `.zip`; in theory, we can use any archive format that is convenient. However, to reduce incompatibility, we should restrict ourselves to the best formats for the job: `.zip` and `.7z`

* `.zip` - PKZIP, the standard archive format for Windows-based systems.
* `.7z` or `.lzma` or `.xz` - LZMA, the open-source heavy compression format. It is the king of the archivers; however, it demands a lot more power and time than `.zip`, and may not be as suitable for mobile devices.
* `.tar.gz` and `.tar.bz2` - GNU zip and bzip2, the standard archive formats for Unix-based systems. The fundamental flaw of these formats is that they rely on `.tar`, an antiquated tape-backup archive format that does not allow straight file deletion. However, they do compress and decompress better than zip, despite generally using the same algorithm.

## (FUTURE) Implement useful functions from other CSS/JS mods

* Expand image in the current HTML
* IQDB/TinEye/Google/SauceNao

## (FUTURE) Fix backquotes

Javascript backquotes are broken; add a `.html` extension.

* Orig: `g/33013702/33013702#p33013796`
* Fix: `g/33013702/33013702.html#p33013796`

## (SOLVED) post['com'] key error bug

on these threads (which just happen to be stickies): <http://boards.4chan.org/k/res/14013417> <http://boards.4chan.org/g/res/33013702>

py4chan spits out this error:

    Traceback (most recent call last):
      File "4chan-thread-archiver", line 263, in <module>
    main(args)
      File "4chan-thread-archiver", line 243, in main
    list_external_links(curr_thread, dst_dir)
      File "4chan-thread-archiver", line 152, in list_external_links
    if not linkregex.search(reply.Comment):
      File "/usr/lib/python2.7/site-packages/py4chan/__init__.py", line 309, in Comment
    return self._data['com'] or None
    KeyError: 'com'
    
My script that doesn't use py4chan spits out this error:

    Traceback (most recent call last):
      File "4chan-thread-archiver-orig", line 239, in <module>
    main(args)
      File "4chan-thread-archiver-orig", line 218, in main
    get_files(dst_dir, board, thread, nothumbs, thumbsonly)
      File "4chan-thread-archiver-orig", line 191, in get_files
    list_external_links(json_thread, dst_dir)
      File "4chan-thread-archiver-orig", line 156, in list_external_links
    if not linkregex.search(post['com']):
    KeyError: 'com'
    
However, the in the Python interpreter, `Post.Comment` works fine.

    Python 2.7.3 (default, Feb 26 2013, 22:57:37) 
    [GCC 4.7.2] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import py4chan
    >>> k = py4chan.Board("k")
    >>> thread = k.getThread(14013417)
    >>> thread.Sticky
    True
    >>> reply = thread.replies[1]
    >>> reply.Comment
    u"Once you've chosen a frame size, <etc.> anyway."

Even without py4chan, the result is the same.

    >>> json_thread = requests.get(FOURCHAN_API_URL % (board, thread))
    >>> post = json_thread.json['posts'][0]
    >>> post['com']
    u'Welcome to /k/. In this thread you will find basic knowledge to get you to know weapons and how to use them safely plus some more detailed guides. All the useful information is gathered in the following infographics.<br><br>Safety is the most important thing so we will start with safety instructions.'
    
Checking the JSON, every single post has an associated `"com"` value, so there's no problem in the JSON itself. What is going on?

Finally, I inserted this statement into `list_external_links()` where the loop checks the comment field for links. Maybe it was choking on a certain post?

    for post in json_thread.json['posts']:
    print post['com']

The idea is that if the comment field existed, the loop would return the value of the comment all the way until it failed, and I could check that value to see what was up. Right after it printed the last comment, the script failed, and I checked what entry was right after the last working comment.

    {
      "ext": ".png",
      "filename": "1302620113762",
      "fsize": 1462132,
      "h": 1225,
      "md5": "wblCqtPMg5D6OdNXVIaN9w==",
      "name": "Anonymous",
      "no": 14013856,
      "now": "01/02/13(Wed)16:43",
      "resto": 14013417,
      "tim": 1357162982849,
      "time": 1357162982,
      "tn_h": 95,
      "tn_w": 125,
      "w": 1600
    }

I was right. This bug involved nonexistent `"com"` fields, which are theoretically optional on the [4chan API](); but in practice, it wasn't easy to trick 4chan into posting nothing. As a result, posts without comments were rare enough for me to forget about them.

Now I had to somehow handle nonexistent `"com"` fields in the program itself. Thanks to handy-dandy [StackOverflow](http://stackoverflow.com/questions/13606426/need-to-handle-keyerror-exception-python), I found that I could use a `try/except` loop or a special `if` statement. I already had a loop, so I added the `if` statement to my `list_external_links()` for loop.

`4chan-thread-archiver-orig`

    # comments are optional in 4chan API
    if "com" not in post:
    continue

And for the py4chan based one, I had to modify the library itself; the library was handling optional attributes incorrectly when polled. The pull request is below.
      
And now it finally dumps correctly!

### Pull request: BUG: Optional attributes aren't returning `None` when polled

Certain attributes in the 4chan API are optional and are not passed in the JSON. When an attribute does not exist for a post, the py4chan library should return the `None` object. 

Going by your code, you've tried to do that with this statement:

    return self._data['sub'] or None

However, it doesn't return `None` as expected when the attribute doesn't exist. It instead gives a `KeyError` that causes scripts to fail in a cryptic manner:

    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/usr/lib/python2.7/site-packages/py4chan/__init__.py", line 305, in Subject
    return self._data['sub'] or None
    KeyError: 'sub'

### Solution B

For some reason, the FileSize attribute uses this statement that returns `None` correctly:

    return self._data.get('fsize', None)

So I simply replaced the faulty statements with this one in this pull request. Now the error disappeared. 

Why wasn't this one used in the first place?

### Solution A (not used)

Another solution is to check if the attribute exists with a special `if` statement.

    if 'sub' not in self._data:
    return None
    else:
    return self._data['com']

And now the library works fine.
