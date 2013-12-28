import argparse
import logging
import sys
import os
from threading import Thread

if sys.version_info > (3,):
    from queue import Queue
else:
    # fallback to python2
    from Queue import Queue

console_file_path = os.path.realpath(os.path.abspath(__file__))
sys.path.append(os.path.dirname(console_file_path))
sys.path.append(os.path.dirname(os.path.dirname(console_file_path)))

import extractors
import wrappers
from utils import debug_break


dl_queue = Queue()
result_list = []


class LogFormatter(logging.Formatter):
    color = {
        "HEADER": '\033[95m',       # magenta
        "DEBUG": '\033[94m',        # blue
        "INFO": '\033[92m',         # green
        "WARNING": '\033[93m',      # yellow
        "WARN": '\033[93m',         # yellow
        "ERROR": '\033[91m',        # red
        "CRITICAL": '\033[41m',     # background red
        "FATAL": '\033[41m',        # background red
        "ENDC": '\033[0m',          # end formatting
    }

    def format(self, record):
        final_msg = super(LogFormatter, self).format(record)

        level = record.__dict__['levelname']
        return LogFormatter.color[level] + final_msg + LogFormatter.color['ENDC']


def get_args():
    aparser = argparse.ArgumentParser()

    aparser.add_argument("--site", default="tubeplus", help="stream site name (example: --site streamsite)")
    aparser.add_argument("-vv", "--verbose", action="store_true", help="verbose output for debugging")
    aparser.add_argument("-w", "--workers", action="store", type=int, default=5, help="number of download workers")
    aparser.add_argument("-s", "--search", help="search site, prints result, ex: '-s Vampire Diaries'")
    aparser.add_argument("-de", "--download-episode", help="code from episode to download, ex: '-de s01e02'")
    aparser.add_argument("-x", "--extract", help="extract raw url from a given url")
    aparser.add_argument("-p", "--play", action="store_true", help="play video using vlc or ffplay")
    aparser.add_argument("--player", default="vlc", help="specify the player to use for the --play option, ex: --player vlc")
    args = aparser.parse_args()

    return args


def download(q, print_url=True):
    while True:
        stream = q.get()
        logging.debug("init downloading: Stream(host={0.host}, id={0.id}, url={0.url})".format(stream))
        # try:
        try:
            extractor = extractors.get_from_host(stream.host)
        except TypeError:
            logging.debug("Couldn't get extractor by host for stream: {0}".format(stream))
            try:
                extractor = extractors.get_from_url(stream.url)
            except TypeError:
                logging.debug("Couldn't get extractor by host for stream: {0}".format(stream))
                logging.error("Error when extracting url for stream: {0}".format(stream))

        if extractor:
            raw_url = extractor.get_raw_url(stream.id if stream.id else stream.url)
            if raw_url:
                if print_url:
                    sys.stdout.write(raw_url)
                    sys.stdout.write('\n')
                    sys.stdout.flush()
                else:
                    result_list.append(raw_url)
                logging.debug("finished downloading: Stream(host={}, id={}) ...".format(stream.host, stream.id))

        q.task_done()


def spawn_workers(num_of_workers, print_url=True):
    for i in range(num_of_workers):
        worker = Thread(target=download, args=(dl_queue, print_url,))
        worker.daemon = True
        worker.start()
        logging.debug("started worker: {}".format(i + 1))


def go_download_episode(args):
    site = wrappers.get_wrapper(args.site)
    search_query = args.search
    search_list = site.search_tvshow(search_query)

    if not search_list:
        logging.info('No media found for: [%s]...' % search_query)
        return 0

    for media in search_list:
        episodes = site.get_children(media)
        episode_code = args.download_episode
        if episodes and next((e for e in episodes if e.code == episode_code), False):
            episode_found = next(e for e in episodes if e.code == episode_code)
            for stream in site.get_streams(episode_found):
                dl_queue.put(stream)

            # Found an episode then join the queue and return
            return


def go_extract(args):
    from pycis.items import Stream
    url = args.extract
    stream = Stream(url=url, id=None, host=None)
    dl_queue.put(stream)

    return


def go_play(args):
    import subprocess

    for url in result_list:
        command = [args.player, url]
        ret_value = subprocess.check_output(command, stderr=open(os.devnull))
        break


def go_print_search_list(args):
    site = wrappers.get_wrapper(args.site)
    search_query = args.search
    search_list = site.search(search_query)

    for media in search_list:
        sys.stdout.write("[{0.category}] {0.title} - {0.url}\n".format(media))
        sys.stdout.flush()


def main():
    args = get_args()

    # Setup logger
    root = logging.getLogger()
    handler = logging.StreamHandler()
    bf = LogFormatter('%(levelname)s:%(module)s:%(message)s')
    handler.setFormatter(bf)
    root.addHandler(handler)
    if args.verbose:
        root.setLevel(logging.DEBUG)
    else:
        root.setLevel(logging.CRITICAL)

    # Setup thread workers
    print_url = True if not args.play else False
    spawn_workers(num_of_workers=args.workers, print_url=print_url)

    if args.extract:
        go_extract(args)
    elif args.search and args.download_episode:
        go_download_episode(args)
    elif args.search and not args.download_episode:
        go_print_search_list(args)
    else:
        import iteractive
        iteractive.main()

    dl_queue.join()

    if args.play:
        go_play(args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
