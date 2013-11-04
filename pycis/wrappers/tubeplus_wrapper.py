import logging
import re
import sys

if sys.version_info > (3, 0):
    from urllib.parse import quote_plus, urljoin
else:
    # fallback to python2
    from urllib import quote_plus
    from urlparse import urljoin

from pyquery import PyQuery

from .base_wrapper import BaseWrapper
from pycis.utils import fetch_page, debug_break
from pycis.items import Media, Film, Stream, TvShow


class TubeplusWrapper(BaseWrapper):

    def __init__(self):
        self.site_url = "http://www.tubeplus.me"

    def get_streams(self, media):
        logging.info("Extracting: {}".format(media))

        if not media.url:
            logging.warn("{} has no url".format(media))
            return None

        media_page = fetch_page(media.url)
        pq = PyQuery(media_page)

        stream_list = []

        # extract video id and video host name from href links
        # from page fetched by media url
        href_rgx = re.compile(
            r"'(?P<vid>[\w\.:/\?\=\&]+)'[\s,]+'(?:[\w\s\-\":,\.`´\\]+)?'[\s,]+'(?P<host>[\w\.]+)'"
        )
        for href in (a.attrib.get('href') for a in pq('#links_list .link a:not([class])')):
            try:
                video_url = href
                video_host = href_rgx.search(href).group('host')
                video_id = href_rgx.search(href).group('vid')

                stream = Stream(video_id, video_host, video_url)
                logging.info("Found {} for {}".format(stream, media))

                stream_list.append(stream)
            except AttributeError:
                # if an exception occured the href_rgx couldn't match something on href
                logging.error("Couldn't get video info from: {}".format(href))
                pass

        return stream_list

    def get_children(self, media):
        logging.info('Searching children for media: {}'.format(media))

        if sys.version_info > (3, 0):
            from html.parser import HTMLParser
            from urllib.parse import unquote
        else:
            from HTMLParser import HTMLParser
            from urllib2 import unquote

        media_page = fetch_page(media.url)
        pq = PyQuery(media_page)

        rgx = re.compile(
            r"/player/\d+/(?P<serie>\w+)/season_(?P<season>\d+)/episode_(?P<episode>\d+)/(?P<title>[\w´`\'\",\.]+)")
        links = [a.attrib.get('href') for a in pq('.seasons[href]')]

        # build episodes
        episode_list = []
        for link in links:
            title = re.search(rgx, link).group('title')
            title = re.sub('_', ' ', title)
            url = urljoin(self.site_url, link)

            episode = TvShow(title=title, url=url)

            link = HTMLParser().unescape(unquote(link))
            episode.episode_num = int(re.search(rgx, link).group('episode'))
            episode.season_num = int(re.search(rgx, link).group('season'))

            episode_list.append(episode)

        return episode_list

    def search_film(self, search_query):
        logging.info('Searching film for query: {}'.format(search_query))

        search_url = "/search/movies/" + quote_plus(search_query)
        search_page = fetch_page(self.site_url, extra_path=search_url)
        pq = PyQuery(search_page)

        dom_search_list = pq(".list_item")
        film_list = []
        for dom_item in dom_search_list:
            title = pq(dom_item).find('img[border="0"]').show().attr('alt')
            href = pq(dom_item).find('a.panel').attr('href')
            url = urljoin(self.site_url, href)

            film = Media(title=title, url=url)

            # set description
            desc = pq(dom_item).find('.plot').text()
            film.description = re.sub(r'\s', ' ', str(desc))  # remove newlines from description
            film.rating = pq(dom_item).find('span.rank_value').text()

            # set thumbnail url
            href_thumbnail = pq(dom_item).find('img[border="0"]').show().attr('src')
            film.thumbnail = urljoin(self.site_url, href_thumbnail)

            film_list.append(film)

        return film_list

    def search_tvshow(self, search_query):
        logging.info('Searching tvshow for query: {}'.format(search_query))

        search_url = "/search/tv-shows/" + quote_plus(search_query)
        search_page = fetch_page(self.site_url, extra_path=search_url)
        pq = PyQuery(search_page)

        dom_search_list = pq(u".list_item")
        tvshow_list = []

        for dom_item in dom_search_list:
            title = pq(dom_item).find('img[border="0"]').show().attr('alt')
            href = pq(dom_item).find('a.panel').attr('href')
            url = urljoin(self.site_url, href)

            # Since it is a tvshow we need to fetch the children episodes
            tvshow = Media(title=title, url=url, has_children=True)

            # set description
            desc = pq(dom_item).find('.plot').text()
            tvshow.description = re.sub('\s', ' ', str(desc))  # remove newlines from description

            # set rating
            tvshow.rating = pq(dom_item).find('span.rank_value').text()

            # set thumbnail url
            href_thumbnail = pq(dom_item).find('img[border="0"]').show().attr('src')
            tvshow.thumbnail = urljoin(self.site_url, href_thumbnail)

            tvshow_list.append(tvshow)

        return tvshow_list

    def search(self, search_query, best_match=False):
        media_list = self.search_film(search_query)
        media_list.extend(self.search_tvshow(search_query))

        if best_match == True:
            if media_list:
                from difflib import SequenceMatcher as sq
                return max((m for m in media_list),
                           key=lambda x: sq(None, search_query, x.title).quick_ratio())
            else:
                return None

        return media_list

    def index(self):
        pass
