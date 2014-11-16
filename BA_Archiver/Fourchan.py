# coding: utf-8
"""
    BA Archiver - 4chan Tools
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    ../BA_Archiver/Fourchan.py

    The Archiver class utilizes the py4chan wrapper for the 4chan API 
    to archive all json, html, images, and/or thumbnails of a 4chan thread.
    * Logs all events in a nice log file instead of printing to console
    * handles all the downloading and object setup and such

    Import the BA_Archiver using `import BA_Archiver.Fourchan`
    import a class using `obj = BA_Archiver.Fourchan.Archiver("a", "1234567", dst_dir)`

"""

import errno
import fileinput
import json
import re
import os

import requests
import py4chan

# Setup logging: http://victorlin.me/posts/2012/08/good-logging-practice-in-python/
import logging
logging.basicConfig(filename = "dump.log",
                    filemode = 'a',
                    format = '%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt = '%H:%M:%S',
                    level = logging.INFO)
logger = logging.getLogger(__name__)



"""=== 4chan URL Settings ==="""

""" 4chan top level domain names """
FOURCHAN_BOARDS = 'boards.4chan.org'
FOURCHAN_CDN = '4cdn.org'

"""
    4chan Content Delivery Network domain names
    (for images, thumbs, api)
"""
FOURCHAN_API = 'a.' + FOURCHAN_CDN
FOURCHAN_IMAGES = 'i.' + FOURCHAN_CDN
FOURCHAN_THUMBS = 't.' + FOURCHAN_CDN
FOURCHAN_STATIC = 's.' + FOURCHAN_CDN

"""
    Retrieval Footer Regex
    Format is (boards, object_id)
"""
FOURCHAN_BOARDS_FOOTER = '/%s/res/%s'
FOURCHAN_API_FOOTER = FOURCHAN_BOARDS_FOOTER + '.json'
FOURCHAN_IMAGES_FOOTER = '/%s/src/%s'
FOURCHAN_THUMBS_FOOTER = '/%s/thumb/%s'

"""
    Full HTTP Links to 4chan servers, without HTTP headers
    Used for creating download links.
"""
FOURCHAN_BOARDS_URL = FOURCHAN_BOARDS + FOURCHAN_BOARDS_FOOTER
FOURCHAN_API_URL = FOURCHAN_API + FOURCHAN_API_FOOTER
FOURCHAN_IMAGES_URL = FOURCHAN_IMAGES + FOURCHAN_IMAGES_FOOTER
FOURCHAN_THUMBS_URL = FOURCHAN_THUMBS + FOURCHAN_THUMBS_FOOTER

"""
    HTML Parsing Regex
    Matches links in dumped HTML.
"""
HTTP_HEADER_UNIV = r"https?://"          # works for both http and https links
FOURCHAN_IMAGES_REGEX = r"/\w+/src/"
FOURCHAN_THUMBS_REGEX = r"/\w+/thumb/"
FOURCHAN_CSS_REGEX = r"/css/(\w+)\.\d+.css"

"""
    Regex Links to 4chan servers, without HTTP headers
    Used to match and replace links in dumped HTML.
"""

FOURCHAN_IMAGES_URL_REGEX = re.compile(HTTP_HEADER_UNIV + FOURCHAN_IMAGES + FOURCHAN_IMAGES_REGEX)
FOURCHAN_THUMBS_URL_REGEX = re.compile(HTTP_HEADER_UNIV + "\d+." + FOURCHAN_THUMBS + FOURCHAN_THUMBS_REGEX)

"""=== Folder Structure Settings ==="""

""" default folder names for image and thumbnails """
_DEFAULT_FOLDER = "4chan"
_IMAGE_DIR_NAME = "images"
_THUMB_DIR_NAME = "thumbs"
_CSS_DIR_NAME = "css"

"""
    The Ultimate URL Regex
    <http://stackoverflow.com/questions/520031/whats-the-cleanest-way-to-extract-urls-from-a-string-using-python>
"""
URLREGEX = re.compile(r"""((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.‌​][a-z]{2,4}/)(?:[^\s()<>]+|(([^\s()<>]+|(([^\s()<>]+)))*))+(?:(([^\s()<>]+|(‌​([^\s()<>]+)))*)|[^\s`!()[]{};:'".,<>?«»“”‘’]))""", re.DOTALL)

""" external link filename """
EXT_LINKS_FILENAME = "external_links.txt"

