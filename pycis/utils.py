import sys
if sys.version_info > (3, 0):
    from urllib.request import urlopen, Request
    from urllib.parse import urljoin
else:
    # fallback to python2
    from urllib2 import urlopen, Request
    from urlparse import urljoin


def fetch_page(url, extra_path=None):
    """ Download page using default user agent, read it and return its content

    If extra_path is given, it appends this path to url before request 
    """

    if extra_path:
        url = urljoin(url, extra_path)

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0'
    headers = {'User-Agent': user_agent}
    req = Request(url, data=None, headers=headers)
    response = urlopen(req)
    content = response.read()
    return content


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
