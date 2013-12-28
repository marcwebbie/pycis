import sys
if sys.version_info > (3, 0):
    from urllib.parse import urljoin
else:
    # fallback to python2
    from urlparse import urljoin

import requests


def fetch_page(url, extra_path=None):
    """Download page using default user agent, read it and return its content
    If extra_path is given, it appends this path to url before request
    """
    if extra_path:
        url = urljoin(url, extra_path)
    response = requests.get(url)
    return response.text


def debug_break(func):
    """ Decorator to break in the first line of decorated function
    """

    from functools import wraps
    import pdb

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = pdb.runcall(func, *args, **kwargs)
        return result
    return wrapper