def make_sure_path_exists(path):
    """
        Recursively create folder paths if they don't exist 
        (update) with `os.makedirs(path,exist_ok=True)` in python3
        :param path: os.path object to file

        >>> dst_dir = os.path.join(os.getcwd() + os.path.sep + "archives")
        >>> BA_Archiver.Fourchan.make_sure_path_exists()
        >>> # find some way to check if that path exists
    """
    try:
        logging.debug("Recursively creating folder path: " + path)
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            logging.error("The path " + path + " could not be created.")
            raise



def download_file(fname, dst_folder, file_url, overwrite=False):
    """
        Download any file using requests, in chunks.
        :param fname: filename string
        :param dst_folder: output folder string
        :param file_url: url to download from, string
        :param overwrite: Overwrite any existing files, bool

        # Try not to initialize object to download
        >>> dst_dir = os.path.join(os.getcwd() + os.path.sep + "archives")
        >>> BA_Archiver.Fourchan.download_file("12345.jpg", dst_dir, "http:/i.imgur.com/12345.jpg")
    """
    # Destination of downloaded file
    file_dst = os.path.join(dst_folder, fname)

    # If the file doesn't exist, download it
    if ( not os.path.exists(file_dst) ) or overwrite:
        logging.info('%s downloading...' % fname)
        i = requests.get(file_url)

        if i.status_code == 404:
            logging.info('Failed, try later (%s)' % file_url)
        else:
            # download file in chunks of 1KB
            with open(file_dst, 'wb') as fd:
                for chunk in i.iter_content(chunk_size=1024):
                    fd.write(chunk)

    else:
      logging.info('%s already downloaded' % fname)



def download_json(json_url, fname, dst_dir):
    """
        Download JSON to local file, pretty printed

        :param json_url: string, URL to download from
        :param fname: string, destination filename, no extension
        :param dst_dir: string, destination folder name
    """
    json_filename = "%s.json" % fname
    json_path = os.path.join(dst_dir, json_filename)
    print(_TAG + "Dumping %s...", json_filename)

    json_thread = requests.get(json_url)
    json.dump(json_thread.json(), open(json_path, 'w'), sort_keys=True, indent=2, separators=(',', ': '))



def file_replace(fname, pat, s_after):
    """
        File in place regex function, using fileinput
        Notice: all parameters are recommended to be in r"raw strings"

        :param fname: filename string
        :param pat: regex pattern to search for, as a string
        :param s_after: what to replace pattern in file with, string
    """

    for line in fileinput.input(fname, inplace=True):
        logging.info(re.sub(pat, s_after, line))



