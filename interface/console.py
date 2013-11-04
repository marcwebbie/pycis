import argparse
import logging
from queue import Queue
import sys
import os
from threading import Thread


console_file_path = os.path.realpath(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(console_file_path)))

from pycis import extractors
from pycis import wrappers

dl_queue = Queue()
num_of_workers = 5
final_url_list = []


def get_args():
    aparser = argparse.ArgumentParser()

    aparser.add_argument(
        "--site", default="tubeplus",
        help="Stream site name (example: -c streamsite)"
    )
    aparser.add_argument("-V", "--verbose", action="store_true", help="verbose output")
    aparser.add_argument("-w", "--workers",  action="store",
                         type=int, default=5, help="number of download workers")
    aparser.add_argument(
        "-s", "--search", help="Do a search and get best match")
    aparser.add_argument(
        "-d", "--download", help="What item code to download")
    args = aparser.parse_args()
    return args


def download(q):
    st = q.get()
    logging.info("init downloading: Stream(host={}, id={}) ...".format(st.host, st.id))
    ext = extractors.get_from_host(st.host)
    raw_url = ext.get_raw_url(st.id)
    logging.info("finished downloading: Stream(host={}, id={}) ...".format(st.host, st.id))
    final_url_list.append(raw_url)
    q.task_done()


if __name__ == "__main__":

    args = get_args()

    if args.verbose:
        logging.basicConfig(
            format="{levelname}:{thread:#x}:{module}:{funcName}:{message}",
            style='{',
            level=logging.DEBUG)

    num_of_workers = args.workers

    site = wrappers.get_wrapper(args.site)

    # Set up some workers
    for i in range(num_of_workers):
        worker = Thread(target=download, args=(dl_queue,))
        worker.setDaemon(True)
        worker.start()
        logging.info("started worker: {}".format(i + 1))

    search_query = args.search
    dl_choice = args.download

    # =================================================================
    # =================================================================
    # from timeit import timeit
    # time_search = "Function: {}, Time: {}".format('site.search',
    #                                               timeit(
    #                                                   'site.search("vampire diaries", best_match=True)',
    #                                               setup='from __main__ import site', number=1)
    #                                               )
    # print(time_search)

    # time_old_search = "Function: {}, Time: {}".format('site.old_search',
    #                                                   timeit(
    #                                                       'site.old_search("vampire diaries", best_match=True)',
    #                                                   setup='from __main__ import site', number=1)
    #                                                   )
    # print(time_old_search)
    # =================================================================
    # =================================================================

    logging.info('searching: [%s]...' % search_query)
    media_matched = site.search(search_query, best_match=True)

    logging.info('getting children for: [%s]...' % media_matched)
    media_children = site.get_children(media_matched)

    logging.info('getting episode: [%s]...' % dl_choice)
    episode = None
    for c in media_children:
        if c.code == dl_choice:
            episode = c

    logging.info('getting streams for: [%s]...' % episode)
    streams = site.get_streams(episode)

    logging.info("getting urls for: [%s]..." % episode)
    url_list = []
    for st in streams:
        ext = extractors.get_from_host(st.host)
        if ext:
            logging.info("extracting url for: Stream(host={}, id={})".format(st.host, st.id))
            dl_queue.put(st)

    dl_queue.join()

    print("\n".join(final_url_list))
