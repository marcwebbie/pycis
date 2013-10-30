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
from .utils import fetch_page
from pycis.items import Media, Film


class TubeplusWrapper(BaseWrapper):

    def __init__(self):
        self.site_url = "http://www.tubeplus.me"

    def get_streams(self):
        pass

    def search(self, search_query):
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

            film = Film(title=title, url=url)

            # set description
            desc = pq(dom_item).find('.plot').text()
            film.description = re.sub(r'\s', ' ', str(desc))  # remove newlines from description
            film.rating = pq(dom_item).find('span.rank_value').text()

            # set thumbnail url
            href_thumbnail = pq(dom_item).find('img[border="0"]').show().attr('src')
            film.thumbnail = urljoin(self.site_url, href_thumbnail)

            film_list.append(film)

        return film_list

    def index(self):
        pass
