try:
    from urllib.request import urlopen, Request
except:
    # fallback to python2
    from urllib2 import urlopen, Request


def fetch_page(url):
    """ Download page using default user agent, read it and return its content
    """

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0'
    headers = {'User-Agent': user_agent}
    req = Request(url, data=None, headers=headers)
    response = urlopen(req)
    content = response.read()
    return content
