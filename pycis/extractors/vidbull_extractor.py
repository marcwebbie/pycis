import logging
import re
import sys

from pyquery import PyQuery

from .base_extractor import BaseExtractor
from pycis import utils


class VidbullExtractor(BaseExtractor):

    """ vidbull.com extractor
    """

    def __init__(self):
        # super().__init__(self)
        super(VidbullExtractor, self).__init__()
        self.host_list = ["vidbull.com"]
        self.holder_url = "http://vidbull.com/embed-{}-650x328.html"
        self.regex_url = re.compile(
            r'http(s)?\://(www\.)?(?P<host>vidbull\.com)/(embed\-)?(?P<id>\w+)(\-\w+(\.html)?)'
        )
        self.example_urls = ["http://vidbull.com/embed-hkvelwsmgsm0-650x328.html"]

    @staticmethod
    def baseconv(number, base=36):
        alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'.lower()
        result = ''
        while number:
            number, i = divmod(number, base)
            result = alphabet[i] + result

        return result or alphabet[0]

    @staticmethod
    def unpacker(p, a, c, k, e=None, d=None):
        for c in reversed(range(c)):
            if(k[c]):
                p = re.sub(r'\b' + VidbullExtractor.baseconv(c, base=a) + r'\b', k[c], p)
        return p

    def get_raw_url(self, video_id_or_url, show_progress=False):
        video_id = None
        if self.regex_url.match(video_id_or_url):
            video_id = self.regex_url.match(video_id_or_url).group('id')
        else:
            video_id = video_id_or_url
        dest_url = self.holder_url.format(video_id)

        logging.info("Destination url {}".format(dest_url))

        html_embed = None
        try:
            html_embed = utils.fetch_page(dest_url)
        except:
            logging.error("Couldn't fetch page at url: {}".format(dest_url))

        # get script with the packed eval function
        pq = PyQuery(html_embed)
        script_text_raw = pq('#player_code script:not([src])').text()
        script_text = re.sub(r'\\', '', str(script_text_raw))

        rgx = re.compile(r"}\('(.+)',(\d+),(\d+),'([\w|]+)'")

        try:
            parg1 = re.search(rgx, script_text).group(1)
            parg2 = int(re.search(rgx, script_text).group(2))
            parg3 = int(re.search(rgx, script_text).group(3))
            parg4 = re.search(rgx, script_text).group(4).split('|')
        except:
            logging.info('Error trying to parse script text')
            return None
        try:
            unpacked_vars = self.unpacker(parg1, parg2, parg3, parg4)
        except:
            logging.info('Error trying unpack script text')
            return None
        try:
            url_found = re.search(r'file:"([\w\.:/\-_]+)"', unpacked_vars).group(1)
        except:
            logging.info('Error file url_found url not found in script unpacked')
            return None

        if show_progress:
            if url_found:
                sys.stdout.write('.')
            else:
                sys.stdout.write('F')
            sys.stdout.flush()

        return url_found
