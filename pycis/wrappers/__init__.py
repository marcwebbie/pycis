import os
import glob


__all__ = [os.path.basename(f)[:-3]
           for f in glob.glob(os.path.dirname(__file__) + "/*.py")]


def _import_all_crawler_files():
    __import__(__name__, globals(), locals(), __all__, 0)


def get_wrapper_list():
    """ Get all classes with names ending with 'Wrapper' from
    the module extractors directory
    instantiate it and return a list with all the instances
    """
    _import_all_crawler_files()

    wrapper_instance_list = []
    for mod in [v for k, v in globals().items() if k in __all__]:
        wrapper_instance_list += [getattr(mod, klass)()
                                  for klass in dir(mod)
                                  if klass.endswith("Wrapper")
                                  and klass != "BaseWrapper"]
    return wrapper_instance_list


def get_wrapper(name):
    for wrapper in get_wrapper_list():
        if wrapper.name == name:
            return wrapper
