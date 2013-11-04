import os
import glob


__all__ = [os.path.basename(f)[:-3]
           for f in glob.glob(os.path.dirname(__file__) + "/*.py")]


def _import_all_extractor_files():
    __import__(__name__, globals(), locals(), __all__, 0)


def get_extractor_instances():
    """ Get all classes with names ending with 'Extractor' from
    the module extractors directory
    instantiate it and return a list with all the instances
    """
    _import_all_extractor_files()

    extractor_instance_list = []
    for mod in [v for k, v in globals().items() if k in __all__]:
        extractor_instance_list += [getattr(mod, klass)()
                                    for klass in dir(mod)
                                    if klass.endswith("Extractor")
                                    and klass != "BaseExtractor"]
    return extractor_instance_list


def get_extractor(name):
    for extractor in get_extractor_instances():
        if extractor.name == name:
            return extractor


def get_from_host(host):
    for extractor in get_extractor_instances():
        if host in extractor.host_list:
            return extractor


def get_from_url(url):
    for extractor in get_extractor_instances():
        if extractor.is_valid_url(url):
            return extractor
