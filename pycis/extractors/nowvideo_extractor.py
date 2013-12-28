import logging
import re
import sys

if sys.version_info < (3, 0):
    from urllib import urlencode
else:
    from urllib.parse import urlencode

from .base_extractor import BaseExtractor


class NowVideoExtractor(BaseExtractor):

    """ nowvideo.sx extractor
    """

    def __init__(self):
        # super().__init__(self)
        super(NowVideoExtractor, self).__init__()
        self.host_list = ["nowvideo.eu", "nowvideo.ch"]
        self.holder_url = "http://embed.nowvideo.sx/embed.php?v={}"
        self.regex_url = re.compile(
            r'http(s)?\://(embed\.|www\.)?(?P<host>nowvideo\.(ws|sx|ch))/((embed\.php\?v\=)|(video/))(?P<id>\w+)'
        )
        self.example_urls = ["http://www.nowvideo.ws/video/12e4587e327fa",
                             "http://embed.nowvideo.sx/embed.php?v=hanu11wjzx2d7&width=650&height=510"]

    def get_raw_url(self, video_id_or_url, show_progress=False):
        video_id = None
        if self.regex_url.match(video_id_or_url):
            video_id = self.regex_url.match(video_id_or_url).group('id')
        else:
            video_id = video_id_or_url

        dest_url = self.holder_url.format(video_id)
        logging.info("Destination url {}".format(dest_url))

        html_embed = str(self.fetch_page(dest_url))

        # find "key" query param
        qparam_key = re.search(r'fkzd=["|\'](?P<key>[\w\s\.\-]+)["|\']', html_embed).group('key')

        # find "file" query param
        qparam_file = video_id
        # qparam_file = re.search(
        #     r'flashvars.file[\s=]+["|\'](?P<file>[\w]+)', html_embed).group('file')

        qparams = {
            "key": qparam_key,
            "file": qparam_file,
            "cid": "undefined",
            "cid2": "undefined",
            "cid3": "undefined",
            "user": "undefined",
            "pass": "undefined",
        }

        # build api request url with params to api
        api_url = "http://www.nowvideo.sx/api/player.api.php?{}".format(urlencode(qparams))

        # fetch response with containing raw url
        html_response = str(self.fetch_page(api_url))

        url_found = None
        try:
            rgx = re.compile(r'url=(?P<rurl>http://[\w\.\-/&=?]+\.flv|mp4|avi|mk4|m4a)')
            url_found = re.search(rgx, html_response).group('rurl')
        except (IndexError, AttributeError):
            logging.info('url was not found in response: {}'.format(html_response))

        if show_progress:
            if url_found:
                sys.stdout.write('.')
            else:
                sys.stdout.write('F')
            sys.stdout.flush()

        return url_found