"""=== 4chan Archiver Class ==="""
class Archiver(object):
    def __init__(self, board, thread, https=False, logger = None):
        """
            Archiver Class Constructor, set up objects, logging,
            and any necessary variables
            :param dst_dir: string, destination folder
            :param board: string, board name
            :param thread: string, thread id

            # replace link with some SFW board's permanent sticky thread
            >>> dst_dir = os.path.join(os.getcwd() + os.path.sep + "archives")
            >>> curr_archiver = BA_Archiver.Fourchan.Archiver("a", "1234567", dst_dir)
        """
        # Setup logger
        self.logging = logger or logging.getLogger(__name__)

        # Copy parameters to object (should probably make constant and private)
        self.board = board
        self.thread = thread

        # HTTP header: use SSL when prompted
        self._https = https
        self.HTTP_HEADER = ('http://' if not https else 'https://')

        # Initialize py4chan Board object
        self.curr_board = py4chan.Board(board, https=self._https)

        # Check if the thread exists, then create py4chan thread object.
        try:
            if (self.curr_board.threadExists(int(thread))):
                self.curr_thread = self.curr_board.getThread(int(thread))
    #        if (self.curr_board.thread_exists(int(thread))):
    #            self.curr_thread = self.curr_board.get_thread(int(thread))       # BA py-4chan 0.3
            else:
                # log nonexistent thread
                self.logging.warning("Thread not found. curr_thread set to None")
                # set to Null object
                self.curr_thread = None
                # used to set Archiver object's nonexistent id property
                self.invalid_id = True
        # If thread could not be checked for any reason (typically connection error), set to Null
        except:
            # log failure to retrieve thread
            self.logging.warning("Could not connect to 4chan.org. curr_thread set to None")
            # set to Null object
            self.curr_thread = None
            # used to set Archiver object's nonexistent id property
            self.invalid_id = True


    @property
    def inaccessible(self):
        """
            Is the thread inaccessible?
            :return: bool

            >>> dst_dir = os.path.join(os.getcwd() + os.path.sep + "archives")
            >>> curr_archiver = BA_Archiver.Fourchan.Archiver("a", "1234567", dst_dir)
            >>> curr_archiver.inaccessible()
            True
        """
        return self.invalid_id

    @property
    def dumped_correctly(self):
        """
            Was the latest dump done correctly? Monitors the status.
            :return: bool

            >>> dst_dir = os.path.join(os.getcwd() + os.path.sep + "archives")
            >>> curr_archiver = BA_Archiver.Fourchan.Archiver("a", "1234567", dst_dir)
            >>> curr_archiver.dump()
            >>> curr_archiver.dumped_correctly()
            True
        """
        if (self.dump_complete):
            return True


    def dump_json(self, dst_dir):
        """
            Dump 4chan JSON to local file, pretty printed

            :param dst_dir: string, destination folder
            # variables from initialized object
            :param board: string, board name
            :param thread: string, thread id
        """
        json_url = self.HTTP_HEADER + FOURCHAN_API_URL % (self.board, self.thread)
        download_json(json_url, self.thread, dst_dir)



    def dump_css(self, dst_dir):
        """
            Dumps the CSS from 4cdn.
            (FIXME) Currently uses a static list of links, which works but is not ideal.
            Eventually, we need to create a JSON HTML Templater system.

            :param dst_dir: string, destination folder
        """
        fourchan_css_url_regex = re.compile(HTTP_HEADER_UNIV + FOURCHAN_STATIC + FOURCHAN_CSS_REGEX)

        # (FUTURE) Mod dump_css() to automatically scrape CSS links each time.
        css_list = [self.HTTP_HEADER + FOURCHAN_STATIC + "/css/yotsubluemobile.473.css",
        self.HTTP_HEADER + FOURCHAN_STATIC + "/css/yotsubluenew.473.css", 
        self.HTTP_HEADER + FOURCHAN_STATIC + "/css/yotsubanew.473.css", 
        self.HTTP_HEADER + FOURCHAN_STATIC + "/css/futabanew.473.css", 
        self.HTTP_HEADER + FOURCHAN_STATIC + "/css/burichannew.473.css", 
        self.HTTP_HEADER + FOURCHAN_STATIC + "/css/photon.473.css",
        self.HTTP_HEADER + FOURCHAN_STATIC + "/css/tomorrow.473.css"]

        for css_url in css_list:
            css_name = re.sub(fourchan_css_url_regex, r"\1.css", css_url)
            self.logging.info("Downloading %s" % (css_name))
            download_file(css_name, dst_dir, css_url)



    def dump_html(self, dst_dir):
        """
            Dumps thread in raw HTML format to `<thread-id>.html`

            :param dst_dir: string, destination folder
            # variables from initialized object
            :param board: string, board name
            :param thread: string, thread id
        """
        self.logging.info("Dumping/Converting HTML...")

        FOURCHAN_IMAGES_URL_REGEX = re.compile(HTTP_HEADER_UNIV + FOURCHAN_IMAGES + FOURCHAN_IMAGES_REGEX)
        FOURCHAN_THUMBS_URL_REGEX = re.compile(HTTP_HEADER_UNIV + "\d+." + FOURCHAN_THUMBS + FOURCHAN_THUMBS_REGEX)
        html_filename = "%s.html" % self.thread
        html_url = self.HTTP_HEADER + FOURCHAN_BOARDS_URL % (self.board, self.thread)
        download_file(html_filename, dst_dir, html_url, overwrite=True)

        # Convert all links in HTML dump to use locally downloaded files
        html_path = os.path.join(dst_dir, html_filename)
        file_replace(html_path, '"//', '"' + self.HTTP_HEADER)
        file_replace(html_path, FOURCHAN_IMAGES_URL_REGEX, _IMAGE_DIR_NAME + "/")
        file_replace(html_path, FOURCHAN_THUMBS_URL_REGEX, _THUMB_DIR_NAME + "/")

        # Download a local copy of all CSS files
        dst_css_dir = os.path.join(dst_dir, _CSS_DIR_NAME)
        make_sure_path_exists(dst_css_dir)
        self.dump_css(dst_css_dir)

        # convert HTML links to use local CSS files that we just downloaded
        # (FIXME) Might want to mod the HTML to use only ONE CSS file (perhaps by option)
        file_replace(html_path, HTTP_HEADER_UNIV + FOURCHAN_STATIC + FOURCHAN_CSS_REGEX, _CSS_DIR_NAME + r"/\1.css")



    def find_in_all_posts(self, regex, fname, dst_dir):
        """
            Find a regex pattern in all comments and record them in a file

            :param dst_dir: string, destination folder
            :param regex: re.compile() object pattern to look for
            :param fname: filename to write to
            # variables from initialized object
            :param curr_thread: py4chan Thread object
        """

        # File to store list of all external links quoted in comments (overwrite upon each loop iteration)
        listing_dst = os.path.join(dst_dir, fname)
        listing_file = open(listing_dst, "w")

        for reply in self.curr_thread.replies:
            if (reply.Comment == None):
                continue
            if not regex.search(reply.Comment):
                continue
            else:
                # We need to get rid of all <wbr> tags before parsing
                cleaned_com = re.sub(r'\<wbr\>', '', reply.Comment)
                listing = re.findall(regex, cleaned_com)
                for item in listing:
                    self.logging.info("Found URL, saving in %s:\n%s\n" % (listing_dst, item[0]))
                    listing_file.write(item[0])        # re.findall creates tuple
                    listing_file.write('\n')   # subdivide with newlines

        # Close linklist file after loop
        listing_file.close()



    def get_images(self, dst_dir):
        """
            Download all images
            :param curr_thread: py4chan Thread object
            :param dst_dir: string, destination folder
        """
        # Create and set destination folders
        dst_images_dir = os.path.join(dst_dir, _IMAGE_DIR_NAME)
        make_sure_path_exists(dst_images_dir)

