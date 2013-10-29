import logging
import os
import sys
import unittest

testfile_path = os.path.realpath(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(testfile_path)))

from pycis import items
from pycis import wrappers


class ItemsTestCase(unittest.TestCase):

    def test_media_items_instantiantion(self):
        title = "The Animal Kingdom"
        url = "https://archive.org/details/Animal_Kingdom"
        media = items.Media(title=title, url=url)

        self.assertEqual(media.title, title)
        self.assertEqual(media.url, url)
        self.assertNotEqual(media.title, "wrong title")

    def test_media_items_has_children_method_returns_true_when_get_children_is_set(self):
        title = "The Animal Kingdom"
        url = "https://archive.org/details/Animal_Kingdom"
        get_children_func = lambda: "I have no children"
        media_with_children = items.Media(title=title, url=url, get_children=get_children_func)
        media_without_children = items.Media(title=title, url=url)

        self.assertFalse(media_without_children.has_children)
        self.assertTrue(media_with_children.has_children)

    def test_media_get_children(self):
        title = "The Animal Kingdom"
        url = "https://archive.org/details/Animal_Kingdom"
        children_media = [items.Media(None, None), items.Media(None, None)]
        get_children_func = lambda: children_media

        media = items.Media(title=title, url=url, get_children=get_children_func)

        self.assertEqual(media.get_children, get_children_func)
        self.assertEqual(media.get_children(), children_media)

    def test_media_str_representation(self):
        title = "The Animal Kingdom"
        url = "https://archive.org/details/Animal_Kingdom"
        media = items.Media(title=title, url=url)
        media_with_children = items.Media(title=title, url=url, get_children=lambda: "function")

        expected_str = 'Media(title="The Animal Kingdom", url="https://archive.org/details/Animal_Kingdom", has_children={})'
        self.assertEqual(str(media), expected_str.format(False))
        self.assertEqual(str(media_with_children), expected_str.format(True))


class Wrappers(unittest.TestCase):

    def test_get_wrapper_list_return_list(self):
        wrapper_list = wrappers.get_wrapper_list()
        self.assertIsInstance(wrapper_list, list)

if __name__ == "__main__":
    unittest.main()
