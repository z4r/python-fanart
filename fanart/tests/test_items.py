from unittest import TestCase
import os
from fanart.items import LeafItem, ResourceItem, CollectableItem
from httpretty import httprettified, HTTPretty
from fanart.tests import LOCALDIR


class LeafItemTestCase(TestCase):
    def setUp(self):
        self.leaf = LeafItem(id=11977, likes=2, url='http://test.tv/50x50.txt')

    def test_str(self):
        self.assertEqual(str(self.leaf), 'http://test.tv/50x50.txt')

    @httprettified
    def test_content(self):
        with open(os.path.join(LOCALDIR, 'response/50x50.png')) as fp:
            body = fp.read()
        HTTPretty.register_uri(
            HTTPretty.GET,
            'http://test.tv/50x50.txt',
            body=body
        )
        self.assertEqual(self.leaf.content(), body)
        self.assertEqual(len(HTTPretty.latest_requests), 1)
        self.assertEqual(self.leaf.content(), body)  # Cached
        self.assertEqual(len(HTTPretty.latest_requests), 1)


class ResourceItemTestCase(TestCase):
    def setUp(self):
        self.resource = ResourceItem()

    def test_from_dict(self):
        self.assertRaises(NotImplementedError, self.resource.from_dict, None)


class CollectableItemTestCase(TestCase):
    def setUp(self):
        self.collectable = CollectableItem()

    def test_from_dict(self):
        self.assertRaises(NotImplementedError, self.collectable.from_dict, None, None)
