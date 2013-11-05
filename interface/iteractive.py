import cmd
from collections import namedtuple
import os
import sys
from threading import Thread
from queue import Queue

console_file_path = os.path.realpath(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(console_file_path)))

from pycis import extractors
from pycis import wrappers


def download(q):
    while True:
        st = q.get()

        try:
            ext = extractors.get_from_host(st.host)
            raw_url = ext.get_raw_url(st.id) if ext else None
            if raw_url:
                sys.stdout.write(raw_url)
                sys.stdout.write('\n')
                sys.stdout.flush()
        except:
            pass

        q.task_done()


class Color(object):
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    END = "\033[0m"


def set_color(s, color):
    return "{}{}{}".format(color, s, Color.END)


class IteractiveConsole(cmd.Cmd):

    """ Iterative mode console for searching """

    def __init__(self, site, num_of_workers=5):
        super().__init__()
        self.choice_list = []
        self.stream_queue = Queue()
        self.site = wrappers.get_wrapper(site)

        # set up workers
        for i in range(num_of_workers):
            worker = Thread(target=download, args=(self.stream_queue,))
            worker.setDaemon(True)
            worker.start()
            # logging.critical("started worker: {}".format(i + 1))

    def populate_choice_list(self, media_list):
        """Add list of Media as choice items to choice_list list
        """

        self.choice_list.clear()

        if not media_list:
            return

        for idx, media in enumerate(media_list):
            item = namedtuple("Item", "code media title category rating")
            if media.code:
                item.code = media.code
            else:
                item.code = str(idx)

            item.media = media
            item.title = media.title
            item.category = media.category
            item.rating = media.rating

            self.choice_list.append(item)

    def do_search(self, search_query):
        """Search streams for active site with a given query
        """

        print("Searching: {}".format(set_color(search_query, Color.BLUE)))

        media_list = self.site.search(search_query)
        self.populate_choice_list(media_list)
        self.do_choices()

    def do_search_film(self, search_query):
        """Search films for active site with a given query
        """

        print("Searching film: {}".format(set_color(search_query, Color.BLUE)))

        media_list = []
        try:

            media_list = self.site.search_film(search_query)
        except AttributeError:
            print(set_color("Site doesn't support film search", Color.RED))
        self.populate_choice_list(media_list)
        self.do_choices()

    def do_search_tvshow(self, search_query):
        """Search tvshows for active site with a given query
        """

        print("Searching tv show: {}".format(set_color(search_query, Color.BLUE)))

        media_list = []
        try:
            media_list = self.site.search_tvshow(search_query)
        except AttributeError:
            print(set_color("Site doesn't support tv show search", Color.RED))
        self.populate_choice_list(media_list)
        self.do_choices()

    def do_search_song(self, search_query):
        """Search songs for active site with a given query
        """

        print("Searching song: {}".format(set_color(search_query, Color.BLUE)))

        media_list = []
        try:
            media_list = self.site.search_song(search_query)
        except AttributeError:
            print(set_color("Site doesn't support song search", Color.RED))
        self.populate_choice_list(media_list)
        self.do_choices()

    def do_get(self, code):
        """Get an item from choice list by code chosen
        """

        choice = next((i for i in self.choice_list if i.code == code), None)

        if not choice:
            return

        print("chosen: {}".format(set_color(choice.title, Color.BLUE)))

        if choice.media.has_children:
            media_list = self.site.get_children(choice.media)
            self.populate_choice_list(media_list)
            self.do_choices()
        else:
            stream_list = self.site.get_streams(choice.media)
            for stream in stream_list:
                self.stream_queue.put(stream)

            self.stream_queue.join()

    def do_choice(self, line):
        """Same as command 'get'
        """

    def do_choices(self, line=None):
        """Print choice list
        """

        plist = []
        fstr = "[{0}] {1} [{2}, Rating: {3}]"
        for i in self.choice_list:
            plist.append(fstr.format(
                set_color(i.code, Color.GREEN),
                i.title,
                set_color(i.category, Color.GREEN),
                set_color(i.rating, Color.YELLOW)
            ))

        print('\n'.join(plist))

    def do_sites(self, line=None):
        """Print a list of available sites
        """

        print("======= Available sites ========")
        wrapper_list = wrappers.get_wrapper_list()
        for w in wrapper_list:
            if w.name == self.site.name:
                print(set_color(w.name, Color.YELLOW) + "[selected]")
            else:
                print(w.name)
        print()

    def do_exit(self, line):
        """Quit program
        """
        print("")
        return True

    def do_EOF(self, line):
        """Quit program"""
        print("")
        return True


def main():
    iconsole = IteractiveConsole("tubeplus")
    iconsole.prompt = "(pycis) "
    iconsole.cmdloop()

if __name__ == '__main__':
    main()
