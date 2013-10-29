from .base_wrapper import BaseWrapper
from .utils import fetch_page


class ArchiveWrapper(BaseWrapper):

    def __init__(self):
        self.site_url = "http://archive.org"

    def search(self, search_query):
        return []