#        for image_url in self.curr_thread.image_urls():
        for image_url in self.curr_thread.Files():
            image_name = re.sub(FOURCHAN_IMAGES_URL_REGEX, '', image_url)
            download_file(image_name, dst_images_dir, image_url)

    def get_thumbs(self, dst_dir):
        """
            Download all thumbnails
            :param curr_thread: py4chan Thread object
            :param dst_dir: string, destination folder
        """
        # Create and set destination folders
        dst_thumbs_dir = os.path.join(dst_dir, _THUMB_DIR_NAME)
        make_sure_path_exists(dst_thumbs_dir)

        # Dump all thumbnails within a thread from 4chan
#        for thumb_url in self.curr_thread.thumb_urls():
        for thumb_url in self.curr_thread.Thumbs():
            thumb_name = re.sub(FOURCHAN_THUMBS_URL_REGEX, '', thumb_url)
            download_file(thumb_name, dst_thumbs_dir, thumb_url)



    def dump(self, dst_dir, nothumbs=False, thumbsonly=False):
        """ 
            Dump the thread using the functions defined above
            :param dst_dir: string, destination folder
            :param nothumbs: bool, get thumbnails or not. (optional)
            :param thumbsonly: bool, only get thumbnails. (optional)

            >>> dst_dir = os.path.join(os.getcwd() + os.path.sep + "archives")
            >>> curr_archiver = BA_Archiver.Fourchan.Archiver("a", "1234567", dst_dir)
            >>> curr_archiver.dump()
            >>> curr_archiver.dump(thumbsonly=True)
            # find some way to verify that the thread was dumped

        """
        # Create paths if they don't exist
        make_sure_path_exists(dst_dir)

        # log current thumbsonly or nothumbs value
        if (thumbsonly):
            self.logging.info("--thumbsonly : " + thumbsonly)

        if (nothumbs):
            self.logging.info("--nothumbs : " + nothumbs)

        # Choose whether to download images
        if (thumbsonly == False):
            self.get_images(dst_dir)

        # Choose whether to download thumbnails
        if (thumbsonly or (nothumbs == False)):
            self.get_thumbs(dst_dir)

        # Get all external links quoted in comments
        self.find_in_all_posts(URL_REGEX, EXT_LINKS_FILENAME, dst_dir)

        # Dumps thread in raw HTML format to `<thread-id>.html`
        self.dump_html(dst_dir)

        # Dumps thread in JSON format to `<thread-id>.json` file, pretty printed
        self.dump_json(dst_dir)

    def __repr__(self):
        return '<BA_Archiver.Fourchan - /Board/Thread: /%s/%s>' % (self.board, self.thread)