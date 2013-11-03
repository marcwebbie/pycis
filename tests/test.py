import logging
import os
import sys
import unittest

testfile_path = os.path.realpath(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(testfile_path)))

from pycis import items
from pycis import extractors
from pycis import wrappers
from pycis.wrappers.base_wrapper import BaseWrapper


class ItemsTestCase(unittest.TestCase):

    def test_media_items_instantiantion(self):
        title = "The Animal Kingdom"
        url = "https://archive.org/details/Animal_Kingdom"
        media = items.Media(title=title, url=url)

        self.assertEqual(media.title, title)
        self.assertEqual(media.url, url)
        self.assertNotEqual(media.title, "wrong title")

    def test_media_str_representation(self):
        title = "The Animal Kingdom"
        url = "https://archive.org/details/Animal_Kingdom"
        media = items.Media(title=title, url=url)
        media_with_children = items.Media(title=title, url=url, has_children=True)

        expected_str = 'Media(title="The Animal Kingdom", url="https://archive.org/details/Animal_Kingdom", has_children={})'
        self.assertEqual(str(media), expected_str.format(False))
        self.assertEqual(str(media_with_children), expected_str.format(True))


class WrappersTestCase(unittest.TestCase):

    def setUp(self):
        self.tubeplus_wrapper = wrappers.get_wrapper("tubeplus")
        self.archive_wrapper = wrappers.get_wrapper("archive")

    def test_get_wrapper_list_return_list(self):
        wrapper_list = wrappers.get_wrapper_list()
        self.assertIsInstance(wrapper_list, list)

    def test_get_wrapper_list_return_list_doesnt_include_base_wrapper(self):
        from pycis.wrappers.base_wrapper import BaseWrapper

        wrapper_list = wrappers.get_wrapper_list()
        for wrapper in wrapper_list:
            self.assertNotEqual(wrapper.name, "base")

        self.assertEqual(wrappers.get_wrapper(name="base"), None)

    def test_get_wrapper_by_name_is_callable(self):
        self.assertTrue(callable(wrappers.get_wrapper))

    def test_archive_wrapper_search_return_media_list(self):
        self.assertIsInstance(self.archive_wrapper, BaseWrapper)
        media_list = self.archive_wrapper.search("the animal kingdom")

        self.assertIsInstance(media_list, list)

        for media in media_list:
            self.assertIsInstance(media, items.Media)

    def test_tubeplus_wrapper_search_returns_right_media(self):
        media_list = self.tubeplus_wrapper.search("Eat Pray Love")

        self.assertIsInstance(media_list, list)
        self.assertIn("Eat Pray Love", (m.title for m in media_list))

    def test_tubeplus_wrapper_get_streams_return_list(self):
        media_list = self.tubeplus_wrapper.search_film("Eat Pray Love")
        first_media = media_list[0]
        stream_list = self.tubeplus_wrapper.get_streams(first_media)
        self.assertIsInstance(stream_list, list)

    def test_tubeplus_wrapper_get_children(self):
        media_list = self.tubeplus_wrapper.search_tvshow("Vampire Diaries")
        first_media = media_list[0]

        children_list = self.tubeplus_wrapper.get_children(first_media)

        self.assertIsInstance(children_list, list)
        self.assertTrue(all(m for m in children_list if isinstance(m, items.Media)))


class ExtractorsTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_nowvideo_extractor(self):
        url = "http://www.nowvideo.sx/video/02452e9362f53"
        extractor = extractors.get_from_url(url)

        dlurl = extractor.get_raw_url(url)
        self.assertIsNot(dlurl, None)
        self.assertTrue("flv" in dlurl or "mp4" in dlurl)

    def test_divxstage_extractor(self):
        url = "http://www.divxstage.eu/video/v7f6bhbgvcbgw"
        extractor = extractors.get_from_url(url)

        dlurl = extractor.get_raw_url(url)
        self.assertIsNot(dlurl, None)
        self.assertTrue("flv" in dlurl or "mp4" in dlurl)

if __name__ == "__main__":
    unittest.main()
