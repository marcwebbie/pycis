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
    while True:
        st = q.get()
        logging.info("init downloading: Stream(host={}, id={}) ...".format(st.host, st.id))
        ext = extractors.get_from_host(st.host)
        raw_url = ext.get_raw_url(st.id)
        logging.info("finished downloading: Stream(host={}, id={}) ...".format(st.host, st.id))
        if raw_url:
            # final_url_list.append(raw_url)
            sys.stdout.write(raw_url)
            sys.stdout.write('\n')
            sys.stdout.flush()
        q.task_done()

dl_queue = Queue()


def main():
    args = get_args()

    # setup log level
    if args.verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.CRITICAL

    logging.basicConfig(
        format="{levelname}:{thread:#x}:{module}:{funcName}:{message}",
        style='{',
        level=log_level)

    # Set up some workers
    num_of_workers = args.workers
    for i in range(num_of_workers):
        worker = Thread(target=download, args=(dl_queue,))
        worker.setDaemon(True)
        worker.start()
        logging.info("started worker: {}".format(i + 1))

    site = wrappers.get_wrapper(args.site)

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
    if not media_matched:
        return

    logging.info('getting children for: [%s]...' % media_matched)
    media_children = site.get_children(media_matched)
    if not media_children:
        return

    logging.info('getting episode: [%s]...' % dl_choice)
    episode = None
    for c in media_children:
        if c.code == dl_choice:
            episode = c

    if not episode:
        return

    logging.info('getting streams for: [%s]...' % episode)
    streams = site.get_streams(episode)
    if not streams:
        return

    logging.info("getting urls for: [%s]..." % episode)
    url_list = []
    for st in streams:
        ext = extractors.get_from_host(st.host)
        if ext:
            logging.info("extracting url for: Stream(host={}, id={})".format(st.host, st.id))
            dl_queue.put(st)

    dl_queue.join()
    print("")


if __name__ == "__main__":
    main()
