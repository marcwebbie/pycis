from .base_wrapper import BaseWrapper
from .utils import fetch_page
from pycis.items import Media


class ArchiveWrapper(BaseWrapper):

    def __init__(self):
        self.site_url = "http://archive.org"

    def search(self, search_query):
        return [Media("search_query", "http://archive")]
